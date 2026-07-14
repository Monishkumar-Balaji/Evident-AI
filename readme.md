# Advanced Document RAG Project

This project is a document question-answering system built with a full Retrieval-Augmented Generation pipeline. It can index PDF and DOCX files, store their embeddings in ChromaDB, retrieve relevant chunks for a user question, generate a grounded answer with a HuggingFace LLM, and show confidence, evidence, verification, and source details.

What makes this project stand out from a normal college RAG project is that it does not simply retrieve the top chunks and pass them to an LLM. It adds multiple safety and quality layers around retrieval, context filtering, evidence extraction, hallucination checking, confidence scoring, and auditability.

## Setup

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a HuggingFace token and place it in a `.env` file:

```env
HF_TOKEN=<YOUR-API-TOKEN>
```

Run the terminal app:

```powershell
python src\main.py
```

## Project Architecture

```text
rag_project/
|
|-- .env
|-- requirements.txt
|-- uploads/
|-- chroma_db/
|-- data/
|   |-- documents.json
|
|-- src/
|   |-- config.py                  # Central settings and thresholds
|   |-- parser.py                  # PDF and DOCX text extraction
|   |-- preprocessor.py            # Text cleanup
|   |-- chunker.py                 # Recursive overlapping chunk creation
|   |-- embedder.py                # Embedding generation
|   |-- vectordb.py                # Persistent ChromaDB storage
|   |-- document_registry.py       # File hash registry for change detection
|   |-- indexer.py                 # Document indexing pipeline
|   |-- retriever.py               # Adaptive vector retrieval
|   |-- retrieval_gate.py          # Retrieval quality gate
|   |-- chunk_filter.py            # Chunk scoring, deduplication, and pruning
|   |-- sentence_extractor.py      # Sentence-level evidence extraction
|   |-- prompt.py                  # Grounded prompt construction
|   |-- generator.py               # HuggingFace LLM call
|   |-- hallucination_detector.py  # Answer sentence verification
|   |-- confidence.py              # Confidence scoring
|   |-- evidence.py                # Evidence package builder
|   |-- audit.py                   # Claim-to-evidence audit trail
|   |-- rag.py                     # Complete RAG pipeline
|   |-- main.py                    # CLI entry point
|
|-- tests/
```

## Advanced Features 

### 1. Adaptive Retrieval Depth

A normal RAG project usually retrieves a fixed number of chunks for every question. This project changes the number of retrieved chunks based on the question length.

Behind the screen:

- `src/retriever.py` uses `choose_top_k(query)`.
- Short questions use fewer chunks through `MIN_TOP_K`.
- Medium questions use `DEFAULT_TOP_K`.
- Longer or broader questions use `MAX_TOP_K`.
- This prevents small factual questions from receiving unnecessary context while still giving complex questions a wider search window.

Why it stands out:

This makes retrieval more efficient and context-aware instead of treating every query the same way.

### 2. Retrieval Quality Gate Before Generation

Most basic RAG projects always generate an answer after retrieval, even if the retrieved chunks are weak. This project checks whether the retrieval result is good enough before allowing the LLM to answer.

Behind the screen:

- `src/retrieval_gate.py` calculates retrieval quality from best vector distance, average score of strong chunks, and number of strong matching chunks.
- It converts ChromaDB distance into a 0-100 quality score.
- It sets a quality level such as `STRONG`, `GOOD`, `WEAK`, or `POOR`.
- If retrieval is too weak, `src/rag.py` returns a safe fallback response instead of calling the LLM.

Why it stands out:

This reduces hallucination because the model is not asked to answer when the system does not have enough document support.

### 3. Safe Empty Response for Missing Information

Instead of forcing the model to guess, the pipeline has a standard response for questions that cannot be answered from the uploaded documents.

Behind the screen:

- `empty_response()` in `src/rag.py` returns a fixed answer saying the information was not found.
- It also returns zero confidence, empty evidence, empty sources, and retrieval quality details.
- This path is used when retrieval fails or all chunks are removed during filtering.

