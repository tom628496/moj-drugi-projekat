from PIL import Image, ImageFile
import os
import re

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

def create_image_grid(input_folder, output_filename):
    images = []
    row = 8
    rows = row+1
    cols = 7
    output_image_size = (cols * 2000, rows * 2000) 

    image_files = [f for f in os.listdir(input_folder) if f.endswith(".jpg") or f.endswith(".png")]
    image_files.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf'))  
    for filename in image_files:
        try:
            img = Image.open(os.path.join(input_folder, filename))
            img = img.resize((output_image_size[0] // cols, output_image_size[1] // rows), Image.BICUBIC)  
            images.append(img)
        except PIL.Image.DecompressionBombError:
            print(f"Skipping image {filename} due to DecompressionBombError.")

    grid_image = Image.new('RGB', (output_image_size[0], output_image_size[1] + 180), color='white')  

    for i in range(len(images)+cols):
        row_position = i // cols if i >= cols else i // cols + 1 
        grid_image.paste(images[i-7], (i % cols * output_image_size[0] // cols, row_position * output_image_size[1] // rows))

    output_path = os.path.join(input_folder, output_filename)
    grid_image.save(output_path)

input_folder = "input_folder"
output_filename = "output_image.jpg"

create_image_grid(input_folder, output_filename)