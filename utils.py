from PIL import Image

def validate_image(path):
    try:
        img = Image.open(path)
        img.verify()
        return True, "Valid image file"
    except Exception as e:
        return False, f"Invalid image: {str(e)}"