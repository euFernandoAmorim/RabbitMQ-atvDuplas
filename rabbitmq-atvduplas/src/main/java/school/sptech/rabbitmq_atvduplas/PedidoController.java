package school.sptech.rabbitmq_atvduplas;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import school.sptech.rabbitmq_atvduplas.objetos.Pedido;
import school.sptech.rabbitmq_atvduplas.rabbitConfig.PedidoProducer;

@RestController
@RequestMapping("/pedidos")
@RequiredArgsConstructor
public class PedidoController {

    private final PedidoProducer pedidoProducer;

    private final PedidoService pedidoService;

    @PostMapping
    public ResponseEntity<Pedido> criarPedido(@RequestBody Pedido pedido) {
        Pedido pedidoValidado = pedidoService.criarPedido(pedido);
        pedidoProducer.enviarPedido(pedidoValidado);
        return ResponseEntity.ok(pedidoValidado);
    }
}

