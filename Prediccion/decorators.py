from django.contrib.auth.decorators import user_passes_test


def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and user.is_admin(),
        login_url='login'
    )(view_func)
    return decorated_view_func


def registered_user_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and user.is_registered(),
        login_url='login'
    )(view_func)
    return decorated_view_func
