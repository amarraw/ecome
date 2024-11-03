from django.shortcuts import redirect 

def auth_middleware(get_response):

    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        if not request.session.get('User'):
            return redirect(f'/auth/login?return_url={returnUrl}')
        response = get_response(request)
        return response

    return middleware