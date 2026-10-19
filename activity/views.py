from activity.models import Activity
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity
    paginate_by = 10
    def get_queryset(self):
        search = self.request.GET.get("search")
        if search:
            query = Q(customer__full_name__icontains=search)
            query.add(Q(customer__email__icontains=search), Q.OR)
            query.add(Q(description__icontains=search), Q.OR)
            query.add(Q(subject__icontains=search), Q.OR)
            query.add(Q(related_license__product__name__icontains=search), Q.OR)
            return Activity.objects.filter(query).distinct().order_by("-updated_at")
        else:
            return Activity.objects.all().order_by("-updated_at")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get("search")
        context['search'] = search
        context['search_link'] = f"&search={search}" if search else ""
        return context
