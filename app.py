import streamlit as st
import requests
from utils import read_file

# Set page_config
st.set_page_config(
    page_title="Workcohol AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - styling
st.markdown("""
    <style>
    /* Background styling */
    .stApp {
        background-image: url('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXJmYnNscXVjZmQxamNiYjRlNGc3NTYzdmg4ejZ6aHB2d244cmIxOSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/u1WhXLjwgcXpHJBMRM/giphy.gif');
        background-size: 100% 100%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
        width: 100%;
    }
    
    /* styling of Main container */
    .main {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        min-height: calc(100vh - 2rem);
    }
    
    /* Logo styling */
    .logo-container {
        background-color: #dc3545;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .logo-text {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Title styling */
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Subtitle styling */
    .subtitle-text {
        font-size: 1.2rem;
        color: #fff;
        margin-bottom: 2rem;
    }
    
    /* styling of Input field */
    .stTextInput>div>div>input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 8px;
        border: 2px solid #E5E7EB;
        background-color: rgba(255, 255, 255, 0.9);
    }
    
    /* styling of Button */
    .stButton>button {
        width: 100%;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 8px;
        background-color: #dc3545;
        color: white;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #bb2d3b;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    /* styling Chat message */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        background-color: rgba(255, 255, 255, 0.95);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background-color: rgba(239, 246, 255, 0.95);
        border-left: 4px solid #dc3545;
    }
    
    .bot-message {
        background-color: rgba(243, 244, 246, 0.95);
        border-left: 4px solid #4B5563;
    }
    
    /* styling File uploader */
    .stFileUploader>div>div>button {
        background-color: rgba(243, 244, 246, 0.9);
        color: #fff;
        border: 2px dashed #D1D5DB;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* styling Spinner */
    .stSpinner>div {
        border-color: #dc3545;
    }
    
    /* styling Error message */
    .stAlert {
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.95);
    }
    
    /* styling Sidebar */
    .css-1d391kg {
        background-color: rgba(248, 249, 250, 0.95);
    }
    
    /* Make sure all text is readable */
    .stMarkdown, .stText {
        color: #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <h1 class="logo-text">Workcohol</h1>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    Workcohol's AI Assistant helps you get quick answers to your questions. 
    Upload any document to enhance the context of your queries.
    """)
    st.markdown("---")
    st.markdown("### Supported File Types")
    st.markdown("""
    - 📄 Text Files (.txt)
    - 📑 PDF Documents (.pdf)
    - 📊 JSON Files (.json)
    - 📈 CSV Files (.csv)
    """)

# Main content
st.markdown('<h1 class="title-text">🤖 Workcohol AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Your intelligent workplace companion</p>', unsafe_allow_html=True)

# Initializing  session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Creating two columns for the input area
col1, col2 = st.columns([3, 1])

with col1:
    query = st.text_input("Ask your question:", key="query_input", placeholder="Type your question here...")

with col2:
    uploaded_file = st.file_uploader("📎 Upload File", type=["txt", "pdf", "json", "csv"])

# Send button
if st.button("Send Message", key="send_button"):
    if not query.strip():
        st.warning("Please enter a question!")
    else:
        try:
            # Showing loading spinner
            with st.spinner("🤔 Thinking..."):
                # Prepare file data if uploaded
                file_data = read_file(uploaded_file) if uploaded_file else None
                
                # Make API request
                res = requests.post(
                    "http://localhost:8000/chat/",
                    json={
                        "query": query,
                        "user_file": file_data
                    },
                    timeout=30
                )
                
                # Handling  response
                if res.ok:
                    response = res.json()["response"]
                    # Add to chat history
                    st.session_state.chat_history.append({"query": query, "response": response})
                else:
                    st.error(f"Error: {res.status_code} - {res.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Please make sure the FastAPI server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# chat history Display
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation History")
    for chat in st.session_state.chat_history:
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {chat['query']}
        </div>
        """, unsafe_allow_html=True)
        
        # message from bot
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>AI Assistant:</strong><br>
            {chat['response']}
        </div>
        """, unsafe_allow_html=True)