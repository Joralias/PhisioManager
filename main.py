#-*-coding:utf8;-*-
#qpy:2
#qpy:kivy

from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.lang import Builder 
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

from libFisio import myThread,checkNewPatientInDB, registerPatientToDB, getNumberOfPatients, resourceInit
import threading

from functools import partial




class RegisterGrid(GridLayout):


    def registerPatient(self, instance):
        
        checkbox_status = [self.cbmag.active,self.cbcor.active,self.cbcal.active,self.cbbic.active,self.cbman.active,self.cbeje.active]
        if self.patient.text!= "":

            registerPatientToDB(self.patient.text,checkbox_status)
            print("termine de registrar")
            thread = myThread(self.patient.text)
            thread.start()    
            print(threading.enumerate())
            sm.current = 'main'
            sm.current_screen.grid.addPatientStatus()
            sm.current_screen.grid.updateGrid()

        else:
            popup = Popup(title='Campo vacío', content=Label(text='Introduce un nombre para el paciente'),size_hint=(None, None), size=(400, 400))
            popup.open()            


    def backToMainScreen(self,*args):
        sm.current = 'main'

    def __init__(self, **kwargs):
        super(RegisterGrid, self).__init__(**kwargs)
        self.cols = 2
        self.row = 6
        self.add_widget(Label(text='Paciente'))
        self.patient = TextInput(multiline=False)
        self.add_widget(self.patient)
        self.add_widget(Label(text='Magneto'))
        self.cbmag = CheckBox()
        self.add_widget(self.cbmag)
        self.add_widget(Label(text='Corrientes'))
        self.cbcor = CheckBox()
        self.add_widget(self.cbcor)
        self.add_widget(Label(text='Calor'))
        self.cbcal = CheckBox()
        self.add_widget(self.cbcal)
        self.add_widget(Label(text='Bici'))
        self.cbbic = CheckBox()
        self.add_widget(self.cbbic)
        self.add_widget(Label(text='Manual'))
        self.cbman = CheckBox()
        self.add_widget(self.cbman)
        self.add_widget(Label(text='Ejercicios'))
        self.cbeje = CheckBox()
        self.add_widget(self.cbeje)

        self.Back = Button(text="Atrás")
        self.Back.bind(on_press=self.backToMainScreen)
        self.add_widget(self.Back)

        self.Registrar = Button(text="Registrar")
        self.Registrar.bind(on_press=self.registerPatient)
        self.add_widget(self.Registrar)




class pop(Widget):


    def sayYesToRegister(self,*args):

        self.main_pop.dismiss()
        sm.current = 'register'

    def show_it(self):
        self.box=FloatLayout()
        
        self.lab=(Label(text="Paciente no encontrado, ¿introducir en base de datos? ",font_size=15,
            size_hint=(None,None),pos_hint={'x':.35,'y':.6}))
        self.box.add_widget(self.lab)
        
        self.butNo=(Button(text="No",size_hint=(None,None),
            width=200,height=50,pos_hint={'x':.5,'y':0}))
        self.box.add_widget(self.butNo)

        self.butYes=(Button(text="Si",size_hint=(None,None),
            width=200,height=50,pos_hint={'x':0,'y':0}))
        self.box.add_widget(self.butYes)        
       
        self.main_pop = Popup(title="Paciente no encontrado",content=self.box,
            size_hint=(None,None),size=(450,300),auto_dismiss=False,title_size=15)
            

        self.butYes.bind(on_press=self.sayYesToRegister)
        self.butNo.bind(on_press=self.main_pop.dismiss)
        
        self.main_pop.open()




class MainGrid(GridLayout):


    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.cols = 2
        self.row = 2
        self.add_widget(Label(text='Paciente'))
        self.patient = TextInput(multiline=False)
        self.add_widget(self.patient)
        self.start = Button(text="START")
        self.start.bind(on_press=self.startPatient)
        self.add_widget(self.start)

        #last square, hen progress is set
        self.progress_status = GridLayout(padding=[0,0,30,0])
        self.progress_status.rows = 0
        self.progress_status.cols = 3
        self.progress_status.patients = []
        self.progress_status.pb = []
        self.progress_status.treatements = []
        self.add_widget(self.progress_status)

        #inicializacion de los recursos
        resourceInit()


    def startPatient(self, instance):
        #chek if there is something written
        if self.patient.text!="":
            
            if checkNewPatientInDB(self.patient.text):    
                popup = pop()
                popup.show_it()

            else:
                patient_initiating = False
                for t in threading.enumerate():
                    if self.patient.text == t.name:
                        patient_initiating = True

                if not patient_initiating:
                    thread = myThread(self.patient.text)
                    thread.start()
                    self.addPatientStatus()

                else:
                    popup = Popup(title='Paciente ya iniciado', content=Label(text='El paciente introducido ya esta en tratamiento'),size_hint=(None, None), size=(400, 400))
                    popup.open()                          
                    
        self.patient.text =""            

    def addPatientStatus(self):
        self.progress_status.rows +=1
        self.progress_status.pb.append(ProgressBar(max=100))
        self.progress_status.treatements.append(Label(text='Iniciando Tratamiento'))  
        self.progress_status.patients.append(Label(text=self.patient.text))     
        self.progress_status.add_widget(self.progress_status.patients[-1])
        self.progress_status.add_widget(self.progress_status.treatements[-1])
        self.progress_status.add_widget(self.progress_status.pb[-1])

    def deletePatientStatus(self, index):

        print ("BORRO PATIENT")
        popup = Popup(title='Paciente Listo', content=Label(text='El paciente ' +self.progress_status.patients[index].text +' ha concluido su sesion de hoy'),size_hint=(None, None), size=(400, 400))
        popup.open()                  
        self.progress_status.remove_widget(self.progress_status.patients[index])
        self.progress_status.remove_widget(self.progress_status.treatements[index])
        self.progress_status.remove_widget(self.progress_status.pb[index])

        self.progress_status.patients.pop(index)
        self.progress_status.treatements.pop(index)
        self.progress_status.pb.pop(index)


    def updateGrid(self):

        if len(threading.enumerate())==1 and len(self.progress_status.patients)>0: # just mainthread but some patients still in array
            self.deletePatientStatus(0)

        for t in [x for x in threading.enumerate() if x.name !=  'MainThread']: #excluding mainTread       
            index = 0
            for patient in self.progress_status.patients: 
                if not any(x.name == patient.text for x in threading.enumerate()): #if there is no thread for this patient.
                    self.deletePatientStatus(index)
                    continue

                if t.name == patient.text:
                    data = t.getThreadData()
                    self.progress_status.treatements[index].text = data[0] #treatement
                    self.progress_status.pb[index].value = data[1] #pb %

                index +=1

            

        


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.grid = MainGrid()
        self.add_widget(self.grid)


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.add_widget(RegisterGrid())


sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(RegisterScreen(name='register'))


class MyApp(App):
    def build(self):
        def update(self):
            
            if sm.current_screen.name == 'main':
                sm.current_screen.grid.updateGrid()
            

        Clock.schedule_interval(update, 0.5)
        return sm

if __name__ == '__main__':
    
    MyApp().run()

