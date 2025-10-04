import pika
import json
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from collections import defaultdict

app = FastAPI()
pedidos_por_mesa = defaultdict(list)

def salvar_pedido(pedido: dict):
    mesa = pedido.get("mesa")
    itens = pedido.get("itens", [])
    
    pedidos_por_mesa[mesa].append({
        "itens": itens,
        "hora": datetime.now().strftime("%H:%M:%S")
    })

def agrupar_pedidos():
    resultado = []
    for mesa, pedidos in pedidos_por_mesa.items():
        itens_agrupados = defaultdict(int)
        
        for pedido in pedidos:
            for item in pedido["itens"]:
                itens_agrupados[item["nome"]] += item["quantidade"]
        
        resultado.append({
            "mesa": mesa,
            "itens": [{"nome": nome, "quantidade": qtd} for nome, qtd in itens_agrupados.items()],
            "horario_ultimo_pedido": pedidos[-1]["hora"],
            "total_itens": sum(itens_agrupados.values())
        })
    
    return resultado

def callback(ch, method, properties, body):
    pedido = json.loads(body)
    salvar_pedido(pedido)
    print(f"✅ Pedido salvo -> Mesa {pedido['mesa']}")

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

@app.get("/pedidos")
def get_pedidos():
    return agrupar_pedidos()

if __name__ == "__main__":
    import threading
    
    t = threading.Thread(target=iniciar_consumidor, daemon=True)
    t.start()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
