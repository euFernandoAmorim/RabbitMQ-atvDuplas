package school.sptech.rabbitmq_atvduplas;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import school.sptech.rabbitmq_atvduplas.objetos.Pedido;
import school.sptech.rabbitmq_atvduplas.rabbitConfig.PedidoProducer;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    private final PedidoProducer pedidoProducer;

    public PedidoController(PedidoProducer pedidoProducer) {
        this.pedidoProducer = pedidoProducer;
    }

    @PostMapping
    public ResponseEntity<String> criarPedido(@RequestBody Pedido pedido) {
        pedidoProducer.enviarPedido(pedido);
        return ResponseEntity.ok("Pedido enviado com sucesso!");
    }
}

