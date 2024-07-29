import os, math
from vertor_store import Vector_Store 

'''
Class that gets the best context from the vector store for the provided querry
'''
class Retriever():

    '''
    Constructor for this class

    Parameters:
        extentions (list of strings): this is a list of the valid extentions that can be processed
        path (str): path of the directory where all the files exist. 
    '''
    def __init__(self, extentions: list[str], path: str) -> None:
        all_files = os.listdir(path)
        self.files = [path+'/'+file for file in all_files if file.split('.')[-1] in extentions]
        self.vector = Vector_Store(self.files)
        self.vector_store = self.vector.get_vector_store()
        self.vector_store_text = self._get_text_store()
        self.vector_store_table = self._get_table_store()         

    '''
    PRIVATE: this function is used to get the text embeddings in the vectore store

    Returns:
        dict: dictionary of embeddings
    '''
    def _get_text_store(self) -> dict:
        try:
            vector_store_text = self.vector.get_vector_store()['text']
        except KeyError:
            vector_store_text = {}
        return vector_store_text
    
    '''
    PRIVATE: this function is used to get the table embeddings in the vectore store

    Returns:
        dict: dictionary of embeddings
    '''
    def _get_table_store(self) -> dict:
        try:
            vector_store_text = self.vector.get_vector_store()['table']
        except KeyError:
            vector_store_text = {}
        return vector_store_text

    '''
    The main function that processes all the files, and the querry. The code then finds the best matching text and table contexts and returns a tuple of the best context and table. 

    Parameters 
        querry (str): Embedds this querry to process and find the best avaialble context. 
        distance_cutoff (float): This is used to make sure that only the relavant contexts are passed on to the querry engine.
    
    Returns:
        tuple:
            str: The best text context based on the querry
            n-D list: The best table based on the querry
    '''
    def get_context(self,querry: str, distance_cutoff: float = 0.4) -> tuple[str,list[list]]:
        # Processing the files to get the data
        self._process_files()
        embedded_querry = self._get_query_embedding(querry)
        self.vector_store_text = self._get_text_store()
        self.vector_store_table = self._get_table_store() 
        
        closest_matching_contex = {}

        for doc in self.vector_store_text:
            best_context, best_context_value, best_context_vector = '', math.inf, None
            for context in self.vector_store_text[doc]:
                vector_compare_score = self._vector_compare(self.vector_store_text[doc][context], embedded_querry)
                if vector_compare_score < best_context_value:
                    best_context_value, best_context, best_context_vector = vector_compare_score, context, self.vector_store_text[doc][context]
            if best_context_vector != None:
                closest_matching_contex[doc] = (best_context, best_context_vector)
        
        closest_matching_table ={}
        
        for table in self.vector_store_table:
            best_context, best_context_value, best_context_vector = '', math.inf, None
            for context in self.vector_store_table[table]:
                vector_compare_score = self._vector_compare(self.vector_store_table[table][context], embedded_querry)
                if vector_compare_score < best_context_value:
                    best_context_value, best_context, best_context_vector = vector_compare_score, context, self.vector_store_table[table][context]
            if best_context_vector != None:
                closest_matching_table[table] = (best_context, best_context_vector )

        # Use best contexts to find the similarity
        final_value, final_context = math.inf, ''
        for i in closest_matching_contex:
            comp = self._vector_compare(closest_matching_contex[i][1], embedded_querry)
            if final_value > comp and distance_cutoff > comp:
                final_value = comp
                final_context = closest_matching_contex[i][0]
        
        final_table_value, final_table = math.inf, ''
        for i in closest_matching_table:
            comp = self._vector_compare(closest_matching_table[i][1], embedded_querry)
            if final_table_value > comp and distance_cutoff > comp:
                final_table_value = comp
                final_table = closest_matching_table[i][0]

        return (final_context, final_table)

    '''
    PRIVATE: function used to compare the disance between 2 vectors. 

    Parameters:
        context_vector (list of floats): embedding vector.
        querry_vector (list of floats): embedding vector.
    
    Returns:
        float: Euclidean distance between the 2 vectors. 
    '''
    def _vector_compare(self,context_vector: list[float], querry_vector: list[float]) -> float:
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(context_vector, querry_vector)))  

    '''
    PRIVATE: Uses the vector_store file to process the files in the given files path
    
    Returns:
        str: Confirmation that the file processing was completed.
    '''
    def _process_files(self) -> str:
        return self.vector.process_files()
         
    '''
    Uses the vector_store file to process a single file
    
    Parameters:
        file_name (str): name of the file
    
    Returns:
        str: Confirmation that the file processing was completed.
    '''
    def process_single_file(self, file_name: str) -> str:
        return self.vector.add_sigle_file(file_name)

    '''
    PRIVATE: funtion that uses the vector_store file to embed the querry
    
    Parameters:
        string (str): user defined querry. 
    
    Returns:
        list of list of floats: list of the embedded vectors. 
    '''
    def _get_query_embedding(self, string: str) -> list[float]:
        return self.vector.get_query_embedding(string)
