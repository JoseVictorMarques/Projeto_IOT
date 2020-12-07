from tkinter import *

def myClick():
    myLabel = Label(root, text =" Searching Roof Images...")
    myLabel.pack()

root = Tk()
root.title('Eroof - Verify roofs')
root.iconbitmap('images/drone_figure.ico')
root.geometry('380x380')

myButton = Button(root, text = "Search", command = myClick)
myButton.pack()

photo = PhotoImage(file ='images/roof_background.png')
labelphoto = Label(root, image = photo)
labelphoto.pack()


root.mainloop()
