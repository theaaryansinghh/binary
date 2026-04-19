import os

def image_to_binary(image_path):
    if not os.path.exists(image_path):
        print("File not found")
        return

    with open(image_path, "rb") as img:
        data = img.read()

    print(f"Size: {len(data)} bytes\n")

    for i in range(0, len(data), 4):
        chunk = data[i:i + 4]
        print(' '.join(format(byte, '08b') for byte in chunk))


path = input("Enter image path: ").strip()
image_to_binary(path)