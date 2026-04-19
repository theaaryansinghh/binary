import os

binary_input = input("Enter binary code: ").strip()

bytes_list = binary_input.split()
data = bytes([int(b, 2) for b in bytes_list])

with open("output_image.png", "wb") as img:
    img.write(data)

print("Image saved as output_image.png")