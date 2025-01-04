import cv2
import numpy as np
import pytesseract

# Đường dẫn đến tesseract.exe nếu cần thiết
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def img_to_text(path_to_img):
    
    # Khi truyền path ảnh
    gray = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)

    # Tăng độ tương phản
    contrast = cv2.convertScaleAbs(gray, alpha=1, beta=0)
    # tăng nét
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(contrast, -1, sharpen_kernel)
    # chỉ tăng nét ok
    cv2.namedWindow('tang do tuong phan Image',
                    cv2.WINDOW_NORMAL)
    cv2.resizeWindow('tang do tuong phan Image', 500, 500)
    cv2.imshow('tang do tuong phan Image', sharpened)

    result_text = ""
    # Sử dụng OCR để nhận diện chữ
    text1 = pytesseract.image_to_string(sharpened, lang='vie')
    return text1


image_path = './images/cv.jpg'

# Kiểm tra xem ảnh có bị ngược không
text = img_to_text(image_path)
print(text)

cv2.waitKey(0)
cv2.destroyAllWindows()
