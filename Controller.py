import PreProcesser
import ImgSpliter
import Filter
import time
import os
import shutil


def main():
    if os.path.exists("PictureBooks\\data"):
        shutil.rmtree("PictureBooks\\data")
    ppr = PreProcesser.RowPreProcesser("PictureBooks")
    img_list = ppr.retrieve()
    isr = ImgSpliter.RowImgSpliter(img_list, "PictureBooks")
    isr.make_dir()
    start = time.time()
    count = isr.run_quere()
    end = time.time()
    print("总耗时%d秒，平均耗时%d秒" % (end - start, (end - start) / count))
    Filter.Filter.dup_remove("PictureBooks\\data")


if __name__ == "__main__":
    main()
    pwd = os.getcwd()
    path = os.path.join(pwd, "PictureBooks\\data")
    os.system("explorer " + path)
    os.system("AnimationMaker.exe")
    os.system("pause")
