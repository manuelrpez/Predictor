#todo lo que tiene que ver con bases de datos, descargas y cargas
import requests
import json
import urllib
import pandas as pd
import os
import sqlite3 as sql
import Errores
import datetime
from urllib import request

#descargar los datos de ESIOS
#"Authorization":"Token token="+str(token),
def down_ESIOS(token, id, fecha_inicio, fecha_fin): #ya está lista

    headers = {"x-api-key": str(token),
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
               }

    pagina = f"https://api.esios.ree.es/indicators/{id}?start_date={fecha_inicio}T00%3A00%3A00&end_date={fecha_fin}T23%3A55%3A00"
    req = urllib.request.Request(pagina, headers=headers)
    response = urllib.request.urlopen(req)

    json_data = response.read().decode('utf-8')
    result = json.loads(json_data)
    return result
#descargar los datos de ESIOS
def down_OMIE_curves(date,ruta): #ya esta lista

    file_name = f"curva_pbc_{date}.1"

    url=f"https://www.omie.es/en/file-download?parents%5B0%5D=curva_pbc&filename=curva_pbc_{date}.1"

    request.urlretrieve(url, ruta+"\\"+file_name)

def down_OMIE_portugal(date,ruta):

    file_name = f"pdbc_tot_{date}.1"

    url=f"https://www.omie.es/en/file-download?parents%5B0%5D=pdbc_tot&filename=pdbc_tot_{date}.1"

    request.urlretrieve(url, ruta+"\\"+file_name)

def down_OMIE_price(date,ruta):
    file_name = f"marginalpdbc_{date}.1"

    url=f"https://www.omie.es/en/file-download?parents%5B0%5D=marginalpdbc&filename=marginalpdbc_{date}.1"


    request.urlretrieve(url, ruta+"\\"+file_name)

#modificar los datos descargados para adaptar el formato
def convertESIOS2df(result,ID,name): #está lista

    #compruebo que ID y nombre están bien y reviso los intervalos de tiempo para hacerlo horario
    posibles_tiempos = ["Cinco minutos", "Hora", "Quince minutos"]
    result["indicator"]["name"]=result["indicator"]["name"].replace(" ", "_")
    result["indicator"]["name"] = result["indicator"]["name"].replace(".", "")
    result["indicator"]["name"]=result["indicator"]["name"].replace("+","")
    if result["indicator"]["id"]!=ID:Errores.error(0)
    if result["indicator"]["name"]!=name:Errores.error(1,result["indicator"]["name"],name)
    if result["indicator"]["tiempo"][0]["name"] not in posibles_tiempos:Errores.error(2)


    df = pd.DataFrame(result["indicator"]["values"])#cojo solo los valores
    df=df[["datetime","value"]]#me quedo con las fechas y el dato
    #convierto la columna de fechas que es un str a un datetime
    df["datetime"]=df["datetime"].str.slice(stop=19) #quito algunos digitos para que me detecte el formato
    df["datetime"] = pd.to_datetime(df["datetime"]) #convierto a fecha
    df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H") #convierto formato fecha a str para eliminar minutos
    df["datetime"] = pd.to_datetime(df["datetime"]) #Lo paso de nuevo a  datetime para poder manejarlo como tal
    df = df.groupby("datetime",as_index=False)["value"].mean() #hago la media segun horas
    df.columns=["datetime",name]

    #if len(df)!=((df.iloc[-1][0]-df.iloc[0][0])+pd.Timedelta(hours=1))/pd.Timedelta(hours=1):
    # En caso de que fues emuy lento habría que utilizar este if pero fallaría si en descargas de medidas para el ultimo dia

    #miro que días tiene menos de 24 datos
    df["days"] = df["datetime"].dt.strftime("%Y-%m-%d")  # no extraigo solo el día porque necesito mes y año
    df["days"] = pd.to_datetime(df["days"])  # lo paso a formato fecha
    n_dias = df.groupby("days",as_index=False)[name].count() #agrupo datos por días
    n_dias = n_dias[n_dias[name] != 24] #selecciono los días que no tengan 24 datos (quizá debería cambiarse por un <24)
    def añadir_ceros():
        hoy = datetime.date.today()
        for i in range(len(n_dias)):

            n_horas = df[df["days"] == n_dias.iloc[i][0]]
            for x in range(24):

                hora = n_dias.iloc[i][0] + datetime.timedelta(hours=x)

                if hora not in n_horas.datetime.values:

                    df.loc[max(df.index) + 1] = [hora, 0, n_dias.iloc[i][0]]

    añadir_ceros()
    df=df.sort_values("datetime")
    return df[df.columns[:2]]

