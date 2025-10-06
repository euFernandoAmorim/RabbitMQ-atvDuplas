# RabbitMQ-atvDuplas
Repositório destinado a execução da atividade de implementação de Rabbit MQ da matéria de Técnicas Avançadas de Back-Ned.

-- TEMA: O tema dessa atividade é a simulação de envio de pedidos em um restaurante. Os pedidos são separados por mesa, sendo possível pedir para uma única mesa por vez, mas dentro de um pedido podem vir diversos itens sendo eles bebidas ou pratos


INTEGRANTES
- nome: Fernando Almeida
- RA: 04241027
- nome: Luis Henrique
- RA: 04241047

Como executar:
- suba  o container com 'docker compose up -d'
- verifique se o container está rodando com 'docker ps'
- Utilize 'python ConsumidorEmPython.py' na raiz da pasta para iniciar o consumidor.
- obs: o usuario e senha do container são definidos no arquivo compose.yaml e são referenciados para acesso no arquivo python (por padrão eles estão como guest)

URL POST para envio de pedido: localhost:8080/pedidos
- exemplo JSON: {
	"mesa":1,
	"itens":[{
		"tipo": "drink",
		"id":1,
						"nome":"sex on the beach",
						"descricao":"A sex on the beach is an alcoholic cocktail containing vodka, peach schnapps, orange juice and cranberry juice.",
						"preco":50.0,
						"quantidade":1,
					 "tipoBebida": "alcoolica"},
					{
		"tipo": "prato",
		"id":2,
						"nome":"feijoada",
						"descricao":"Feijoada is the name for varieties of bean stew with beef or pork prepared in the Portuguese-speaking world.",
						"preco":100.0,
						"quantidade":1,
					 "nacionalidade": "brasil"}],
	"horarioPedido":"2025-04-12T10:15:30"
}

URL GET do consumidor: 
- localhost:8000/pedidos
- localhost:8000/status
