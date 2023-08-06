#tres formas de tener una serie de datos entre dos fechas o de una fecha concreta
import pandas as pd
import datetime
n_datos1=df[(df["datetime"]>="2023-02-07 00:00:00") & (df["datetime"]<"2023-02-08 00:00:00")]

n_datos2=df.iloc[(df['datetime'].dt.date == fecha_buscada).values]

n_datos3=df.loc[(df['datetime'] >= "2023-02-07 00:00:00") & (df['datetime'] < "2023-02-08 00:00:00")]

#cambiar el formato de la fecha. Hay una condición format en la funcion to_datetime pero no siempre me ha funcionado.
df["fecha"]=df["fecha"].dt.strftime("%Y-%m-%d %H")
df["fecha"]=pd.to_datetime(df["fecha"])
#cositas con padas dataframes
n_dias = df.groupby("days", as_index=False)[result["indicator"]["name"]].count()  # agrupo datos por días
n_dias = n_dias[n_dias[result["indicator"]["name"]] != 24]  # selecciono los días que no tengan 24 datos (quizá debería cambiarse por un <24)


