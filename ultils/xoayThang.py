import cv2
import numpy as np

def duongVienLonNhat(img):
    # Áp dụng bộ lọc Gaussian để làm mờ ảnh
    blurred = cv2.GaussianBlur(img, (5, 5), 1.4)

    # Áp dụng giải thuật Canny
    edges = cv2.Canny(blurred, 50, 150)

    cv2.namedWindow('edges', cv2.WINDOW_NORMAL)

    cv2.resizeWindow('edges', 500, 500)
    cv2.imshow('edges', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Tìm các đường viền trong ảnh
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def xoayThangAnh(path_to_img):
    gray_image = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)
    color_image = cv2.imread(path_to_img)

    # Tính toán hình chữ nhật bao quanh đường viền lớn nhất
    contours = duongVienLonNhat(gray_image)
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.int8(box)

    # Tính toán góc xoay
    angle = rect[2]
    if angle < -45:
        angle += 90

    # Xoay ảnh để làm thẳng đứng
    (h, w) = color_image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(color_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# image3 = xoayThangAnh(image1)

# cv2.namedWindow('Colored Rotated Image', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Colored Rotated Image', 500, 500)
# cv2.imshow('Colored Rotated Image', image3)

# cv2.waitKey(0)
# cv2.destroyAllWindows()