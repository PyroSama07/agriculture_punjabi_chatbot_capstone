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

model_name = 'l3cube-pune/punjabi-sentence-similarity-sbert'
embeddings = HuggingFaceEmbeddings(model_name=model_name)
llm = ChatMistralAI(model="mistral-large-latest")

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["fruits", "vegetable", "rabi_crop","kharif_crop"] = Field(
        ...,
        description="Given a user question choose which datasource would be most relevant for answering their question",
    )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ਤੁਸੀਂ ਕਾਲ ਸੈਂਟਰ ਵਿੱਚ ਇੱਕ ਕਰਮਚਾਰੀ ਹੋ, ਆਪਣੇ ਖੁਦ ਦੇ ਗਿਆਨ ਤੋਂ ਸਵਾਲ ਦਾ ਜਵਾਬ ਪ੍ਰਦਾਨ ਕਰੋ, ਤੁਸੀਂ ਪ੍ਰਦਾਨ ਕੀਤੇ ਸੰਦਰਭ ਦੀ ਵਰਤੋਂ ਕਰ ਸਕਦੇ ਹੋ
            ਸੰਦਰਭ: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)

system = """You are an expert at routing a user question to the appropriate data source.
Based on the what whether the question is about fruits, vegetable or rabi or kharif crop; route it to the relevant data source."""

prompt_routing = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at routing a user question to the appropriate data source.
            Based on the what whether the question is about fruits, vegetable or rabi or kharif crop; route it to the relevant data source."""
        ),
        ("human", "{question}"),
    ]
)

def get_doc(path):
    f = open(path)
    sample_doc = f.read()
    f.close()
    sample_doc = sample_doc.replace('\n\n','#sentencesahikarnekeliyerandomvariable')
    sample_doc = sample_doc.replace('\n' ,'')
    sample_doc = sample_doc.replace('#sentencesahikarnekeliyerandomvariable','\n\n')
    return sample_doc

def get_retriever(persist_directory):
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={'k':1})
    return retriever

def router(query):
    structured_llm = llm.with_structured_output(RouteQuery)
    router = prompt_routing | structured_llm
    result = router.invoke({"question": query})
    return result.datasource.lower()

def create_rag_chain(retriever):
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

def create_vectorstores():
    fruits_doc = get_doc('../../ocr_code/data_books/ocr_punjabi/pp_fruits_pbi.txt')
    citrus_doc = get_doc('../../ocr_code/data_books/ocr_punjabi/Citrus_Cultivation_pbi.txt')
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = [fruits_doc,citrus_doc])
    
    persist_directory='../vectorstore/fruit'
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=embeddings,
                                        persist_directory=persist_directory)
    vectorstore.persist()
    
    sample_doc = get_doc('../../ocr_code/data_books/ocr_punjabi/pp_veg_pbi.txt')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = [sample_doc])
    
    persist_directory='../vectorstore/vegetable'
    vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=embeddings,
                                    persist_directory=persist_directory)
    vectorstore.persist()
    
    sample_doc = get_doc('../../ocr_code/data_books/ocr_punjabi/pp_kharif_pbi.txt')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = [sample_doc])
    
    persist_directory='../vectorstore/kharif'
    vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=embeddings,
                                    persist_directory=persist_directory)
    vectorstore.persist()
    
    sample_doc = get_doc('../../ocr_code/data_books/ocr_punjabi/pp_rabi_pbi.txt')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    splits = text_splitter.create_documents(texts = [sample_doc])
    
    persist_directory='../vectorstore/rabi'
    vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=embeddings,
                                    persist_directory=persist_directory)
    vectorstore.persist()

