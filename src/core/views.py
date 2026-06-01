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
    # Página inicial pública do site
    template_name = 'index.html'

    # O motor de contexto do index é responsável por puxar os dados mais relevantes para a homepage, 
    # como os serviços em destaque e a equipa de veterinários
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Slicing [:3] para não inundar a homepage, mostramos só os 3 primeiros serviços do catálogo
        context['servicos'] = Servico.objects.all()[:3]
        # Mandamos a lista de veterinários para aparecerem os cartões da equipa no index
        context['vets'] = Veterinario.objects.all()
        return context
    
class DonoView(DetailView):
    # Página de perfil do cliente, onde ele vê os detalhes da sua conta e o dashboard das suas consultas e animais
    model = Dono
    template_name = "perfil.html"
    context_object_name = "dono"


@login_required
def dono_view(request):
    # Vista principal do perfil do cliente logado. Controla o dashboard dele.
    try:
        # Amarramos o utilizador do Django ao nosso modelo Dono usando o e-mail como chave
        dono = Dono.objects.get(email=request.user.email)
        animais = Animal.objects.filter(dono=dono)
        
        # Organização do painel: não misturar o que já passou com o que ainda vai acontecer
        # Consultas Futuras: Tudo o que for igual ou maior que a hora atual (da mais recente para a mais distante)
        consultas_futuras = Consulta.objects.filter(
            animal__in=animais, 
            data_hora__gte=timezone.now()
        ).order_by('data_hora')
        
        # Histórico de Consultas: Tudo o que ficou para trás (ordenado para mostrar a última onde ele foi no topo)
        consultas_passadas = Consulta.objects.filter(
            animal__in=animais, 
            data_hora__lt=timezone.now()
        ).order_by('-data_hora')
        
    except Dono.DoesNotExist:
        # Se for um superuser ou um admin sem ficha de "Dono" criada, limpa tudo para o ecrã não rebentar com erros
        dono = None
        animais = []
        consultas_futuras = []
        consultas_passadas = []

    # Passamos tudo para o contexto do template para o dashboard do perfil do cliente
    context = {
        'dono': dono,
        'animais': animais,
        'consultas_futuras': consultas_futuras,
        'consultas_passadas': consultas_passadas,
    }
    return render(request, 'perfil.html', context)


@login_required
def desmarcar_consulta(request, pk):
    # Botão de pânico do cliente para cancelar agendamentos
    consulta = get_object_or_404(Consulta, pk=pk)
    
    # Validação de segurança crucial: impede que um esperto mude o ID no URL para apagar consultas de outros donos
    if consulta.animal.dono.email == request.user.email:
        consulta.delete()
        
    # Quando apaga, faz um reload limpo na página de perfil
    return redirect('core:perfil')


# ==========================================
# 2. SISTEMA DE AUTENTICAÇÃO (LOGIN/LOGOUT)
# ==========================================

def login_view(request):
    # Captura o parâmetro '?next=' para saber de onde o utilizador veio antes de ser travado pelo login_required
    next_url = request.GET.get('next') or request.POST.get('next')

    # Se o gajo já estiver logado e tentar aceder à página de login, salta fora para não fazer dupla sessão
    if request.user.is_authenticated:
        return redirect(next_url) if next_url and next_url.startswith('/') else redirect('core:home')

    error_message = None

    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        
        user = authenticate(request, username=user_name, password=pass_word)
        
        if user is not None:
            login(request, user)
            # Se ele vinha a tentar marcar uma consulta e foi travado, o 'next_url' manda-o de volta para o sítio certo
            return redirect(next_url) if next_url and next_url.startswith('/') else redirect('core:home')
        else:
            error_message = 'Utilizador ou palavra-passe incorretos.'

    # Passamos o next para o contexto para o input hidden do HTML segurar o valor no POST
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
        # Puxa a lista de animais atrelados a este dono específico usando a relation
        context["animais"] = self.object.animais.all()
        return context
    
    
