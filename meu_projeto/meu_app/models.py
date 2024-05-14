from django.db import models
from decimal import Decimal

class Compra(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    numero = models.CharField(max_length=20)
    data_compra = models.DateField()
    pacote = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def taxa_catarse(self):
        return self.valor * Decimal('0.13')

    @property
    def faturamento(self):
        return self.valor * Decimal('0.87')

    def __str__(self):
        return f"{self.nome} - {self.pacote}"

    @property
    def numero_formatado(self):
        return f"({self.numero[0:2]}) {self.numero[2:7]}-{self.numero[7:]}"

    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @property
    def taxa_catarse_formatada(self):
        return f"R$ {self.taxa_catarse:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @property
    def faturamento_formatado(self):
        return f"R$ {self.faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")