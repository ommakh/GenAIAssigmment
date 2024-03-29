import langchain
from langchain.llms import GooglePalm
from langchain.schema import document
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
import langchain_community
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


api_key = 'AIzaSyArZsaHMMlPwCd6h_YVhdZQQMGk2g5fZgs'
print("we are good...")

llm = GooglePalm(google_api_key=api_key)


from langchain.document_loaders.csv_loader import CSVLoader

from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS

instructor_embeddings = HuggingFaceInstructEmbeddings()
vectordb_file_path = "vector3"


def create_vector_db():
    from langchain_community.document_loaders import PyPDFLoader

    loader = PyPDFLoader(file_path='48lawsofpower.pdf' )
    datx = loader.load()


    print(datx)
    vectordb = FAISS.from_documents(documents=datx, embedding=instructor_embeddings)
    vectordb.save_local("vector3")





def get_chain():
    vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)
    retrival = vectordb.as_retriever(score_threshold=0.3)
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
       In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
       If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

       CONTEXT: {context}

       QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retrival,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain


if __name__ == "__main__":
    create_vector_db()
    chain = get_chain()
    print(chain(""))
