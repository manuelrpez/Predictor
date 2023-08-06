import Descargas
import os
import datetime
BBDD="OMIE"
BBDD=Descargas.createBD(os.getcwd(),BBDD)
date="2023-07-09"

df=Descargas.cargar_datosOMIE_Port(BBDD,"DemandaPortugal",date,date)
print(df)