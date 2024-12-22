import os
import shutil
from PIL import Image
from typing import Union


def get_image_extension(filepath: str) -> str:
    """
    使用 PIL 检测图片的真实格式并返回对应的扩展名
    """
    try:
        with Image.open(filepath) as img:
            fmt = img.format.lower()
            ext_map = {
                'jpeg': '.jpg',
                'png': '.png',
                'webp': '.webp',
                'gif': '.gif',
                'bmp': '.bmp'
            }
            return ext_map.get(fmt, f'.{fmt}')
    except Exception:
        return os.path.splitext(filepath)[1]


def rename_and_zip_images(source_folder: str, output_folder: str, zip_folder: str) -> None:
    """
    读取源文件夹下所有图像文件，重命名复制到输出文件夹，然后压缩到zip文件夹。

    Args:
        source_folder: 源图片文件夹路径
        output_folder: 重命名后图片的输出文件夹路径
        zip_folder: zip文件的输出文件夹路径
    """
    # 1. 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(zip_folder, exist_ok=True)

    # 2. 获取文件夹下所有图像文件
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif')
    image_files = [
        f for f in os.listdir(source_folder)
        if str(f).lower().endswith(valid_extensions)
    ]

    # 3. 按创建时间从新到旧排序（descending）
    image_files.sort(
        key=lambda x: os.path.getctime(str(os.path.join(source_folder, x))),
        reverse=True
    )

    # 4. 按顺序重命名并复制到输出文件夹
    for idx, old_file_name in enumerate(image_files, start=1):
        old_full_path = str(os.path.join(source_folder, old_file_name))

        # 检测真实的图片格式
        real_ext = get_image_extension(old_full_path)
        new_file_name = f"{idx:04d}{real_ext}"
        new_full_path = str(os.path.join(output_folder, new_file_name))

        # 复制文件（而不是移动）
        shutil.copy2(old_full_path, new_full_path)

    # 5. 将输出文件夹压缩到zip文件夹
    base_name = os.path.basename(source_folder)
    zip_path = os.path.join(zip_folder, base_name)

    shutil.make_archive(
        base_name=zip_path,
        format="zip",
        root_dir=output_folder,  # 直接压缩输出文件夹中的文件
        base_dir='.'  # 压缩当前目录下的所有文件
    )


if __name__ == "__main__":
    # 源文件夹路径
    source_folder = "/Users/qiyucai/Documents/target_images"
    # 重命名后图片的输出路径
    output_folder = "/Users/qiyucai/Documents/renamed_images"
    # zip文件输出路径
    zip_folder = "/Users/qiyucai/Documents/zips"

    rename_and_zip_images(source_folder, output_folder, zip_folder)
    print("Done!")