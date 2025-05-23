# 📚 Hybrid Summarization Tool: A RAG-Based Approach 📚

This repository houses a versatile text summarization and lexical analysis tool built with Gradio. It features both a general-purpose summarizer and a conceptual Retrieval Augmented Generation (RAG) approach for document summarization, along with a lexical analyzer for word information.

## 🚀 Features

This application offers a range of functionalities to help you distill information and explore word meanings:

**Paragraph Summarization (app.py):**
- Summarize any given text paragraph.
- Choose from Precise, Bullet Points, or Detailed summary formats.

**Document Summarization (app.py & rag.py):**
- **General Document Summarization (app.py)**: Upload .txt, .pdf, or .docx files for summarization with customizable output types.
- **RAG-Based Document Summarization (rag.py)**: A conceptual implementation demonstrating how FAISS could be integrated to retrieve relevant context for more informed document summaries. (Note: The FAISS integration in rag.py is currently a placeholder and requires further development for full RAG functionality.)

**Lexical Analyzer (app.py):**
- Get summaries for words directly from Wikipedia.
- If a Wikipedia entry isn't found, retrieve definitions and examples from WordNet.

**Word Summarization (rag.py):**
- Directly query Wikipedia for a summary of a given word. Handles disambiguation errors to guide you to the correct meaning.

## 🛠️ Technologies Used

The project leverages powerful open-source libraries:

- **gradio**: For creating the interactive and user-friendly web interface.
- **transformers**: Utilizes pre-trained models (specifically facebook/bart-large-cnn) for high-quality text summarization.
- **torch**: The underlying deep learning framework for the transformers models.
- **faiss-cpu**: (Or faiss-gpu) For efficient similarity search, forming the basis of the RAG approach in rag.py.
- **wikipedia & wikipedia-api**: Python wrappers for accessing and retrieving information from Wikipedia.
- **PyPDF2**: For extracting text from PDF documents.
- **python-docx**: For extracting text from Microsoft Word (.docx) documents.
- **nltk**: The Natural Language Toolkit, used for lexical analysis, specifically with wordnet.

## ⚙️ Setup and Installation

To get the application running on your local machine, follow these steps:

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
*(Replace your-username and your-repo-name with your actual GitHub details.)*

2. **Create a virtual environment (recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. **Install dependencies:**
Install all the required libraries using the provided requirements.txt file:

```bash
pip install -r requirements.txt
```

4. **Download NLTK data:**
The nltk library requires some data to be downloaded. Run a Python interpreter and execute:

```python
import nltk
nltk.download('wordnet')
```
*You only need to do this once.*

## 🚀 How to Run

You can run either app.py or rag.py independently.

### Running app.py (General Summarization & Lexical Analyzer)

```bash
python app.py
```

This will launch the Gradio interface in your web browser, typically at http://127.0.0.1:7860.

### Running rag.py (BART Summarization & Conceptual RAG)

```bash
python rag.py
```

This will also launch a Gradio interface in your web browser.

## 💡 Future Enhancements

- **Full FAISS Integration**: Implement actual vector embeddings and retrieval for a fully functional RAG system in rag.py.
- **More Summarization Models**: Allow users to select different pre-trained summarization models.
- **Advanced Lexical Analysis**: Incorporate more lexical resources or provide richer word information.
- **Error Handling**: Enhance robust error handling for various inputs and edge cases.
- **User Interface Improvements**: Further refine the Gradio UI for a smoother user experience.

## 🙏 Acknowledgements

- Hugging Face transformers library for providing access to powerful NLP models.
- Wikipedia for its vast knowledge base.
- NLTK for natural language processing tools.
- Gradio for simplifying web application development.
