from InstructorEmbedding import INSTRUCTOR
from loader import PDFLoader,DOCLoader
from chunking import Chunker
# This file is the implemnetation for the BaseEmbedding class to incorporate custom embeding

class Embedder():
    def __init__(self, instructor_model_name: str = 'hkunlp/instructor-large', instruction: str = '') -> None:
        self.model = INSTRUCTOR(instructor_model_name)
        self.instruction = instruction

    def get_query_embedding(self,query:str) -> list[float]:
        return self.model.encode([[self.instruction,query]])[0].tolist()
    
    def get_text_embedding(self,text:str) -> list[float]:
        return self.model.encode([[self.instruction,text]])[0].tolist()
    
    def get_text_embedding(self,texts:list[str]) -> list[float]:
        return self.model.encode([[self.instruction,text] for text in texts]).tolist()



# loader = PDFLoader('data/attention_is_all_you_need.pdf')
loader = PDFLoader('data/selections.pdf')
text = loader.extract_reader_text()
chunker = Chunker()
chunks = chunker.topic_based_chunking(text)

embedder = Embedder()
embeded_data = embedder.get_text_embedding(chunks)
for i in embeded_data:
    print(len(i))