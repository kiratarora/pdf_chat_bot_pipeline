from loader import PDFLoader,DOCLoader
from chunking import Chunker
from embedder import Embedder

# loader = PDFLoader('data/attention_is_all_you_need.pdf')
loader = PDFLoader('data/selections.pdf')
text = loader.extract_reader_text()
chunker = Chunker()
chunks = chunker.topic_based_chunking(text)

embedder = Embedder()
embeded_data = embedder.get_text_embedding(chunks)
for i in embeded_data:
    print(len(i))