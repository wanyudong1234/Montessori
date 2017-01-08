# modify the system coding ways
# coding=utf-8

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=50, required=True, error_messages={'required':'请输入用户名'})
    password = forms.CharField(label="密码", widget=forms.PasswordInput, required=True, error_messages={'required':'请输入密码'})