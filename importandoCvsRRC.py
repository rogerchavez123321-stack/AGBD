import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('CLEAN_FIFA17_official_data-RRC .csv')

print("OKEY! archivo descargado correctamente")

print(df.head())


print("\n" + "=" * 60)
print("EJERCICIO 1 - Filas y columnas de la tabla")
print("=" * 60)

filas, columnas = df.shape
print(f"La tabla contiene {filas} filas y {columnas} columnas")


print("\n" + "=" * 60)
print("EJERCICIO 2 - Filtro por coincidencia exacta")
print("=" * 60)

filtro_exacto = df['Nationality'] == 'Argentina'
df_exacto = df[filtro_exacto]

print(f"Jugadores con Nationality == 'Argentina': {len(df_exacto)} filas")
print(df_exacto[['Name', 'Nationality', 'Overall']].head())

print("--- Analisis Avanzado de Datos ---")

filtro_avanzado = df['Name'].str.startswith('R', na=False)
df_filtrado = df[filtro_avanzado]

print("\n" + "=" * 60)
print("EJERCICIO 4 - Seleccion de columnas clave")
print("=" * 60)

columnas_clave_ej4 = df_filtrado[['Name', 'Overall']]
print(columnas_clave_ej4.head())

print("\n" + "=" * 60)
print("EJERCICIO 5 - Agrupacion y resumen con groupby()")
print("=" * 60)

resumen_nacionalidad = (
    df.groupby('Nationality')['Value(£)'].sum().sort_values(ascending=False)
)
print(resumen_nacionalidad.head(10))

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

# Grafico de barras usando toda DF

print("\n[Generando GRAFICO de Barras]")
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
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

plt.savefig("grafico_barra.png", dpi=300)
plt.close()

# EJERCICIO 8 - Grafico de Torta (matplotlib puro)

print("\n" + "=" * 60)
print("EJERCICIO 8 - Grafico de Torta")
print("=" * 60)

top5_nacionalidad = resumen_nacionalidad.nlargest(5)
print(top5_nacionalidad)

plt.figure(figsize=(8, 8))
plt.pie(
    top5_nacionalidad.values,
    labels=top5_nacionalidad.index,
    autopct='%1.1f%%',
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
)
plt.title("Top 5 Nacionalidades por Valor de Mercado Total")

plt.savefig("reporte_torta.png", dpi=300)
plt.close()

print("\n!Hecho¡ Torta guardada como 'reporte_torta.png'")

# EJERCICIO 9 - .loc[] con doble condicion

print("\n" + "=" * 60)
print("EJERCICIO 9 - .loc[] Doble condicion")
print("=" * 60)

condicion_extra = df['Overall'] > 80

resultado_ej9 = df.loc[
    filtro_avanzado & condicion_extra,
    ['Name', 'Nationality', 'Overall']
]

print(resultado_ej9)
print(f"\nFilas seleccionadas: {len(resultado_ej9)}")

# EJERCICIO 10 - Deteccion y manejo de valores nulos

print("\n" + "=" * 60)
print("EJERCICIO 10 - Valores nulos")
print("=" * 60)

print("Nulos por columna (solo columnas con nulos):")
nulos_originales = df.isnull().sum()
print(nulos_originales[nulos_originales > 0])

df_con_nulos = df.copy()
df_con_nulos.loc[[0, 3, 7], 'Value(£)'] = None

print("\nNulos en 'Value(£)' despues de modificar:", df_con_nulos['Value(£)'].isnull().sum())

df_sin_nulos = df_con_nulos.dropna(subset=['Value(£)'])

media_valor = df_con_nulos['Value(£)'].mean()
df_rellenado = df_con_nulos.fillna({'Value(£)': round(media_valor, 2)})

print(f"\nOriginal: {len(df_con_nulos)} filas")
print(f"Con dropna: {len(df_sin_nulos)} filas (se eliminaron filas con nulos)")
print(f"Con fillna: {len(df_rellenado)} filas (se rellenaron los huecos, no se pierde nada)")

# EJERCICIO 11 - Grafico de Lineas con anotacion del maximo

print("\n" + "=" * 60)
print("EJERCICIO 11 - Grafico de Lineas")
print("=" * 60)

agrupado_lineas = (
    df.groupby('Nationality')['Overall'].mean().sort_values(ascending=False).head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    agrupado_lineas.index, agrupado_lineas.values,
    marker='o', color='#2E75B6', linewidth=2, markersize=8,
)

idx_max = agrupado_lineas.idxmax()
val_max = agrupado_lineas.max()
ax.annotate(
    f'Maximo: {val_max:,.1f}',
    xy=(idx_max, val_max),
    xytext=(0.5, val_max * 0.97),
    arrowprops=dict(arrowstyle='->', color='red'),
    fontsize=11, color='red', fontweight='bold',
)

