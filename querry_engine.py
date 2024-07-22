from retriever import Retriever

while True:
    user_input = input("User Inputquit: ")
    if user_input == 'q' or user_input == 'Q' or user_input == 'quit' or user_input == 'Quit':
        break
    context = Retriever(['pdf','docx'], path='data').get_context(user_input)
    
