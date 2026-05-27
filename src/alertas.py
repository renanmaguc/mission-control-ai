def avaliar(dados):

    alertas = []

    if dados["temperatura"] >= 85:
        alertas.append("CRÍTICO: Temperatura extremamente elevada")
    elif dados["temperatura"] >= 75:
        alertas.append("ALERTA: Temperatura elevada")

    if dados["energia"] <= 20:
        alertas.append("CRÍTICO: Nível de energia muito baixo")
    elif dados["energia"] <= 35:
        alertas.append("ALERTA: Energia reduzida")

    if dados["comunicacao"] == "OFFLINE":
        alertas.append("CRÍTICO: Falha total de comunicação")
    elif dados["comunicacao"] == "INSTÁVEL":
        alertas.append("ALERTA: Comunicação instável")

    if dados["latencia"] >= 220:
        alertas.append("ALERTA: Latência elevada")

    if dados["estabilidade"] <= 35:
        alertas.append("CRÍTICO: Instabilidade orbital grave")
    elif dados["estabilidade"] <= 50:
        alertas.append("ALERTA: Estabilidade orbital reduzida")

    if not alertas:
        alertas.append("NORMAL: Nenhum alerta detectado")

    return alertas