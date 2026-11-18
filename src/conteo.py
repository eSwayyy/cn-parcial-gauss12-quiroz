def mostrar_conteo(cont):
    print("i\t*/÷\t+/-\tTotal")

    for i in range(len(cont["muldiv_pasos"])):
        md = cont["muldiv_pasos"][i]
        ad = cont["addsub_pasos"][i]

        print(f"{i+1}\t{md}\t{ad}\t{md+ad}")

    muldiv = sum(cont["muldiv_pasos"]) + cont["muldiv_sust"]
    addsub = sum(cont["addsub_pasos"]) + cont["addsub_sust"]

    print("\nMultiplicaciones/divisiones:", muldiv)
    print("Sumas/restas:", addsub)
    print("Total flops:", muldiv + addsub)

    print("Comparaciones:", cont["comparaciones"])
    print("Intercambios:", cont["intercambios"])