Why it stands out:

It behaves like a reliable document assistant instead of a chatbot that always tries to answer.

### 4. Intelligent Chunk Filtering After Retrieval

Basic RAG systems directly pass retrieved chunks into the prompt. This project has a second filtering layer that re-ranks and removes bad context before generation.

Behind the screen:

- `src/chunk_filter.py` removes chunks that are above the similarity threshold, duplicates, or below a minimum relevance score.
- Each chunk gets a filter score using retrieval score, best evidence sentence score, and average evidence sentence score.
- Only the best chunks are kept using `MAX_CONTEXT_CHUNKS`.

Why it stands out:

The LLM receives cleaner, smaller, and more relevant context. This improves answer quality and lowers the chance of irrelevant text influencing the response.

### 5. Sentence-Level Evidence Extraction

The system does not only say which chunk was retrieved. It extracts the most relevant sentences inside each chunk.

Behind the screen:

- `src/sentence_extractor.py` splits each chunk into sentences.
- It embeds the user question and the candidate sentences.
- It uses cosine similarity to rank sentences by relevance to the question.
- Each selected sentence gets text, similarity score, and a strength rating such as `[**** ]`.

Why it stands out:

This gives fine-grained evidence. Instead of showing a large chunk and expecting the user to trust it, the system highlights the exact sentences that support the answer.

### 6. Hallucination Detection Through Answer Verification

This project checks the generated answer after the LLM responds. Each answer sentence is compared against the extracted evidence.

Behind the screen:

- `src/hallucination_detector.py` splits the answer into individual sentences.
- It embeds every answer sentence and every evidence sentence.
- It calculates cosine similarity between answer claims and evidence.
- A sentence is marked verified only if its similarity is above the threshold.

Why it stands out:

This adds a post-generation safety layer. The system can identify whether generated claims are actually supported by retrieved document evidence.

### 7. Multi-Factor Confidence Scoring

Many student RAG projects show an answer without saying how trustworthy it is. This project calculates a confidence score from multiple signals.

Behind the screen:

- `src/confidence.py` combines best retrieval score, average retrieval score, evidence strength, and answer verification score.
- It applies penalties when verification is weak or no strong evidence sentences exist.
- It also caps confidence based on retrieval quality so a weak retrieval result cannot produce an overly confident answer.

Why it stands out:

Confidence is not a random percentage. It is calculated from retrieval, evidence, and verification signals.

### 8. Claim-to-Evidence Audit Trail

The project can map generated answer claims back to the closest supporting evidence sentence.

Behind the screen:

- `src/audit.py` collects all evidence sentences.
- It embeds both answer claims and evidence quotes.
- It finds the closest evidence sentence for every generated claim.
- It returns an audit trail containing the claim, support status, similarity score, source, page, and supporting quote.

Why it stands out:

This makes the system explainable. A user can inspect not only the final answer, but also why the system believes the answer is supported.

### 9. Source and Page Metadata Tracking

The system keeps document source and page details throughout indexing, retrieval, filtering, and final output.

Behind the screen:

- `src/chunker.py` attaches `source`, `page`, `chunk`, and `length` to every chunk.
- `src/vectordb.py` stores this metadata with each vector in ChromaDB.
- `src/retriever.py` returns metadata with every retrieved result.
- `src/main.py` displays sources and page numbers to the user.

Why it stands out:

This allows citation-style answers and makes the system useful for real document QA, where users need to know where the answer came from.

### 10. Hash-Based Document Change Detection

The project avoids re-indexing unchanged documents.

Behind the screen:

- `src/document_registry.py` calculates a SHA-256 hash for each indexed file.
- It stores file hash, page count, and chunk count in `data/documents.json`.
- Before indexing, `src/indexer.py` checks whether the file has changed.
- If the file is unchanged, indexing is skipped.

Why it stands out:

This is a practical production-style feature. It saves time, avoids duplicate work, and keeps the vector database cleaner.

