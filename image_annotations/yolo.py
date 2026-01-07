# -*- coding: utf-8 -*-
import os
import re
import json
from typing import List
from datetime import datetime
import getpass
from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString
import numpy as np
import cv2
from tqdm import tqdm
import image_annotations
from image_annotations.exceptions import BadFileException
from image_annotations.utils import dict2element
from image_annotations.utils import prefix_name


def to_voc(images_dir: str, annotations_dir: str, classes: List[str], output_dir: str) -> int:
    """
    转换成voc格式\n
    :param images_dir: 图像文件夹
    :param annotations_dir: 标注文件夹
    :param classes: 类的列表
    :param output_dir: 输出文件夹
    :return: 转换多少个文件
    """
    count = 0
    os.makedirs(output_dir, exist_ok=True)
    for file in tqdm(os.listdir(annotations_dir)):
        if file.lower().endswith(".txt"):
            annotation = dict()
            annotation["folder"] = os.path.basename(images_dir)
            annotation["filename"] = prefix_name(file) + ".jpg"
            annotation["path"] = os.path.join(os.path.abspath(images_dir), annotation["filename"])
            annotation["source"] = {"database": "Unknown"}
            height, width, depth = cv2.imdecode(np.fromfile(os.path.join(images_dir, prefix_name(file) + ".jpg"), dtype=np.uint8), -1).shape
            annotation["size"] = {"width": str(width), "height": str(height), "depth": str(depth)}
            annotation["segmented"] = "0"
            annotation["object"] = list()
            with open(os.path.join(annotations_dir, file), "r") as f:
                for i, line in enumerate(f.readlines()):
                    search_result = re.search(r"^(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)$", line.strip())
                    if search_result:
                        try:
                            class_id = int(search_result[1])
                            x_center = float(search_result[2]) * width
                            y_center = float(search_result[3]) * height
                            w_bbox = float(search_result[4]) * width
                            h_bbox = float(search_result[5]) * height
                        except IndexError as e:
                            raise BadFileException(os.path.join(annotations_dir, file), f"文件第{i+1}行格式有误: {line.strip()}")
                        name = classes[class_id]
                        xmin = int(x_center - 0.5 * w_bbox)
                        xmax = int(x_center + 0.5 * w_bbox)
                        ymin = int(y_center - 0.5 * h_bbox)
                        ymax = int(y_center + 0.5 * h_bbox)
                        annotation["object"].append({
                            "name": name,
                            "pose": "Unspecified",
                            "truncated": "0",
                            "difficult": "0",
                            "bndbox": {"xmin": str(xmin), "ymin": str(ymin), "xmax": str(xmax), "ymax": str(ymax)}
                        })
            xml = parseString(tostring(dict2element("annotation", annotation))).toprettyxml(indent="\t")
            with open(os.path.join(output_dir, f"{prefix_name(file)}.xml"), "w") as f:
                f.write(xml)
            count = count + 1
    return count


def to_coco(images_dir: str, annotations_dir: str, classes: List[str], output_path: str) -> int:
    """
    转成COCO格式\n
    :param images_dir: 图片文件夹
    :param annotations_dir: 标注文件夹
    :param classes: 类的列表
    :param output_path: 输出的路径
    :return: 转换多少个文件
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
        if file.lower().endswith(".txt"):
            height, width, _ = cv2.imdecode(np.fromfile(os.path.join(images_dir, prefix_name(file) + ".jpg"), dtype=np.uint8), -1).shape
            image = {
                "id": i,
                "width": width,
                "height": height,
                "file_name": prefix_name(file) + ".jpg",
                "license": 0,
                "flickr_url": "https://github.com/ZongXR/image-annotations",
                "coco_url": "https://github.com/ZongXR/image-annotations",
                "date_captured": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            }
            images.append(image)
            with open(os.path.join(annotations_dir, file), "r") as f:
                for line in f.readlines():
                    search_result = re.search(r"^(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)$", line.strip())
                    if search_result:
                        try:
                            class_id = int(search_result[1])
                            x_center = float(search_result[2]) * width
                            y_center = float(search_result[3]) * height
                            w_bbox = float(search_result[4]) * width
                            h_bbox = float(search_result[5]) * height
                        except IndexError as e:
                            raise BadFileException(os.path.join(annotations_dir, file), f"文件第{i}行格式有误: {line.strip()}")
                        xmin = int(x_center - 0.5 * w_bbox)
                        xmax = int(x_center + 0.5 * w_bbox)
                        ymin = int(y_center - 0.5 * h_bbox)
                        ymax = int(y_center + 0.5 * h_bbox)
                        annotation = {
                            "id": j,  # 目标对象ID（每个对象ID唯一），每张图片可能有多个目标
                            "image_id": i,  # 对应图片ID
                            "category_id": class_id,  # 对应类别ID，与categories中的ID对应
                            "segmentation": [],  # 实例分割，对象的边界点坐标[x1,y1,x2,y2,....,xn,yn]
                            "area": (xmax - xmin) * (ymax - ymin),  # 对象区域面积
                            "bbox": [xmin, ymin, xmax - xmin, ymax - ymin],  # 目标检测，对象定位边框[x,y,w,h]
                            "iscrowd": 0,  # 表示是否是人群
                        }
                        annotations.append(annotation)
                        j = j + 1
            i = i + 1
    with open(output_path, "w") as f:
        json.dump({
            "info": info,
            "licenses": licenses,
            "categories": categories,
            "images": images,
            "annotations": annotations
        }, f, indent=4, ensure_ascii=False)
    return i


def get_all_classes_ids(annotations_dir: str) -> List[int]:
    """
    获取全部类ID\n
    :param annotations_dir: 标注文件所在文件夹
    :return: 类ID组成的列表
    """
    results = set()
    for file in tqdm(os.listdir(annotations_dir)):
        if file.lower().endswith(".txt"):
            fullpath = os.path.join(annotations_dir, file)
            with open(fullpath, "r") as f:
                for line in f.readlines():
                    search_result = re.search(r"^(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)$", line.strip())
                    if search_result:
                        class_id = int(search_result[1])
                        results.add(class_id)
    return sorted(list(results))


if __name__ == '__main__':
    # to_voc(r"C:\Users\DrZon\Downloads\images", r"C:\Users\DrZon\Downloads\labels", ["Pedestrian", "Cyclist", "Car", "Truck", "Tram", "Tricycle"], r"C:\Users\DrZon\Downloads\output")
    to_coco(r"C:\Users\DrZon\Downloads\images", r"C:\Users\DrZon\Downloads\labels", ["Pedestrian", "Cyclist", "Car", "Truck", "Tram", "Tricycle"], r"C:\Users\DrZon\Downloads\result.json")


