
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from members import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('users/', include('users.urls', namespace='users')),
    path('social-auth/', include('social_django.urls', namespace='social')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)