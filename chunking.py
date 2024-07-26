'''
2 types of chunks: 
   1) for tabular data, having tables together and not splitting them up
   2) for text based data:
        > Fixed length chunking (Split the text into chunks of a fixed number of characters, words, or sentences)
        > Windowed Chunking (Use overlapping windows to create chunks, ensuring each chunk has some overlap with the previous one to preserve context)
        > Parargraph Based Chunking (split your text data into individual sentences or paragraphs)
        > Semantic Chunking  (Use a semantic segmentation approach to split the text based on sentence boundaries, paragraphs, or topic changes)
        > Topic Based Chunking (Split when a change in topic is detected)
'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from gensim import corpora, models

import math

class Chunker:
        'Function to clean the data in the chunks'
        def _data_cleaner(self,data,chars_to_remove):
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
        def chunkTable(self, data):
                tables = []
                for table in data:
                        if type(table) != str:
                                tables.append(str(table))
                        else:
                                tables.append(table)                                

        '''
        Function to implement simple fixed length chunking

        Parameters: 
                data (str): string of the text to be chunked
                size (int): chunk size
        Returns: 
                list of strs: returns a list of chunked data strings
        '''
        def fixed_length_chunking(self,data,size=2000):
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
        def window_chunking(self,data,size=2000,overlap=500):
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
        def paragraph_chunking(self,data,size = 2500, delimiter = '\n', add_back_delimiter = False):  
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
        def semantic_chunking(self,data,delimiter='.', chunk_size = 4, chunk_similarity_threshold = 0.3):
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
        def topic_based_chunking(self, data, num_topics = 5, passes = 15):
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
        def hybrid_chunking():
                return None

        def best_chunks(self, data):
                return self.semantic_chunking(data=data)

def setup():
        nltk.download('punkt')
        nltk.download('stopwords')
# # _____________________________________________________________________________________
# setup() # Uncomment this function to setup the downloads required to run the function
# # _____________________________________________________________________________________


# step 1: loading the data
# step 2: chunking the data
# step 3: vectorizing the data to store it 
# step 4: implementing the embedding engine (finds the best context vector for the prompt)
# step 5: implenting the retrevial engine to fetch the context
# step 6: implement the querry engine to combine all those processes