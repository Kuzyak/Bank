from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Article
from .models import Post

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
    return render(request, 'blogapp/post_list.html', dictionary)

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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    dictionary = bank_info()
    dictionary['post'] = post
    return render(request, 'blogapp/post_detail.html', dictionary)

def rate_ex_bank(request):
    dictionary = bank_info()
    return render(request, 'blogapp/rate_ex_bank.html', dictionary)

class rate_ex_history(View):
    def get(self, request, *args, **kwargs):
        dictionary = bank_info()
        return render(request, 'blogapp/rate_ex_history.html', dictionary)

'''
def get_data(request, *args, **kwargs):
    data = {
        "car":10,
        "moto":3,
        "jeep":2,
    }
    return JsonResponse(data)
'''

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

#def rate_ex_history(request):
    #dictionary = bank_info()
    #return render(request, 'blogapp/rate_ex_history.html', dictionary)


def bank_info():
    firstbank = Article.objects.filter(title="NachBank")
    num0 = len(firstbank)-1
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
