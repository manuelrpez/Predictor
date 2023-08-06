import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def graf_dif(titulo,xdata, ycalc,yaprox, frame):
    # Crear figura de Matplotlib y ejes para el gráfico
    fig, ax = plt.subplots(figsize=(5, 3), dpi=80)
    fig.set_facecolor('none')
    yplots=[]
    # Gráfico 1
    for y in ycalc:
        yplots.append([y.name,"cal"])
        if len(y)>=len(xdata):
            ax.plot(xdata, y.values.tolist()[:len(xdata)],linestyle=":",label="Previsión",color="orange")
    for y in yaprox:
        yplots.append([y.name,"aprox"])
        if len(y)>=len(xdata):
            ax.plot(xdata, y.values.tolist()[:len(xdata)],label="Referencia",color="blue")

    ax.set_xlim(min(xdata), max(xdata))
    ax.set_ylabel("MWh", labelpad=-20, y=1, rotation=0)
    ax.legend()

    ax.set_title(f"{titulo}")
    # Crear lienzo de dibujo utilizando FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    config = [titulo]
    plt.subplots_adjust(left=.1, right=.97, bottom=.1, top=.90)
    return fig,ax,canvas,yplots,config

def graf_price(titulo,xdata, ycalc,yaprox, frame):

    fig, ax = plt.subplots(figsize=(7, 3), dpi=125)
    ax.set_ylabel("Eur/MWh",labelpad=-10,y=1,rotation=0)
    fig.set_facecolor('none')
    yplots = []

    for y in ycalc:
        yplots.append([y.name, "cal"])
        if len(y) >= len(xdata):
            ax.plot(xdata, y.values.tolist()[:len(xdata)], linestyle=":",color="blue")
    for y in yaprox:
        yplots.append([y.name, "aprox"])
        if len(y) >= len(xdata):
            ax.plot(xdata, y.values.tolist()[:len(xdata)],color="blue",label="Referencia")
    ax.set_xlim(min(xdata),max(xdata))
    ax.legend()
    ax.set_title(f"{titulo}")
    config=[titulo]
    plt.subplots_adjust(left=.1, right=.98, bottom=.1, top=.90)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


    return fig, ax, canvas, yplots,config
def graf_inter(titulo,xdata, imp,exp,bars,variable, frame):
    # Crear figura de Matplotlib y ejes para el gráfico
    fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
    fig.set_facecolor("white")
    yplots = []
    yplots.append([bars.name,"bar", "aprox"])
    yplots.append([imp.name,"bar", "calimp"])
    yplots.append([exp.name,"bar", "calexp"])
    if len(bars) >= len(xdata):
        ax.bar(xdata,bars.values.tolist()[:len(xdata)],label="Referencia",color="blue")
    if len(imp) >= len(xdata):
        ax.plot(xdata, imp.values.tolist()[:len(xdata)])
    if len(exp) >= len(xdata):
        ax.plot(xdata, exp.values.tolist()[:len(xdata)])
    ax.set_xlim(min(xdata), max(xdata))
    ax.legend()
    ax.set_title(f"{titulo}")
    plt.subplots_adjust(left=.13, right=.99, bottom=.1, top=.90)
    # Crear lienzo de dibujo utilizando FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    config = [titulo,variable]
    return fig, ax, canvas, yplots,config

def graf_dwnl(nombre,datos,frame,list_data):

    if len(list_data)==0:
        fig, ax = plt.subplots(figsize=(6, 3), dpi=130)
        fig.set_facecolor('white')
        xdata=list(range(len(datos)))
        ax.plot(xdata, datos.values.tolist()[:len(xdata)])
        ax.set_xlim(min(xdata), max(xdata))

        ax.set_title(f"{nombre}")
        plt.subplots_adjust(left=.1, right=.98, bottom=.1, top=.90)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        ax=list_data[1]
        fig=list_data[0]
        canvas=list_data[2]
        ax.clear()
        xdata = list(range(len(datos)))
        ax.plot(xdata, datos.values.tolist()[:len(xdata)])
        ax.set_title(f"{nombre}")
        ax.set_xlim(min(xdata), max(xdata))
        canvas.draw()

    return fig,ax,canvas

