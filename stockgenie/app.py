from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import logging
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import ToolMessage
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel
from tools import fetch_holding_price, get_prompt, fetch_market_price
from langchain.tools import Tool

model = ChatOpenAI(model="gpt-4o")

from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

load_dotenv()
OPEN_API_KEY = os.getenv("OPENAI_API_KEY")

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

price_tool = Tool(
    name="holding_price",
    description ="Get holding price",
    func=fetch_holding_price
)

market_price_tool = Tool(
    name="market_price",
    description ="Get market price",
    func=fetch_market_price
)

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
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            print('tool call done------')
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}
    
abot = Agent(model, [fetch_holding_price,fetch_market_price], system=get_prompt("STOCK_GENIE_SYSTEM_PROMPT"), checkpointer=checkpointer)

messages = [HumanMessage(content="what is recommendation of APPL?")]
thread = {"configurable": {"thread_id": "1"}}
for event in abot.graph.stream({"messages": messages}, thread):
    for v in event.values():
        print(v)