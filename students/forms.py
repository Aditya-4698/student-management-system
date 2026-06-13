from django import forms
from .models import Book

class BookForm(forms.ModelForm):

    class Meta:

        model = Book

        fields = "__all__"

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'author': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'isbn': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'publisher': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'available_quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'shelf_no': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'book_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

        }