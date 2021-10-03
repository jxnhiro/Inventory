from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from pymongo import MongoClient
from collections import OrderedDict

Builder.load_string('''
<DataTable>:
    id: main_window
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id: tableFloor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1, None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor                 
        Rectangle:
            size: self.size
            pos: self.pos
''')
class dataTable(BoxLayout):
    def __init__(self,table = '', **kwargs):
        super().__init__(**kwargs)

        # products = self.get_products()
        products = table
        # STB = {
        # 'TH0': {0:'ST0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},
        # 'TH1': {0:'STM0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},
        # 'TH2': {0:'STMP0',1:'SAMPLED1.0',2:'SAMPLED2.0',3:'SAMPLED4.0'},
        # 'TH3': {0:'STMPL0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},  
        # 'TH4': {0:'STMPLE0',1:'SAMPLE1',2:'SAMPLE2',3:'SAMPLE4'},   
        # }
        #database
        
        column_titles = [k for k in products.keys()]
        rows_len = len(products[column_titles[0]])
        self.columns = len(column_titles)
        #print(rows_len)
        table_data = []
        for t in column_titles:
            table_data.append({'text':str(t),'size_hint_y':None,'height':50, 'bcolor':(0,0,0,0.6)})
        
        for r in range(rows_len):
            for t in column_titles:
                table_data.append({'text':str(products[t][r]),'size_hint_y':None,'height':30, 'bcolor':(0,0,0,0.8)})    
        self.ids.table_floor.data = table_data
        self.ids.tableFloor_layout.cols = self.columns
        
        
    
# class dataTableApp(App):
#     def build(self):
#         return dataTable()
    
if __name__ == '__main__':
    dataTableApp().run()