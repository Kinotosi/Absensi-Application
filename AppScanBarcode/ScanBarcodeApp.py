from pyzbar import pyzbar
from tkinter import *
from PIL import Image, ImageTk
from xlsxwriter.workbook import Workbook
from base64 import b64encode
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox
import argparse
import cv2
import datetime
import base64
import time
import qrcode


#====================MAIN MENU=================================
class MainApp:
    def __init__(self, window):
        #Root
        self.window = window
        self.window.geometry('500x570')
        self.window.title("Barcode Scan Application")
        self.window.resizable(False, False)

        #Frame
        self.frame = Frame(self.window, relief=RIDGE, borderwidth=2)
        self.frame.pack(fill=BOTH, expand=1)
        self.frame.config(background="black")

        #Top Label
        self.label_title = Label(self.frame, text="SCAN BARCODE FOSTI", bg="black", fg="gainsboro")
        self.label_title.config(font=("times new roman", 30))
        self.label_title.pack(side=TOP)

        #Background
        self.picture = PhotoImage(file="mainbg.png")
        self.background = Label(self.frame, image=self.picture)
        self.background.pack(fill=X)

        #Submenu
        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)

        self.sub_menu = Menu(self.menu)
        self.menu.add_cascade(label="help", menu=self.sub_menu)
        self.sub_menu.add_command(label="About", command=self.HelpMenu)

        #Button
        self.btn_start = Button(self.frame, padx=5, pady=5, width=39, bg="black", text="Start", command=self.StartMenu,
                                relief=GROOVE, fg="gainsboro", font=('helvetica 15 bold'))
        self.btn_start.place(x=25, y=170)
        self.btn_option = Button(self.frame, padx=5, pady=5, width=39, bg="black", text="Data Record",
                                 command=self.OptionMenu, relief=GROOVE, fg="gainsboro", font=('helvetica 15 bold'))
        self.btn_option.place(x=25, y=240)
        self.btn_qrbarcode = Button(self.frame, padx=5, pady=5, width=39, bg="black", text="Generate QR Barcode", command=self.QRBarcode, relief=GROOVE, fg="gainsboro", font=('helvetica 15 bold'))
        self.btn_qrbarcode.place(x=25, y=310)
        self.btn_exit = Button(self.frame, padx=5, pady=5, width=39, bg="black", text="Exit", command=self.Exit,
                               relief=GROOVE, fg="gainsboro", font=('helvetica 15 bold'))
        self.btn_exit.place(x=25, y=380)

        #Mainloop
        self.window.mainloop()

    def StartMenu(self):
        return StartApp()

    def OptionMenu(self):
        return DataMenu()

    def QRBarcode(self):
        return QrBarcode()

    def Exit(self):
        self.result = tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want to exit", icon="warning")
        if self.result == "yes":
            exit()

    def HelpMenu(self):
        tkinter.messagebox.showinfo("About", "Scan Barcode Application \n"
                                             "Version   : 1.0 \n"
                                             "Copyright : Fosti")

