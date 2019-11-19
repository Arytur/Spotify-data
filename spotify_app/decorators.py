def token_validation(function):
    def wrap(request, *args, **kwargs):
        if 'access_token' not in request.session:
            return redirect('callback')
        else:
            return function(request, *args, **kwargs)
    return wrap
