from django import forms
from .models import Dono, Animal, Veterinario, Consulta, Medicamento, Servico, DetalheConsulta

class DonoForm(forms.ModelForm):
    # Campos extra para a conta de utilizador
    password = forms.CharField(
        label="Palavra-passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite uma password segura'}),
        required=True
    )
    confirm_password = forms.CharField(
        label="Confirmar Palavra-passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a password'}),
        required=True
    )

    class Meta:
        model = Dono
        # Mantemos os campos originais do teu modelo Dono
        fields = ['nome', 'nif', 'telefone', 'email']

    # Validação: verifica se as duas passwords são iguais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            # Se forem diferentes, o Django mostra este erro no formulário
            self.add_error('confirm_password', "As palavras-passe não coincidem!")

        return cleaned_data
    

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'raca', 'data_nascimento', 'dono']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

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