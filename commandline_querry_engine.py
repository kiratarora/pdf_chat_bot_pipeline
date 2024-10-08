from retriever import Retriever
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import nltk

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

print(''' 
_____________________________________________________________________________________
        Instructions: 
                        Type 'q' or 'quit' to quit.
                        Type 'setup' if running the function for the first time.
_____________________________________________________________________________________
        
    ''')

def setup():
        nltk.download('punkt')
        nltk.download('stopwords')

chat_history = []
while True:
    user_input = input("User Input: ")
    if user_input == 'q' or user_input == 'Q' or user_input == 'quit' or user_input == 'Quit':
        break
    if user_input == 'setup' or user_input == 'Setup':
        print('downloading......')
        setup()
    chat_history.append("User Input: " + user_input)
    context = Retriever(['pdf','docx', 'doc', 'xltx', 'xltm', 'xlt', 'xlsx', 'xlsm', 'xls', 'csv'], path='data').get_context(user_input)
    text_context = context[0]
    table_context = context[1]
    # print('')
    # print(text_context)
    # print('')
    # print('')
    # print(table_context)
    # print('')
    AI_answer = chain.invoke({ "chat_history": chat_history, "input": user_input, "text_context":text_context, "table_context":table_context })
    print("AI Answer: "+ AI_answer)
    chat_history.append("AI Answer: " + AI_answer)
