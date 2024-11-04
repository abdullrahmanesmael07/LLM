from flask import Flask, render_template, request
import subprocess
from docx import Document
import fitz  # PyMuPDF
from plyer import notification
import os
import re
from termcolor import colored

app = Flask(__name__)


# Array of custom prompts to control response style
PROMPTS = [
    "Be concise. Answer only with specific information requested without additional context.",
    "Focus only on the product specified and avoid mentioning others.",
    "Respond directly and briefly, using fewer words to convey the answer.",
    "Provide the information as briefly as possible without detailed explanations.",
]

def save_uploaded_files(files):
    """Save uploaded files to the UPLOAD_FOLDER and return their paths."""
    file_paths = []
    for file in files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        file_paths.append(file_path)
    return file_paths

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Your Custom App Name",  # Set your own app name
        timeout=5
    )

def extract_text_from_files(file_paths):
    """Extract and return concatenated text from multiple files."""
    content = []
    for file_path in file_paths:
        try:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content.append(f.read())
            elif file_path.endswith('.pdf'):
                with fitz.open(file_path) as pdf:
                    pdf_text = "\n".join(page.get_text() for page in pdf)
                    content.append(pdf_text)
            elif file_path.endswith('.docx'):
                doc = Document(file_path)
                doc_text = "\n".join(para.text for para in doc.paragraphs)
                content.append(doc_text)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        finally:
            os.remove(file_path)  # Clean up file after processing
    return "\n".join(content)

def clean_text(text):
    """Remove non-printable characters and control sequences from text."""
    return re.sub(r'[^\x20-\x7E\n]+', '', text)

def run_ollama_query(query):
    """Run the ollama command and return the cleaned output."""
    print(colored("run ollama query", 'red'))
    process = subprocess.Popen(
        ["C:\\Users\\abdul\\AppData\\Local\\Programs\\Ollama\\ollama.exe", "run", "mistral", query],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    print(colored("run query", 'red'))
    output, error = process.communicate()
    print(colored("run ", 'red'))
    return clean_text(output), clean_text(error)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        query = request.form['query']

        files = request.files.getlist('files')

        
        # Step 1: Save uploaded files and extract text
        file_paths = save_uploaded_files(files)

        document_text = extract_text_from_files(file_paths)

        
        # Step 2: Combine chosen prompt, document text, and user query
        chosen_prompt = ""

        for i in PROMPTS:

            chosen_prompt += i

        combined_query = f"{chosen_prompt}\n\n{document_text}\n\nUser Query: {query}".strip()
        # Step 3: Run ollama query and capture output
        output, error = run_ollama_query(combined_query)
        
        # Step 4: Prepare the response
        response =  output.strip()

        search_sentence = "failed to get console mode for stdout: The handle is invalid. failed to get console mode for stderr: The handle is invalid. "
        response = response[response.find(search_sentence) + len(search_sentence):].strip()

        print(colored("-----------0----------", 'red'))
        print(colored(response, 'yellow'))
        print(colored("-----------1----------", 'red'))

        send_notification("Query", "Answer is ready!")


    
    return render_template('index.html', response=response)

if __name__ == '__main__':
    print(colored("Welcome", 'red'))
    app.run(debug=True)
