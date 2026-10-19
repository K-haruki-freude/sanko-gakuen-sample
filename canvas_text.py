import tkinter
root = tkinter.Tk()
root.title("ウィンドウに文字を表示")
cvs = tkinter.Canvas(width=800, height=600, bg="white")
cvs.create_text(200, 200, text="Python", font=("Times New Roman", 40))
cvs.pack()
root.mainloop()