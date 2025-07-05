from django.forms import BaseModelForm
from django.http import HttpResponse
from .models import ExpenseIncome
from django.views.generic import(
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView )




class ExposeListView(ListView):
    model = ExpenseIncome
    template_name = 'expose_list.html'
    context_object_name = 'exposes'


class ExposeDetailView(DetailView):
    model = ExpenseIncome
    template_name = 'expose_detail.html'
    context_object_name = 'expose'
    
class ExposeCreateView(CreateView):
    model = ExpenseIncome
    template_name = 'expose_form.html'
    fields = ['title', 'description', 'amount','transaction_type','tax','tax_type']
    success_url = '/'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)

class ExposeUpdateView(UpdateView):
    model = ExpenseIncome
    template_name = 'expose_form.html'
    fields = ['title', 'description', 'amount','transaction_type','tax','tax_type']
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)

class ExposeDeleteView(DeleteView):
    model = ExpenseIncome
    template_name = 'expose_confirm_delete.html'
    success_url = '/'
    