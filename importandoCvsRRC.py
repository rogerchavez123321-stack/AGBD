import pandas as pd 

df=pd.read_csv('CLEAN_FIFA17_official_data-RRC .csv')

print("OKEY! archivo descargado correctamente") 

print(df.head())

#resultado = df[df['Year_Joined'] == 2022]

#print(resultado) 

YearsJ = df['Year_Joined']

YearJ = df['Year_Joined'].sum()

print(f"total de jugadores ingresados hasta ahora es: {YearJ}")