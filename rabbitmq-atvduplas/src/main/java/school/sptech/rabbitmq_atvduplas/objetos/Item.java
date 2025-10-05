package school.sptech.rabbitmq_atvduplas.objetos;

import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.PROPERTY,
        property = "tipo"
)
@JsonSubTypes({
        @JsonSubTypes.Type(value = Drink.class, name = "drink"),
        @JsonSubTypes.Type(value = Prato.class, name = "prato")
})
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
