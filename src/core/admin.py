from django.contrib import admin
from .models import Dono, Animal, Veterinario, Consulta, Medicamento, Servico, DetalheConsulta

# Registar os modelos para aparecerem no Dashboard
admin.site.register(Dono)
admin.site.register(Animal)
admin.site.register(Veterinario)
admin.site.register(Consulta)
admin.site.register(Medicamento)
admin.site.register(Servico)
admin.site.register(DetalheConsulta)    