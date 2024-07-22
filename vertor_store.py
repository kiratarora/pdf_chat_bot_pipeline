from InstructorEmbedding import INSTRUCTOR
from loader import PDFLoader,DOCLoader
from chunking import Chunker
from embedder import Embedder
import json

class Vector_Store():
    def __init__(self, files:str) -> None:
        self.files = files
        self.chunker = Chunker()
        self.vector_store = self.get_vector_store()
        self.embedder = Embedder()


    def get_vector_store(self):
        file_path = 'vector_store.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def _write_vector_store(self):
        with open('vector_store.json', 'w') as file:
            json.dump(self.vector_store, file, indent=4)

    '''
    This function is the main funtion of the vector_store class. It passes over each file, parses all the data, chunks it, embbeds it and then stores it. 
    '''        
    def _process_files_helper(self, files, flag):
        # Parsing over all the files
        for file in files:
            if file not in self.vector_store or flag:
                doc_type = self._doc_type(file)
                if doc_type == 'pdf':
                    loader = PDFLoader(file)
                    data_reader = loader.parse_data()
                elif doc_type == 'doc':
                    loader = DOCLoader(file)
                    data_reader = loader.get_text()
                else: # Add more loaders
                    continue
                data_chunked = self.chunker.best_chunks(data_reader)
                data_embedded = self.embedder.get_text_embedding(data_chunked)
                embedding_dict = dict(zip(data_chunked,data_embedded))
                self.vector_store[file]=embedding_dict
        self._write_vector_store()
        return 'Files Added'
    
    def process_files(self):
        return self._process_files_helper(files = self.files, flag = False)

    def _doc_type(self, file):
        extention = file.split('.')
        return extention[-1]

    def add_sigle_file(self,file_name):
        return self._process_files_helper(flag = True, files = [file_name])

    def get_query_embedding(self,string):
        return self.embedder.get_query_embedding(string)