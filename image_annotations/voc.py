# -*- coding: utf-8 -*-
import os
import re
from typing import List
import xml.etree.ElementTree as ET
import json
import traceback
from datetime import datetime
import getpass
from tqdm import tqdm
import image_annotations
from image_annotations.exceptions import BadFileException
from image_annotations.utils import prefix_name


def to_yolo(annotations_dir: str, classes: List[str], output_dir: str) -> int:
    """
    转换成YOLO格式
    :param annotations_dir: 标注文件目录
    :param classes: 所有的类组成的列表
    :param output_dir: 输出目录
    :return: 转换的标注文件数
    """
    count = 0
    os.makedirs(output_dir, exist_ok=True)
    for file in tqdm(os.listdir(annotations_dir)):
        if file.lower().endswith(".xml"):
            results = ""
            tree = ET.parse(os.path.join(annotations_dir, file))
            root = tree.getroot()
            try:
                width = int(root.findtext("size/width"))
                height = int(root.findtext("size/height"))
                for obj in root.findall("object"):
                    name = obj.findtext("name")
                    class_id = classes.index(name)
                    xmin = int(obj.findtext("bndbox/xmin"))
                    xmax = int(obj.findtext("bndbox/xmax"))
                    ymin = int(obj.findtext("bndbox/ymin"))
                    ymax = int(obj.findtext("bndbox/ymax"))
                    result = "{} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(
                        class_id,
                        (xmin + xmax) / 2 / width,
                        (ymin + ymax) / 2 / height,
                        (xmax - xmin) / width,
                        (ymax - ymin) / height
                    )
                    results = results + result
            except AttributeError as e:
                if getattr(e, "obj") is None:
                    raise BadFileException(os.path.join(annotations_dir, file), f"代码第{e.__traceback__.tb_lineno}行报错, {traceback.extract_tb(e.__traceback__)[-1].line}")
                else:
                    raise
            except TypeError as e:
                if "NoneType" in str(e):
                    raise BadFileException(os.path.join(annotations_dir, file), f"代码第{e.__traceback__.tb_lineno}行报错, {traceback.extract_tb(e.__traceback__)[-1].line}")
                else:
                    raise
            with open(os.path.join(output_dir, prefix_name(file) + ".txt"), "w") as f:
                f.write(results.strip())
            count = count + 1
    return count


def to_coco(annotations_dir: str, classes: List[str], output_path: str) -> int:
    """
    转换成COCO格式\n
    :param annotations_dir: 标注文件目录
    :param classes: 所有的类组成的列表
    :param output_path: 输出路径
    :return: 标注文件个数
    """
    info = {
        "year": datetime.now().year,
        "version": image_annotations.__version__,
        "description": "converted by image-annotations",
        "contributor": getpass.getuser(),
        "url": "https://github.com/ZongXR/image-annotations",
        "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    licenses = [{
        "id": 0,
        "name": "GNU General Public License v3 (GPLv3)",
        "url": "https://github.com/ZongXR/image-annotations/blob/main/LICENSE"
    }]
    categories = list(map(lambda x: {"id": x[0], "name": x[1], "supercategory": ""}, enumerate(classes)))
    images = []
    annotations = []
    i = 0
    j = 0
    for file in tqdm(os.listdir(annotations_dir)):
        if file.lower().endswith(".xml"):
            tree = ET.parse(os.path.join(annotations_dir, file))
            root = tree.getroot()
            try:
                width = int(root.findtext("size/width"))
                height = int(root.findtext("size/height"))
                image = {
                    "id": i,
                    "width": width,
                    "height": height,
                    "file_name": root.findtext("filename"),
                    "license": 0,
                    "flickr_url": "https://github.com/ZongXR/image-annotations",
                    "coco_url": "https://github.com/ZongXR/image-annotations",
                    "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                }
                images.append(image)
                for obj in root.findall("object"):
                    name = obj.findtext("name")
                    xmin = int(obj.findtext("bndbox/xmin"))
                    xmax = int(obj.findtext("bndbox/xmax"))
                    ymin = int(obj.findtext("bndbox/ymin"))
                    ymax = int(obj.findtext("bndbox/ymax"))
                    annotation = {
                        "id": j,  # 目标对象ID（每个对象ID唯一），每张图片可能有多个目标
                        "image_id": i,  # 对应图片ID
                        "category_id": classes.index(name),  # 对应类别ID，与categories中的ID对应
                        "segmentation": [],  # 实例分割，对象的边界点坐标[x1,y1,x2,y2,....,xn,yn]
                        "area": (xmax - xmin) * (ymax - ymin),  # 对象区域面积
                        "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],  # 目标检测，对象定位边框[x,y,w,h]
                        "iscrowd": 0,  # 表示是否是人群
                    }
                    annotations.append(annotation)
                    j = j + 1
                i = i + 1
            except AttributeError as e:
                if getattr(e, "obj") is None:
                    raise BadFileException(os.path.join(annotations_dir, file), f"代码第{e.__traceback__.tb_lineno}行报错, {traceback.extract_tb(e.__traceback__)[-1].line}")
                else:
                    raise
            except TypeError as e:
                if "NoneType" in str(e):
                    raise BadFileException(os.path.join(annotations_dir, file), f"代码第{e.__traceback__.tb_lineno}行报错, {traceback.extract_tb(e.__traceback__)[-1].line}")
                else:
                    raise
    with open(output_path, "w") as f:
        json.dump({
            "info": info,
            "licenses": licenses,
            "categories": categories,
            "images": images,
            "annotations": annotations
        }, f, indent=4, ensure_ascii=False)
    return i


def get_all_classes(annotations_dir: str) -> List[str]:
    """
    获取全部类别名称\n
    :param annotations_dir: 标注文件所在文件夹
    :return: 全部类别名称组成的列表
    """
    results = set()
    for file in tqdm(os.listdir(annotations_dir)):
        if file.lower().endswith(".xml"):
            fullpath = os.path.join(annotations_dir, file)
            with open(fullpath, "r") as f:
                results.update(set(re.findall(r"<object>.*?<name>(.*?)</name>.*?</object>", f.read(), re.DOTALL)))
    return list(results)


if __name__ == '__main__':
    print(get_all_classes(r"C:\Users\DrZon\Desktop"))
