#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/16 13:21
# @Author  : HD
# @Site    : 
# @File    : view.py
# @Software: PyCharm




from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms



def upload_file(request):
    if request.method == 'GET':
        return render(request,'upload.html')
    elif request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return render(request, 'upload.html', context={'error':'上传失败'})
        import os
        destination = open(os.path.join(os.getcwd(),myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
    return render(request, 'upload.html',  context={'success':'上传成功'})


class UserForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=10)


# 用户登录

def login(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 把获取表单的用户名传递给session对象
            request.session['username'] = username
            request.session['password'] = password
            request.session['is_login'] = True
            return HttpResponseRedirect('/index/')
    else:
        uf = UserForm()
    return render(request, 'login.html', {'uf': uf})


# 登录之后跳转页
def index(request):
    username = request.session.get('username', '未登录')
    password = request.session.get('password', '')

    return render(request,'index.html', {'username': username})


# 注销动作
def logout(request):
    if request.session.get('is_login', False):
        del request.session['username']  # 删除session
        del request.session['password']
        del request.session['is_login']
        return render(request, '/login/', {'loginstatic': '成功登出'})
    else:
        return render(request, '/login/', {'loginstatic': '尚未登录'})
