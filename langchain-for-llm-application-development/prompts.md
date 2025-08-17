![status: under development](https://img.shields.io/badge/status-under%20development-yellow.svg)

### LLM-Assisted Error Resolution Log

This log shows how an LLM can help a beginner debug and update the course notebooks, ensuring the code works with the latest packages.

<a name="toc-top"></a>
<details>
    <summary>Table of Contents</summary>
    <ul>
        <li><a href="#api-error">API Error</a></li>
        <li>
          <a href="#class-deprecation-warning">Class Deprecation Warning</a>
          <ol>
            <li><a href="#class-deprecation-warning-1">Example 1</a></li>
            <li><a href="#class-deprecation-warning-2">Example 2</a></li>
          </ol>
        </li>
        <li><a href="#type-and-attribute-errors">Incorrect Object and Method Usage</a></li>
</details>

<br/>

<a name="api-error"></a>
> API Error

**Error type**:
`APIRemovedInV1`

**Description**:

The error is a custom alert from the OpenAI Python library. It means your code is trying to use an outdated function, `openai.ChatCompletion`, that was removed in the library's v1.0.0 update.

**Full Error message**:

{
  APIRemovedInV1:

You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0 - see the README at https://github.com/openai/openai-python for the API.

You can run openai migrate to automatically upgrade your codebase to use the 1.0.0 interface.

Alternatively, you can pin your installation to the old version, e.g. pip install openai==0.28

A detailed migration guide is available here: https://github.com/openai/openai-python/discussions/742
}

**Full LLM answer**:
{
  The error means your code is calling the removed v0.x API (openai.ChatCompletion). Fix it by either migrating to the new openai v1 client, or pinning openai to the old version.

Files:

L1-Model_prompt_parser.ipynb — notebook with get_completion
.env

Options

1. Migrate to the new OpenAI client (recommended). Replace the import + function in L1-Model_prompt_parser.ipynb as shown:
```python
# ...existing code...
import os
from openai import OpenAI

# create new client (uses OPENAI_API_KEY from .env)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    # return content from the first choice
    return response.choices[0].message["content"]
# ...existing code...
```

2. Pin to the old API (quick workaround). Run:
```python
pip install openai==0.28
```

Notes:

If you migrate, you may also update other call sites where openai.ChatCompletion was used.
For migration guidance see the OpenAI repo/discussion: https://github.com/openai/openai-python/discussions/742.
}


<p align="right">(<a href="#toc-top">back to top</a>)</p>
</br>

<a name="#class-deprecation-warning"></a>
> Class Deprecation Warning

**Error code**:
`LangChainDeprecationWarning`

**Description**:

Getting a deprecation message from the library developers is common in Python. The warning is not a bug. It's telling you that a function or class you're using is outdated and will be removed in a future version. This gives you time to update your code without it suddenly breaking.

<a name="#class-deprecation-warning-1"></a>
#### Example 1

**Full Error message**:
{
  LangChainDeprecationWarning: The class ChatOpenAI was deprecated in LangChain 0.0.10 and will be removed in 1.0. An updated version of the class exists in the :class:~langchain-openai package and should be used instead. To use it run pip install -U :class:~langchain-openai and import as from :class:~langchain_openai import ChatOpenAI``.
chat = ChatOpenAI(temperature=0.0, model=llm_model)
ChatOpenAI(client=<openai.resources.chat.completions.completions.Completions object at 0x000001DB581A16D0>, async_client=<openai.resources.chat.completions.completions.AsyncCompletions object at 0x000001DB581A1F70>, temperature=0.0, model_kwargs={}, openai_api_key='sk-{"my_api_key"}', openai_proxy='')
}

**Full LLM answer**:
{
  Install the new adapter and update the import — short steps:
  1. In Git Bash (venv active)
  ```bash
  source .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install --upgrade langchain-openai langchain
# restart the notebook kernel after install
```

2. Replace the langchain import in your notebook with the new package import. Example patch:
```python
# ...existing code...
# old (deprecated)
# from langchain.chat_models import ChatOpenAI

# new
from langchain_openai import ChatOpenAI

# use same construction
chat = ChatOpenAI(temperature=0.0, model=llm_model)
# ...existing code...
```

3. Restart the kernel and re-run the cells.
Security note (short): I saw your API key printed in output earlier — if that key was exposed, rotate it on https://platform.openai.com/account/api-keys and remove it from any committed files.
}


<p align="right">(<a href="#toc-top">back to top</a>)</p>
</br>

<a name="#class-deprecation-warning-2"></a>
#### Example 2

**Full Error message**:
{
  LangChainDeprecationWarning: The method BaseChatModel.__call__ was deprecated in langchain-core 0.1.7 and will be removed in 1.0. Use :meth:~invoke instead.
customer_response = chat(customer_messages)
}

**Full LLM answer**:
{
Use the new invoke API instead of calling the chat object. Replace the cell that does customer_response = chat(customer_messages) with an invoke call and robust extraction of the response text.

```python
# ...existing code...
# Call the LLM to translate to the style of the customer message
# (use invoke instead of the deprecated __call__)
customer_response = chat.invoke(customer_messages)

# Safely get the generated text (try common shapes)
try:
    # some adapters provide a .content property
    print(customer_response.content)
except Exception:
    try:
        # LangChain result often has .generations -> list[list[Generation]]
        print(customer_response.generations[0][0].text)
    except Exception:
        # fallback: inspect the object
        print(repr(customer_response))
# ...existing code...
```
After editing, restart the notebook kernel and re-run the cells. If you still see a warning or different return shape, paste the new traceback/output and I’ll adjust the extraction.
}


<p align="right">(<a href="#toc-top">back to top</a>)</p>
</br>

### Using an LLM to Understand an Intentional Error

Throughout the tutorials, an LLM can also help a learner better understand the details of an intentional error.

<a name="#type-and-attribute-errors"></a>
> Incorrect Object and Method Usage

**Abstracted Error**:
`TypeError: 'ChatCompletionMessage' object is not subscriptable & AttributeError: 'str' object has no attribute 'get'`

**Summary of LLM Advice**:

The API's response object had changed. The original notebooks attempted to access the message content using dictionary-style bracket notation (e.g., `['content']`), but the new API returns a ChatCompletionMessage object. The LLM recommended accessing the content using dot notation (e.g., `response.choices[0].message.content`). It also clarified that `response.content` returns a string, so methods like `.get()` are not applicable, and a proper parser or dictionary conversion is necessary to access nested information.


<p align="right">(<a href="#toc-top">back to top</a>)</p>


----
*This log was created with the assistance of Gemini 2.5 Flash, which compiled the solutions originally provided by GPT-5 mini.*