def convertOMIE2df(archivo,ruta):

    test_file = "support_file"  # para no alterar los descarados

    open_file = open(ruta + "\\" + archivo, "r")
    open_test_file = open(ruta + "\\" + test_file, "w")

    datos = open_file.readlines()
    open_file.close()
    open_test_file.writelines(datos[2:])
    open_test_file.close()

    datos = pd.read_csv(ruta + "\\" + test_file, delimiter=";", encoding='ISO-8859-1')
    datos = datos.iloc[:, [0,1, 2, 4, 5, 6, 7]]
    datos["Precio Compra/Venta"]=datos["Precio Compra/Venta"].str.replace(".","")
    datos["Precio Compra/Venta"]=datos["Precio Compra/Venta"].str.replace(",",".")
    datos["Energía Compra/Venta"]=datos["Energía Compra/Venta"].str.replace(".","")
    datos["Energía Compra/Venta"]=datos["Energía Compra/Venta"].str.replace(",",".")

    datos["Precio Compra/Venta"]=pd.to_numeric(datos["Precio Compra/Venta"])
    datos["Energía Compra/Venta"] = pd.to_numeric(datos["Energía Compra/Venta"])

    datos["Fecha"]=pd.to_datetime(datos["Fecha"],format='%d/%m/%Y')


    os.remove(ruta + "\\" + test_file)

    return datos

def convertPort2df(archivo,ruta,date):

    test_file = "support_file"  # para no alterar los descarados

    open_file = open(ruta + "\\" + archivo, "r")
    open_test_file = open(ruta + "\\" + test_file, "w")

    datos = open_file.readlines()
    open_file.close()
    open_test_file.writelines(datos[2:])
    open_test_file.close()

    datos = pd.read_csv(ruta + "\\" + test_file, delimiter=";", encoding='ISO-8859-1')

    datos = datos.iloc[6,2:27].to_frame()
    date = datetime.datetime.strptime(date, '%Y%m%d')
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    datos=datos.rename(columns={6:"Values"})
    hours=range(1,len(datos)+1)
    date=list(date for i in range(1,len(datos)+1))
    datos["Hora"]=hours
    datos["Fecha"]=date
    datos["Fecha"] = pd.to_datetime(datos["Fecha"], format='%Y-%m-%d')
    datos=datos.reindex(columns=["Hora","Fecha","Values"])

    datos["Values"] = datos["Values"].str.replace('.', '').str.replace(',', '.').astype(float)

    os.remove(ruta + "\\" + test_file)

    return datos

def convertPrice2df(archivo,ruta,date):

    test_file = "support_file"  # para no alterar los descarados

    open_file = open(ruta + "\\" + archivo, "r")
    open_test_file = open(ruta + "\\" + test_file, "w")

    datos = open_file.readlines()
    open_file.close()
    open_test_file.writelines(datos[1:])
    open_test_file.close()

    datos = pd.read_csv(ruta + "\\" + test_file, delimiter=";", encoding='ISO-8859-1',header=None)

    datos = datos.iloc[:,[5]]

    date = datetime.datetime.strptime(date, '%Y%m%d')
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    datos=datos.rename(columns={5:"Values"})
    hours=range(1,len(datos)+1)
    date=list(date for i in range(1,len(datos)+1))
    datos["Hora"]=hours
    datos["Fecha"]=date
    datos["Fecha"]=pd.to_datetime(datos["Fecha"], format='%Y-%m-%d')
    datos=datos.reindex(columns=["Hora","Fecha","Values"])

    os.remove(ruta + "\\" + test_file)

    return datos

