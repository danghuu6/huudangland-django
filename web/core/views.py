from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from product.models import Product
from customer.models import Customer
from django.contrib.auth import authenticate, login
# Create your views here.


class HomeView(View):
    def get(self, request):
        product_list = Product.objects.all()
        product_list.reverse()
        return render(request, 'homepage/index.html', {'p': product_list})


class DetailView(View):
    def get(self, request, product_id):
        p = Product.objects.get(pk=product_id)
        return render(request, 'homepage/detail.html', {'pid': p})


class LoginView(View):
    def get(self, request):
        return render(request, 'homepage/login.html')


    def post(self, request):
        user_name = request.POST['username']
        pass_word = request.POST['password']


        my_user = authenticate(request, username=user_name, password=pass_word)
        if my_user is not None:
            login(request, my_user)
            request.session['user_name'] = user_name
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:

                return HttpResponse('dang nhap thanh cong')

class RegisterCustomer(View):
    def get(self, request):
        return render(request, 'homepage/register.html')

    def post(self, request):
        phone_number = request.POST['phone-register']
        name = request.POST['name-register']
        pass_word = request.POST['password-register']
        birthday = request.POST['birthday-register']
        gt = request.POST['modal-radio']

        warn = 'dang ky thanh cong'

        gtdb = True
        if gt == 4:
            gtdb = False

        customer = Customer(phone_number=phone_number, name_customer=name, password=pass_word, date_of_birth=birthday, gt=gtdb)

        customer.save()

        return HttpResponse('dang ky thanh cong')