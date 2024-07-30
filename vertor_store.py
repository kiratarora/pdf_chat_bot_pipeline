from loader import PDFLoader,DOCLoader, XLSLoader
from embedder import Embedder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim import corpora, models
import math, json

class Chunker:
        'Function to clean the data in the chunks'
        def _data_cleaner(self,data: str,chars_to_remove: list[str]) -> str:
                for i in range(len(data)):
                        data[i] = data[i].rstrip()
                        data[i] = data[i].lstrip()
                        for chars in chars_to_remove:
                                data[i] = data[i].replace(chars,'')
                return data

        def __init__(self):
                self.chunks = []
        
        '''
        Function to chunk table data, this is used to separate tables into chunnks
        
        Parameters:
                data(n-D list/pd df): This is going to be a collection of tables, and this function converts them to a list of lists where each inner list represents a table

        Returns:
                list of lists: The function returns a list of lists
        '''
        def chunk_table(self, data: list[list]) -> list[str]:
                tables = []
                for table in data:
                        if len(table) == 0:
                                continue
                        title_row = table[0]
                        for i in range(9,len(table),9):
                                table.append(title_row+table[i-9:i])                              
                return str(tables)
        
        '''
        Function to implement simple fixed length chunking

        Parameters: 
                data (str): string of the text to be chunked
                size (int): chunk size
        Returns: 
                list of strs: returns a list of chunked data strings
        '''
        def fixed_length_chunking(self, data:str, size:int=2000) -> list[str]:
                return self.window_chunking(data,size,overlap=0)
        
        '''
        this function splits the data based on sliding window chunks meaning they have some overlapping characters

        Parameters:
                data (str): data to be split
                size (int): this is the size of the chunks
                overlap (int): number of characters over lapping in each chunk
        Returns:
                list of strings: list of chunked data
        '''
        def window_chunking(self, data:str, size:int=2000, overlap:int=500) -> list[str]:
                return [data[i:i+size] for i in range(0,len(data),(size-overlap))]
        
        '''
        this function splits the data based on paragraphs (it also limits the max chunk size to 3000 chunks) 

        Parameters:
                data (str): data to be split
                size (int): set the size of the chunks
                delimilter(char/string): this is the delimter for chunking
        Returns:
                list of strings: list of chunked data
        '''
        def paragraph_chunking(self, data:str, size:int = 2500, delimiter:str = '\n', add_back_delimiter:bool = False) -> list[str]:  
                chunks = data.split(delimiter)
                chunks = [i for i in chunks if i!=' '] # removing all the empty characters
                if add_back_delimiter:
                        for chunk in range(len(chunks)):
                                chunks[chunk] = chunks[chunk] + delimiter
                # Checking to see if there are any chunks greater than 3000 characters, and if there are, we will split them in half
                limited_chunks = []
                for chunk in chunks:
                        if (len(chunk)>size):
                                divisions = math.ceil(len(chunk)/size)
                                division_size = math.ceil(len(chunk)/divisions)
                                divided_chunks = self.fixed_length_chunking(chunk,division_size)
                                for i in divided_chunks:
                                        limited_chunks.append(i)
                        else:
                                limited_chunks.append(chunk)
                return self._data_cleaner(limited_chunks, ['\n'])    
        
        '''
        This function splits the data based on semantic context. 
        The first step is to split the entire data into smaller chunks or tokens and then doing a semantic analysis to finally group the tokens into semantically similar chunks.

        Parameters: 
                data (str): this is a string of characters representing the whole data.
                chunk_size (int): the size of the chunk meaning the number of tokens in a chunk
                chunk_similarity_threshold (float): the similarity threshold for the tokens to be chunked
        
        Returns:
                list of strings: retuns a list of strings reprensing the chunked data.
        '''
        def semantic_chunking(self, data:str, delimiter:str = '.', chunk_size:int = 4, chunk_similarity_threshold:float = 0.3) -> list[str]:
                sentences = self.paragraph_chunking(data=data, delimiter=delimiter, add_back_delimiter=True)
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(sentences)
                similarity_matrix = cosine_similarity(tfidf_matrix)
                
                chunks = []
                for i in range(0, len(sentences), chunk_size):
                        chunk_sentences = sentences[i:i + chunk_size]
                        chunk_similarity = similarity_matrix[i:i + chunk_size, i:i + chunk_size]
                        avg_similarity = np.mean(chunk_similarity)
                        if avg_similarity > chunk_similarity_threshold: 
                                chunks.append(' '.join(chunk_sentences))
                
                return chunks
        
        '''
        This function takes the data, splits it based distict on topics. 

        Parameters:
                raw_data (str): data to be chunked
                num_topics (int): the number of topics for the lda model
                passes (int): number of passes for the lda model
        Returns:
                list of strings: chunked data
        '''
        def topic_based_chunking(self, data: str, num_topics: int = 5, passes: int = 15) -> list[str]:
                # Preprocessing Data
                sentences = sent_tokenize(data)
                stop_words = set(stopwords.words('english'))
                preprocessed_data = [] # 2-D array with the list of preprocessed words
                for sentence in sentences:
                        words = word_tokenize(sentence.lower())
                        words = [word for word in words if word.isalpha() and word not in stop_words]
                        preprocessed_data.append(words)
                # Vectorizing the data
                dictionary = corpora.Dictionary(preprocessed_data)
                corpus = [dictionary.doc2bow(sentence) for sentence in preprocessed_data]
                lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
                # Distribution based on topics
                sentence_topics = []
                for bow in corpus:
                        topic_distribution = lda_model.get_document_topics(bow)
                        dominant_topic = max(topic_distribution, key=lambda x: x[1])[0]
                        sentence_topics.append(dominant_topic)
                # Chunking
                chunks = []
                current_chunk = [sentences[0]]
                current_topic = sentence_topics[0]
                
                for i in range(1, len(sentences)):
                        if sentence_topics[i] == current_topic:
                                current_chunk.append(sentences[i])
                        else:
                                chunks.append(' '.join(current_chunk))
                                current_chunk = [sentences[i]]
                                current_topic = sentence_topics[i]
                
                if current_chunk:
                        chunks.append(' '.join(current_chunk))
                
                return chunks

        '''
        This is a hybrid function that tokenizes the data, then chunks it by joining all the related sentences togeter irrespecive of it's original position. 
        '''
        def hybrid_chunking(self):
                return None

        '''
        Function to return the best chunks based on the different chunking stratergies
        Parameters:
                data (str): data to be chunked
        Returns: 
                list of strings: chunked data
        '''
        def best_chunks(self, data: str) -> list[str]:
                if data != '':
                        return self.semantic_chunking(data=data)
                else:
                        return ['']




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