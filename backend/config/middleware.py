import re
import json
from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import resolve, reverse 
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from re import compile
import logging
from config import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.urls import NoReverseMatch, resolve, reverse

# EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
# if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
#     EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

logger = logging.getLogger(__name__)


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass
        # assert hasattr(request, 'user')

        # path = request.path_info.lstrip('/')
        # url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
        # # if "dashboard" not in path:
        # #     url_is_exempt = True
        # redirect_to = settings.LOGIN_URL
        # if path == settings.LOGOUT_REDIRECT_URL.lstrip('/'):
        #     logout(request)
        # if request.user.is_authenticated or url_is_exempt:
        #     return None
        # else:
        #     return redirect(reverse(redirect_to))

        #     ## return redirect(f"{settings.LOGIN_URL}?next=/{path}")


# class LoginRequiredMiddleware(MiddlewareMixin):
#     """
#     Middleware that requires a user to be authenticated to view any page other
#     than LOGIN_URL. Exemptions to this requirement can optionally be specified
#     in settings by setting a tuple of routes to ignore
#     """
#     def process_request(self, request):
#         pass
    
    #### DECOMMENT WHEN COMPLETING ACCOUNTS APP WITH ITS URLS ####

        # if request.path.startswith(reverse('admin:index')):
        #     return None
        # assert hasattr(request, 'user'), """
        # The Login Required middleware needs to be after AuthenticationMiddleware.
        # Also make sure to include the template context_processor:
        # 'django.contrib.auth.context_processors.auth'."""

        # if not request.user.is_authenticated:
        #     current_route_name = resolve(request.path_info).url_name

        #     if not current_route_name in settings.AUTH_EXEMPT_ROUTES:
        #         return HttpResponseRedirect(reverse(settings.LOGIN_URL))


IGNORE_PATHS = [re.compile(settings.LOGIN_URL)]
IGNORE_PATHS += [
    re.compile(url) for url in getattr(settings, 'LOGIN_REQUIRED_IGNORE_PATHS', [])
]

IGNORE_VIEW_NAMES = [
    name for name in getattr(settings, 'LOGIN_EXEMPT_URLS', [])
]
class LoginRequiredMiddleware(AuthenticationMiddleware):
    """
    If LOGIN_REQUIRED is True, redirect all non-authenticated users to the login page.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path
        

        if not settings.LOGIN_REQUIRED or request.user.is_authenticated:
            return

        resolver = resolve(path)
        view_found = (True for name in IGNORE_VIEW_NAMES if name == resolver.view_name)

        path = path.split("?next=")[0]

        if not any(view_found) and not any(re.search(url, path) for url in IGNORE_PATHS):
            try:
                login_url = reverse(settings.LOGIN_URL)
            except NoReverseMatch:
                login_url = settings.LOGIN_URL
            return redirect(f'{login_url}?next={path}')



class HtmxMessageMiddleware(MiddlewareMixin):
    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        if "HX-Request" not in request.headers or 300 <= response.status_code < 400:
            return response

        messages = [{"message": str(message.message), "tags": message.tags} for message in get_messages(request)]
        if not messages:
            return response

        try:
            hx_trigger = json.loads(response.headers.get("HX-Trigger", "{}"))
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in HX-Trigger header")
            hx_trigger = {}

        hx_trigger["messages"] = messages
        response.headers["HX-Trigger"] = json.dumps(hx_trigger)
        return response