def graf_reload(graf_datas,calculate_day,aproxim_day):

    for graf_data in graf_datas:#por cada uno de los gráficos creados a los que se la hayan guardado los datos
        fig = graf_data[0]
        ax=graf_data[1]
        canvas=graf_data[2]
        ydata=graf_data[3]
        titulo=ax.get_title()
        xdata=list(range(1,25))
        ax.clear()
        ax.set_title(f"{titulo}")
        ax.set_xlim(min(xdata), max(xdata))
        if titulo=="Precio":
            ax.set_ylabel("Eur/MWh", labelpad=-10, y=1, rotation=0)
        else:
            ax.set_ylabel("MWh", labelpad=-20, y=1, rotation=0)
        for y in ydata:
            if y[1]=="cal":
                if len(calculate_day[y[0]]) >= len(xdata):
                    ax.plot(xdata, calculate_day[y[0]].values.tolist()[:len(xdata)],linestyle=":",label="Previsión",color="orange")
                    ax.set()
            elif y[1]=="aprox":
                if len(aproxim_day[y[0]]) >= len(xdata):
                    ax.plot(xdata, aproxim_day[y[0]].values.tolist()[:len(xdata)],label="Referencia",color="blue")
            elif y[1]=="bar":
                if y[2] == "calimp":
                    if len(calculate_day[y[0]]) >= len(xdata):
                        ax.plot(xdata, (-calculate_day[y[0]]).values.tolist()[:len(xdata)])
                if y[2] == "calexp":
                    if len(calculate_day[y[0]]) >= len(xdata):
                        ax.plot(xdata, calculate_day[y[0]].values.tolist()[:len(xdata)])
                if y[2] == "aprox":
                    graf_data[4][1].set(0)
                    if len(aproxim_day[y[0]]) >= len(xdata):
                        ax.bar(xdata, aproxim_day[y[0]].values.tolist()[:len(xdata)],label="Referencia",color="blue")
            elif y[1]=="PV":
                if y[0][len(y[0]) - 1].get():
                    values = []
                    for elem in range(len(xdata)):
                        values.append(y[0][elem].get())
                    ax.plot(xdata, values, linestyle=":")
            elif y[1]=="Av":

                values = []
                for elem in range(len(xdata)):
                    values.append(y[0][elem].get())
                if sum(values)!=0:
                    ax.plot(xdata, values, linestyle="solid",color="orange",label="Promedio")

        ax.legend()
        canvas.draw()
        #canvas.itemconfig()
        #canvas.get_tk_widget().pack()
    pass
def graf_int_option(ax,canvas, imp,exp,bars):
    titulo = ax.get_title()
    xdata = list(range(1, 25))
    ax.clear()
    ax.set_title(f"{titulo}")
    ax.set_xlim(min(xdata), max(xdata))
    if len(bars) >= len(xdata):
        ax.bar(xdata,bars.values.tolist()[:len(xdata)],label="Referencia",color="blue")
    if len(imp) >= len(xdata):
        ax.plot(xdata, imp.values.tolist()[:len(xdata)])
    if len(exp) >= len(xdata):
        ax.plot(xdata, exp.values.tolist()[:len(xdata)])
    ax.legend()
    canvas.draw()
def graf_price_option(precio,graf_data):

    index=0
    while graf_data[index][1].get_title() != "Precio" and index<len(graf_data):
        index +=1
    ax=graf_data[index][1]
    canvas = graf_data[index][2]
    ydata = graf_data[index][3]
    titulo = ax.get_title()
    xdata = list(range(1, 25))
    ax.clear()
    ax.set_title(f"{graf_data[index][1].get_title()}")
    ax.set_xlim(min(xdata), max(xdata))
    ax.set_ylabel("Eur/MWh", labelpad=-10, y=1, rotation=0)
    for y in ydata:
        if y[0]=='Precio':
            if len(precio) >= len(xdata):
                ax.plot(xdata,precio.values.tolist()[:len(xdata)],label="Referencia")
        else:
            if y[0][len(y[0])-1].get():
                values=[]
                for elem in range(len(xdata)):
                    values.append(y[0][elem].get())
                if y[1]=="PV":
                    ax.plot(xdata,values,linestyle=":",color="blue")
                elif y[1]=="Av":
                    ax.plot(xdata, values, linestyle="solid",color="orange",label="Promedio")

    ax.set_title(f"{titulo}")
    ax.legend()
    canvas.draw()

if __name__=="__main__":
    grafico1([1,2,3],[1,2,3])


