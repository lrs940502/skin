import numpy as np
import cv2
import os
class Solution:
    def skin(self,path,file):
        imname =path
        # 读入图像
        '''
        使用函数 cv2.imread() 读入图像。这幅图像应该在此程序的工作路径，或者给函数提供完整路径.
        警告：就算图像的路径是错的，OpenCV 也不会提醒你的，但是当你使用命令print(img)时得到的结果是None。
        '''
        #--------------------------分割手部-------------------------#
        img = cv2.imread(imname, cv2.IMREAD_COLOR)
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb) # 把图像转换到YUV色域
        (y, cr, cb) = cv2.split(ycrcb) # 图像分割, 分别获取y, cr, br通道图像
        # 高斯滤波, cr 是待滤波的源图像数据, (5,5)是值窗口大小, 0 是指根据窗口大小来计算高斯函数标准差
        cr1 = cv2.GaussianBlur(cr, (5, 5), 0) # 对cr通道分量进行高斯滤波
        # 根据OTSU算法求图像阈值, 对图像进行二值化
        _, skin1 = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #cv2.imshow("image CR", cr1)
        #cv2.imshow("Skin Cr+OSTU", skin1)
        size = 15
        kernel = np.ones((size, size), dtype=np.uint8)
        #skin1 = cv2.erode(skin1, kernel, iterations=1)
        #skin1 = cv2.dilate(skin1, kernel, iterations=1)
        skin1 = cv2.dilate(cv2.erode(skin1, kernel), kernel)
        print(skin1.shape)
        skin=cv2.bitwise_and(img,img,mask=skin1)
        file=file.split(".")[0]
        cv2.imwrite("images_save/{}.jpg".format(file),skin)
        #cv2.waitKey(0)
if __name__=="__main__":
     files=os.listdir("images")
     solution=Solution()
     for file in files:
         #print(file)
         path=os.path.join("images/",file)
         solution.skin(path,file)