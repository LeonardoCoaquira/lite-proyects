from tkinter import ttk
from tkinter import LabelFrame,Label,Entry,CENTER,N,S,W,E,Toplevel,END,Entry,StringVar,Button,Tk

import sqlite3
import ctypes

#Screen and Position
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
widht, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

#Windows
widht_index,height_index = 400, 402
widht_edit,height_edit = 195, 110
widht_delete,height_delete = 126, 47

#Screen Center
left = (widht-widht_index)*0.5
top = (height-height_index)*0.5

class Product:

    #Create Database
    db_name = 'database_product.db'
    backup = 'CREATE TABLE IF NOT EXISTS "product" ("id" INTEGER NOT NULL, "name"  TEXT NOT NULL, "price" REAL NOT NULL, PRIMARY KEY("id" AUTOINCREMENT));'
    con1 = sqlite3.connect(db_name)
    Move = con1.cursor()
    Move.execute(backup)
    con1.commit()

    def __init__(self,window):

        self.wind = window
        self.wind.title('Products Application')
        self.wind.geometry("%dx%d+%d+%d" % (widht_index, height_index, left, top))

        #Create a Frame Content
        frame = LabelFrame(self.wind, text = 'Register A New Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        #Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        #Price Input
        Label(frame, text='Price: ').grid(row=2,column=0)
        self.price = Entry(frame)
        self.price.grid(row=2,column=1)

        #Button Add Product
        ttk.Button(frame, text='Save Product',command=self.add_product).grid(row=3,columnspan=2,sticky=W + E)

        #Output Messages
        self.message = Label(text='',fg='red')
        self.message.grid(row = 3, column=0,columnspan=2,sticky=W + E)

        #Table
        self.tree = ttk.Treeview(height=10,columns = 2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Name',anchor=CENTER)
        self.tree.heading('#1',text='Price',anchor=CENTER)
        
        #Buttons
        ttk.Button(text='DELETE',command=self.delete_product).grid(row=5,column=0,sticky=W+E)
        ttk.Button(text='EDIT',command=self.edit_product).grid(row=5,column=1,sticky=W+E)

        self.get_products()

    def run_query(self,query,parameters = ()):

        #Connection To Database
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result

    def get_products(self):
        
        #Clean Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #Quering Data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text=row[1],value=row[2])

    def validation(self):

        return len(self.name.get()) != 0 and len(self.price.get()) != 0
                    
    def add_product(self):

        if self.validation():

            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = ((self.name.get()), self.price.get())

            #Validate decimals
            if self.price.get().isnumeric() == False:
                
                #Check Number of Points
                if self.price.get().count('.') > 1:
                    self.message['text'] = 'Many Points'
                
                #Correct Decimal Point
                elif self.price.get().count('.') == 1:
                    self.run_query(query,parameters)
                    self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
                    self.name.delete(0,END)
                    self.price.delete(0,END)
                    self.get_products()

                #Input Another Number
                else:
                    self.message['text'] = 'Incorrect Data Price'
                    self.price.delete(0,END)

            #Input Only Numbers
            else: 
                self.run_query(query,parameters)
                self.message['text'] = 'Product {} added Successfully'.format(self.name.get())
                self.name.delete(0,END)
                self.price.delete(0,END)
                self.get_products()

        #Empty Entry
        else:
            self.message['text'] = 'Name and Price are Required'

    def delete_product(self):

        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Please Select a Record'
            return

        #Delete Window
        self.name_delete = self.tree.item(self.tree.selection())['text']
        self.delete_wind = Toplevel()
        self.delete_wind.title = 'Delete Product'
        self.delete_wind.geometry("%dx%d+%d+%d" % (widht_delete, height_delete, left-150, top))

        #Removal Tools
        Label(self.delete_wind,text='Are you sure to delete?').grid(row=1,column=1,columnspan=2)
        Button(self.delete_wind,text='YES',command=self.delete).grid(row=2,column=1,sticky=N+E+S+W)
        Button(self.delete_wind,text='NO',command=self.delete_wind.destroy).grid(row=2,column=2,sticky=N+E+S+W)

        self.get_products()

    def delete(self): 
        
        #Delete Inyection
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query,(self.name_delete, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(self.name_delete)
        self.delete_wind.destroy()

        self.get_products()

    def edit_product(self):

        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError:
            self.message['text'] = 'Please Select a Record'
            return

        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title('Edit Product')
        self.edit_wind.geometry("%dx%d+%d+%d" % (widht_edit, height_edit, left+420, top))

        #Old Name
        Label(self.edit_wind,text='Old Name: ').grid(row=0,column=1)
        Entry(self.edit_wind,textvariable=StringVar(self.edit_wind,value = name),state='readonly').grid(row=0,column=2)
         
        #New Name
        Label(self.edit_wind, text='New Name: ').grid(row=1,column=1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row=1,column=2)

        #Old Price
        Label(self.edit_wind,text='Old Price: ').grid(row=2,column=1)
        Entry(self.edit_wind,textvariable=StringVar(self.edit_wind,value = old_price),state='readonly').grid(row=2,column=2)
        
        #New Price
        Label(self.edit_wind, text='New Price: ').grid(row=3,column=1)
        new_price = Entry(self.edit_wind)
        self.edit_new_price = new_price
        new_price.grid(row=3,column=2)

        #Command Button
        Button(self.edit_wind,text='Update',command=lambda:self.edit_records(new_name.get(),new_price.get(),name,old_price)).grid(row=5,column=1,columnspan=2,sticky=W+E)
        
    def edit_records(self,new_name,new_price,name,old_price):

        if (new_name != '') and (new_price != ''):
            
            #Validate Decimals
            if self.edit_new_price.get().isnumeric() == False:

                #Check Number of Points
                if self.edit_new_price.get().count('.') > 1:
                    self.message['text'] = 'Many Points'
                
                #Correct Decimal Point
                elif self.edit_new_price.get().count('.') == 1:
                    query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
                    parameters = (new_name,new_price,name,old_price)
                    self.run_query(query,parameters)
                    self.message['text'] = 'Product {} added Successfully'.format(new_name)
                    self.edit_wind.destroy()
                    self.get_products()

                #Input Another Number
                else:
                    self.message['text'] = 'Incorrect Data Price'
                    self.price.delete(0,END)
            
            #Input Characters
            else:
                query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
                parameters = (new_name,new_price,name,old_price)
                self.run_query(query,parameters)
                self.message['text'] = 'Product {} added Successfully'.format(new_name)
                self.edit_wind.destroy()                

        #Empty Entry
        else:
            self.message['text'] = 'Missing Data'

#Executor
if __name__ == '__main__':
    window = Tk()
    application = Product(window)   
    window.mainloop()
