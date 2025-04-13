# AI Test Project

A simple multi-mode LLM application built with Streamlit. It demonstrates:
- **Document Chat:** local document retrieval
- **LLM Chain Chat:** prompt-based Q&A
- **Flow Chat:** multi-step logic (Think → Act → Branch → Observe)
- **Memory Chat:** conversation history

## Setup & Installation

1. **Clone & Enter Folder**:
   ```bash
   git clone https://github.com/1JigSaW/AITest.git
   cd AITest
   ```

2. **Virtual Env**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Deps**:
   ```bash
   pip install -r requirements.txt
   ```
   
4. **.env**:
   ```bash
   Create .env in the root with your OPENAI_API_KEY
   ```
   
5. **Run the Interface**:
   ```bash
   streamlit run main.py
   ```