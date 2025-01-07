from django.urls import path
from .views import (
    FilterView,
    homeview, 
    todayview, 
    lastweekview, 
    lastmonthview,
    incomeview,
    onlymonthview
    )

app_name = 'home'
urlpatterns = [
    path('', homeview, name='home'),
    path('last-day-monitoring/', todayview, name='today'),
    path('last-week-monitoring/', lastweekview, name='last_week'),
    path('last-month-monitoring/', lastmonthview, name='last_month'),
    path('income/<str:type>', incomeview, name='income'),
    path('filter/', FilterView.as_view(), name='filter'),
    path('only-month/', onlymonthview, name='only_month')
]