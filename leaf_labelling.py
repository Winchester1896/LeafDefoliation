import PIL
from PIL import ImageTk, Image
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

root = Tk()
root.title("Image Labelling")

def get_directory_name(caption):
    dirname = filedialog.askdirectory(parent=root,initialdir="/",title=caption)
    if len(dirname ) > 0:
        print (' You chose %s' % dirname)
        return dirname

def get_file_name(caption):
    file = tkinter.filedialog.askopenfile(parent=root,mode='rb',title=caption)
    if file != None:
        data = file.read()
    #file.close()
    print (" I got %d bytes from this file." % len(data))
    return file

class TruthSeeker(Frame):
    def __init__(self,master):
        Frame.__init__(self,master=None)

        frame = ttk.Frame(self, borderwidth=5, relief="sunken", width=500, height=500)
        self.namelbl = ttk.Label(self, text="Classification:")
        self.class_name = ttk.Entry(self)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(1, weight=1)
        
        ##
        ## Define variables
        self.onevar = BooleanVar()
        self.twovar = BooleanVar()
        ##
        self.classificationvar = StringVar()
        ##
        self.onevar.set(False)
        self.twovar.set(False)
        
        ## Define Widgits
        #self.options checkboxes (not used at this tome)
        self.one = ttk.Checkbutton(self, text="Option One", variable=self.onevar, onvalue=True)
        self.two = ttk.Checkbutton(self, text="Option Two", variable=self.twovar, onvalue=True)
        ##
        ## Classification combobox
        self.classification = ttk.Combobox(self, textvariable=self.classificationvar)
        ## Get classification names
        # (1) Get file with class names
        self.valid_classes = []
        print('Please select file with class names: ')
        classes_file = get_file_name('Select file with class names: ')
        with open(classes_file.name) as f:
            for line_1 in f:
                self.valid_classes.append(line_1)

        self.classification['value'] = self.valid_classes
        self.classification.bind('<<ComboboxSelected>>', self.on_clasification)
        self.classificationvar.set(self.valid_classes[0])
        self.classification.set(self.classificationvar.get())
     
        self.cancel = ttk.Button(self, text="Cancel",command = self.on_cancel) #retunss without saving line
        self.apply = ttk.Button(self, text="Apply",command = self.on_apply) #adds  a bb,value to line
        self.finish = ttk.Button(self, text="Finish",command = self.on_finish) # returns line after processing this image


        self.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self.namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), pady = 15,padx=5)
        
        self.x = self.y = 0
        print(root.winfo_screenwidth(), root.winfo_screenheight())
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.canvas = Canvas(self, cursor="cross",width = sw-150,height =sh-150)

        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(column=0, row=0, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
        self.sbarv.grid(row=0,column=2,stick=N+S)
        self.sbarh.grid(row=2,column=0,columnspan = 2, sticky=E+W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        ### add kestroke reply
        self.master.bind('a', self.on_apply)
        self.master.bind('c', self.on_cancel)
        self.master.bind('f', self.on_finish)

        ### Define grid and format and place place widgets
        self.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self.namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), pady = 15,padx=5)

        ##
        self.one.grid(column=0, row=3)
        self.two.grid(column=1, row=3)
        self.cancel.grid(column=2, row=3)
        self.apply.grid(column=3, row=3)
        self.finish.grid(column=4, row=3)
        ##


        self.rect = None

        self.start_x = None
        self.start_y = None

        self.clasificationvar = StringVar()
        self.curX = 0
        self.curY = 0

        self.line = ""

        self.image_index = 0
        self.out_file_name = ""
        self.image_files_directory = ""
        self.image_files = ""

        self.classification.grid(column=3, row=0, columnspan=2, sticky=(N, E, W), pady=35, padx=5)

        ## Get name of directory containing images to process
        print ('Please select directory containing image files: ')
        self.image_files_directory = get_directory_name('Select directory containing image files:')

        ## Get list of image files to process
        self.image_files = os.listdir(self.image_files_directory)
        print (self.image_files)

        self.image_index = 0
        self.line = self.image_files_directory + '/' + self.image_files[0]

        self.im = PIL.Image.open(self.line)
        self.wazil,self.lard=self.im.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.imgpane = self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

        ### (2) Get output file directory name
        print ('Please select dirctory for output file: ')
        self.out_file_directory = get_directory_name('Select output file directory: ')
        self.out_file_name = self.out_file_directory + '/dataset.txt'



    def on_cancel(self, _event = None):
        self.canvas.delete("all")
        self.line = self.image_files_directory + '/' + self.image_files[self.image_index]
        tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.image = tk_im  # line added to fix bug in canvas widget
        self.canvas.create_image(0,0,anchor="nw",image=tk_im,tag = 'current_image')
        print(self.line)

    def on_apply(self, _event=None):
        self.canvas.create_rectangle(self.start_x, self.start_y, self.curX, self.curY,
                                     outline='green',width = 2.0, tags = 'class 1')
        self.canvas.create_text((self.start_x+self.curX)/2,(self.start_y+self.curY)/2,
                                text=str(self.valid_classes[self.classification.current()]),fill='red',
                                width = int(.8*(self.curX-self.start_x)))
        self.line = self.line + ' ' + str(int(self.start_x)) + ' ' + str(int(self.start_y))
        self.line = self.line + ' ' + str(int(self.curX)) + ' ' + str(int(self.curY))
        self.line = self.line + ' ' + str(self.classification.current())
        #print ('.8*(self.curX-self.start_x)',.8*(self.curX-self.start_x))
        print(self.line)

    def on_finish(self,_event=None):
        dsf = open(self.out_file_name,'a+')
        self.line = self.line + '\n'
        dsf.write(self.line)
        dsf.close()
        self.image_index += 1
        self.line = ""
        if  self.image_index < len(self.image_files):
            self.line = self.image_files_directory + '/' + self.image_files[self.image_index]
            print(self.line)
            #create new canvas
            self.canvas.delete("all")
            self.im = PIL.Image.open(self.line)
            tk_im = ImageTk.PhotoImage(self.im)
            self.canvas.image = tk_im  # line added to fix bug in canvas widget
            self.canvas.create_image(0,0,anchor="nw",image=tk_im,tag = 'current_image')
            print('current image position',self.canvas.coords('current_image'))
            
    def on_clasification(self,event):
        print (self.clasificationvar.get())

    def on_button_press( self,event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # deletge old test rectangle and creat new one 
        self.canvas.delete('test_rec')
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red',tag = 'test_rec')

    def on_move_press(self,event):
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units') 
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units') 
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)    

    def on_button_release(self,event):
        pass    

# Start main loop
if __name__ == "__main__":
    root = Tk()
    root.title("Truth Seeker")
    app = TruthSeeker(root)
    app.pack()
    root.mainloop()