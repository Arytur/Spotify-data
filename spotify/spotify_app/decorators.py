from typing import Any, Callable, TypeVar, cast

from django.shortcuts import redirect

F = TypeVar('F', bound=Callable[..., Any])


def token_validation(func: F) -> F:
    def wrapper(request, *args, **kwargs):
        if 'access_token' not in request.session:
            return redirect('callback')
        else:
            return func(request, *args, **kwargs)
    return cast(F, wrapper)
