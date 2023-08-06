import tkinter as tk
from tkinter import ttk
import openpyxl
import Calculos
import Descargas
import pandas as pd
import datetime
import Graficas
import os
class ventana_principal(tk.Tk):

    pass

class ventana_secundaria(tk.Toplevel):

    def cerrar_ventana(self,Button):
        Button.config(state=tk.NORMAL)
        self.destroy()

class Panel_descargas(tk.Frame):

    def eliminate(panel):

        pass


    def dwnld_frame(self,Entradas_pred):
        Entradas = ["Nombre:","Desde:","Hasta:"]
        contador = 0
        Texto_entrada = []


        for entrada in Entradas:
            entrada_texto = tk.Label(self,
                                     bd=2,
                                     text=entrada.title(),
                                     width=5,
                                     font=("Times new Roman", "12")
                                     )
            entrada_texto.grid(row=0,
                               column=2 * contador,
                               sticky="w")

            Texto_entrada.append("")
            Texto_entrada[contador] = tk.StringVar()
            Texto_entrada[contador].set(Entradas_pred[contador])
            if entrada=="Nombre:":
                entrada_entry = tk.Label(self,
                                         bd=2,
                                         width=30,
                                         textvariable=Texto_entrada[contador])
            else:
                entrada_entry = tk.Label(self,
                                         bd=2,
                                         width=8,
                                         textvariable=Texto_entrada[contador])
            entrada_entry.grid(row=0,
                               column=2 * contador + 1,
                               sticky="w")
            borrar_Descarga=tk.Button(self,
                                      width=8,
                                      text=""
                                           "Eliminar",
                                      command=self.destroy)
            borrar_Descarga.grid(row=0,
                                 column=len(Entradas)*2+1,
                                 sticky="w")
            contador += 1

def Aproxim_row():
    calculate_day=Descargas.calculate_day(label1.cget("text"))
    aproxim_day=Descargas.aproxim_day(label2.cget("text"))
    PVaprox=Calculos.aprox_dayPV(BBDD_concepts[BBDD_concepts["Tabla"] == "CurvasOfertaDemanda"]["BBDD"].values[0],
                         BBDD_concepts[BBDD_concepts["Tabla"] == "CurvasOfertaDemanda"]["Tabla"].values[0],
                         label2.cget("text"), aproxim_day, calculate_day, int1, int2, Add_Vol_fila_vars)

    nueva_fila_vars = []

    text_aporx=tk.Label(inner_frame,text=label2.cget("text"))
    text_aporx.grid(row=len(entry_vars),column=0)
    for columna in range(len(price)):
        var = tk.DoubleVar()
        entry = tk.Entry(inner_frame, textvariable=var,width=4)
        entry.bind('<Return>', lambda event: Graficas.graf_reload(graf_data,calculate_day,aproxim_day))
        var.set(PVaprox.iloc[columna]["Precio"])
        entry.grid(row=len(entry_vars), column=columna+1,padx=2)
        nueva_fila_vars.append(var)
    index=0
    while graf_data[index][1].get_title() != "Precio" and index<len(graf_data):
        index +=1


    variable=tk.BooleanVar()
    boton = tk.Checkbutton(inner_frame,variable=variable,
                      command=lambda: Graficas.graf_price_option(aproxim_day['Precio'],graf_data))
    boton.grid(row=len(entry_vars), column=len(price)+2)

    nueva_fila_vars.append(variable)

    results.config(width=656, height=330)
    entry_vars.append(nueva_fila_vars)
    graf_data[index][3].append([nueva_fila_vars,"PV",label2.cget("text")])

