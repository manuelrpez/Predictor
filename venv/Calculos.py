#Aqui hay popurri de calculos que quiero hacer con los datos que hay en base de datos.
#No voy a meterme aqui en BBDD solo con pandas
import numpy as np
import pandas as pd
import Descargas
import os
import datetime


def BS_curves(df, hour):

    df = df[df["Pais"] != "PT"]

    # dt con las ofertas casadas
    dflock_buy = df.loc[(df["Hora"] == hour) & (df["Ofertada_OC"] == "C") & (df["Tipo_Oferta"] == "C"), (
        "Precio_CompraVenta", "Energía_CompraVenta", "Ofertada_OC","Pais")].reset_index(drop=True)
    dflock_sell = df.loc[(df["Hora"] == hour) & (df["Ofertada_OC"] == "C") & (df["Tipo_Oferta"] == "V"), (
        "Precio_CompraVenta", "Energía_CompraVenta", "Ofertada_OC","Pais")].reset_index(drop=True)

    #precios a los que casó
    lower_price = dflock_buy.iloc[dflock_buy["Precio_CompraVenta"].idxmin()][0]
    #dflock_sell["Precio_CompraVenta"].max()
    higher_price = dflock_sell.iloc[dflock_sell["Precio_CompraVenta"].idxmax()][0]

    #elimino la ultima oferta que casó
    dflock_buy = dflock_buy.drop(index=len(dflock_buy)-1)
    dflock_sell = dflock_sell.drop(index=len(dflock_sell) - 1)

    #hago un df con las ofertas al mismo precio para eliminarlas de las ofertas
    dflock_sell_max = dflock_sell.loc[dflock_sell["Precio_CompraVenta"] == higher_price].reset_index(drop=True)
    dflock_buy_min = dflock_buy.loc[dflock_buy["Precio_CompraVenta"] == lower_price].reset_index(drop=True)

    #dt con las ofertas
    dfoffer_buy = df.loc[(df["Hora"] == hour) & (df["Ofertada_OC"] == "O") & (df["Tipo_Oferta"] == "C") & (
            df["Precio_CompraVenta"] <= lower_price), (
                             "Precio_CompraVenta", "Energía_CompraVenta", "Ofertada_OC","Pais")].reset_index(drop=True)
    dfoffer_sell = df.loc[(df["Hora"] == hour) & (df["Ofertada_OC"] == "O") & (df["Tipo_Oferta"] == "V") & (
            df["Precio_CompraVenta"] >= higher_price), (
                              "Precio_CompraVenta", "Energía_CompraVenta", "Ofertada_OC","Pais")].reset_index(drop=True)

    #elimino las ofertas con el precio max y min para quitar duplicados
    for i in range(len(dflock_sell_max)):
        precio=dflock_sell_max.loc[i][0]
        vol=dflock_sell_max.loc[i][1]

        dfoffer_sell = dfoffer_sell.drop(dfoffer_sell[(dfoffer_sell["Precio_CompraVenta"] == precio) & (
                    dfoffer_sell["Energía_CompraVenta"] == vol)].index)


    for i in range(len(dflock_buy_min)):
        precio=dflock_buy_min.loc[i][0]
        vol=dflock_buy_min.loc[i][1]

        dfoffer_buy = dfoffer_buy.drop(dfoffer_buy[(dfoffer_buy["Precio_CompraVenta"] == precio) & (
                dfoffer_buy["Energía_CompraVenta"] == vol)].index)



    #dfoffer_sell = dfoffer_sell.drop(dflock_sell_max[(dflock_sell_max["Precio_CompraVenta"] == 1) & (dflock_sell_max["Energía_CompraVenta"] == 2)].index)


    df_buy = pd.concat([dfoffer_buy, dflock_buy]).sort_values("Precio_CompraVenta", ascending=False).reset_index(
        drop=True)
    df_sell = pd.concat([dfoffer_sell, dflock_sell]).sort_values("Precio_CompraVenta").reset_index(drop=True)

    return df_buy,df_sell

def hourprice(df_buy,df_sell):
    isell = 0
    ibuy = 0
    sellvol = df_sell.iloc[isell][1]
    buyvol = df_buy.iloc[ibuy][1]

    sellprice = df_sell.iloc[isell][0]
    buyprice = df_buy.iloc[ibuy][0]

    while buyprice >= sellprice:

        if sellvol <= buyvol:

            isell += 1
            sellprice = df_sell.iloc[isell][0]
            sellvol += df_sell.iloc[isell][1]
            index = 1
            #print(sellprice,sellvol)
        else:

            ibuy += 1
            buyprice = df_buy.iloc[ibuy][0]
            buyvol += df_buy.iloc[ibuy][1]

            index = 0
            #print(buyprice,buyvol)

    if index == 1:
        price = buyprice
        vol = sellvol - df_sell.iloc[isell][1]

    if index == 0:
        price = sellprice
        vol = buyvol - df_buy.iloc[ibuy][1]


    country=df_buy.iloc[ibuy][3]

    return price,vol,country

def dayPV(BBDD,tabla,fecha):
    PV=pd.DataFrame(columns=["Hora","Precio","Volumen","Pais"],index=range(0,24))
    df = Descargas.cargar_datosOMIE(Descargas.createBD(os.getcwd(), BBDD), tabla, fecha)
    for hour in range(1,25):
        df_buy, df_sell=BS_curves(df,hour)
        price,vol,country=hourprice(df_buy, df_sell)
        PV.iloc[hour-1]=(hour,price,vol,country)
    return PV



