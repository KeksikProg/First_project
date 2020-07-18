from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from .forms import PostForm, AIFormSet
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Post, AdditionalImage, Comment
from django.http import HttpResponseForbidden
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import ChangeUserInfoForm, CommentForm
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q



def home(request):
	posts = Post.objects.all()
	paginator = Paginator(posts, 2)
	if 'page' in request.GET:
		page_num = request.GET['page']
	else:
		page_num = 1
	page = paginator.get_page(page_num)
	context = {'posts' : page.object_list, 'page' : page}
	return render(request, 'news/home.html', context)

def other(request, page): # Это будет наша страница со скучными бумагами
	try:
		template = get_template('news/' + page + '.html') # Пытаемся получить шаблон
	except TemplateDoesNotExist: # Если не находит такуб страницу
		raise Http404 # То ошибка 404 (страница не найдена)
	return HttpResponse(template.render(request = request)) # Иначе вернуть ответ клиенту


def add(request):
	if request.user.is_superuser:
		if request.method == 'POST':
			form = PostForm(request.POST, request.FILES)
			if form.is_valid():
				post = form.save()
				formset = AIFormSet(request.POST, request.FILES, instance = post)
				if formset.is_valid():
					formset.save()
					messages.add_message(request, messages.SUCCESS, message = 'Пост успешно добавлен')
					return redirect ('news:home')
		else:
			form = PostForm(initial = {'author' : request.user.pk})
			formset = AIFormSet()
		context = {'form' : form, 'formset' : formset}
		return render (request, 'news/add.html', context)
	else:
		raise Http404

@login_required
def detail(request, pk):
	post = Post.objects.get(pk = pk)
	ai = post.additionalimage_set.all()
	comment = Comment.objects.filter(post = pk)
	initial = {'post':post.pk}
	if request.user.is_authenticated:
		initial['author'] = request.user.username
		form_class = CommentForm
	form = form_class(initial=initial)
	if request.method == 'POST':
		c_form = form_class(request.POST)
		if c_form.is_valid():
			response = c_form.save()
			response.author = request.user.username
			response.save()
			messages.add_message(request, messages.SUCCESS, message = 'Комментарий успешно добавлен')
		else:
			form = c_form
			messages.add_message(request, messages.WARNING, message = 'Комментарий не был добавлен')		
	context = {'post' : post, 'ai' : ai, 'comment':comment, 'form':form}
	return render(request, 'news/detail.html', context)

def comment_delete(request, comments):
	if request.user.is_superuser:
		comment = get_object_or_404(Comment, pk = comments)
		if request.method == 'POST':
			comment.delete()
			messages.add_message(request, messages.SUCCESS, message = 'Коммент удален!')
			return redirect('news:home')
		else:
			context = {'comment' : comment}
			return render(request, 'news/comment_delete.html', context)
	else:
		raise Http404


def post_delete(request, pk):
	if request.user.is_superuser:
		post = get_object_or_404(Post, pk = pk)
		if request.method == 'POST':
			post.delete()
			messages.add_message(request, messages.SUCCESS, message = 'Пост удален!')
			return redirect('news:home')
		else:
			context = {'post' : post}
			return render(request, 'news/post_delete.html', context)
	else:
		raise Http404

def post_change(request, pk):
	if request.user.is_superuser:
		post = get_object_or_404(Post, pk = pk)
		if request.method == 'POST':
			form = PostForm(request.POST, request.FILES, instance = post)
			if form.is_valid():
				post = form.save()
				formset = AIFormSet(request.POST, request.FILES, instance = post)
				if formset.is_valid():
					formset.save()
					messages.add_message(request, messages.SUCCESS, message = 'Пост изменен!')
					return redirect('news:home')
		else:
			form = PostForm(instance = post)
			formset = AIFormSet(instance = post)
		context = {'form' : form, 'formset' : formset}
		return render(request, 'news/post_change.html', context)
	else:
		raise Http404

class UserRegister(CreateView, SuccessMessageMixin, LoginRequiredMixin):
	model = User
	template_name = 'news/register.html'
	form_class = UserRegForm
	success_messsage = 'Пользователь успешно создан!'
	success_url = reverse_lazy('news:home')


class PostLogin(LoginView):
	template_name = 'news/login.html'
	success_url = reverse_lazy('news:home')

class PostLogout(LogoutView, LoginRequiredMixin):
	template_name = 'news/logout.html'

class ChangeUserInfo(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
	model = User
	template_name = 'news/change_user_info.html'
	form_class = ChangeUserInfoForm
	success_url = reverse_lazy('news:home')
	success_messsage = 'Личные данные пользователя были успешно изменены!'

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class DeleteUserView(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
	model = User
	template_name = 'news/delete_user.html'
	success_url = reverse_lazy('news:home')

	def dispatch(self, request, *args, **kwargs):
		self.user_id = request.user.pk
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		logout(request)
		messages.add_message(request, messages.SUCCESS, message = 'Пользователь успешно удален!')
		return super().post(request, *args, **kwargs)

	def get_object(self, queryset=None):
		if not queryset:
			queryset = self.get_queryset()
		return get_object_or_404(queryset, pk = self.user_id)

class UserPasswordChange(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
	template_name = 'news/change_password.html'
	success_url = reverse_lazy('news:home')
	success_messsage = 'Пароль успешно изменен!'
# Create your views here.
