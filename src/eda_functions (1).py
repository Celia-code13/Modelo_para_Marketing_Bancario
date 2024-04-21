import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# uso:

#  import eda_functions                                    importar las funciones (como importariais numpy o pandas) 

# llamar a las funciones con el prefijo eda_functions. (eda_functions.df_info(df))
# eda_functions.multi_boxplot(df, ['columna1', 'columna2', 'columna3'], 1, 3) ejemplo de uso
# eda_functions.multi_countplot(df, ['columna1', 'columna2', 'columna3'], 1, 3) ejemplo de uso
# columnas_categoricas = ['a', 'b', 'c', 'd'] ---------> eda_functions.multi_histplot(df, columnas_categoricas, 2, 2) ejemplo de uso                                  

#####################################################################################################################


# Proporciona un resumen del DataFrame: valores únicos, nulos, tipos de datos, etc. parametros: el dataframe a analizar.
def df_info(df):
    df_info = pd.DataFrame({
        'nunique': df.nunique(),
        'nulls': df.isnull().sum(),
        'percent_nulls' : df.isnull().mean()*100,
        'Dtype': df.dtypes,
        'non_null': df.count(),
        'total_values': len(df)  
    })
    types_counter = df_info['Dtype'].value_counts()
    duplicated = df.duplicated().sum()
    display(df_info, types_counter)
    print(f'El dataframe tiene {df.shape[0]} filas y {df.shape[1]} columnas')
    print(f'Hay {duplicated} valores duplicados')

    #####################################################################################################################

# Crea múltiples boxplots para visualizar la distribución de varias columnas. 
# parametros: (el dataframe, la lista de columnas, nºfilas del grafico, nºcolumnas del grafico, tamaño de la figura (fig_size)).

def multi_boxplot(dataframe, columns_list, n_rows, n_cols, fig_size=(12, 20)):
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=fig_size)
    axs = axs.flatten()
    
    for i, col in enumerate(columns_list):
        sns.boxplot(y=dataframe[col], ax=axs[i])
        axs[i].set_title(col)
        
    # Oculta los subgráficos no utilizados
    for ax in axs[len(columns_list):]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

    #####################################################################################################################
    
# Genera múltiples countplots para varias columnas, incluyendo porcentajes sobre las barras.
# parametros: (el dataframe, la lista de columnas, nºfilas del grafico, nºcolumnas del grafico, tamaño de la figura (fig_size), tamaño de la fuente de los porcentajes).
def multi_countplot(dataframe, columns_list, n_rows, n_cols, fig_size=(12, 20), percentage_fontsize=8):
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=fig_size)
    axs = axs.flatten()
    
    for i, col in enumerate(columns_list):
        sns.countplot(x=dataframe[col], ax=axs[i])
        axs[i].set_title(col)
        axs[i].set_xlabel(None)
        axs[i].tick_params(axis='x', rotation=90)
        
        total = len(dataframe[col])

        # Añade el porcentaje sobre cada barra
        for p in axs[i].patches:
            porcentaje = round(100 * p.get_height() / total)
            conteo = round(p.get_height().round())
            texto = f'{porcentaje}%\n({conteo})'
            x = p.get_x() + p.get_width() / 2 
            y = p.get_height()
            axs[i].annotate(texto, (x, y), ha='center', va='bottom', fontsize=percentage_fontsize)

    # Oculta los subgráficos no utilizados
    for ax in axs[len(columns_list):]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

    #####################################################################################################################


# Crea múltiples histogramas para visualizar la distribución de varias columnas(la lista que proporcionemos).
# parametros: (el dataframe, la lista de columnas, nºfilas del grafico, nºcolumnas del grafico, tamaño de la figura (fig_size)).
def multi_histplot(dataframe, columns_list, n_rows, n_cols, fig_size=(12, 20)):
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=fig_size)
    axs = axs.flatten()
    
    for i, col in enumerate(columns_list):
        sns.histplot(x=dataframe[col], ax=axs[i], bins=50, kde=True)
        axs[i].set_title(col)
        
    # Oculta los subgráficos no utilizados
    for ax in axs[len(columns_list):]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

    #####################################################################################################################

