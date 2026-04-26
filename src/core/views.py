from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User 
from django.contrib.auth import login

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

# ==========================================
# 2. SISTEMA DE AUTENTICAÇÃO (LOGIN/LOGOUT)
# ==========================================

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pass_word)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Utilizador ou password incorretos'})
            
    return render(request, 'login.html')

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
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # 1. Guarda os dados do Dono primeiro
        response = super().form_valid(form)
        dono = self.object

        # 2. Cria um utilizador no sistema Django para este Dono
        # Usaremos o email como username e o telefone como password temporária
        # (Podes ajustar isto conforme preferires)
        if not User.objects.filter(username=dono.email).exists():
            user = User.objects.create_user(
                username=dono.email, 
                email=dono.email,
                password=dono.telefone # Define a password como o telefone por defeito
            )
            
            # 3. Efetua o login automático do novo utilizador
            login(self.request, user)
            
        return response

class DonoUpdateView(UpdateView):
    model = Dono
    form_class = DonoForm
    template_name = "dono_form.html"
    success_url = reverse_lazy("dono_list")

class DonoDeleteView(DeleteView):
    model = Dono
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("dono_list")

# ==========================================
# 4. GESTÃO DE ANIMAIS
# ==========================================

class AnimalListView(ListView):
    model = Animal
    template_name = "animal_list.html"
    context_object_name = "animais"
    queryset = Animal.objects.select_related("dono").all()

class AnimalDetailView(DetailView):
    model = Animal
    template_name = "animal_detail.html"
    context_object_name = "animal"

class AnimalCreateView(CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = "animal_form.html"
    success_url = reverse_lazy("animal_list")

class AnimalUpdateView(UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = "animal_form.html"
    success_url = reverse_lazy("animal_list")

class AnimalDeleteView(DeleteView):
    model = Animal
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("animal_list")

# ==========================================
# 5. GESTÃO DE CONSULTAS
# ==========================================

class ConsultaListView(ListView):
    model = Consulta
    template_name = "consulta_list.html"
    context_object_name = "consultas"
    queryset = Consulta.objects.select_related("veterinario", "animal").all()

class ConsultaCreateView(CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = "consulta_form.html"
    success_url = reverse_lazy("consulta_list")

class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = "consulta_detail.html"
    context_object_name = "consulta"