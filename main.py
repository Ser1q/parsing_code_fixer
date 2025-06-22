import streamlit as st
from google import genai
from google.genai import types
from openai import OpenAI
import os
from dotenv import load_dotenv
from scraper import extract_body_content, clean_html_for_llm
### For scraping via ai-agent
# from smolagents import CodeAgent, LiteLLMModel
# from agent_tools import extract_body_content, clean_html_for_llm, scrape_website
# For local llm usage
# from models.deepseek import generate_function_iteratively, generate_prompt_for_deepseek 
# from codellama import get_html_differences

# loading api keys 
load_dotenv()
GEMINI_APIKEY = os.getenv("GEMINI_API_KEY")
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

st.title("AI Code Fixer 1.1")
html_old = st.text_area("Enter old HTML: ")
html_new = st.text_area("Enter new HTML: ")
if st.button("Get differences"):
    if (html_old or html_new) == "":
        st.write("Please enter HTMLs!")
    else:
        st.write("Analyzing...")

        ### Using AI-AGENT to scrape and clean webpage
        # scraping_agent = CodeAgent(
        #     model=LiteLLMModel(model_id="gemini/gemini-2.0-flash-lite", api_key=GEMINI_APIKEY),
        #     tools=[scrape_website, extract_body_content, clean_html_for_llm],
        #     additional_authorized_imports=["cloudscraper", "bs4"],
        # )
                
        # task = (
        #     "Your job is to process either a link or raw HTML string:\n"
        #     "1. If it is a link, use `scrape_website` to get HTML.\n"
        #     "2. Then use `extract_body_content` to extract <body> content.\n"
        #     "3. Then use `clean_html_for_llm` to clean the result.\n"
        #     "If it's raw HTML, skip step 1."
        # )        
        
        # prompt_old = f"""{task}
        # HTML:
        # {html_old}
        # """
        # prompt_new = f"""{task}
        # HTML:
        # {html_new}
        # """

        # cleaned_html_old = scraping_agent.run(prompt_old)
        # cleaned_html_new = scraping_agent.run(prompt_new)
        
        body_content_old = extract_body_content(html_old)
        body_content_new = extract_body_content(html_new)
        
        cleaned_html_old = clean_html_for_llm(body_content_old)
        cleaned_html_new = clean_html_for_llm(body_content_new)
        
        ### Using OPENAI_API_KEY
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        
        # Prompt to compare HTML versions
        prompt = f"""
        You are a helpful assistant specialized in analyzing changes in HTML structure.

        Please compare the following two HTML code snippets and list the differences.

        Requirements:
        1. Identify removed or changed tags and attributes.
        2. Identify newly added tags or attributes.
        3. Highlight class name or tag name replacements.
        4. Summarize key semantic or structural differences in a concise bullet list.

        Old HTML:
        ```html
        {cleaned_html_old}
        ```
        New HTML:
        ```html
        {cleaned_html_new}
        ```
        """
        
        # Configure the model
        config = types.GenerateContentConfig(
            system_instruction=(
            "You are a senior frontend developer and HTML structure expert."
            "You analyze HTML changes and output a structured summary of edits."
            "Always be concise and use bullet points for readability."
            ),
            temperature=0.1,
            max_output_tokens=1024
        )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt,
            config=config
        )

        result = response.text
        print("Result: ", result)
        
        ### Using local LLM
        # result = get_html_differences(cleaned_html_old, cleaned_html_new)

        st.session_state.html_differences = result

        
        with st.expander("View HTML differences"):
            st.text_area("HTML content", result, height=300)

old_code = st.text_area("Enter old code: ", height=150)

if st.button("Fix code"):
    
    ### Using OPENAI_API_KEY
    if "html_differences" in st.session_state and old_code is not None:
        st.write("Writing Code...")
        
        client = OpenAI()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior Python developer specializing in HTML parsing."
                    "Your job is to fix broken Python code that parses HTML based on updated HTML structure."
                    "Always return only updated Python code inside one markdown code block. Do not explain."
                )
            },
            {
                "role": "user",
                "content": f"""
                    Here is a description of how the HTML structure has changed:
                    {st.session_state.html_differences}

                    Here is the old Python code:
                    ```python
                    {old_code}
                    ```
                    Please return the fixed version of the Python code.
            """
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4.1",  
            messages=messages,
            temperature=0.2
        )
        print("Response: \n", response)
        
        result = response.choices[0].message.content
        print("Result: \n", result)

        print("\n🟩 Final Generated Code:\n")
        print(result)    
        st.write("\n🟩 Final Generated Code:\n")
        st.write(result)
    else:
        st.write("Please enter correct inputs!")
        
    ### Using local LLM
    
    # if "html_differences" in st.session_state and old_code is not None:
    #     st.write("Writing Code...")
    #     prompt = generate_prompt_for_deepseek(old_code=old_code, changed_html=st.session_state.html_content)
        
    #     result = generate_function_iteratively(prompt=prompt)
    #     print(result.strip())

    #     print("\n🟩 Final Generated Code:\n")
    #     print(result)    
    #     st.write("\n🟩 Final Generated Code:\n")
    #     st.write(result)
    # else:
    #     st.write("Please enter old code!")
