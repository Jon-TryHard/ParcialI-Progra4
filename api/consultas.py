import unicodedata
import pandas as pd

RUTA_EXCEL = "resultado_laboratorio_suelo.xlsx"

COLUMNAS_EDAFICAS = {
    "pH": "pH agua:suelo 2,5:1,0",
    "Fosforo(P)": "Fósforo (P) Bray II mg/kg",
    "Potasio(K)": "Potasio (K) intercambiable cmol(+)/kg",
}


def limpiar_texto(serie: pd.Series) -> pd.Series:
    """Convierte a mayúsculas, elimina espacios extra y quita las tildes de una columna."""
    return (
        serie.astype(str)
        .str.strip()
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )


def limpiar_entrada(texto: str) -> str:
    """Normaliza el texto ingresado por el usuario quitando tildes y pasándolo a mayúsculas."""
    texto_norm = unicodedata.normalize("NFKD", texto.strip().upper())
    return texto_norm.encode("ascii", "ignore").decode("utf-8")


def formatear_valor(valor) -> str:
    """Formatea valores numéricos o devuelve N/D si el dato no es numérico."""
    if pd.isna(valor):
        return "N/D"
    return f"{valor:.2f}" if abs(valor) < 10000 else f"{valor:.4e}"


def cargar_datos(ruta: str = RUTA_EXCEL) -> pd.DataFrame:
    """Carga la hoja principal del archivo Excel en un DataFrame."""
    return pd.read_excel(ruta, sheet_name="resultado_laboratorio_suelo")


def filtrar_registros(
    df: pd.DataFrame,
    departamento: str,
    municipio: str,
    cultivo: str,
    limite: int,
) -> pd.DataFrame:
    """Filtra el DataFrame ignorando mayúsculas, minúsculas y tildes."""
    dep_limpio = limpiar_entrada(departamento)
    mun_limpio = limpiar_entrada(municipio)
    cul_limpio = limpiar_entrada(cultivo)

    filtro = (
        (limpiar_texto(df["Departamento"]) == dep_limpio)
        & (limpiar_texto(df["Municipio"]) == mun_limpio)
        & (limpiar_texto(df["Cultivo"]) == cul_limpio)
    )
    return df[filtro].head(limite).copy()


def obtener_resumen_edafico(df_filtrado: pd.DataFrame) -> dict:
    """Retorna la lista de los N registros consultados y el cálculo de las medianas."""
    if df_filtrado.empty:
        return {}

    serie_ph = pd.to_numeric(df_filtrado[COLUMNAS_EDAFICAS["pH"]], errors="coerce")
    serie_p = pd.to_numeric(df_filtrado[COLUMNAS_EDAFICAS["Fosforo(P)"]], errors="coerce")
    serie_k = pd.to_numeric(df_filtrado[COLUMNAS_EDAFICAS["Potasio(K)"]], errors="coerce")

    registros = []
    for idx, (_, fila) in enumerate(df_filtrado.iterrows(), start=1):
        ph_val = pd.to_numeric(fila[COLUMNAS_EDAFICAS["pH"]], errors="coerce")
        p_val = pd.to_numeric(fila[COLUMNAS_EDAFICAS["Fosforo(P)"]], errors="coerce")
        k_val = pd.to_numeric(fila[COLUMNAS_EDAFICAS["Potasio(K)"]], errors="coerce")

        registros.append({
            "#": idx,
            "Departamento": fila["Departamento"],
            "Municipio": fila["Municipio"],
            "Cultivo": fila["Cultivo"],
            "Topología": fila["Topografia"] if pd.notna(fila["Topografia"]) else "No indica",
            "pH": formatear_valor(ph_val),
            "Fósforo (P)": formatear_valor(p_val),
            "Potasio (K)": formatear_valor(k_val),
        })

    topologias = ", ".join(df_filtrado["Topografia"].dropna().astype(str).unique())

    mediana = {
        "Departamento": df_filtrado["Departamento"].iloc[0],
        "Municipio": df_filtrado["Municipio"].iloc[0],
        "Cultivo": df_filtrado["Cultivo"].iloc[0],
        "Topología": topologias if topologias else "No indica",
        "Mediana pH": formatear_valor(serie_ph.median()) if serie_ph.notna().any() else "N/D",
        "Mediana P": formatear_valor(serie_p.median()) if serie_p.notna().any() else "N/D",
        "Mediana K": formatear_valor(serie_k.median()) if serie_k.notna().any() else "N/D",
    }

    return {"registros": registros, "mediana": mediana}