#====================DATA MENU=================================
class DataMenu:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Data Record")
        self.window.resizable(False, False)

        self.Title()
        self.texts.set('Data Record Fosti')

        #Frame
        self.frame_data = Frame(self.window, width=800, height=400, bd=1, relief="raise")
        self.frame_data.pack(side=TOP)
        self.frame_btn = Frame(self.window, width=300, height=100, bd=0, relief="raise")
        self.frame_btn.pack(side=RIGHT)
        self.frame_text = Label(self.frame_btn)
        self.frame_text.pack(side=TOP)

        #Button
        self.btn_export = Button(self.frame_btn, text="Export", command=self.Export, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_export.pack(side=RIGHT)
        self.btn_delete = Button(self.frame_btn, text="Delete", command=self.Delete, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_delete.pack(side=RIGHT)
        self.btn_delete_all = Button(self.frame_btn, text="Delete All", command=self.DeleteAll, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_delete_all.pack(side=RIGHT)
        self.btn_reload = Button(self.frame_btn, command=self.Reload, text="Reload", padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_reload.pack(side=RIGHT)
        self.btn_exit = Button(self.frame_btn, command=self.Exit, text="Exit", padx=30, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_exit.pack(side=RIGHT)

        #Tree
        self.scrollbary = Scrollbar(self.frame_data, orient=VERTICAL)
        self.tree = ttk.Treeview(self.frame_data, columns=("MemberID", "Time", "Name", "NIM", "Gender", "Email","Information", "Status"), selectmode="extended", height=10, yscrollcommand=self.scrollbary.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.tree.heading('MemberID', text="MemberID", anchor=W)
        self.tree.heading('Time', text="Time", anchor=W)
        self.tree.heading('Name', text="Name", anchor=W)
        self.tree.heading('NIM', text="NIM", anchor=W)
        self.tree.heading('Gender', text="Gender", anchor=W)
        self.tree.heading('Email', text="Email", anchor=W)
        self.tree.heading('Information', text="Information", anchor=W)
        self.tree.heading('Status', text="Status", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=0)
        self.tree.column('#2', stretch=NO, minwidth=0, width=80)
        self.tree.column('#3', stretch=NO, minwidth=0, width=250)
        self.tree.column('#4', stretch=NO, minwidth=0, width=150)
        self.tree.column('#5', stretch=NO, minwidth=0, width=100)
        self.tree.column('#6', stretch=NO, minwidth=0, width=200)
        self.tree.column('#7', stretch=NO, minwidth=0, width=250)
        self.tree.column('#8', stretch=NO, minwidth=0, width=100)

        self.tree.pack(side=TOP)

        self.tree_insert()

    def Title(self):
        self.texts = StringVar()

        self.titles = Label(self.window, textvariable=self.texts, font=('times new roman', 30), bg='black', fg='gainsboro')
        self.titles.pack(fill=BOTH, expand=1)

    def tree_insert(self):
        conn = sqlite3.connect('formdata.db')
        cursor = conn.cursor()
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM `member` ORDER BY `times` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            self.tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        conn.commit()
        cursor.close()
        conn.close()

    def Export(self):
        workbook = Workbook('Absensi.xlsx')
        worksheet = workbook.add_worksheet()

        conn = sqlite3.connect('formdata.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `member` ORDER BY `times` ASC")
        fetch = cursor.execute("SELECT * FROM `member` ORDER BY `names` ASC")

        top = ["No", "Waktu", "Nama", "NIM", "P/L", "Email","Keterangan", "Status"]

        for n, data_top in enumerate(top):
            worksheet.write(0, n, data_top)

        i = 1

        for data in fetch:
            worksheet.write(i, 0, str(i))
            worksheet.write(i, 1, data[1])
            worksheet.write(i, 2, data[2])
            worksheet.write(i, 3, data[3])
            worksheet.write(i, 4, data[4])
            worksheet.write(i, 5, data[5])
            worksheet.write(i, 6, data[6])
            worksheet.write(i, 7, data[7])
            i += 1

        workbook.close()
        self.frame_text.config(text="Succesfully convert record to Excel", fg="green")

    def Delete(self):
        if not self.tree.selection():
            self.frame_text.config(text="Please select an item firts", fg="red")
        else:
            result=tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want delete this record", icon="warning")
            if result == 'yes':
                curItem = self.tree.focus()
                contents = (self.tree.item(curItem))
                selectitem = contents['values']
                self.tree.delete(curItem)
                conn = sqlite3.connect('formdata.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selectitem[0])
                conn.commit()
                cursor.close()
                conn.close()
            self.frame_text.config(text="Successfully deleted the data", fg="green")

    def DeleteAll(self):
        result = tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want delete all record", icon="warning")
        if result == 'yes':
            conn = sqlite3.connect('formdata.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM `member`")
            conn.commit()
            cursor.close()
            conn.close()
            self.tree_insert()
            self.frame_text.config(text="Successfully deleted all data", fg="green")

    def Reload(self):
        self.tree_insert()
        self.frame_text.config(text="Successfully update record", fg="green")

    def Exit(self):
        result = tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want to exit", icon="warning")
        if result == 'yes':
            self.window.destroy()

#====================QR BARCODE MENU===========================
class QrBarcode:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Generate QR Barcode")
        self.window.resizable(False, False)

        self.Title()
        self.text.set('Generate QR Barcode')

        # Variable
        self.name = StringVar()
        self.nim = StringVar()
        self.gender = StringVar()
        self.email = StringVar()
        self.info = StringVar()

        #Frame
        self.frame_entry = Frame(self.window, width=500, height=500, bd=0, relief="raise")
        self.frame_entry.pack(side=TOP)
        self.frame_btn = Frame(self.window, width=300, height=100, bd=0, relief="raise")
        self.frame_btn.pack(side=RIGHT)
        self.frame_text = Label(self.frame_btn)
        self.frame_text.pack(side=TOP)
        self.RodioGroup = Frame(self.frame_entry)
        self.Male = Radiobutton(self.RodioGroup, text="Male", variable=self.gender, value="Laki-Laki", font=('helvetica', 16)).pack(side=LEFT)
        self.Female = Radiobutton(self.RodioGroup, text="Female", variable=self.gender, value="Perempuan", font=('helvetica', 16)).pack(side=LEFT)

        #Button
        self.btn_generate = Button(self.frame_btn, text="Generate", command=self.Generate, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_generate.pack(side=RIGHT)
        self.btn_clear = Button(self.frame_btn, text="Clear All", command=self.ClearEnter, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_clear.pack(side=RIGHT)
        self.btn_exit = Button(self.frame_btn, text="Exit", command=self.Exit, padx=30, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_exit.pack(side=RIGHT)

        #Label
        self.txt_name = Label(self.frame_entry, text="Name", font=('helvetica', 16), bd=15)
        self.txt_name.grid(row=0, sticky="e")
        self.txt_nim = Label(self.frame_entry, text="NIM", font=('helvetica', 16), bd=5)
        self.txt_nim.grid(row=1, sticky="e")
        self.txt_gender = Label(self.frame_entry, text="Gender", font=('helvetica', 16), bd=5)
        self.txt_gender.grid(row=2, sticky="e")
        self.text_email = Label(self.frame_entry, text="Email", font=('helvetica', 16), bd=5)
        self.text_email.grid(row=3, sticky="e")
        self.txt_info = Label(self.frame_entry, text="Information", font=('helvetica', 16), bd=5)
        self.txt_info.grid(row=4, sticky="e")

        #Entry
        self.entry_nama = Entry(self.frame_entry, textvariable=self.name, width=30)
        self.entry_nama.grid(row=0, column=1)
        self.entry_nim = Entry(self.frame_entry, textvariable=self.nim, width=30)
        self.entry_nim.grid(row=1, column=1)
        self.RodioGroup.grid(row=2, column=1)
        self.entry_email = Entry(self.frame_entry, textvariable=self.email, width=30)
        self.entry_email.grid(row=3, column=1)
        self.entry_info = Entry(self.frame_entry, textvariable=self.info, width=30)
        self.entry_info.grid(row=4, column=1)

        self.currentbarcode = []
        self.name_barcode = ""

        self.Text()

        self.window.mainloop()

    def Exit(self):
        result = tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want exit?", icon="warning")
        if result == "yes":
            self.window.destroy()

    def Title(self):
        self.text = StringVar()

        self.titles = Label(self.window, textvariable=self.text, font=('times new roman', 30), bg='black', fg='gainsboro')
        self.titles.pack(fill=BOTH, expand=1)

    def Text(self):
        date = datetime.datetime.now().date()
        date_split = str(date).split("-")
        num = len(self.currentbarcode)
        date_num = str(date_split[2])+str(date_split[1])+str(date_split[0])+str(num)
        self.name_barcode = "FB"+date_num+".jpg"
        self.currentbarcode.append("1")


    def ConvertBarcode(self, input):
        logo = Image.open('favicon.png')
        basewidth = 75
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr_big.add_data(input)
        qr_big.make()
        img_qr_big = qr_big.make_image(fill_color="black", back_color="white").convert('RGB')
        pos = ((img_qr_big.size[0] - logo.size[0]) // 2, (img_qr_big.size[1] - logo.size[1]) // 2)
        img_qr_big.paste(logo, pos)
        img_qr_big.save(self.name_barcode)
        self.frame_text.config(text="Succesfully create barcode", fg="green")
        self.entry_nama.delete(0, 'end')
        self.entry_nim.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_info.delete(0, 'end')
        self.Text()

    def ClearEnter(self):
        self.entry_nama.delete(0, 'end')
        self.entry_nim.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_info.delete(0, 'end')
        self.frame_text.config(text="Succesfully clear all entry", fg="green")


    def Generate(self):
        nama = self.name.get()
        nim = self.nim.get()
        gender = self.gender.get()
        email = self.email.get()
        inform = self.info.get()

        if nama == "" or gender == "" :
            tkinter.messagebox.showinfo("Alert", "Please complete record Name and Gender", icon="warning")
        else:
            result = tkinter.messagebox.askquestion("Generate Barcode", "Are you sure you want generate this record")
            if result == "yes":
                text = "FOSTI2020/"+nama+"/"+nim+"/"+gender+"/"+email+"/"+inform
                texts = b64encode(bytes(text, 'utf-8'))
                texts_split = str(texts).split("'")
                text_ori = texts_split[1]
                self.ConvertBarcode(text_ori)


#====================START MENU================================
class StartApp:
    def __init__(self):
        #Main Start Menu
        self.window = Toplevel()
        self.window.title("Barcode Scan Application")
        self.window.resizable(False, False)

        #DataBases
        self.DataBases()

        #Time
        self.Time()
        self.TimeUpdate()

        #VideoCapture
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", 0)

        self.args = CommandLineParse().args
        self.csv = CommandLineParse().csv
        self.found = CommandLineParse().found

        self.res = (500, 300)
        self.width, self.height = self.res
        self.current_info = []

        #Canvas
        self.canvas = Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack(side=TOP)
        self.canvas_info = Frame(self.window, width=500, height=300, bd=1, relief="raise")
        self.canvas_info.pack(side=TOP)
        self.canvas_btn = Frame(self.window, width=300, height=100, bd=0, relief="raise")
        self.canvas_btn.pack(side=RIGHT)
        self.text_result = Label(self.canvas_btn)
        self.text_result.pack(side=TOP)

        #Button
        self.btn_export = Button(self.canvas_btn, text="Export", command=self.Export, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_export.pack(side=RIGHT)
        self.btn_delete = Button(self.canvas_btn, text="Delete", command=self.Delete, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_delete.pack(side=RIGHT)
        self.btn_reload = Button(self.canvas_btn, text="Reload", command=self.Reload, padx=20, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_reload.pack(side=RIGHT)
        self.btn_exit = Button(self.canvas_btn, text="Exit", command=self.Exit, padx=30, bg="black", relief=GROOVE, fg="gainsboro", font=('helvetica 10 bold'))
        self.btn_exit.pack(side=RIGHT)

        #Tree
        self.scrollbary = Scrollbar(self.canvas_info, orient=VERTICAL)
        self.tree = ttk.Treeview(self.canvas_info, columns=("MemberID", "Time", "Name", "Status"), selectmode="extended", height=10, yscrollcommand=self.scrollbary.set)
        self.scrollbary.config(command=self.tree.yview)
        self.scrollbary.pack(side=RIGHT, fill=Y)
        self.tree.heading('MemberID', text="MemberID", anchor=W)
        self.tree.heading('Time', text="Time", anchor=W)
        self.tree.heading('Name', text="Name", anchor=W)
        self.tree.heading('Status', text="Status", anchor=W)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=0)
        self.tree.column('#2', stretch=NO, minwidth=0, width=80)
        self.tree.column('#3', stretch=NO, minwidth=0, width=250)
        self.tree.column('#4', stretch=NO, minwidth=0, width=150)
        self.tree.pack(side=TOP)

        #Input VideoCapture to Canvas
        self.delay = 10
        self.update()

        #Input database from sqlite3 to tree
        self.tree_insert()

    def Exit(self):
        result = tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want to exit", icon="warning")
        if result == 'yes':
            self.window.destroy()

    def Delete(self):
        if not self.tree.selection():
            self.text_result.config(text="Please select an item firts", fg="red")
        else:
            result=tkinter.messagebox.askquestion("Barcode Scan Application", "Are you sure you want delete this record", icon="warning")
            if result == 'yes':
                curItem = self.tree.focus()
                contents = (self.tree.item(curItem))
                selectitem = contents['values']
                self.tree.delete(curItem)
                conn = sqlite3.connect('formdata.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selectitem[0])
                conn.commit()
                cursor.close()
                conn.close()
                self.text_result.config(text="Successfully deleted the data", fg="green")

    def Export(self):
        workbook = Workbook('Absensi.xlsx')
        worksheet = workbook.add_worksheet()

        conn = sqlite3.connect('formdata.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `member` ORDER BY `times` ASC")
        fetch = cursor.execute("SELECT * FROM `member` ORDER BY `times` ASC")

        top = ["No", "Waktu", "Nama", "NIM", "P/L", "Email","Keterangan", "Status"]

        for n, data_top in enumerate(top):
            worksheet.write(0, n, data_top)

        i = 1

        for data in fetch:
            worksheet.write(i, 0, str(i))
            worksheet.write(i, 1, data[1])
            worksheet.write(i, 2, data[2])
            worksheet.write(i, 3, data[3])
            worksheet.write(i, 4, data[4])
            worksheet.write(i, 5, data[5])
            worksheet.write(i, 6, data[6])
            worksheet.write(i, 7, data[7])
            i += 1

        workbook.close()
        self.text_result.config(text="Succesfully covert record to Excel", fg="green")

    def tree_insert(self):
        conn = sqlite3.connect('formdata.db')
        cursor = conn.cursor()
        self.tree.delete(*self.tree.get_children())
        cursor.execute("SELECT * FROM `member` ORDER BY `times` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            self.tree.insert('', 'end', values=(data[0], data[1], data[2], data[7]))
        conn.commit()
        cursor.close()
        conn.close()

    def Reload(self):
        self.tree_insert()
        self.text_result.config(text="Succesfully update record", fg="green")

    def Time(self):
        self.teksJam = StringVar()

        self.hours = Label(self.window, textvariable=self.teksJam, font=('helvetica', 20, 'bold'), bg='black', fg='gainsboro')
        self.hours.pack(fill=BOTH, expand=1)

    def TimeUpdate(self):
        datHour = time.strftime("%H:%M:%S", time.localtime())

        self.hour = time.strftime("%H", time.localtime())
        self.minute = time.strftime("%M", time.localtime())
        second = time.strftime("%S", time.localtime())

        self.teksJam.set(datHour)
        self.timer = self.window.after(1000, self.TimeUpdate)

    def DataBases(self):
        self.conn = sqlite3.connect('formdata.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, times TEXT, names TEXT, nim TEXT, gender TEXT, email TEXT, keterangan TEXT, status TEXT)")

    def info(self):
        f = open("barcodes.csv", "r")
        jumInfo = len(self.current_info)
        texts = f.readlines()
        jumtext = len(texts)
        tam = "1"

        if jumtext > jumInfo:
            baca = texts[jumInfo]
            text = baca.split(", ")
            times = text[0]
            status = text[2]
            identitas = text[1].split("'")
            identitas_split = identitas[1].split("/")
            code = identitas_split[0]
            names = identitas_split[1]
            nims = identitas_split[2]
            genders = identitas_split[3]
            email = identitas_split[4]
            ket = identitas_split[5]

            if str(code) != "FOSTI2020" or str(code) is None:
                tkinter.messagebox.showinfo("Alert", "Your code not same or broken, Try Again!", icon="warning")
            else:
                self.DataBases()
                self.cursor.execute("INSERT INTO `member` (times, names, nim, gender, email,keterangan, status) VALUES(?, ?, ?, ?, ?, ?, ?)", (str(times), str(names), str(nims), str(genders), str(email), str(ket), str(status)))
                self.conn.commit()
                self.cursor.close()
                self.conn.close()
                self.tree_insert()
                self.text_result.config(text="Successfully scan barcode", fg="green")
            self.current_info.append(tam)

    def get_frame(self, ret=None):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcode_data = barcode.data.decode("utf-8")
                barcode_text = base64.b64decode(barcode_data)
                text = "Barcode Scan...."
                cv2.putText(frame, text, (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if barcode_text not in self.found:
                    date = datetime.datetime.now()
                    hour = date.hour
                    minute = date.minute
                    self.time = str(hour)+':'+str(minute)
                    self.csv.write("{}, {}, {}, {}".format(self.time, barcode_text, "Hadir", "\n"))
                    self.csv.flush()
                    self.found.add(barcode_text)
                self.info()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def update(self):
        ret, frame = self.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.after(self.delay, self.update)

#====================ARGSPARSE==================================
class CommandLineParse:
    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
        self.args = vars(ap.parse_args())

        self.csv = open(self.args["output"], "w")
        self.found = set()

#====================MAIN MENTHOD==============================
if __name__ == "__main__":
    root = Tk()
    MainApp(root)