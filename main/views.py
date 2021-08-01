from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.signing import BadSignature

from .models import *
from .forms import *
from .utilities import *


def index(request):
    events = Event.objects.all()
    context = {'events': events, }
    return render(request, 'main/index.html', context)


@login_required
def profile(request):
    vol = Volunteer.objects.get(pk=request.user.pk)
    events = Event.objects.filter(volunteers=vol)
    context = {'user': vol, 'events': events}
    return render(request, 'main/profile.html', context)


# class EventDetail(DetailView):
#     model = Event
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


def detail_event(request, pk):
    event = Event.objects.get(pk=pk)
    if request.user.is_authenticated:
        user = get_object_or_404(Volunteer, pk=request.user.pk)
        followed = False
        for v in event.volunteers.all():
            if user.username == v.username:
                followed = True
        context = {'event': event, 'user': user, 'followed': followed}
    else:
        context = {'event': event, }
    if event.name.lower().find('раздельный сбор'):
        wastes = Waste.objects.filter(date=event.date)
        context['wastes'] = wastes
    return render(request, 'main/event_detail.html', context)


def follow_event(request, pk, status):
    event = Event.objects.get(pk=pk)
    if status == 'followed':
        event.volunteers.add(request.user)
    elif status == 'unfollowed':
        event.volunteers.remove(request.user)
    return redirect('index')


def register_volunteer(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if request.recaptcha_is_valid and form.is_valid():
            form.save()
            return render(request, 'main/bid_complete.html')
    else:
        form = RegistrationForm()
    context = {'form': form, }
    return render(request, 'main/registration.html', context)


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(Volunteer, username=username)
    if user.is_active:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.save()
    return render(request, template)


class Login(LoginView):
    template_name = 'main/login.html'
    redirect_field_name = 'next'


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Volunteer
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('index')
    success_message = 'Пароль пользователя изменен'


class PasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_complete.html'
# Create your views here.
