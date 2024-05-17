from django import forms
from datetime import date


class PaySystemForm(forms.Form):
  cart_number = forms.IntegerField(label='Номер карты', widget=forms.TextInput(attrs={'class': 'form-input', 'maxlength': '16'}))
  day = forms.DateTimeField(label='День', widget=forms.TextInput(attrs={'class': 'form-input', 'maxlength': '2'}))
  month = forms.DateTimeField(label='Месяц', widget=forms.TextInput(attrs={'class': 'form-input', 'maxlength': '2'}))
  year = forms.DateTimeField(label='Год', widget=forms.TextInput(attrs={'class': 'form-input', 'maxlength': '2'}))
  cvv_number = forms.IntegerField(label='CVV', widget=forms.TextInput(attrs={'class': 'form-input', 'maxlength': '3'}))
  amount = forms.DecimalField(label='Сумма', widget=forms.NumberInput(attrs={'class': 'form-input', 'maxlength': '300'}))
  description = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'form-input'}))
  token = forms.CharField(widget=forms.HiddenInput())

  def clean_cart_number(self):
    cart_number = self.cleaned_data.get('cart_number')
    if cart_number and len(str(cart_number)) != 16:
        raise forms.ValidationError('Неверный номер карты')
    return cart_number

  def clean_data_number(self):
    cleaned_data = super().clean()
    day = cleaned_data.get('day')
    month = cleaned_data.get('moth')
    year = cleaned_data.get('year')

        # Проверка корректности даты
    try:
      date(year, month, day)
    except ValueError:
      raise forms.ValidationError('Некорректная дата')
    if not len(day) == 2 or len(month) == 2 or len(year) == 2:
        raise forms.ValidationError('Некорректная дата')

    return cleaned_data

  def clean_cvv_number(self):
    cvv_number = self.cleaned_data.get('cvv_number')
    if cvv_number and len(str(cvv_number)) != 3:
      raise forms.ValidationError('Неверное количество символов в CVV')
    return cvv_number

  def clean_amount(self):
    amount = self.cleaned_data.get('amount')
    if amount and amount <= 0:
      raise forms.ValidationError('Сумма должна быть положительной')
    return amount
  

class ColorFilterForm(forms.Form):
    color = forms.CharField(required=False)