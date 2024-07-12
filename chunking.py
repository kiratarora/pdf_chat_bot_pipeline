'''
2 types of chunks: 
   1) for tabular data, having tables together and not splitting them up
   2) for text based data:
        > Fixed length chunking (Split the text into chunks of a fixed number of characters, words, or sentences)
        > Semantic Chunking  (Use a semantic segmentation approach to split the text based on sentence boundaries, paragraphs, or topic changes)
        > Windowed Chunking (Use overlapping windows to create chunks, ensuring each chunk has some overlap with the previous one to preserve context)
        > Topic Based Chunking ()
        > Parargraph Based Chunking (split your text data into individual sentences or paragraphs)

'''

from loader import PDFLoader,DOCLoader

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

loader = PDFLoader('data/Selections.pdf')
text = loader.extract_reader_text()
chunker = Chunker()
chunks = chunker.window_chunking(text)
for i in chunks:
        print('--------------------------------------------')
        print(i)
        print('--------------------------------------------')

        
