from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm
from .models import User,Profile

# ۱. فرم ساخت کاربر جدید در ادمین
class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# ۲. فرم ویرایش کاربر در ادمین
class MyUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text="Password hashes help keep your password secure. "
                  "You can change the password using <a href=\"../password/\">this form</a>."
    )

    class Meta:
        model = User
        fields = '__all__'

# ۳. تنظیمات نهایی پنل ادمین
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    # فرم‌هایی که بالا ساختیم را اینجا معرفی می‌کنیم
    form = MyUserChangeForm
    add_form = MyUserCreationForm

    # فیلدهایی که در لیست نمایش داده می‌شوند
    list_display = ('email', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')
    
    # فیلدهایی که در صفحه ویرایش نمایش داده می‌شوند
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_date', 'updated_date')}),
    )

    # فیلدهایی که موقع ساخت کاربر نمایش داده می‌شوند
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password'),
        }),
    )

    search_fields = ('email', )
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('created_date', 'updated_date', 'last_login')



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # فیلدهایی که می‌خواهید برای پروفایل در ادمین نمایش داده شود
    list_display = ('user', 'first_name','last_name') 