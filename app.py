import gradio as gr
from huggingface_hub import InferenceClient

# --- Configuration ---
# We will use the Mistral-7B-Instruct-v0.2 model, which is powerful,
# commercially usable, and available on the free Hugging Face Inference API.
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
SYSTEM_PROMPT = "You are a friendly and helpful chatbot named Carl IA."

# --- Inference API Client ---
# The hf_token is automatically provided by Gradio when the user logs in.
def get_client(hf_token: gr.OAuthToken):
    return InferenceClient(model=MODEL, token=hf_token.token if hf_token else None)

# --- Chatbot Logic ---
def predict(message, history, hf_token: gr.OAuthToken):
    client = get_client(hf_token)

    # Format the history for the API
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

    # Stream the response from the API
    response_stream = ""
    for token in client.chat_completion(messages, max_tokens=1000, stream=True):
        if token.choices:
            response_stream += token.choices[0].delta.content or ""
            yield response_stream

# --- JavaScript for "Coming Soon" Buttons ---
js_coming_soon = """
function() {
    alert('This feature is coming soon!');
}
"""

# --- Gradio Interface ---
with gr.Blocks(css="style.css") as demo:
    gr.Markdown("<h1><center>Carl IA</center></h1>")

    chatbot = gr.Chatbot(elem_classes="chatbot", type="messages")

    with gr.Row():
        msg = gr.Textbox(
            show_label=False,
            placeholder="Enter your message and press enter",
            container=False,
            scale=8,
            elem_classes="textbox"
        )

    with gr.Row():
        clear = gr.Button("Clear Conversation", elem_classes=["button", "primary-button"])
        copy_btn = gr.Button("Copy Last Response", elem_classes=["button", "disabled-button"])
        call_btn = gr.Button("Call IA", elem_classes=["button", "disabled-button"])
        music_btn = gr.Button("Create Music", elem_classes=["button", "disabled-button"])
        image_btn = gr.Button("Create Image", elem_classes=["button", "disabled-button"])

    # OAuth token for Hugging Face API
    hf_token = gr.OAuthToken()

    # --- Event Handlers ---
    msg.submit(predict, [msg, chatbot, hf_token], chatbot)
    clear.click(lambda: [], None, chatbot, queue=False)

    # Attach "coming soon" JavaScript to the disabled buttons
    copy_btn.click(None, js=js_coming_soon)
    call_btn.click(None, js=js_coming_soon)
    music_btn.click(None, js=js_coming_soon)
    image_btn.click(None, js=js_coming_soon)

if __name__ == "__main__":
    demo.launch()
