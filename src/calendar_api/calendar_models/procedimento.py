from django.db import models
from ..validators import *


class Procedimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=128, validators=[validade_char_lower_than_128], unique=True)
    def __str__(self) -> str:
        return self.nome