from tkPDFViewer import tkPDFViewer as pdf
from tkinter import*
root = Tk()

#create object like this.
variable1 = pdf.ShowPdf()
#Add your pdf location and width and height.
variable2 = variable1.pdf_view(root,pdf_location=r"C:\Users\DELL\Documents\Salary2020.pdf",width=50,height=100)
variable2.pack()
root.mainloop()
