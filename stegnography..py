from PIL import Image
import stepic
import hashlib
import os

# Function to calculate SHA-256 hash of a file
def get_file_hash(file_path):
    if not os.path.exists(file_path):
        return "File not found"
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large images
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Hiding data
def hide_data(image_path, message):
    if not os.path.exists(image_path):
        print(f" Error: {image_path} not found!")
        return

    # Calculate hash before change
    pre_hash = get_file_hash(image_path)
    print(f" Original Image Hash: {pre_hash}")

    img = Image.open(image_path)
    encoded_img = stepic.encode(img, message.encode())
    encoded_img.save("secret_image.png")
    
    # Calculate hash after change
    post_hash = get_file_hash("secret_image.png")
    print(f" Stego Image Hash:    {post_hash}")
    print(" Message hidden successfully in 'secret_image.png'")
    print("This proves the data has changed.")

# Extracting data
def show_data(image_path):
    if not os.path.exists(image_path):
        print(f" Error: {image_path} not found!")
        return
    
    img = Image.open(image_path)
    message = stepic.decode(img)
    print(f" The hidden message is: {message}")

# --- INTERACTIVE MENU ---
if __name__ == "__main__":
    print("---  Stegnography tool ---")
    print("1. Hide a Message")
    print("2. Extract a Message")
    choice = input("Select an option (1 or 2): ")

    if choice == "1":
        img_name = input("Enter the name of your original PNG (e.g., original.png): ")
        secret_text = input("Enter the secret message to hide: ")
        hide_data(img_name, secret_text)
    elif choice == "2":
        img_name = input("Enter the stego image name (e.g., secret_image.png): ")
        show_data(img_name)
    else:
        print("Invalid choice. Exiting.")
