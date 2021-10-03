from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

from collections import OrderedDict
from pymongo import MongoClient
from utilities.dataTable import dataTable
from datetime import datetime
import hashlib

Builder.load_file('admin/admin.kv')
class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(.7,.7)
        
class adminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db = client.dataInventory
        self.users = db.users
        self.products = db.stocks
        self.notify = Notify()
        
        # STB = {
        # 'TH0': {0:'ST0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},
        # 'TH1': {0:'STM0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},
        # 'TH2': {0:'STMP0',1:'SAMPLED1.0',2:'SAMPLED2.0',3:'SAMPLED4.0'},
        # 'TH3': {0:'STMPL0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},  
        # 'TH4': {0:'STMPLE0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},   
        # }
        #database
        # print(self.get_products())
        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = dataTable(table=users)
        content.add_widget(userstable)
        
        prodContent = self.ids.scrn_product_contents
        products = self.get_products()
        productsTable = dataTable(table=products)
        prodContent.add_widget(productsTable)
    def logout(self):
        self.parent.parent.current = 'scrnSi'
    def add_user_field(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name',multiline = False)
        crud_last = TextInput(hint_text='Last Name',multiline = False)
        crud_user = TextInput(hint_text='Username',multiline = False)
        crud_pwd = TextInput(hint_text='Password',multiline = False)
        crud_des = Spinner(text='Operator',values=['Operator','Administrator'])
        crud_submit = Button(text='Add',size_hint_x = None,width=100,on_release=lambda x: self.add_user(crud_first.text,crud_last.text,crud_user.text,crud_pwd.text,crud_des.text))
         
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)
    def add_product_field(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
         #code name weight price stock order
        crud_code = TextInput(hint_text='Product Code',multiline = False)
        crud_name = TextInput(hint_text='Product Name',multiline = False)
        crud_weight = TextInput(hint_text='Product Weight',multiline = False)
        crud_price = TextInput(hint_text='Product Price',multiline = False)
        crud_stock = TextInput(hint_text='Product Stock',multiline = False)
        crud_order = TextInput(hint_text='Last Date Product Order',multiline = False)  
        crud_submit = Button(text='Add',size_hint_x = None,width=100,on_release=lambda x:self.add_product(crud_code.text,crud_name.text,crud_weight.text,crud_price.text,crud_stock.text,crud_order.text))
    
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_stock)
        target.add_widget(crud_price)
        target.add_widget(crud_order)
        target.add_widget(crud_submit)
    
    def add_user(self,first,last,user,pwd,des):
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if first == '' or last == '' or user == '' or pwd == '':
            self.notify.add_widget(Label(text='[b]Semua Detail Harus Diisi',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            content = self.ids.scrn_contents
            content.clear_widgets()
            self.users.insert_one({'first_name':first,'last_name':last,'user_name':user,'password':pwd,'designation':des,'date':datetime.now()})
            users = self.get_users()
            userstable = dataTable(table=users)
            content.add_widget(userstable)
            
    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()
        #code name weight price stock order
    def add_product(self,code,name,weight,price,stock,order):
        if code == '' or name == '' or weight == '' or price == '' or stock == '' or order == '':
            self.notify.add_widget(Label(text='[b]Semua Detail Harus Diisi',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:                                                                                              
            self.products.insert_one({'product_code':code,'product_name':name,'product_weight':weight,'product_price':price,'in_stock':stock,'order':order})
            content = self.ids.scrn_product_contents
            content.clear_widgets()
            prods = self.get_products()
            stockstable = dataTable(table=prods)
            content.add_widget(stockstable)
            
            
            
    
    def update_user_field(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='Nama Pertama',multiline = False)
        crud_last = TextInput(hint_text='Nama Akhir',multiline = False)
        crud_user = TextInput(hint_text='Username',multiline = False)
        crud_pwd = TextInput(hint_text='Password',multiline = False)
        crud_des = Spinner(text='Operator',values=['Operator','Administrator'])
        crud_submit = Button(text='Edit',size_hint_x = None,width=100,on_release=lambda x: self.update_user(crud_first.text,crud_last.text,crud_user.text,crud_pwd.text,crud_des.text))
         
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)
    
    def update_product_field(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        #code name weight price stock order
        crud_code = TextInput(hint_text='Kode Produk',multiline = False)
        crud_name = TextInput(hint_text='Nama Produk',multiline = False)
        crud_weight = TextInput(hint_text='Berat Produk',multiline = False)
        crud_price = TextInput(hint_text='Harga Produk',multiline = False)
        crud_stock = TextInput(hint_text='Berapa Terjual',multiline = False)
        crud_order = TextInput(hint_text='Terakhir Order Produk',multiline = False)                                           #code name weight price stock order
        crud_submit = Button(text='Edit',size_hint_x = None,width=100,on_release=lambda x:self.update_product(crud_code.text,crud_name.text,crud_weight.text,crud_price.text,crud_stock.text,crud_order.text))
    
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_order)
        
        target.add_widget(crud_submit)
        
    def update_user(self,first,last,user,pwd,des):
        
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if user == '':
            self.notify.add_widget(Label(text='[b]Semua Detail Harus Diisi',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            user = self.users.find_one({'user_name':user})
            if user == None:
                self.notify.add_widget(Label(text='[b]Invalid',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 2) 
            else:
                if first == '':
                    first = user['first_name']
                if last == '':
                    last = user['last_name']
                if pwd == '':
                    pwd = user['password']
                self.users.update_one({'user_name':user},{'$set':{'first_name':first,'last_name':last,'user_name':user,'password':pwd,'designation':des,'date':datetime.now()}})
                content = self.ids.scrn_contents
                content.clear_widgets()
                users = self.get_users()
                userstable = dataTable(table=users)
                content.add_widget(userstable)
    #code name weight price stock order
    def update_product(self,code,name,weight,price,stock,order):
        
        
        if code == '':
            self.notify.add_widget(Label(text='[b]Semua Detail Harus Diisi',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            target_code = self.products.find_one({'product_code':code})
            if target_code == None:
                self.notify.add_widget(Label(text='[b]Invalid',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 2)
            else:
                #code name weight price stock order
                if name == '':
                    name = target_code['product_name']
                if weight == '':    
                    weight = target_code['product_weight']
                if price == '':    
                    price = target_code['product_price']
                if stock == '':    
                    stock = target_code['in_stock']
                if order == '':   
                    order = target_code['order']                                                            #code name weight price stock order
                self.products.update_one({'product_code':code},{'$set':{'product_code':code,'product_name':name,'product_weight':weight,'product_price':price,'in_stock':stock,'order':order}})
                content = self.ids.scrn_product_contents
                content.clear_widgets()
                products = self.get_products()
                stocktable = dataTable(table=products)
                content.add_widget(stocktable)
        
    def remove_user_field(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='Username')
        crud_submit = Button(text='Hapus',size_hint_x = None,width=100,on_release=lambda x: self.remove_user(crud_user.text))       
    
        target.add_widget(crud_user)
        target.add_widget(crud_submit)
    
    def remove_product_field(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Kode Produk')
        crud_submit = Button(text='Hapus',size_hint_x = None,width=100,on_release=lambda x: self.remove_product(crud_code.text))       
    
        target.add_widget(crud_code)
        target.add_widget(crud_submit)
        
    def remove_user(self, user):
        
        
        if user == '':
            self.notify.add_widget(Label(text='[b]Semua Detail Harus Diisi',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            target_user = self.users.find_one({'user_name':user})
            if target_user == None:
                self.notify.add_widget(Label(text='[b]Invalid',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 2)
            else:
                content = self.ids.scrn_contents
                content.clear_widgets()
                self.users.remove({'user_name':user})
        
                users = self.get_users()
                userstable = dataTable(table=users)
                content.add_widget(userstable)
        
    def remove_product(self,code):
        
        if code == '':
            self.notify.add_widget(Label(text='[b]Semua Detail Harus Diisi',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 2)
        else:
            target_code = self.products.find_one({'product_code':code})
            if target_code == None:
                self.notify.add_widget(Label(text='[b]Invalid',markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 2)
            else:
                content = self.ids.scrn_product_contents
                content.clear_widgets()
                self.products.remove({'product_code':code})
        
                products = self.get_products()
                stocktable = dataTable(table=products)
                content.add_widget(stocktable)
                
    def get_users(self):        
        client = MongoClient()
        db = client.dataInventory
        users = db.users
        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['passwords'] = {}
        _users['designations'] = {}
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []  
        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            designations.append(user['designation'])
        # print(designations)
        users_length = len(first_names)
        indexV = 0
        while indexV < users_length:
            _users['first_names'][indexV] = first_names[indexV]
            _users['last_names'][indexV] = last_names[indexV]
            _users['user_names'][indexV] = user_names[indexV]
            _users['passwords'][indexV] = passwords[indexV]
            _users['designations'][indexV] = designations[indexV]
            indexV += 1
        
        return _users
    
    def get_products(self):        
        client = MongoClient()
        db = client.dataInventory
        products = db.stocks
        _stocks = OrderedDict()
        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['product_price'] = {}
        _stocks['in_stock'] = {}
        _stocks['order'] = {}
        product_code = []
        product_name = []
        product_weight = []
        product_price = []  
        in_stock = []
        order = []  
        
        for product in products.find():
            product_code.append(product['product_code'])
            name = product['product_name']
            if len(name) > 10:
                name = name[:10] + '...'
            product_name.append(name)
            product_weight.append(product['product_weight'])
            product_price.append(product['product_price'])
            in_stock.append(product['in_stock'])
            order.append(product['order'])
        # print(designations)
        products_length = len(product_code)
        indexV = 0
        while indexV < products_length:
            _stocks['product_code'][indexV] = product_code[indexV]
            _stocks['product_name'][indexV] = product_name[indexV]
            _stocks['product_weight'][indexV] = product_weight[indexV]
            _stocks['product_price'][indexV] = product_price[indexV]
            _stocks['in_stock'][indexV] = in_stock[indexV]
            _stocks['order'][indexV] = order[indexV]
            indexV += 1
        
        return _stocks
    
    def change_screen(self, instance):
        if instance.text == 'Products':
            self.ids.scrn_manager.current = 'productContent'
        elif instance.text == 'Users':
            self.ids.scrn_manager.current = 'usersContent'
class adminApp(App):
    def build(self):
        
        return adminWindow()
    
if __name__ == '__main__':
    adminApp().run()