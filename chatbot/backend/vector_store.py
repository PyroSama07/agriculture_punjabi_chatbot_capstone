import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import utils

model_name = 'l3cube-pune/punjabi-sentence-similarity-sbert'
embeddings = HuggingFaceEmbeddings(model_name=model_name)

path = "../../ocr_code/data_books/rag_docs/"

def fruit():
    docs = []
    for doc in os.listdir(path+'fruit'):
        docs.append(utils.get_doc(path+'fruit/'+doc))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = docs)
    
    persist_directory='../vectorstore/fruit'
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=embeddings,
                                        persist_directory=persist_directory)
    vectorstore.persist()

def vegetable():
    docs = []
    for doc in os.listdir(path+'vegetable'):
        docs.append(utils.get_doc(path+'vegetable/'+doc))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = docs)
    
    persist_directory='../vectorstore/vegetable'
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=embeddings,
                                        persist_directory=persist_directory)
    vectorstore.persist()

def rabi():
    docs = []
    for doc in os.listdir(path+'rabi'):
        docs.append(utils.get_doc(path+'rabi/'+doc))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = docs)
    
    persist_directory='../vectorstore/rabi'
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=embeddings,
                                        persist_directory=persist_directory)
    vectorstore.persist()

def kharif():
    docs = []
    for doc in os.listdir(path+'kharif'):
        docs.append(utils.get_doc(path+'kharif/'+doc))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = docs)
    
    persist_directory='../vectorstore/kharif'
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=embeddings,
                                        persist_directory=persist_directory)
    vectorstore.persist()
