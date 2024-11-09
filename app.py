from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from document_processing import process_document
from sentence_transformers import SentenceTransformer
import json

app = Flask(__name__, static_folder='.')
CORS(app)

# Konfiguration des Upload-Verzeichnisses
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Globale Variablen
document_metadata = {}
index = None  # FAISS-Index, der die Vektoren speichert

# Initialisiere das Modell
model = SentenceTransformer('all-MiniLM-L6-v2')

# Funktionen zum Speichern und Laden der Metadaten
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

# Metadaten beim Start laden
load_metadata()

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/query', methods=['POST'])
def query():
    if index is None:
        return jsonify({'error': 'Kein Dokument verarbeitet'}), 400

    data = request.get_json()
    question = data.get('question', 'Keine Frage gestellt.')
    query_vector = model.encode([question])

    distances, indices = index.search(query_vector, top_k=3)
    return jsonify({'indices': indices.tolist(), 'distances': distances.tolist()})

@app.route('/upload', methods=['POST'])
def upload_document():
    global index
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Dokument-ID generieren (z.B. Dateiname verwenden)
        document_id = filename
        index = process_document(file_path, document_id)

        # Speichere die Metadaten
        document_metadata[document_id] = {
            'file_path': file_path,
            'chunks': "Anzahl der Chunks (hier einzufügen)"
        }
        save_metadata()

        return jsonify({'message': 'Dokument erfolgreich verarbeitet'}), 200

# Route zum Abrufen der verarbeiteten Dokumente
@app.route('/documents', methods=['GET'])
def get_documents():
    return jsonify(document_metadata)

if __name__ == '__main__':
    app.run(debug=True)

