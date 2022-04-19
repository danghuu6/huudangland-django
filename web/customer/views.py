from django.shortcuts import render
from django.views import View
from .models import Customer
# Create your views here.


class RegisterCustomer(View):
    def register(self, request):
        phone_number = request.POST['phone-register']
        name = request.POST['name-register']
        pass_word = request.POST['password-register']
        birthday = request.POST['birthdat-register']
        gt = request.POST['modal-radio']

        warn = 'dang ky thanh cong'

        gtdb = True
        if gt == 2:
            gtdb = False


        try:
            customer = Customer(phone_number='phone_number', name_customer='name', password='pass_word', date_of_birth='birthday',
                                gt='gtdb')

            customer.save()
        except:
            warn = 'dang ky that bai'
            return render(request, 'homepage/test.html', {'w': warn})

        return render(request, 'homepage/test.html', {'w': warn})
