from django.shortcuts import render, redirect
from django.views import View
from product.models import Product
from customer.models import Customer
from feedback.models import Feedback
from predict.models import Predict, Parameter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.


class HomeView(View):
    def get(self, request):
        loai_bds = request.GET.get('loai-bds')
        address_filter = request.GET.get('dia-diem')
        price_filter = request.GET.get('price-filter')
        search_name = request.GET.get('search')
        sort_filter = request.GET.get('sort-filter')

        price_min = 0
        price_max = 0

        if price_filter == 'lessthan1ty':
            price_min = 1
            price_max = 1000000000
        if price_filter == 'fr1tyto5ty':
            price_min = 1000000000
            price_max = 5000000000
        if price_filter == 'fr5tyto10ty':
            price_min = 5000000000
            price_max = 10000000000
        if price_filter == 'morethan10ty':
            price_max = 10000000000

        #Filter

        if loai_bds and address_filter and price_filter and sort_filter:
            if loai_bds == 'dat_nen':
                if price_max == 10000000000:
                    product_list = Product.objects.filter(floors=0, address__icontains=address_filter, price__gt=price_max).order_by(sort_filter)
                else:
                    product_list = Product.objects.filter(floors=0, address__icontains=address_filter, price__range=[price_min, price_max]).order_by(sort_filter)
            else:
                if price_max == 10000000000:
                    product_list = Product.objects.filter(floors__gt=0, address__icontains=address_filter, price__gt=price_max).order_by(sort_filter)
                else:
                    product_list = Product.objects.filter(floors__gt=0, address__icontains=address_filter, price__range=[price_min, price_max]).order_by(sort_filter)
        elif address_filter and price_filter:
            if sort_filter:
                if price_max == 10000000000:
                    product_list = Product.objects.filter(address__icontains=address_filter, price__gt=price_max).order_by(sort_filter)
                else:
                    product_list = Product.objects.filter(address__icontains=address_filter, price__range=[price_min, price_max]).order_by(sort_filter)
            else:
                if price_max == 10000000000:
                    product_list = Product.objects.filter(address__icontains=address_filter, price__gt=price_max)
                else:
                    product_list = Product.objects.filter(address__icontains=address_filter, price__range=[price_min, price_max])
        elif address_filter and loai_bds:
            if sort_filter:
                if loai_bds == 'dat_nen':
                    product_list = Product.objects.filter(floors=0, address__icontains=address_filter).order_by(sort_filter)
                else:
                    product_list = Product.objects.filter(floors__gt=0, address__icontains=address_filter).order_by(sort_filter)
            else:
                if loai_bds == 'dat_nen':
                    product_list = Product.objects.filter(floors=0, address__icontains=address_filter)
                else:
                    product_list = Product.objects.filter(floors__gt=0, address__icontains=address_filter)
        elif loai_bds and price_filter:
            if sort_filter:
                if loai_bds == 'dat_nen':
                    if price_max == 10000000000:
                        product_list = Product.objects.filter(floors=0, price__gt=price_max).order_by(sort_filter)
                    else:
                        product_list = Product.objects.filter(floors=0, price__range=[price_min, price_max]).order_by(sort_filter)
                else:
                    if price_max == 10000000000:
                        product_list = Product.objects.filter(floors__gt=0, price__gt=price_max).order_by(sort_filter)
                    else:
                        product_list = Product.objects.filter(floors__gt=0, price__range=[price_min, price_max]).order_by(sort_filter)
            else:
                if loai_bds == 'dat_nen':
                    if price_max == 10000000000:
                        product_list = Product.objects.filter(floors=0, price__gt=price_max)
                    else:
                        product_list = Product.objects.filter(floors=0, price__range=[price_min, price_max])
                else:
                    if price_max == 10000000000:
                        product_list = Product.objects.filter(floors__gt=0, price__gt=price_max)
                    else:
                        product_list = Product.objects.filter(floors__gt=0, price__range=[price_min, price_max])
        elif loai_bds:
            if sort_filter:
                if loai_bds == 'dat_nen':
                    product_list = Product.objects.filter(floors=0).order_by(sort_filter)
                else:
                    product_list = Product.objects.filter(floors__gt=0).order_by(sort_filter)
            else:
                if loai_bds == 'dat_nen':
                    product_list = Product.objects.filter(floors=0)
                else:
                    product_list = Product.objects.filter(floors__gt=0)
        elif address_filter:
            if sort_filter:
                product_list = Product.objects.filter(address__icontains=address_filter).order_by(sort_filter)
            else:
                product_list = Product.objects.filter(address__icontains=address_filter)
        elif price_filter:
            if sort_filter:
                if price_max == 10000000000:
                    product_list = Product.objects.filter(price__gt=price_max).order_by(sort_filter)
                else:
                    product_list = Product.objects.filter(price__range=[price_min, price_max]).order_by(sort_filter)
            else:
                if price_max == 10000000000:
                    product_list = Product.objects.filter(price__gt=price_max)
                else:
                    product_list = Product.objects.filter(price__range=[price_min, price_max])
        elif search_name is not None:
            product_list = Product.objects.filter(Q(title__icontains=search_name) | Q(address__icontains=search_name))
        elif sort_filter:
            product_list = Product.objects.all().order_by(sort_filter)
        else:
            product_list = Product.objects.all().order_by('-id')

        for i in product_list:
            i.address = i.address.split(',')
            i.address[-1] = i.address[-1].lstrip(' ')
            i.address[-2] = i.address[-2].lstrip(' ')
            i.address = i.address[-2:]
            i.address = ', '.join(i.address)

        for j in product_list:
            j.image = j.image.split(',')[0]


        #Paging
        paginator = Paginator(product_list, 8)
        page = request.GET.get('page', 1)
        try:
            orders_paged = paginator.page(page)
        except PageNotAnInteger:
            orders_paged = paginator.page(1)
        except EmptyPage:
            orders_paged = paginator.page(paginator.num_pages)

        context = {
            'product_all': orders_paged
        }
        return render(request, 'homepage/index.html', context)


