import datetime
import bs4
import requests
import os
from urllib import request

ruta = os.getcwd()
# creo la carpeta Curva_PBC_ESIOS si no existe (first time)
if "Curvas_PBC_OMIE" not in os.listdir(ruta): os.mkdir(ruta + "\\Curvas_PBC_OMIE")

ruta = ruta + "\\Curvas_PBC_OMIE"

def down_omie(fecha,ruta):

    #si entra como string fecha= "2023-04-01"
    #date=datetime.datetime.strptime(fecha,'%Y-%m-%d')
    #date= datetime.datetime.strftime(date,'%Y%m%d')
    #si entra como datetime.datetime
    date= datetime.datetime.strftime(fecha,'%Y%m%d')

    file_name = f"curva_pbc_{date}.1"

    url=f"https://www.omie.es/en/file-download?parents%5B0%5D=curva_pbc&filename=curva_pbc_{date}.1"

    request.urlretrieve(url, ruta+"\\"+file_name)

def last_down(ruta):


    pass

def convertOMIE2df(fecha,ruta):
    date = datetime.datetime.strftime(fecha, '%Y%m%d')
    archivo = f"curva_pbc_{date}.1"  # este es variable
    test_file = "support_file"  # para no alterar los descarados

    ruta = os.getcwd() + "\\Curvas_PBC_OMIE"
    open_file = open(ruta + "\\" + archivo, "r")
    open_test_file = open(ruta + "\\" + test_file, "w")

    datos = open_file.readlines()
    open_test_file.writelines(datos[2:])

    datos = pd.read_csv(ruta + "\\" + test_file, delimiter=";", encoding='ISO-8859-1')
    datos = datos.iloc[:, [1, 2, 4, 5, 6, 7]]
    open_file.close()
    open_test_file.close()
    os.remove(ruta + "\\" + test_file)


if __name__=="__main__":

    ruta = os.getcwd()
    # creo la carpeta Curva_PBC_ESIOS si no existe (first time)
    if "Curvas_PBC_OMIE" not in os.listdir(ruta): os.mkdir(ruta + "\\Curvas_PBC_OMIE")

    ruta = ruta + "\\Curvas_PBC_OMIE"
    Today= datetime.datetime.now()
    Tomorrow =Today + datetime.timedelta(days=1)

    if datetime.datetime.now().hour>12:
        date = Tomorrow.date()
    else:
        date = Today.date()

    start_date = datetime.date(2023, 4, 1)

    while start_date<=date:

        down_omie(start_date,ruta)
        start_date+=datetime.timedelta(days=1)
