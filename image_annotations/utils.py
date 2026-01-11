# -*- coding: utf-8 -*-
import os
from typing import Union, Dict
from numbers import Number
from xml.sax.saxutils import escape
from xml.etree.ElementTree import Element, tostring, ElementTree


def dict2element(tag_name: str, elements: Union[Dict, Number]) -> Element:
    """
    将字典转换为xml的元素
    :param tag_name: 根标签名
    :param elements: 元素
    :return: 组装好的元素
    """
    result = Element(tag_name)
    if isinstance(elements, dict):
        for key, value in elements.items():
            if isinstance(value, dict):
                result.append(dict2element(key, value))
            elif isinstance(value, (list, tuple)):
                for val in value:
                    result.append(dict2element(key, val))
            else:
                child = Element(key)
                child.text = escape(str(value))
                result.append(child)
    else:
        result.text = escape(str(elements))
    return result


def dict2xml(tag_name: str, key_value: dict) -> ElementTree:
    """
    字典转xml树\n
    :param tag_name: 标签名
    :param key_value: 字典
    :return: 树
    """
    return ElementTree(dict2element(tag_name, key_value))


def prefix_name(filename: str) -> str:
    """
    获取文件前缀名\n
    :param filename: 原文件名
    :return: 前缀名
    """
    result = os.path.basename(filename).rsplit(".")
    return ".".join(result[0:-1])


def suffix_name(filename: str) -> str:
    """
    获取文件后缀名\n
    :param filename: 文件名
    :return: 后缀名
    """
    return filename.rsplit(".")[-1]


if __name__ == '__main__':
    d = {"filename": "aaa", "folder": "bbb", "size": {"width": 3, "height": 2, "depth": 3}, "object": [{"name": "aaa", "xmin": "bbb"}, {"name": "ccc", "xmin": "ddd"}, [3, 2]]}
    print(tostring(dict2element("annotation", d)))
    print(tostring(dict2element("annotation", 3)))

