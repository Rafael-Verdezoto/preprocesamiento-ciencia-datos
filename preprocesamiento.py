"""
preprocesamiento.py
--------------------
Módulo de preprocesamiento completo de datasets para Ciencia de Datos.
Incluye: manejo de valores nulos, normalización, codificación de
variables categóricas y eliminación de duplicados.

Universidad Nacional de Chimborazo — Ciencia de Datos
Materia: Cultura Digital y Sociedad
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder


# 1. CARGA DEL DATASET

def cargar_dataset(ruta: str) -> pd.DataFrame:
    """
    Carga un dataset desde un archivo CSV.

    Parámetros:
        ruta (str): Ruta al archivo CSV.

    Retorna:
        pd.DataFrame: Dataset cargado.
    """
    df = pd.read_csv(ruta)
    print("Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas.")
    return df


def crear_dataset_ejemplo() -> pd.DataFrame:
    """
    Crea un dataset de ejemplo para demostrar el preprocesamiento.

    Retorna:
        pd.DataFrame: Dataset de muestra con valores nulos y duplicados.
    """
    data = {
        "edad":      [25, 30, None, 45, 30, 25, 60, None, 35, 40],
        "salario":   [3000, 4500, 2800, None, 4500, 3000, 7000, 5500, None, 4000],
        "ciudad":    ["Quito", "Guayaquil", "Cuenca", "Quito", "Guayaquil",
                      "Quito", "Cuenca", None, "Ambato", "Guayaquil"],
        "categoria": ["A", "B", "A", "C", "B", "A", "C", "B", None, "A"],
        "activo":    [True, False, True, True, False, True, False, True, True, False],
    }
    df = pd.DataFrame(data)
    print(" Dataset de ejemplo creado.")
    return df


# 2. EXPLORACIÓN INICIAL

def explorar_dataset(df: pd.DataFrame) -> None:
    """
    Muestra información general del dataset: tipos, nulos y estadísticas.

    Parámetros:
        df (pd.DataFrame): Dataset a explorar.
    """
    print(" EXPLORACIÓN DEL DATASET")
    print("Forma: {df.shape}")
    print("Tipos de datos:")
    print(df.dtypes)
    print("Primeras 5 filas:")
    print(df.head())
    print("Valores nulos por columna:")
    print(df.isnull().sum())
    print("Estadísticas descriptivas:")
    print(df.describe(include="all"))
    print("=" * 46)

# 3. ELIMINACIÓN DE DUPLICADOSb

def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas duplicadas del dataset.

    Parámetros:
        df (pd.DataFrame): Dataset de entrada.

    Retorna:
        pd.DataFrame: Dataset sin filas duplicadas.
    """
    duplicados = df.duplicated().sum()
    df_sin_dup = df.drop_duplicates().reset_index(drop=True)
    print("Duplicados eliminados: {duplicados} filas. "
          "Filas restantes: {df_sin_dup.shape[0]}")
    return df_sin_dup

# 4. MANEJO DE VALORES NULOS

def manejar_valores_nulos(df: pd.DataFrame,
                          estrategia_numerica: str = "media",
                          estrategia_categorica: str = "moda") -> pd.DataFrame:
    """
    Rellena los valores nulos según la estrategia indicada.

    Parámetros:
        df (pd.DataFrame): Dataset de entrada.
        estrategia_numerica (str): 'media', 'mediana' o 'cero'.
        estrategia_categorica (str): 'moda' o 'desconocido'.

    Retorna:
        pd.DataFrame: Dataset sin valores nulos.
    """
    df = df.copy()

    for col in df.columns:
        nulos = df[col].isnull().sum()
        if nulos == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            if estrategia_numerica == "media":
                valor = df[col].mean()
            elif estrategia_numerica == "mediana":
                valor = df[col].median()
            else:
                valor = 0
            df[col].fillna(round(valor, 2), inplace=True)
            print("  [num] '{col}': {nulos} nulos → reemplazados con {estrategia_numerica} ({round(valor, 2)})")

        else:
            if estrategia_categorica == "moda":
                valor = df[col].mode()[0]
            else:
                valor = "Desconocido"
            df[col].fillna(valor, inplace=True)
            print("  [cat] '{col}': {nulos} nulos → reemplazados con '{valor}'")

    print("Manejo de valores nulos completado.")
    return df

