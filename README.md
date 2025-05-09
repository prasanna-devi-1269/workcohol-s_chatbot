# Custom Chatbot with Streamlit and FastAPI

This is a custom chatbot that uses Google's Gemini Pro and Hugging Face's FLAN-T5 models to answer questions based on a sample dataset and user-uploaded files.

## Features

- Chat interface using Streamlit
- Support for multiple file formats (PDF, TXT, JSON)
- Integration with Google's Gemini Pro and Hugging Face's FLAN-T5
- FastAPI backend for robust API handling
- Fallback mechanism if primary model fails

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Google Gemini API key:
```
GOOGLE_GEMINI_KEY=your_api_key_here
```

## Running the Application

1. Start the FastAPI backend:
```bash
uvicorn main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run streamlit_app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## Usage

1. The chatbot will automatically load the sample.json dataset
2. You can upload additional files (PDF, TXT, JSON) using the file uploader
3. Type your questions in the chat input and press Enter or click Send
4. The chatbot will respond using both the sample data and any uploaded files

## Requirements

- Python 3.12.4
- All dependencies listed in requirements.txt
- Google Gemini API key 
