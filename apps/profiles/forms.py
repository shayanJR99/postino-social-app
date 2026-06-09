from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # فیلدهایی که کاربر مجاز به ویرایش آن‌ها است
        fields = ["first_name", "last_name", "username", "description", "image"]


        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'ID'}),
            'description': forms.Textarea(attrs={'class': 'input-text biography', 'placeholder': 'Bio'}),
        }