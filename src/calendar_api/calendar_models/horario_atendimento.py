from django.db import models
from .profissional import Profissional
from ..validators import *
from django.core.exceptions import ValidationError
from ..utils.choices import WEEK_DAYS


class HorariosAtendimento(models.Model):
    id = models.BigAutoField(primary_key=True)
    dia_da_semana = models.CharField(choices=WEEK_DAYS, max_length=3, validators=[validate_days_of_week])
    inicio = models.TimeField()
    fim = models.TimeField()
    profissional_fk = models.ForeignKey(Profissional, null=True, on_delete=models.CASCADE)

    def clean(self):
        # Chama a implementação original da superclasse
        super().clean()

        # Verifica se o tempo de início é posterior ao de fim
        if self.inicio and self.fim and self.inicio > self.fim:
            raise ValidationError(
                _("ERROR - The finish time must be after the start time.")
            )

    def __str__(self) -> str:
        return f"{self.dia_da_semana}: {self.inicio}-{self.fim}"