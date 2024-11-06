import React, { useState } from 'react';

function App() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const askQuestion = async () => {
        const response = await fetch('http://127.0.0.1:5000/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();
        setAnswer(data.answer || 'Keine Antwort erhalten');
    };

    return (
        <div>
            <h1>RAG-System: Frage stellen</h1>
            <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Gib deine Frage ein"
            />
            <button onClick={askQuestion}>Frage senden</button>
            <p><strong>Antwort:</strong> {answer}</p>
        </div>
    );
}

export default App;