# Crea boxplots comparativos para visualizar la distribución de varias columnas basadas en la columna objetivo.
# parametros: (el dataframe, la lista de columnas, la columna objetivo, nºfilas del grafico, nºcolumnas del grafico, tamaño de la figura (fig_size)).
def multi_compare_box(dataframe, columns_list,target, n_rows, n_cols, fig_size=(12, 20)):
    fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=fig_size)
    axs = axs.flatten()
    
    for i, col in enumerate(columns_list):
        sns.boxplot(x=dataframe[target], y=dataframe[col], ax=axs[i])
        axs[i].set_title(col)
        
    # Oculta los subgráficos no utilizados
    for ax in axs[len(columns_list):]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()

#####################################################################################################################
# grqafico de barras comparativo de variables categoricas: Grafica la tasa de respuesta por categoría de una variable categórica.
# (una grafica por cada columna categórica)  
# parametros: (el dataframe, la lista de columnas categóricas, la columna objetivo).
def categorical_comparison(dataframe, cat_cols, target_col):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Define los colores

    for col in cat_cols:
        # Calculamos los porcentajes de respuesta por categoría para la columna actual
        category_percentages = dataframe.groupby(col)[target_col].value_counts(normalize=True).mul(100)

        # Creamos el gráfico de barras
        category_percentages.plot(kind='bar', figsize=(12, 6), color=colors, title=(f'{col} vs response'))
        # Añadimos el porcentaje encima de cada barra
        for i in range(len(category_percentages)):
            plt.text(x=i, y=category_percentages.iloc[i]+1,
                    s=f"{round(category_percentages.iloc[i])}% ({dataframe.groupby(col)[target_col].value_counts().iloc[i]})",
                        ha='center', fontsize=8)
        # Mostramos el gráfico
        plt.tight_layout()
        plt.show()

        # ejemplo:
'''categorical_comparison(df, cat_cols, 'y')'''

###############################################################################################
    
# Visualiza la tasa de conversión de una variable objetivo en función de otra variable.
# parametros: (el dataframe, la variable predictora, la variable objetivo, tipo de gráfico, orden de las categorías).

def tasa_conversion(dataframe, var_predictora, var_target, type=['line', 'bar', 'scatter'], order=None):
    grupo = dataframe.groupby(var_predictora)[var_target].mean().mul(100).rename('tasa_conversion').reset_index()
    
    if type == 'line':
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=var_predictora, y='tasa_conversion', data=grupo)
        plt.grid()
    elif type == 'bar':
        plt.figure(figsize=(14, 6))
        sns.barplot(x=var_predictora, y='tasa_conversion', data=grupo, order=order)
        plt.grid()
    elif type == 'scatter':
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=var_predictora, y='tasa_conversion', data=grupo)
        plt.grid()

###############################################################################################

# Realiza codificación objetivo (target encoding) para una columna categórica.
# parametros: (el dataframe, la columna a codificar, la columna objetivo, coeficiente de suavizado).
        
def target_encoding(dataframe, column, target_column, smooth_coef=0):
    conteo_columna = dataframe.groupby(column)[target_column].count().reset_index(name='conteo')
    promedio_columna = dataframe.groupby(column)[target_column].mean().reset_index(name='column_mean')
    final_df = promedio_columna.merge(conteo_columna, on=column)
    global_mean = dataframe[target_column].mean()
    m = smooth_coef
    final_df[f'encoded_{column}'] = (final_df['conteo'] * final_df['column_mean'] + m * global_mean) / (final_df['conteo'] + m)
    encoded_value_dict = pd.Series(final_df[f'encoded_{column}'].values, index=final_df[column]).to_dict()
    result_df = dataframe.merge(final_df[[column, f'encoded_{column}']], on=column, how='left')
    return result_df

###############################################################################################




