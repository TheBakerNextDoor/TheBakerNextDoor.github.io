from PIL import Image
import base64
import os

# Define source and output folders
source_folder = 'static/source'
output_folder = 'static/cata'

# Define the filename suffixes
thumbnail_suffix = '-thumb'
original_suffix = '-original'

# Define the cropping percentage
crop_percentage = 5

# Define the name of the HTML output file
html_output_file = 'gallery.html'

# Function to process and save images
def process_images(src_folder, dst_folder, html_output_file):
    with open(html_output_file, 'w') as html_file:
        for root, _, files in os.walk(src_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    source_image_path = os.path.join(root, file)
                    relative_path = os.path.relpath(source_image_path, src_folder)
                    output_subfolder = os.path.dirname(relative_path)
                    output_subfolder_path = os.path.join(dst_folder, output_subfolder)

                    # Create subfolders in the output directory if they don't exist
                    os.makedirs(output_subfolder_path, exist_ok=True)

                    # Open the source image file
                    original_image = Image.open(source_image_path)

                    # Calculate the cropping amounts
                    original_width, original_height = original_image.size
                    crop_amount = int(min(original_width, original_height) * (crop_percentage / 100))

                    # Crop the image
                    left = top = crop_amount
                    right = original_width - crop_amount
                    bottom = original_height - crop_amount
                    cropped_image = original_image.crop((left, top, right, bottom))

                    # Calculate the new width while maintaining the aspect ratio
                    new_width = 500
                    new_height = int(cropped_image.height * (new_width / cropped_image.width))

                    # Resize the cropped image to the new size
                    resized_image = cropped_image.resize((new_width, new_height))

                    # Create a new file name with the thumbnail suffix added
                    base_name, ext = os.path.splitext(file)
                    thumbnail_image_path = os.path.join(output_folder, output_subfolder, f'{base_name}{thumbnail_suffix}{ext}')

                    # Create a new file name with the original suffix added
                    original_image_path = os.path.join(output_folder, output_subfolder, f'{base_name}{original_suffix}{ext}')

                    # Save the resized and cropped image with the thumbnail suffix
                    resized_image.save(thumbnail_image_path)

                    # Save the cropped image as the original with the original suffix
                    cropped_image.save(original_image_path)

                    # Convert the image to a binary format
                    image_binary = resized_image.tobytes()

                    # Encode the binary image as base64
                    image_base64 = base64.b64encode(image_binary).decode('utf-8')

                    # Create an HTML string for each image with a link to the "original" image
                    html_code = f'''
                    <div class="gallery-tag fade-container">
                        <a href="{original_image_path}" target="_blank" class="image-link">
                            <img src="{thumbnail_image_path}" alt="{output_subfolder}">
                            <span class="image-text">{output_subfolder}</span>
                        </a>
                    </div>
                    '''

                    # Write the HTML code to the HTML output file
                    html_file.write(html_code + '\n')

# Process images from the source folder and save them in the output folder
process_images(source_folder, output_folder, html_output_file)

print(f"New HTML file {html_output_file} created.")
