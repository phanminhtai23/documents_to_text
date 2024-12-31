import cv2
import pytesseract

# Đường dẫn đến tesseract.exe nếu cần thiết
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def is_image_upside_down(image):
    # Chuyển ảnh sang grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sử dụng OCR để nhận diện chữ
    text = pytesseract.image_to_string(gray, lang='vie')

    print(text)

    # Kiểm tra xem có ký tự tiếng Việt nào không
    vietnamese_characters = "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"
    for char in vietnamese_characters:  
        if char in text:
            return False  # Ảnh không bị ngược
    return True  # Ảnh có thể bị ngược
