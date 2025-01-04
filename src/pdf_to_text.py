import pytesseract
import os
import cv2
import numpy as np
import pdfplumber
from PIL import Image, ImageEnhance, ImageFilter
import re

# Đường dẫn đến tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đường dẫn đến file PDF
pdf_path = "ThuocPDF/1-AL.pdf"
save_text_path = "output.txt"
save_temp_image_path = "pdf_images"


def pdf_to_images(pdf_path, output_folder):
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            image_path = os.path.join(output_folder, f"page_{i + 1}.png")
            page_image = page.to_image(resolution=300)
            page_image.save(image_path)
            print(f"Saved page {i + 1} as image: {image_path}")


# Chuyển đổi PDF thành danh sách các ảnh
pdf_to_images(pdf_path, save_temp_image_path)

# Tạo thư mục để lưu ảnh tạm thời (nếu cần)
output_dir = save_temp_image_path

# Kết quả OCR
extracted_text = ""

print("Đang trích xuất văn bản từ PDF...")

for file_name in os.listdir(output_dir):
    if file_name.endswith(".png"):
        image_path = os.path.join(output_dir, file_name)
        gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Xử lý ảnh
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        denoised = cv2.medianBlur(binary, 3)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        resized = cv2.resize(sharpened, None, fx=2, fy=2,
                             interpolation=cv2.INTER_LINEAR)

        # OCR
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(
            resized, lang="vie", config=custom_config)

        extracted_text += f"\n--- {file_name} ---\n{text}"
        print(f"{file_name} đã xong.")

# Lưu kết quả vào file văn bản (nếu cần)
with open(save_text_path, "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("Extracted text:")
print(extracted_text)
