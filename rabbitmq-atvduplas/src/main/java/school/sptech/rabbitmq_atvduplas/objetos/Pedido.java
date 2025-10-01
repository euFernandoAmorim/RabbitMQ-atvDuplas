package school.sptech.rabbitmq_atvduplas.objetos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Pedido {
    private Integer mesa;
    private List<Item> itens;
}