# 5. NORMALIZACIÓN DE VARIABLES NUMÉRICAS

def normalizar_columnas(df: pd.DataFrame,
                        columnas: list) -> pd.DataFrame:
    """
    Normaliza columnas numéricas al rango [0, 1] usando MinMaxScaler.

    Parámetros:
        df (pd.DataFrame): Dataset de entrada.
        columnas (list): Lista de columnas a normalizar.

    Retorna:
        pd.DataFrame: Dataset con columnas normalizadas (sufijo '_norm').
    """
    df = df.copy()
    scaler = MinMaxScaler()

    for col in columnas:
        if col not in df.columns:
            print("  Columna '{col}' no encontrada. Se omite.")
            continue
        col_norm = "{col}_norm"
        df[col_norm] = scaler.fit_transform(df[[col]])
        print(" {col}' normalizada → '{col_norm}' (min=0, max=1)")

    print("Normalización completada.")
    return df

# 6. CODIFICACIÓN DE VARIABLES CATEGÓRICAS

def codificar_categoricas(df: pd.DataFrame,
                          columnas: list,
                          metodo: str = "label") -> pd.DataFrame:
    """
    Codifica variables categóricas usando Label Encoding u One-Hot Encoding.

    Parámetros:
        df (pd.DataFrame): Dataset de entrada.
        columnas (list): Columnas categóricas a codificar.
        metodo (str): 'label' para LabelEncoder, 'onehot' para get_dummies.

    Retorna:
        pd.DataFrame: Dataset con variables categóricas codificadas.
    """
    df = df.copy()

    for col in columnas:
        if col not in df.columns:
            print("Columna '{col}' no encontrada. Se omite.")
            continue

        if metodo == "label":
            le = LabelEncoder()
            df["{col}_encoded"] = le.fit_transform(df[col].astype(str))
            clases = dict(zip(le.classes_, le.transform(le.classes_)))
            print("  [✔] '{col}' → Label Encoding: {clases}")

        elif metodo == "onehot":
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[col], inplace=True)
            print(" '{col}' → One-Hot Encoding: {list(dummies.columns)}")

    print("Codificación completada.")
    return df


# 7. PIPELINE COMPLETO

def preprocesar_dataset(df: pd.DataFrame,
                        cols_numericas: list = None,
                        cols_categoricas: list = None,
                        metodo_codificacion: str = "label") -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de preprocesamiento:
        1. Eliminar duplicados
        2. Manejar valores nulos
        3. Normalizar columnas numéricas
        4. Codificar variables categóricas

    Parámetros:
        df (pd.DataFrame): Dataset original.
        cols_numericas (list): Columnas a normalizar.
        cols_categoricas (list): Columnas a codificar.
        metodo_codificacion (str): 'label' u 'onehot'.

    Retorna:
        pd.DataFrame: Dataset completamente preprocesado.
    """
    print("INICIO DEL PREPROCESAMIENTO")

    print("→ Paso 1: Eliminar duplicados")
    df = eliminar_duplicados(df)

    print("\n→ Paso 2: Manejar valores nulos")
    df = manejar_valores_nulos(df)

    if cols_numericas:
        print("\n→ Paso 3: Normalizar columnas numéricas")
        df = normalizar_columnas(df, cols_numericas)

    if cols_categoricas:
        print("\n→ Paso 4: Codificar variables categóricas")
        df = codificar_categoricas(df, cols_categoricas, metodo_codificacion)

    print("PREPROCESAMIENTO COMPLETADO")
    print("Dataset final: {df.shape[0]} filas × {df.shape[1]} columnas\n")
    return df


# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":
    # Crear dataset de ejemplo
    df_original = crear_dataset_ejemplo()

    # Explorar antes del preprocesamiento
    explorar_dataset(df_original)

    # Ejecutar pipeline completo
    df_procesado = preprocesar_dataset(
        df=df_original,
        cols_numericas=["edad", "salario"],
        cols_categoricas=["ciudad", "categoria"],
        metodo_codificacion="label"
    )

    # Ver resultado final
    print("Dataset procesado:")
    print(df_procesado.to_string())
