# -*- coding: utf-8 -*-
import setuptools
import image_annotations


base_url = "https://github.com/ZongXR/image-annotations"
with open("./README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
packages = setuptools.find_packages()
requires_list = open('./requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [x.strip() for x in requires_list if (not x.startswith("setuptools")) and (not x.startswith("twine") and (not x.startswith("packaging")))]


setuptools.setup(
    name="image-annotations",
    version=image_annotations.__version__,
    author="Xiangrui Zong",
    author_email="zxr@tju.edu.cn",
    description="图像标注格式转换器，能让你自由转换YOLO、COCO、VOC格式的图像标注文件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=base_url,
    packages=packages,
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.7,<3.11',
    install_requires=requires_list
)
