from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from plate_detector import detect_plate
root = Tk()

root.geometry("800x600")
root.resizable(0, 0)


def fileDialog():

    filename = filedialog.askopenfilename(initialdir="/media/aichunks/data1/", title="Select file",
                                               filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

    label = ttk.Label(root, text="Plate Number : ")
    label.grid(column=2, row=1)


    label = ttk.Label(root, text="")
    label.grid(column=3, row=1)
    text = detect_plate(filename)
    label.configure(text=text)

    img = Image.open(filename).resize((350, 250))
    photo = ImageTk.PhotoImage(img)

    label2 = Label(image=photo, width=350, height=250, )
    label2.image = photo
    label2.grid(column=1, row=2)






button = ttk.Button(root, text = "Browse A File",command = fileDialog)
button.grid(column = 1, row = 1,padx=30,pady=30)





root.mainloop()
