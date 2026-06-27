## Create virtual Environment
python -m venv .venv

## Activate virtual Environment
.venv\Scripts\Activate.ps1

## Install dependencies

pip install -r requirements.txt

## Create HuggingFace token
create a hugging face token and place it in a .env file as HF_TOKEN =<YOUR-API-TOKEN>

## project architecture 

rag_project/
│
├── .env
├── requirements.txt
├── uploads/
├── chroma_db/
│
├── src/
│   ├── config.py          # Configurations
│   ├── parser.py          # PDF/DOCX extraction
│   ├── chunker.py         # Chunking
│   ├── embedder.py        # Embedding model
│   ├── vectordb.py        # ChromaDB
│   ├── retriever.py       # Similarity search
│   ├── prompt.py          # Prompt templates
│   ├── generator.py       # HuggingFace LLM
│   ├── rag.py             # Main pipeline
│   └── main.py            # Entry point
│
└── tests/

## To run in terminal

python main.py