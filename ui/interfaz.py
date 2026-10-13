from tabulate import tabulate


def solicitar_datos_usuario() -> tuple[str, str, str, int]:
    """Solicita al usuario los parámetros de búsqueda por línea de comandos."""
    print("\n" + "=" * 65)
    print("  CONSULTA DE PROPIEDADES EDÁFICAS DE SUELOS EN COLOMBIA")
    print("=" * 65)

    departamento = input("1. Ingrese el Departamento (ej. RISARALDA): ").strip()
    municipio = input("2. Ingrese el Municipio (ej. SANTA ROSA DE CABAL): ").strip()
    cultivo = input("3. Ingrese el Cultivo (ej. Plátano): ").strip()

    while True:
        try:
            limite = int(input("4. Ingrese el Número de Registros a consultar: ").strip())
            if limite > 0:
                break
            print("   [!] Por favor ingrese un número entero mayor a 0.")
        except ValueError:
            print("   [!] Entrada inválida. Ingrese un número entero.")

    return departamento, municipio, cultivo, limite


def mostrar_tabla_resultados(resumen: dict, total_encontrados: int) -> None:
    """Muestra la tabla con los N registros consultados y la tabla de medianas."""
    if not resumen:
        print("\n[!] No se encontraron registros con los criterios especificados.")
        return

    print(f"\n1. Registros consultados ({total_encontrados} filas encontradas):\n")
    print(tabulate(resumen["registros"], headers="keys", tablefmt="fancy_grid"))

    print("\n2. Resumen de Medianas de las variables edáficas:\n")
    print(tabulate([resumen["mediana"]], headers="keys", tablefmt="fancy_grid"))
