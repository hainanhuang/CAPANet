import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

def add_crop_box(img, box, color=(255, 0, 0), thickness=2):
    """在图像上画局部放大框，返回带框图像和放大区域。"""
    x, y, w, h = box
    img_boxed = img.copy()
    cv2.rectangle(img_boxed, (x, y), (x + w, y + h), color, thickness)
    crop = img[y:y+h, x:x+w]
    return img_boxed, crop

def make_comparison(image_name, methods, box, save_path):
    """
    image_name: 图像文件名（无扩展名），如 "img001"
    methods: dict，格式 {方法名: SR图路径}
    box: (x, y, w, h) 放大框坐标（HR图像空间）
    """
    # 过滤掉不存在的路径
    available_methods = {}
    for name, path in methods.items():
        if path.exists():
            available_methods[name] = path
        else:
            print(f"Warning: {path} not found, skipping {name}")
    
    if not available_methods:
        print("No images found for comparison.")
        return

    n = len(available_methods)
    fig, axes = plt.subplots(2, n, figsize=(4 * n, 8))

    # 如果只有一列，axes 会是一维的，需要调整
    if n == 1:
        axes = np.array([axes]).T

    for col, (method_name, img_path) in enumerate(available_methods.items()):
        img = cv2.imread(str(img_path))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_boxed, crop = add_crop_box(img, box)

        axes[0][col].imshow(img_boxed)
        axes[0][col].set_title(method_name, fontsize=10)
        axes[0][col].axis('off')

        crop_resized = cv2.resize(crop, (crop.shape[1]*3, crop.shape[0]*3),
                                  interpolation=cv2.INTER_NEAREST)
        axes[1][col].imshow(crop_resized)
        axes[1][col].axis('off')

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {save_path}")

if __name__ == '__main__':
    # ===== 使用示例 =====
    methods = {
        "Bicubic": Path("results/Bicubic/Urban100/img001_bicubic.png"),
        "CATANet": Path("results/CATANet/Urban100/img001_CATANet.png"),
        "PFT-light": Path("results/PFT/Urban100/img001_PFT.png"),
        "CAPANet": Path("results/CAPANet/visualization/Urban100/img001_CAPANet.png"),
        "HR": Path("/home/featurize/data/TestDataSR/HR/Urban100/x4/img001.png"),
    }
    # box 坐标以 HR 图像分辨率为准，挑选建筑线条、重复纹理等关键区域
    make_comparison("img001", methods, box=(120, 80, 60, 60),
                    save_path="output/visual_urban100_img001.png")
