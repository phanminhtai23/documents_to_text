import cv2
import numpy as np
import pytesseract


def duongVienLonNhat(img):
    # Áp dụng bộ lọc Gaussian để làm mờ ảnh
    blurred = cv2.GaussianBlur(img, (5, 5), 1.4)

    # Áp dụng giải thuật Canny
    edges = cv2.Canny(blurred, 50, 150)

    # cv2.namedWindow('edges', cv2.WINDOW_NORMAL)

    # cv2.resizeWindow('edges', 500, 500)
    # cv2.imshow('edges', edges)

    # Tìm các đường viền trong ảnh
    contours, _ = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours


def xoayThangAnh(path_to_img):
    gray_image = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)
    color_image = cv2.imread(path_to_img)

    # Tính toán hình chữ nhật bao quanh đường viền lớn nhất
    contours = duongVienLonNhat(gray_image)
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    # Đảm bảo rằng chiều dài của hình chữ nhật luôn là cạnh dài nhất
    width, height = rect[1]
    if width < height:
        angle = rect[2]
    else:
        angle = rect[2] + 90
    box = cv2.boxPoints(rect)
    box = np.int8(box)

    # Tính toán góc xoay để cạnh dài nhất thẳng đứng
    angle = rect[2]
    if width < height:
        angle = rect[2]
    else:
        angle = rect[2] + 90

    # Xoay ảnh để làm thẳng đứng
    (h, w) = color_image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(color_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


# Đường dẫn đến tesseract.exe nếu cần thiết
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def is_image_upside_down(image):
    # print(image_path)

    # image = cv2.imread(image_path)

    # Chuyển ảnh sang grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # # Tăng độ tương phản 
    contrast = cv2.convertScaleAbs(gray, alpha=1, beta=0)
    # tăng nét
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(contrast, -1, sharpen_kernel)
    # chỉ tăng nét ok
    cv2.namedWindow('tang do tuong phan Image',
                            cv2.WINDOW_NORMAL)
    cv2.resizeWindow('tang do tuong phan Image', 500, 500)
    cv2.imshow('tang do tuong phan Image', sharpened)

    
    # Sử dụng OCR để nhận diện chữ
    text = pytesseract.image_to_string(sharpened, lang='vie')

    print(text)

    # Kiểm tra xem có ký tự tiếng Việt nào không
    vietnamese_characters = "áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ"
    for char in vietnamese_characters:
        if char in text:
            return False  # Ảnh không bị ngược

    return True


# def get_text_from_image(image):
#     while(is_image_upside_down(image)):
#         image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        
#         cv2.namedWindow('ROTATE_90_CLOCKWISE Rotated Image', cv2.WINDOW_NORMAL)
#         cv2.resizeWindow('ROTATE_90_CLOCKWISE Rotated Image', 500, 500)
#         cv2.imshow('ROTATE_90_CLOCKWISE Rotated Image', image)


image_path = './images/hoadon_xoay.jpg'

# Xoay ảnh
rotated_image = xoayThangAnh(image_path)

# Hiển thị ảnh đã xoay
# cv2.namedWindow('Colored Rotated Image', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Colored Rotated Image', 500, 500)
# cv2.imshow('Colored Rotated Image', rotated_image)

# Kiểm tra xem ảnh có bị ngược không
is_upside_down = is_image_upside_down(rotated_image)
    
# text_from_img = get_text_from_image(rotated_image)
# print(text_from_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
