import kivy 
import gspread
import cv2 
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
from kivy.graphics.texture import Texture 
from kivy.clock import Clock

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("qrscanner-390410-60be511e0f54.json", scope)
client = gspread.authorize(creds)
s = client.open('Almacen')
found = set()
outputtext=''

class Box01(GridLayout):
    
    def __init__(self):
        super(Box01,self).__init__()
        
        self.cam = cv2.VideoCapture(0)
        self.cam.set(3, 1280)
        self.cam.set(4, 720)
        self.img = Image()
        self.qr_model = ''
        self.pop= Popup(title = "Escaneando",content=self.img)

        self.cols = 1
        self.row = 3
        
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
            on_press=self.open_Camera
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
    
    def open_Camera(self, *args):
        self.pop.open()
        Clock.schedule_interval(self.dec,1/30)

    def dec(self,qr_model):

            togglfag = True
            if togglfag == True :
                ret, frame = self.cam.read()
                togglfag = False

            if ret:
                buf1 = cv2.flip(frame,0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf,colorfmt='bgr',bufferfmt='ubyte')
                self.img.texture = image_texture

                QR_decode = decode(frame)
                togglfag = True

                for code in QR_decode:
                    (x,y,w,h) = code.rect
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255),2)

                    self.qr_model = code.data.decode('utf-8')
                    qr_type = code.type
                    self.text = "{} ({})".format(qr_model,qr_type)
                    
                    if self.qr_model not in found:
                        found.add(self.qr_model)
                        if self.qr_model == ' ':
                            self.pop.dismiss()
                            togglfag = True
                            self.Aviso_pop("Escaneo incorrecto")
                            self.qr_model = ' '
                        else:
                            self.Aviso_pop(self.qr_model)
                            self.pop.dismiss()
                            self.cam.release()
                            self.qr_model = ' '
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    exit(0)

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

    def Guardar_sheet(self,instance):   
             
        layout = GridLayout(cols = 1, padding = 10)
        popup = Popup(title = "Guardar",
                      content = layout, 
                      size_hint = (.5,.5))  

        popupLabel = Label(text = "Vas a retirar "+ self.Cantidad.text +" de " + self.qr_model+" estas seguro?")
        yesbutton = Button(text = "Si",size_hint = (.3,.3))
        closeButton = Button(text = "No",size_hint = (.3,.3))
        
        layout.add_widget(popupLabel)
        layout.add_widget(yesbutton)
        layout.add_widget(closeButton)   

        popup.open()   

        yesbutton.bind(on_press = popup.dismiss)
        popup.bind(on_dismiss = self.datos)

        closeButton.bind(on_press = popup.dismiss)

    def datos(self,instance):
        
        sheet3 = s.worksheet("Hoja 2")
        sheet1 = s.worksheet("Hoja 1")

        if self.name.text == '':
            self.Error("Introducir nombre")
        else:
            try:
                print("datos")
                a = self.buscar_vacia(sheet3)
                b = self.buscar_y_cambiar(self.qr_model, int(self.Cantidad.text),sheet1)
                sheet3.update_cell(a,1,self.name.text)
                sheet3.update_cell(a,2,self.qr_model)
                sheet3.update_cell(a,3, int(self.Cantidad.text)) 

                sheet1.update_cell(b[0],b[1],b[2])

                self.Aviso_pop("Hecho")

                if self.aviso(self.qr_model, sheet1) == 0 :
                    self.Error("No queda Stock")

            except ValueError or NameError:
                self.Error("introducir cantidad a retirar")
            except TypeError:
                self.Error("No inventariado")
      
    def Aviso_pop(self, text):
        layout = GridLayout(cols = 1, padding = 10)
        popup = Popup(title = "Aviso!",
                        content = layout,
                      size_hint = (.5,.5))  

        popupLabel = Label(text = text)
        closeButton = Button(text = "cerrar",size_hint = (.3,.3))
    
        layout.add_widget(popupLabel)

        layout.add_widget(closeButton)   
    
        popup.open()   

        closeButton.bind(on_press = popup.dismiss)
   
    def Error(self, text):
        layout = GridLayout(cols = 1, padding = 10)  
        popup = Popup(title = "Error",
                      content = layout,
                      size_hint=(.5,.5))  
  
        popupLabel = Label(text = text)
        closeButton = Button(text = "Cerrar", size_hint = (.3,.3))
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)     
        popup.open()   
  
        closeButton.bind( on_press = popup.dismiss )


class mainApp(App):
    title = "Escanner QR"
    def build(self):
        return Box01()

if __name__ == '__main__':
    mainApp().run()

