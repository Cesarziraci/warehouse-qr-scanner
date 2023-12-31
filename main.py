import kivy
import gspread
import smtplib
from PIL import Image
from enum import Enum
from time import ctime
from pyzbar.pyzbar import decode
from oauth2client.service_account import ServiceAccountCredentials

kivy.require('2.0.0')
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from email.mime.text import MIMEText
from kivy.uix.gridlayout import GridLayout
from email.mime.multipart import MIMEMultipart
from kivy.uix.screenmanager import Screen, ScreenManager

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("sigit-apps-cc25c0f862ec.json", scope)
client = gspread.authorize(creds)
s = client.open('AlmacenManto')
sheet3 = s.worksheet("Hoja 2")
sheet1 = s.worksheet("Hoja 1")

msg = MIMEMultipart()
password = "pass"
msg['From'] = "From"
msg['To'] = "To"
msg['subject']= "Stock Almacen"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(msg["From"],password)

Builder.load_string('''

<MainScreen>:
    GridLayout:
        padding: 45
        spacing: 45
        cols : 1
        rows: 3
    
        canvas:
            Color: 
                rgb: 1, 1, 1
            Rectangle:
                size: self.size
                pos: self.pos

        Image: 
            source: 'SIGIT.png'
            size_hint_x: 0.23
            allow_stretch: True
        
        Button:
            id: retirar
            text: 'Retirar material'
            on_press: root.ret()
            height: '48dp'
            size_hint: .5, .75
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 70
            
        Button:
            id: anadir
            text: 'Añadir material'
            on_press: root.an()
            height: '48dp'
            size_hint: .5, .75
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 70

<RetirarScreen>:
    GridLayout:
        cols:1
        rows:9
        padding: 10
        apacing: 5
        canvas:
            Color: 
                rgb: 1, 1, 1
            Rectangle:
                size: self.size
                pos: self.pos

        Image: 
            source: 'SIGIT.png'
            size_hint_x: 0.21
            allow_stretch: True

        ToggleButton:
            text: 'Abrir Escaner'
            on_press: root.open_camera()
            height: '48dp'
            size_hint: .5, .85
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 40

        Label: 
            text: 'Nombre y apellidos: '
            color: 0,0,0
            size_hint: .5, .85
            font_size: 40
            markup: True
            size: self.texture_size
            bold: True

        TextInput:
            id: name
            pos_hint: {'center_x': 0.5, 'center_y': 0.705}
            size_hint: .5, .85
            focus: True
            multiline: False

        Label: 
            text: 'Cantidad a extraer (numero): '
            color: 0,0,0
            size_hint: .5, .85
            font_size: 40
            markup: True
            bold: True

        TextInput:
            id: cantidad
            pos_hint: {'center_x': 0.5, 'center_y': 0.705}
            size_hint: .5, .85 
            focus: True
            multiline: False
        
        Label: 
            text: 'Uso: '
            color: 0,0,0
            size_hint: .5, .85
            font_size: 40
            markup: True
            bold: True

        TextInput:
            id: uso
            pos_hint: {'center_x': 0.5, 'center_y': 0.705}
            size_hint: .5, .85 
            focus: True
            multiline: False
        
        Button:
            id: guardar
            text: 'Guardar'
            on_press: root.Guardar_sheet()
            height: '48dp'
            size_hint: .5, .85
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 40
    
<Contrasena>:    
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 40
        canvas:
            Color: 
                rgb: 1, 1, 1
            Rectangle:
                size: self.size
                pos: self.pos
        Label: 
            text: 'Contraseña: '
            color: 0,0,0
            size_hint: .5, .95
            font_size: 50
            markup: True
            size: self.texture_size
            bold: True

        TextInput:
            id: pas
            pos_hint: {'center_x': 0.5, 'center_y': 0.705}
            size_hint: .5, .95
            focus: True
            multiline: False
            password: True
                    
        Button:
            id: comp
            text: 'Entrar'
            on_press: root.Comp()
            height: '48dp'
            size_hint: .5, .95
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 50
                    
        Button:
            id: vol
            text: 'Volver'
            on_press: root.volver()
            height: '48dp'
            size_hint: .5, .95
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 50
    
<AnadirScreen>:
    GridLayout:
        cols:1
        rows:7
        padding: 10
        apacing: 5
        canvas:
            Color: 
                rgb: 1, 1, 1
            Rectangle:
                size: self.size
                pos: self.pos

        Image: 
            source: 'SIGIT.png'
            size_hint_x: 0.21
            allow_stretch: True

        ToggleButton:
            text: 'Abrir Escaner'
            on_press: root.open_camera()
            height: '48dp'
            size_hint: .5, .95
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 50

        Label: 
            text: 'Cantidad a ingresar: '
            color: 0,0,0
            size_hint: .5, .95
            font_size: 50
            markup: True
            bold: True

        TextInput:
            id: cantidad
            pos_hint: {'center_x': 0.5, 'center_y': 0.705}
            size_hint: .5, .95 
            focus: True
            multiline: False

        Button:
            id: guardar
            text: 'Guardar'
            on_press: root.Guardar_sheet()
            height: '48dp'
            size_hint: .5, .95
            pos_hint: {"center_x": .5, "center_y": .5}
            bold: True
            font_size: 50

<CameraScreen>:
    BoxLayout:
        orientation: 'vertical'    
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
            canvas.before:
                Rotate:
                    angle: -90
                    origin: self.center

<ScreenManager>:

    MainScreen:
    RetirarScreen:
    Contrasena:
    AnadirScreen:
    CameraScreen:
    
'''
)

