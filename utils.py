from table_ocr import extract_tables, extract_cells, ocr_to_csv
import numpy as np
import cv2
import math, itertools
import pytesseract


def recognize_image(input_image):

    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)

    table_images = extract_tables.find_tables(grayscale_image)

    output_text = f"Success! There ar {len(table_images)} images."

    return table_images, output_text


def recognize_cells(input_images):
  
    # Convert to grayscale
    if input_images.ndim > 2:
        grayscale_image = cv2.cvtColor(input_images, cv2.COLOR_BGR2GRAY)
    else:
        grayscale_image = input_images

    # output_images = extract_cells.extract_cell_images_from_table(grayscale_image)
    cell_images = extract_cells.extract_cell_images_from_table(grayscale_image)
    # print(cell_images)
    # cell_images = list(itertools.chain.from_iterable(output_images))
    # list(itertools.chain.from_iterable())
    # cell_images = [ocr_image.crop_to_text(image) for image in output_images]

    output_text = f"Success! {len(cell_images)}"

    return cell_images, output_text
    # return output_text


def ocr_crop_to_text(input_images):

    text = f"This list is Multidemensional {is_multi_dimensional(input_images)}"
    # print_list_structure(input_images)
    output_images = []

    for i, image in enumerate(input_images):
        # text += f"Num:{i}, size: {len(image)}, type: {type(image)}"
        # Convert to grayscale
        if image.ndim > 2:
          grayscale_image = cv2.cvtColor(input_images, cv2.COLOR_BGR2GRAY)
        else:
          grayscale_image = image
        output_images.append(grayscale_image)

    return output_images, text

def ocr_cells(images):
    tess_args = ["--psm", "7", "-l", "chi_sim+eng"]   
    output_text = ""
    for i, image in enumerate(images):        
        color_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # print(ocr_image.ocr_image(color_image, tess_args))
        # output_text += ocr_image.ocr_image(color_image, config=tess_args) 
        output_text += pytesseract.image_to_string(color_image, config=" ".join(tess_args))
        # print(txt)
        # output_text =+ txt
        # output_text += f"Step {i}, type:{type(color_image)} , dim: {color_image.ndim}\n"
        # output_text += pytesseract.image_to_string(color_image)
        # output_text += "\n" 
    
    return output_text

#----------------------------------------------------------------------
def combine_images_in_grid(images):
    # Determine grid size
    n = len(images)
    grid_size = math.ceil(math.sqrt(n))

    # Resize images to the smallest width and height among all images
    min_height = min(img.shape[0] for img in images)
    min_width = min(img.shape[1] for img in images)
    resized_images = [cv2.resize(img, (min_width, min_height)) for img in images]

    # Pad the images list with blank images if necessary
    while len(resized_images) < grid_size * grid_size:
        blank_img = np.ones((min_height, min_width, 3), dtype=np.uint8) * 255  # white image
        resized_images.append(blank_img)

    # Form the grid
    rows = []
    for i in range(0, len(resized_images), grid_size):
        rows.append(np.hstack(resized_images[i:i+grid_size]))
    grid_combined = np.vstack(rows)

    return grid_combined


def is_multi_dimensional(lst):
    if not isinstance(lst, list):
        return False  # Not a list

    if not lst:
        return True  # An empty list is considered multi-dimensional

    # Check if any element in the list is itself a list (recursively)
    return any(isinstance(item, list) for item in lst)


def print_list_structure(lst, level=0):
    for item in lst:
        if isinstance(item, list):
            print("  " * level + "List:")
            print_list_structure(item, level + 1)
        else:
            print("  " * level + f"Item: {item}")