import cv2
import easyocr
from docxtpl import DocxTemplate
import numpy as np
from datetime import datetime


class ImageProcessing:
    context = {}

    def __init__(self, image_path):
        self.image_path = image_path
        self.image_preparation()
        self.image = None

    def image_preparation(self):
        f = open(self.image_path, "rb")
        chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        self.image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = self.image.shape
        if w > h:
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        return self.image

    @staticmethod
    def rotation(img):
        """Функция поворота изображения на 90 градусов против часовой стрелки"""
        (h, w) = img.shape[:2]
        center = (int(w / 2), int(h / 2))
        rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1)
        rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
        return rotated

    @staticmethod
    def resizing(img, new_width=None, new_height=None, interp=cv2.INTER_LINEAR):
        h, w = img.shape[:2]

        if new_width is None and new_height is None:
            return img

        if new_width is None:
            ratio = new_height / h
            dimension = (int(w * ratio), new_height)

        else:
            ratio = new_width / w
            dimension = (new_width, int(h * ratio))
        res_img = cv2.resize(img, dimension, interpolation=interp)
        return res_img

    @staticmethod
    def crop_image(img, rotate=False, side="up"):
        h, w = img.shape
        if rotate is False:
            crop_img = img[int(0.05 * h):int(0.3 * h), int(0.05 * w):int(0.91 * w)]
        elif rotate is True:
            crop_img = img[int(0.15 * h):int(0.23 * h), int(0.6 * w):int(0.99 * w)]
        if side == "down":
            crop_img = img[int(0.5 * h):int(0.85 * h), int(0.37 * w):int(0.92 * w)]
        return crop_img

    @staticmethod
    def ocr_recognition(img):
        reader = easyocr.Reader(["ru"])
        result = reader.readtext(img, detail=0, paragraph=True, text_threshold=0.89)
        # print(result)
        return result

    @classmethod
    def insert_data_word(cls, lst: list):
        parts_split_up = "".join(lst[0]).split()
        passport_info = " ".join(parts_split_up)

        parts_split_down = " ".join(lst[1]).split()
        res_lst_down = []
        num = 0
        for i in parts_split_down:
            if len(i) >= 2 and num < 3:
                res_lst_down.append(i)
                num += 1
        surname = res_lst_down[0]
        name = res_lst_down[1]
        patronymic = res_lst_down[2]

        s_res_right = "".join(lst[2]).replace(" ", "")
        count = 0
        series_lst = []
        number_lst = []
        s_res_right_lst = list(s_res_right)
        res_right_lst = list(map(int, s_res_right_lst))
        for i in res_right_lst:
            if count < 4:
                series_lst.append(i)
            else:
                number_lst.append(i)
            count += 1
        series = "".join(list(map(str, series_lst)))
        number = "".join(list(map(str, number_lst)))

        context_new = {'surname': surname, 'name': name, 'patronymic': patronymic, 'series': series, 'number': number,
                       "passport_info": passport_info}
        cls.context.update(context_new)

    @classmethod
    def render_word(cls):
        try:
            series = cls.context["series"]
            number = cls.context["number"]
            doc = DocxTemplate("GNZ.docx")
            doc.render(cls.context)
            doc.save(f"all_doc\GNZ_result{series}{number}.docx")
        except KeyError:
            doc = DocxTemplate("GNZ.docx")
            doc.render(cls.context)
            doc.save("all_doc\GNZ_result.docx")


class TCProcessing(ImageProcessing):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.image_path = image_path
        self.image_preparation()
        self.image = None

    def image_preparation(self):
        f = open(self.image_path, "rb")
        chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        self.image = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = self.image.shape
        return self.image

    @staticmethod
    def crop_image(img, side="down"):
        h, w = img.shape
        if w > h and side == "down":
            crop_img = img[int(0.9 * h):int(0.98 * h), int(0.07 * w):int(0.42 * w)]
        elif w < h and side == "down":
            crop_img = img[int(0.8 * h):int(0.95 * h), int(0.15 * w):int(0.9 * w)]
        elif w > h and side == "up":
            crop_img = img[int(0.2 * h):int(0.29 * h), int(0.27 * w):int(0.5 * w)]
        elif w < h and side == "up":
            crop_img = img[int(0.15 * h):int(0.26 * h), int(0.6 * w):int(0.94 * w)]
        return crop_img

    @classmethod
    def insert_data_word(cls, lst: list):
        parts_split_up = "".join(lst[0]).split()
        register_sign_tc = "".join(parts_split_up)
        s_res_down = "".join(lst[1]).replace(" ", "")
        s_res_down_lst = list(s_res_down)
        seria_tc = "".join(s_res_down_lst[:4])
        number_tc = "".join(s_res_down_lst[-6:])
        current_datetime = datetime.now()
        ye = str(current_datetime.year)[-2:]
        month = str(current_datetime.month)
        if len(month) == 1:
            month = '0' + month
        day = str(current_datetime.day)
        if len(day) == 1:
            day = '0' + day

        context_new = {'register_sign_tc': register_sign_tc, 'seria_tc': seria_tc, 'number_tc': number_tc,
                       'ye': ye, 'month': month, 'day': day}
        cls.context.update(context_new)
