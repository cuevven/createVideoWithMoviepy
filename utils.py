# -*- coding: utf-8 -*-
import os
from PIL import Image

def resizeImage(target_image_path, origin_target_dir, target_size):
    """
    调整图片大小，缺失的部分用黑色填充
    :param target_image_path: 图片路径
    :param origin_target_dir: 图片最终保存目录 :type (origin_dir, target_dir)
    :param target_size: 分辨率大小 :type (width, height)
    :return:
    """
    image = Image.open(target_image_path)

    iw, ih = image.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    scale = min(w / iw, h / ih)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()

    new_image = Image.new('RGB', target_size, (0, 0, 0, 0))  # 生成黑色图像
    # // 为整数除法，计算图像的位置
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
    # new_image.show()

    # 写入目标位置
    target_image_path = target_image_path.replace(origin_target_dir[0], origin_target_dir[-1])
    print('>>新图片：%s' % target_image_path)
    target_dir = '/'.join(target_image_path.split('/')[:-1])
    mkdirs(target_dir)
    
    new_image.save(target_image_path, quality=100)

def mkdirs(path):
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录,创建目录操作函数
        '''
        os.mkdir(path)与os.makedirs(path)的区别是:
        当父目录不存在的时候os.mkdir(path)不会创建；
        os.makedirs(path)则会创建父目录
        '''
        os.makedirs(path)
        print('>>%s created.' % path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print('>>%s is exists.' % path)
        return False


def readDir(dirPath):
    if dirPath[-1] == '/':
        print(u'>>文件夹路径末尾不能加/')
        return
    allFiles = []
    if os.path.isdir(dirPath):
        fileList = os.listdir(dirPath)
        for f in fileList:
            if f == '.DS_Store' or f == '.gitkeep':
                continue
            f = dirPath+'/'+f
            if os.path.isdir(f):
                subFiles = readDir(f)
                allFiles = subFiles + allFiles #合并当前目录与子目录的所有文件路径
            else:
                allFiles.append(f)
        return allFiles
    else:
        return 'Error,not a dir'

def writeToFile(filesPath):
    print('>>开始写入文件路径')
    with open('GetAbsolutePath.txt', 'w') as f:
        for filePath in filesPath:
            # if filePath.split('/')[-1] != '.DS_Store':
            f.write(str(filePath))
            f.write('\n')
    print('>>写入完毕，一共有 %s 行' % len(filesPath))