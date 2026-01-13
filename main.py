import cv2
import numpy as np


# Bộ ký tự ASCII đơn giản, rõ nét
CHARACTER_SET = "-:.,;i1tfLCG08@"

# Đọc ảnh màu
image_color = cv2.imread("image/mywife.jpg")
image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

# Lấy kích thước ảnh gốc
height, width = image_gray.shape

# Số cột ký tự (tăng để chi tiết hơn)
num_cols = 180

# Tính số hàng giữ đúng tỷ lệ ảnh gốc
# Vì ký tự cao hơn rộng (khoảng 2:1), cần chia cho hệ số này
num_rows = int(num_cols * height / width * 0.4)

# Kích thước mỗi ký tự khi vẽ
char_width = 10
char_height = 18

# Resize ảnh
resized_gray = cv2.resize(image_gray, (num_cols, num_rows), interpolation=cv2.INTER_AREA)
resized_color = cv2.resize(image_color, (num_cols, num_rows), interpolation=cv2.INTER_AREA)

# Tăng độ sáng và tương phản
resized_gray = cv2.convertScaleAbs(resized_gray, alpha=1.3, beta=20)

# Tạo ảnh ASCII màu
output_height = num_rows * char_height
output_width = num_cols * char_width
ascii_image = np.zeros((output_height, output_width, 3), dtype=np.uint8)

# Chuyển đổi thành ASCII
for i in range(num_rows):
    for j in range(num_cols):
        # Lấy giá trị grayscale và màu
        gray_value = resized_gray[i, j]
        color = resized_color[i, j]
        
        # Tăng độ sáng màu
        color = np.clip(color.astype(np.float32) * 1.3 + 20, 0, 255).astype(np.uint8)
        
        # Chọn ký tự ASCII dựa trên độ sáng
        char_index = int(gray_value / 255 * (len(CHARACTER_SET) - 1))
        char = CHARACTER_SET[char_index]
        
        # Vẽ ký tự lên ảnh với màu tương ứng
        y = i * char_height
        x = j * char_width
        cv2.putText(ascii_image, char, (x, y + char_height - 4), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                    (int(color[0]), int(color[1]), int(color[2])), 1, cv2.LINE_AA)

# Resize để vừa màn hình nếu quá lớn
max_display_height = 800
if ascii_image.shape[0] > max_display_height:
    scale = max_display_height / ascii_image.shape[0]
    display_img = cv2.resize(ascii_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
else:
    display_img = ascii_image

cv2.imshow("ASCII Art Color", display_img)
cv2.imwrite("ascii_output_color.png", ascii_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
