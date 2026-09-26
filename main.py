import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

PORTS = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,
         1433,3306,3389,5432,5900,6379,8080,8443,27017]

class ScanApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.target = TextInput(hint_text='IP', multiline=False,
                                size_hint_y=None, height=50)
        root.add_widget(self.target)
        btn = Button(text='SCAN', size_hint_y=None, height=50)
        btn.bind(on_press=self.start)
        root.add_widget(btn)
        self.out = Label(text='Ready', size_hint_y=None)
        self.out.bind(texture_size=lambda i, v: setattr(i, 'size', v))
        sv = ScrollView()
        sv.add_widget(self.out)
        root.add_widget(sv)
        return root

    def start(self, *_):
        h = self.target.text.strip()
        if not h:
            self.out.text = 'no target'
            return
        self.out.text = 'scanning...'
        threading.Thread(target=self.run_scan, args=(h,), daemon=True).start()

    def run_scan(self, host):
        found = []
        for p in PORTS:
            try:
                s = socket.socket()
                s.settimeout(0.8)
                if s.connect_ex((host, p)) == 0:
                    found.append('port %d open' % p)
                s.close()
            except:
                pass
        self.out.text = '\n'.join(found) if found else 'none'

ScanApp().run()
