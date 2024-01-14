import os
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = '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'  # Replace 'your-api-key' with your actual API key

def load_and_process_document(file_name):
    name, extension = os.path.splitext(file_name)

    if extension == '.pdf':
        loader = PyPDFLoader(file_name)
    elif extension == '.docx':
        loader = Docx2txtLoader(file_name)
    elif extension == '.txt':
        loader = TextLoader(file_name)
    else:
        raise ValueError('Document format is not supported!')

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(chunks, embeddings)

    return vector_store

def create_conversational_retrieval_chain(vector_store):
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    retriever = vector_store.as_retriever()
    crc = ConversationalRetrievalChain.from_llm(llm, retriever)
    return crc

#btn2
def generate_qa_from_document(file_path, question):
    vector_store = load_and_process_document(file_path)
    crc = create_conversational_retrieval_chain(vector_store)

    history = []
    response = crc.run({'question': question, 'chat_history': history})
    history.append((question, response))

    return response

#btn1
def generate_insight_from_document(file_path, question):
    vector_store = load_and_process_document(file_path)
    crc = create_conversational_retrieval_chain(vector_store)

    history = []
    response = crc.run({'question': question, 'chat_history': history})
    history.append((question, response))

    return response





# # Example usage
file_name = "C:/Users/ghaia/Desktop/courses/OS2/pro2 (os2)/Report on Addressing the Readers.pdf"  # Replace with your document's path
question = 'generate 10 questions and answers about the topics in this document'
# # question = 'give me insight for this document'
response = generate_qa_from_document(file_name, question)

print("Question:", question)
print("Answer:", response)
