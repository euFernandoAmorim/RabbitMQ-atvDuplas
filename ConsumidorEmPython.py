import pika
import json
from datetime import datetime
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Armazenamento em memória: pedidos agrupados por mesa
pedidos_por_mesa = {}

# ===============================
# 📌 Método 1: Receber e salvar pedido
# ===============================
def salvar_pedido(pedido: dict):
    mesa = pedido.get("mesa")
    itens = pedido.get("itens", [])

    if mesa not in pedidos_por_mesa:
        pedidos_por_mesa[mesa] = []

    pedidos_por_mesa[mesa].append({
        "itens": itens,
        "hora": datetime.now().strftime("%H:%M:%S")
    })

# ===============================
# 📌 Método 2: Agrupar por mesa
# ===============================
def agrupar_pedidos():
    resultado = []
    for mesa, pedidos in pedidos_por_mesa.items():
        itens_agrupados = {}

        for pedido in pedidos:
            for item in pedido["itens"]:
                nome = item["nome"]
                quantidade = item["quantidade"]
                if nome not in itens_agrupados:
                    itens_agrupados[nome] = 0
                itens_agrupados[nome] += quantidade

        resultado.append({
            "mesa": mesa,
            "itens": [{"nome": k, "quantidade": v} for k, v in itens_agrupados.items()],
            "horario_ultimo_pedido": pedidos[-1]["hora"],
            "total_itens": sum(itens_agrupados.values())
        })

    return resultado

# ===============================
# 📌 RabbitMQ - Callback
# ===============================
def callback(ch, method, properties, body):
    pedido = json.loads(body)
    salvar_pedido(pedido)
    print(f"✅ Pedido salvo -> Mesa {pedido['mesa']}")

# ===============================
# 📌 RabbitMQ - Configuração
# ===============================
def iniciar_consumidor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='pedidos_queue', durable=True)

    channel.basic_consume(
        queue='pedidos_queue',
        on_message_callback=callback,
        auto_ack=True
    )

    print("👂 Aguardando pedidos...")
    channel.start_consuming()

# ===============================
# 📌 Endpoint GET para visualizar pedidos agrupados
# ===============================
@app.get("/pedidos")
def get_pedidos():
    return agrupar_pedidos()

# ===============================
# 📌 Rodar o FastAPI + Consumidor
# ===============================
if __name__ == "__main__":
    import threading
    # Thread separada para o consumidor RabbitMQ
    t = threading.Thread(target=iniciar_consumidor, daemon=True)
    t.start()

    # Inicia o servidor FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
