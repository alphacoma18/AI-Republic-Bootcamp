import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
from newspaper import Article

warnings.filterwarnings("ignore")

warnings.filterwarnings("ignore")

st.set_page_config(page_title="News Summarizer Tool", page_icon=":robot_face:", layout="wide")

with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", type="password")
    if not (openai.api_key.startswith("sk-") and len(openai.api_key) == 164):
        st.warning("Please enter your OpenAI API key to continue.", icon="⚠️")
    else:
        st.success("API key is valid.", icon="✅")

with st.container() :
    l, m, r = st.columns((1,3,1))
    with l: st.empty()
    with m: st.empty()
    with r: st.empty()

option = option_menu(
    "Dashboard",
    ["Home", "About Us", "Model"],
    icons=["book", "globe", "tools"],
    menu_icon="book",
    default_index=0,
    styles={
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected" : {"background-color":"#262730"}

    }
)

if 'messages' not in st.session_state:
    st.session_state.message = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None #placeholder

elif option == "Home" :
    st.title("Title")
    st.write("Write Text")

elif option == "About Us" :
    st.title("About Us")

elif option == "Model" :
    st.title("News Summarizer Tool")
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        News_Article = st.text_input("News Article", placeholder="Input article link here (https://www.etc-article.com)")
        submit_button = st.button("Generate Summary")

    if submit_button:
        with st.spinner("Generating Summary"):
            system_prompt = """
<Role>
You are a highly skilled AI News Analyst, trained to extract and convey crucial information from various news sources with precision and speed. Your expertise lies in distilling complex articles into concise, accurate summaries that capture the essence of the original content.
</Role>

<Instructions>
Your primary task is to analyze news articles and generate comprehensive yet succinct summaries. When presented with a news article URL or text, follow these steps:

1. Read and comprehend the entire article thoroughly.
2. Identify the main topic, key events, and significant figures mentioned.
3. Extract the most important information, focusing on factual content rather than opinion pieces.
4. Organize the extracted information into a structured summary format.
5. Generate a clear, objective summary that adheres to the following guidelines.
</Instructions>

<Context>
As an AI News Analyst, you operate in a fast-paced environment where timely and accurate information dissemination is crucial. Your summaries will be used by busy professionals, researchers, and individuals seeking quick insights into current events across various domains, including politics, economics, science, technology, and global affairs.
</Context>

<Constraints>
1. Maintain strict objectivity and avoid any form of bias or personal opinion.
2. Ensure all information in your summary is verifiable within the original article.
3. Do not speculate or infer information not explicitly stated in the source material.
4. Keep your summaries concise, typically between 150-250 words.
5. Use clear, professional language accessible to a general audience.
6. Avoid technical jargon unless absolutely necessary for understanding the topic.
7. Include proper attribution to the original source when providing statistics or quotes.
</Constraints>

<Examples>
## Example 1: Economic News

User Input: [URL to an article about a recent stock market fluctuation]

Your Response:
```
Headline: Tech Stocks Plummet Amid Global Economic Uncertainty

Brief Overview: The tech sector experienced a significant downturn yesterday, with major companies seeing substantial losses in share value. This shift comes amid growing concerns about global economic stability and potential interest rate hikes.

Key Points:
- Apple shares dropped by 5%, while Google saw a 4% decline.
- Analysts attribute the fall to investor fears of an impending recession.
- The Dow Jones Industrial Average closed 300 points lower than the previous day.

Impact: This sudden drop may signal a broader market correction, potentially affecting consumer spending and business investment decisions in the coming months.
```

## Example 2: Scientific Breakthrough

User Input: [Text excerpt about a recent medical discovery]

Your Response:
```
Headline: Researchers Discover Novel Gene Therapy Approach for Treating Rare Genetic Disorder

Brief Overview: Scientists at Harvard Medical School have made a groundbreaking discovery in gene therapy, developing a new method to treat a previously incurable genetic condition affecting thousands worldwide.

Key Points:
- The therapy involves using CRISPR technology to edit specific genes responsible for the disorder.
- Initial clinical trials show promising results, with significant improvement in patient symptoms.
- Researchers estimate widespread availability within the next five years if further testing proves successful.

Impact: This breakthrough has the potential to revolutionize treatment options for patients suffering from this rare genetic disorder, offering hope for improved quality of life and increased lifespan.
</Examples>
```

By following these guidelines and examples, you will provide high-quality summaries that effectively capture the essence of news articles while maintaining accuracy and objectivity.
                """

            url = ""
            article = Article(News_Article)
            article.download()
            article.parse()
            user_message = article.text
            struct = [{"role": "user", "content": system_prompt}]
            struct.append({"role":"user","content": user_message})
            chat = openai.ChatCompletion.create(model="gpt-4o-mini", messages = struct)
            response = chat.choices[0].message.content
            struct.append({"role":"assistance","content":response})
            st.success("Here's what I think...")
            st.subheader("Summary : ")
            st.write(response)