class DetailView(View):
    def get(self, request, product_id):
        # Detail product
        product_detail = Product.objects.get(pk=product_id)

        hist_cmt = Feedback.objects.filter(product=product_id).order_by('-id')

        address_short = product_detail.address

        address_short = address_short.split(',')
        address_short = address_short[-2].lstrip(' ')

        # Product suggest
        product_suggest = Product.objects.filter(address__icontains=address_short).exclude(id=product_id).order_by('-id')

        for i in product_suggest:
            i.address = i.address.split(',')
            i.address[-1] = i.address[-1].lstrip(' ')
            i.address[-2] = i.address[-2].lstrip(' ')
            i.address = i.address[-2:]
            i.address = ', '.join(i.address)
            i.image = i.image.split(',')[0]

        product_detail.image = product_detail.image.split(',')

        for j in hist_cmt:
            list_y = j.time.strftime("%Y")
            list_m = j.time.strftime("%m")
            list_d = j.time.strftime("%d")
            j.time = list_d+"/"+list_m+"/"+list_y

        context = {
            'product': product_detail,
            'p_suggest': product_suggest[:4],
            'hist_cmt': hist_cmt,
            'count_cmt': Feedback.objects.filter(product=product_id).count()
        }

        return render(request, 'homepage/detail.html', context)

    def post(self, request, product_id):
        p = Product.objects.get(pk=product_id)

        customer_id = request.POST.get('customer-id')
        c_id = Customer.object.get(pk=customer_id)

        content_feedbacked = request.POST.get('comment-content')
        tel_contact = request.POST.get('comment-phone')

        feedbacked = Feedback(customer=c_id, product=p, content=content_feedbacked, tel_contact=tel_contact)

        feedbacked.save()

        return redirect('.')

def delFeedback(request):
    redirect_to = request.GET.get('next')
    cmt_id = request.GET.get('cmt-id')
    cmt_del = ''
    try:
        cmt_del = Feedback.objects.get(pk=cmt_id)
        cmt_del.delete()
        return redirect(redirect_to)
    except:
        return redirect(redirect_to)


