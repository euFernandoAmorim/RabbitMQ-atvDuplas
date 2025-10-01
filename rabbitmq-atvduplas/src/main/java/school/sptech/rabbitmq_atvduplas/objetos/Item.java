package school.sptech.rabbitmq_atvduplas.objetos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public abstract class Item {

    Integer id;

    String nome;

    String descricao;

    Double preco;

    Integer quantidade;
}
