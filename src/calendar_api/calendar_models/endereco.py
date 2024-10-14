from django.db import models
from ..validators import *
from django.core.exceptions import ValidationError
from ..utils.choices import BRAZIL_STATES


class Endereco(models.Model):
    id = models.BigAutoField(primary_key=True)
    cep = models.CharField(max_length=8, validators=[validate_cep])
    rua = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    bairro = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    numero = models.IntegerField(null=True, blank=True, validators=[validate_integer])
    quadra_lote = models.CharField(null=True, blank=True, max_length=16, validators=[validade_char_lower_than_16])
    cidade = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    estado = models.CharField(max_length=2, choices=BRAZIL_STATES, validators=[validate_state])
    complemento = models.CharField(max_length=32, validators=[validade_char_lower_than_32])

    def clean(self):
        # Chama a implementação original da superclasse
        super().clean()
        # Verifica se pelo menos um dos campos numero ou quadra_lote está preenchido
        if not self.numero and not self.quadra_lote:
            raise ValidationError(
                "ERROR - Um dos campos número ou quadra/lote deve existir."
            )

    def __str__(self):
        if self.numero:
            return f"{self.numero}, {self.bairro}, {self.cidade}"
        return f"{self.quadra_lote}, {self.bairro}, {self.cidade}"

    class Meta:
        permissions = [
            ("endereco_create", "Pode criar endereços"),
            ("endereco_list", "Pode listar endereços"),
            ("endereco_retrieve", "Pode recuperar um endereço"),
            ("endereco_update", "Pode atualizar endereços"),
            ("endereco_partial_update", "Pode atualizar parcialmente endereços"),
            ("endereco_destroy", "Pode destruir endereços"),
        ]
        managed = True
