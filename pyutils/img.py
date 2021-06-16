import os

import cv2
from PIL import Image as PillowImage


class Images(object):

    def __init__(self):
        self.upper_img_offsets = [
            157, 145, 265, 277, 181, 169, 241, 253, 109, 97, 289, 301,
            85, 73, 25, 37, 13, 1, 121, 133, 61, 49, 217, 229, 205, 193
        ]
        self.lower_img_offsets = [
            145, 157, 277, 265, 169, 181, 253, 241, 97, 109, 301, 289,
            73, 85, 37, 25, 1, 13, 133, 121, 49, 61, 229, 217, 193, 205
        ]

    def restore_img(self, bg_img_path):
        '''
        @description: 图像还原
        @param bg_img_path: 待还原的图像路径
        @return: 还原后的图像
        '''
        img = PillowImage.open(bg_img_path)
        height = img.size[1]
        half_height = height >> 1
        new_img = PillowImage.new('RGB', (260, height))

        for i, x in enumerate(self.upper_img_offsets):
            crop = img.crop((x, half_height, x + 10, height))
            new_img.paste(crop, (i * 10, 0))

        for i, x in enumerate(self.lower_img_offsets):
            crop = img.crop((x, 0, x + 10, half_height))
            new_img.paste(crop, (i * 10, half_height))

        restore_img_path = os.path.join(
            os.path.dirname(bg_img_path),
            "restore_" + os.path.basename(bg_img_path))
        new_img.save(restore_img_path)
        new_img.close()

        return restore_img_path

    def get_gap_distance(self, bg_img_path, slide_img_path):
        '''
        @description: 获取图像中缺口的距离
        @params bg_img_path: 还原后的图像路径
        @params slide_img_path: 滑块图像路径
        @return: 缺口距离
        '''
        slide_img = cv2.imread(slide_img_path, 0)
        slide_img = abs(255 - slide_img)
        bg_img = cv2.imread(bg_img_path, 0)
        # 模板匹配, 使用归一化相关系数匹配法
        result = cv2.matchTemplate(slide_img, bg_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_loc[0]
