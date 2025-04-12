import difflib

with open("everything.yaml", encoding="utf-8") as f1, open("everything-cgpt.yaml", encoding="utf-8") as f2:
    lineas1 = f1.readlines()
    lineas2 = f2.readlines()

umbral = 0.6  # porcentaje mínimo de similitud (de 0 a 1)

with open("comparacion.txt", "w", encoding="utf-8") as salida:
    for l1 in lineas1:
        for l2 in lineas2:
            similitud = difflib.SequenceMatcher(None, l1.strip(), l2.strip()).ratio()
            if similitud >= umbral:
                salida.write(f"[{similitud:.2f}]\n")
                salida.write("  Archivo1: " + l1.strip() + "\n")
                salida.write("  Archivo2: " + l2.strip() + "\n")
                salida.write("\n")