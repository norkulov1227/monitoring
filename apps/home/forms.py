from django import forms
from .models import Monitoring

class MonitoringForm(forms.ModelForm):
    TYPE_CHOICES = (
        ("card", "Karta"),
        ("cash", "Naqt")
    )
    STATUS_CHOICES = (
        ("income", "Kirim"),
        ("expense", "Chiqim")
    )

    payment_type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(
            attrs={'class' : "form-control"}
        ),
        label="Karta yoki Naqt tanlang:"
    )

    price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={'class' : "form-control", 'placeholder' : "Summani kiriting:"}
        )
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={'class' : "form-control", 'rows' : "5", 'placeholder' : "Izoh yozing:"}
        )
    )


    class Meta:
        model = Monitoring
        fields = ('payment_type', 'price', 'comment')