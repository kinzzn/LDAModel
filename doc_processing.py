# -*- coding:utf-8 -*-
# 处理文件，最后返回文件为分好词、标记好类别的文档/文件对象
# python2.7 和python3的处理有不同

import jieba
import re
from settings import Configs

# 所有的路径都最终在conf中进行统一处理
# 处理分类文件，应具有文件的原类别

def doc_process():
    # 按之前Ipython的来
    # 分词
    doc_path = 'F:/ProgramInstall/JetBrains/PyCharm/work/mylda/input'
    # 读取分好类的txt
    doc_dir = '/'
    # 文档顺序：ZARA，虾米，雅思，RADWIMPS
    doc_name = ['1744769622.txt']#, '1718436033.txt', '2010639813.txt', '5539705240.txt']

    marklist = []
    all_shorttext = []
    for name in doc_name:
        with open(doc_path + doc_dir + name, 'r', encoding='utf8') as f:  # 只在这里固定编码方式，2.7没有问题
            doc = f.read()
            li = doc.split('\n')
            mark = len(li)
            marklist.append(mark)
            for content in li:
                # 去掉内容里的数字编号
                m = re.findall('\d+:(.+)', content)
                if m:
                    content = m[0]
                # 去掉链接
                m2 = re.findall('[a-z]+://[0-9A-Za-z./]+', content)
                for links in m2:
                    content = content.replace(links, ' ')
                # 去掉表情符号
                m = re.findall('\[\w+\]', content)
                if m:
                    for emojis in m:
                        content = content.replace(emojis, ' ')
                # 去掉除'之外的标点符号
                m = re.findall('[’：“”，。！？》《【】!"#$%&()*+,-./:;<=>?@[\\]^_`{|}「」~]+', content)
                if m:
                    for code in m:
                        content = content.replace(code, ' ')
                content = content.replace('\u200b', '')
                content = content.replace('\xa0','')
                content = content.replace('\u3000','')
                doc_cut = jieba.cut(content)  # _decode)
                result = ' '.join(doc_cut)
                # 去掉多余空格
                result = re.sub(" +", " ", result)
                #print(result)
                all_shorttext.append(result)
            # result = ' '.join(doc_cut)
            print(name + ' : finish')
            # print(result)
            # result = result.encode('utf-8')
            # with open('E:/20171204 BS/coderef/scikit-LDA/r'+note+'.txt','w',encoding='utf8') as f2:#只在这里固定编码方式，2.7没有问题
            #    f2.write(result)
        f.close()
        # f2.close()
        # print (note+' : finish')

    all_text_num = 0    # 所有文档数
    for n in marklist:
        all_text_num += n
    print(marklist) # marklist是每类总篇数
    print(all_shorttext)

    # 去除停用词
    # 导入停用词，读取文件转为list
    stpwpath = 'F:/ProgramInstall/JetBrains/PyCharm/work/mylda/input/stop_words.txt'
    stpw_dic = open(stpwpath, 'r')
    stpw_content = stpw_dic.read()
    stpwlst = stpw_content.splitlines()
    stpwlst.append('图片')
    stpwlst.append('来自')
    stpwlst.append('网络')
    stpwlst.append('全文')
    stpw_dic.close()

    all_dict = {}   # 词表
    dict_count = 0  # 第几个出现的词
    all_text = []   # 去掉停用词后的所有文本
    all_text_words = []     # 去掉停用词后每一条的词数
    for text in all_shorttext:
        wordnum = 0
        newtext=''
        segs = text.split(' ')
        for seg in segs:    # 每个seg是一个词
            if seg not in stpwlst:
                wordnum += 1
                newtext = newtext + ' ' + seg
                # 如果键不存在于字典中，将会添加键并将值设为默认值
                all_dict.setdefault(seg,dict_count)
                dict_count += 1
        all_text.append(newtext.strip())    # strip去掉最开始的所有空格
        all_text_words.append(wordnum)

    print('所有文本：')
    print(all_text)
    print('词典：')
    print(all_dict)


    # 将这些所有返回值存入文件
    confobj = Configs()
    confobj.confgetpaths()
    # 存所有文档
    alltextfw = open(confobj.alltextfile,'w',encoding='utf8')   # ‘w'：覆盖原文件内容
    for t in all_text:
        alltextfw.write(str(t)+'\n')
    alltextfw.close()
    # 存每个文档的词数
    alltextwordsfw = open(confobj.alltextwordsfile,'w',encoding='utf8')
    for nums in all_text_words:
        alltextwordsfw.write(str(nums)+'\n')
    alltextwordsfw.close()
    # 存词表
    dictfw = open(confobj.dictfile,'w',encoding='utf8')
    for d in all_dict.keys():
        dictfw.write(str(d)+'\n')
    dictfw.close()
    # 存文档篇数
    confobj.confsettextnums(all_text_num)

    return(all_text_num, len(all_dict))
    # 文档集list，每篇的词数，词典->存到相应的文件
    # M，V返回给调用，不一定用


