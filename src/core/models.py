from django.db import models

class Dono(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    nif = models.CharField(max_length=9, blank=True, null=True)
    telefone = models.CharField(max_length=9)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Diz ao Django para não tentar alterar esta tabela
        db_table = 'dono' # O nome exato da tabela no teu pgAdmin

    def __str__(self):
        return self.nome


class Animal(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raca = models.CharField(max_length=50, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    dono = models.ForeignKey(Dono, models.DO_NOTHING)
    foto = models.ImageField(upload_to='animais_fotos/', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'animal'

    def __str__(self):
        return f"{self.nome} ({self.especie})"


class Veterinario(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    celula_profissional = models.CharField(unique=True, max_length=20)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'veterinario'

    def __str__(self):
        return f"{self.nome} ({self.celula_profissional})"


class Consulta(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255, blank=True, null=True)
    observacoes = models.CharField(max_length=255, blank=True, null=True)
    veterinario = models.ForeignKey(Veterinario, models.DO_NOTHING)
    animal = models.ForeignKey(Animal, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'consulta'

    def __str__(self):
        return f"Consulta de {self.animal.nome} a {self.data_hora.strftime('%d/%m/%Y %H:%M')}"


class Medicamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    dose = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicamento'

    def __str__(self):
        return self.nome


class Servico(models.Model):
    id = models.BigAutoField(primary_key=True)
    servico = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'servico'

    def __str__(self):
        return self.servico


class DetalheConsulta(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    notas = models.CharField(max_length=255, blank=True, null=True)
    medicamento = models.ForeignKey(Medicamento, models.DO_NOTHING, blank=True, null=True)
    servico = models.ForeignKey(Servico, models.DO_NOTHING, blank=True, null=True)
    consulta = models.ForeignKey(Consulta, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'detalheconsulta'

    def __str__(self):
        return f"Detalhe da Consulta ID {self.consulta.id}"