def avaliar(dados):

    alertas = []

    if dados["temperatura"] > 80:
        alertas.append("Temperatura crítica")

    if dados["energia"] < 20:
        alertas.append("Baixo nível de energia")

    if dados["comunicacao"] == "OFFLINE":
        alertas.append("Falha de comunicação")

    if dados["latencia"] > 200:
        alertas.append("Latência elevada")

    if dados["estabilidade"] < 50:
        alertas.append("Instabilidade orbital")

    return alertas