ax.set_title('Overall promedio por Nacionalidad (Top 10)', fontsize=14, fontweight='bold')
ax.set_xlabel('Nacionalidad')
ax.set_ylabel('Overall promedio')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("grafico_lineas.png", dpi=150)
plt.close()

print("\n!Hecho¡ Grafico de lineas guardado como 'grafico_lineas.png'")

# EJERCICIO 12 query() filtros escritos como texto

print("\n" + "=" * 60)
print("EJERCICIO 12 - .query()")
print("=" * 60)

resultado_original = df[filtro_avanzado]

letra_inicial = 'R'
resultado_query = df.query(
    "Name.str.startswith(@letra_inicial, na=False)",
    engine='python'
)

print(f"Con corchetes ({len(resultado_original)} filas):")
print(resultado_original[['Name', 'Age', 'Nationality']].head())

print(f"\nCon .query() ({len(resultado_query)} filas):")
print(resultado_query[['Name', 'Age', 'Nationality']].head())

print('\n¿Son iguales?', resultado_original.equals(resultado_query))

# EJERCICIO 13 isin() incluir y excluir categorias
print("\n" + "=" * 60)
print("EJERCICIO 13 - .isin() y ~")
print("=" * 60)

categorias_elegidas = ['Argentina', 'Brazil', 'Spain']

df_incluidos = df[df['Nationality'].isin(categorias_elegidas)]
df_excluidos = df[~df['Nationality'].isin(categorias_elegidas)]

print(f"Filas incluidas ({len(df_incluidos)}):")
print(df_incluidos[['Name', 'Nationality']].head())

print(f"\nFilas excluidas ({len(df_excluidos)}):")
print(df_excluidos[['Name', 'Nationality']].head())

total = len(df)
suma = len(df_incluidos) + len(df_excluidos)
print(f"\nTotal original: {total} | Incluidos + Excluidos: {suma}")
print(f"¿Coinciden? {total == suma}")

# EJERCICIO 14 value_counts() .unique() .nunique()

print("\n" + "=" * 60)
print("EJERCICIO 14 - value_counts / unique / nunique")
print("=" * 60)

print('=== DataFrame completo ===')
print(df['Nationality'].value_counts())
print('Valores únicos:', df['Nationality'].unique())
print('Cantidad de categorías:', df['Nationality'].nunique())
print('Porcentajes:')
print((df['Nationality'].value_counts(normalize=True) * 100).round(1))

df_filtrado = df[filtro_avanzado]
print('\n=== DataFrame filtrado (Name empieza con R) ===')
print(df_filtrado['Nationality'].value_counts())
print('Valores únicos:', df_filtrado['Nationality'].unique())
print('Cantidad de categorías:', df_filtrado['Nationality'].nunique())
print('Porcentajes:')
print((df_filtrado['Nationality'].value_counts(normalize=True) * 100).round(1))

# EJERCICIO 15 -- Exportar a CSV + Heatmap de correlacion

print("\n" + "=" * 60)
print("EJERCICIO 15 - Exportar CSV + Heatmap")
print("=" * 60)

df_filtrado = df[filtro_avanzado]
df_filtrado.to_csv('mi_resultado_filtrado.csv', index=False)
print(f'Archivo exportado: {len(df_filtrado)} filas guardadas.')

correlacion = df.corr(numeric_only=True)
print('\nMatriz de correlación (recorte):')
print(correlacion.round(2).iloc[:6, :6])

columnas_clave = [
    'Age', 'Overall', 'Potential', 'Value(£)', 'Wage(£)',
    'Acceleration', 'SprintSpeed', 'Strength', 'Stamina',
    'ShortPassing', 'Dribbling', 'Finishing'
]
correlacion_clave = df[columnas_clave].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    correlacion_clave,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    linewidths=0.5,
    vmin=-1, vmax=1
)
plt.title('Correlación entre variables — FIFA17', fontweight='bold')
plt.tight_layout()
plt.savefig('heatmap_mi_dataset.png', dpi=150)
plt.close()

print("\n!Hecho¡ Heatmap guardado como 'heatmap_mi_dataset.png'")

mask = np.triu(np.ones(correlacion_clave.shape), k=0).astype(bool)
correlacion_sin_diag = correlacion_clave.where(~mask)
par_max = correlacion_sin_diag.stack().idxmax()
par_min = correlacion_sin_diag.stack().idxmin()
print(f'\nPar más correlacionado: {par_max[0]} ↔ {par_max[1]} '
      f'({correlacion_sin_diag.loc[par_max]:.2f})')
print(f'Par menos correlacionado: {par_min[0]} ↔ {par_min[1]} '
      f'({correlacion_sin_diag.loc[par_min]:.2f})')

print("\nProceso completo: carga -> exploración -> filtrado -> "
      "agrupación -> visualización -> exportación. listo")