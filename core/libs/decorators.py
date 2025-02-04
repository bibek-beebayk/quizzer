from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.urls import reverse

def superadmin_required(view_func=None, login_url=None, raise_exception=False):
    """
    Decorator to restrict access to superadmin users only.
    
    Args:
        view_func: The view function to be decorated
        login_url: Optional URL to redirect non-authenticated users
        raise_exception: Whether to raise PermissionDenied instead of redirecting
    
    Usage:
    @superadmin_required
    def admin_view(request):
        # Only accessible by superadmin
        return render(request, 'admin.html')
    """

    def check_superadmin(user):
        return user.is_authenticated and user.is_superuser
    
    if view_func is None:
        return lambda fn: superadmin_required(fn, login_url, raise_exception)
    
    decorator = user_passes_test(
        check_superadmin,
        login_url = login_url
    )

    return decorator(view_func)