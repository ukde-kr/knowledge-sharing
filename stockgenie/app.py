from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langgraph.checkpoint.memory import MemorySaver
from tools import fetch_holding_price, fetch_market_price, search_news, get_prompt

# Load environment variables
load_dotenv(".env")
api_key = os.getenv("OPENAI_API_KEY")

# Initialize model and checkpointer
model = ChatOpenAI(api_key=api_key, model="gpt-4o")
checkpointer = MemorySaver()

# Tools
inventory_search_tool = Tool(
    name="inventory_search",
    description="Search client investment inventory to find holding value and number of units information with ticker name",
    func=fetch_holding_price
)

market_price_tool = Tool(
    name="market_price",
    description="Get market price of ticker",
    func=fetch_market_price
)

news_search_tool = Tool(
    name="news_search",
    description="Search stored news about a company name.",
    func=search_news
)

# AgentState
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# Agent class
class Agent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(getattr(result, "tool_calls", [])) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        return {'messages': results}

# Recursive message extractor
def extract_messages(result):
    msgs = []
    if isinstance(result, dict):
        for val in result.values():
            if isinstance(val, list):
                for item in val:
                    if hasattr(item, 'content') or hasattr(item, 'tool_calls'):
                        msgs.append(item)
                    elif isinstance(item, dict):
                        msgs.extend(extract_messages(item))
            elif isinstance(val, dict):
                msgs.extend(extract_messages(val))
    return msgs

# Initialize agent
abot = Agent(
    model,
    [inventory_search_tool, market_price_tool, news_search_tool],
    checkpointer=checkpointer,
    system=get_prompt("STOCK_GENIE_SYSTEM_PROMPT")
)

# Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def chat():
    answer = ""
    functions = []
    if request.method == "POST":
        question = request.form.get("question", "")
        if question:
            messages = [HumanMessage(content=question)]
            thread = {"configurable": {"thread_id": "local"}}

            result = abot.graph.invoke({"messages": messages}, thread)
            all_msgs = extract_messages(result)
            for msg in all_msgs:
                if isinstance(msg, ToolMessage):
                    functions.append({"name": msg.name, "args": getattr(msg, "args", {})})
                if isinstance(msg, AIMessage):
                    answer = msg.content

            print("Functions:", functions)
            print("Answer:", answer)

    return render_template("chat.html", answer=answer, functions=functions)

if __name__ == "__main__":
    app.run(debug=True)