class MainScreen(Screen):
    def ret(self):
        self.manager.current = 'retirar'
    def an(self):
        self.manager.current = 'contrasena' 

class Contrasena(Screen):
    
    def volver(self):
        self.manager.current = 'main'
    def Comp(self):    
        layout = GridLayout(cols=1, padding=10)
        popup = Popup(title="Guardar",
            content=layout,
            size_hint=(.5, .5))
        if self.ids.pas.text == "9876":
            self.manager.current = 'anadir'
        else:    
            texto = "Contraseña incorrecta"
            popupLabel = Label(text=texto)
            closeButton = Button(text="Cerrar", size_hint=(.3, .3))

            layout.add_widget(popupLabel)
            layout.add_widget(closeButton)

            popup.open()
            closeButton.bind(on_press = popup.dismiss)

class AnadirScreen(Screen):
    qr_model = ''
    def open_camera(self):
        camera_screen = self.manager.get_screen('camera')
        camera_screen.set_state('anadir')  
        self.manager.current = 'camera'

    def set_qr_model(self, qr_code_data):
        self.qr_model = qr_code_data
        error(self.qr_model,'QR ESCANEADO')
        
    def Guardar_sheet(self):
        if self.qr_model == '':
            error("Escanea alguna pieza primero",'Error')
        else:
            try:
                temp = int(self.ids.cantidad.text)
                guardar(self.qr_model, temp, "Ingreso", "Ingreso", 'Ingresar')
                self.qr_model = ' '
            except (ValueError, NameError):
                error("Ingresa Cantidad a Introducir",'Error')

class RetirarScreen(Screen):
    qr_model = ''
    def open_camera(self):
        camera_screen = self.manager.get_screen('camera')
        camera_screen.set_state('retirar')  
        self.manager.current = 'camera'

    def set_qr_model(self, qr_code_data):
        self.qr_model = qr_code_data
        error(self.qr_model,'QR ESCANEADO')
        
    def Guardar_sheet(self):
        Errores = Enum('Errores', ['QR','USO','Nombre','OK'])

        if self.qr_model == '':
            Error = Errores.QR.name
        elif  self.ids.uso.text == '':
            Error = Errores.Nombre.name
        elif self.ids.name.text == '':
            Error = Errores.USO.name
        else:
            Error = Errores.OK.name

        if Error != 'OK':
            error("Error, Introduce {}".format(Error.lower()), 'Error')
        else:
            try:
                guardar(self.qr_model, int(self.ids.cantidad.text), self.ids.name.text, self.ids.uso.text, 'Retirar')
                self.qr_model = ''
            except ValueError:
                error("Introducir cantidad a retirar", 'Error')

class CameraScreen(Screen):
    camera_active = False
    qr_detected = False
    state = ''
    def set_state(self, new_state):
        self.state = new_state

    def on_enter(self):
        self.camera = self.ids.camera
        self.qr_detected = False
        self.camera.play = True
        Clock.schedule_interval(self.decode_qr, 1 / 30)
        self.camera_active = True

    def on_leave(self):
        if self.camera is not None:
            self.camera.play = False
            Clock.unschedule(self.decode_qr)
            self.camera_active = False

    def close_camera(self):
        self.manager.current = self.state

    def decode_qr(self,dt):
        image_data = self.camera.texture.pixels
        width, height = self.camera.resolution
        image = Image.frombytes(mode='RGBA', size=(width, height), data=image_data)
        image_flip = image.transpose(Image.FLIP_LEFT_RIGHT)
        decoded_qr_codes = decode(image_flip)

        if not self.qr_detected and len(decoded_qr_codes) > 0:
            qr_code_data = decoded_qr_codes[0].data.decode('utf-8')
            mainscreen = self.manager.get_screen(self.state)
            mainscreen.set_qr_model(qr_code_data)
            self.qr_detected = True
            self.manager.current = self.state

###############################
##         Funciones         ##
###############################

def buscar_vacia(sheet):
    j = 1
    for i in sheet.col_values(1):
        j += 1
        if sheet.cell(j, 1).value is None:
            return j

