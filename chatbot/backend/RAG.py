from dotenv import load_dotenv
load_dotenv()

from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_mistralai import ChatMistralAI
from typing import Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableLambda
from langchain.chains import RetrievalQA
import time 
import utils

import warnings
warnings.filterwarnings("ignore")

model_name = 'l3cube-pune/punjabi-sentence-similarity-sbert'
embeddings = HuggingFaceEmbeddings(model_name=model_name)

fruit_retriever = utils.get_retriever('../vectorstore/fruit/')
vegetable_retriever = utils.get_retriever('../vectorstore/vegetable/')
rabi_retriever = utils.get_retriever('../vectorstore/rabi/')
kharif_retriever = utils.get_retriever('../vectorstore/kharif/')

query=input("Enter Question:\n")
domain = utils.router(query)
if "fruits" in domain:
    rag_chain = utils.create_rag_chain(fruit_retriever)
elif "vegetable" in domain:
    rag_chain = utils.create_rag_chain(vegetable_retriever)
elif "rabi" in domain:
    rag_chain = utils.create_rag_chain(rabi_retriever)
else:
    rag_chain = utils.create_rag_chain(kharif_retriever)
print(domain)
time.sleep(1)
print('-'*20)
print(rag_chain.invoke(query))