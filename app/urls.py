from django.urls import path
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'colorpicker'
urlpatterns = [
    path('', views.predict, name='color'),
    path('token',views.get_csrf_token,name='token')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
