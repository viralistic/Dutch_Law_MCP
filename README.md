# Dutch Legal Assistant (MCP)

A web-based legal assistant that helps users understand Dutch legislation and get advice on legal situations.

## Project Structure

This is a monorepo containing both the backend API (Flask) and frontend application (React):

```
Dutch_Law_MCP/
├── backend/           # Flask backend API
│   ├── src/
│   │   ├── models/   # Law models and parsers
│   │   ├── web/      # Flask application
│   │   └── ...
│   └── requirements.txt
├── frontend/         # React frontend application
│   ├── src/
│   ├── public/
│   └── package.json
└── README.md
```

## Backend Features

- Natural language processing of legal queries
- Analysis of legal situations based on Dutch law
- Categorization of legal issues
- Relevant law references and advice
- History tracking of queries
- Downloadable legal advice documents
- RESTful API endpoints

## Frontend Features

- Modern, responsive web interface
- Interactive legal query submission
- Real-time analysis results
- Downloadable advice documents
- Mobile-friendly design

## Installation

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
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

4. Start the Flask application:

```bash
PYTHONPATH=$PYTHONPATH:. python src/web/app.py
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

## Usage

1. Start both the backend and frontend servers following the installation instructions above.

2. Open your web browser and navigate to the frontend application (default: http://localhost:3000)

3. Use the interface to:
   - Enter your legal situation
   - Get analysis and advice
   - View relevant laws and references
   - Download detailed advice documents

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
