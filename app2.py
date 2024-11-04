from flask import Flask, render_template, request
import subprocess
from docx import Document
import fitz  # PyMuPDF
from plyer import notification
import os
import re
from termcolor import colored

app = Flask(__name__)

# Define folder path and prompt for queries
DOCUMENTS_FOLDER = 'data'
PROMPT = " ".join([
    "Be concise. Answer only with specific information requested without additional context.",
    "Focus only on the product specified and avoid mentioning others.",
    "Respond directly and briefly, using fewer words to convey the answer.",
    "Provide the information as briefly as possible without detailed explanations.",
])

def extract_text_from_files():
    """Extract text from all supported files in DOCUMENTS_FOLDER."""
    content = []
    for filename in os.listdir(DOCUMENTS_FOLDER):
        file_path = os.path.join(DOCUMENTS_FOLDER, filename)
        try:
            if filename.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content.append(f.read())
            elif filename.endswith('.pdf'):
                with fitz.open(file_path) as pdf:
                    content.append("\n".join(page.get_text() for page in pdf))
            elif filename.endswith('.docx'):
                doc = Document(file_path)
                content.append("\n".join(para.text for para in doc.paragraphs))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return "\n".join(content)

def clean_text(text):
    """Remove non-printable characters and control sequences from text."""
    return re.sub(r'[^\x20-\x7E\n]+', '', text)

def run_ollama_query(query):
    """Run the Ollama command with the query and return cleaned output."""
    try:
        process = subprocess.Popen(
            ["C:\\Users\\abdul\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "mistral", query],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        output, _ = process.communicate()
        return clean_text(output)
    except Exception as e:
        print(f"Error executing query: {e}")
        return "Error in processing the query."

def send_notification(title, message):
    """Send a desktop notification."""
    notification.notify(title=title, message=message, app_name="Query Application", timeout=5)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        query = request.form['query']
        
        # Prepare the combined query with prompt, document text, and user input
        combined_query = prepare_query(query)
        
        # Run the query and process the response
        raw_response = run_ollama_query(combined_query)
        response = process_response(raw_response)

        # Send a notification when the answer is ready
        send_notification("Query", "Answer is ready!")

    # Render the template with the response
    return render_template('index2.html', response=response)

def prepare_query(query):
    
    document_text = extract_text_from_files()
    combined_query = f"{PROMPT}\n\n{document_text}\n\nUser Query: {query}".strip()
    print(colored(combined_query, 'red'))  # Debugging display of the combined query
    return combined_query

def process_response(raw_response):

    unwanted_text = "failed to get console mode for stdout: The handle is invalid. failed to get console mode for stderr: The handle is invalid."

    if unwanted_text in raw_response:
        response = raw_response.split(unwanted_text)[-1].strip()
    else:
        response = raw_response.strip()
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
