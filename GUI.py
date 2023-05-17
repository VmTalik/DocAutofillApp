from tkinter import Frame, Tk, Button, GROOVE, LEFT, Label, LabelFrame
from tkinter import filedialog as fd
from PIL import Image as PILImage
from PIL import ImageTk
import cv2
import core


class Window:
    def __init__(self):
        self.count_transport = 0
        self.count_passport = 0
        self.output_tick = None
        self.check_passport = None
        self.check_transport = None
        self.output_image = None
        self.label = None
        self.root = Tk()
        self.root.geometry(f"900x700+400+50")
        self.root.title('Autocomplete')
        self.root.resizable(False, False)
        self.root.config(bg='#DBDADA')

    def draw_widgets(self):
        passport_frame = Frame(self.root)
        passport_frame.pack(anchor="w")
        transport_frame = Frame(self.root)
        transport_frame.pack(anchor="w")
        # fill_frame = Frame(self.root)
        # fill_frame.pack(anchor="w")
        output_frame = LabelFrame(self.root, text="Загруженное изображение", font=("Arial", 10, "bold"))
        output_frame.pack(anchor="e", pady=20)
        Label(passport_frame, width=15, height=1, text="Паспорт РФ", font=("Arial", 12, "bold")).pack(side=LEFT)
        Button(passport_frame, width=15, height=1, text="Загрузить", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8, command=lambda: self.open_image('passport')).pack(side=LEFT)
        self.check_passport = Label(passport_frame)
        self.check_passport.pack(side=LEFT)
        Label(transport_frame, width=30, height=1, text="Свидетельство о регистрации ТС",
              font=("Arial", 12, "bold")).pack(side=LEFT)
        Button(transport_frame, width=15, height=1, text="Загрузить", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8, command=lambda: self.open_image('transport')).pack(side=LEFT)
        self.check_transport = Label(transport_frame)
        self.check_transport.pack(side=LEFT)
        Button(self.root, width=15, height=1, text="Заполнить договор", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8).place(x=80, y=250)
        Button(self.root, width=20, height=1, text="Проверить заполнение", font=("Arial", 11, "bold"),
               relief=GROOVE, bd=8).place(x=70, y=320)
        Button(self.root, width=20, height=1, text="Отбор договоров", font=("Arial", 11, "bold"),
               relief=GROOVE, bd=8).place(x=120, y=600)
        self.label = Label(output_frame)
        self.label.pack()

    def open_image(self, par: str):
        image_path = fd.askopenfilename()
        image_file = fd.askopenfile()
        # print(image_name)
        img = PILImage.open(image_path)
        if (img.width or img.height) >= 2800:
            img = img.reduce(7)
        elif 2000 < (img.width or img.height) < 2800:
            img = img.reduce(4)
        elif 1000 < (img.width or img.height) <= 2000:
            img = img.reduce(3)
        elif 500 < (img.width or img.height) <= 1000:
            img = img.reduce(2)
        else:
            pass
        self.output_image = ImageTk.PhotoImage(img)
        self.change_label_output()
        tick = PILImage.open("checkmark.png")
        tick = tick.reduce(12)
        self.output_tick = ImageTk.PhotoImage(tick)
        if par == "passport":
            self.put_tick(par)
            self.passport_rec(image_path)
        else:
            self.put_tick(par)
        # print(ocr_recognition(image_file))
        # print(core.ocr_recognition(image_name))
        return image_path

    def passport_rec(self, image_path):
        img_proc = core.ImageProcessing(image_path)
        image = img_proc.image_preparation()
        res_img = img_proc.resizing(image, new_width=818, new_height=1162, interp=cv2.INTER_LINEAR)
        res_img_rotate = img_proc.rotation(res_img)
        crop_image_up = img_proc.crop_image(res_img, side="up")
        crop_image_down = img_proc.crop_image(res_img, side="down")
        crop_image_rotate = img_proc.crop_image(res_img_rotate, rotate=True)
        result_up = img_proc.ocr_recognition(crop_image_up)
        result_down = img_proc.ocr_recognition(crop_image_down)
        result_rotate = img_proc.ocr_recognition(crop_image_rotate)
        results = [result_up, result_down, result_rotate]
        img_proc.insert_data_word(results)

    def change_label_output(self):
        self.label.configure(image=self.output_image, height=550, width=450)

    def put_tick(self, par: str):
        # self.count_passport = 0
        # self.count_transport = 0
        if par == 'passport':
            self.check_passport.configure(image=self.output_tick)
            self.count_passport += 1
            if self.count_transport > 0:
                self.check_transport.configure(image=self.output_tick)
        else:
            self.check_transport.configure(image=self.output_tick)
            self.count_transport += 1
            if self.count_passport > 0:
                self.check_passport.configure(image=self.output_tick)

    def run(self):
        self.draw_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    window = Window()
    window.run()
    # print(window.open_image("passport"))