class LoginView(View):
    def get(self, request):
        return render(request, 'homepage/login.html')


    def post(self, request):
        redirect_to = request.POST.get('next')
        user_name = request.POST['username']
        pass_word = request.POST['password']


        my_user = authenticate(request, username=user_name, password=pass_word)
        if my_user is not None and redirect_to == '':
            login(request, my_user)

            context = {'redirect_to': redirect_to}

            messages.success(request, 'login success')
            # render(request, 'homepage/login.html', context)
            return redirect('/')

        elif my_user is not None and redirect_to != '':
            login(request, my_user)

            messages.success(request, "You have successfully logged in")

            context = {'redirect_to': redirect_to}

            return redirect(redirect_to)
        elif my_user is None:
            context = {
                'message': 'Đăng nhập thất bại, vui lòng kiểm tra lại'
            }
            return render(request, 'homepage/login.html', context)



def logoutUser(request):
    redirect_to = request.GET.get('next')
    logout(request)
    return redirect(redirect_to)


class RegisterCustomer(View):
    def get(self, request):
        return render(request, 'homepage/register.html')

    def post(self, request):
        redirect_to = request.POST.get('next')
        phone_number = request.POST['phone-register']
        name = request.POST['name-register']
        pass_word = request.POST['password-register']
        birthday = request.POST['birthday-register']
        gt = request.POST['modal-radio']

        pass_word = make_password(pass_word)

        gtdb = True
        if gt == 4:
            gtdb = False

        cus_hist = Customer.object.filter(phone_number=phone_number)
        if len(phone_number) == 10:
            if cus_hist:
                context = {
                    'mess': 'Số điện thoại đã tồn tại'
                }
                return render(request, 'homepage/register.html', context)
            else:
                customer = Customer(phone_number=phone_number, name_customer=name, password=pass_word, date_of_birth=birthday, gt=gtdb)

                customer.save()

                return redirect('login')
        else:
            context = {
                'mess': 'Số điện thoại phải có 10 số'
            }
            return render(request, 'homepage/register.html', context)



class predictProduct(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, 'homepage/predict.html')

    def post(self, request):
        land_name = request.POST['name-land-predict']
        area = request.POST['area-predict']
        floors = request.POST['floors-predict']
        to_center = request.POST['tocenter-predict']
        location = request.POST['location']

        sendMail = request.POST['email-predict']
        user_predict = request.POST['predict-er']
        customer_id = request.POST['id-user']
        c_id = Customer.object.get(pk=customer_id)

        variable_list = [1, area, floors, location, to_center]

        param_list = Parameter.objects.get(parameter_using=1)
        param_list = param_list.parameter_list.split(',')
        value_predict_temp = 0.0
        if len(variable_list) == len(param_list):
            for p in range(len(variable_list)):
                value_predict_temp += float(param_list[p])*float(variable_list[p])

        value_predict = value_predict_temp

        value_predict = str(value_predict)
        value_predict = value_predict.split('.')[0]
        value_predict = value_predict + '000000'

        p_predict = Predict(customer=c_id, title=land_name, area=float(area), location_house=int(location), floors=int(floors), to_center=float(to_center), price_predict=int(value_predict), email=sendMail)
        p_predict.save()

        context = {
            'value_predict': value_predict
        }

        # Send mail
        subject = 'ĐỊNH GIÁ BẤT ĐỘNG SẢN TÊN "'+land_name+'"'
        msg = 'Xin Chào '+user_predict+'\n' \
                                       'Bạn đã sử dụng chức năng tự định giá của chúng tôi\n' \
                                       'Với các thông tin:\n' \
                                       '- Tên nhà/đất: '+land_name+'\n' \
                                                                   '- Diện tích: '+area+'\n' \
                                                                                        '- Số tầng: '+floors+'\n' \
                                                                                                             '- KC đến TT: '+to_center+'\n' \
                                                                                                                                       '- Vị trí nhà/đất: '+location+'\n' \
                                                                                                                                                                     '- Giá trị dự đoán là: '+value_predict+'\n' \
                                                                                                                                                                                                            'XIN TRÂN THÀNH CẢM ƠN'

        if value_predict:
            send_mail(subject, msg, 'dinhgianhadat.cantho@gmail.com', [sendMail], fail_silently=False)

        return render(request, 'homepage/predict.html', context)


