import random


def coletar():

    return {
        "temperatura": random.randint(20, 100),

        "energia": random.randint(10, 100),

        "comunicacao": random.choice([
            "ONLINE",
            "INSTÁVEL",
            "OFFLINE"
        ]),

        "latencia": random.randint(20, 300),

        "estabilidade": random.randint(40, 100)
    }