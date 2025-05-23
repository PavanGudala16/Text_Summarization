import gradio as gr
import PyPDF2
import docx
from transformers import pipeline
import wikipediaapi
from nltk.corpus import wordnet

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize Wikipedia API
wiki = wikipediaapi.Wikipedia(user_agent="TextSummarizationApp/1.0", language="en")

def text_summarization(mode, summary_type, text=None, file=None, word=None):
    def summarize_text(text):
        if summary_type == "Precise":
            return summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        elif summary_type == "Bullet Points":
            summary = summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
            bullet_points = summary.split('. ')
            bullet_points = [point.strip() for point in bullet_points if point]
            return "\n- " + "\n- ".join(bullet_points[:4])  # Limit to 3-4 points
        elif summary_type == "Detailed":
            return summarizer(text, max_length=250, min_length=100, do_sample=False)[0]['summary_text']
        return "Invalid summarization type."

    if mode == "Paragraph Summarization" and text:
        return summarize_text(text)

    elif mode == "Document Summarization" and file:
        if file.name.endswith(".txt"):
            doc_text = file.read().decode("utf-8")
        elif file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(file)
            doc_text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif file.name.endswith(".docx"):
            doc = docx.Document(file)
            doc_text = " ".join([para.text for para in doc.paragraphs])
        else:
            return "Unsupported file format"
        return summarize_text(doc_text)

    elif mode == "Lexical Analyzer" and word:
        page = wiki.page(word)
        if page.exists():
            summary = page.summary[:1000]  # Get the first 1000 characters
            last_period = summary.rfind(". ")  # Find the last full stop before 1000 characters
            if last_period != -1:
                summary = summary[:last_period+1]  # Trim at the last full stop
            return summary

        synsets = wordnet.synsets(word)
        if synsets:
            return f"Definition: {synsets[0].definition()}\nExample: {synsets[0].examples()[0] if synsets[0].examples() else 'No example available'}"
        return "No information found for this word."

    return "Invalid input. Please provide the required data."

with gr.Blocks(css="""
    body { background-color: #000000; color: #FFFFFF; }
    .container { max-width: 800px; margin: auto; }
    h1 { color: #FF69B4; text-align: center; }
    label { font-weight: bold; color: #00FF7F; }
    button { background-color: #98FB98; color: black; font-weight: bold; }
    button:hover { background-color: #90EE90; }
    .gradio-container { padding: 20px; border-radius: 10px; background: #222; box-shadow: 0px 4px 6px rgba(255, 255, 255, 0.1); }
""") as demo:
    gr.Markdown("""
    # 📚 HYBRID SUMMARIZTION TOOL : A RAG BASED APPROACH 📚
    Select a summarization type and provide input accordingly.
    """, elem_classes=["text-center", "text-2xl", "font-bold", "mb-5"])

    mode = gr.Radio(["Paragraph Summarization", "Document Summarization", "Lexical Analyzer"],
                    label="Choose Summarization Type", interactive=True, elem_classes=["mb-4"])
    summary_type = gr.Radio(["Precise", "Bullet Points", "Detailed"],
                            label="Choose Output Type (Only for Paragraph/Document)", interactive=True, elem_classes=["mb-4"], visible=False)

    text_input = gr.Textbox(label="📝 Enter Paragraph", interactive=True, visible=False)
    file_input = gr.File(label="📂 Upload Document", visible=False)
    word_input = gr.Textbox(label="🔍 Enter a Word", interactive=True, visible=False)

    def update_inputs(selected_mode):
        return {
            text_input: gr.update(visible=selected_mode == "Paragraph Summarization"),
            file_input: gr.update(visible=selected_mode == "Document Summarization"),
            word_input: gr.update(visible=selected_mode == "Lexical Analyzer"),
            summary_type: gr.update(visible=selected_mode in ["Paragraph Summarization", "Document Summarization"])
        }

    mode.change(update_inputs, inputs=[mode], outputs=[text_input, file_input, word_input, summary_type])

    submit_btn = gr.Button("✨ Summarize")
    clear_btn = gr.Button("❌ Clear")

    output = gr.Textbox(label="📝 Summarization Output", interactive=False)

    submit_btn.click(fn=text_summarization, inputs=[mode, summary_type, text_input, file_input, word_input], outputs=output)
    clear_btn.click(fn=lambda: "", inputs=[], outputs=output)

demo.launch()