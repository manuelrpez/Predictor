#Aqui se prepara la lista de errores
#cada error entrara con un codigo y luego se mostrara en pantalla para que quede constancia

def error(numerito,*variables):
    match numerito:

        case 0:
            print("El id de la descarga no coincide con el que se quería descargar. Puede haber cambiado el formato de consulta de ESIOS")
        case 1:
            print(f"El nombre '{variables[0]}' no corresponde con el dato que se quería descargar '{variables[1]}'. Esios puede haber cambiado la ruta del dato")

        case 2:
            print("La temporalidad de los datos no está soportada por el programa. Debe modificar el programa en el Modulo: Descargas función: convert2Pd_format")
        case 3:
            print("casa")



