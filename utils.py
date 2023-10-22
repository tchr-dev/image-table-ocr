from table_ocr import extract_tables
import numpy as np
import cv2
import math

def recongize_image(input_image):
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    images = extract_tables.find_tables(grayscale_image)
    output_image = combine_images_in_grid(images)
    # output_image = images[0]
    output_text = "Success!"
    return [output_image, output_text]


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


# import math
# import numpy as np
# import cv2

# def combine_images_in_grid(images):
#     if not images:
#         raise ValueError("No images provided.")

#     # Determine grid size
#     n = len(images)
#     grid_size = math.ceil(math.sqrt(n))

#     # Ensure the provided items in the list are valid numpy images
#     for img in images:
#         if not isinstance(img, np.ndarray) or len(img.shape) != 3:
#             raise ValueError("All items in the images list must be valid numpy images.")

#     # Resize images to the smallest width and height among all images
#     min_height = min(img.shape[0] for img in images)
#     min_width = min(img.shape[1] for img in images)
#     resized_images = [cv2.resize(img, (min_width, min_height)) for img in images]

#     # Pad the images list with blank images if necessary
#     while len(resized_images) < grid_size * grid_size:
#         blank_img = np.ones((min_height, min_width, 3), dtype=np.uint8) * 255  # white image
#         resized_images.append(blank_img)

#     # Form the grid
#     rows = []
#     for i in range(0, len(resized_images), grid_size):
#         rows.append(np.hstack(resized_images[i:i+grid_size]))
#     grid_combined = np.vstack(rows)

#     return grid_combined

# # Sample Usage:
# try:
#     # ... code to obtain the list of numpy images ...
#     result = combine_images_in_grid(images_list)
# except ValueError as e:
#     print(f"Error: {e}")
