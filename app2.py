import gradio as gr
from utils import recognize_image, recognize_cells, ocr_cells, ocr_crop_to_text

table_images = []
cells_images = [] # in ROWS!

#technical demo - flatten table
bordered_cell_images = []

#
# Functions block
#

async def handle_extract_table(input_image):
    global table_images  # Use the global table_images list
    table_images, output_text = recognize_image(input_image)  # Update table_images and get output_text
    return table_images, output_text


async def handle_extract_cells(input_images):
    global cells_images
    cells_images, output_text = recognize_cells(input_images)
    processed_images = [element for row in cells_images for element in row]    
    return processed_images
    # return output_text


async def copy_table():
    if table_images:
        return gr.Image(value=table_images[0])    
    else:
        return gr.Image()
    

async def handle_crop_to_text():
    global cells_images
    # output_images = ocr_crop_to_text()
    processed_images = [element for row in cells_images for element in row] 
    bordered_cell_images = ocr_crop_to_text(processed_images)
    return bordered_cell_images


async def handle_ocr():
    global cells_images
    processed_images = [element for row in cells_images for element in row]     
    text = ocr_cells(processed_images)
    return text
#
# Interface block
#

with gr.Blocks(0) as demo:
    title = gr.Label(value="Table Recognition", show_label=False)
    
    with gr.Tab("Table Extraction"):
    # ---------------------------
        with gr.Row():
            with gr.Column():
                input_image_page = gr.Image(label="Input Image", type="numpy")
                recognize_table_btn = gr.Button("Recognize")
            with gr.Column():
                # output_image = gr.Image(label="Output Image", type="numpy")
                output_images = gr.Gallery(label="Tables Images", elem_id="tables_gallery", columns=[2], rows=[2], object_fit="contain", height="auto")
                output_text = gr.Textbox("Output Text")
                copy_btn = gr.Button("Copy Image to Next Tab")
    # ---------------------------
    with gr.Tab("Cell Extraction"):
        with gr.Row():
            with gr.Column():
                input_image_table = gr.Image(label="Input Image", type="numpy")
                recognize_cells_btn = gr.Button("Recognize cells")
                recognized_text = gr.Textbox("Recognized Text")
            with gr.Column():
                output_cell_images = gr.Gallery(label="Cells Images", elem_id="cells_gallery", columns=[5], rows=[20], object_fit="contain", height="auto")
                process_cell_images = gr.Button("Process These Cell Images!")
                processed_cells_gallery = gr.Gallery(label="Processed Cells Images", elem_id="processed_cells_gallery", columns=[5], rows=[20], object_fit="contain", height="auto")
                ocr_button = gr.Button("Ocr This Text!")
                output_cells_text = gr.Textbox(label="Output Text")
                

#
# Action block
#
    recognize_table_btn.click(handle_extract_table, inputs=input_image_page, outputs=[output_images, output_text])
    copy_btn.click(copy_table, outputs=input_image_table)
    
    recognize_cells_btn.click(handle_extract_cells, inputs = input_image_table, outputs = [output_cell_images])
    process_cell_images.click(handle_crop_to_text, outputs=[processed_cells_gallery, output_cells_text])
    ocr_button.click(handle_ocr, outputs=recognized_text)


#
# Launch block
#
demo.launch(debug=True)