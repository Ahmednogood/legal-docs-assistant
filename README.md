# Legal Document Assistant 🤖📄

A powerful AI-powered assistant that helps users understand legal documents by answering questions in plain English and summarizing complex clauses.

> **Note:** Some UI elements (such as the upload button color) are currently not customizable due to Chainlit frontend limitations. This may change in future releases.

## Features ✨

- Upload and process legal documents (PDF, DOCX, TXT)
- Ask questions about the document content
- Get clear, concise answers with source citations
- Support for complex legal terminology
- Secure document processing

## Setup 🛠️

1. Clone the repository:

```bash
git clone <repository-url>
cd legal-docs-assistant
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
```

5. Run the application:

```bash
chainlit run main.py
```

## Usage 📝

1. Open your browser and navigate to `http://localhost:8000`
2. Upload a legal document (PDF, DOCX, or TXT)
3. Wait for the document to be processed
4. Ask questions about the document content
5. Get clear answers with source citations

## Requirements 📋

- Python 3.8+
- OpenAI API key
- Internet connection for API access

## Project Structure 📁

```
legal-docs-assistant/
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
├── .env                # Environment variables
├── .gitignore         # Git ignore file
├── README.md          # Project documentation
└── data/              # Directory for sample documents
```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
