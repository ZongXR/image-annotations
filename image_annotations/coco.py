# -*- coding: utf-8 -*-
import os
from typing import List
from pycocotools.coco import COCO
from xml.etree.ElementTree import tostring
from xml.dom.minidom import parseString
from image_annotations.utils import dict2element
from image_annotations.utils import prefix_name


def to_yolo(annotation_path: str, output_dir: str) -> int:
    """
    转换成YOLO格式\n
    :param annotation_path: json文件路径
    :param output_dir: 输出文件夹
    :return: 转换了几张图片
    """
    count = 0
    os.makedirs(output_dir, exist_ok=True)
    coco = COCO(annotation_path)
    for image in coco.loadImgs(coco.getImgIds()):
        width = image["width"]
        height = image["height"]
        results = ""
        with open(os.path.join(output_dir, prefix_name(image["file_name"]) + ".txt"), "w") as f:
            for annotation in coco.loadAnns(coco.getAnnIds([image["id"]])):
                xmin, ymin, w, h = annotation["bbox"]
                result = "{} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(
                    annotation["category_id"],
                    (xmin + 0.5 * w) / width,
                    (ymin + 0.5 * h) / height,
                    w / width,
                    h / height
                )
                results = results + result
            f.write(results.strip())
        count = count + 1
    return count


def to_voc(annotation_path: str, images_dir: str, output_dir: str) -> int:
    """
    转换成VOC格式\n
    :param annotation_path: json文件路径
    :param images_dir: 图片文件夹
    :param output_dir: 输出文件夹
    :return: 转换了几张图片
    """
    count = 0
    os.makedirs(output_dir, exist_ok=True)
    coco = COCO(annotation_path)
    for image in coco.loadImgs(coco.getImgIds()):
        annotation = dict()
        annotation["folder"] = os.path.basename(images_dir)
        annotation["filename"] = image["file_name"]
        annotation["path"] = os.path.join(os.path.abspath(images_dir), annotation["filename"])
        annotation["source"] = {"database": "Unknown"}
        annotation["size"] = {"width": str(image["width"]), "height": str(image["height"]), "depth": "3"}
        annotation["segmented"] = "0"
        annotation["object"] = list()
        for annotation in coco.loadAnns(coco.getAnnIds([image["id"]])):
            xmin, ymin, w, h = annotation["bbox"]
            annotation["object"].append({
                "name": coco.loadCats([annotation["category_id"]])[0]["name"],
                "pose": "Unspecified",
                "truncated": "0",
                "difficult": "0",
                "bndbox": {"xmin": str(xmin), "ymin": str(ymin), "xmax": str(xmin + w), "ymax": str(ymin + h)}
            })
        xml = parseString(tostring(dict2element("annotation", annotation))).toprettyxml(indent="\t")
        with open(os.path.join(output_dir, f"{prefix_name(image['file_name'])}.xml"), "w") as f:
            f.write(xml)
        count = count + 1
    return count


def get_all_classes(annotation_path: str) -> List[str]:
    """
    获取全部类别名称\n
    :param annotation_path: 标注文件路径
    :return: 全部类别名称组成的列表
    """
    coco = COCO(annotation_path)
    cats = coco.loadCats(coco.getCatIds())
    cats = sorted(cats, key=lambda x: x["id"])
    return [x["name"] for x in cats]


if __name__ == '__main__':
    # to_voc(r"C:\Users\DrZon\Downloads\result.json", r"C:\Users\DrZon\Downloads\output", r"C:\Users\DrZon\Downloads\output")
    print(get_all_classes(r"C:\Users\DrZon\Downloads\result.json"))
