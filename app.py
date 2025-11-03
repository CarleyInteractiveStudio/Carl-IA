import gradio as gr
from huggingface_hub import InferenceClient

# --- Configuration ---
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
SYSTEM_PROMPT = "You are a friendly and helpful chatbot named Carl IA."

# --- Chatbot Logic ---
# The hf_token is passed from the LoginButton. We've added it as an explicit input to our submit event.
def predict(message, history, hf_token):
    # Check if the user is logged in.
    if not hf_token:
        raise gr.Error("Please log in with your Hugging Face account to use the chatbot.")

    client = InferenceClient(model=MODEL, token=hf_token)

    # Format the history for the API. History is a list of [user, assistant] pairs.
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
            # The history object is a list of lists, so we update the last assistant message.
            history[-1][1] = response_stream
            yield history

def user(user_message, history):
    """Adds the user's message to the chat history."""
    return "", history + [[user_message, None]]

# --- JavaScript for "Coming Soon" Buttons ---
js_coming_soon = """
function() {
    alert('This feature is coming soon!');
}
"""

# --- Gradio Interface ---
with gr.Blocks(css="style.css") as demo:
    with gr.Sidebar():
        # The LoginButton provides the hf_token.
        hf_token = gr.LoginButton()

    with gr.Column():
        gr.Markdown("<h1><center>Carl IA</center></h1>")

        # We create the chatbot window manually.
        chatbot = gr.Chatbot(
            elem_id="chatbot",
            bubble_full_width=False,
            elem_classes="chatbot"
        )

        # We create the textbox for user input.
        with gr.Row():
            txt = gr.Textbox(
                scale=8,
                show_label=False,
                placeholder="Enter your message and press enter",
                container=False,
                elem_classes="textbox"
            )

        # We create our custom "coming soon" buttons.
        with gr.Row():
            copy_btn = gr.Button("Copy Last Response", elem_classes=["button", "disabled-button"])
            call_btn = gr.Button("Call IA", elem_classes=["button", "disabled-button"])
            music_btn = gr.Button("Create Music", elem_classes=["button", "disabled-button"])
            image_btn = gr.Button("Create Image", elem_classes=["button", "disabled-button"])

        # This is the crucial part: we manually define what happens when the user submits a message.
        txt.submit(user, [txt, chatbot], [txt, chatbot], queue=False).then(
            predict, [chatbot, hf_token], chatbot
        )

        # Attach JavaScript to the custom buttons
        copy_btn.click(None, js=js_coming_soon)
        call_btn.click(None, js=js_coming_soon)
        music_btn.click(None, js=js_coming_soon)
        image_btn.click(None, js=js_coming_soon)

if __name__ == "__main__":
    demo.launch()
