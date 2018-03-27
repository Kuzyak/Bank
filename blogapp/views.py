# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Article, Post, IcoName, BankCard, AboutUs
from .forms import PostForm, ContactForm, ContactForm_en, IcoNameForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from operator import itemgetter
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

def ico_en(request):
    ico = IcoName.objects.all()
    ico_list = list(IcoName.objects.values())
    newlist = sorted(ico_list, key=itemgetter('start_date'), reverse=True)
    dictionary = bank_info()
    if request.method == "POST":
        preset = request.POST['preset']
        if preset == "1":
            newlist = sorted(ico_list, key=itemgetter('ICO_name'))
        elif preset == "2":
            newlist = sorted(ico_list, key=itemgetter('ICO_name'), reverse=True)
        elif preset == "3":
            newlist = sorted(ico_list, key=itemgetter('start_date'))
        elif preset == "4":
            newlist = sorted(ico_list, key=itemgetter('start_date'), reverse=True)
        dictionary['ico'] = newlist
        return render(request, 'blogapp/ico_en.html', dictionary)
    else:
        dictionary['ico'] = newlist
        return render(request, 'blogapp/ico_en.html', dictionary)

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

def ico_new_en(request):
    dictionary = bank_info()
    if request.method == "POST":
        form = IcoNameForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            #post.ICO_image = form.cleaned_data['ICO_image']
            #post.ICO_name = form.cleaned_data['ICO_name']
            #post.platform = form.cleaned_data['platform']
            #post.info_block = form.cleaned_data['info_block']
            #post.link = form.cleaned_data['link']
            #post.start_date = form.cleaned_data['start_date']
            print("some_________________---")
            print(post.ICO_name)
            print("some_________________---")
            post.save()
            return redirect('ico_en')
    else:#'ICO_name', 'platform','info_block','start_date','link','ICO_image',)
        form = IcoNameForm()
        dictionary['form'] = form
    return render(request, 'blogapp/ico_new_en.html', dictionary)

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
            return redirect('post_detail_en', pk=post.pk)
    else:
        form = PostForm()
        dictionary['form'] = form
    return render(request, 'blogapp/post_new_en.html', dictionary)

def post_edit(request, pk):
    dictionary = bank_info()
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail_en', pk=post.pk)
    else:
        form = PostForm(instance=post)
        dictionary['form'] = form
    return render(request, 'blogapp/post_new_en.html', dictionary)

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
            www.coinblooming.com 
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
    #BINANCE
    BINANCE = Article.objects.filter(title="binance")
    num1 = len(BINANCE)-1
    BINANCE = BINANCE[num1]
    BINANCE.USD1 = BINANCE.USD.split("/")[0]
    BINANCE.USD2 = BINANCE.USD.split("/")[1]
    BINANCE.ETH1 = BINANCE.CNY.split("/")[0]
    BINANCE.ETH2 = BINANCE.CNY.split("/")[1]
    BINANCE.XRP1 = BINANCE.RUB.split("/")[0]
    BINANCE.XRP2 = BINANCE.RUB.split("/")[1]
    BINANCE.BCH1 = BINANCE.RON.split("/")[0]
    BINANCE.BCH2 = BINANCE.RON.split("/")[1]
    BINANCE.XLM1 = BINANCE.GBP.split("/")[0]
    BINANCE.XLM2 = BINANCE.GBP.split("/")[1]
    BINANCE.LTC1 = BINANCE.CHF.split("/")[0]
    BINANCE.LTC2 = BINANCE.CHF.split("/")[1]
    #KRAKEN
    KRAKEN = Article.objects.filter(title="kraken")
    num1 = len(KRAKEN)-1
    KRAKEN = KRAKEN[num1]
    KRAKEN.USD1 = KRAKEN.USD.split("/")[0]
    KRAKEN.USD2 = KRAKEN.USD.split("/")[1]
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
    #BITTREX
    BITTREX = Article.objects.filter(title="bittrex")
    num1 = len(BITTREX)-1
    BITTREX = BITTREX[num1]
    BITTREX.USD1 = BITTREX.USD.split("/")[0]
    BITTREX.USD2 = BITTREX.USD.split("/")[1]
    BITTREX.ETH1 = BITTREX.CNY.split("/")[0]
    BITTREX.ETH2 = BITTREX.CNY.split("/")[1]
    BITTREX.XRP1 = BITTREX.RUB.split("/")[0]
    BITTREX.XRP2 = BITTREX.RUB.split("/")[1]
    BITTREX.BCH1 = BITTREX.RON.split("/")[0]
    BITTREX.BCH2 = BITTREX.RON.split("/")[1]
    BITTREX.XLM1 = BITTREX.GBP.split("/")[0]
    BITTREX.XLM2 = BITTREX.GBP.split("/")[1]
    BITTREX.LTC1 = BITTREX.CHF.split("/")[0]
    BITTREX.LTC2 = BITTREX.CHF.split("/")[1]
    time = timezone.now().date()
    dictionary = {  'BITFINEX':BITFINEX,
                    'KRAKEN':KRAKEN,
                    'BINANCE':BINANCE,
                    'BITTREX':BITTREX,
                    'time_date':time}
    return dictionary
