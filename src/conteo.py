def mostrar_conteo(cont, metodo):
    print("i\t*/÷\t+/-\tTotal")

    with open("resultados/conteo_flops.md", "a", encoding="utf-8") as archivo:
        archivo.write(f"\n## Método: {metodo}\n\n")
        archivo.write("| Paso | Mult/Div | Sumas/Restas | Total |\n")
        archivo.write("|---|---:|---:|---:|\n")

        for i in range(len(cont["muldiv_pasos"])):
            md = cont["muldiv_pasos"][i]
            ad = cont["addsub_pasos"][i]

            print(f"{i+1}\t{md}\t{ad}\t{md+ad}")
            archivo.write(f"| {i+1} | {md} | {ad} | {md+ad} |\n")

        muldiv = sum(cont["muldiv_pasos"]) + cont["muldiv_sust"]
        addsub = sum(cont["addsub_pasos"]) + cont["addsub_sust"]

        print("\nMultiplicaciones/divisiones:", muldiv)
        print("Sumas/restas:", addsub)
        print("Total flops:", muldiv + addsub)
        print("Comparaciones:", cont["comparaciones"])
        print("Intercambios:", cont["intercambios"])

        archivo.write(f"\n- Multiplicaciones/divisiones: {muldiv}\n")
        archivo.write(f"- Sumas/restas: {addsub}\n")
        archivo.write(f"- Total flops: {muldiv + addsub}\n")
        archivo.write(f"- Comparaciones: {cont['comparaciones']}\n")
        archivo.write(f"- Intercambios: {cont['intercambios']}\n")