from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

from admin.admin import adminWindow
from login.login import loginWindow
from control.control import controlWindow

class inventoryWindow(BoxLayout):
    admin_widget = adminWindow()
    login_widget = loginWindow()
    control_widget = controlWindow()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.ids.scrn_si.add_widget(self.login_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.control_widget)
class inventoryApp(App):
    def build(self):
        return inventoryWindow()
    
if __name__ == '__main__':
    ia = inventoryApp()
    ia.run()