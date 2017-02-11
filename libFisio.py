import dbManage
import ctypes  # An included library with Python install.
import time
import threading
from enum import Enum

#class Treatement(Enum):
#    UNASIGNED = 0
#    MAGNETO = 1
#    CORRIENTES = 2
#    MANUAL = 3
#    BICI = 4
#    EJERCICIOS = 5
#    CALOR = 6


patients = []





def getNumberOfPatients():
    print (len(threading.enumerate()) - 1)
    return (len(threading.enumerate()) - 1) #less mainThread


def registerPatientToDB(name,values):
    
    connection = dbManage.connect("fisioproject", "root", "1234")
    #ctypes.windll.user32.MessageBoxW(0, "Introduce 'Y' en los tratamientos que apliquen", "Mensaje", 1)    
    
    magneto_time = 15 if values[0] ==True else 0
    corrientes_time = 10 if values[1] ==True else 0
    calor_time = 10 if values[2] ==True else 0
    bici_time = 15 if values[3] ==True else 0
    manual_time = 15 if values[4] ==True else 0
    ejercicios_time = 15 if values[5] ==True else 0

    dbManage.insertPatient(connection,name,magneto_time, corrientes_time, manual_time, bici_time, ejercicios_time, calor_time)

    dbManage.disconnect(connection)



def checkNewPatientInDB(patient):
    connection = dbManage.connect("fisioproject", "root", "1234")
    patient_data = dbManage.readPatient(connection,patient)
    if patient_data==None:
        #new patient
        return True
    else:
        #already have it
        return False


def arrivePatient(name):

    patient = Patient(name)
    patients.append(patient)
   
    #simulacion (funcion futura)
    #selectTreatement (otra funcion futura)
    #ejecuta el treatment

    patient.performTreatement(patient.future_treatements[0])


class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.treatement = ""
        self.progress = 0


    def getThreadData(self):
        return self.treatement, self.progress

    def run(self):
        print ("Starting " + self.name)
        arrivePatient(self.name)
        print (self.name + " se marcho ")



class Treatement():
    def __init__(self, name, time):
        self.name = name
        self.time = time


class Patient():
    def __init__(self, name):
        self.name = name
        
        self.start_time = 0
        self.end_time = 0
        self.time_spent = self.start_time - self.end_time

        self.readPatient()
          
        self.optimal_time = self.magneto_time + self.corrientes_time + self.manual_time + self.bici_time + self.ejercicios_time + self.calor_time
        self.actual_treatement = 0
        self.finished_treatements = []
        self.future_treatements = []

        if self.magneto_time > 0: self.future_treatements.append(Treatement('MAGNETO',15))
        if self.calor_time > 0: self.future_treatements.append(Treatement('CALOR',10))
        if self.corrientes_time > 0: self.future_treatements.append(Treatement('CORRIENTES', 10))
        if self.manual_time > 0: self.future_treatements.append(Treatement('MANUAL',15))
        if self.ejercicios_time > 0: self.future_treatements.append(Treatement('EJERCICIOS',15))
        if self.bici_time > 0: self.future_treatements.append(Treatement('BICI',15))



    def readPatient(self):
        
        connection = dbManage.connect("fisioproject", "root", "1234")

        patient_data = dbManage.readPatient(connection,self.name)
        self.magneto_time = patient_data['magneto']
        self.calor_time =  patient_data['calor']
        self.corrientes_time =  patient_data['corrientes']
        self.bici_time =  patient_data['bici']
        self.manual_time = patient_data['manual']
        self.ejercicios_time = patient_data['autoejercicios']

        dbManage.disconnect(connection)



    def performTreatement(self,treatement):

        self.actual_treatement = treatement

        print(self.name+ ": Tratamiento empezado: " +self.actual_treatement.name)
        start_treatement_time = time.time()

        threading.current_thread().treatement = self.actual_treatement.name

        elapsed_time = 0
        while self.actual_treatement.time - elapsed_time > 0:
            elapsed_time = (time.time()-start_treatement_time)
            threading.current_thread().progress = (elapsed_time/self.actual_treatement.time)*100
            time.sleep(1)

            #print ("%s: %s" % ( patient.name, time.ctime(time.time()) ))

        self.actual_treatement.time = 0
        print (self.name + " ha terminado "+ self.actual_treatement.name)

        self.endTreatement(self.actual_treatement)




    def endTreatement(self, finished_treatement):

        self.future_treatements.remove(finished_treatement)
        self.finished_treatements.append(finished_treatement)


        if len(self.future_treatements)>0:
            print (self.name+ ": Tiempo de cambio de tratamiento....")
            time.sleep(3)
            self.performTreatement(self.future_treatements[0])
 
        else:
            print (self.name + " ha terminado su sesion de hoy")
            



