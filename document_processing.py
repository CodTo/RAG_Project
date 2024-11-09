import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

#This function reads a PDF-File and extracts the text from the pages
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

#This function splits the text into smaller chunks
def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks


#Vectorisation of documents
model = SentenceTransformer('all-MiniLM-L6-v2')

def vectorize_chunks(chunks):
    vectors = model.encode(chunks)
    return vectors

#Safe the Vectors in a Vector Database
def store_vectors_in_faiss(vectors):
    dimension = vectors.shape[1]  # Die Dimension der Vektoren
    index = faiss.IndexFlatL2(dimension)  # Index für Ähnlichkeitssuche
    index.add(vectors)  # Vektoren hinzufügen
    return index



#Function to put the Workflow together
def process_document(file_path):
    text = extract_text_from_pdf(file_path)
    chunks = split_text_into_chunks(text)
    vectors = vectorize_chunks(chunks)
    index = store_vectors_in_faiss(np.array(vectors))
    return index


#from document_processing import process_document

# Test-Pfad zu deinem Dokument
#file_path = 'C:\Users\hartm\RAG_Project\bescheid_M-MT 4222_Wiederzulassung.pdf'

# Rufe die Verarbeitungsfunktion auf
#index = process_document(file_path)

# Bestätige, dass das Dokument erfolgreich verarbeitet wurde
#print(f"Dokument {file_path} wurde erfolgreich verarbeitet. Index: {index}")

#chunks = split_text_into_chunks(text)
#print(f"Anzahl der Chunks: {len(chunks)}")


document_metadata = {}

def process_document(file_path, document_id):
    text = extract_text_from_pdf(file_path)
    chunks = split_text_into_chunks(text)

    # Speichere Metadaten für das Dokument
    document_metadata[document_id] = {
        'file_path': file_path,
        'chunks': len(chunks)
    }

    vectors = vectorize_chunks(chunks)
    index = store_vectors_in_faiss(np.array(vectors))
    return index

for document_id, metadata in document_metadata.items():
    print(f"Dokument-ID: {document_id}")
    print(f"Dateipfad: {metadata['file_path']}")
    print(f"Anzahl der Chunks: {metadata['chunks']}")
    print("-" * 30)


def save_metadata():
    with open('document_metadata.json', 'w') as f:
        json.dump(document_metadata, f)

def load_metadata():
    global document_metadata
    try:
        with open('document_metadata.json', 'r') as f:
            document_metadata = json.load(f)
    except FileNotFoundError:
        document_metadata = {}

# Beispiel beim Start der Anwendung
load_metadata()