#Añadir los datos a la bbdd
def add_data_ESIOS(BBDD,tabla1,datos): #creo una tabla temporal, introduzco los cambios en la tabla "medidas" e inserto nuevas filas
    conn = sql.connect(BBDD)
    cursor=conn.cursor()
    tabla2="tabla2"
    if tabla2 not in tablas_BBDD(BBDD):
        tabla2 = createTable(BBDD, tabla2, [("datetime", "Date"), (datos.columns[1], "Decimal")])

    datos.to_sql(tabla2,conn,if_exists="replace", index=False)
    fecha=datos.columns[0]
    valor=datos.columns[1]

    #query = f"UPDATE {tabla1}.{valores} = (SELECT {tabla2}.{valores} WHERE " \
    #        f"{tabla1}.{fecha} = {tabla2}.{fecha})" \
    #        f" WHERE EXISTS (SELECT 1 FROM {tabla2} WHERE {tabla2}.{fecha} = {tabla1}.{fecha})"
    query= f"UPDATE {tabla1} SET {valor} = (SELECT {tabla2}.{valor} FROM {tabla2} WHERE " \
            f"{tabla1}.{fecha} = {tabla2}.{fecha})" \
            f" WHERE EXISTS (SELECT 1 FROM {tabla2} WHERE {tabla2}.{fecha} = {tabla1}.{fecha})"
    cursor.execute(query)

    #query = f"INSERT INTO {tabla1} ({tabla1}.{fecha}, {tabla1}.{valores}) (SELECT {tabla2}.{fecha}, {tabla2}.{valores} " \
    #        f"FROM {tabla2} " \
    #        f"WHERE NOT EXISTS (SELECT 1 FROM {tabla1} WHERE {tabla1}.{fecha} = {tabla2}.{fecha}))"
    #query = f"INSERT INTO {tabla1} ({fecha},{valores}) (SELECT {tabla2}.{fecha},{tabla2}.{valores} FROM {tabla2} " \
    #        f"WHERE NOT EXISTS (SELECT 1 FROM {tabla1} WHERE {tabla1}.{fecha} = {tabla2}.{fecha}))
    query=f"INSERT INTO {tabla1} ({fecha},{valor}) SELECT {tabla2}.{fecha},{tabla2}.{valor} FROM {tabla2} " \
          f"LEFT JOIN {tabla1} ON {tabla1}.{fecha} ={tabla2}.{fecha} WHERE {tabla1}.{fecha} IS NULL"
    cursor.execute(query)

    query=f"DROP TABLE {tabla2}"
    cursor.execute(query)

    conn.commit()
    conn.close()

def add_data_OMIE(BBDD,tabla1,datos):
    conn = sql.connect(BBDD)
    cursor=conn.cursor()
    tabla2="tabla2"
    if tabla2 not in tablas_BBDD(BBDD):
        tabla2 = createTable(BBDD, tabla2, [
            ('Hora', 'INT'),
            ('Fecha', 'Date'),
            ('Pais', 'VARCHAR(4)'),
            ('Tipo_Oferta', 'VARCHAR(1)'),
            ('Energía_CompraVenta', 'FLOAT'),
            ('Precio_CompraVenta', 'FLOAT'),
            ('Ofertada_OC', 'VARCHAR(1)')])

    datos.to_sql(tabla2,conn,if_exists="replace", index=False)

    query =f"INSERT INTO {tabla1} SELECT * FROM {tabla2}"

    cursor.execute(query)
    conn.commit()

    #query=f"DELETE FROM {tabla2}"
    query = f" DROP TABLE IF EXISTS {tabla2}"

    cursor.execute(query)

    conn.commit()
    conn.close()

def add_data_OMIE_port(BBDD,tabla1,datos):
    conn = sql.connect(BBDD)
    cursor=conn.cursor()
    tabla2="tabla2"
    if tabla2 not in tablas_BBDD(BBDD):
        tabla2 = createTable(BBDD, tabla2, [
            ('Hora', 'INT'),
            ('Fecha', 'Date'),
            ('Demanda_Portugal', 'FLOAT')])

    datos.to_sql(tabla2,conn,if_exists="replace", index=False)

    query =f"INSERT INTO {tabla1} SELECT * FROM {tabla2}"

    cursor.execute(query)
    conn.commit()

    query=f" DROP TABLE IF EXISTS {tabla2}"
    cursor.execute(query)

    conn.commit()
    conn.close()

def add_data_OMIE_price(BBDD,tabla1,datos):
    conn = sql.connect(BBDD)
    cursor=conn.cursor()
    tabla2="tabla2"
    if tabla2 not in tablas_BBDD(BBDD):
        tabla2 = createTable(BBDD, tabla2, [
            ('Hora', 'INT'),
            ('Fecha', 'Date'),
            ('Precio', 'FLOAT')])

    datos.to_sql(tabla2,conn,if_exists="replace", index=False)

    query =f"INSERT INTO {tabla1} SELECT * FROM {tabla2}"

    cursor.execute(query)
    conn.commit()

    query=f" DROP TABLE IF EXISTS {tabla2}"
    cursor.execute(query)

    conn.commit()
    conn.close()

#Todo lo que tiene que ver con las bases de datos
def createBD(ruta,nombre): #ya esta lista
    #ruta=(os.path.dirname(os.getcwd()) + "\\BBDD\\")
    conn=sql.connect(f"{ruta}\{nombre}.db") #crear
    conn.commit() #Guardar
    conn.close() #Cerrar
    BBDD=f"{ruta}\\{nombre}.db" #Para el resto de tareas
    return BBDD

def eliminateBD(ruta,nombre):
    pass
