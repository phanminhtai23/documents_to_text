import cv2
import numpy as np


def detect_and_rotate_paper(image_path):
    # Đọc ảnh
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Không thể mở hoặc đọc tệp ảnh: {image_path}")

    # Chuyển đổi sang ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Áp dụng bộ lọc Gaussian để làm mờ ảnh
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Sử dụng Canny edge detection để phát hiện các cạnh
    edged = cv2.Canny(blurred, 50, 150)

    # Tìm các đường viền
    contours, _ = cv2.findContours(
        edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Sắp xếp các đường viền theo diện tích giảm dần và lấy đường viền lớn nhất
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        # Xấp xỉ đa giác từ đường viền
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Kiểm tra nếu đa giác có 4 đỉnh (hình chữ nhật)
        if len(approx) == 4:
            # Sắp xếp các đỉnh theo thứ tự: top-left, top-right, bottom-right, bottom-left
            rect = np.zeros((4, 2), dtype="float32")
            s = approx.sum(axis=1)
            rect[0] = approx[np.argmin(s)]
            rect[2] = approx[np.argmax(s)]

            diff = np.diff(approx, axis=1)
            rect[1] = approx[np.argmin(diff)]
            rect[3] = approx[np.argmax(diff)]

            # Tính toán chiều rộng và chiều cao của hình chữ nhật
            (tl, tr, br, bl) = rect
            widthA = np.linalg.norm(br - bl)
            widthB = np.linalg.norm(tr - tl)
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.linalg.norm(tr - br)
            heightB = np.linalg.norm(tl - bl)
            maxHeight = max(int(heightA), int(heightB))

            # Tạo ma trận biến đổi phối cảnh
            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

            return warped

    raise ValueError("Không tìm thấy hình chữ nhật trong ảnh.")


# Sử dụng hàm
image_path = r'D:\Project\AI\OCR\images\nghieng.jpg'
rotated_image = detect_and_rotate_paper(image_path)

# Lưu ảnh đã xoay
output_path = r'D:\Project\AI\OCR\images\rotated_image.jpg'
cv2.imwrite(output_path, rotated_image)

# Hiển thị ảnh đã xoay
cv2.imshow("Rotated Image", rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
