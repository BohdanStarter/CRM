from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin

class BlockSalesMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.groups.filter(name='Sales').exists()

    def handle_no_permission(self):
        raise Http404("Page not found")

class BlockSupportMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.groups.filter(name='Support').exists()

    def handle_no_permission(self):
        raise Http404("Page not found")

class BlockAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.groups.filter(name='Admin').exists()

    def handle_no_permission(self):
        raise Http404("Page not found")