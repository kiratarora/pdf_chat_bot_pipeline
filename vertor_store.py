from loader import PDFLoader,DOCLoader, XLSLoader
from chunking import Chunker
from embedder import Embedder
import json

'''
Class to streamline extractions, chunking, and embedding the data.
'''
class Vector_Store():

    '''
    Constructor for the class
    Parameters:
        files (list of str): the address of the files that need to be parseds
    '''
    def __init__(self, files:list[str]) -> None:
        self.files = files
        self.chunker = Chunker()
        self.vector_store = self.get_vector_store()
        if 'text' not in self.vector_store:
            self.vector_store['text'] = {}
            self._write_vector_store()
        if 'table' not in self.vector_store:
            self.vector_store['table'] = {}
            self._write_vector_store()
        self.embedder = Embedder()

    '''
    Function that returns the latest edition of the vector_store.json where all the embedded data is stored.

    Returns: 
        dict: the vector store with the embeddings for all the data and tables
    '''
    def get_vector_store(self) -> dict:
        file_path = 'vector_store.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    '''
    PRIVATE: function to witre the updated vectore store into the json file
    '''
    def _write_vector_store(self) -> None:
        with open('vector_store.json', 'w') as file:
            json.dump(self.vector_store, file, indent=4)

    '''
    PRIVATE HELPER: this function is the main funtion of the vector_store class. It passes over each file, parses all the data, chunks it, embbeds it and then stores it. 
    
    Parameters: 
        file (list of str): the address of all the files to be processed.
        flag (bool): flag value that is used to override and re-process a file that has already been processed.

    Returns:
        str: Confirmation that the file processing was completed.
    '''        
    def _process_files_helper(self, files: list[str], flag: bool) -> str:
        # Parsing over all the files
        for file in files:
            if file not in self.vector_store['text'] or flag:
                doc_type = self._doc_type(file)
                if doc_type == 'pdf':
                    loader = PDFLoader(file)
                    data_reader = loader.parse_data()
                    table_reader = loader.extract_table()
                elif doc_type == 'docx' or doc_type == 'doc':
                    loader = DOCLoader(file)
                    data_reader = loader.extract_text()
                    table_reader = loader.extract_table()
                elif doc_type == 'xls' or doc_type == 'xlsm' or doc_type == 'xlsx' or doc_type == 'xlt' or doc_type == 'xltm' or doc_type == 'xltx':
                    loader = XLSLoader(file)
                    data_reader = ''
                    table_reader = loader.read_excel()
                elif doc_type == 'csv':
                    loader = XLSLoader(file)
                    data_reader = ''
                    table_reader = loader.read_csv()
                #~~~#~~~# ADD MORE LOADERS BELOW #~~~#~~~#
                else:
                    continue

                data_chunked = self.chunker.best_chunks(data_reader)
                data_embedded = self.embedder.get_text_embedding(data_chunked)
                embedding_dict = dict(zip(data_chunked,data_embedded))
                self.vector_store['text'][file]=embedding_dict

                table_chunked = self.chunker.chunk_table(table_reader)
                if table_chunked is not None and len(table_chunked) != 0:
                    table_embedded = self.embedder.get_text_embedding(table_chunked)
                    table_embedding_dict = dict(zip(table_chunked,table_embedded))
                    self.vector_store['table'][file]=table_embedding_dict

        self._write_vector_store()
        return 'Files Added'
    
    '''
    Function that processes the files assigned to it at the time of creation of the object

    Returns: 
        str: Confirmation that the file processing was completed.
    '''
    def process_files(self) -> str:
        return self._process_files_helper(files = self.files, flag = False)

    '''
    PRIVATE: function that determines the typr of file

    Parameters:
        file (str): name of the file

    Retuns:
        str: extention of the file
    '''
    def _doc_type(self, file: str) -> str:
        extention = file.split('.')
        return extention[-1]

    '''
    Function to add a single file, surpasses the need for a file to not be processes (can re-process already processed files)

    Parameters:
        file_name (str): address of the file to be reprocessed

    Returns: 
        str: Confirmation that the file processing was completed.
    '''
    def add_sigle_file(self,file_name:str) -> str:
        return self._process_files_helper(flag = True, files = [file_name])

    '''
    Function to embed a querry

    Parameters:
        string (str): used defined querry

    Returns: 
        list of floats: embedding vector
    '''
    def get_query_embedding(self,string:str) -> list[float]:
        return self.embedder.get_query_embedding(string)