"""
Web interface for the Dutch Legal Assistant.
"""
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from src.test_legal_assistant import LegalAssistant
import uuid

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow all origins during development
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

# Initialize the legal assistant
legal_assistant = LegalAssistant()

@app.route('/')
def home():
    """Render the home page."""
    if 'conversation_id' not in session:
        session['conversation_id'] = str(uuid.uuid4())
        session['conversation_history'] = []
    return render_template('index.html', history=session['conversation_history'])

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a legal situation and return advice."""
    data = request.get_json()
    situation = data.get('situation', '')
    
    try:
        # Analyze the situation
        result = legal_assistant.analyze_situation(situation)
        
        # Format the response
        response = {
            'categories': result['relevant_categories'],
            'laws': result['relevant_laws'],
            'advice': result['advice'],
            'references': result['references']
        }
        
        # Add to conversation history
        history_entry = {
            'situation': situation,
            'response': response
        }
        session['conversation_history'].append(history_entry)
        session.modified = True
        
        return jsonify({'success': True, 'data': response})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear the conversation history."""
    session['conversation_history'] = []
    session.modified = True
    return jsonify({'success': True})

@app.route('/api/download-advice', methods=['POST'])
def download_advice():
    """Generate and download advice document."""
    data = request.get_json()
    situation = data.get('situation', '')
    result = legal_assistant.analyze_situation(situation)
    
    # Format the document content
    content = f"""
Legal Advice Report
==================

Situation
---------
{situation}

Relevant Categories
------------------
{', '.join(result['relevant_categories'])}

Relevant Laws
------------
{chr(10).join('- ' + law for law in result['relevant_laws'])}

Advice
------
{result['advice']}

References
----------
"""
    for ref in result['references']:
        content += f"""
{ref['name_of_law']} ({ref['citation_title']})
BWB ID: {ref['identification_number']}
Domain: {ref['legal_domain']}
Entry into force: {ref['date_of_entry_into_force']}
Regulatory authority: {ref['regulatory_authority']}
"""
    
    return jsonify({
        'success': True,
        'content': content,
        'filename': f"legal_advice_{session['conversation_id'][:8]}.txt"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 