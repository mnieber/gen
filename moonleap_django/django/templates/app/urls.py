from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # TODO add urls from other apps
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
