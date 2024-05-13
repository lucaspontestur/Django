from django.db import models

class Compra(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    numero = models.CharField(max_length=20)
    data_compra = models.DateField()
    pacote = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nome} - {self.pacote}"