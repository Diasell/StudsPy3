"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from .settings import MEDIA_ROOT, DEBUG
from django.conf.urls import url, include, patterns
from django.contrib import admin
from .routers import router, bot_router, auth_router, schedule_router, news_router


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^telegram/', include(bot_router.urls)),
    url(r'^auth/', include(auth_router.urls)),
    url(r'^schedule/', include(schedule_router.urls)),
    url(r'^news/', include(news_router.urls)),
    url(r'^docs/', include('rest_framework_docs.urls')),

]

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT})
    )
