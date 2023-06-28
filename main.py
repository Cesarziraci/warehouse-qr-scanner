import kivy 
import gspread
import cv2 
import time
from pyzbar.pyzbar import decode 
from oauth2client.service_account import ServiceAccountCredentials
kivy.require('2.2.0')
from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("qrscanner-390410-60be511e0f54.json", scope)
client = gspread.authorize(creds)
s = client.open('Almacen')

class Box01(GridLayout):
    
    def __init__(self):
        super(Box01,self).__init__()
        self.cam = cv2.VideoCapture(0)
        self.cam.set(5, 640)
        self.cam.set(6, 480)
        self.sheet3 = s.worksheet("Hoja 2")
        self.sheet1 = s.worksheet("Hoja 1")

        self.cols = 1
        self.row = 3
        self.size_hint = (0.6, 0.7)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.qr_model = ''
        
        self.name = TextInput(
            multiline = False,
            padding_y= (20,20)
            )
        self.Cantidad = TextInput(
            multiline = False,
            padding_y= (20,20)
            )

        self.Camera = Button(
            text="Abrir Escaner", 
            font_size=20,
            size_hint = (1,0.7),
            bold = True
            )
        
        self.Submit = Button(
            text="Guardar", 
            font_size=20
            )
        
        self.add_widget(
            Image(
            source='SIGIT.jpg'
            )
        )

        self.add_widget(self.Camera)

        self.Camera.bind(
            on_press=self.Open_Camera
            )
        self.Camera.disabled

        self.add_widget(Label(
            text="Nombre de operario: ", 
            color= (0,0,0), 
            font_size= 20,

            )
        )
        
        self.add_widget(self.name)
        
        self.add_widget(Label(
            text="Cantidad a extraer: ", 
            color= (0,0,0), 
            font_size= 25
            )
        )
        
        self.add_widget(self.Cantidad)

        self.add_widget(self.Submit)
        self.Submit.bind(on_press=self.Guardar_sheet)

    def dec(self,qr_model):
        while True:
            suceess, frame= self.cam.read()
            for i in decode(frame):
                qr_model = i.data.decode('utf-8')
                time.sleep(6)

                cv2.waitKey(100)
                cv2.destroyAllWindows
            
            break
        cv2.waitKey(100)
        cv2.destroyAllWindows()
        return qr_model

    def buscar_vacia(self,sheet):
        j = 1
        for i in sheet.col_values(1):
            j = j+1
            if sheet.cell(j,1).value == None: 
                return j

    def buscar_y_cambiar(self,qr_model,qr_value,sheet):
        for i in sheet.col_values(1):
            if i == qr_model:
                cell = sheet.find(qr_model)
                stock = sheet.cell(cell.row,cell.col+2).value
                resultado = int(stock) - qr_value
                return [cell.row,cell.col+2,resultado]

    def aviso(self,qr_model,sheet):
        for i in sheet.col_values(1): 
            if i == qr_model: 
                Model = sheet.find(qr_model)
                col = Model.col
                if (col + 1) > (col + 2): 
                    return 0
                else:
                    return 1

    def Open_Camera(self,Instance):
            self.qr_model=self.dec('')
            if self.qr_model == '':
                self.Aviso("Escaneo incorrecto")
            else:
                self.Aviso(self.qr_model)

    def Guardar_sheet(self,instance):   
             
        layout = GridLayout(cols = 1, padding = 10)
        popup = Popup(title = "Aviso!",
                      content = layout)  

        popupLabel = Label(text = "Vas a retirar "+ self.Cantidad.text +" de " + self.qr_model+" estas seguro?")
        yesbutton = Button(text = "Si")
        closeButton = Button(text = "No")
        
        layout.add_widget(popupLabel)
        layout.add_widget(yesbutton)
        layout.add_widget(closeButton)   

        popup.open()   

        yesbutton.bind(on_press = popup.dismiss)
        popup.bind(on_dismiss = self.datos)

        closeButton.bind(on_press = popup.dismiss)

    def datos(self,instance):
        if self.name.text == '':
            self.Error("Introducir nombre")
        else:
            try:
                print("datos")
                a = self.buscar_vacia(self.sheet3)
                b = self.buscar_y_cambiar(self.qr_model, int(self.Cantidad.text),self.sheet1)
                self.sheet3.update_cell(a,1,self.name.text)
                self.sheet3.update_cell(a,2,self.qr_model)
                self.sheet3.update_cell(a,3, int(self.Cantidad.text)) 

                self.sheet1.update_cell(b[0],b[1],b[2])

                self.Aviso("Hecho")

                if self.aviso(self.qr_model, self.sheet1) == 0 :
                    self.Error("No queda Stock")

            except ValueError or NameError:
                self.Error("introducir cantidad a retirar")
            except TypeError:
                self.Error("No hay en inventario")
      
    def Aviso(self, text):
        layout = GridLayout(cols = 1, padding = 10)

        popupLabel = Label(text = text)
        closeButton = Button(text = "cerrar")
  
        layout.add_widget(popupLabel)

        layout.add_widget(closeButton)   
  
        popup = Popup(title = "Aviso!",
                      content = layout)  
        popup.open()   

        closeButton.bind(on_press = popup.dismiss)
   
    def Error(self, text):
        layout = GridLayout(cols = 1, padding = 10)
  
        popupLabel = Label(text = text)
        closeButton = Button(text = "Cerrar")
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title = "Error",
                      content = layout)  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind( on_press = popup.dismiss )


class mainApp(App):
    title = "Escanner QR"
    def build(self):
        return Box01()

if __name__ == '__main__':
    mainApp().run()

