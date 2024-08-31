import os
import chromadb
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders import PyMuPDFLoader

def set_environment_variables(open_ai_key, langchain_key):
    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ['LANGCHAIN_API_KEY'] = langchain_key
    os.environ['OPENAI_API_KEY'] = open_ai_key

def initialize_rag(document_path:str, 
                   open_ai_key:str, 
                   lang_chain_key:str, 
                   chunk_size:int=1000, 
                   chunk_ovelap:int=200, 
                   collection_name:str="crop-disease-collection", 
                   data_persistence_path:str="chroma_db/", 
                   prompt:str="rlm/rag-prompt", 
                   embedding_model_name:str="gpt-3.5-turbo", 
                   embedding_model_temprature:int=0):
    # Document Loader from PDF
    doc_path = document_path
    docs = PyMuPDFLoader(doc_path).load()
    # Document Chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_ovelap)
    splits = text_splitter.split_documents(docs)

    # Chroma DB Local persistent client and retriever initialization
    client = chromadb.PersistentClient(path=data_persistence_path)
    collection = client.get_or_create_collection(collection_name)
    vector_store_from_client = Chroma.from_documents(
        documents=splits,
        client=client,
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(),
    )
    retriever = vector_store_from_client.as_retriever()
    # Prompt and LLM Initialization
    prompt = hub.pull(prompt)
    Open_AI_Model = ChatOpenAI(model_name=embedding_model_name, temperature=embedding_model_temprature)
    # Create an RAG chain for the document retrieval process
    rag_chain = (
        {"context": retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)), "question": RunnablePassthrough()} # Retriever | Pre-processing (Joining retrieved docs)
        | prompt
        | Open_AI_Model
        | StrOutputParser()
    )
    return rag_chain

def get_rag_answer(rag_chain, question:str):
    return rag_chain.invoke(question)