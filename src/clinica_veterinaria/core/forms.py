from django import forms
from .models import Dono, Animal, Veterinario, Consulta, Medicamento, Servico, DetalheConsulta

class DonoForm(forms.ModelForm):
    class Meta:
        model = Dono
        fields = ['nome', 'nif', 'telefone', 'email']

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'raca', 'data_nascimento', 'dono']

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = ['nome', 'celula_profissional', 'especialidade', 'telefone']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['data_hora', 'motivo', 'observacoes', 'veterinario', 'animal']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'fabricante', 'dose']

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['servico', 'preco']

class DetalheConsultaForm(forms.ModelForm):
    class Meta:
        model = DetalheConsulta
        fields = ['consulta', 'servico', 'medicamento', 'quantidade', 'preco', 'notas']