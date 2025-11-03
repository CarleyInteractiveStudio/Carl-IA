import gradio as gr
from huggingface_hub import InferenceClient

# --- Configuration ---
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
SYSTEM_PROMPT = "You are a friendly and helpful chatbot named Carl IA."

# --- Chatbot Logic ---
# This function is designed to work with gr.ChatInterface, which handles history automatically.
def respond(message, history, hf_token: gr.OAuthToken):
    # If the user is not logged in, hf_token will be None.
    if not hf_token:
        raise gr.Error("Please log in with your Hugging Face account to use the chatbot.")

    client = InferenceClient(model=MODEL, token=hf_token)

    # The history from ChatInterface comes as a list of tuples [user, assistant].
    # We need to convert it to the format the API expects.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})
    messages.append({"role": "user", "content": message})

    # Stream the response
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
# We use gr.Blocks to combine the standard ChatInterface with our custom layout.
with gr.Blocks(css="style.css") as demo:
    gr.Markdown("<h1><center>Carl IA</center></h1>")

    # Use the official ChatInterface for robust functionality
    gr.ChatInterface(
        respond,
        chatbot=gr.Chatbot(elem_classes="chatbot", bubble_full_width=False),
        textbox=gr.Textbox(
            placeholder="Enter your message and press enter",
            container=False,
            scale=8,
            elem_classes="textbox"
        ),
        # Pass the token implicitly via the function signature
        additional_inputs=[gr.OAuthToken()],
        submit_btn=None, # Hide the default submit button
        clear_btn=gr.Button("Clear Conversation", elem_classes=["button", "primary-button"]),
        examples=[["Hello!", None], ["How are you?", None]]
    )

    # Add our custom "coming soon" buttons in a separate row
    with gr.Row():
        copy_btn = gr.Button("Copy Last Response", elem_classes=["button", "disabled-button"])
        call_btn = gr.Button("Call IA", elem_classes=["button", "disabled-button"])
        music_btn = gr.Button("Create Music", elem_classes=["button", "disabled-button"])
        image_btn = gr.Button("Create Image", elem_classes=["button", "disabled-button"])

    # Attach the JavaScript alert to our custom buttons
    copy_btn.click(None, js=js_coming_soon)
    call_btn.click(None, js=js_coming_soon)
    music_btn.click(None, js=js_coming_soon)
    image_btn.click(None, js=js_coming_soon)

if __name__ == "__main__":
    demo.launch()
