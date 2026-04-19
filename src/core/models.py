from django.db import models

class Dono(models.Model):
    nome = models.CharField(max_length=100)
    nif = models.CharField(max_length=9, blank=True, null=True)
    telefone = models.CharField(max_length=9)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Animal(models.Model):
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    dono = models.ForeignKey(Dono, on_delete=models.CASCADE, related_name='animais')

    def __str__(self):
        return f"{self.nome} ({self.especie}) - Dono: {self.dono.nome}"

class Veterinario(models.Model):
    nome = models.CharField(max_length=100)
    celula_profissional = models.CharField(max_length=20, unique=True)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.nome} ({self.celula_profissional})"

class Consulta(models.Model):
    data_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE, related_name='consultas')
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='consultas')

    def __str__(self):
        return f"Consulta de {self.animal.nome} a {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    dose = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome

class Servico(models.Model):
    servico = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.servico

class DetalheConsulta(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='detalhes')
    servico = models.ForeignKey(Servico, on_delete=models.SET_NULL, blank=True, null=True)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.SET_NULL, blank=True, null=True)
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Detalhe da Consulta ID {self.consulta.id}"