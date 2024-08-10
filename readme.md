# Project Overview

This project is designed to process and analyze various types of documents, including PDFs, Word files, CSVs, and Excel spreadsheets. It performs several key functions: loading data, chunking it into manageable pieces, vectorizing it for storage, embedding context for queries, retrieving relevant context, and handling user queries. The project was developed using a variety of libraries and is designed with modularity in mind.

## Table of Contents

- [Step 1: Loading the Data](#step-1-loading-the-data)
- [Step 2: Chunking the Data](#step-2-chunking-the-data)
- [Step 3: Vectorizing the Data](#step-3-vectorizing-the-data)
- [Step 4: Implementing the Embedding Engine](#step-4-implementing-the-embedding-engine)
- [Step 5: Implementing the Retrieval Engine](#step-5-implementing-the-retrieval-engine)
- [Step 6: Implementing the Query Engine](#step-6-implementing-the-query-engine)
- [Technology Stack](#technology-stack)
- [Query Engine and AI Integration](#query-engine-and-ai-integration)
- [Installation](#installation)
- [Usage](#usage)
- [Future Work](#future-work)
- [License](#license)

## Step 1: Loading the Data

The initial step in the pipeline involves loading and parsing data from multiple document formats such as PDF, Word, CSV, and Excel. Custom loaders were developed to efficiently extract both textual and tabular data. The loaders are designed to handle a wide range of document structures and formats, ensuring robust data extraction.

### Libraries Used:
- `pdfplumber`:Used for extracting text and images from PDF files. This library handles complex PDF structures and supports precise text extraction.
- `re`:Employed for pattern matching and text processing. Regular expressions are crucial for cleaning and preprocessing the extracted data.
- `PdfReader`:Facilitates reading and parsing PDF documents at a low level, providing fine-grained control over the extraction process.
- `Document`:Used for working with Word documents, allowing for the extraction of text, tables, and other elements from `.docx` files.
- `pandas`: Utilized for handling data structures and performing operations on tabular data, particularly when working with CSV and Excel files.

## Step 2: Chunking the Data

Once the data is loaded, it is essential to split it into smaller, manageable chunks to facilitate downstream processing. Chunking strategies are tailored to the type and structure of the data, with the aim of preserving context while ensuring that the chunks are of a manageable size.

### Chunking Strategies

#### 1. Chunking for Tabular Data

A function to chunk table data, used to separate tables into chunks. This function converts a collection of tables into a list of lists where each inner list represents a table.

#### 2. Chunking for Text-Based Data

- **Fixed Length Chunking:** This approach splits the text into fixed-sized chunks based on a predefined number of characters, words, or sentences. It is simple but effective for uniformly structured text.
- **Windowed Chunking:** In this method, overlapping windows of text are created, ensuring that each chunk contains some overlap with the previous one. This helps to preserve context between adjacent chunks.
- **Paragraph Based Chunking:** The text is split based on paragraph boundaries, which is particularly useful for maintaining logical separations in narrative text.
- **Semantic Chunking:** This method uses semantic analysis to split the text based on meaning, ensuring that each chunk represents a coherent unit of thought.
- **Topic Based Chunking:** The text is split whenever a significant change in topic is detected. 

### Hybrid Chunking Algorithm

Currently in development, this algorithm groups tokens based on their underlying topic defined by a self-implented `Latent Dirichlet Allocation (LDA)` technique, combining the strengths of both topic-based and semantic chunking.


### Libraries Used:
- `sklearn`: Provides tools for vectorization and similarity computations, which are integral to semantic and topic-based chunking.
- `numpy`: Used for efficient numerical operations and matrix manipulations, essential for processing large datasets during chunking.
- `nltk`: Employed for text processing tasks such as tokenization, stopword removal, and sentence segmentation.
- `gensim`: Utilized for topic modeling and semantic analysis, particularly in the implementation of LDA for topic-based chunking.

## Step 3: Vectorizing the Data

Vectorization transforms the text chunks into numerical representations that can be efficiently stored and compared. Each chunk is converted into a vector, which captures the semantic meaning of the text and allows for similarity comparisons during retrieval.

- **TF-IDF Vectorization:** Term Frequency-Inverse Document Frequency (TF-IDF) is used to convert text into vectors that represent the importance of each word in a chunk relative to the entire dataset.

### Libraries Used:
- `sklearn`: Provides the TF-IDF vectorizer and tools for dimensionality reduction.
- `numpy`: Facilitates efficient computation and storage of large vector matrices.
- `nltk`: Supports preprocessing steps required before vectorization, such as tokenization and stopword removal.
- `gensim`: Used for advanced topic modeling techniques like LDA, which are crucial for generating meaningful vector representations.
- `math`: Provides mathematical functions for operations on vectors and matrices.
- `json`: Used for storing and retrieving vectorized data in a structured format.

## Step 4: Implementing the Embedding Engine

The embedding engine is responsible for generating dense vector representations for the text chunks using a pre-trained model. These embeddings are used to capture the contextual meaning of the text, which is crucial for accurate retrieval of relevant information. The vectorized text chunks are stored in a vectore store to steamline the computational task. 

### Embedding Process:

#### InstructorEmbedding Model: 

This model, sourced from Hugging Face's hkunlp/instructor-large, is used to generate embeddings for the text chunks. The model leverages large-scale training on diverse datasets to produce high-quality, context-aware embeddings.

#### Contextual Representation:

The embeddings are designed to capture the semantic context of the text, making them ideal for downstream tasks like similarity computation and information retrieval.

### Libraries Used:
- `InstructorEmbedding`: A model from Hugging Face that generates embeddings for text data, capturing the context and meaning of each chunk.

## Step 5: Implementing the Retrieval Engine

The retrieval engine is designed to efficiently fetch the most relevant chunks of data based on a user query. It compares the query's vector embedding against the stored vectors and selects the chunks with the highest similarity scores.

### Retrieval Process:

#### Vector Comparison: 

The vectors are compared using euclidean distance to compare the query vectors against the stored chunk vectors to identifying the most relavant chunks.

#### Efficient Search: 

The retrieval engine is optimized for speed, ensuring that relevant information is fetched quickly, even from large datasets.

### Libraries Used:
- `os`: Used for file handling and directory operations, essential for managing vector stores.
- `math`: Provides functions for calculating cosine similarity and other mathematical operations necessary for vector comparisons.

## Step 6: Implementing the Query Engine

The query engine integrates all the previous components to provide a seamless interface for users to interact with the system. It handles user queries, processes them through the embedding and retrieval engines, and returns the most relevant context to the user.

### Query Processing:

#### Prompt Handling: 
The engine takes user input, generates an embedding for the query, and uses it to retrieve relevant chunks from the vector store.

#### Result Aggregation: 
The retrieved chunks are processed and aggregated to provide a coherent response to the user's query.


### Libraries Used:
- `dotenv`: Manages environment variables, ensuring secure handling of API keys and other sensitive information.
- `langchain_openai`: Facilitates integration with OpenAI's language models, enhancing the capabilities of the query engine.
- `langchain_core`: Provides core functionality for building and deploying language model applications, streamlining the development of the query engine.

## Technology Stack
- **Backend:** The backend of the application is built using `Flask`. It provides the foundational structure for handling HTTP requests, managing routing, and document upload and storage.

- **Frontend:** The frontend is developed using HTML, CSS, and JavaScript where HTML structures the content, CSS handles the visual styling, and JavaScript adds dynamic functionality. The frontend communicates with the Flask backend through RESTful APIs, ensuring a smooth flow of data between the user interface and the server. The frontend is hosted on GitHub Pages, providing a reliable and accessible platform for deployment.

- **Model:** For vectorization, the project utilizes Hugging Face's hkunlp/instructor-large, a sophisticated transformer-based model. This model is designed to generate high-dimensional, dense vector embeddings that encapsulate the semantic meaning of text. The embeddings produced by hkunlp/instructor-large are crucial for the system's ability to perform context-aware retrieval and matching tasks.

## Query Engine and AI Integration

The query engine is a critical component of the system, designed to deliver accurate and contextually relevant responses to user queries. It operates by integrating several key processes:

- **Contextual Data Processing:** When a user submits a query, the query engine retrieves relevant text and table contexts from the vector store, which have been pre-processed and vectorized for efficient retrieval.

- **Chat History Management:** The query engine also takes into account the chat history, ensuring that the AI's responses are consistent with the ongoing conversation and reflect any prior exchanges between the user and the system.

- **AI-Powered Response Generation:** The query engine sends the combined data—text contexts, table contexts, the user's query, and the chat history—to OpenAI's chat-gpt model. This model, hosted by OpenAI, processes the input and generates a coherent, contextually appropriate response.

- **Integration with OpenAI's GPT:** The system utilizes OpenAI's API to connect with chat-gpt, ensuring that responses leverage the latest advancements in natural language processing and are informed by the most relevant data available.

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```
## Usage

### Running the Backend

1. **Start the Flask Server:**
Navigate to the directory containing your project and run the following command to start the Flask backend:

```bash
python server.py
```
The server will start running on http://localhost:5000 by default.

1. **Accessing the Frontend:**
The frontend is hosted separately on GitHub Pages. Once the Flask server is running, open your web browser and navigate to the GitHub Pages URL where the frontend is hosted.

### Interacting with the Application
1. Uploading Files:
Upload the document files (PDF, Word, CSV, Excel) you want to process using the file upload interface on the frontend.

2. Processing and Chunking:
After uploading, the application will automatically parse and chunk the document data using the chunking strategies you have implemented. The chunked data will be vectorized and stored for retrieval.

3. Querying:
Enter your query in the input box on the frontend. The query engine will process your input, retrieve the most relevant chunks from the vector store, and display the context based on the best matching vectors.

4. Viewing Results:
The results, including the extracted context, will be displayed on the frontend. You can review the chunks of data that are most relevant to your query.

## Future Work
#### Hybrid Chunking Algorithm:
Develop and integrate a hybrid chunking algorithm that combines topic-based and semantic chunking strategies to group tokens based on their underlying topics.

#### Enhanced Query Engine:
Improve the query engine to handle more complex and nuanced queries, providing more accurate and contextually relevant results incuding access to different APIs and Wikipedia search.

## License
This project is licensed under the MIT License. See the LICENSE file for details.