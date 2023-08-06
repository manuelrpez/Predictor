import openpyxl
import pandas as pd
import Descargas
import datetime
import Calculos
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
class int:
    def __init__(self,valor):
        self.valor=valor
    def get(self):
        return 0

def exportar(df,icolumna,ifila):
    ruta = os.path.expanduser("~/Desktop")
    nombre = f'Backtesting.xlsx'

    libro_trabajo = openpyxl.load_workbook(os.path.join(ruta, nombre))
    hoja = libro_trabajo.active
    index=0
    for elem in df:
        hoja.cell(row=ifila+index ,column=icolumna,value=elem)
        index+=1

    direccion = os.path.join(ruta, nombre)
    # Guardar el libro de trabajo como un archivo Excel
    libro_trabajo.save(direccion)

int=int(0)
day=datetime.datetime(datetime.datetime.now().year,1,1)+datetime.timedelta(days=30)

"""while day<=datetime.datetime.now():
    day+=datetime.timedelta(days=1)
    inputday=day.strftime("%Y-%m-%d")
"""
ruta = os.path.expanduser("~/Desktop")
nombre = f'Backtesting.xlsx'

libro_trabajo = openpyxl.load_workbook(os.path.join(ruta, nombre))
hoja = libro_trabajo.active

ifila=1
while day<=datetime.datetime.now():

    day += datetime.timedelta(days=1)
    inputday = day.strftime("%Y-%m-%d")
    print(inputday)
    for icolumna in range(1,31):

        aproxday=day-datetime.timedelta(days=icolumna)
        aproxdayinput=aproxday.strftime("%Y-%m-%d")

        calculate_day=Descargas.calculate_day(inputday)
        aproxim_day=Descargas.aproxim_day(aproxdayinput)
        PVaprox=Calculos.aprox_dayPV("OMIE",
                                     "CurvasOfertaDemanda",
                                     datetime.datetime.now().strftime("%Y-%m-%d"), aproxim_day,
                                 calculate_day, int, int, [])

        index = 0
        for elem in PVaprox["Precio"]:
            hoja.cell(row=ifila + index, column=icolumna, value=elem)
            index += 1

    direccion = os.path.join(ruta, nombre)
    # Guardar el libro de trabajo como un archivo Excel
    libro_trabajo.save(direccion)
    ifila+=24
