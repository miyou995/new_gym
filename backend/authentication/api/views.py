# from django.contrib.auth.models import User
from rest_framework import pagination, status
from rest_framework.permissions import (
    AllowAny,
    DjangoModelPermissions,
)
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken

# @method_decorator(csrf_protect, name='dispatch')

# @method_decorator(ensure_csrf_cookie, name='dispatch')


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class BaseModelPerm(DjangoModelPermissions):
    def get_custom_perms(self, method, view):
        app_name = view.queryset.model._meta.app_label
        if hasattr(view, "extra_perms_map"):
            return [perms for perms in view.extra_perms_map.get(method, [])]
        else:
            return []

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, view.queryset.model)
        perms.extend(self.get_custom_perms(request.method, view))
        return request.user and request.user.has_perms(perms)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)
            # print('refresh_token',refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            # print('eeee',e)
            return Response(
                {"error": "déconnection refusé"}, status=status.HTTP_400_BAD_REQUEST
            )
