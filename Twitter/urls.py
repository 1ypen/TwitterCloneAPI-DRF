from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import debug_toolbar

from Twitter import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tweet/', include('tweet.urls')),
    path('api/comment/', include('comment.urls')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
