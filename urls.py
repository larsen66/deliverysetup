from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    // ... existing code ...
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 