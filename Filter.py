import os
import cv2


class Filter(object):
    """
    分割图片后进行过滤
    """

    def __init__(self):
        pass

    @staticmethod
    def dup_remove(dir_path="."):
        """
        过滤相似图片
        :param dir_path:
        :return:
        """
        for root, dirs, files in os.walk(dir_path):
            com = (-1, -1)
            for filename in files:
                x, y = filename.split(",")
                if len(y) > 3:
                    y, _ = y.split(".")
                # print(x,y)
                if (int(x) - com[0]) ** 2 + (int(y) - com[1]) ** 2 < 4:
                    try:
                        name = str(com[0]) + "," + str(com[1]) + ".png"
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        pass
                    try:
                        name = str(com[0]) + "," + str(com[1])
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        pass
                com = (int(x), int(y))
            for dir_name in dirs:
                pass

    @staticmethod
    def trans_offset(dir_path="."):
        """
        转换为相对坐标
        :param dir_path:开始搜索的路径
        :return:
        """
        for root, dirs, files in os.walk(dir_path):
            com = (-1, -1)
            for filename in files:
                if filename.split("\\"[-2]) == "offset":
                    cv2.imread(os.path.join(root, filename))
            for dir_name in dirs:
                pass
