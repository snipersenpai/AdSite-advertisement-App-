from django import forms

class CartAddAdForm(forms.Form):
    quantity = forms.IntegerField(required=False,initial=1,widget=forms.HiddenInput)
