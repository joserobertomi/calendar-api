from django.db import models
from ..validators import *


class Convenio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=32, validators=[validade_char_lower_than_32])
    inscricao = models.CharField(max_length=64, validators=[validade_char_lower_than_64])

    def __str__(self) -> str:
        return self.nome
