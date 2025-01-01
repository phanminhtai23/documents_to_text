from pdf2image import convert_from_path
import pytesseract
import os
import cv2
import numpy as np


# Đường dẫn đến tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Đường dẫn đến file PDF
pdf_path = "D:/Project/AI/OCR/images/1555568099824_Nhãn 94-763-769.pdf"

# Chuyển đổi PDF thành danh sách các ảnh
images = convert_from_path(pdf_path)

# Tạo thư mục để lưu ảnh tạm thời (nếu cần)
output_dir = "temp_images"
os.makedirs(output_dir, exist_ok=True)

# Kết quả OCR
extracted_text = ""
count = 0


print("Đang trích xuất văn bản từ PDF...")
# Duyệt qua từng trang (ảnh) và áp dụng OCR
for i, image in enumerate(images):

    # Xử lý ảnh
    # Chuyển đổi ảnh PIL thành định dạng numpy array
    image_np = np.array(image)

    # Chuyển đổi ảnh thành ảnh xám
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Tăng độ tương phản
    contrast = cv2.convertScaleAbs(gray, alpha=1, beta=0)
    # tăng nét
    # sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    # sharpened = cv2.filter2D(contrast, -1, contrast)

    # Lưu ảnh tạm thời
    temp_image_path = os.path.join(output_dir, f"page_{i+1}.jpg")
    # sharpened.save(temp_image_path, "JPEG")
    cv2.imwrite(temp_image_path + ".jpeg", contrast)

    text = pytesseract.image_to_string(contrast, lang="vie")
    extracted_text += f"\n--- Page {i+1} ---\n{text}"
    print(f"Trang {i+1} đã xong.")

# Lưu kết quả vào file văn bản (nếu cần)
with open("extracted_content/extracted_text1.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)


print("Extracted text1:")
print(extracted_text)

# for file_name in os.listdir(output_dir):
#     os.remove(os.path.join(output_dir, file_name))
# os.rmdir(output_dir)
