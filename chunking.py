'''
2 types of chunks: 
   1) for tabular data, having tables together and not splitting them up
   2) for text based data:
        > Fixed length chunking (Split the text into chunks of a fixed number of characters, words, or sentences)
        > Windowed Chunking (Use overlapping windows to create chunks, ensuring each chunk has some overlap with the previous one to preserve context)
        > Parargraph Based Chunking (split your text data into individual sentences or paragraphs)
        > Semantic Chunking  (Use a semantic segmentation approach to split the text based on sentence boundaries, paragraphs, or topic changes)
        > Topic Based Chunking ()

'''

from loader import PDFLoader,DOCLoader
import math

class Chunker:
        def __init__(self):
                self.chunks = []
        
        '''
        Function to chunk table data, this is used to separate tables into chunnks
        
        Parameters:
                data(n-D list/pd df): This is going to be a collection of tables, and this function converts them to a list of lists where each inner list represents a table

        Returns:
                list of lists: The function returns a list of lists
        '''
        # def chunkTable(self, data):

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
        def paragraph_chunking(self,data,size = 2500, delimiter = '\n'):  
                chunks = data.split(delimiter)
                chunks = [i for i in chunks if i!=' '] # removing all the empty characters
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
                return limited_chunks
                



loader = PDFLoader('data/attention_is_all_you_need.pdf')
# loader = PDFLoader('data/selections.pdf')
text = loader.extract_reader_text()
chunker = Chunker()
chunks = chunker.paragraph_chunking(text)
# for i in chunks:
#         print('--------------------------------------------')
#         print(i)
#         print('--------------------------------------------')
print(len(chunks))

        

# step 1: loading the data
# step 2: chunking the data
# step 3: vectorizing the data to store it 
# step 4: implementing the embedding engine (finds the best context vector for the prompt)
# step 5: implenting the retrevial engine to fetch the context
# step 6: implement the querry engine to combine all those processes