def Average():
    List=[]
    Average=[]
    index = 0
    while graf_data[index][1].get_title() != "Precio" and index < len(graf_data):
        index += 1
    ydata = graf_data[index][3]
    for y in ydata:
        if y[1]=="PV" and y[0][len(y[0])-1].get():
            values = []
            for elem in range(len(y[0])-1):
                values.append(y[0][elem].get())
            List.append(values)
    i = 0
    if len(List)>0:
        for entry in Average_entry_vars:
            entry.delete(0, tk.END)  # Borra el contenido actual del Entry

            values=[]

            for val in List:
                values.append(val[i])
            i += 1

            val=sum(values)/len(values)
            entry.insert(0, val)
            Average.append(val)


    Graficas.graf_reload(graf_data, calculate_day, aproxim_day)

def update_label(label, increment,graf_data,price_entry_vars):
    current_date = datetime.datetime.strptime(label["text"], "%Y-%m-%d")

    if increment:
        current_date += datetime.timedelta(days=1)
    else:
        current_date -= datetime.timedelta(days=1)
    label.config(text=current_date.strftime("%Y-%m-%d"))

    #if label.winfo_parent()==".!frame3.!frame":

    calculate_day=Descargas.calculate_day(label1.cget("text"))
    #else:
    aproxim_day=Descargas.aproxim_day(label2.cget("text"))

    price = aproxim_day[aproxim_day['Precio'].notna()]['Precio']
    if len(price)>0:
        label_count=0
        for label_price in price_entry_vars:
            label_price.config(text=int(price[label_count]))
            label_count+=1

    Graficas.graf_reload(graf_data,calculate_day,aproxim_day)

def down():

    if len(BBDD_concepts)>0:
        for descarga in range(len(BBDD_concepts)):

            if BBDD_concepts.iloc[descarga]["BBDD"]=="ESIOS":
                Descargas.descargaESIOS("Introducir token personal",
                                     BBDD_concepts.iloc[descarga]["BBDD"],
                                     BBDD_concepts.iloc[descarga]["Tabla"],
                                     int(BBDD_concepts.iloc[descarga]["ID"]),
                                     BBDD_concepts.iloc[descarga]["Nombre"],
                                     BBDD_concepts.iloc[descarga]["MIN(datetime)"],
                                     BBDD_concepts.iloc[descarga]["MAX(datetime)"],
                                     5)

                BBDD_concepts.loc[descarga,"MAX(datetime)"]=datetime.datetime.today().strftime("%Y-%m-%d")

            elif BBDD_concepts.iloc[descarga]["BBDD"]=="OMIE":

                if BBDD_concepts.iloc[descarga]["MAX(datetime)"]=="          ":
                    date=datetime.datetime.strptime(BBDD_concepts.iloc[descarga]["MIN(datetime)"],"%Y-%m-%d").date()
                elif BBDD_concepts.iloc[descarga]["MAX(datetime)"]!=BBDD_concepts.iloc[descarga]["MAX(datetime)"]:
                    date=datetime.datetime.strptime("2023-01-01","%Y-%m-%d").date()
                else:
                    date = datetime.datetime.strptime(BBDD_concepts.iloc[descarga]["MAX(datetime)"], "%Y-%m-%d").date()

                if BBDD_concepts.iloc[descarga]["Tabla"]=="DemandaPortugal":

                    while date <= datetime.datetime.today().date():

                        Descargas.descargaPortugal(BBDD_concepts.iloc[descarga]["BBDD"],
                                                   BBDD_concepts.iloc[descarga]["Tabla"],
                                                   date)
                        date = date + datetime.timedelta(days=1)

                if BBDD_concepts.loc[descarga,"Tabla"]=="CurvasOfertaDemanda":

                    while date <= datetime.datetime.today().date():
                        Descargas.descargaOMIE(BBDD_concepts.iloc[descarga]["BBDD"],
                                                   BBDD_concepts.iloc[descarga]["Tabla"],
                                                   date)
                        date=date+datetime.timedelta(days=1)

                if BBDD_concepts.loc[descarga,"Tabla"]=="PrecioDiario":

                    while date <= datetime.datetime.today().date():
                        Descargas.descargaPrecio(BBDD_concepts.iloc[descarga]["BBDD"],
                                                   BBDD_concepts.iloc[descarga]["Tabla"],
                                                   date)
                        date=date+datetime.timedelta(days=1)


                BBDD_concepts.loc[descarga,"MAX(datetime)"]=datetime.datetime.strftime(date, '%Y-%m-%d')

    tk.messagebox.showinfo("Descargas", "Descarga terminada")

