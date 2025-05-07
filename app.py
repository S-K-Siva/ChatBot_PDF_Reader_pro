from flask import Flask, request, jsonify, render_template
import os
import uuid
import time
import sys
print("Started importing...")
from pdfminer.high_level import extract_text
print("Imported pdfminer")
import faiss
print("Imported faiss")
import numpy as np
print("Imported numpy")
from openai import OpenAI
print("Imported open ai")
import torch
print("imported Torch")
print("Starting application...")
print("Importing Sentence Transformers...")
start_time = time.time()
from sentence_transformers import SentenceTransformer
print(f"Sentence Transformers imported in {time.time() - start_time:.2f} seconds")
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Global variables to store data
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created upload folder: {UPLOAD_FOLDER}")

# Store documents and index globally (for simplicity)
documents = {}
index = None  # Global FAISS index to store embeddings

# Initialize embedder
print("Loading embedding model - this may take a while on first run...")
start_time = time.time()
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"Embedding model loaded in {time.time() - start_time:.2f} seconds")
except Exception as e:
    print(f"Error loading embedding model: {str(e)}")
    sys.exit(1)

# Initialize OpenAI client
print("Initializing OpenAI client...")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def split_text_into_chunks(text, max_tokens=500, overlap=50):
    """Split text into chunks with overlap"""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+max_tokens]
        chunks.append(" ".join(chunk))
        i += max_tokens - overlap
    return chunks

def process_pdf(file_path):
    """Process PDF and store document data globally"""
    global index
    
    # Extract text from PDF
    text = extract_text(file_path)
    
    # Chunk text
    chunks = split_text_into_chunks(text, max_tokens=500)
    
    # Embed chunks
    embeddings = embedder.encode(chunks)
    
    # If the index doesn't exist, create it
    if index is None:
        index = faiss.IndexFlatL2(embeddings.shape[1])
    
    # Add embeddings to the global index
    index.add(np.array(embeddings).astype('float32'))
    
    # Store document data
    doc_id = str(uuid.uuid4())  # Unique ID for this document
    documents[doc_id] = {
        'text': text,
        'chunks': chunks,
        'file_path': file_path
    }
    
    return doc_id

def query_document(query, k=2):
    """Query the document index and return relevant chunks"""
    if index is None:
        return None, "No document uploaded yet"
    
    # Embed query
    query_embedding = embedder.encode([query])
    
    # Search for relevant chunks
    D, I = index.search(np.array(query_embedding).astype('float32'), k=k)
    
    # Get relevant chunks from documents
    relevant_chunks = []
    for idx in I[0]:
        # Get the chunk from any document, assuming all docs are in one index
        for doc_id, doc_data in documents.items():
            if idx < len(doc_data['chunks']):
                relevant_chunks.append(doc_data['chunks'][idx])
    
    return relevant_chunks, None

def generate_answer(context, query):
    """Generate answer using OpenAI's API"""
    combined_chunks = " ".join(context)
    # Limit tokens for context
    combined_chunks = " ".join(combined_chunks.split()[:1500])
    
    # Create prompt for LLM
    prompt = f"Use the following context to answer:\n{combined_chunks}\n\nQuestion: {query}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant that provides accurate information based on the document context."
            },
            {
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {str(e)}"

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """API endpoint to upload PDF"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Process PDF and get document ID
        doc_id = process_pdf(file_path)
        
        return jsonify({
            'message': 'PDF uploaded and processed successfully',
            'document_id': doc_id
        })
    
    return jsonify({'error': 'Invalid file format. Only PDF files are allowed'}), 400

@app.route('/query', methods=['POST'])
def query_pdf():
    """API endpoint to query PDF"""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    query = data.get('query')
    
    if not query:
        return jsonify({'error': 'Missing query'}), 400
    
    # Get relevant chunks
    relevant_chunks, error = query_document(query)
    
    if error:
        return jsonify({'error': error}), 404
    
    # Generate answer
    answer = generate_answer(relevant_chunks, query)
    
    return jsonify({
        'query': query,
        'answer': answer
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False)  # Disable reloader to avoid loading models twice
