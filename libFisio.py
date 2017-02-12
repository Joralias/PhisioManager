import dbManage
import ctypes  # An included library with Python install.
import time
import threading


patients = []
resources=[]


def resourceInit():
    connection = dbManage.connect("fisioproject", "root", "1234")

    resourcesDB = dbManage.readResources(connection)

    dbManage.disconnect(connection)
    for resource in resourcesDB:
        for i in range(resource['cantidad']):
            resources.append(Resource(resource['nombre']+str(i), resource['nombre']))





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

    selected_treatement = patient.future_treatements[0]

    patient.performTreatement(selected_treatement)


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



class Resource():
    def __init__(self, resource_id, type_treatement):
        self.type_treatement = type_treatement
        self.resource_id = resource_id
        self.available = True

    def holdResource(self):
        print("Holding: "+self.resource_id)
        self.available = False

    def releaseResource(self):
        self.available = True



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

        #create the future_treatements array
        if self.magneto_time > 0: self.future_treatements.append(Treatement('MAGNETO',15))
        if self.calor_time > 0: self.future_treatements.append(Treatement('CALOR',10))
        if self.corrientes_time > 0: self.future_treatements.append(Treatement('CORRIENTES', 10))
        if self.manual_time > 0: self.future_treatements.append(Treatement('MANUAL',15))
        if self.ejercicios_time > 0: self.future_treatements.append(Treatement('EJERCICIOS',15))
        if self.bici_time > 0: self.future_treatements.append(Treatement('BICI',15))
        self.waiting_treatement = Treatement('ESPERAR',0)

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

        self.actual_treatement = treatement #first assing and the modify in the for loop
        for resource in resources:
            if resource.type_treatement.upper() == treatement.name.upper():
                print (resource.resource_id)
                print (resource.available)                
                if resource.available == True:
                    self.actual_treatement = treatement
                    resource.holdResource()
                    #at soon as one of the resources type is available, stop searching
                    break
                else:
                    self.actual_treatement = self.waiting_treatement

        print(self.name+ ": Tratamiento empezado: " +self.actual_treatement.name)
       

        threading.current_thread().treatement = self.actual_treatement.name


        while self.actual_treatement == self.waiting_treatement: #wait if there is no availability
            threading.current_thread().progress = 50
            for resource in resources:
                if resource.type_treatement.upper() == treatement.name.upper():
                    if resource.available == True:
                        self.actual_treatement = treatement
                        print(self.name+ ": Tratamiento empezado (despues de esperar): " +self.actual_treatement.name)
                        threading.current_thread().treatement = self.actual_treatement.name 
                        resource.holdResource()            
                    time.sleep(1)

        start_treatement_time = time.time()
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


        for resource in resources:
            if resource.type_treatement.upper() == finished_treatement.name.upper():
                resource.releaseResource()

        for t in self.future_treatements:
            print (t.name)

        self.future_treatements.remove(finished_treatement)
        self.finished_treatements.append(finished_treatement)

        if len(self.future_treatements)>0:
            print (self.name+ ": Tiempo de cambio de tratamiento....")
            threading.current_thread().treatement = "Cambiando"+ "\n"+ "Tratamiento"
            time.sleep(3)     
            self.performTreatement(self.future_treatements[0])
 
        else:
            print (self.name + " ha terminado su sesion de hoy")
            



