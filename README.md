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
   
## Usage Examples for Chat Modes

---

## 1. Document Chat

**What it does:**  
Searches local documents (text or Markdown files) that you have ingested into a vector database (ChromaDB) and returns relevant document fragments incrementally.

**Example Usage:**  
- **Test Query:** Enter "git stash" in the Document Chat input.
- **Expected Result:** A snippet from one of your text files (e.g., a brief description of LangGraph) will be displayed gradually, showing how the system retrieves relevant content.

---

## 2. LLM Chain Chat

**What it does:**  
Uses a predefined prompt template combined with an LLMChain to generate an answer to your query.

**Example Usage:**  
- **Test Query:** Enter "Explain the benefits of LangChain" in the LLM Chain Chat input.
- **Expected Result:** The model generates an answer based on the fixed prompt, providing a clear explanation of LangChain’s benefits.

---

## 3. LangGraph Flow Chat

**What it does:**  
Implements a multi-step workflow (Think → Act → Branch → Observe). It processes your input through several steps, and if a certain keyword (like "special") is detected, the flow follows an alternative branch.

**Example Usage:**  
- **Test Query:** Enter "Tell me something special" in the Flow Chat input.
- **Expected Result:** The graph processes the query through the steps; if the intermediate result includes the word "special", a special output branch is activated and you see an alternative final response.

---

## 4. Memory Chat

**What it does:**  
Maintains conversation history across multiple turns using persistent memory. Every message you send and every reply from the assistant is stored, so subsequent queries are processed with full context. This allows the system to generate more personalized and context-aware responses.

**Example Usage:**  
- **Test Query:**  
  Start with: "Hello, who are you?"  
  Then follow up with: "What do you know about me?"  
- **Expected Result:**  
  The chat remembers your earlier message ("Hello, who are you?") and uses that context when generating its reply to the follow-up query, resulting in answers that build upon the previous conversation.

---