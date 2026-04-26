from django.contrib import admin
from .models import Dono, Animal, Veterinario, Consulta, Servico

admin.site.register(Dono)
admin.site.register(Animal)
admin.site.register(Veterinario)
admin.site.register(Consulta)
admin.site.register(Servico)