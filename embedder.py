from InstructorEmbedding import INSTRUCTOR


'''
Class that uses hungging face's instructor model to implement custom embedding.
'''
class Embedder():

    '''
    Constructor for the class

    Parameters:
        instructor_model_name (str): name of the model to be used
        instruction (str): special instructions to use while embedding the querry and instructions
    '''
    
    def __init__(self, instructor_model_name: str = 'hkunlp/instructor-large', instruction: str = '') -> None:
        self.model = INSTRUCTOR(instructor_model_name)
        self.instruction = instruction
    '''
    Function to embedd a querry
    
    Parameters:
        querry (str): user provided querry.
    Returns:
        list of floats: the embedded vector
    '''
    
    def get_query_embedding(self,query:str) -> list[float]:
        return self.model.encode([[self.instruction,query]])[0].tolist()
    '''
    Function to embedd chunked text
    
    Parameters:
        text (str): single chunk
    Returns:
        list of floats: the embedded vector
    '''
    
    def get_text_embedding(self,text:str) -> list[float]:
        return self.model.encode([[self.instruction,text]])[0].tolist()
    '''
    Function to embedd a list of chunked text
    
    Parameters:
        texts (list of str): chunks
    Returns:
        list of list of floats: list of the embedded vectors
    '''
    def get_text_embedding(self,texts:list[str]) -> list[list[float]]:
        return self.model.encode([[self.instruction,text] for text in texts]).tolist()