def createTable(BBDD,tabla,informacion): #ya está lista
    #compruebo si la tabla ya existe
    infor=""
    #los datos dentro de informacion son duplas que contienen el nombre del dato y el tipo de dato
    for info in informacion: #Creo un str para las columnas de la bbdd
        infor=infor+f"\n{info[0]} {info[1]}" if info==informacion[len(informacion)-1] else infor+f"\n{info[0]} {info[1]},"
    conn= sql.connect(BBDD)
    cursor=conn.cursor()
    #ALTER TABLE personas ADD edad INTEGER NOT NULL DEFAULT 0
    cursor.execute(f"CREATE TABLE {tabla} ({infor})")
    conn.commit()
    conn.close()
    return tabla

def eliminateTable(BBDD,tabla):
    conexion = sql.connect(f'{BBDD}')
    cursor = conexion.cursor()

    consulta = f"DROP TABLE {tabla}"
    cursor.execute(consulta)

    conexion.commit()
    conexion.close()

def eliminate_rows(BBDD,tabla,fecha1,fecha2):
    fecha1 = datetime.datetime.strptime(fecha1, '%Y-%m-%d')
    conn = sql.connect(BBDD)
    cursor = conn.cursor()
    if os.path.basename(BBDD)=="OMIE.db":
        fecha2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d')
        cursor.execute(f"DELETE FROM {tabla} WHERE Fecha>='{fecha1}' and Fecha<='{fecha2}'")
    elif os.path.basename(BBDD)=="ESIOS.db":
        fecha2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d')+ datetime.timedelta(hours=23)
        cursor.execute(f"DELETE FROM {tabla} WHERE datetime>='{fecha1}' and datetime<='{fecha2}'")
    conn.commit()

    conn.close()
def tablas_BBDD(BBDD):#ya está lista
    conn = sql.connect(BBDD)
    cursor=conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #sqlite_master es una tabla que crea el sistema automaticamente
    tablas=cursor.fetchall()
    conn.close()
    tablas=[dato[0] for dato in tablas]
    return tablas

def columna_Tabla(BBDD,tabla):
    conn = sql.connect(BBDD)
    cursor=conn.cursor()
    query=f"PRAGMA table_info({tabla})"
    cursor.execute(query)
    columnas_tabla=cursor.fetchall()
    conn.commit()
    conn.close()
    columnas_tabla=[elem[1] for elem in columnas_tabla]
    return columnas_tabla
#añade una nueva columan
def newColumn(BBDD,tabla,columna,tipo_dato):#ya está lista
    conn = sql.connect(BBDD)
    cursor = conn.cursor()
    columna=columna.replace(" ","_")
    columna = columna.replace(".","")
    columna = columna.replace("+", "")
    cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo_dato}")

    conn.commit()
    conn.close()


#recupera datos de la bbdd
def cargar_datosESIOS(BBDD,tabla,columnas,fecha_inicio,fecha_fin): #funciona
    if tabla in tablas_BBDD(BBDD):
        if type(columnas)==tuple or type(columnas)==list:
            infor=""
            for columna in columnas:
                infor = infor + f"{columna.replace(' ', '_')} " if columna == columnas[len(columnas) - 1] else infor + f"{columna.replace(' ','_')}, "
        elif type(columnas)==str:
            infor=columnas.replace(' ','_')

        fi = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
        ff = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d') + datetime.timedelta(hours=23)

        conn = sql.connect(BBDD)

        sql_query=pd.read_sql_query(f"SELECT {infor} FROM {tabla} WHERE  datetime>= '{fi}' and datetime<='{ff}' " ,conn)
        #sql_query=pd.read_sql_query(f"SELECT datetime, {infor} FROM {tabla} WHERE  datetime>= '{fi}' and datetime<='{ff}' " ,conn)
        #datetime,
        conn.commit()
        conn.close()
        return sql_query

def cargarrr(BBDD,tabla):
    conn = sql.connect(BBDD)

    sql_query = pd.read_sql_query(f"SELECT  * FROM {tabla} ", conn)

    conn.commit()
    conn.close()
    return sql_query

def cargar_datosOMIE(BBDD,tabla,fecha):
    if tabla in tablas_BBDD(BBDD):
        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')

        conn = sql.connect(BBDD)

        sql_query=pd.read_sql_query(f"SELECT Hora, Precio_CompraVenta, Energía_CompraVenta ,Tipo_Oferta,Ofertada_OC,Pais FROM {tabla} WHERE  Fecha='{fecha}' " ,conn)

        conn.commit()
        conn.close()
        return sql_query

def cargar_datosOMIE_Precio(BBDD,tabla,fecha1,fecha2):
    if tabla in tablas_BBDD(BBDD):
        fecha1=datetime.datetime.strptime(fecha1, '%Y-%m-%d')
        fecha2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d')
        conn = sql.connect(BBDD)

        sql_query=pd.read_sql_query(f"SELECT Hora,Precio FROM {tabla} WHERE  Fecha>='{fecha1}' and Fecha<='{fecha2}' " ,conn)

        conn.commit()
        conn.close()
        return sql_query
