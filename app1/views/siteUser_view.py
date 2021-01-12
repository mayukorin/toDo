from django.views import View
from django.shortcuts import render, redirect
from app1.forms.siteUserForm import SiteUserRegisterForm, SiteUserLoginForm, SiteUserUpdateForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin


class SiteUserRegisterView(View):
    
    def get(self, request, *args, **kwargs):
        
        context = {'form': SiteUserRegisterForm(), }
        return render(request, 'siteUser/register.html', context)
    
    def post(self, request, *args, **kwargs):
        
        form = SiteUserRegisterForm(request.POST)
        
        if not form.is_valid():
            
            return render(request, 'siteUser/register.html', {'form': form})
        
        site_user = form.save(commit=False)
        site_user.set_password(form.cleaned_data['password'])
        site_user.flag = 0
        
        site_user.save()
        
        messages.success(request, 'ユーザの登録が完了しました')
        
        return redirect('app1:siteUser_login')
    

siteUser_register = SiteUserRegisterView.as_view()


class SiteUserUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        
        context = {'form': SiteUserUpdateForm(username=request.user.username)}
        return render(request, 'siteUser/update.html', context)
   
    def post(self, request, *args, **kwargs):
        
        form = SiteUserUpdateForm(request.user.username, request.POST)
        
        if not form.is_valid():
            
            return render(request, 'siteUser/update.html', {'form': form})
        
        if form.cleaned_data['password'] != "":
            
            request.user.set_password(form.cleaned_data['password'])
            
        request.user.username = form.cleaned_data['username']
        
        request.user.save()
        
        return redirect('app1:siteUser_logout', from_flag=1)
    
    
siteUser_update_view = SiteUserUpdateView.as_view()     
        

class SiteUserLoginView(View):
    
    def get(self, request, *args, **kwargs):
        
        context = {'form': SiteUserLoginForm(), }
        
        return render(request, 'siteUser/login.html', context)
    
    def post(self, request, *args, **kwargs):
        
        form = SiteUserLoginForm(request.POST)
        
        if not form.is_valid():
            
            return render(request, 'siteUser/login.html', {'form': form})
        
        site_user = form.get_user_cache()
        auth_login(request, site_user)
        
        messages.success(request, 'こんにちは'+request.user.username+'さん')
        
        return redirect('app1:task_list', page=1)
    
    
siteUser_login = SiteUserLoginView.as_view()


class SiteUserLogoutView(View):
    def get(self, request, from_flag, *args, **kwargs):
        
        if request.user.is_authenticated:
            
            auth_logout(request)
            
        if from_flag == 1:
            
            messages.success(request, '会員情報の更新が完了しました')
        else:
            messages.success(request, 'ログアウトしました')
        
        return redirect('app1:siteUser_login')
            
            
siteUser_logout = SiteUserLogoutView.as_view()
