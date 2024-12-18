from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

model_name = 'l3cube-pune/punjabi-sentence-similarity-sbert'
embeddings = HuggingFaceEmbeddings(
    model_name=model_name  # Provide the pre-trained model's path
    # model_kwargs=model_kwargs, # Pass the model configuration options
    # encode_kwargs=encode_kwargs # Pass the encoding options
)

print(embeddings)