def cargar_datosOMIE_Port(BBDD,tabla,fecha1,fecha2):
    if tabla in tablas_BBDD(BBDD):
        fecha1=datetime.datetime.strptime(fecha1, '%Y-%m-%d')
        fecha2 = datetime.datetime.strptime(fecha2, '%Y-%m-%d')
        conn = sql.connect(BBDD)

        sql_query=pd.read_sql_query(f"SELECT Hora, Demanda_Portugal FROM {tabla} WHERE  Fecha>='{fecha1}' and Fecha<='{fecha2}'" ,conn)
        conn.commit()
        conn.close()
        return sql_query




#IDs
def comprobar_id(BBDD):
    conn = sql.connect(BBDD)
    cursor=conn.cursor()

    query=f"SELECT ID FROM IDs"
    cursor.execute(query)
    id = cursor.fetchall()
    cursor.close()
    conn.close()

    if id== None:
        ids=[0]
        return ids
    else:
        ids = []
        for ele in id:
            ids.append(ele[0])
        return ids

def añadir_id(BBDD,id,name,name_ESIOS,tabla): #lista
    conn = sql.connect(BBDD)
    cursor = conn.cursor()

    query = f"INSERT INTO IDs (ID,Nombre,Nombre_ESIOS,Tabla) VALUES ({id},'{name}','{name_ESIOS}','{tabla}')"

    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

def obtener_nombre_esios(BBDD,id):
    conn = sql.connect(BBDD)
    cursor = conn.cursor()

    query = f"SELECT Nombre_ESIOS FROM IDs WHERE ID={id}"

    cursor.execute(query)

    Nombre_ESIOS=cursor.fetchone()

    cursor.close()
    conn.close()
    return Nombre_ESIOS[0]

def obtener_id(BBDD,tabla,nombre_ESIOS):

    conn = sql.connect(f"{os.getcwd()}\{BBDD}.db")
    cursor=conn.cursor()

    query=f"SELECT ID FROM {tabla} WHERE Nombre_ESIOS={nombre_ESIOS}"

    cursor.execute(query)
    id=cursor.fetchall()
    conn.commit()
    conn.close()
    return id

def ver_tabla_ids(BBDD,tabla):
    conn = sql.connect(BBDD)
    sql_query = pd.read_sql_query(f"SELECT * FROM IDs", conn)
    conn.commit()
    conn.close()
    return sql_query

def descargaOMIE(BBDD,tabla,fecha):

    BBDD = createBD(os.getcwd(), BBDD)

    # compruebo si el archivo es nuevo o no
    if "Curvas_PBC_OMIE" not in os.listdir(os.getcwd()): os.mkdir(os.getcwd() + "\\Curvas_PBC_OMIE")

    ruta = os.getcwd() + "\\Curvas_PBC_OMIE"

    date = datetime.datetime.strftime(fecha, '%Y%m%d')

    archivo = f"curva_pbc_{date}.1"
    archivos = os.listdir(ruta)
    if archivo not in archivos:
        down_OMIE_curves(date,ruta)
    if tabla not in tablas_BBDD(BBDD):
        tabla = createTable(BBDD, tabla, [
            ('Hora', 'INT'),
            ('Fecha', 'Date'),
            ('Pais', 'VARCHAR(30)'),
            ('Tipo_Oferta', 'VARCHAR(1)'),
            ('Energía_CompraVenta', 'FLOAT'),
            ('Precio_CompraVenta', 'FLOAT'),
            ('Ofertada_OC', 'VARCHAR(1)')])
    if len(cargar_datosOMIE(BBDD,tabla,datetime.datetime.strftime(fecha,"%Y-%m-%d")))==0:
        df = convertOMIE2df(archivo, ruta)
        add_data_OMIE(BBDD, tabla, df)

