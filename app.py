from flask import Flask, jsonify, request, send_from_directory

# Erstelle die Flask-App
app = Flask(__name__, static_folder='.')

# Startseite
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    question = data.get('question', 'Keine Frage gestellt.')
    response = {"answer": f"Deine Frage war: {question}"}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)


