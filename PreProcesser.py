import cv2
import os


class PreProcesser(object):
    """
    输入图片预处理器接口
    """
    def __init__(self, root_path):
        self._root_path = root_path

    # return a list of image blong to root dirctory
    def detect(self):
        pass


class RowPreProcesser(PreProcesser):
    """
        输入图片预处理器初步实现
        """
    def __init__(self, root_path):
        super(RowPreProcesser, self).__init__(root_path)

    def retrieve(self):
        """
        适用于指定文件夹下为所有待分割图片的情况
        :return:指定文件夹下图片名列表
        """
        img_list = []
        for root, dirs, files in os.walk(self._root_path):
            for file_name in files:
                if file_name.endswith(".jpg"):
                    img_list.append(file_name)
            for dir_name in dirs:
                raise Exception("请不要嵌套文件夹")
        return img_list

    def recursionDetect(self):
        """
        适用于指定文件夹下为画册文件夹，画册文件夹下为待分割图片的情况
        :return:字典，key为画册文件夹名称，value为该画册文件夹下图片文件名列表
        """
        book_dict = {}
        for root, dirs, files in os.walk(self._root_path):
            _book_dict = {}
            for dir_name in dirs:
                book_dict[dir_name] = []
            for file_name in files:
                if file_name.endswith(".jpg"):
                    try:
                        suffix, book = root.split("\\")
                        book_dict[book].append(file_name)
                    except Exception as e:
                        print("请将图片放在画册名文件夹下")

        return book_dict


if __name__ == "__main__":
    rpp = RowPreProcesser("./PictureBooks")
    dir = rpp.retrieve()
    print(dir)
