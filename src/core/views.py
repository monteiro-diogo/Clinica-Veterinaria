from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.utils import timezone

from .models import Dono, Animal, Veterinario, Consulta, Medicamento, Servico, DetalheConsulta
from .forms import DonoForm, AnimalForm, ConsultaForm, ConsultaGeralForm, MedicamentoForm, ServicoForm, DetalheConsultaForm

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
        
        # --- ALTERAÇÃO: Filtro cronológico das consultas ---
        # Consultas Futuras: da mais próxima para a mais distante (>= agora)
        consultas_futuras = Consulta.objects.filter(
            animal__in=animais, 
            data_hora__gte=timezone.now()
        ).order_by('data_hora')
        
        # Consultas Passadas: da mais recente para a mais antiga (< agora)
        consultas_passadas = Consulta.objects.filter(
            animal__in=animais, 
            data_hora__lt=timezone.now()
        ).order_by('-data_hora')
        
    except Dono.DoesNotExist:
        dono = None
        animais = []
        consultas_futuras = []
        consultas_passadas = []

    context = {
        'dono': dono,
        'animais': animais,
        'consultas_futuras': consultas_futuras,  # Enviado para a nova tabela
        'consultas_passadas': consultas_passadas,  # Enviado para o histórico
    }
    
    return render(request, 'perfil.html', context)


# --- Cancelamento de consultas pelo cliente ---
@login_required
def desmarcar_consulta(request, pk):
    # Procura a consulta ou retorna erro 404 caso não exista
    consulta = get_object_or_404(Consulta, pk=pk)
    
    # Validação de Segurança: Garante que o utilizador logado é mesmo o dono do animal da consulta
    if consulta.animal.dono.email == request.user.email:
        consulta.delete()
        
    # Redireciona de volta para a página de perfil (ajusta o nome da rota se necessário)
    return redirect('core:perfil')


# ==========================================
# 2. SISTEMA DE AUTENTICAÇÃO (LOGIN/LOGOUT)
# ==========================================

def login_view(request):
    # Capta o URL de destino pretendido antes do login ser forçado
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.user.is_authenticated:
        return redirect(next_url) if next_url and next_url.startswith('/') else redirect('core:home')

    error_message = None

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        user = authenticate(request, username=user_name, password=pass_word)
        
        if user is not None:
            login(request, user)
            return redirect(next_url) if next_url and next_url.startswith('/') else redirect('core:home')
        else:
            error_message = 'Utilizador ou palavra-passe incorretos.'

    # Passamos o next_url para o template para o não perdermos ao submeter o POST
    return render(request, 'login.html', {'error': error_message, 'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('core:home')

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


# <<< NOVA VIEW PARA AJUSTE DOS HORÁRIOS DISPONÍVEIS (ISOLADA DA CLASSE) >>>
def ajax_horarios_indisponiveis(request):
    """
    View AJAX independente que devolve as horas já ocupadas de um veterinário numa data.
    """
    veterinario_id = request.GET.get('veterinario_id')
    data_selecionada = request.GET.get('data')  # Recebe o formato 'YYYY-MM-DD' vindo do HTML

    # Se faltar algum dos parâmetros, devolvemos uma lista vazia para evitar erros catastróficos
    if not veterinario_id or not data_selecionada:
        return JsonResponse({'horas_indisponiveis': []})

    # Como o teu modelo usa o campo unificado 'data_hora', aplicamos o filtro '__date' 
    # para extrair e comparar apenas o dia na Base de Dados.
    consultas_ocupadas = Consulta.objects.filter(
        veterinario_id=veterinario_id,
        data_hora__date=data_selecionada
    )
    
    # Extrai apenas as horas formatadas como "HH:MM" para bater certo com os quadrados do ecrã
    horas_bloqueadas = [consulta.data_hora.strftime('%H:%M') for consulta in consultas_ocupadas]

    # Devolve a resposta limpa em formato JSON para o JavaScript ler
    return JsonResponse({'horas_indisponiveis': horas_bloqueadas})


class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = "consulta_detail.html"
    context_object_name = "consulta"

class ConsultaGeralCreateView(LoginRequiredMixin, CreateView):
    model = Consulta
    form_class = ConsultaGeralForm
    template_name = 'consulta_form.html'
    login_url = reverse_lazy('core:login') # Redireciona para a tua página de login se o user for anónimo

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Injeta o utilizador autenticado no formulário para filtrar a query
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        # Após guardar, o utilizador regressa ao seu perfil onde os dados já estarão refletidos
        return reverse_lazy('core:perfil')
    
    #serviços -> marcaçao
    def get_initial(self):
        initial = super().get_initial()
        # Captura o valor de 'motivo' enviado pela URL (se existir)
        motivo_url = self.request.GET.get('motivo')
        if motivo_url:
            # Preenche o campo 'motivo' do teu formulário automaticamente
            initial['motivo'] = motivo_url
        return initial

    def get_success_url(self):
        return reverse_lazy('core:perfil')

    
# ==========================================
# 6. GESTÃO DE SERVIÇOS E MEDICAMENTOS
# ==========================================

class ServicoListView(ListView):
    model = Servico
    template_name = "servico_list.html"
    context_object_name = "servicos"

class ServicoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = "servico_form.html"
    success_url = reverse_lazy("core:servico_list")

    # (admin/funcionário)
    def test_func(self):
        return self.request.user.is_staff

class MedicamentoListView(ListView):
    model = Medicamento
    template_name = "medicamento_list.html"
    context_object_name = "medicamentos"

class MedicamentoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = "medicamento_form.html"
    success_url = reverse_lazy("core:medicamento_list")

    # (admin/funcionário)
    def test_func(self):
        return self.request.user.is_staff

# ==========================================
# 7. FATURAÇÃO / DETALHES DA CONSULTA
# ==========================================

class DetalheConsultaCreateView(CreateView):
    model = DetalheConsulta
    form_class = DetalheConsultaForm
    template_name = "detalheconsulta_form.html"

    def get_initial(self):
        # Trade-off: Preenchemos a consulta de forma automática através do ID passado no URL,
        # melhorando a experiência do utilizador ao evitar que este tenha de procurar a consulta numa lista extensa.
        initial = super().get_initial()
        initial['consulta'] = self.kwargs.get('consulta_id')
        return initial

    def get_success_url(self):
        # Após adicionar um detalhe (ex: vacina ou tosquia), regressa à página da consulta correspondente
        return reverse_lazy('core:consulta_detail', kwargs={'pk': self.kwargs.get('consulta_id')})