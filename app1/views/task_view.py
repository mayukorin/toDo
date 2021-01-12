from app1.models.task import Task
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from app1.forms.taskForm import TaskRegisterForm
from django.core.paginator import Paginator, EmptyPage
from config.settings.base import PAGE_PER_ITEM, DEADLINE_FORMAT_NECESSARY, DEADLINE_FORMAT_UNNECESSARY, BASE_DIR, PROJECT_NAME


class TaskListView(LoginRequiredMixin, View):
    
    def get(self, request, page, *args, **kwargs):
        
        tasks = Task.objects.filter(site_user__id=request.user.id).order_by('deadline')
        paginator = Paginator(tasks, PAGE_PER_ITEM)
        print('aa')
        print(BASE_DIR)
        print(PROJECT_NAME)
        
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        return render(request, 'task/list.html', {'tasks': page_obj})
    
    
task_list_view = TaskListView.as_view()


class TaskRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        
        context = {'form': TaskRegisterForm()}
        return render(request, 'task/register.html', context)
    
    def post(self, request, *args, **kwargs):
        
        form = TaskRegisterForm(request.POST)
        
        if not form.is_valid():
            
            return render(request, 'task/register.html', {'form': form})
        
        task = form.save(commit=False)
        task.done_flag = False
        task.site_user = request.user
        task.save()
        
        messages.success(request, '新しいtaskの登録が完了しました')
       
        return redirect('app1:task_list', page=1)
    

task_register_view = TaskRegisterView.as_view()


class TaskShowView(LoginRequiredMixin, View):
    
    def get(self, request, task_id, page, *args, **kwargs):
        
        task = Task.objects.get(pk=task_id)
        request.session['page'] = page
        return render(request, 'task/show.html', {'task': task})
    
task_show_view = TaskShowView.as_view()


class TaskUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, task_id, *args, **kwargs):
        
        task = Task.objects.get(pk=task_id)
        
        context = {'form': TaskRegisterForm(instance=task), 'task_id': task_id, 'deadline_format_necessity': DEADLINE_FORMAT_NECESSARY}
        
        return render(request, 'task/edit.html', context)
    
    def post(self, request, task_id, *args, **kwargs):
        
        task = Task.objects.get(pk=task_id)
        form = TaskRegisterForm(request.POST, instance=task)
        
        if not form.is_valid():
            
            return render(request, 'task/edit.html', {'form': form, 'task_id': task_id, 'deadline_format_necessity': DEADLINE_FORMAT_UNNECESSARY})
        
        form.save()
        
        messages.success(request, 'taskの更新が完了しました')
        
        return redirect('app1:task_list', page=request.session['page'])
    
task_update_view = TaskUpdateView.as_view()


class TaskDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, task_id, *args, **kwargs):
        
        task = Task.objects.get(pk=task_id)
        task.delete()
        
        messages.success(request, 'taskの削除が完了しました')
        
        return redirect('app1:task_list', page=request.session['page'])
    
    
task_delete_view = TaskDeleteView.as_view()


class TaskDoneView(LoginRequiredMixin, View):
    
    def get(self, request, task_id, page, *args, **kwargs):
        
        task = Task.objects.get(pk=task_id)
        task.done_flag = not task.done_flag
        task.save()
        
        if task.done_flag is True:
            messages.success(request, 'taskを実行済みにしました')
        else:
            messages.success(request, 'taskを未実行にしました')
        
        return redirect('app1:task_list', page=page)
    
task_done_view = TaskDoneView.as_view()
