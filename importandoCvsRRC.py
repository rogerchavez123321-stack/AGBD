import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv('CLEAN_FIFA17_official_data-RRC .csv')

print("OKEY! archivo descargado correctamente") 

print(df.head())

#resultado = df[df['Year_Joined'] == 2022]

#print(resultado) 

#YearsJ = df['Year_Joined']

#YearJ = df['Year_Joined'].sum()

#print(f"total de jugadores ingresados hasta ahora es: {YearJ}")

print("--- Analisis Avanzado de Datos ---")

filtro_avanzado = df['Name'].str.startswith('R', na =False) 
df_filtrado = df[filtro_avanzado]

sumo_Age = df_filtrado['Age'].sum()

print("--- Reporte de Edad ---")
print(f"Suma de Edades Total: {sumo_Age:.2f}\n")

if Default_limite_alto := (sumo_Age > 20000):
   print("!Alerta¡ Las Edades superan el limite de edades totales establecidas")
   print("Requiere revision inmediata")
elif sumo_Age < 5000:
   print("Aviso: No supera el minimo de edad necesaria total de jugadores")
   print("Monitorear Cantidad de jugadores")
else:
   print("Edad Total estables")



#-------------------------------------------------
#Grafico de barras usando toda DF
#-------------------------------------------------

print("\n[Generando GRAFICO de Barras]")
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10,6))
sns.barplot(
   data=df,
   x="Age",
   y="Overall",
   estimator=sum,
   errorbar=None,
   palette="viridis",





)
plt.title("Comparativa de mercado por tipo de Jugador")
plt.xticks(rotation=20)


#Guardo grafico generado
plt.savefig("grafico_barra.png", dpi=300)
plt.close()

print ("\n !Hecho¡ Los graficos se guardaron correctamente en tu carpeta")


plt.tight_Layout() 
plt.show()