from tkinter import filedialog, ttk, LabelFrame, Label, Entry,CENTER,W,E,N,S,Entry,Tk,Button,StringVar
from subprocess import Popen,PIPE

class Product:

    def __init__(self,window):

        #Save audio and merge it with video
        self.best_audio = []


        #Create window
        self.wind = window
        self.wind.title('Download Video and')

        #Create a Frame Content
        frame = LabelFrame(self.wind, text = 'Downloads Video')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name Input
        Label(frame, text = 'URL: ').grid(row = 1, column = 0)
        self.url = Entry(frame)
        self.url.focus()
        self.url.grid(row = 1, column = 1)

        #Button Add Product
        ttk.Button(frame, text='Search Data',command=self.search_data).grid(row=3,columnspan=1,column=0,sticky=W + E)
        ttk.Button(frame, text='Clean Data',command=self.clean_data).grid(row=3,columnspan=1,column=1,sticky=W + E)
        ttk.Button(frame, text='PATH',command=self.select_path).grid(row=4,column=0,columnspan=2,sticky=W+E)

        self.message_directory = Label(text='',fg='blue')
        self.message_directory.grid(row = 5, column=0,columnspan=2,sticky=W + E)

        #Output Messages
        self.message = Label(text='',fg='red')
        self.message.grid(row = 6, column=0,columnspan=2,sticky=W + E)

        #Table
        self.tree = ttk.Treeview(height=20,columns = ('#0','#1','#2'))
        self.tree.grid(row=7,column=0,columnspan=2,sticky=W+E)
        self.tree.heading('#0',text='ID',anchor=CENTER)
        self.tree.heading('#1',text='Data',anchor=CENTER)
        self.tree.heading('#2',text='Type',anchor=CENTER)
        self.tree.heading('#3',text='Size',anchor=CENTER)


        #Buttons
        ttk.Button(text='Download Audio',command=self.download_audio).grid(row=8,column=0,sticky=W+E)
        ttk.Button(text='Download Video',command=self.download_video).grid(row=8,column=1,sticky=W+E)

    def search_data(self):

        #Quering Data
        command = "youtube-dl -F {}".format(self.url.get())
        process = Popen(command, stdout=PIPE, stderr=None, shell=True)

        #Save the terminal :D
        output = process.communicate()

        #Capture Data in Lists
        abc = output[0].decode()
        list_lines = abc.splitlines()
    

        #List for save the data of video
        self.library = []

        #Index data on tables
        for i in range(len(list_lines)):
            
            if i>3:
                
                #Extract elements for list
                data = list_lines[i]
                list_data1 = data.split()
                self.library.append(list_data1)
                self.cant_data = len(self.library)

                #Search in lists the parameters to index and chane someones
                if not 'iB' in list_data1[-1]:
                    if not 'iB' in list_data1[-1]:
                        list_data1[-1],list_data1[-2] = list_data1[-2],list_data1[-1] 
                
                #Insert Data on Tables
                self.tree.insert('',1,text=list_data1[0],values=(list_data1[2],list_data1[1],list_data1[-1]))
                if list_data1[2] == 'audio':
                    self.best_audio.append(list_data1[0])

    def clean_data(self):

        #Clean Data 
        for i in self.tree.get_children():
            self.tree.delete(i)
    
    def select_path(self):
        self.path_name = filedialog.askdirectory()
        self.message_directory['text'] = self.path_name

    def download_video(self):
        try: 
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError:
            self.message['text'] = 'Please Select a Record'
            return
    
        self.name_value = self.tree.item(self.tree.selection())['text']
        
        #Download video + audio
        self.message['text'] = 'Wait Please'
        self.command = 'youtube-dl -f {}+'.format(self.name_value) + '{} '.format(self.best_audio[-1]) + self.url.get()
        process = Popen(self.command,cwd=self.path_name, stdout=PIPE, stderr=None, shell=True)
        process.communicate()
        self.message['text'] = 'Downloaded Video'
        

    def download_audio(self):

        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Please Select a Record'
            return
        

        self.name_value = self.tree.item(self.tree.selection())['text']
        
        self.message['text'] = 'Wait Please'
        
        self.command= 'youtube-dl -f {} '.format(self.name_value) + self.url.get()
        process = Popen(self.command,cwd=self.path_name, stdout=PIPE, stderr=None, shell=True)
        process.communicate()
        self.message['text'] = 'Downloaded Audio'
        

#Executor
if __name__ == '__main__':
    window = Tk()
    application = Product(window)   
    window.mainloop()