class DonoCreateView(CreateView):
    # Processo de registo público na plataforma
    model = Dono
    form_class = DonoForm
    template_name = "registo.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        # 1. Guarda primeiro a ficha técnica do Dono na base de dados
        response = super().form_valid(form)
        dono = self.object

        # 2. Puxa a password limpa e validada que passou nos testes do forms.py
        password_escolhida = form.cleaned_data.get('password')

        # 3. Cria a conta de autenticação oficial do Django (User) usando o e-mail como username
        if not User.objects.filter(username=dono.email).exists():
            user = User.objects.create_user(
                username=dono.email, 
                email=dono.email,
                password=password_escolhida
            )
            
            # 4. Experiência de utilizador fluida: acabou de se registar, fica logo logado automaticamente
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            
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
    # select_related evita fazer centenas de queries à BD para descobrir quem é o dono de cada bicho na listagem
    queryset = Animal.objects.select_related("dono").all()


class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = "animal_detail.html"
    context_object_name = "animal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mostra a folha de histórico médica do bicho, ordenando sempre das consultas mais novas para as mais antigas
        context['consultas'] = Consulta.objects.filter(animal=self.object).order_by('-data_hora')
        return context


class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    success_url = reverse_lazy('core:perfil')

    def form_valid(self, form):
        # Automatismo de segurança: vai buscar o registo Dono associado ao e-mail da sessão atual
        dono_atual = Dono.objects.get(email=self.request.user.email)
        # Injeta o dono diretamente na instância do bicho antes de salvar na BD (assim o user não precisa de se selecionar a si próprio)
        form.instance.dono = dono_atual
        return super().form_valid(form)


class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animal
    form_class = AnimalForm
    template_name = 'animal_form.html'
    
    def get_success_url(self):
        # Concluída a edição, faz reverse dinâmico diretamente para o ecrã de detalhes deste mesmo bicho
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


