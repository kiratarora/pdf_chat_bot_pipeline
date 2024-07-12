'''
2 types of chunks: 
   1) for tabular data, having tables together and not splitting them up
   2) for text based data:
        > Fixed length chunking (Split the text into chunks of a fixed number of characters, words, or sentences)
        > Semantic Chunking  (Use a semantic segmentation approach to split the text based on sentence boundaries, paragraphs, or topic changes)
        > Windowed Chunking (Use overlapping windows to create chunks, ensuring each chunk has some overlap with the previous one to preserve context)
        > Topic Based Chunking ()
        > Sentence or Parargraph Bases Chunking (split your text data into individual sentences or paragraphs)

'''
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

        
