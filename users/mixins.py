from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

class RedirectAuthenticatedUserMixin(UserPassesTestMixin):
    """
    Mixin to redirect authenticated users away from login/signup pages.
    """
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('generator:post-list')