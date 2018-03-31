# -*- coding:utf-8 -*-


import doc_processing
from lda import LDAModel


def run():
    doc_processing.doc_process()  # 讲道理也可以把所有文件信息通过传参传进来
    lda = LDAModel()#所有数据从文件读取
    lda.start()


if __name__ == '__main__':
    run()
