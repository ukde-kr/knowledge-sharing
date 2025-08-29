![status: under development](https://img.shields.io/badge/status-under%20development-yellow.svg)

<br/>
<div align="center">
    <h3 align="center">AI Agent in LangGraph</h3>
    <p align="center">
        The folder aims to bring the notebooks up to date with the latest LangChain library, ensuring all code runs without deprecated functions. The process of updating these notebooks, including the replacement of deprecated functions and refactoring, was conducted with the assistance of a large language model (GPT-5 mini). This approach demonstrates the practical application of LLM-powered tools in development workflows. A subset of the notebooks has been successfully updated and is fully operational, while work on the remaining notebooks is ongoing.
        <br/>
    </p>
</div>

<br/>

### Disclaimer

This collection of Jupyter notebooks is from the DeepLearning.AI course, [AI Agent in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/). These notebooks are a personal learning record and are not a substitute for the official course materials. All intellectual property and copyright remain with DeepLearning.AI. I am not affiliated with or endorsed by DeepLearning.AI.

<details>
    <summary>Table of Contents</summary>
    <ul>
        <li><a href="Lesson_1_Student.ipynb">Built an Agent from Scratch</a></li>
        <li><a href="Lesson_2_Student.ipynb">LangGraph components</a></li>
        <li><a href="Lesson_3_Student.ipynb">Agentic Search Tools</a></li>
        <li><a href="Lesson_4_Student.ipynb">Persistence and Streaming</a></li>
        <li><a href="Lesson_5_Student.ipynb">Human in the loop</a></li>
        <li><a href="Lesson_6_Student.ipynb">Essay Writer</a></li>
</details>

<br/>

### About the Course

The course was taught by Andrew Ng and Harrison Chase, the creator of the LangChain framework... (course summary to be updated).

### Getting Started

*Prerequisites*:
- Python (3.9+)
- An [OpenAI API key](https://platform.openai.com/api-keys) or another compatible LLM API key
- Optional: VS Code with Copilot (or another LLM-powered IDE such as Cursor)

*NB* - Your API key should not be shared. If exposed, rotate it immediately at https://platform.openai.com/account/api-keys

</br>

To run these notebooks locally, you will need to set up a suitable Python environment.

1. Clone the repository and navigate into this folder:
```bash
git clone https://github.com/ukde-kr/knowledge-sharing.git
cd langchain-for-llm-application-development
```

2. Install packages in a virtual environment using pip and venv:
- See the official instructions for [details](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the folder and add your API key:
```
OPENAI_API_KEY="your_api_key_here"
```