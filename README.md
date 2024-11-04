
# Document Query Application

This application is a Flask-based web interface that allows users to submit queries related to information stored in document files. The app reads content from `.txt`, `.pdf`, and `.docx` files stored in a specified folder, processes the content with a custom prompt, and returns concise answers tailored to the user's query.

## Prerequisites

1. **Python 3.x** installed on your system.
2. **Required Python Packages**: Install the following packages using `pip`:
   ```bash
   pip install flask pymupdf python-docx termcolor
   ```
3. **Ollama CLI** (for local model processing): Install [Ollama](https://ollama.com) and ensure it’s accessible at `C:\Users\abdul\AppData\Local\Programs\Ollama\ollama.exe`.

## Configuration

1. **Set the Document Folder**: Define the path to the folder containing your `.txt`, `.pdf`, and `.docx` files in the `DOCUMENTS_FOLDER` variable inside `app.py`:
   ```python
   DOCUMENTS_FOLDER = 'C:/path/to/your/documents'
   ```
2. **Verify Ollama Installation**: Ensure that Ollama is installed and accessible at the specified path.

3. **Custom Prompts (Optional)**: The script includes an array of prompts in the `PROMPTS` variable to tailor the response style. Adjust these prompts as desired for concise, focused, or direct responses.

## Running the Application

1. **Start the Flask Application**: Run the following command to start the app:
   ```bash
   python app.py
   ```
   You should see output similar to:
   ```plaintext
   * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
   ```

2. **Access the Web Interface**: Open a web browser and navigate to `http://127.0.0.1:5000`. Enter your query in the text field on the page, and the app will use the documents in the specified folder to generate a response.

## Usage Instructions

1. **Submitting a Query**: Enter a question or query into the input field, then click "Submit". The app will read content from the files in the `DOCUMENTS_FOLDER`, apply the chosen prompt, and return a concise answer based on the documents' information.

2. **Customizing the Prompt**: To modify the response style, you can edit the `PROMPTS` array in `app.py`. Example prompt modifications:
   ```python
   PROMPTS = [
       "Answer briefly and only with relevant information.",
       "Provide direct answers without additional context.",
       "Avoid mentioning unrelated topics."
   ]
   ```
   The prompts are automatically combined and applied to the query context.

## Troubleshooting

1. **Error Messages**: If you encounter `failed to get console mode` errors in the output, the script automatically filters these messages from the response.

2. **File Compatibility**: Ensure all files in the `DOCUMENTS_FOLDER` are either `.txt`, `.pdf`, or `.docx`. Unsupported file types in the folder are ignored.

3. **Console Output**: The combined prompt and query are displayed in red in the console for debugging purposes.

## Example Usage

1. Place files like `product_info.txt`, `installation_guide.pdf`, and `support_info.docx` in your specified document folder.
2. Open the web interface and enter a query, such as:
   ```
   "What is the return policy for the products?"
   ```
3. The application will return a response based on the content in the provided files.

## Stopping the Application

Press `CTRL+C` in the terminal where the Flask app is running to stop the server.

