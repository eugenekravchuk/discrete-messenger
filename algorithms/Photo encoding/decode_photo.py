import base64
from PIL import Image
from io import BytesIO

def decode_base64_file_to_image(input_file_path, output_image_path):
    with open(input_file_path, "r") as input_file:
        base64_encoded_image = input_file.read()
        decoded_image = base64.b64decode(base64_encoded_image)
        image = Image.open(BytesIO(decoded_image))
        image.save(output_image_path)

# Example usage:
input_file_path = "encoded_image.txt"  # Replace "encoded_image.txt" with the path to your Base64 encoded image file
output_image_path = "decoded_image.jpg"  # Specify the path where you want to save the decoded image
decode_base64_file_to_image(input_file_path, output_image_path)
print("Image decoded and saved to:", output_image_path)