### 11. Persistent ChromaDB Vector Store

The embeddings are stored in a persistent ChromaDB database instead of being recreated every time the app starts.

Behind the screen:

- `src/vectordb.py` creates a `chromadb.PersistentClient`.
- Vectors are saved under `chroma_db/`.
- Each chunk gets a deterministic ID based on the source file and chunk ID.
- Old vectors for a changed document are deleted before new vectors are inserted.

Why it stands out:

The project behaves more like a real searchable knowledge base. Indexed documents stay available across sessions.

### 12. Rebuild and Legacy Metadata Checks

The project includes utilities for rebuilding the vector collection and checking whether old vectors are missing source metadata.

Behind the screen:

- `src/rebuild.py` can inspect the current collection status.
- It counts total vectors and legacy vectors without source metadata.
- `rebuild_collection()` clears the current collection, resets the registry, and indexes supplied documents again.
- `src/rebuild_collection.py` provides a guarded terminal flow that requires typing `REBUILD` before clearing vectors.

Why it stands out:

This shows maintenance thinking. The project includes tooling for fixing and refreshing the vector database, not just creating it once.

### 13. Strict Grounded Prompting

The prompt explicitly prevents the LLM from using outside knowledge.

Behind the screen:

- `src/prompt.py` builds a context-only prompt.
- The prompt instructs the LLM to use only provided context, avoid assumptions, avoid fabrication, return a fixed fallback message if the answer is missing, and mention page numbers used.
- `src/generator.py` also uses a system message that reinforces context-only answering.
- Temperature is set to `0` for more deterministic answers.

Why it stands out:

The generation step is controlled and document-grounded rather than open-ended.

### 14. Multi-Format Ingestion

The project supports both PDF and DOCX files.

Behind the screen:

- `src/parser.py` uses PyMuPDF for PDFs.
- It extracts text page by page from PDFs.
- It uses `python-docx` for DOCX files.
- DOCX content is normalized into the same page-style contract used by PDFs.

Why it stands out:

This makes the ingestion pipeline more flexible than PDF-only demos.

### 15. Recursive Overlapping Chunking

The project uses structured chunking instead of arbitrary text splitting.

Behind the screen:

- `src/chunker.py` uses `RecursiveCharacterTextSplitter`.
- It uses a chunk size of `350` and overlap of `50`.
- It tries to split by paragraphs, new lines, sentences, words, and finally characters.
- Each chunk keeps source and page metadata.

Why it stands out:

Recursive overlapping chunks preserve context better than naive fixed-length slicing.

## End-to-End Pipeline

```text
User document
    |
    v
PDF/DOCX parser
    |
    v
Text cleaning and recursive chunking
    |
    v
Embedding generation
    |
    v
Persistent ChromaDB storage
    |
    v
User question
    |
    v
Adaptive retrieval
    |
    v
Retrieval quality gate
    |
    v
Chunk filtering and sentence evidence extraction
    |
    v
Grounded LLM generation
    |
    v
Hallucination verification
    |
    v
Confidence score and audit trail
    |
    v
Final answer with sources
```

## Why This Is Better Than a Basic College RAG Project

A basic RAG project usually has this flow:

```text
Upload document -> chunk -> embed -> retrieve top-k -> send to LLM -> answer
```

This project has a more advanced flow:

```text
Upload document
-> detect document changes
-> chunk with metadata
-> persist vectors
-> adapt retrieval depth
-> assess retrieval quality
-> reject weak retrieval
-> filter and score chunks
-> extract sentence-level evidence
-> generate grounded answer
-> verify each generated sentence
-> calculate confidence
-> provide audit trail and citations
```

That extra validation and explainability layer is what makes the project stand out.

## Main Technologies Used

- Python
- ChromaDB
- HuggingFace Inference API
- `BAAI/bge-small-en-v1.5` embeddings
- `microsoft/Phi-3-mini-4k-instruct` LLM
- PyMuPDF
- python-docx
- scikit-learn cosine similarity
- LangChain text splitters
