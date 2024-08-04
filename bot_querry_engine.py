from retriever import Retriever
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
output_parser = StrOutputParser()
llm = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Continue the conversation based on the chat history and context and table provided."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "{text_context}"),
        ("user", "{table_context}")
    ])
# MessagesPlaceholder(variable_name="context"),
chain = prompt | llm | output_parser

retriever = Retriever(['pdf','docx', 'doc', 'xltx', 'xltm', 'xlt', 'xlsx', 'xlsm', 'xls', 'csv'], path='data')

def querry_eingine_upload_file(file_name):
    retriever.process_single_file(file_name)

def get_pdf_answers(reload, user_input, chat_history):
    context = retriever.get_context(user_input)
    text_context = context[0]
    table_context = context[1]
    AI_answer = chain.invoke({ "chat_history": chat_history, "input": user_input, "text_context":text_context, "table_context":table_context })
    return AI_answer
