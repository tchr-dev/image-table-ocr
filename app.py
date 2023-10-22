import gradio as gr
from utils import recongize_image

#
# Interface blocke
#

with gr.Blocks(0) as interface:
    title = gr.Label(value="Table Recognition", show_label=False)
    with gr.Row():
        with gr.Column():
            input_image = gr.Image(label="Input Image", type="numpy")
            recognize_btn = gr.Button("Recognize")
        with gr.Column():
            output_image = gr.Image(label="Output Image", type="numpy")
            output_text = gr.Textbox("Output Text")

#
# Action block
#
    recognize_btn.click(recongize_image, inputs=input_image, outputs=[output_image, output_text])


#
# Launch block
#
interface.launch()