# -*- coding: utf-8 -*-


class BadFileException(Exception):
    """
    文件损坏异常\n
    """

    def __init__(self, filepath, message):
        """
        构造函数\n
        :param filepath: 文件路径
        :param message: 消息
        """
        self.filepath = filepath
        self.message = message

    def __str__(self) -> str:
        """
        格式化成字符串\n
        :return:
        """
        return f"文件{self.filepath}损坏, {self.message}"

    def __repr__(self) -> str:
        """
        对象表达式\n
        :return:
        """
        return f"{self.__class__.__name__}({self.filepath}, {self.message})"
