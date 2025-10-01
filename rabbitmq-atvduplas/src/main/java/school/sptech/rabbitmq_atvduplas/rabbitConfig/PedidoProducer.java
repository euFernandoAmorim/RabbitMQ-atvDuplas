package school.sptech.rabbitmq_atvduplas.rabbitConfig;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;
import school.sptech.rabbitmq_atvduplas.objetos.Pedido;

@Service
public class PedidoProducer {

    private final RabbitTemplate rabbitTemplate;

    public PedidoProducer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void enviarPedido(Pedido pedido) {
        rabbitTemplate.convertAndSend(
                RabbitTemplateConfiguration.EXCHANGE,
                RabbitTemplateConfiguration.ROUTING_KEY,
                pedido
        );
        System.out.println("📦 Pedido enviado para RabbitMQ: " + pedido);
    }
}