class ConsultaCreateView(LoginRequiredMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consulta_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicos'] = Servico.objects.all().order_by('servico')
        return context

    def form_valid(self, form):
        form.instance.animal_id = self.kwargs.get('pk')
        response = super().form_valid(form)
        
        servico_id = self.request.POST.get('servico_id')
        if servico_id:
            try:
                servico_objeto = Servico.objects.get(id=servico_id)
                DetalheConsulta.objects.create(
                    consulta=self.object,
                    servico=servico_objeto,
                    medicamento=None,
                    quantidade=1,
                    preco=servico_objeto.preco,
                    notes="Agendamento inicial via catálogo de serviços."
                )
            except Servico.DoesNotExist:
                pass
                
        return response

    def get_success_url(self):
        return reverse_lazy('core:animal_perfil', kwargs={'pk': self.kwargs.get('pk')})


def ajax_horarios_indisponiveis(request):
    veterinario_id = request.GET.get('veterinario_id')
    data_selecionada = request.GET.get('data')

    if not veterinario_id or not data_selecionada:
        return JsonResponse({'horas_indisponiveis': []})

    consultas_ocupadas = Consulta.objects.filter(
        veterinario_id=veterinario_id,
        data_hora__date=data_selecionada
    )
    
    horas_bloqueadas = [consulta.data_hora.strftime('%H:%M') for consulta in consultas_ocupadas]
    return JsonResponse({'horas_indisponiveis': horas_bloqueadas})


# VISTA CORRIGIDA: Agora a Class-Based View injeta os detalhes e calcula o total financeiro!
class ConsultaDetailView(LoginRequiredMixin, DetailView):
    model = Consulta
    template_name = "consulta_detail.html"
    context_object_name = "consulta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Procura as linhas financeiras/médicas desta consulta na tabela intermédia
        context['detalhes'] = DetalheConsulta.objects.filter(
            consulta=self.object
        ).select_related('servico', 'medicamento')
        
        # 2. Motor de cálculo: Soma dinamicamente (Preço * Quantidade) de cada item encontrado
        context['total_consulta'] = sum(item.preco * item.quantidade for item in context['detalhes'])
        
        return context


# Mantemos a função por compatibilidade com as tuas URLs, mas agora corrigida e segura!
@login_required
def consulta_detalhes(request, pk):
    try:
        dono = Dono.objects.get(email=request.user.email)
        consulta = get_object_or_404(Consulta, pk=pk, animal__dono=dono)
    except Dono.DoesNotExist:
        # Fallback para o caso de ser um admin/staff sem ficha de dono criada
        consulta = get_object_or_404(Consulta, pk=pk)
    
    detalhes = DetalheConsulta.objects.filter(consulta=consulta).select_related('servico', 'medicamento')
    total_consulta = sum(item.preco * item.quantidade for item in detalhes)

    context = {
        'consulta': consulta,
        'detalhes': detalhes,
        'total_consulta': total_consulta,
    }
    return render(request, 'consulta_detalhes.html', context)

class ConsultaGeralCreateView(LoginRequiredMixin, CreateView):
    # Fluxo de agendamento global (iniciado fora do perfil do bicho, ex: Menu Principal ou botão do Catálogo)
    model = Consulta
    form_class = ConsultaGeralForm
    template_name = 'consulta_form.html'
    login_url = reverse_lazy('core:login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Passa o utilizador autenticado para o formulário conseguir filtrar o dropdown mostrando apenas os animais dele
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        # Se o utilizador vier da página institucional de serviços e clicou em "Marcar este Serviço", captura o motivo via GET
        motivo_url = self.request.GET.get('motivo')
        if motivo_url:
            # Pré-preenche o campo de texto da caixa de texto do formulário automaticamente com o nome da especialidade
            initial['motivo'] = motivo_url
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Disponibiliza os serviços para o motor JS de seleção de preços do template
        context['servicos'] = Servico.objects.all().order_by('servico')
        return context

    def form_valid(self, form):
        # Salva o agendamento geral primeiro
        response = super().form_valid(form)
        
        # Cria a ligação automática de faturação idêntica à vista focada no animal
        servico_id = self.request.POST.get('servico_id')
        if servico_id:
            try:
                servico_objeto = Servico.objects.get(id=servico_id)
                DetalheConsulta.objects.create(
                    consulta=self.object,
                    servico=servico_objeto,
                    medicamento=None,
                    quantidade=1,
                    preco=servico_objeto.preco,
                    notas="Agendamento inicial via catálogo de serviços."
                )
            except Servico.DoesNotExist:
                pass
                
        return response

    def get_success_url(self):
        # Como este fluxo partiu do menu global, faz todo o sentido devolver o utilizador ao seu painel geral de perfil
        return reverse_lazy('core:perfil')
    

# ==========================================
# 6. GESTÃO DE SERVIÇOS E MEDICAMENTOS
# ==========================================

class ServicoListView(ListView):
    model = Servico
    template_name = "servico_list.html"
    context_object_name = "servicos"


class ServicoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Zona de parametrização interna de preços e exames
    model = Servico
    form_class = ServicoForm
    template_name = "servico_form.html"
    success_url = reverse_lazy("core:servico_list")

    def test_func(self):
        # Trava de segurança administrativa: apenas membros internos ou administradores (staff) editam tabelas de preços
        return self.request.user.is_staff


class MedicamentoListView(ListView):
    model = Medicamento
    template_name = "medicamento_list.html"
    context_object_name = "medicamentos"


class MedicamentoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Gestão do armazém/farmácia da clínica veterinária
    model = Medicamento
    form_class = MedicamentoForm
    template_name = "medicamento_form.html"
    success_url = reverse_lazy("core:medicamento_list")

    def test_func(self):
        # Bloqueio de segurança igual ao do catálogo de serviços
        return self.request.user.is_staff


# ==========================================
# 7. FATURAÇÃO / DETALHES DA CONSULTA
# ==========================================

class DetalheConsultaCreateView(CreateView):
    # Introdução manual de consumíveis e tratamentos durante ou após o ato médico na clínica
    model = DetalheConsulta
    form_class = DetalheConsultaForm
    template_name = "detalheconsulta_form.html"

    def get_initial(self):
        initial = super().get_initial()
        # Captura o ID da consulta injetado na URL da rota (/consulta/<id>/adicionar-linha/)
        # Facilita a vida ao médico preenchendo logo a que consulta esta linha pertence, escusando de procurar numa lista gigante
        initial['consulta'] = self.kwargs.get('consulta_id')
        return initial

    def get_success_url(self):
        # Assim que o médico adiciona o item (ex: uma vacina), recarrega de imediato o ecrã de resumo dessa mesma consulta
        return reverse_lazy('core:consulta_detail', kwargs={'pk': self.kwargs.get('consulta_id')})