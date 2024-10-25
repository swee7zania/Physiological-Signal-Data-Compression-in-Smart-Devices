from PIL import Image
import os

# 打开刚刚生成的ECG图像
img = Image.open('ecg_image.png')

# 如果图像是RGBA模式，转换为RGB模式
if img.mode == 'RGBA':
    img = img.convert('RGB')

# 压缩图像并保存为JPEG格式
compressed_image_path = 'compressed_ecg_image.jpg'
img.save(compressed_image_path, quality=10)  # 调整quality参数以测试不同压缩率

# 获取并输出文件大小
file_size = os.path.getsize(compressed_image_path)
print(f'Compressed image size: {file_size / 1024:.2f} KB')

# 显示压缩后的图像
img.show()
