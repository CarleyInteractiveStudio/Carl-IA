import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# --- Configuration ---
# We are switching to a model that runs directly on the Space.
# microsoft/DialoGPT-medium is a good conversational model that is small
# enough to have a chance of running on the free CPU hardware.
# This completely removes the need for an API key or user login.
# We are using a model specifically trained for Spanish.
MODEL_NAME = "datificate/gpt2-small-spanish"

# --- Model Loading ---
# This happens once when the app starts. It might be slow.
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
chat_history_ids = {} # Dictionary to store conversation histories

# --- Chatbot Logic ---
def predict(message, history, session_id="default"):
    history = history or []

    # Encode the new user input
    new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')

    # Append the new user input tokens to the chat history
    # We use a global dictionary to keep track of the conversation tensors
    past_user_inputs = chat_history_ids.get(session_id)
    bot_input_ids = torch.cat([past_user_inputs, new_user_input_ids], dim=-1) if past_user_inputs is not None else new_user_input_ids

    # Generate a response
    # The model will generate a response up to 1000 tokens
    chat_history_ids[session_id] = model.generate(
        bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )

    # Decode the response
    response = tokenizer.decode(chat_history_ids[session_id][:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Add the conversation to the Gradio history
    history.append((message, response))

    return history, history

# --- JavaScript for "Coming Soon" Buttons ---
js_coming_soon = """
function() {
    alert('This feature is coming soon!');
}
"""

# --- Gradio Interface ---
with gr.Blocks(css="style.css") as demo:
    with gr.Column():
        gr.Markdown("<h1><center>Carl IA</center></h1>")

        chatbot = gr.Chatbot(
            elem_id="chatbot",
            bubble_full_width=False,
            elem_classes="chatbot"
        )

        history_state = gr.State([])

        with gr.Row():
            txt = gr.Textbox(
                scale=8,
                show_label=False,
                placeholder="Enter your message and press enter",
                container=False,
                elem_classes="textbox"
            )

        with gr.Row():
            copy_btn = gr.Button("Copy Last Response", elem_classes=["button", "disabled-button"])
            call_btn = gr.Button("Call IA", elem_classes=["button", "disabled-button"])
            music_btn = gr.Button("Create Music", elem_classes=["button", "disabled-button"])
            image_btn = gr.Button("Create Image", elem_classes=["button", "disabled-button"])

        txt.submit(predict, [txt, history_state], [chatbot, history_state])

        copy_btn.click(None, js=js_coming_soon)
        call_btn.click(None, js=js_coming_soon)
        music_btn.click(None, js=js_coming_soon)
        image_btn.click(None, js=js_coming_soon)

if __name__ == "__main__":
    demo.launch()