def descargaESIOS(token, BBDD, tabla, id, name, fecha_inicio,fecha_fin,max_prevs):


    BBDD = createBD(os.getcwd(), BBDD)
    today= datetime.datetime.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    max=datetime.time(11,0,0)
    now=datetime.datetime.now().time()
    prevs=(datetime.datetime.today()+datetime.timedelta(days=1+max_prevs)).strftime("%Y-%m-%d")


    if "IDs" not in tablas_BBDD(BBDD):  # Para la primera vez
        createTable(BBDD, "IDs", [("ID", "INT"), ("Nombre", "VARCHAR(100)"), ("Nombre_ESIOS", "VARCHAR(100)"),("Tabla", "VARCHAR(30)")])

    # compruebo si el ID es nuevo o no
    if tabla == "Previsiones":
        """if now <= max:
            data = down_ESIOS(token, id, tomorrow, prevs)
            if id not in comprobar_id(BBDD):
                nombre_ESIOS = data["indicator"]["name"].replace(" ", "_")
                nombre_ESIOS = nombre_ESIOS.replace(".", "")
                nombre_ESIOS = nombre_ESIOS.replace("+", "")
                añadir_id(BBDD, id, name, nombre_ESIOS, tabla)

            else:
                nombre_ESIOS = obtener_nombre_esios(BBDD, id)

            if len(data["indicator"]["values"]) > 0:
                df = convertESIOS2df(data, id, nombre_ESIOS)
                if tabla not in tablas_BBDD(BBDD):
                    tabla = createTable(BBDD, tabla, [("datetime", "Date"), (df.columns[1], "Decimal")])
                if nombre_ESIOS not in columna_Tabla(BBDD, tabla):
                    newColumn(BBDD, tabla, nombre_ESIOS, "Decimal")
                add_data_ESIOS(BBDD, tabla, df)
        else:
            tomorrow = (datetime.datetime.today() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")"""
        data = down_ESIOS(token, id, fecha_inicio, prevs)

        if id not in comprobar_id(BBDD):
            nombre_ESIOS = data["indicator"]["name"].replace(" ", "_")
            nombre_ESIOS = nombre_ESIOS.replace(".", "")
            nombre_ESIOS = nombre_ESIOS.replace("+", "")
            añadir_id(BBDD, id, name, nombre_ESIOS, tabla)

        else:
            nombre_ESIOS = obtener_nombre_esios(BBDD, id)

        if len(data["indicator"]["values"]) > 0:
            df = convertESIOS2df(data, id, nombre_ESIOS)
            if tabla not in tablas_BBDD(BBDD):
                tabla = createTable(BBDD, tabla, [("datetime", "Date"), (df.columns[1], "Decimal")])
            if df.columns[1] not in columna_Tabla(BBDD, tabla):
                newColumn(BBDD, tabla, df.columns[1], "Decimal")
            add_data_ESIOS(BBDD, tabla, df)
    elif tabla == "Interconexiones":

        if id not in comprobar_id(BBDD):
            data = down_ESIOS(token, id, fecha_inicio, prevs)
            nombre_ESIOS = data["indicator"]["name"].replace(" ", "_")
            nombre_ESIOS = nombre_ESIOS.replace(".", "")
            nombre_ESIOS = nombre_ESIOS.replace("+", "")
            añadir_id(BBDD, id, name, nombre_ESIOS, tabla)
        else:
            nombre_ESIOS = obtener_nombre_esios(BBDD, id)
            data = down_ESIOS(token, id, fecha_fin, prevs)

        if len(data["indicator"]["values"]) > 0:
            df = convertESIOS2df(data, id, nombre_ESIOS)
            if tabla not in tablas_BBDD(BBDD):
                tabla = createTable(BBDD, tabla, [("datetime", "Date"), (nombre_ESIOS, "Decimal")])
            if nombre_ESIOS not in columna_Tabla(BBDD, tabla):
                newColumn(BBDD, tabla, nombre_ESIOS, "Decimal")
            add_data_ESIOS(BBDD, tabla, df)
    else:
        if id not in comprobar_id(BBDD):

            data = down_ESIOS(token, id, fecha_inicio, today)
            nombre_ESIOS = data["indicator"]["name"].replace(" ", "_")
            nombre_ESIOS = nombre_ESIOS.replace(".", "")
            nombre_ESIOS = nombre_ESIOS.replace("+", "")
            añadir_id(BBDD, id, name, nombre_ESIOS, tabla)

            if len(data["indicator"]["values"]) > 0:

                df = convertESIOS2df(data, id, nombre_ESIOS)
                if tabla not in tablas_BBDD(BBDD):
                    tabla = createTable(BBDD, tabla, [("datetime", "Date"), (nombre_ESIOS, "Decimal")])
                if nombre_ESIOS not in columna_Tabla(BBDD, tabla):

                    newColumn(BBDD, tabla, nombre_ESIOS, "Decimal")
                add_data_ESIOS(BBDD, tabla, df)

        else:
            if fecha_fin != today:
                data = down_ESIOS(token, id, fecha_fin, today)
                nombre_ESIOS = obtener_nombre_esios(BBDD, id)
                if len(data["indicator"]["values"]) > 0:
                    df = convertESIOS2df(data, id, nombre_ESIOS)
                    if tabla not in tablas_BBDD(BBDD):
                        tabla = createTable(BBDD, tabla, [("datetime", "Date"), (nombre_ESIOS, "Decimal")])
                    if nombre_ESIOS not in columna_Tabla(BBDD, tabla):
                        newColumn(BBDD, tabla, nombre_ESIOS, "Decimal")
                    add_data_ESIOS(BBDD, tabla, df)

