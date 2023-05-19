from tkinter import Frame, Tk, Button, GROOVE, LEFT, Label, LabelFrame, Toplevel, Entry
from tkinter import filedialog as fd
from PIL import Image as PILImage
from PIL import ImageTk
import cv2, os
import core
import db


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
               relief=GROOVE, bd=8, command=self.fill_contract).place(x=80, y=250)
        Button(self.root, width=20, height=1, text="Проверить заполнение", font=("Arial", 11, "bold"),
               relief=GROOVE, bd=8, command=self.check_filling).place(x=70, y=320)
        Button(self.root, width=20, height=1, text="Внести договор в БД", font=("Arial", 11, "bold"),
               relief=GROOVE, bd=8, command=self.add_contract_to_db).place(x=70, y=420)
        Button(self.root, width=20, height=1, text="Отбор договоров", font=("Arial", 11, "bold"),
               relief=GROOVE, bd=8, command=self.contract_selection).place(x=120, y=600)
        self.label = Label(output_frame)
        self.label.pack()

    def open_image(self, par: str):
        image_path = fd.askopenfilename()
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
            self.tc_rec(image_path)
        return image_path

    @staticmethod
    def passport_rec(image_path):
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

    @staticmethod
    def tc_rec(image_path):
        img_proc = core.TCProcessing(image_path)
        image = img_proc.image_preparation()
        res_img = img_proc.resizing(image, new_width=818, new_height=1162, interp=cv2.INTER_LINEAR)
        crop_image_up = img_proc.crop_image(res_img, side="up")
        crop_image_down = img_proc.crop_image(res_img, side="down")
        result_up = img_proc.ocr_recognition(crop_image_up)
        result_down = img_proc.ocr_recognition(crop_image_down)
        results_two_pages = [result_up, result_down]
        img_proc.insert_data_word(results_two_pages)

    @staticmethod
    def fill_contract():
        core.ImageProcessing.render_word()

    @staticmethod
    def check_filling():
        try:
            contract_dict = core.ImageProcessing.context
            series = contract_dict["series"]
            number = contract_dict["number"]
            os.startfile(f'all_doc\GNZ_result{series}{number}.docx', 'edit')
        except KeyError:
            print('Загружено только ТС без паспорта! ')
            os.startfile(f'all_doc\GNZ_result.docx', 'edit')

    @staticmethod
    def add_contract_to_db():
        contract_dict = core.ImageProcessing.context
        if len(contract_dict) > 6:
            name = contract_dict["name"]
            surname = contract_dict["surname"]
            patronymic = contract_dict["patronymic"]
            date = "20" + contract_dict["ye"] + '-' + contract_dict["month"] + "-" + contract_dict["day"]
            series = contract_dict["series"]
            number = contract_dict["number"]
            word_name = f'all_doc\GNZ_result{series}{number}.docx'
            db.insert_data(name, surname, patronymic, series, number, date, word_name)

    def contract_selection(self):
        ChildWindow(self.root)

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


class ChildWindow:
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.root.geometry(f"900x700+400+50")
        self.root.title('database search')
        self.root.resizable(False, False)
        self.root.config(bg='#DBDADA')
        self.entry = None
        self.draw_widgets()

    def draw_widgets(self):
        Label(self.root, text="Отбор по ФИО", font=("Arial", 14, "bold")).grid(row=1, column=3, pady=8)
        Label(self.root, width=15, height=1, text="ФИО", font=("Arial", 12, "bold")).grid(row=2, column=0, ipady=4)
        self.full_name = Entry(self.root, width=35, bd=4, font=("Arial", 12, "bold"))
        self.full_name.grid(row=3, column=1, ipady=4)
        Button(self.root, width=15, height=1, text="Отбор", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8, command=self.get_full_name).grid(row=3, column=4)

        Label(self.root, text="Отбор по дате создания", font=("Arial", 14, "bold")).grid(row=6, column=3, pady=10)
        Label(self.root, width=15, height=2, text="Дата создания\n(yyyy-mm-dd)", font=("Arial", 12, "bold")).grid(row=8,
                                                                                                                  column=0,
                                                                                                                  ipady=4)
        self.date = Entry(self.root, width=35, bd=4, font=("Arial", 12, "bold"))
        self.date.grid(row=9, column=1, ipady=4)
        Button(self.root, width=15, height=1, text="Отбор", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8, command=self.get_date).grid(row=9, column=4)

    def get_full_name(self):
        full_name = self.full_name.get().upper()
        print(full_name)
        full_name_lst = full_name.split()
        if len(full_name_lst) != 3:
            print('Ошибка ввода')
        else:
            name = full_name_lst[1]
            surname = full_name_lst[0]
            patronymic = full_name_lst[2]
            self.get_contract_from_db('', name, surname, patronymic)

    def get_date(self):
        date = self.date.get()
        print(date)
        self.get_contract_from_db(date)

    @staticmethod
    def get_contract_from_db(date, name='', surname='', patronymic=''):
        if date:
            db.read_data(date)
        else:
            db.read_data('', name, surname, patronymic)