def aprox_dayPV(BBDD,tabla,fecha,aproxim_day,calculate_day,int1,int2,vol_añadido):

    vol_add=[]
    if len(vol_añadido)>0:
        for elem in vol_añadido:
            vol_add.append(-elem.get())
    else:
        vol_add=[0]*24
    vol_add = pd.DataFrame(vol_add, columns=['Volumen añadido'])
    PV=pd.DataFrame(columns=["Hora","Precio","Volumen","Pais"],index=range(0,24))
    df = Descargas.cargar_datosOMIE(Descargas.createBD(os.getcwd(), BBDD), tabla, fecha)
    volum = diff_tot(calculate_day,aproxim_day,int1,int2,vol_add)
    for hour in range(1,25):
        df_buy, df_sell=BS_curves(df,hour)
        df_sell=add_vol(df_sell,volum[hour-1])
        price,vol,country=hourprice(df_buy, df_sell)
        PV.iloc[hour-1]=(hour,price,vol,country)
    return PV

def Vol_ESIOS(pbf):
    pbf = pbf.fillna(0)
    Demanda_calculated = (pbf['Generación_programada_PBF_Nuclear'] - pbf['Programa_bilateral_PBF_Nuclear']
                         + pbf['Generación_programada_PBF_Carbón'] - pbf['Programa_bilateral_PBF_Carbón']
                         + pbf['Programa_bilateral_PBF_Genéricas_bajar']
                         + pbf['Generación_programada_PBF_Turbinación_bombeo']
                         + pbf['Generación_programada_PBF_UGH__no_UGH'] - pbf[
                             'Programa_bilateral_PBF_Hidráulica_no_UGH'] -
                         pbf['Programa_bilateral_PBF_Hidráulica_UGH']
                         + pbf['Generación_programada_PBF_Cogeneración'] - pbf[
                             'Programa_bilateral_PBF_Gas_Natural_Cogeneración']
                         + pbf['Generación_programada_PBF_Eólica'] - pbf['Programa_bilateral_PBF_Eólica_terrestre']
                         + pbf['Generación_programada_PBF_otras_renovables'] - pbf[
                             'Programa_bilateral_PBF_Otras_renovables']
                         + pbf['Generación_programada_PBF_Solar_fotovoltaica'] + pbf[
                             'Generación_programada_PBF_Solar_térmica'] - pbf[
                             'Programa_bilateral_PBF_Solar_fotovoltaica']
                         + pbf['Generación_programada_PBF_Residuos']
                         + pbf['Generación_programada_PBF_Ciclo_combinado']
                         + pbf["Demanda_Portugal"]
                         ).reset_index(drop=True)
    return Demanda_calculated


def diff(prev0,prev1):

    prev0 =prev0.replace(0,np.nan)
    prev1 = prev1.replace(0, np.nan)

    diff = prev1.fillna(0)-prev0.fillna(0)

    diff=diff.dropna()
    return diff

def dif_inter(aprox,imp,exp,int1):

    if int1.get()==0:
        vol_int=aprox
    elif int1.get()==1:
        vol_int=-imp
    else:
        vol_int=exp
    df_min = pd.DataFrame.min(pd.concat([vol_int, exp], axis=1), axis=1)
    df_max= pd.DataFrame.max(pd.concat([df_min, -imp], axis=1), axis=1)
    dif_inter=df_max-aprox
    dif_inter=(-dif_inter).dropna()
    return dif_inter
def dif_infl():
    pass
def diff_tot(calculate_day,aproxim_day,int1,int2,vol_add):
    eol=diff( calculate_day['Previsión_de_la_producción_eólica_peninsular'],
              aproxim_day['Previsión_de_la_producción_eólica_peninsular'])
    sol=diff(calculate_day['Generación_prevista_Solar'],
             aproxim_day['Generación_prevista_Solar'])

    dem=diff(calculate_day ["Previsión_diaria_de_la_demanda_eléctrica_peninsular"],
             aproxim_day["Previsión_diaria_de_la_demanda_eléctrica_peninsular"])

    port=dif_inter(aproxim_day['Generación_programada_PBF_Saldo_Portugal'],
                   calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_importación'],
                   calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Portugal_exportación'],
                   int2)

    fran=dif_inter(aproxim_day['Generación_programada_PBF_Saldo_Francia'],
                   calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_importación'],
                   calculate_day['Capacidad_de_intercambio_comercial_en_la_interconexión_con_Francia_exportación'],
                   int1)

    vol=sol+eol-dem+vol_add['Volumen añadido']+port+fran

    return vol
def add_vol(df_sell,vol):

    df_sell.loc[len(df_sell)]=[df_sell['Precio_CompraVenta'].min(),vol,"N",df_sell.iloc[0][3]]
    df_sell=df_sell.sort_values("Precio_CompraVenta").reset_index(drop=True)
    return df_sell
if __name__=="__main__":
    BBDD = "OMIE"
    fecha = "2023-06-13"
    tabla = "CurvasOfertaDemanda"

    PV_real=dayPV(BBDD,tabla,"2023-07-11")