def adaptar_ventana(Alto_ventana,Ancho_ventana):
    screen_width= Inicio.winfo_screenwidth()
    screen_height = Inicio.winfo_screenheight()
    coef_ventana=1

    if min(screen_height/Alto_ventana,screen_width/Ancho_ventana)<1:
        coef_ventana=min(screen_height/Alto_ventana,screen_width/Ancho_ventana)


    # el 0.6 es para que la ventan este más arriba y no tan centrada encuanto a altura
    x1=int((screen_height-Alto_ventana*coef_ventana)*0.5/2)
    y1=int((screen_width-Ancho_ventana*coef_ventana)/2)

    return y1,x1,coef_ventana

def descargas_window():

   
    def cerrar_ventana_descargas():
        Ventana_descargas.cerrar_ventana(btn_page_dwnld)
    def dwnl_graf_data():
        ind = 0

        while BBDD_concepts.iloc[ind][2] != var1.get() and ind < len(BBDD_concepts):
            ind+=1
        if BBDD_concepts.iloc[ind][2] == var1.get():
            datos = Descargas.dwnl_graf_data(BBDD_concepts.iloc[ind], var2.get(),
                                             var3.get())

            fig,ax,canvas=Graficas.graf_dwnl(var1.get(), datos, dwnl_graf_frame,grafdwnl)
            if len(grafdwnl)==0:
                grafdwnl.append(fig)
                grafdwnl.append(ax)
                grafdwnl.append(canvas)
            """except:
                tk.messagebox.showinfo("Error", "Comprueba que esta todo en el formato correcto")"""
    def add_descarga():
        global BBDD_concepts
        def Aceptar(inputs,Add_descarga):

            New_row=[]
            for entry in inputs:
                New_row.append(entry.get())


            BBDD_concepts.loc[len(BBDD_concepts)]=[New_row[0],New_row[1],New_row[2],"",New_row[3],New_row[4],"          "]

            Ventana_descargas.destroy()
            descargas_window()
            Add_descarga.destroy()



        Entradas=["BBDD","Tabla","Nombre:", "Id:", "Fecha inicial:"]
        Add_descarga = tk.Toplevel(Ventana_descargas)
        Add_descarga.geometry(f"280x220+{str(700)}+{str(300)}")
        contador = 0
        head_add_descarga=tk.Frame(Ventana_descargas,
                                   bd=5)
        head_add_descarga.grid(row=0,column=0)
        inputs=[]

        for entrada in Entradas:
            entradatext = tk.Label(Add_descarga,
                                   text=Entradas[contador],
                                   bd=4)
            entradatext.grid(row=contador+1,
                             column=2)

            entradaentry = tk.Entry(Add_descarga,
                                    bd=4
                                    )
            entradaentry.grid(row=contador+1,
                              column=3)
            inputs.append(entradaentry)
            contador += 1

        btn_add_descarga = tk.Button(Add_descarga,
                                     text="Aceptar",
                                     bd=4,
                                     command=lambda:Aceptar(inputs,Add_descarga))
        btn_add_descarga.grid(row=7,
                              column=3,
                              sticky="se")

        btn_no_add_descarga = tk.Button(Add_descarga,
                                        text="Cancelar",
                                        bd=4,
                                        command=Add_descarga.destroy)
        btn_no_add_descarga.grid(row=7,
                                 column=4,
                                 sticky="se")
        return BBDD_concepts

    grafdwnl = []
    btn_page_dwnld.config(state=tk.DISABLED)
    Ventana_descargas=ventana_secundaria()
    Ventana_descargas.geometry(f"{str(Ancho_ventana)}x{str(Alto_ventana)}+{str(200)}+{str(100)}")
    Ventana_descargas.protocol("WM_DELETE_WINDOW", cerrar_ventana_descargas)

    principal_frame=ttk.Frame(Ventana_descargas)
    principal_frame.grid(sticky="nsew")
    head_dwnld=tk.Frame(principal_frame,
                        relief='raised')
    head_dwnld.grid(row=0,
                    column=0,
                    sticky="ew")

    left_panel_dwnl = ttk.Frame(principal_frame)
    left_panel_dwnl.grid(row=0,column=0,sticky="w")

    right_panel_dwnl=ttk.Frame(principal_frame,
                              width=(Ancho_ventana/2))
    right_panel_dwnl.grid(row=0,column=1,sticky="e")

    left_head_dwnld=tk.Frame(left_panel_dwnl,bg='red', relief='raised',width=int(Ancho_ventana/2-200))
    left_head_dwnld.grid(row=0,column=0)
    label_left_head=tk.Label(left_head_dwnld,
                             text="Conceptos a descargar")
    label_left_head.grid(row=0,column=0,sticky="ew")
    btn_page_add_dwnld=tk.Button(left_panel_dwnl,
                        text="+",
                        relief="flat",
                        font=("Times new Roman","12","bold"),
                        command=add_descarga)

    btn_page_add_dwnld.grid(row=0,column=1,sticky="w")



    left_panel_dwnl2=tk.Frame(left_panel_dwnl)
    left_panel_dwnl2.grid(row=1,column=0)
    scrollbar = ttk.Scrollbar(left_panel_dwnl2,orient="vertical")
    scrollbar.grid(row=1, column=0,sticky="ns")

    lienzo = tk.Canvas(left_panel_dwnl2,width=(Ancho_ventana)/2-100, height=(Alto_ventana)-100, yscrollcommand=scrollbar.set)
    lienzo.grid(row=1, column=1,sticky="w")
    scrollbar.config(command=lienzo.yview)

    frame_dwnl = ttk.Frame(lienzo)
    lienzo.create_window((0, 1), window=frame_dwnl, anchor="nw")

    # Configurar el lienzo para ajustar su tamaño al contenido
    frame_dwnl.bind("<Configure>", lambda event: lienzo.configure(scrollregion=lienzo.bbox("all")))

    # Paneles de conceptos a descargar
    contadorconceptos=1
    for i in range(len(BBDD_concepts)):
        A_descargar=Panel_descargas(frame_dwnl,
                              bg="white",
                              bd=2)
        A_descargar.grid(row=contadorconceptos+1,
                         column=1,
                         sticky="w")

        Entradas_pred = BBDD_concepts.loc[i,["Nombre","MIN(datetime)","MAX(datetime)"]].to_list()
        A_descargar.dwnld_frame(Entradas_pred)
        contadorconceptos+=1

    btn_dwnld2sql=tk.Button(left_panel_dwnl2,
                            text="Descargar",
                            command=down)
    btn_dwnld2sql.grid(row=contadorconceptos,
                       column=2,
                       sticky="se")

    Top_right_frame=tk.Frame(right_panel_dwnl,height=50)
    Top_right_frame.grid(row=0,column=0,sticky="n")
    dwnl_entry_frame=tk.Frame(right_panel_dwnl)
    dwnl_entry_frame.grid(row=1,column=0,sticky="n")

    var1=tk.StringVar()
    var2=tk.StringVar()
    var3=tk.StringVar()

    dwnl_label1=tk.Label(dwnl_entry_frame,text="Nombre:")
    dwnl_label1.grid(row=0,column=0,sticky="n")

    dwnl_entry1=tk.Entry(dwnl_entry_frame,textvariable=var1)
    dwnl_entry1.grid(row=0,column=1)

    dwnl_label2 = tk.Label(dwnl_entry_frame, text="Fecha inicial:")
    dwnl_label2.grid(row=0, column=2)
    dwnl_entry2 = tk.Entry(dwnl_entry_frame,textvariable=var2)
    dwnl_entry2.grid(row=0, column=3)

    dwnl_label3 = tk.Label(dwnl_entry_frame, text="Fecha final:")
    dwnl_label3.grid(row=0, column=4)
    dwnl_entry3 = tk.Entry(dwnl_entry_frame,textvariable=var3)
    dwnl_entry3.grid(row=0, column=5)

    dwnl_graf_frame=tk.Frame(right_panel_dwnl)
    dwnl_graf_frame.grid(row=2,column=0)
    dwnl_botton_frame=tk.Button(right_panel_dwnl,text="Visualizar",command=dwnl_graf_data)
    dwnl_botton_frame.grid(row=3,column=0)


