# Dutch Legal Assistant (MCP)

A web-based legal assistant that helps users understand Dutch legislation and get advice on legal situations.

## Features

- Natural language processing of legal queries
- Analysis of legal situations based on Dutch law
- Categorization of legal issues
- Relevant law references and advice
- History tracking of queries
- Downloadable legal advice documents
- Modern, responsive web interface

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Dutch_Law_MCP.git
cd Dutch_Law_MCP
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:

```bash
PYTHONPATH=$PYTHONPATH:. python src/web/app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5000
```

3. Enter your legal situation in the text area and click "Analyze" or press Ctrl/Cmd + Enter.

4. View the analysis results, including:

   - Relevant legal categories
   - Applicable laws
   - Legal advice
   - References

5. Download the legal advice as a text document using the "Download Advice" button.

6. Clear your query history using the "Clear History" button.

## Project Structure

```
src/
├── web/
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── script.js
│   └── app.py
├── models/
│   ├── law_model.py
│   └── wetten_parser.py
└── legal_assistant.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
