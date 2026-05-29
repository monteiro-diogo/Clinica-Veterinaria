from django import forms
from .models import Dono, Animal, Veterinario, Consulta, Medicamento, Servico, DetalheConsulta

# O DonoForm é um formulário para criar ou editar donos de animais. Ele inclui campos para o nome, NIF, telefone e email do dono, bem como campos adicionais para a criação de uma conta de utilizador (password e confirm_password). A validação personalizada garante que as palavras-passe inseridas sejam iguais.
class DonoForm(forms.ModelForm):
    # Campos extra para a conta de utilizador
    password = forms.CharField(
        label="Palavra-passe*",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite uma password segura'}),
        required=True
    )
    confirm_password = forms.CharField(
        label="Confirmar Palavra-passe*",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita a password'}),
        required=True
    )

    class Meta:
        model = Dono
        fields = ['nome', 'nif', 'telefone', 'email']

        labels = {
            'nome': 'Nome Completo*',
            'nif': 'NIF (Opcional)',
            'telefone': 'Telemóvel*',
            'email': 'Email*',
        }

    # Validação: verifica se as duas passwords são iguais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            # Se forem diferentes, o Django mostra este erro no formulário
            self.add_error('confirm_password', "As palavras-passe não coincidem!")

        return cleaned_data
    
    # Sobrescreve o método __init__ para tornar o campo email obrigatório, já que é essencial para a criação da conta de utilizador.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True # Força o email a ser obrigatório no formulário
    
# O AnimalForm é um formulário para criar ou editar animais. Ele inclui campos para o nome, espécie, raça, data de nascimento e uma foto do animal. O Django irá gerar automaticamente os campos de formulário com base no modelo Animal.
ESPECIE_CHOICES = [
    ('Cão', 'Cão'),
    ('Gato', 'Gato'),   
    ('Coelho', 'Coelho'),
    ('Hamster', 'Hamster'),
    ('Porquinho-da-Índia', 'Porquinho-da-Índia'),
    ('Furão', 'Furão'),
    ('Chinchila', 'Chinchila'),
    ('Rato', 'Rato'),
    ('Tartaruga', 'Tartaruga'),
    ('Iguana', 'Iguana'),
    ('Lagarto', 'Lagarto'),
    ('Cobra', 'Cobra'),
    ('Peixe', 'Peixe'),
    ('Papagaio', 'Papagaio'),
    ('Canário', 'Canário'),
    ('Periquito', 'Periquito'),
    ('Galinha', 'Galinha'),
    ('Pato', 'Pato'),
    ('Cabra', 'Cabra'),
    ('Ovelha', 'Ovelha'),
    ('Porco', 'Porco'),
    ('Cavalo', 'Cavalo'),
    ('Burro', 'Burro'),
    ('Outro', 'Outro'),
]

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome', 'especie', 'raca', 'data_nascimento', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'especie': forms.Select(choices=ESPECIE_CHOICES, attrs={'class': 'form-input'}),
            'raca': forms.TextInput(attrs={'class': 'form-input'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'foto': forms.FileInput(attrs={'class': 'form-input'}),
        }
        
        labels = {
            'nome': 'Nome do Patudo*',
            'especie': 'Espécie*',
            'raca': 'Raça (Opcional)',
            'data_nascimento': 'Data de Nascimento (Opcional)',
            'foto': 'Fotografia (Opcional)',
        }

# VeterinárioForm é um formulário simples para criar ou editar veterinários. Ele inclui os campos básicos como nome, número de cédula profissional, especialidade e telefone. O Django irá gerar automaticamente os campos de formulário com base no modelo Veterinario.
class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = ['nome', 'celula_profissional', 'especialidade', 'telefone']

# ConsultaForm atual foi desenhado para ser acedido através do perfil de um animal específico, por isso o campo 'animal' não é necessário (será preenchido automaticamente).
class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        # O campo 'animal' fica de fora porque será automático
        fields = ['data_hora', 'motivo', 'observacoes', 'veterinario']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'motivo': forms.TextInput(attrs={'class': 'form-input'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'veterinario': forms.Select(attrs={'class': 'form-input'}),
        }

# Os formulários para Medicamento, Serviço e DetalheConsulta são simples e incluem os campos relevantes para cada modelo. O Django irá gerar automaticamente os campos de formulário com base nos modelos correspondentes.
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nome', 'fabricante', 'dose']

# O ServicoForm é um formulário para criar ou editar serviços oferecidos pela clínica. Ele inclui campos para o nome do serviço e o preço.
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['servico', 'preco']

# O DetalheConsultaForm é um formulário para criar ou editar detalhes de uma consulta. Ele inclui campos para a consulta associada, o serviço prestado, o medicamento utilizado, a quantidade, o preço e quaisquer notas adicionais.
class DetalheConsultaForm(forms.ModelForm):
    class Meta:
        model = DetalheConsulta
        fields = ['consulta', 'servico', 'medicamento', 'quantidade', 'preco', 'notas']

# O ConsultaGeralForm é um formulário mais abrangente para criar ou editar consultas, incluindo a possibilidade de selecionar o animal associado à consulta. Ele também inclui uma validação personalizada para garantir que o dono só possa selecionar os seus próprios animais.
class ConsultaGeralForm(forms.ModelForm):
    class Meta:
        model = Consulta
        # Incluímos o campo 'animal' para que o dono o possa selecionar
        fields = ['animal', 'veterinario', 'data_hora', 'motivo', 'observacoes']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-input'}),
            'veterinario': forms.Select(attrs={'class': 'form-input'}),
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'motivo': forms.TextInput(attrs={'class': 'form-input'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Captura o utilizador logado passado pela view
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtra a lista de animais para exibir apenas os que pertencem ao utilizador atual
        if user and user.is_authenticated:
            try:
                dono = Dono.objects.get(email=user.email)
                self.fields['animal'].queryset = Animal.objects.filter(dono=dono)
            except Dono.DoesNotExist:
                self.fields['animal'].queryset = Animal.objects.none()