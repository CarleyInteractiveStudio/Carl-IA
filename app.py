import gradio as gr
from huggingface_hub import InferenceClient

# --- Configuration ---
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
SYSTEM_PROMPT = "You are a friendly and helpful chatbot named Carl IA."

# --- Chatbot Logic ---
# The hf_token is passed automatically by Gradio when the user logs in via the LoginButton.
def respond(message, history, hf_token: gr.OAuthToken):
    if not hf_token:
        raise gr.Error("Please log in with your Hugging Face account to use the chatbot.")

    client = InferenceClient(model=MODEL, token=hf_token)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

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
    # We add a sidebar for the login button, following the official HF template.
    with gr.Sidebar():
        gr.LoginButton()

    # The main content area for the chat.
    with gr.Column():
        gr.Markdown("<h1><center>Carl IA</center></h1>")

        gr.ChatInterface(
            respond,
            chatbot=gr.Chatbot(
                elem_classes="chatbot",
                type="messages" # This fixes the warning.
            ),
            textbox=gr.Textbox(
                placeholder="Enter your message and press enter",
                container=False,
                scale=8,
                elem_classes="textbox"
            ),
            # The token is now passed via the LoginButton, not here.
            submit_btn=None
        )

        with gr.Row():
            copy_btn = gr.Button("Copy Last Response", elem_classes=["button", "disabled-button"])
            call_btn = gr.Button("Call IA", elem_classes=["button", "disabled-button"])
            music_btn = gr.Button("Create Music", elem_classes=["button", "disabled-button"])
            image_btn = gr.Button("Create Image", elem_classes=["button", "disabled-button"])

        copy_btn.click(None, js=js_coming_soon)
        call_btn.click(None, js=js_coming_soon)
        music_btn.click(None, js=js_coming_soon)
        image_btn.click(None, js=js_coming_soon)

if __name__ == "__main__":
    demo.launch()
