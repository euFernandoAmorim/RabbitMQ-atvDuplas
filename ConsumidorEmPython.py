import pika
import json
from datetime import datetime
from fastapi import FastAPI, Query
import uvicorn
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Sistema de Pedidos", description="API para gerenciar pedidos por mesa")
pedidos_por_mesa = defaultdict(list)
stats = {"total_pedidos": 0, "inicio": datetime.now().strftime("%H:%M:%S")}

def salvar_pedido(pedido: dict):
    mesa = pedido.get("mesa")
    itens = pedido.get("itens", [])
    
    pedidos_por_mesa[mesa].append({
        "itens": itens,
        "hora": datetime.now().strftime("%H:%M:%S"),
        "timestamp": datetime.now().isoformat()
    })
    stats["total_pedidos"] += 1

def agrupar_pedidos():
    resultado = []
    for mesa, pedidos in pedidos_por_mesa.items():
        itens_agrupados = defaultdict(int)
        
        for pedido in pedidos:
            for item in pedido["itens"]:
                itens_agrupados[item["nome"]] += item["quantidade"]
        
        resultado.append({
            "mesa": mesa,
            "itens": sorted([{"nome": nome, "quantidade": qtd} for nome, qtd in itens_agrupados.items()], 
                           key=lambda x: x["quantidade"], reverse=True),
            "horario_ultimo_pedido": pedidos[-1]["hora"],
            "total_itens": sum(itens_agrupados.values()),
            "total_pedidos": len(pedidos)
        })
    
    return sorted(resultado, key=lambda x: x["mesa"])

def callback(ch, method, properties, body):
    pedido = json.loads(body)
    salvar_pedido(pedido)
    print(f"Pedido recebido -> Mesa {pedido['mesa']}")

def iniciar_consumidor():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='pedidos_queue', durable=True)
        
        channel.basic_consume(
            queue='pedidos_queue',
            on_message_callback=callback,
            auto_ack=True
        )
        
        print(" Conectado ao RabbitMQ - Aguardando pedidos do Java...")
        channel.start_consuming()
    except Exception as e:
        print(f" Erro RabbitMQ: {e}")
        print("  Verifique se o RabbitMQ está rodando em localhost:5672")

@app.get("/pedidos")
def get_pedidos(mesa: int = Query(None, description="Filtrar por mesa específica")):
    pedidos = agrupar_pedidos()
    return [p for p in pedidos if p["mesa"] == mesa] if mesa else pedidos

@app.get("/status")
def get_status():
    return {"total_pedidos": stats["total_pedidos"], "mesas_ativas": len(pedidos_por_mesa), 
            "inicio_servico": stats["inicio"], "uptime": str(datetime.now() - datetime.strptime(stats["inicio"], "%H:%M:%S").replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day))[:7]}

if __name__ == "__main__":
    import threading
    
    t = threading.Thread(target=iniciar_consumidor, daemon=True)
    t.start()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)