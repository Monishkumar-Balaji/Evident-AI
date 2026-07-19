# server.py
import time
import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

# Ensure src/ modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from config import PROJECT_ROOT
from indexer import index_document
from rag import ask
from document_registry import load_registry

UPLOAD_DIR = PROJECT_ROOT / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


@app.route("/api/upload", methods=["POST"])
def upload_documents():
    """Accept one or more PDF files, save them to uploads/, and index each."""
    if "files" not in request.files:
        return jsonify({"status": "error", "message": "No files provided"}), 400

    files = request.files.getlist("files")
    if not files:
        return jsonify({"status": "error", "message": "No files selected"}), 400

    results = []

    for file in files:
        if not file.filename:
            continue

        filename = file.filename
        if not filename.lower().endswith((".pdf", ".docx")):
            results.append({
                "filename": filename,
                "status": "error",
                "message": "Unsupported file type. Only PDF and DOCX are allowed."
            })
            continue

        save_path = UPLOAD_DIR / filename
        file.save(str(save_path))

        try:
            index_document(save_path)

            registry = load_registry()
            doc_info = registry.get(filename, {})

            results.append({
                "filename": filename,
                "status": "success",
                "pages": doc_info.get("pages", 0),
                "chunks": doc_info.get("chunks", 0),
                "message": f"{filename} indexed successfully"
            })
        except Exception as e:
            results.append({
                "filename": filename,
                "status": "error",
                "message": str(e)
            })

    return jsonify({
        "status": "success",
        "documents": results,
        "message": f"Processed {len(results)} file(s)"
    })


@app.route("/api/ask", methods=["POST"])
def ask_question():
    """Run the full RAG pipeline for a question and return JSON."""
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"status": "error", "message": "No question provided"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"status": "error", "message": "Question cannot be empty"}), 400

    start_time = time.time()
    result = ask(question)
    elapsed = round(time.time() - start_time, 2)

    # Determine overall verification status
    verification_items = result.get("verification", [])
    if not verification_items:
        verification_status = "NO_DATA"
        verification_score = 0
    else:
        verified_count = sum(1 for v in verification_items if v.get("verified"))
        total_count = len(verification_items)
        verification_score = round((verified_count / total_count) * 100, 1)
        if verified_count == total_count:
            verification_status = "VERIFIED"
        elif verified_count > 0:
            verification_status = "PARTIALLY_VERIFIED"
        else:
            verification_status = "UNSUPPORTED"

    # Build clean sources list (remove embedding/text bulk from sources)
    clean_sources = []
    for source in result.get("sources", []):
        clean_sources.append({
            "source": source.get("source", "Unknown"),
            "page": source.get("page", 0),
            "distance": round(source.get("distance", 0), 3),
            "filter_score": source.get("filter_score", 0),
            "retrieval_score": source.get("retrieval_score", 0),
            "evidence_score": source.get("evidence_score", 0),
        })

    response = {
        "answer": result.get("answer", ""),
        "confidence": result.get("confidence", {}),
        "retrieval_quality": result.get("retrieval_quality", {}),
        "verification": {
            "status": verification_status,
            "score": verification_score,
            "details": verification_items
        },
        "sources": clean_sources,
        "evidence": result.get("evidence", []),
        "analysis": {
            "retrieved_chunks": result.get("chunk_filter", {}).get("retrieved_count", 0),
            "kept_chunks": result.get("chunk_filter", {}).get("kept_count", 0),
            "duplicates_removed": result.get("chunk_filter", {}).get("removed_duplicate_count", 0),
            "weak_removed": result.get("chunk_filter", {}).get("removed_weak_count", 0),
            "low_score_removed": result.get("chunk_filter", {}).get("removed_low_score_count", 0),
            "chunk_filter_reason": result.get("chunk_filter", {}).get("reason", ""),
            "kept_chunk_details": result.get("chunk_filter", {}).get("kept_chunks", []),
            "audit_trail": result.get("audit_trail", []),
        },
        "time_taken": elapsed
    }

    return jsonify(response)


@app.route("/api/documents", methods=["GET"])
def list_documents():
    """List all indexed documents from the registry."""
    registry = load_registry()

    documents = []
    for filename, info in registry.items():
        documents.append({
            "filename": filename,
            "pages": info.get("pages", 0),
            "chunks": info.get("chunks", 0)
        })

    return jsonify({
        "status": "success",
        "documents": documents
    })


@app.route("/api/documents/<name>", methods=["DELETE"])
def delete_document(name):
    """Remove a document's vectors and registry entry."""
    from vectordb import delete_document as delete_vectors
    from document_registry import load_registry, save_registry

    registry = load_registry()
    if name not in registry:
        return jsonify({"status": "error", "message": f"{name} not found"}), 404

    delete_vectors(name)
    del registry[name]
    save_registry(registry)

    # Also remove the file from uploads if it exists
    upload_path = UPLOAD_DIR / name
    if upload_path.exists():
        upload_path.unlink()

    return jsonify({
        "status": "success",
        "message": f"{name} removed successfully"
    })


if __name__ == "__main__":
    print("Starting Evident AI server...")
    print("API running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
