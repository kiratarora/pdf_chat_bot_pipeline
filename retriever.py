import os, math
from vertor_store import Vector_Store 

class Retriever():
    def __init__(self, extentions, path) -> None:
        all_files = os.listdir(path)
        self.files = [path+'/'+file for file in all_files if file.split('.')[-1] in extentions]
        self.vector = Vector_Store(self.files)
        self.vector_store = self.vector.get_vector_store()

    def get_context(self,querry):
        # Processing the files to get the data
        self._process_files()
        self.vector_store = self.vector.get_vector_store()
        embedded_querry = self._get_query_embedding(querry)

        closest_matching_contex = {}
        for doc in self.vector_store:
            best_context, best_context_value, best_context_vector = '', math.inf, None
            for context in self.vector_store[doc]:
                vector_compare_score = self._vector_compare(self.vector_store[doc][context], embedded_querry)
                if vector_compare_score < best_context_value:
                    best_context_value, best_context, best_context_vector = vector_compare_score, context, self.vector_store[doc][context]
            if best_context_vector != None:
                closest_matching_contex[doc] = (best_context, best_context_vector )

        # Use best contexts to find the similarity
        test_value, test_context = math.inf, ''
        for i in closest_matching_contex:
            comp = self._vector_compare(closest_matching_contex[i][1], embedded_querry)
            if test_value > comp:
                test_value = comp
                test_context = closest_matching_contex[i][0]
        
        return test_context

    def _vector_compare(self,context_vector, querry_vector):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(context_vector, querry_vector)))  

    def _process_files(self):
        return self.vector.process_files()
         
    def process_single_file(self, file_name):
        return self.vector.add_sigle_file(file_name)

    def _get_query_embedding(self,string):
        return self.vector.get_query_embedding(string)
