from django.urls import path,include
from .views import index, prediction
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index),
    path('predict/', prediction, name='predict')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)