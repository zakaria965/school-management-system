from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Announcement, Message, Notification
from academics.models import ClassSection


@login_required
def communications_dashboard(request):
    announcements = Announcement.objects.filter(is_published=True)[:5]
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:10]
    return render(request, 'communications/dashboard.html', {
        'announcements': announcements,
        'notifications': notifications
    })


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    fields = ['title', 'content', 'priority', 'target_roles', 'target_classes', 'is_published']
    template_name = 'communications/form.html'
    success_url = reverse_lazy('announcement-list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Announcement created')
        return super().form_valid(form)


class AnnouncementListView(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'communications/announcement_list.html'
    context_object_name = 'announcements'
    
    def get_queryset(self):
        qs = Announcement.objects.all()
        if not self.request.user.is_admin:
            qs = qs.filter(is_published=True)
        return qs


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['recipient', 'subject', 'content']
    template_name = 'communications/form.html'
    success_url = reverse_lazy('message-list')
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        messages.success(self.request, 'Message sent')
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'communications/message_list.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user) | Message.objects.filter(recipient=self.request.user)


class InboxView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'communications/inbox.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-created_at')


class SentView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'communications/sent.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-created_at')


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'communications/notification_list.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, pk):
    notification = Notification.objects.get(pk=pk)
    if notification.user == request.user:
        notification.is_read = True
        notification.save()
    return redirect('notification-list')


@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:10]
    data = [{'id': n.pk, 'title': n.title, 'message': n.message, 'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')} for n in notifications]
    return JsonResponse(data, safe=False)