def descargaPortugal(BBDD,tabla,fecha):
    BBDD = createBD(os.getcwd(), BBDD)

    # compruebo si el archivo es nuevo o no
    if "Demanda_Portugal" not in os.listdir(os.getcwd()): os.mkdir(os.getcwd() + "\\Demanda_Portugal")

    ruta = os.getcwd() + "\\Demanda_Portugal"


    date = datetime.datetime.strftime(fecha, '%Y%m%d')
    archivo = f"pdbc_tot_{date}.1"
    archivos = os.listdir(ruta)
    if archivo not in archivos:
        down_OMIE_portugal(date,ruta)
    if tabla not in tablas_BBDD(BBDD):
        tabla = createTable(BBDD, tabla, [
            ('Hora', 'INT'),
            ('Fecha', 'Date'),
            ('Demanda_Portugal', 'FLOAT')])
    if len(cargar_datosOMIE_Port(BBDD, tabla, datetime.datetime.strftime(fecha,"%Y-%m-%d"),datetime.datetime.strftime(fecha,"%Y-%m-%d"))) == 0:
        df = convertPort2df(archivo, ruta, date)
        add_data_OMIE_port(BBDD, tabla, df)

def descargaPrecio(BBDD,tabla,fecha):
    BBDD = createBD(os.getcwd(), BBDD)

    # compruebo si el archivo es nuevo o no
    if "PrecioDiario" not in os.listdir(os.getcwd()): os.mkdir(os.getcwd() + "\\PrecioDiario")

    ruta = os.getcwd() + "\\PrecioDiario"



    date = datetime.datetime.strftime(fecha, '%Y%m%d')
    archivo = f"marginalpdbc_{date}.1"

    archivos = os.listdir(ruta)
    if archivo not in archivos:
        down_OMIE_price(date,ruta)
    if tabla not in tablas_BBDD(BBDD):
        tabla = createTable(BBDD, tabla, [
            ('Hora', 'INT'),
            ('Fecha', 'Date'),
            ('Precio', 'FLOAT')])
    if len(cargar_datosOMIE_Precio(BBDD, tabla, datetime.datetime.strftime(fecha,"%Y-%m-%d"),datetime.datetime.strftime(fecha,"%Y-%m-%d"))) == 0:
        df = convertPrice2df(archivo, ruta, date)
        add_data_OMIE_price(BBDD, tabla, df)
#consulta inicial para ver que datos hay

def start_consult(BBDD):
    BBDD_concepts = pd.DataFrame(
        columns=["BBDD", "Tabla", "Nombre", "Nombre_ESIOS", "ID", "MIN(datetime)", "MAX(datetime)"])
    if type(BBDD)==list:

        for BD in BBDD:

            ruta = f"{os.getcwd()}\{BD}.db"
            if BD == "ESIOS":

                conn = sql.connect(ruta)

                #cursor = conn.cursor()

                query =pd.read_sql_query( f"SELECT Nombre, Nombre_ESIOS,Tabla,ID FROM IDs",conn)

                conn.commit()
                df=pd.DataFrame(columns=["MIN(datetime)","MAX(datetime)"])
                for i in range(len(query)):
                    try:

                        query2 = pd.read_sql_query(f"SELECT MIN(datetime),MAX(datetime) FROM {query['Tabla'][i]} "
                                               f"WHERE {query['Nombre_ESIOS'][i].replace(' ', '_').replace('.', '').replace('+', '')} IS NOT NULL ",conn)
                        df=pd.concat([df,query2])

                    except:
                        query2=pd.DataFrame(columns=["MIN(datetime)","MAX(datetime)"])
                        query2.loc[len(query2)]=[datetime.datetime.today(),datetime.datetime.today()]
                        df = pd.concat([df, query2])






                df=df.reset_index(drop=True)
                query=pd.concat([query,df],axis=1)
                query["MIN(datetime)"]=pd.to_datetime(query["MIN(datetime)"]).dt.strftime("%Y-%m-%d")
                query["MAX(datetime)"] = pd.to_datetime(query["MAX(datetime)"]).dt.strftime("%Y-%m-%d")
                query["BBDD"]=BD
                query=query.reindex(columns=["BBDD","Tabla","Nombre","Nombre_ESIOS","ID","MIN(datetime)","MAX(datetime)"])

                conn.commit()
                conn.close()
                BBDD_concepts = pd.concat([BBDD_concepts,query])

                #query = pd.DataFrame(columns=["BBDD","Tabla","Nombre","Nombre_ESIOS","ID","MIN(datetime)","MAX(datetime)"])


            elif BD == "OMIE":
                for tabla in tablas_BBDD(ruta):

                    if tabla== "CurvasOfertaDemanda":
                        conn = sql.connect(ruta)
                        query = pd.read_sql_query(f"SELECT MIN(Fecha), MAX(Fecha) FROM {tabla}", conn)

                        query["MIN(Fecha)"] = pd.to_datetime(query["MIN(Fecha)"]).dt.strftime("%Y-%m-%d")
                        query["MAX(Fecha)"] = pd.to_datetime(query["MAX(Fecha)"]).dt.strftime("%Y-%m-%d")
                        query = [BD, tabla, tabla, tabla, tabla, query["MIN(Fecha)"][0], query["MAX(Fecha)"][0]]
                        BBDD_concepts.loc[len(BBDD_concepts)] = query
                    elif tabla in["DemandaPortugal","PrecioDiario"]:
                        conn = sql.connect(ruta)
                        query = pd.read_sql_query(f"SELECT MIN(Fecha), MAX(Fecha) FROM {tabla}", conn)
                        query["MIN(Fecha)"] = pd.to_datetime(query["MIN(Fecha)"]).dt.strftime("%Y-%m-%d")
                        query["MAX(Fecha)"] = pd.to_datetime(query["MAX(Fecha)"]).dt.strftime("%Y-%m-%d")
                        query=[BD,tabla,tabla,tabla,tabla,query["MIN(Fecha)"][0],query["MAX(Fecha)"][0]]
                        BBDD_concepts.loc[len(BBDD_concepts)] = query


    return BBDD_concepts
