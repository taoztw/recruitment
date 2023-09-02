"""
URL configuration for recruitment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include
from django.urls import path, re_path
from django.utils.translation import gettext as _

import settings.base
from jobs.models import Job


def trigger_error(request):
  division_by_zero = 1 / 0
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'jobs', JobViewSet)


urlpatterns = [
    re_path(r"^", include("jobs.urls")),
    path("grappelli/", include('grappelli.urls')),
    path('admin/', admin.site.urls),
    re_path(r"^accounts/", include('registration.backends.simple.urls')), # 注册
    path('api-auth/', include('rest_framework.urls')),
    path('sentry-debug/', trigger_error),
    path('api/', include(router.urls)),
]


from django.conf.urls.static import static

urlpatterns += static(settings.base.MEDIA_URL,
                      document_root=settings.base.MEDIA_ROOT)
admin.site.site_header = _("招聘管理系统")