def Exportar():
    Export=[]
    index=0
    while graf_data[index][1].get_title() != "Precio" and index < len(graf_data):
        index += 1
    ydata = graf_data[index][3]

    for y in ydata:
        if y[1]=="PV" and y[0][len(y[0])-1].get():
            values = []
            values.append(y[2])
            for elem in range(len(y[0])-1):
                values.append(y[0][elem].get())
            Export.append(values)
        elif y[1]=="Av":
            values = []
            values.append("Promedio")
            for elem in range(len(y[0]) - 1):
                values.append(y[0][elem].get())
            Export.append(values)



    # Crear un nuevo libro de trabajo (workbook) y una hoja (sheet)
    libro_trabajo = openpyxl.Workbook()
    hoja = libro_trabajo.active
    for fila in Export:
        hoja.append(fila)
    ruta=os.path.expanduser("~/Desktop")
    nombre=f'Precio electricidad {label1.cget("text")}.xlsx'
    direccion=os.path.join(ruta, nombre)
    # Guardar el libro de trabajo como un archivo Excel
    libro_trabajo.save(direccion)



BBDD_concepts=Descargas.start_consult(["ESIOS","OMIE"])

calculate_day=Descargas.calculate_day((datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
aproxim_day=Descargas.aproxim_day(datetime.datetime.now().strftime("%Y-%m-%d"))
graf_data=[]
price=aproxim_day[aproxim_day['Precio'].notna()]['Precio']
Inicio=ventana_principal()
Inicio.title("Predictor")
Ancho_ventana=1650
Alto_ventana=850
#y1,x1,coef_ventana=adaptar_ventana(Alto_ventana,Ancho_ventana)


#Inicio.geometry(f"{str(Ancho_ventana * coef_ventana)}x{str(Alto_ventana * coef_ventana)}+{str(y1)}+{str(x1)}")
Inicio.geometry(f"{str(Ancho_ventana)}x{str(Alto_ventana)}+{str(200)}+{str(100)}")
Inicio.config(bg='white')
top_panel=tk.Frame(Inicio, width=Ancho_ventana, height=50,bg='white')
top_panel.grid(row=0,column=0,sticky="nw")
btn_page_dwnld=tk.Button(top_panel,
                    text='Descargas',
                    command=descargas_window)
btn_page_dwnld.grid(row=0,column=0)
btn_page_chrg=tk.Button(top_panel,
                   text="Exportar",
                   command=Exportar)
btn_page_chrg.grid(row=0,column=1)
"""btn_dwnld2sql = tk.Button(top_panel,
                          text="Actualizar",
                          command=down)
btn_dwnld2sql.grid(row=0,
                   column=2,
                   sticky="e")"""

Left_panel=tk.Frame(Inicio,bg='white')
Left_panel.grid(row=1,
                column=0,sticky="nw")
#Panelday
day_panel=tk.Frame(Left_panel)
day_panel.grid(row=0,
               column=0,
               sticky="w")
#Día a calcular:
calculate_panel=tk.Frame(day_panel,bg='white')
calculate_panel.grid(row=0,
                     column=0,
                     sticky="w")
calculate_panel_text=tk.Label(calculate_panel,text="Día a calcular:",width=10,bg='white')
calculate_panel_text.grid(row=0,
                          column=0,
                          sticky="w")
label1 = tk.Label(calculate_panel, text=(datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d"),bg='white')
label1.grid(row=0,
            column=2,sticky="w")
prev_button1 = tk.Button(calculate_panel, text="<", command=lambda: update_label(label1, False,graf_data,price_entry_vars),bg='white')
prev_button1.grid(row=0,
            column=1,sticky="w")
next_button1 = tk.Button(calculate_panel, text=">", command=lambda: update_label(label1, True,graf_data,price_entry_vars),bg='white')
next_button1.grid(row=0,
                  column=3,
                  sticky="w")

#Día ejemplo:
aproxim_panel=tk.Frame(day_panel,bg='white')
aproxim_panel.grid(row=1,
                   column=0,
                   sticky="w")
aproxim_panel_text=tk.Label(aproxim_panel,text="Día ejemplo:",width=10,bg='white')
aproxim_panel_text.grid(row=0,
                        column=0,
                        sticky="w")
label2 = tk.Label(aproxim_panel, text=datetime.datetime.now().strftime("%Y-%m-%d"),bg='white')
label2.grid(row=0,
            column=2,
            sticky="w")
prev_button2 = tk.Button(aproxim_panel, text="<", command=lambda: update_label(label2, False,graf_data,price_entry_vars),bg='white')
prev_button2.grid(row=0,
                  column=1,
                  sticky="w")
next_button2 = tk.Button(aproxim_panel, text=">", command=lambda: update_label(label2, True,graf_data,price_entry_vars),bg='white')
next_button2.grid(row=0,
                  column=3,
                  sticky="w")


inter_panel1= tk.Frame(Left_panel,bg='white')
inter_panel1.grid(row=1,
                 rowspan=2,
                 column=0,
                 columnspan=1)
int1=tk.IntVar()
fig,ax,canvas,yplots,config=Graficas.graf_inter("Inteconexión Francia",list(range(1,25)),
                                         -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación'],
                                         calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación'],
                                         aproxim_day['Generación_programada_PBF_Saldo_Francia'],int1,
                                         inter_panel1)

graf_data.append([fig,ax,canvas,yplots,config])
inter1_option_panel=tk.Frame(Left_panel,bg='white')
inter1_option_panel.grid(row=3,column=0)


int1_data= [lista for lista in graf_data if lista[1].get_title() =="Inteconexión Francia" ]

radiobtnexp1=tk.Radiobutton(inter1_option_panel,text="Día ejemplo",variable=int1,value=0,padx=5,bg='white',
                            command=lambda:Graficas.graf_int_option(int1_data[0][1],
                                                                    int1_data[0][2],
                                                                    -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación'],
                                                                    calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación'],
                                                                    aproxim_day['Generación_programada_PBF_Saldo_Francia']))
radiobtnexp1.grid(row=0,column=0)
radiobtnimp1=tk.Radiobutton(inter1_option_panel,text="Importación",variable=int1,value=1,padx=5,bg='white',
                            command=lambda: Graficas.graf_int_option(int1_data[0][1],
                                                                     int1_data[0][2],
                                                                     -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación'],
                                                                     calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación'],
                                                                     -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación']))


radiobtnimp1.grid(row=0,column=1)
radiobtnexp1=tk.Radiobutton(inter1_option_panel,text="Exportación",variable=int1,value=2,padx=5,bg='white',
                            command=lambda:Graficas.graf_int_option(int1_data[0][1],
                                                                    int1_data[0][2],
                                                                    -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación'],
                                                                    calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación'],
                                                                    calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación']))
radiobtnexp1.grid(row=0,column=2)



inter_panel2= tk.Frame(Left_panel,bg='white')
inter_panel2.grid(row=4,
                 rowspan=2,
                 column=0,
                 columnspan=1)
int2=tk.IntVar()

fig,ax,canvas,yplots,config=Graficas.graf_inter("Inteconexión Portugal",list(range(1,25)),
                                         -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_importación'],
                                         calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_exportación'],
                                         aproxim_day['Generación_programada_PBF_Saldo_Portugal'],int2,
                                         inter_panel2)
graf_data.append([fig,ax,canvas,yplots,config])
inter2_option_panel=tk.Frame(Left_panel,bg='white')
inter2_option_panel.grid(row=6,
                 column=0,
                 columnspan=1)

int2_data= [lista for lista in graf_data if lista[1].get_title() =="Inteconexión Portugal" ]
radiobtnexp2=tk.Radiobutton(inter2_option_panel,text="Día ejemplo",variable=int2,value=0,padx=5,bg='white',
                            command=lambda: Graficas.graf_int_option(int2_data[0][1],
                                                                     int2_data[0][2],
                                                                     -calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_importación'],
                                                                     calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_exportación'],
                                                                     aproxim_day['Generación_programada_PBF_Saldo_Portugal']))
radiobtnexp2.grid(row=0,column=0)
radiobtnimp2=tk.Radiobutton(inter2_option_panel,text="Importación",variable=int2,value=1,padx=5,bg='white',
                            command=lambda: Graficas.graf_int_option(int2_data[0][1],
                                                                     int2_data[0][2],
                                                                     -calculate_day[
                                                                         'Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_importación'],
                                                                     calculate_day[
                                                                         'Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_exportación'],
                                                                     -calculate_day[
                                                                         'Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_importación'])
                            )
radiobtnimp2.grid(row=0,column=1)
radiobtnexp2=tk.Radiobutton(inter2_option_panel,text="Exportación",variable=int2,value=2,padx=5,bg='white',
                            command=lambda: Graficas.graf_int_option(int2_data[0][1],
                                                                     int2_data[0][2],
                                                                     -calculate_day[
                                                                         'Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_importación'],
                                                                     calculate_day[
                                                                         'Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_exportación'],
                                                                     calculate_day[
                                                                         'Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_exportación'])
                            )
radiobtnexp2.grid(row=0,column=2)







Mid_panel=tk.Frame(Inicio,bg='white')
Mid_panel.grid(row=1,
               column=1)

price_graf= tk.Frame(Mid_panel,bg='white')
price_graf.grid(row=0,
                 column=0,
                 rowspan=3,
                 sticky="ns")

fig,ax,canvas,yplots,config=Graficas.graf_price("Precio",list(range(1,25)),
                                      [],
                                       #[calculate_day['Previsión_de_la_producción_eólica_peninsular']],
                                      [aproxim_day['Precio']],
                                       price_graf)
graf_data.append([fig,ax,canvas,yplots,config])

price_panel=tk.Frame(Mid_panel,bg='white',width=860)
price_panel.grid(row=3,
                 column=0,sticky="ew")

price_vars = []
price_entry_vars=[]

for columna in range(24 if len(price)==0 else len(price)):  # Supongamos que queremos 24 columnas
    label_price = tk.Label(price_panel, text=int(0 if len(price)==0 else price[columna]),width=4,font=("Arial",10),bg='white',padx=0,bd=0)
    label_price.grid(row=0, column=columna)
    price_vars.append(label_price.cget("text"))
    price_entry_vars.append(label_price)
label_unity=tk.Label(price_panel,text="Eur/MWh",font=("Arial",10),width=7,bg='white',padx=0)
label_unity.grid(row=0, column=len(price),sticky="w")


Add_Vol_Frame=tk.Frame(Mid_panel,width=860)
Add_Vol_Frame.grid(row=4,
                   column=0)
Add_Vol_Label=tk.Label(Add_Vol_Frame,text="Añadir Volumen(MWh)")

Add_Vol_Label.grid(row=0,
                   column=0,
                   columnspan = 24 if len(price)==0 else len(price))


#Add_Vol_entry_fila_vars = []
Add_Vol_fila_vars = []
Add_Vol_entry_vars=[]
entry_vars = []
for columna in range(24 if len(price)==0 else len(price)):  # Supongamos que queremos 24 columnas
    Var=tk.IntVar()
    Add_Vol_Entry = tk.Entry(Add_Vol_Frame, textvariable=Var,width=5,bg='white')
    Add_Vol_Entry.grid(row=1, column=columna)
    Add_Vol_fila_vars.append(Var)
    Add_Vol_entry_vars.append(Add_Vol_Entry)

results=tk.Frame(Mid_panel,width=860,height=240,bg='white',bd=2)
results.grid(row=5,
             column=0,
             sticky="ns")



# Agregar un scrollbar al frame

scrollbar = tk.Scrollbar(results,orient="vertical",bg='white')
scrollbar.grid(row=0, column=0,sticky="ns")

price_canvas = tk.Canvas(results,width=860, height=280, yscrollcommand=scrollbar.set,bg='white')
price_canvas.grid(row=0, column=1,sticky="ns")
scrollbar.config(command=price_canvas.yview)

inner_frame = tk.Frame(price_canvas,bg='white')
price_canvas.create_window((0, 1), window=inner_frame, anchor="s")

# Configurar el lienzo para ajustar su tamaño al contenido
inner_frame.bind("<Configure>", lambda event: price_canvas.configure(scrollregion=price_canvas.bbox("all")))



Average_panel=tk.Frame(Mid_panel)
Average_panel.grid(row=6,column=0)

Add_Vol_Label=tk.Label(Average_panel,text="Promedio")

Add_Vol_Label.grid(row=0,
                   column=0,
                   columnspan = 24 if len(price)==0 else len(price))


#Add_Vol_entry_fila_vars = []
Average_fila_vars = []
Average_entry_vars=[]

for columna in range(24 if len(price)==0 else len(price)):  # Supongamos que queremos 24 columnas
    Var=tk.DoubleVar()
    Average_Entry = tk.Entry(Average_panel, textvariable=Var,width=5)
    Average_Entry.grid(row=1, column=columna)
    Average_fila_vars.append(Var)
    Average_entry_vars.append(Average_Entry)

index=0
while graf_data[index][1].get_title() != "Precio" and index < len(graf_data):
    index += 1
graf_data[index][3].append([Average_fila_vars, "Av"])

mid_btn_frame=tk.Frame(Mid_panel)
mid_btn_frame.grid(row=7,column=0,sticky="se")

mid_btn1=tk.Button(mid_btn_frame,text="Aproximar",command=Aproxim_row)
mid_btn1.grid(row=0,column=0,sticky="w")
mid_btn2=tk.Button(mid_btn_frame,text="Promediar",command=Average)
mid_btn2.grid(row=0,column=1,sticky="w")





#Panel derech
right_panel = tk.Frame(Inicio,bg="white")
right_panel.grid(row=1,
                 rowspan=8,
                 column=2,
                 sticky="w")
fig,ax,canvas,yplots,config=Graficas.graf_dif("Previsión Eólica",list(range(1,25)),
                                       [calculate_day['Previsión_de_la_producción_eólica_peninsular']],[aproxim_day['Previsión_de_la_producción_eólica_peninsular']],
                                       right_panel)
graf_data.append([fig,ax,canvas,yplots,config])
fig,ax,canvas,yplots,config=Graficas.graf_dif("Previsión Solar",list(range(1,25)),
                                       [calculate_day['Generación_prevista_Solar']],
                                       [aproxim_day['Generación_prevista_Solar']],
                                       right_panel)
graf_data.append([fig,ax,canvas,yplots,config])

fig,ax,canvas,yplots,config=Graficas.graf_dif("Previsión Demanda",list(range(1,25)),
                                       [calculate_day['Previsión_diaria_de_la_demanda_eléctrica_peninsular']],
                                       [aproxim_day['Previsión_diaria_de_la_demanda_eléctrica_peninsular']],
                                       right_panel)
graf_data.append([fig,ax,canvas,yplots,config])



Inicio.mainloop()
