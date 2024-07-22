import os
from vertor_store import Vector_Store 

class Retriever():
    def __init__(self, extentions, path) -> None:
        all_files = os.listdir(path)
        self.files = [path+'/'+file for file in all_files if file.split('.')[-1] in extentions]
        self.vector = Vector_Store(self.files)
        self.vector_store = self.vector.get_vector_store()

    def get_context(self,querry):
        # Processing the files to get the data
        print("Processing files, running this the first time may take time")
        self._process_files()
        self.vector_store = self.vector.get_vector_store()
        embedded_querry = self._get_query_embedding(querry)

    def _process_files(self):
        return self.vector.process_files()
         
    def process_single_file(self, file_name):
        return self.vector.add_sigle_file(file_name)

    def _get_query_embedding(self,string):
        return self.vector.get_query_embedding(string)


rev = Retriever(['pdf','docx'], path='data').get_context('Hello')