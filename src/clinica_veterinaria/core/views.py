from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Dono, Animal, Veterinario, Consulta
from .forms import DonoForm, AnimalForm, ConsultaForm

# Home
class HomeView(TemplateView):
    template_name = 'index.html'

# --- DONOS ---
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
        # Seguindo a lógica do professor de listar itens relacionados
        context["animais"] = self.object.animais.all()
        return context

class DonoCreateView(CreateView):
    model = Dono
    form_class = DonoForm
    template_name = "dono_form.html"
    success_url = reverse_lazy("dono_list")

class DonoUpdateView(UpdateView):
    model = Dono
    form_class = DonoForm
    template_name = "dono_form.html"
    success_url = reverse_lazy("dono_list")

class DonoDeleteView(DeleteView):
    model = Dono
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("dono_list")

# --- ANIMAIS ---
class AnimalListView(ListView):
    model = Animal
    template_name = "animal_list.html"
    context_object_name = "animais"
    # Otimização de base de dados usando select_related como no exemplo
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

# --- CONSULTAS ---
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