class managePage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        view_filter = request.GET.get('view-list')
        view = ''

        if view_filter == 'product':
            view = 'pro'
            view_list = Product.objects.all().order_by('-id')
        elif view_filter == 'predict':
            view = 'pre'
            view_list = Predict.objects.all().order_by('-id')
        elif view_filter == 'customer':
            view = 'c'
            view_list = Customer.object.all()
        elif view_filter == 'feedback':
            view = 'f'
            view_list = Feedback.objects.all().order_by('-id')
        else:
            view = 'pro'
            view_list = Product.objects.all().order_by('-id')

        for j in view_list:
            list_y = j.time.strftime("%Y")
            list_m = j.time.strftime("%m")
            list_d = j.time.strftime("%d")
            j.time = list_d+"/"+list_m+"/"+list_y

        context = {
            'view_list': view_list,
            'item_count': view_list.count(),
            'view': view

        }
        return render(request, 'homepage/manage.html', context)

class createData(View):
    def get(self, request):
        return render(request, 'homepage/createdata.html')

    def post(self, request):
        next = request.GET.get('next')

        title = request.POST.get('create-title')
        price = request.POST.get('create-price')
        area = request.POST.get('create-area')
        address = request.POST.get('create-address')
        floors = request.POST.get('create-floors')
        to_center = request.POST.get('create-tocenter')
        location = request.POST.get('create-location')
        img = request.POST.get('create-img')

        variable_list = [1, area, floors, location, to_center]

        param_list = Parameter.objects.get(parameter_using=1)
        param_list = param_list.parameter_list.split(',')
        value_predict_temp = 0.0
        if len(variable_list) == len(param_list):
            for p in range(len(variable_list)):
                value_predict_temp += float(param_list[p]) * float(variable_list[p])

        value_predict = value_predict_temp

        value_predict = str(value_predict)
        value_predict = value_predict.split('.')[0]
        value_predict = value_predict + '000000'

        product_create = Product(title=title, price=int(price), area=float(area), address=address, location_house=int(location), floors=int(floors), to_center=float(to_center), image=img, price_predict=int(value_predict))

        product_create.save()

        return redirect(next)


def delProduct(request):
    redirect_to = request.GET.get('next')
    p_id = request.GET.get('product-id')
    p_del = ''
    try:
        p_del = Product.objects.get(pk=p_id)
        p_del.delete()
        return redirect(redirect_to)
    except:
        return redirect(redirect_to)


class updateData(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        context = {
            'p': product
        }
        return render(request, 'homepage/updatedata.html', context)

    def post(self, request, product_id):
        next = request.GET.get('next')

        title = request.POST.get('update-title')
        price = request.POST.get('update-price')
        area = request.POST.get('update-area')
        address = request.POST.get('update-address')
        floors = request.POST.get('update-floors')
        to_center = request.POST.get('update-tocenter')
        location = request.POST.get('update-location')
        img = request.POST.get('update-img')

        Product.objects.filter(pk=product_id).update(title=title, price=int(price), area=float(area), address=address,
                                 location_house=int(location), floors=int(floors), to_center=float(to_center),
                                 image=img)

        return redirect(next)


class adminPage(View):
    def get(self, request):
        p = Parameter.objects.all().order_by('-parameter_using')

        for i in p:
            i.parameter_list = i.parameter_list.split(',')
            list_y = i.time.strftime("%Y")
            list_m = i.time.strftime("%m")
            list_d = i.time.strftime("%d")
            i.time = list_d + "/" + list_m + "/" + list_y

        context = {
            'param': p,
            'len_p': p[0].parameter_list
        }
        return render(request, 'homepage/admin-page.html', context)

class updateParameter(View):
    def get(self, request, parameter_id):
        param = Parameter.objects.get(pk=parameter_id)

        context = {
            'param_using': param
        }
        return render(request, 'homepage/updateparameter.html', context)

    def post(self, request, parameter_id):
        next = request.GET.get('next')

        p_using = request.POST.get('update-param-using')

        Parameter.objects.filter(pk=parameter_id).update(parameter_using=int(p_using))

        return redirect(next)


class createParameter(View):
    def get(self, request):
        return render(request, 'homepage/createparameter.html')

    def post(self, request):
        next = request.GET.get('next')
        param_list = request.POST.get('create-param')
        param_desc = request.POST.get('create-desc')

        parameter = Parameter(parameter_list=param_list, parameter_descriptions=param_desc)
        parameter.save()

        return redirect(next)