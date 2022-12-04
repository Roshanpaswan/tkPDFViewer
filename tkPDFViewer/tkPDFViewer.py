try:
    import tkinter as tk
    import fitz
    from tkinter import ttk
    from threading import Thread
    import math
    from PIL import Image, ImageTk
    import platform
except Exception as e:
    print(f"This error occured while importing neccesary modules or library {e}")

class ShowPdf():
    img_object_li = []
    tkimg_object_li = []

    def pdf_view(self, master, width=1200, height=600, pdf_location="", bar=True, load="after", dpi=100):

        self.frame = tk.Frame(master, width=width, height=height, bg="white")

        scroll_y = ttk.Scrollbar(self.frame, orient="vertical")
        scroll_x = ttk.Scrollbar(self.frame, orient="horizontal")

        scroll_x.pack(fill="x", side="bottom")
        scroll_y.pack(fill="y", side="right")

        percentage_view = 0
        percentage_load = tk.StringVar()

        if bar==True and load=="after":
            self.display_msg = ttk.Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
            loading.pack(side=tk.TOP, fill=tk.X)

        self.text = tk.Text(self.frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, width=width, height=height)
        self.text.pack(fill="x")

        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)

        def add_img():
            precentage_dicide = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                pix = page.get_pixmap(dpi=dpi)
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                self.img_object_li.append(img)
                self.tkimg_object_li.append(ImageTk.PhotoImage(img))
                if bar==True and load=="after":
                    precentage_dicide = precentage_dicide + 1
                    percentage_view = (float(precentage_dicide)/float(len(open_pdf))*float(100))
                    loading['value'] = percentage_view
                    percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%")
            self.orig_size = self.tkimg_object_li[0].width()

            if bar==True and load=="after":
                loading.pack_forget()
                self.display_msg.pack_forget()

            for im in self.tkimg_object_li:
                self.text.image_create(tk.END, image=im)
                self.text.insert(tk.END, "\n")
            self.text.configure(state="disabled")

        def start_pack():
            t1 = Thread(target=add_img)
            t1.start()

        if load=="after":
            master.after(250, start_pack)
        else:
            start_pack()
        
        def zoom_in(event=None):
            self.text.configure(state="normal")
            self.text.delete(1.0, tk.END)
            scroll_x_state = scroll_x.get()
            scroll_y_state = scroll_y.get()
            res = 1 + 0.1*self.orig_size/self.tkimg_object_li[0].width()
            for i, im in enumerate(self.img_object_li):
                self.tkimg_object_li[i] = ImageTk.PhotoImage(im.resize((int(res*self.tkimg_object_li[i].width()), int(res*self.tkimg_object_li[i].height())), Image.ANTIALIAS))
                self.text.image_create(tk.END, image=self.tkimg_object_li[i])
                self.text.insert(tk.END, "\n")
            self.text.update()
            self.text.xview_moveto(scroll_x_state[0])
            self.text.yview_moveto(scroll_y_state[0])
            self.text.update()
            self.text.configure(state="disabled")
        
        def zoom_out(event=None):
            self.text.configure(state="normal")
            self.text.delete(1.0, tk.END)
            scroll_x_state = scroll_x.get()
            scroll_y_state = scroll_y.get()
            res = 1 - 0.1*self.orig_size/self.tkimg_object_li[0].width()
            for i, im in enumerate(self.img_object_li):
                self.tkimg_object_li[i] = ImageTk.PhotoImage(im.resize((int(res*self.tkimg_object_li[i].width()), int(res*self.tkimg_object_li[i].height())), Image.ANTIALIAS))
                self.text.image_create(tk.END, image=self.tkimg_object_li[i])
                self.text.insert(tk.END, "\n")
            self.text.update()
            self.text.xview_moveto(scroll_x_state[0])
            self.text.yview_moveto(scroll_y_state[0])
            self.text.update()
            self.text.configure(state="disabled")

        def zooming(event=None):
            if event.delta > 0:
                zoom_in(event)
            else:
                zoom_out(event)
        
        if platform.system() == 'Windows' or 'Darwin':
            self.text.bind('<Control-plus>', zoom_in)
            self.text.bind('<Control-minus>', zoom_out)
            self.text.bind('<Control-MouseWheel>', zooming)
        elif platform.system() == 'Linux':
            # cant bind neither control + nor control - events on linux for some reason
            self.text.bind('<Control-Button-4>', zoom_in)
            self.text.bind('<Control-Button-5>', zoom_out)
        else:
            pass
        
        return self.frame
