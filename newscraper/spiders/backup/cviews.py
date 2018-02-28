from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Article, Post, BankCard, AboutUs
from .forms import PostForm, ContactForm, ContactForm_en

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
User = get_user_model()



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    n = len(posts)
    for i in range(n):
        len_text = len(posts[i].text)
        x = posts[i].text.find('\n')
        if len_text > 85 and x > 85:
            posts[i].title_text = posts[i].text[:85]
        elif len_text > 85:
            posts[i].title_text = posts[i].text[:x-1]
        else:
            posts[i].title_text = posts[i].text
    dictionary = bank_info()
    dictionary['posts'] = posts
    about = AboutUs.objects.all()
    num1 = len(about)-1
    about_n = about[num1]
    dictionary['about'] = about_n
    return render(request, 'blogapp/post_list.html', dictionary)

def post_list_en(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    n = len(posts)
    for i in range(n):
        len_text = len(posts[i].text)
        x = posts[i].text.find('\n')
        if len_text > 85 and x > 85:
            posts[i].title_text = posts[i].text[:85]
        elif len_text > 85:
            posts[i].title_text = posts[i].text[:x-1]
        else:
            posts[i].title_text = posts[i].text
    dictionary = bank_info()
    dictionary['posts'] = posts
    about = AboutUs.objects.all()
    num1 = len(about)-1
    about_n = about[num1]
    dictionary['about'] = about_n
    return render(request, 'blogapp/post_list_en.html', dictionary)

def post_list_all(request):
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post = paginator.page(paginator.num_pages)
    dictionary = bank_info()
    dictionary['postst'] = post
    return render(request, 'blogapp/post_list_all.html', dictionary)

def post_list_all_en(request):
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post = paginator.page(paginator.num_pages)
    dictionary = bank_info()
    dictionary['postst'] = post
    return render(request, 'blogapp/post_list_all_en.html', dictionary)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    dictionary = bank_info()
    dictionary['post'] = post
    return render(request, 'blogapp/post_detail.html', dictionary)

def post_detail_en(request, pk):
    post = get_object_or_404(Post, pk=pk)
    dictionary = bank_info()
    dictionary['post'] = post
    return render(request, 'blogapp/post_detail_en.html', dictionary)

def rate_ex_bank(request):
    dictionary = bank_info()
    return render(request, 'blogapp/rate_ex_bank.html', dictionary)

def rate_ex_bank_en(request):
    dictionary = bank_info()
    return render(request, 'blogapp/rate_ex_bank_en.html', dictionary)

def post_new(request):
    dictionary = bank_info()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.images = form.cleaned_data['images']
            post.text = form.cleaned_data['text']
            #post.published_date = timezone.now()
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        dictionary['form'] = form
    return render(request, 'blogapp/post_new.html', dictionary)

def post_edit(request, pk):
    dictionary = bank_info()
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        dictionary['form'] = form
    return render(request, 'blogapp/post_new.html', dictionary)

def bank_cards(request):
    cards = BankCard.objects.all()
    dictionary = bank_info()
    n = len(cards)
    for i in range(n):
        some = cards[i].info_block
        cards[i].info_block = some.split("/*/")
    dictionary['cards'] = cards
    return render(request, 'blogapp/bank_cards.html', dictionary)

def bank_cards_en(request):
    cards = BankCard.objects.all()
    dictionary = bank_info()
    n = len(cards)
    for i in range(n):
        some = cards[i].info_block
        cards[i].info_block = some.split("/*/")
    dictionary['cards'] = cards
    return render(request, 'blogapp/bank_cards_en.html', dictionary)

def contact_us(request):
    dictionary = bank_info()
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            to_email = settings.EMAIL_HOST_USER
            contact_message = """
            %s: %s From: %s
            """%(full_name, message, from_email)
            try:
                send_mail(subject,
                          contact_message,
                          from_email,
                          [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return redirect('success')
            dictionary['email'] = {'send':'Siker! Köszönöm az üzenetet.'}
    dictionary['form'] = form
    #return render(request, 'blogapp/contact_us.html', dictionary)
    return render(request, "blogapp/contact_us.html", dictionary)

def contact_us_en(request):
    dictionary = bank_info()
    if request.method == 'GET':
        form = ContactForm_en()
    else:
        form = ContactForm_en(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            to_email = settings.EMAIL_HOST_USER
            contact_message = """
            %s: %s From: %s
            """%(full_name, message, from_email)
            try:
                send_mail(subject,
                          contact_message,
                          from_email,
                          [to_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            #return redirect('success')
            dictionary['email'] = {'send':'Success! Thank you for your message.'}
    dictionary['form'] = form
    #return render(request, 'blogapp/contact_us.html', dictionary)
    return render(request, "blogapp/contact_us_en.html", dictionary)

def map(request):
    dictionary = bank_info()
    return render(request, 'blogapp/map.html', dictionary)

def map_en(request):
    dictionary = bank_info()
    return render(request, 'blogapp/map_en.html', dictionary)

def loan(request):
    kredit = Article.objects.filter(title="KREDIT")
    num = len(kredit)-1
    KREDIT_N = kredit[num]
    name0 = KREDIT_N.EUR.split("/")
    thm0 = KREDIT_N.USD.split("/")
    year0 = KREDIT_N.CNY.split("/")
    period0 = KREDIT_N.RUB.split("/")
    zatrat0 = KREDIT_N.RON.split("/")
    limit0 = KREDIT_N.CHF.split("/")
    name = []
    thm = []
    year = []
    period = []
    zatrat = []
    limit = []
    for i in range(len(KREDIT_N.EUR.split("/"))):
        name.append(name0[i])
        thm.append(float(thm0[i].replace(",",".")))
        year.append(float(year0[i].replace(",",".")))
        period.append(period0[i])
        zatrat.append(zatrat0[i])
        limit.append(limit0[i])

    data = {
        "name":name,
        "thm":thm,
        "year":year,
        "per":period,
        "zat":zatrat,
        "lim":limit
    }
    dictionary = bank_info()
    dictionary['data'] = data
    return render(request, 'blogapp/loan.html', dictionary)

def loan_en(request):
    kredit = Article.objects.filter(title="KREDIT")
    num = len(kredit)-1
    KREDIT_N = kredit[num]
    name0 = KREDIT_N.EUR.split("/")
    thm0 = KREDIT_N.USD.split("/")
    year0 = KREDIT_N.CNY.split("/")
    period0 = KREDIT_N.RUB.split("/")
    zatrat0 = KREDIT_N.RON.split("/")
    limit0 = KREDIT_N.CHF.split("/")
    name = []
    thm = []
    year = []
    period = []
    zatrat = []
    limit = []
    for i in range(len(KREDIT_N.EUR.split("/"))):
        name.append(name0[i])
        thm.append(float(thm0[i].replace(",",".")))
        year.append(float(year0[i].replace(",",".")))
        period.append(period0[i])
        zatrat.append(zatrat0[i])
        limit.append(limit0[i])

    data = {
        "name":name,
        "thm":thm,
        "year":year,
        "per":period,
        "zat":zatrat,
        "lim":limit
    }
    dictionary = bank_info()
    dictionary['data'] = data
    return render(request, 'blogapp/loan_en.html', dictionary)

class rate_ex_history(View):
    def get(self, request, *args, **kwargs):
        dictionary = bank_info()
        return render(request, 'blogapp/rate_ex_history.html', dictionary)

class rate_ex_history_en(View):
    def get(self, request, *args, **kwargs):
        dictionary = bank_info()
        return render(request, 'blogapp/rate_ex_history_en.html', dictionary)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        HISTOR = Article.objects.filter(title="NachHistory")
        num = len(HISTOR)-1
        HISTOR_N = HISTOR[num]
        day = HISTOR_N.description.split("/")
        lab = day[0] + " – " + day[-1]
        EUR = []
        for some in HISTOR_N.EUR.split("/"):
            EUR.append(float(some))
        USD = []
        for some in HISTOR_N.USD.split("/"):
            USD.append(float(some))
        RON = []
        for some in HISTOR_N.RON.split("/"):
            RON.append(float(some))
        RUB = []
        for some in HISTOR_N.RUB.split("/"):
            RUB.append(float(some))
        CNY = []
        for some in HISTOR_N.CNY.split("/"):
            CNY.append(float(some))
        GBP = []
        for some in HISTOR_N.GBP.split("/"):
            GBP.append(float(some))
        CHF = []
        for some in HISTOR_N.CHF.split("/"):
            CHF.append(float(some))
        data = {
            "EUR":EUR,
            "USD":USD,
            "RON":RON,
            "RUB":RUB,
            "CNY":CNY,
            "GBP":GBP,
            "CHF":CHF,
            "DAY":day,
            "LAB":lab,
        }
        return Response(data)



def bank_info():
    '''for x in range(1000):
        bitfinex = Article.objects.filter(title="SBERBANK")
        if len(bitfinex) > 50:
            bitfinex.first().delete()
        else:
            break'''
    firstbank = Article.objects.filter(title="NachBank")
    num0 = len(firstbank)-1
    #BITFINEX
    BITFINEX = Article.objects.filter(title="bitfinex")
    num1 = len(BITFINEX)-1
    BITFINEX = BITFINEX[num1]
    BITFINEX.USD1 = BITFINEX.USD.split("/")[0]
    BITFINEX.USD2 = BITFINEX.USD.split("/")[1]
    BITFINEX.EUR1 = BITFINEX.EUR.split("/")[0]
    BITFINEX.EUR2 = BITFINEX.EUR.split("/")[1]
    BITFINEX.ETH1 = BITFINEX.CNY.split("/")[0]
    BITFINEX.ETH2 = BITFINEX.CNY.split("/")[1]
    BITFINEX.ETH3 = BITFINEX.CNY.split("/")[2]#
    BITFINEX.XRP1 = BITFINEX.RUB.split("/")[0]
    BITFINEX.XRP2 = BITFINEX.RUB.split("/")[1]
    BITFINEX.XRP3 = BITFINEX.RUB.split("/")[2]#
    BITFINEX.BCH1 = BITFINEX.RON.split("/")[0]
    BITFINEX.BCH2 = BITFINEX.RON.split("/")[1]
    BITFINEX.BCH3 = BITFINEX.RON.split("/")[2]#
    BITFINEX.XLM1 = BITFINEX.GBP.split("/")[0]
    BITFINEX.XLM2 = BITFINEX.GBP.split("/")[1]
    BITFINEX.XLM3 = BITFINEX.GBP.split("/")[2]#
    BITFINEX.LTC1 = BITFINEX.CHF.split("/")[0]
    BITFINEX.LTC2 = BITFINEX.CHF.split("/")[1]
    BITFINEX.LTC3 = BITFINEX.CHF.split("/")[2]#
    #BITFINEX
    KRAKEN = Article.objects.filter(title="kraken")
    num1 = len(KRAKEN)-1
    KRAKEN = KRAKEN[num1]
    KRAKEN.USD1 = KRAKEN.USD.split("/")[0]
    KRAKEN.USD2 = KRAKEN.USD.split("/")[1]
    KRAKEN.EUR1 = KRAKEN.EUR.split("/")[0]
    KRAKEN.EUR2 = KRAKEN.EUR.split("/")[1]
    KRAKEN.ETH1 = KRAKEN.CNY.split("/")[0]
    KRAKEN.ETH2 = KRAKEN.CNY.split("/")[1]
    KRAKEN.XRP1 = KRAKEN.RUB.split("/")[0]
    KRAKEN.XRP2 = KRAKEN.RUB.split("/")[1]
    KRAKEN.BCH1 = KRAKEN.RON.split("/")[0]
    KRAKEN.BCH2 = KRAKEN.RON.split("/")[1]
    KRAKEN.XLM1 = KRAKEN.GBP.split("/")[0]
    KRAKEN.XLM2 = KRAKEN.GBP.split("/")[1]
    KRAKEN.LTC1 = KRAKEN.CHF.split("/")[0]
    KRAKEN.LTC2 = KRAKEN.CHF.split("/")[1]
    #BUDAEST
    BUDAPEST = Article.objects.filter(title="BUDAPEST")
    num1 = len(BUDAPEST)-1
    BUDAPEST_N = BUDAPEST[num1]
    BUDAPEST_N.USD1 = BUDAPEST_N.USD.split("/")[0]
    BUDAPEST_N.USD2 = BUDAPEST_N.USD.split("/")[1]
    BUDAPEST_N.EUR1 = BUDAPEST_N.EUR.split("/")[0]
    BUDAPEST_N.EUR2 = BUDAPEST_N.EUR.split("/")[1]
    BUDAPEST_N.CHF1 = BUDAPEST_N.CHF.split("/")[0]
    BUDAPEST_N.CHF2 = BUDAPEST_N.CHF.split("/")[1]
    BUDAPEST_N.GBP1 = BUDAPEST_N.GBP.split("/")[0]
    BUDAPEST_N.GBP2 = BUDAPEST_N.GBP.split("/")[1]
    #CIB
    CIB = Article.objects.filter(title="CIB")
    num1 = len(CIB)-1
    CIB_N = CIB[num1]
    CIB_N.USD1 = CIB_N.USD.split("/")[0].replace(".",",")
    CIB_N.USD2 = CIB_N.USD.split("/")[1].replace(".",",")
    CIB_N.EUR1 = CIB_N.EUR.split("/")[0].replace(".",",")
    CIB_N.EUR2 = CIB_N.EUR.split("/")[1].replace(".",",")
    CIB_N.CHF1 = CIB_N.CHF.split("/")[0].replace(".",",")
    CIB_N.CHF2 = CIB_N.CHF.split("/")[1].replace(".",",")
    CIB_N.GBP1 = CIB_N.GBP.split("/")[0].replace(".",",")
    CIB_N.GBP2 = CIB_N.GBP.split("/")[1].replace(".",",")
    #ERSTE
    ERSTE = Article.objects.filter(title="ERSTE")
    num1 = len(ERSTE)-1
    ERSTE_N = ERSTE[num1]
    ERSTE_N.USD1 = ERSTE_N.USD.split("/")[0].replace(".",",")
    ERSTE_N.USD2 = ERSTE_N.USD.split("/")[1].replace(".",",")
    ERSTE_N.EUR1 = ERSTE_N.EUR.split("/")[0].replace(".",",")
    ERSTE_N.EUR2 = ERSTE_N.EUR.split("/")[1].replace(".",",")
    ERSTE_N.RON1 = ERSTE_N.RON.split("/")[0].replace(".",",")
    ERSTE_N.RON2 = ERSTE_N.RON.split("/")[1].replace(".",",")
    ERSTE_N.CHF1 = ERSTE_N.CHF.split("/")[0].replace(".",",")
    ERSTE_N.CHF2 = ERSTE_N.CHF.split("/")[1].replace(".",",")
    ERSTE_N.GBP1 = ERSTE_N.GBP.split("/")[0].replace(".",",")
    ERSTE_N.GBP2 = ERSTE_N.GBP.split("/")[1].replace(".",",")
    #GRANIT
    GRANIT = Article.objects.filter(title="GRANIT")
    num1 = len(GRANIT)-1
    GRANIT_N = GRANIT[num1]
    GRANIT_N.USD1 = GRANIT_N.USD.split("/")[0].replace(".",",")
    GRANIT_N.USD2 = GRANIT_N.USD    .split("/")[1].replace(".",",")
    GRANIT_N.EUR1 = GRANIT_N.EUR.split("/")[0].replace(".",",")
    GRANIT_N.EUR2 = GRANIT_N.EUR.split("/")[1].replace(".",",")
    GRANIT_N.CHF1 = GRANIT_N.CHF.split("/")[0].replace(".",",")
    GRANIT_N.CHF2 = GRANIT_N.CHF.split("/")[1].replace(".",",")
    GRANIT_N.GBP1 = GRANIT_N.GBP.split("/")[0].replace(".",",")
    GRANIT_N.GBP2 = GRANIT_N.GBP.split("/")[1].replace(".",",")
    #OTP
    OTP = Article.objects.filter(title="OTP")
    num1 = len(OTP)-1
    OTP_N = OTP[num1]
    OTP_N.USD1 = OTP_N.USD.split("/")[0].replace(".",",")
    OTP_N.USD2 = OTP_N.USD.split("/")[1].replace(".",",")
    OTP_N.EUR1 = OTP_N.EUR.split("/")[0].replace(".",",")
    OTP_N.EUR2 = OTP_N.EUR.split("/")[1].replace(".",",")
    OTP_N.CNY1 = OTP_N.CNY.split("/")[0].replace(".",",")
    OTP_N.CNY2 = OTP_N.CNY.split("/")[1].replace(".",",")
    OTP_N.RON1 = OTP_N.RON.split("/")[0].replace(".",",")
    OTP_N.RON2 = OTP_N.RON.split("/")[1].replace(".",",")
    OTP_N.RUB1 = OTP_N.RUB.split("/")[0].replace(".",",")
    OTP_N.RUB2 = OTP_N.RUB.split("/")[1].replace(".",",")
    OTP_N.CHF1 = OTP_N.CHF.split("/")[0].replace(".",",")
    OTP_N.CHF2 = OTP_N.CHF.split("/")[1].replace(".",",")
    OTP_N.GBP1 = OTP_N.GBP.split("/")[0].replace(".",",")
    OTP_N.GBP2 = OTP_N.GBP.split("/")[1].replace(".",",")
    #RAIFFEISEN
    RAIFFEISEN = Article.objects.filter(title="RAIFFEISEN")
    num1 = len(RAIFFEISEN)-1
    RAIFFEISEN_N = RAIFFEISEN[num1]
    RAIFFEISEN_N.USD1 = RAIFFEISEN_N.USD.split("/")[0].replace(".",",")
    RAIFFEISEN_N.USD2 = RAIFFEISEN_N.USD.split("/")[1].replace(".",",")
    RAIFFEISEN_N.EUR1 = RAIFFEISEN_N.EUR.split("/")[0].replace(".",",")
    RAIFFEISEN_N.EUR2 = RAIFFEISEN_N.EUR.split("/")[1].replace(".",",")
    RAIFFEISEN_N.RON1 = RAIFFEISEN_N.RON.split("/")[0].replace(".",",")
    RAIFFEISEN_N.RON2 = RAIFFEISEN_N.RON.split("/")[1].replace(".",",")
    RAIFFEISEN_N.RUB1 = RAIFFEISEN_N.RUB.split("/")[0].replace(".",",")
    RAIFFEISEN_N.RUB2 = RAIFFEISEN_N.RUB.split("/")[1].replace(".",",")
    RAIFFEISEN_N.CHF1 = RAIFFEISEN_N.CHF.split("/")[0].replace(".",",")
    RAIFFEISEN_N.CHF2 = RAIFFEISEN_N.CHF.split("/")[1].replace(".",",")
    RAIFFEISEN_N.GBP1 = RAIFFEISEN_N.GBP.split("/")[0].replace(".",",")
    RAIFFEISEN_N.GBP2 = RAIFFEISEN_N.GBP.split("/")[1].replace(".",",")
    #MKB
    MKB = Article.objects.filter(title="MKB")
    num1 = len(MKB)-1
    MKB_N = MKB[num1]
    MKB_N.USD1 = MKB_N.USD.split("/")[0].replace(".",",")
    MKB_N.USD2 = MKB_N.USD.split("/")[1].replace(".",",")
    MKB_N.EUR1 = MKB_N.EUR.split("/")[0].replace(".",",")
    MKB_N.EUR2 = MKB_N.EUR.split("/")[1].replace(".",",")
    MKB_N.RON1 = MKB_N.RON.split("/")[0].replace(".",",")
    MKB_N.RON2 = MKB_N.RON.split("/")[1].replace(".",",")
    MKB_N.RUB1 = MKB_N.RUB.split("/")[0].replace(".",",")
    MKB_N.RUB2 = MKB_N.RUB.split("/")[1].replace(".",",")
    MKB_N.CNY1 = MKB_N.CNY.split("/")[0].replace(".",",")
    MKB_N.CNY2 = MKB_N.CNY.split("/")[1].replace(".",",")
    MKB_N.CHF1 = MKB_N.CHF.split("/")[0].replace(".",",")
    MKB_N.CHF2 = MKB_N.CHF.split("/")[1].replace(".",",")
    MKB_N.GBP1 = MKB_N.GBP.split("/")[0].replace(".",",")
    MKB_N.GBP2 = MKB_N.GBP.split("/")[1].replace(".",",")
    #K&H
    KANDH = Article.objects.filter(title="K&H")
    num1 = len(KANDH)-1
    KANDH_N = KANDH[num1]
    KANDH_N.USD1 = KANDH_N.USD.split("/")[0].replace(".",",")
    KANDH_N.USD2 = KANDH_N.USD.split("/")[1].replace(".",",")
    KANDH_N.EUR1 = KANDH_N.EUR.split("/")[0].replace(".",",")
    KANDH_N.EUR2 = KANDH_N.EUR.split("/")[1].replace(".",",")
    KANDH_N.RON1 = KANDH_N.RON.split("/")[0].replace(".",",")
    KANDH_N.RON2 = KANDH_N.RON.split("/")[1].replace(".",",")
    KANDH_N.RUB1 = KANDH_N.RUB.split("/")[0].replace(".",",")
    KANDH_N.RUB2 = KANDH_N.RUB.split("/")[1].replace(".",",")
    KANDH_N.CNY1 = KANDH_N.CNY.split("/")[0].replace(".",",")
    KANDH_N.CNY2 = KANDH_N.CNY.split("/")[1].replace(".",",")
    KANDH_N.CHF1 = KANDH_N.CHF.split("/")[0].replace(".",",")
    KANDH_N.CHF2 = KANDH_N.CHF.split("/")[1].replace(".",",")
    KANDH_N.GBP1 = KANDH_N.GBP.split("/")[0].replace(".",",")
    KANDH_N.GBP2 = KANDH_N.GBP.split("/")[1].replace(".",",")
    #UNICREDIT
    UNICREDIT = Article.objects.filter(title="UNICREDIT")
    num1 = len(UNICREDIT)-1
    UNICREDIT_N = UNICREDIT[num1]
    UNICREDIT_N.USD1 = UNICREDIT_N.USD.split("/")[0].replace(".",",")
    UNICREDIT_N.USD2 = UNICREDIT_N.USD.split("/")[1].replace(".",",")
    UNICREDIT_N.EUR1 = UNICREDIT_N.EUR.split("/")[0].replace(".",",")
    UNICREDIT_N.EUR2 = UNICREDIT_N.EUR.split("/")[1].replace(".",",")
    UNICREDIT_N.RON1 = UNICREDIT_N.RON.split("/")[0].replace(".",",")
    UNICREDIT_N.RON2 = UNICREDIT_N.RON.split("/")[1].replace(".",",")
    UNICREDIT_N.RUB1 = UNICREDIT_N.RUB.split("/")[0].replace(".",",")
    UNICREDIT_N.RUB2 = UNICREDIT_N.RUB.split("/")[1].replace(".",",")
    UNICREDIT_N.CNY1 = UNICREDIT_N.CNY.split("/")[0].replace(".",",")
    UNICREDIT_N.CNY2 = UNICREDIT_N.CNY.split("/")[1].replace(".",",")
    UNICREDIT_N.CHF1 = UNICREDIT_N.CHF.split("/")[0].replace(".",",")
    UNICREDIT_N.CHF2 = UNICREDIT_N.CHF.split("/")[1].replace(".",",")
    UNICREDIT_N.GBP1 = UNICREDIT_N.GBP.split("/")[0].replace(".",",")
    UNICREDIT_N.GBP2 = UNICREDIT_N.GBP.split("/")[1].replace(".",",")
    #SBERBANK
    SBERBANK = Article.objects.filter(title="SBERBANK")
    num1 = len(SBERBANK)-1
    SBERBANK_N = SBERBANK[num1]
    SBERBANK_N.USD1 = SBERBANK_N.USD.split("/")[0].replace(".",",")
    SBERBANK_N.USD2 = SBERBANK_N.USD.split("/")[1].replace(".",",")
    SBERBANK_N.EUR1 = SBERBANK_N.EUR.split("/")[0].replace(".",",")
    SBERBANK_N.EUR2 = SBERBANK_N.EUR.split("/")[1].replace(".",",")
    SBERBANK_N.RUB1 = SBERBANK_N.RUB.split("/")[0].replace(".",",")
    SBERBANK_N.RUB2 = SBERBANK_N.RUB.split("/")[1].replace(".",",")
    SBERBANK_N.CHF1 = SBERBANK_N.CHF.split("/")[0].replace(".",",")
    SBERBANK_N.CHF2 = SBERBANK_N.CHF.split("/")[1].replace(".",",")
    SBERBANK_N.GBP1 = SBERBANK_N.GBP.split("/")[0].replace(".",",")
    SBERBANK_N.GBP2 = SBERBANK_N.GBP.split("/")[1].replace(".",",")
    time = timezone.now().date()
    dictionary = {  'firstbank':firstbank[num0],
                    'BITFINEX':BITFINEX,
                    'BUDAPEST':BUDAPEST_N,
                    'CIB':CIB_N,
                    'ERSTE':ERSTE_N,
                    'GRANIT':GRANIT_N,
                    'OTP':OTP_N,
                    'RAIFFEISEN':RAIFFEISEN_N,
                    'MKB':MKB_N,
                    'KANDH':KANDH_N,
                    'UNICREDIT':UNICREDIT_N,
                    'SBERBANK':SBERBANK_N,
                    'time_date':time}
    return dictionary
