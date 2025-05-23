import gradio as gr
import faiss
from transformers import BartForConditionalGeneration, BartTokenizer
import wikipedia

# Load BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

# FAISS Setup (For simplicity, assuming a prebuilt FAISS index is loaded)
index = faiss.IndexFlatL2(768)  # Example, modify as needed

def summarize_text(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_word(word):
    try:
        summary = wikipedia.summary(word, sentences=8)
    except wikipedia.exceptions.DisambiguationError as e:
        summary = f"Multiple meanings found: {e.options[:3]}... Please be more specific."
    except wikipedia.exceptions.PageError:
        summary = "No information found on Wikipedia."
    return summary

def summarize_document(file):
    with open(file.name, "r", encoding="utf-8") as f:
        doc_text = f.read()
    retrieved_info = "Relevant context from FAISS (Placeholder)"
    final_input = retrieved_info + " " + doc_text
    return summarize_text(final_input)

with gr.Blocks() as demo:
    gr.Markdown("## 📄Text Summarization using RAG")
    
    with gr.Row():
        option = gr.Radio(["Text Summarization", "Word Summarization", "Document Summarization"], label="Choose summarization type")
    
    input_text = gr.Textbox(label="Enter text or word")
    file_input = gr.File(label="Upload document (txt)")
    submit_btn = gr.Button("🔍 Summarize")
    output_text = gr.Textbox(label="Summarized Output", interactive=False)
    
    def process_request(choice, text, file):
        if choice == "Text Summarization":
            return summarize_text(text)
        elif choice == "Word Summarization":
            return summarize_word(text)
        elif choice == "Document Summarization" and file:
            return summarize_document(file)
        return "Invalid choice or missing input"
    
    submit_btn.click(process_request, inputs=[option, input_text, file_input], outputs=output_text)

demo.launch()