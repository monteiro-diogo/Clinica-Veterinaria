from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Dono, Animal, Veterinario, Consulta, Servico
from .forms import DonoForm, AnimalForm, ConsultaForm

# ==========================================
# 1. HOME & PÁGINAS GERAIS
# ==========================================

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Enviamos dados para o index ficar dinâmico
        context['servicos'] = Servico.objects.all()[:3]
        context['vets'] = Veterinario.objects.all()
        return context
    
class DonoView(DetailView):
    model = Dono
    template_name = "perfil.html"
    context_object_name = "dono"

@login_required
def dono_view(request):
    try:
        dono = Dono.objects.get(email=request.user.email)
        animais = Animal.objects.filter(dono=dono)
        
        consultas = Consulta.objects.filter(animal__in=animais).order_by('-data_hora')
        
    except Dono.DoesNotExist:
        dono = None
        animais = []
        consultas = []

    context = {
        'dono': dono,
        'animais': animais,
        'consultas': consultas,
    }
    
    return render(request, 'perfil.html', context)


# ==========================================
# 2. SISTEMA DE AUTENTICAÇÃO (LOGIN/LOGOUT)
# ==========================================

def login_view(request):
    # Se o utilizador já está logado, manda-o para a home (evita login duplo)
    if request.user.is_authenticated:
        return redirect('home')

    error_message = None # Inicializamos a variável

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        user = authenticate(request, username=user_name, password=pass_word)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Definimos a mensagem aqui
            error_message = 'Utilizador ou palavra-passe incorretos.'

    # Passamos a variável de erro (que será None se for um GET ou preenchida se falhar o POST)
    return render(request, 'login.html', {'error': error_message})

def logout_view(request):
    logout(request)
    return redirect('home')

# ==========================================
# 3. GESTÃO DE DONOS (CLIENTES)
# ==========================================

class DonoListView(ListView):
    model = Dono
    template_name = "dono_list.html"
    context_object_name = "donos"

class DonoDetailView(DetailView):
    model = Dono
    template_name = "dono_detail.html"
    context_object_name = "dono"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["animais"] = self.object.animais.all()
        return context
    
    
# Esta view serve para o Registo Público ou Adição manual pelo Admin
class DonoCreateView(CreateView):
    model = Dono
    form_class = DonoForm
    template_name = "registro.html" # O ficheiro bonito com CSS que criámos
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # 1. Guarda os dados do Dono primeiro (Cria o registo na tabela Dono)
        response = super().form_valid(form)
        dono = self.object

        # 2. Pega na password que o utilizador escolheu no formulário
        # O 'cleaned_data' garante que pegamos na password já validada pelo forms.py
        password_escolhida = form.cleaned_data.get('password')

        # 3. Cria um utilizador no sistema Django para este Dono
        if not User.objects.filter(username=dono.email).exists():
            user = User.objects.create_user(
                username=dono.email, 
                email=dono.email,
                password=password_escolhida # Agora usa a password real escolhida
            )
            
            # 4. Efetua o login automático do novo utilizador
            login(self.request, user)
            
        return response

class DonoUpdateView(UpdateView):
    model = Dono
    form_class = DonoForm
    template_name = "dono_form.html"
    success_url = reverse_lazy("core:dono_list")

class DonoDeleteView(DeleteView):
    model = Dono
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("core:dono_list")

# ==========================================
# 4. GESTÃO DE ANIMAIS
# ==========================================

class AnimalListView(ListView):
    model = Animal
    template_name = "animal_list.html"
    context_object_name = "animais"
    queryset = Animal.objects.select_related("dono").all()

# Garante que tens a Consulta importada no topo do teu views.py:
# from .models import Animal, Dono, Consulta
class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = "animal_detail.html"
    context_object_name = "animal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puxa todas as consultas deste animal específico, ordenadas pela data mais recente
        context['consultas'] = Consulta.objects.filter(animal=self.object).order_by('-data_hora')
        return context

class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    success_url = reverse_lazy('core:perfil')

    def form_valid(self, form):
        dono_atual = Dono.objects.get(email=self.request.user.email)
        form.instance.dono = dono_atual  # Associa automaticamente
        return super().form_valid(form)


# 3. EDITAR ANIMAL
class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    
    def get_success_url(self):
        # Quando acaba de editar, volta para o perfil do próprio animal
        return reverse_lazy('core:animal_perfil', kwargs={'pk': self.object.pk})

class AnimalDeleteView(DeleteView):
    model = Animal
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("core:animal_list")

# ==========================================
# 5. GESTÃO DE CONSULTAS
# ==========================================

class ConsultaListView(ListView):
    model = Consulta
    template_name = "consulta_list.html"
    context_object_name = "consultas"
    queryset = Consulta.objects.select_related("veterinario", "animal").all()

# 4. MARCAR CONSULTA (Animal Automático via URL)
class ConsultaCreateView(LoginRequiredMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consulta_form.html'

    def form_valid(self, form):
        # Captura o id do animal diretamente a partir da URL e associa-o à consulta
        form.instance.animal_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        # Quando a consulta é marcada, volta para o perfil deste mesmo animal
        return reverse_lazy('core:animal_perfil', kwargs={'pk': self.kwargs.get('pk')})
    
class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = "consulta_detail.html"
    context_object_name = "consulta"