# Project Overview

This project is designed to process and analyze various types of documents, including PDFs, Word files, CSVs, and Excel spreadsheets. It performs several key functions: loading data, chunking it into manageable pieces, vectorizing it for storage, embedding context for queries, retrieving relevant context, and handling user queries. The project was developed using a variety of libraries and is designed with modularity in mind.

## Table of Contents

- [Step 1: Loading the Data](#step-1-loading-the-data)
- [Step 2: Chunking the Data](#step-2-chunking-the-data)
- [Step 3: Vectorizing the Data](#step-3-vectorizing-the-data)
- [Step 4: Implementing the Embedding Engine](#step-4-implementing-the-embedding-engine)
- [Step 5: Implementing the Retrieval Engine](#step-5-implementing-the-retrieval-engine)
- [Step 6: Implementing the Query Engine](#step-6-implementing-the-query-engine)
- [Chunking Algorithms](#chunking-algorithms)
- [Technology Stack](#technology-stack)
- [Frontend](#frontend)
- [Installation](#installation)
- [Usage](#usage)
- [Future Work](#future-work)
- [License](#license)

## Step 1: Loading the Data

The first step involves loading data from various document formats, including PDF, Word, CSV, and Excel files. The loaders were implemented from scratch and are capable of parsing both text and tables.

### Libraries Used:
- `pdfplumber`
- `re`
- `PdfReader`
- `Document`
- `pandas`

## Step 2: Chunking the Data

Once the data is loaded, it is chunked into manageable pieces. This is critical for processing large documents efficiently. Different chunking strategies are used depending on the data type.

### Libraries Used:
- `sklearn`
- `numpy`
- `nltk`
- `gensim`

## Step 3: Vectorizing the Data

After chunking, the data is vectorized for efficient storage and retrieval. This process converts the text chunks into numerical vectors.

### Libraries Used:
- `sklearn`
- `numpy`
- `nltk`
- `gensim`
- `math`
- `json`

## Step 4: Implementing the Embedding Engine

The embedding engine is responsible for finding the best context vector for a given prompt. This is done using the `InstructorEmbedding` model from Hugging Face.

### Libraries Used:
- `InstructorEmbedding`

## Step 5: Implementing the Retrieval Engine

The retrieval engine fetches the most relevant context for a given query by comparing vector embeddings.

### Libraries Used:
- `os`
- `math`

## Step 6: Implementing the Query Engine

The query engine combines all the processes to handle user queries, embedding, and retrieval seamlessly.

### Libraries Used:
- `dotenv`
- `langchain_openai`
- `langchain_core`

## Chunking Algorithms

### 1. Chunking for Tabular Data

A function to chunk table data, used to separate tables into chunks.

- **Parameters:**
  - `data (n-D list/pandas DataFrame)`: A collection of tables, converted into a list of lists where each inner list represents a table.
- **Returns:**
  - `list of lists`: The function returns a list of lists.

### 2. Chunking for Text-Based Data

- **Fixed Length Chunking:** Splits the text into chunks of a fixed number of characters, words, or sentences.
- **Windowed Chunking:** Uses overlapping windows to create chunks, ensuring each chunk has some overlap with the previous one to preserve context.
- **Paragraph Based Chunking:** Splits the text data into individual sentences or paragraphs.
- **Semantic Chunking:** Uses semantic segmentation to split the text based on sentence boundaries, paragraphs, or topic changes.
- **Topic Based Chunking:** Splits text when a change in topic is detected.

### Hybrid Chunking Algorithm

Currently in development, this algorithm groups tokens based on their underlying topic, combining the strengths of both topic-based and semantic chunking.

## Technology Stack

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Model:** Hugging Face's `hkunlp/instructor-large` for vectorization

## Frontend

The frontend is implemented using HTML, CSS, and JavaScript and is hosted on GitHub Pages.

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
python app.py
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