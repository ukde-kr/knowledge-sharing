![status: under development](https://img.shields.io/badge/status-under%20development-yellow.svg)

<br/>
<div align="center">
    <h3 align="center">LangChain for LLM Application Development</h3>
    <p align="center">
        The folder aims to bring the notebooks up to date with the latest LangChain library, ensuring all code runs without deprecated functions. A subset of the notebooks has been successfully updated and is fully operational, while work on the remaining notebooks is ongoing.
        <br/>
    </p>
</div>

<br/>

### Disclaimer

This collection of Jupyter notebooks is from the DeepLearning.AI course, [LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/). These notebooks are a personal learning record and are not a substitute for the official course materials. All intellectual property and copyright remain with DeepLearning.AI. I am not affiliated with or endorsed by DeepLearning.AI.

<details>
    <summary>Table of Contents</summary>
    <ul>
        <li><a href="L1-Model_prompt_parser.ipynb">Models, Prompts, and parsers</a></li>
        <li><a href="L2-Memory.ipynb">Memory</a></li>
        <li><a href="L3-Chains.ipynb">Chains</a></li>
        <li><a href="L4-QnA.ipynb">Question and Answer</a></li>
        <li><a href="L5-Evaluation.ipynb">Evaluation</a></li>
        <li><a href="L6-Agents.ipynb">Agents</a></li>
</details>

<br/>

### About the Course

The course was taught by Andrew Ng and Harrison Chase, the creator of the LangChain framework. It provides an excellent introduction to building applications with large language models (LLMs) and covers core concepts, including:
- Using models, prompts, and parsers
- Implementing memory in conversational applications
- Building chains to link multiple components
- Retrieval-Augmented Generation (RAG) for question answering with custom data
- Utilising agents to give LLMs access to external tools.

### Getting Started

*Prerequisites*:
- Python (3.9+)
- An [OpenAI API key](https://platform.openai.com/api-keys) or another compatible LLM API key

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
