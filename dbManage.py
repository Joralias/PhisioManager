import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect():
    # Connect to the database
    connection = sqlite3.connect('clinic.sqlite')
    connection.row_factory = dict_factory
    print("conected to db")
    #createTables if not exists
    cursor=connection.cursor()
    sql = "CREATE TABLE IF NOT EXISTS pacientes(id INTEGER PRIMARY KEY,  name VARCHAR(50) NOT NULL, magneto TINYINT(3) NULL DEFAULT NULL, corrientes TINYINT(3) NULL DEFAULT NULL,  calor TINYINT(3) NULL DEFAULT NULL, manual TINYINT(3) NULL DEFAULT NULL, bici TINYINT(3) NULL DEFAULT NULL, autoejercicios TINYINT(3) NULL DEFAULT NULL)"
    cursor.execute(sql)
    sql ="CREATE TABLE IF NOT EXISTS recursos (nombre VARCHAR(50) NOT NULL PRIMARY KEY , cantidad INT(11) NOT NULL)"
    cursor.execute(sql)
    
    #at the moment the recursos table is populated hardcoded, future should be another screen.
    #cursor.execute("INSERT INTO recursos VALUES ('bici',1)")
    #cursor.execute("INSERT INTO recursos VALUES ('calor',2)")
    #cursor.execute("INSERT INTO recursos VALUES ('magneto',1)")
    #cursor.execute("INSERT INTO recursos VALUES ('manual',1)")
    #cursor.execute("INSERT INTO recursos VALUES ('corrientes',2)")
    #connection.commit()
    #######################

    return connection


def disconnect(connection):
    connection.close()


def insertPatient(connection, name,magneto_time=0, corriente_time=0, manual_time=0, bici_time=0, ejercicios_time=0, calor_time=0):
    
    try:
        cursor=connection.cursor()
        # Create a new record
        cursor.execute("""INSERT INTO pacientes(name, magneto, corrientes,manual,bici,autoejercicios,calor) VALUES(?,?,?,?,?,?,?)""" , ( name, str(magneto_time), str(corriente_time),str(manual_time), str(bici_time), str(ejercicios_time),str(calor_time)))

        connection.commit()


    except:
        print ("DB Failure")


def readPatient(connection, name):
    
    try:
        cursor=connection.cursor()
        # Read a single record
        
        nameSQL = (name,)
        cursor.execute("SELECT * FROM pacientes WHERE name = '%s'" % nameSQL)
        result = cursor.fetchone()
        
        print("READ PATIENT RESULT")
        
        print(result)
        return result
    except:
        print ("DB Failure")



def readResources(connection):
    
    try:
        c=connection.cursor()
        sql = "SELECT * FROM `recursos`"
        c.execute(sql)
        result = c.fetchall()
        return result
    except:
        print ("DB Failure")




def insertResources(connection, name, quantity):
    
    #try:
        cursor=connection.cursor()
        # update a record new record

        cursor.execute("""INSERT OR REPLACE INTO recursos(nombre,cantidad) VALUES(?,?)""", (name,str(quantity)))
        
        connection.commit()



    #except:
    #    print ("DB Failure")