from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
import re
from pymongo import MongoClient

#nama tidak bisa operator
Builder.load_file('control/control.kv')
Window.maximize()

class controlWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        self.db = client.dataInventory
        self.stocks = self.db.stocks
        global countC
        countC = 0
        self.cart = []
        self.qty = []
        self.total = 0
        self.pre = ''
    def clearAll(self):
        global countC
        global preview
        if countC > 0:
            details.clear_widgets()
            products_container.clear_widgets()
            self.cart.clear()
            self.qty.clear()
            self.total = 0
            preview.text = "Nama Toko\nJalan\n\nTelepon Toko: \nNo Bon:\nTanggal: \n\n"
        else:
            pass
    def printNotepad(self, receipt, user):
        fob = open('Nota.txt','w+')
        fob.write("Pembeli: " + user + "\n")
        fob.write(receipt)
    def logout(self):
        self.parent.parent.current = 'scrnSi'
    def updatePurchases(self):
        global countC
        countC += 1
        kode = self.ids.productCodeInput.text
        global products_container
        products_container = self.ids.products
        global details
        details = BoxLayout(size_hint_y=None,height=30,pos_hint={'top': 1})
        target_code = self.stocks.find_one({'product_code':kode})
        if target_code == None:
            pass
        else:
            for stock in self.stocks.find():
                if kode == stock['product_code']:
                    stockBef = int(stock['in_stock'])
                    stockFin = str(int(stock['in_stock']) - 1)
                else:
                    pass
            
            if stockBef > 0:
                products_container.add_widget(details)
                
                productCode = Label(text=kode, size_hint_x = .15, color=(0,0,0,1))
                productName = Label(text=target_code['product_name'], size_hint_x = .2, color=(0,0,0,1))
                productQty = Label(text='1', size_hint_x = .05, color=(0,0,0,1))
                productDisc = Label(text='0.00', size_hint_x = .175, color=(0,0,0,1))
                productPrice = Label(text =target_code['product_price'], size_hint_x = .175, color=(0,0,0,1))
                productTotal = Label(text='0.00', size_hint_x = .175, color=(0,0,0,1))
                details.add_widget(productCode)
                details.add_widget(productName)
                details.add_widget(productQty)
                details.add_widget(productDisc)
                details.add_widget(productPrice)
                details.add_widget(productTotal)
                
                #update preview info
                pname = productName.text
                pprice = int(productPrice.text)
                pqty = str(1)
                self.total += pprice
                purchase_total = '_\n\nTotal\t\t\t\t\t\t\t\tRp'+str(self.total)+',00'
                self.ids.produk_sekarang.text = pname
                self.ids.harga_sekarang.text = str(pprice)
                global preview
                preview = self.ids.receipt_preview
                #focus
                prev_text = preview.text
                _prev = prev_text.find('_')
                if _prev > 0:
                    prev_text = prev_text[:_prev]

                ptarget = -1
                for i,c in enumerate(self.cart):
                    if c == kode:
                        ptarget = i

                if ptarget >= 0:
                    pqty = self.qty[ptarget]+1
                    self.qty[ptarget] = pqty
                    expr = '%s\t\tx\d\t'%(pname)
                    rexpr = pname + '\t\tx'+str(pqty)+'\t'
                    nu_text = re.sub(expr,rexpr,prev_text)
                    preview.text = nu_text + purchase_total 
                else:
                    self.cart.append(kode)
                    self.qty.append(1)
                    new_preview = '\n'.join([prev_text, pname+'\t\tx'+pqty+'\t\t'+str(pprice),purchase_total])
                    preview.text = new_preview
                
                # for stock in self.stocks.find():
                #     if kode == stock['product_code']:
                #         stockFin = str(int(stock['in_stock']) - 1)
                #     else:
                #         pass
                
                self.stocks.update_one({'product_code':kode},{'$set':{'in_stock':stockFin}})
                #self.ids.discInput.text = '0'
                self.ids.qtyInput.text = str(pqty)
                self.pre = preview.text
            else:
                pass
            
class controlApp(App):
    def build(self):
        return controlWindow()
    
    
    
if __name__ == "__main__":
    aplikasiKontrol = controlApp()
    aplikasiKontrol.run()