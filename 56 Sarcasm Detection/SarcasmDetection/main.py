
import gradio as gr
from detection import clean_text, sarcasm_detection, subtype_detection


def greet(text):
    text = clean_text(text)
    print(text)
    label = sarcasm_detection(text)
    subtypes = None if label != 'Yes' else subtype_detection(text)

    return f"Sarcasm Detection: {label}", f"Sarcasm Subtype Classes: {subtypes}"


if __name__ == '__main__':
    iface = gr.Interface(
        fn=greet,
        inputs=gr.Textbox(label="Enter some text here", placeholder="Type here (text/tweet)..."),
        outputs=[gr.Textbox(label="Sarcasm Classification"), gr.Textbox(label="Sarcasm Subtype Classification")],
        title="Sarcasm Detector",
        allow_flagging='never'
    )


    # Launch the interface
    iface.launch()


