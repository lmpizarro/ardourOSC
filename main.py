#qpy:kivy
'''
'''

try:
    import kivy
except ImportError:
    import androidhelper
    import sys
    sys.exit(0)


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


config1 = {'Play':{'topic':"/transport_play", 'load':[]}, 
          'Stop':{'topic':'/transport_stop', 'load':[]},
          'FFWD':{'topic':'/ffwd', 'load':[]},
          'REW':{'topic':'/rewind', 'load':[]},
          'end':{'topic':'/goto_end', 'load':[]},
          'start':{'topic':'/goto_start', 'load':[]},
          'order':['Play', 'Stop', 'FFWD','REW', 'end', 'start']
          }

config2 = {'>Marker':{'topic':"/next_marker", 'load':[]}, 
          '<Marker':{'topic':'/prev_marker', 'load':[]},
          '+Marker':{'topic':'/add_marker', 'load':[]},
          '-Marker':{'topic':'/remove_marker', 'load':[]},
          'pLoop':{'topic':'/access_action', 'load':['Transport/Loop']},
          'edMixer':{'topic':'/access_action', 'load':['Common/toggle-editor-and-mixer']},
          'order':['>Marker', '<Marker', '+Marker','-Marker','pLoop', 'edMixer']
          }

config3 = {'QUIT':{'topic':'/access_action', 'load':['Common/Quit']},
           'Save':{'topic':'/access_action', 'load':['Common/Save']},
           'Undo':{'topic':'/access_action', 'load':['Editor/undo']},
           'Redo':{'topic':'/access_action', 'load':['Editor/redo']},
           'order':['Undo','Redo','Save', 'QUIT']
          }


from OSC import OSCClient, OSCMessage
import OSC

global net_adress
global port_number 
port_number = 3819
net_adress = '192.168.14.39'

osc_client = OSCClient()
osc_client.connect( (net_adress, port_number) )


class Message():
    def __init__(self, app, message):
        self.message = message
        self.app = app

    def getFunc(self):
        def func(p):
            topic = self.message['topic']
            load = self.message['load']
            
            mess = OSCMessage(topic)
            print mess
            if len(load) > 0:
               mess.append(load[0])
            print mess
            try:
                osc_client.connect((self.app.net_addr, int(self.app.port_nbr)))
                osc_client.send( mess )
            except OSC.OSCClientError, e:
                print 'oss connection error'
        return func

class TestApp(App):

    def row(self, config):
        layout1 = BoxLayout(orientation='horizontal')
        # use a (r, g, b, a) tuple
        
        blue = (0, 0, 1.5, 2.5)
        red = (2.5, 0, 0, 1.5)

        for k in config['order']:
            but = Button(text=k, size=(95, 95),)
            cb = Message(self, config[k])
            but.bind(on_press=cb.getFunc())
            layout1.add_widget(but)
        return layout1 

    def net_set(self):
        layout1 = BoxLayout(orientation='horizontal')
        # use a (r, g, b, a) tuple
        

        but = Button(text="net set", size=(95, 95),)
        but.bind(on_press=self.popup_callback)
        layout1.add_widget(but)
        return layout1

    def ontext_addr(self, instance, value):
        print('The address value: ', value)
        self.net_addr = value

    def ontext_port(self, instance, value):
        print('The port value:', value)
        self.port_nbr = value


    def pop_up_content(self, popup):
        from kivy.uix.textinput import TextInput


        layout1 = BoxLayout(orientation='vertical')
        l = Label(text='Adress')
        net_address = TextInput(text=self.net_addr)

        net_address.bind(text=self.ontext_addr)


        l_port = Label(text='Port')
        net_port = TextInput(text=str(self.port_nbr))

        net_port.bind(text=self.ontext_port)

        # create content and add to the popup
        close_but = Button(text='Close!')
        # bind the on_press event of the button to the dismiss function
        close_but.bind(on_press=popup.dismiss)

        layout1.add_widget(l)
        layout1.add_widget(net_address)

        layout1.add_widget(l_port)
        layout1.add_widget(net_port)

        layout1.add_widget(close_but)
        return layout1

    def popup_callback(self, instance):
        popup = Popup(title='NETWORK SETTINGS')
        popup.content = self.pop_up_content(popup)

        popup.open()
        return True


    def left(self):
        vLayout = BoxLayout(orientation='vertical')
        row1 = self.row(config1)
        row2 = self.row(config2)
        row3 = self.row(config3)
        set_net = self.net_set()
        vLayout.add_widget(row1)
        vLayout.add_widget(row2)
        vLayout.add_widget(row3)
        vLayout.add_widget(set_net)
        return vLayout


    def build(self):
 
        self.net_addr = net_adress
        self.port_nbr = port_number

        hLayout = BoxLayout(orientation='horizontal')
        
        
   
        hLayout.add_widget(self.left())
        print '...............', hLayout.width


        return hLayout 

app = TestApp()
app.run()

