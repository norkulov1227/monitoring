from django.shortcuts import render, redirect
from django.views import View
from .models import Monitoring
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate
from .forms import MonitoringForm
from django.contrib import messages
from django.contrib.auth.models import User

class FilterView(View):

    def get(self, request, *args, **kwargs):
        today = timezone.now()
        month_ago = today - timedelta(days=30)

        context = {
            'today': today.strftime('%Y-%m-%d'),  
            'month_ago': month_ago.strftime('%Y-%m-%d'),  
        }
        return render(request, 'filter.html', context)

    def post(self, request, *args, **kwargs):
        
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

        aware_start_datetime = timezone.make_aware(start_datetime)
        aware_end_datetime = timezone.make_aware(end_datetime)

        monitors = Monitoring.objects.filter(created_at__gte=aware_start_datetime, created_at__lte=aware_end_datetime)
        monitors = monitors.filter(user=request.user)

        total_income = monitors.filter(status='income').aggregate(Sum('price'))['price__sum'] or 0
        total_expence = monitors.filter(status='expense').aggregate(Sum('price'))['price__sum'] or 0
        
        grouped_data = (
        monitors.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(
            total_income=Sum('price', filter=Q(status='income')),
            total_expense=Sum('price', filter=Q(status='expense'))
        )
        .order_by('-day')
    )

        
        context = {
            "monitoring": monitors,
            "grouped_data" : grouped_data,
            "total" : total_income,
            "expence" : total_expence
        }
        return render(request, 'monitoring.html', context)
    

def homeview(request):
    user = request.user
    
    if user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'login.html')

def todayview(request):
    user = request.user
    data = Monitoring.objects.filter(user=user).all()
    today = timezone.localdate()
    today_monitoring = data.filter( created_at__date = today).order_by("-created_at")
    total_income = today_monitoring.filter(status='income').aggregate(Sum('price'))['price__sum'] or 0
    total_expence = today_monitoring.filter(status='expense').aggregate(Sum('price'))['price__sum'] or 0

    grouped_data = (
        today_monitoring.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(
            total_income=Sum('price', filter=Q(status='income')),
            total_expense=Sum('price', filter=Q(status='expense'))
        )
        .order_by('-day')
    )
    context = {
        "grouped_data": grouped_data,
        "monitoring" : today_monitoring,  
        "total" : total_income,
        "expence" : total_expence
    }
    return render(request, 'monitoring.html', context)



def lastweekview(request):
    user = request.user
    data = Monitoring.objects.filter(user=user).all()
    today = timezone.localdate()
    week_ago = today - timedelta(days=7)
    last_week = data.filter(
    created_at__date__range=[week_ago, today]
    ).order_by("-created_at")
    
    total_income = last_week.filter(status='income').aggregate(Sum('price'))['price__sum'] or 0
    total_expence = last_week.filter(status='expense').aggregate(Sum('price'))['price__sum'] or 0
    grouped_data = (
        last_week.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(
            total_income=Sum('price', filter=Q(status='income')),
            total_expense=Sum('price', filter=Q(status='expense'))
        )
        .order_by('-day')
    )
    context = {
        "grouped_data": grouped_data,
        "monitoring" : last_week,
        "total" : total_income,
        "expence" : total_expence
    }

    return render(request, 'monitoring.html', context)



def lastmonthview(request):
    user = request.user
    data = Monitoring.objects.filter(user=user).all()
    today = timezone.now()
    month_ago = today - timedelta(days=30)
    last_month = data.filter(
    created_at__date__range=[month_ago, today]
).order_by("-created_at")

    total_income = last_month.filter(status='income').aggregate(Sum('price'))['price__sum'] or 0
    total_expence = last_month.filter(status='expense').aggregate(Sum('price'))['price__sum'] or 0
    grouped_data = (
        last_month.annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(
            total_income=Sum('price', filter=Q(status='income')),
            total_expense=Sum('price', filter=Q(status='expense'))
        )
        .order_by('-day')
    )

    context = {
        "grouped_data": grouped_data,
        "monitoring" : last_month,
        "total" : total_income,
        "expence" : total_expence
    }

    return render(request, 'monitoring.html', context)


def incomeview(request, type):

    form = MonitoringForm(request.POST or None)
    user = request.user
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        if type == 'kirim':
            instance.status = "income"
            instance.save()
            messages.success(request, "Successfuly")
            return redirect("home:home") 
        else:
            instance.status = "expense" 
            instance.save()
            messages.success(request, "Successfuly")
            return redirect("home:home")     
    type = type.capitalize()
    return render(request, 'income.html', {'form' : form, "type":type})


def onlymonthview(request):
    user = request.user
    data = Monitoring.objects.filter(user=user).all()
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        month_year = data.filter(created_at__year = int(selected_year), created_at__month = int(selected_month)).order_by("-created_at")
        
        total_income = month_year.filter(status='income').aggregate(Sum('price'))['price__sum'] or 0
        total_expence = month_year.filter(status='expense').aggregate(Sum('price'))['price__sum'] or 0
        grouped_data = (
            month_year.annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(
                total_income=Sum('price', filter=Q(status='income')),
                total_expense=Sum('price', filter=Q(status='expense'))
            )
            .order_by('-day')
        )

        context = {
            "grouped_data": grouped_data,
            "monitoring" : month_year,
            "total" : total_income,
            "expence" : total_expence
        }

        return render(request, 'monitoring.html', context)

    else:
        selected_month = None
        selected_year = None
        messages.error(request, "Iltmos! Kerakli oy va yilni tanlang!")
        return redirect("home:filter")

    return render(request, 'monitoring.html', {
        'selected_month': selected_month,
        'selected_year': selected_year,
    })