def calculate_day(date):
    BBDD = createBD(os.getcwd(), "ESIOS")
    tabla="Previsiones"
    columnas=columna_Tabla(BBDD,tabla)
    ESIOS=cargar_datosESIOS(BBDD, tabla, columnas, date, date)
    tabla = "Interconexiones"
    columnas = columna_Tabla(BBDD, tabla)
    InterCap=cargar_datosESIOS(BBDD, tabla, columnas[1:], date, date)

    df = pd.concat([ESIOS, InterCap],axis=1)

    return df
def aproxim_day(date):
    BBDD = createBD(os.getcwd(), "ESIOS")
    tabla="ProgramaPBF"
    columnas=columna_Tabla(BBDD,tabla)
    ESIOSPBF = cargar_datosESIOS(BBDD, tabla, columnas, date, date)
    tabla="Previsiones"
    columnas=columna_Tabla(BBDD,tabla)
    ESIOSPrev=cargar_datosESIOS(BBDD, tabla, columnas[1:], date, date)
    BBDD = createBD(os.getcwd(), "OMIE")
    tabla = "PrecioDiario"
    Precio =cargar_datosOMIE_Precio(BBDD,tabla,date,date)
    tabla = "DemandaPortugal"
    Dem_port = cargar_datosOMIE_Port(BBDD,tabla,date,date)
    df=pd.concat([Precio,Dem_port["Demanda_Portugal"],ESIOSPrev,ESIOSPBF],axis=1)
    return df

def dwnl_graf_data(lista_datos,fechai,fechaf):

    BBDD=lista_datos[0]
    BBDD = createBD(os.getcwd(), BBDD)
    tabla= lista_datos[1]
    Nombre=lista_datos[2]
    columna=lista_datos[3]
    if lista_datos[0]=="ESIOS":
        datos=cargar_datosESIOS(BBDD, tabla, columna, fechai, fechaf)
        datos=datos[f"{columna}"]
    elif lista_datos[0]=="OMIE":
        if tabla=="DemandaPortugal":
            datos=cargar_datosOMIE_Port(BBDD,tabla,fechai, fechaf)
        elif tabla=="PrecioDiario":
            datos=cargar_datosOMIE_Precio(BBDD,tabla,fechai, fechaf)
    else:
        datos=0
    return datos

if __name__=="__main__":

    token = "c2951aa2fff559933828ba277d4459e1da579e89dd09aa6a8659b84846281cf4"
    id = 1775
    name = "Previsiones Demanda D"
    fecha_inicio = "2023-01-01"
    hoy = datetime.datetime.today()
    hoy = hoy.date().strftime("%Y-%m-%d")
    fecha_fin = "2023-06-11"
    fecha= "2023-06-26"

    BBDD = createBD(os.getcwd(), "ESIOS")

    tabla = "Interconexiones"
    InterCap = cargar_datosESIOS(BBDD, tabla, "*", fecha, fecha)

    print(InterCap['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación'])
    print(InterCap['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación'])


