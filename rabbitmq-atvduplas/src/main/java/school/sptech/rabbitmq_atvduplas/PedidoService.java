package school.sptech.rabbitmq_atvduplas;

import org.springframework.stereotype.Service;
import school.sptech.rabbitmq_atvduplas.objetos.Pedido;

@Service
public class PedidoService {

    public Pedido criarPedido(Pedido pedido){
       if (pedido == null || pedido.getItens().isEmpty()){
           throw new RuntimeException("Pedido Inválido!");
       }
       return pedido;
    }

}
