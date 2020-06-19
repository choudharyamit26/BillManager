import csv
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils.translation import gettext, gettext_lazy as _
from django.db.models import Q
from django.template.loader import get_template
from django.template import Context
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (View,
                                  CreateView,
                                  TemplateView,
                                  ListView,
                                  DetailView,
                                  DeleteView,
                                  UpdateView)

from .forms import BillForm, ProductForm, ClientForm, BillUpdateForm, ClientUpdateForm, ProductUpdateForm, \
    OrderItemForm, BillFormSet
from .forms import SignUpForm
from .pdf import render_to_pdf
from .models import Bill, Client, Product, OrderItem
from .numtoword import num_to_word
from .filters import BillFilter


class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        form = SignUpForm(self.request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                self.request, f'Account has been created for {username}! You can now login.')
            return redirect("src:login")
        else:
            form = SignUpForm(self.request.POST)
        return render(self.request, 'register.html', {'form': form})


# class HomeView(TemplateView):
#     template_name = 'home.html'

#     def home(self):
#         return render(self.request, 'home.html')


# class LandingView(TemplateView):
#     template_name = 'first.html'

#     def home(self):
#         return render(self.request, 'first.html')


class BillView(LoginRequiredMixin, CreateView):
    model = Bill
    template_name = 'bill.html'
    form_class = BillForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = BillFormSet(queryset=OrderItem.objects.none())
        context['billform'] = BillForm()
        context['product'] = Product.objects.all()
        return context

    def form_valid(self, form):
        formset = BillFormSet(self.request.POST)
        buyer = form.cleaned_data['buyer']
        buyer_address = form.cleaned_data['buyer_address']
        buyer_gst = form.cleaned_data['buyer_gst']
        instances = formset.save(commit=False)
        order_id = get_random_string(16)
        for instance in instances:
            instance.user = self.request.user
            instance.buyer = buyer
            instance.buyer_address = buyer_address
            instance.buyer_gst = buyer_gst
            instance.order_id = order_id
            instance.ordered = True
            instance.save()
        if instance:
            order = instance.order_id
            ordered_items = OrderItem.objects.filter(order_id=order)
            bill = Bill.objects.create(
                user=self.request.user,
                buyer=buyer,
                buyer_address=buyer_address,
                buyer_gst=buyer_gst,
            )

            for x in ordered_items:
                bill.items.add(x)
        return redirect(bill)

    def form_invalid(self, form):
        messages.error(self.request, 'Some error occured please check.')
        return self.render_to_response(self.get_context_data(form=form))


class ClientView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'client.html'
    form_class = ClientForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product.html'
    form_class = ProductForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class BillList(LoginRequiredMixin, View):
    model = Bill
    template_name = 'bill_list.html'

    def get(self, request, *args, **kwargs):
        data = Bill.objects.filter(user=self.request.user)
        myfilter = BillFilter(self.request.GET, queryset=data)
        formlist = Bill.objects.filter(user=self.request.user)
        filter_data = myfilter.qs
        count = len(formlist)
        paginator = Paginator(formlist, 10)
        page = request.GET.get('page')
        formlist = paginator.get_page(page)
        context = {
            'formlist': formlist,
            'count': count,
            'myfilter': myfilter,
            'filter_data': filter_data
        }
        return render(self.request, "bill_list.html", context)

    def post(self, request, *args, **kwargs):
        qs = self.request.POST.get('qs')
        if qs:
            search = Bill.objects.filter(Q(buyer__name__icontains=qs) |
                                         Q(id__icontains=qs) |
                                         Q(buyer_address__icontains=qs) |
                                         Q(date__icontains=qs))

            search_count = len(search)
            context = {
                'search': search,
                'search_count': search_count
            }
            if search:
                messages.info(self.request, str(
                    search_count) + ' matches found')
                return render(self.request, 'bill_list.html', context)
            else:
                messages.info(self.request, 'No results found')
                return render(self.request, 'bill_list.html', context)
        else:
            messages.info(self.request, 'Please enter some text  ')
            return redirect('src:bill-list')


class BillFilterView(LoginRequiredMixin, ListView):
    model = Bill

    def get(self, request, *args, **kwargs):
        data = Bill.objects.filter(user=self.request.user)
        myFilter = BillFilter(self.request.GET, queryset=data)
        filter_data = myFilter.qs
        context = {
            'myfilter': myFilter,
            'filter_data': filter_data
        }
        return render(self.request, "filetered_list.html", context)


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(user=self.request.user)
        context = {
            'product': product
        }
        return render(self.request, "product_list.html", context)


class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'

    def get(self, request, *args, **kwargs):
        clients = Client.objects.filter(user=self.request.user)
        context = {
            'client': clients
        }
        return render(self.request, "client_list.html", context)


class BillDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = "bill-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['something'] = Bill.objects.filter(pk=self.kwargs.get('pk'))
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product-detail.html"
    form_class = ProductForm


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client-detail.html"
    form_class = ClientForm


class BillUpdateView(LoginRequiredMixin, UpdateView):
    model = Bill
    template_name = "bill-update.html"
    form_class = BillForm
    success_url = reverse_lazy('src:bill-list')

    

    def get_object(self,queryset=None):
        if queryset is None:
            queryset = self.get_queryset().order_by('id')
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        obj = queryset.get()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = OrderItem.objects.filter(bill=self.get_object())
        formset = BillFormSet(queryset=qs)
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = BillFormSet(self.request.POST)
        if (form.is_valid() and formset.is_valid()):
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = "client-update.html"
    form_class = ClientUpdateForm
    success_url = reverse_lazy('src:client-list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = "product-update.html"
    success_url = reverse_lazy('src:product-list')


class BillDeleteView(LoginRequiredMixin, DeleteView):
    model = Bill
    template_name = "bill-delete.html"
    form_class = BillUpdateForm
    success_url = reverse_lazy('src:bill-list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "client-delete.html"
    form_class = BillUpdateForm
    success_url = reverse_lazy('src:client-list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product-delete.html"
    form_class = BillUpdateForm
    success_url = reverse_lazy('src:product-list')


class GeneratePDF(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        template = get_template('invoice.html')
        bill = Bill.objects.get(pk=self.kwargs.get('pk'))
        something = Bill.objects.filter(pk=self.kwargs.get('pk'))
        context = {
            'bill': bill,
            'something': something
        }
        # html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        return HttpResponse(pdf, content_type='application/pdf')


class BillDownloadView(LoginRequiredMixin, View):
    model = Bill

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bills.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['Buyer', 'Buyer Gst', 'Buyer Address', 'Date', 'Product', 'Quantity', 'Price', 'Order Id'])
        bills = Bill.objects.all().values_list('buyer__name', 'buyer_gst', 'buyer_address', 'date',
                                               'items__product__product_name', 'items__quantity', 'items__price', 'items__order_id')
        for bill in bills:
            writer.writerow(bill)
        return response
