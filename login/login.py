from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.config import Config
from pymongo import MongoClient
import hashlib
Builder.load_file('login/login.kv')
from kivy.config import Config
Window.maximize()
class loginWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def validateUser(self):
        client = MongoClient()
        db = client.dataInventory
        users = db.users
        
        user = self.ids.usernameField
        pwd = self.ids.passwordField
        info = self.ids.info
        
        uname = user.text
        passwd = pwd.text
        
        user.text = ''
        pwd.text = ''

        if passwd == '' or uname == '':
            info.text = 'Isi form yang kosong'
        else:
            user = users.find_one({'user_name':uname})
            
            if user == None:
                info.text = 'Invalid'
            else:
                passwd = hashlib.sha256(passwd.encode()).hexdigest()
                if passwd == user['password']:
                    des = user['designation']
                    self.parent.parent.parent.ids.scrn_op.children[0].ids.userLoggedIn.text = uname
                    self.parent.parent.parent.ids.scrn_admin.children[0].ids.userLoggedInAdmin.text = uname
                    if des == 'Administrator':
                        Window.maximize()
                        self.parent.parent.current = 'scrnAdmin'
                    else:
                        Window.maximize()
                        self.parent.parent.current = 'scrnOp'
                else:
                    info.text = 'Invalid'
class loginApp(App):
    def build(self):
        return loginWindow()
    
if __name__ =="__main__":
    sa = loginApp()
    sa.run()
