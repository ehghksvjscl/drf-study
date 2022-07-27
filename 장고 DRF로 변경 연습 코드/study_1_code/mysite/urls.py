# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include

# from mysite.views import HomeView


# urlpatterns = [
#     # shkim
#     path('', HomeView.as_view(), name='home'),
#     path('blog/', include('blog.urls')),
#     path('api/', include('api.urls')),
# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns = [
#     path('api-auth/', include('rest_framework.urls'))
# ]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']




# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api2', include("api2.urls")),
]