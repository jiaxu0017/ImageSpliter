import cv2
import os
import numpy as np


class ImgSpliter(object):
    """
    图片分割接口
    """

    def __init__(self, imgs, root_dir):
        self._imgs = imgs
        self._root_dir = root_dir

    def split(self, src_name, home_path):
        pass


class RowImgSpliter(ImgSpliter):
    """
    图像分割初步实现
    """

    def __init__(self, imgs, root_dir):
        """
        实例化图像分割器
        :param imgs:图片文件名列表
        :param root_dir:图片文件所在文件夹
        """
        super(RowImgSpliter, self).__init__(imgs, root_dir)

    def split(self, src_path, home_path):
        """
        图像分割，保存为以下文件，文件名为轮廓中心矩坐标
        home_path/contours下为轮廓点坐标
        home_path/img下为分割后的图片
        home_path/offset 下为相对坐标
        :param src_path: 传入的图片路径名
        :param home_path: 输出文件夹
        :return:
        """
        img = cv2.imread(src_path, -1)  # flags <0返回包含Alpha通道的加载的图像。
        src = cv2.imread(src_path, -1)

        width = img.shape[1]
        height = img.shape[0]

        # 添加alpha通道
        def addAlpha(image):
            temp_image = []
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    temp = np.append(image[i][j], 255)  # (0~255)
                    temp_image.append(temp)
            return np.array(temp_image)
            #

        if src.ndim != 4:
            src = addAlpha(src)  # 添加alpha
            src.resize((height, width, 4))

        # 转化为灰度图像
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 中值滤波
        imgray = cv2.medianBlur(imgray, 5)

        # 双边滤波
        imgray = cv2.bilateralFilter(imgray, 9, 75, 75)

        # 二值化
        # ret, thresh = cv2.threshold(imgray, 127, 255, 0)

        # Canny 边缘检测代替二值化
        thresh = cv2.Canny(img, 30, 70)

        # 获取外轮廓，精简，改变原图
        # cv2.CHAIN_APPROX_NONE 不精简
        # cv2.RETR_EXTERNAL 只提取外轮廓
        # cv2.RETR_LIST 提取所有
        # cv2.RETR_CCOMP 表示提取所有轮廓并将组织成一个两层结构，其中顶层轮廓是外部轮廓，
        # 第二层轮廓是“洞”的轮廓
        # cv2.RETR_TREE 提取所有轮廓并组织成轮廓嵌套的完整层级结构
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 按面积排序
        areas = np.zeros([len(contours)])
        index = 0  # 面积的下标指针

        # 创建存储轮廓点的文件夹
        if not os.path.exists(home_path + "\\contours"):
            os.mkdir(home_path + "\\contours")
        # 创建存储图片的文件夹
        if not os.path.exists(home_path + "\\img"):
            os.mkdir(home_path + "\\img")
        # 创建存储相对坐标的文件夹
        if not os.path.exists(home_path + "\\offset"):
            os.mkdir(home_path + "\\offset")

        # 遍历轮廓，计算每个轮廓的面积
        for contour in contours:
            areas[index] = cv2.contourArea(contour)
            index = index + 1
        # 对轮廓按面积排序，sortIdx能够得到这些值在原数组中的序号
        areas_s = cv2.sortIdx(areas, cv2.SORT_DESCENDING + cv2.SORT_EVERY_COLUMN)
        (b8, g8, r8, a8) = cv2.split(src)

        # 对每个区域进行处理
        for index in areas_s:
            if areas[index] < width * height * 0.001:
                continue
            m = cv2.moments(contours[index.tolist()[0]])

            # 计算中心矩
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])

            offset_x = (m['m10'] / m['m00']) / height
            offset_y = (m['m01'] / m['m00']) / width

            # 获得轮廓的边缘点
            np.savetxt(home_path + '\\contours\\' + str(cx) + ',' + str(cy),
                       (contours[index.tolist()[0]]).reshape((-1, 2)),
                       fmt='%d',
                       delimiter=',')
            # 获得相对坐标
            contours_points = (contours[index.tolist()[0]]).reshape((-1, 2))
            x_ = contours_points[:, 0]
            y_ = contours_points[:, 1]
            x_ = x_ / height
            y_ = y_ / width
            x_ = x_[:, np.newaxis]
            y_ = y_[:, np.newaxis]
            contours_points = np.concatenate((x_, y_), axis=1)
            np.savetxt(home_path + '\\offset\\' + str(offset_x) + ',' + str(offset_y),
                       contours_points,
                       fmt='%f',
                       delimiter=',')

            # 绘制区域图像，通过将thickness设置为-1可以填充整个区域，否则只绘制边缘
            temp_img = np.zeros(imgray.shape, dtype=np.uint8)
            cv2.drawContours(temp_img, contours, index, [255, 255, 255], -1)
            # 结合灰度图掩膜
            # temp_img = temp_img & imgray

            # 得到彩色的图像
            color_img = cv2.merge([b8 & temp_img, g8 & temp_img, r8 & temp_img, a8 & temp_img])

            # cv2.imshow("img",color_img) 为什么会闪退？
            cv2.imwrite(home_path + '\\img\\' + str(cx) + ',' + str(cy) + '.png', color_img)

    def make_dir(self):
        """
        创建home_path，即各个图片分割后文件的存储文件夹
        :return:
        """
        if not os.path.exists(self._root_dir + '\\data\\'):
            os.mkdir(self._root_dir + '\\data\\')
        for img in self._imgs:
            if not os.path.exists(self._root_dir + '\\data\\' + img.split(".")[0]):
                os.mkdir(self._root_dir + '\\data\\' + img.split(".")[0])

    def run_quere(self):
        """
        依次分割传入图片序列的图片
        :return:分割的图片总数
        """
        i = 0
        for i, img in enumerate(self._imgs):
            print("正在分割第" + str(i + 1) + "张图")
            self.split(self._root_dir + '\\' + img, self._root_dir + '\\data\\' + img.split(".")[0])
            print("第" + str(i + 1) + "张图分割完成")
        return i + 1


if __name__ == "__main__":
    imgs = ["img_6.jpg"]
    ris = RowImgSpliter(imgs, 'PictureBooks')
    ris.make_dir()
    ris.run_quere()
