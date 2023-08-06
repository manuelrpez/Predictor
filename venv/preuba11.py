import Descargas
import os

BBDD="OMIE"
BBDD=Descargas.createBD(os.getcwd(),BBDD)
fecha1="2023-07-01"
fecha2="2023-07-20"
#"PrecioDiario"
#"DemandaPortugal"
#"CurvasOfertaDemanda"
Descargas.eliminate_rows(BBDD,"CurvasOfertaDemanda",fecha1,fecha2)

