""" Photo to base64 encoding """

import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

def write_base64_to_file(base64_string, output_file_path):
    with open(output_file_path, "w") as output_file:
        output_file.write(base64_string)



# image_path = "small_photo.jpg"
# base64_encoded_image = encode_image_to_base64(image_path)

# output_file_path = "encoded_image.txt"
# write_base64_to_file(base64_encoded_image, output_file_path)