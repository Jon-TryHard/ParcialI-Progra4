from api.consultas import cargar_datos, filtrar_registros, obtener_resumen_edafico
from ui.interfaz import solicitar_datos_usuario, mostrar_tabla_resultados


def main():
    print("Cargando base de datos de suelos, por favor espere...")
    df = cargar_datos()

    while True:
        departamento, municipio, cultivo, limite = solicitar_datos_usuario()
        df_filtrado = filtrar_registros(df, departamento, municipio, cultivo, limite)
        resumen = obtener_resumen_edafico(df_filtrado)
        mostrar_tabla_resultados(resumen, len(df_filtrado))

        continuar = input("\n¿Desea realizar otra consulta? (s/n): ").strip().lower()
        if continuar != "s":
            print("Finalizando aplicación.")
            break


if __name__ == "__main__":
    main()