def buscar_y_cambiar_retirar(qr_model, qr_value, sheet):
	try:
		cell = sheet.find(qr_model)
		stock = sheet.cell(cell.row, cell.col + 2).value
		resultado = int(stock) - int(qr_value)
		return [cell.row, cell.col + 2, resultado]
		
	except AttributeError:
		return 0

def stock(qr_model, sheet):
    for i in sheet.col_values(2):
        if i == qr_model:
            Model = sheet.find(qr_model)
            stock_col = Model.col + 2
            if int(sheet.cell(Model.row, stock_col).value) < int(sheet.cell(Model.row, 6).value):
                comprar = int(sheet.cell(Model.row, 6).value) - int(sheet.cell(Model.row, stock_col).value)  
                message = "El stock de {} esta por debajo del minimo, compra minimo {}".format(sheet.cell(Model.row, Model.col-1).value, comprar)
                error("Material Bajo Minimos \n avisar al responsable", 'Aviso!')
                msg.attach(MIMEText(message, 'plain'))
                server.sendmail(msg["From"], msg["To"],msg.as_string())
                server.quit()
                return 0
                
def guardar(qr_model, cantidad, name,uso, state):
	layout = GridLayout(cols=1, padding=10)
	popup = Popup(title="Guardar",
		    content=layout,
		    size_hint=(.8, .8))
		    
	try:
		cell = sheet1.find(qr_model)
		cell_value = sheet1.cell(cell.row, cell.col-1).value

		texto = "Vas a {} {} de {} \n ¿estás seguro?".format(state, cantidad, cell_value)
		
	except (TypeError, AttributeError):
		texto = "Vas a {} {} de {} \n \t ¿estás seguro?".format(state, cantidad, '\n Un material que no esta inventariado')
	except (ValueError):
		error("Error 100, Avisa al responsable", "Error")
	
	popupLabel = Label(text=texto)
	yesbutton = Button(text="Si", size_hint=(.3, .3))
	closeButton = Button(text="No", size_hint=(.3, .3))

	layout.add_widget(popupLabel)
	layout.add_widget(yesbutton)
	layout.add_widget(closeButton)

	popup.open()
	closeButton.bind(on_press=popup.dismiss)
	
	if state == 'Ingresar':
		terminal = 1
	else:
		terminal = 0
		
	yesbutton.bind(on_press=lambda x:datos(qr_model,int(cantidad),name,uso,terminal))
	yesbutton.bind(on_press=popup.dismiss)

def datos(qr_model,cantidad,name,uso, state):
    try:
        Time = ''
        Time = ctime()
        a = buscar_vacia(sheet3)
        sheet3.update_cell(a, 2, name)
        sheet3.update_cell(a, 3, qr_model)

        if state == 1:
            sheet3.update_cell(a, 4, int(cantidad))
            b = buscar_y_cambiar_retirar(qr_model, -1*int(cantidad), sheet1)
        else:
            sheet3.update_cell(a,4, -1*int(cantidad))
            b = buscar_y_cambiar_retirar(qr_model, int(cantidad), sheet1)

        sheet3.update_cell(a, 1, Time)
        sheet3.update_cell(a, 5, uso)
        
        if b == 0:
            error("No esta en el inventario \n avisa al responsable", 'Error')
        else:
            sheet1.update_cell(b[0], b[1], b[2])

        stock(qr_model, sheet1)
        error("Hecho", '')
        
    except (TypeError, AttributeError):
        error("Error 102, Avisa al responsable", 'Error')
    except (ValueError, NameError):
        error("Error 103, Avisa al responsable", 'Error')

def error(text, tittle):
    layout = GridLayout(cols=1, padding=10)
    popup = Popup(title=tittle,
                 content=layout,
                 size_hint=(.5, .5))

    popupLabel = Label(text=text)
    closeButton = Button(text="Cerrar", size_hint=(.3, .3))

    layout.add_widget(popupLabel)
    layout.add_widget(closeButton)
    
    closeButton.bind(on_oress = popup.dismiss)
    popup.open()

    closeButton.bind(on_press=popup.dismiss)

#######################################################
###                                                  ##
#######################################################

class splashscreen(Screen):
	pass

class mainApp(App):
	title = "Escanner QR"
	sm = ScreenManager()

	def build(self):
		self.sm.add_widget(splashscreen(name = 'splash'))
		self.sm.add_widget(MainScreen(name='main'))
		self.sm.add_widget(RetirarScreen(name='retirar'))
		self.sm.add_widget(AnadirScreen(name = 'anadir'))
		self.sm.add_widget(Contrasena(name='contrasena'))
		self.sm.add_widget(CameraScreen(name='camera'))

		self.show_splash()

		return self.sm
		
	def show_splash(self):
		self.sm.current = 'splash'
		Clock.schedule_once(self.change,1)
	
	def change(self,instance):
		self.sm.current = 'main'

if __name__ == '__main__':
    mainApp().run()
    

