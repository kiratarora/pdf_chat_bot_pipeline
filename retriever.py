import os, math
from vertor_store import Vector_Store 

class Retriever():
    def __init__(self, extentions, path) -> None:
        all_files = os.listdir(path)
        self.files = [path+'/'+file for file in all_files if file.split('.')[-1] in extentions]
        self.vector = Vector_Store(self.files)
        self.vector_store = self.vector.get_vector_store()
        self.vector_store_text = self._get_text_store()
        self.vector_store_table = self._get_table_store()         

    def _get_text_store(self):
        try:
            vector_store_text = self.vector.get_vector_store()['text']
        except KeyError:
            vector_store_text = {}
        return vector_store_text
    
    def _get_table_store(self):
        try:
            vector_store_text = self.vector.get_vector_store()['table']
        except KeyError:
            vector_store_text = {}
        return vector_store_text

    def get_context(self,querry):
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
            if final_value > comp:
                final_value = comp
                final_context = closest_matching_contex[i][0]
        
        final_table_value, final_table = math.inf, ''
        for i in closest_matching_table:
            comp = self._vector_compare(closest_matching_table[i][1], embedded_querry)
            if final_table_value > comp:
                final_table_value = comp
                final_table = closest_matching_table[i][0]

        return (final_context, final_table)

    def _vector_compare(self,context_vector, querry_vector):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(context_vector, querry_vector)))  

    def _process_files(self):
        return self.vector.process_files()
         
    def process_single_file(self, file_name):
        return self.vector.add_sigle_file(file_name)

    def _get_query_embedding(self,string):
        return self.vector.get_query_embedding(string)
