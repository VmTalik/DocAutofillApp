from tkinter import Frame, Tk, Button, GROOVE, LEFT, Label, LabelFrame
from tkinter import filedialog as fd
from PIL import Image as PILImage
from PIL import ImageTk


class Window:
    def __init__(self):
        self.output_image = None
        self.label = None
        self.root = Tk()
        self.root.geometry(f"900x700+400+50")
        self.root.title('Autocomplete')
        self.root.resizable(False, False)
        self.root.config(bg='#DBDADA')
        # self.label = Label(self.root, width=50, height=35)

    def draw_widgets(self):
        passport_frame = Frame(self.root)
        passport_frame.pack(anchor="w")
        transport_frame = Frame(self.root)
        transport_frame.pack(anchor="w")
        # fill_frame = Frame(self.root)
        # fill_frame.pack(anchor="w")
        output_frame = LabelFrame(self.root, text="Загруженное изображение", font=("Arial", 10, "bold"))
        output_frame.pack(anchor="e",pady=20)
        Label(passport_frame, width=15, height=1, text="Паспорт РФ", font=("Arial", 12, "bold")).pack(side=LEFT)
        Button(passport_frame, width=15, height=1, text="Загрузить", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8, command=self.open_image).pack(side=LEFT)
        Label(transport_frame, width=30, height=1, text="Свидетельство о регистрации ТС",
              font=("Arial", 12, "bold")).pack(side=LEFT)
        Button(transport_frame, width=15, height=1, text="Загрузить", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8, command=self.open_image).pack(side=LEFT)
        Button(self.root, width=15, height=1, text="Заполнить договор", font=("Arial", 12, "bold"),
               relief=GROOVE, bd=8).place(x=80, y=200)
        self.label = Label(output_frame)
        self.label.pack()

    def open_image(self):
        image_name = fd.askopenfilename()
        image_file = fd.askopenfile()
        # print(image_name)
        img = PILImage.open(image_name)
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
        return image_file, image_name

    def change_label_output(self):
        self.label.configure(image=self.output_image, height=550, width=450)

    def run(self):
        self.draw_widgets()
        self.root.mainloop()


if __name__ == '__main__':
    window = Window()
    window.run()
