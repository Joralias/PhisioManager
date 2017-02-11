import pymysql.cursors


def connect( db_name, user, password,host = 'localhost'):
    # Connect to the database
    connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    return connection


def disconnect(connection):
    connection.close()


def insertPatient(connection, name,magneto_time=0, corriente_time=0, manual_time=0, bici_time=0, ejercicios_time=0, calor_time=0):
    
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `pacientes` (`name`, `magneto`,`corrientes`,`manual`,`bici`,`autoejercicios`,`calor`) VALUES (%s, %s,%s,%s, %s,%s,%s)"
            cursor.execute(sql, (name,magneto_time, corriente_time, manual_time, bici_time, ejercicios_time, calor_time))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

    except:
        print ("DB Failure")


def readPatient(connection, name):
    
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `pacientes` WHERE `name`=%s"
            cursor.execute(sql, name)
            result = cursor.fetchone()
        return result
    except:
        print ("DB Failure")
