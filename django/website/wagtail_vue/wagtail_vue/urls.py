# -*- coding: utf-8 -*-
"""Urls for app."""
from django.conf import settings
from django.urls import path
from django.conf.urls import include, static, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

# from .api import api_router

from grapple import urls as grapple_urls


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    # url(r'^api/v2/', api_router.urls),
    url(r'^api/', include(grapple_urls)),

    # url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^oidc/', include('keycloak_oidc.urls')),
    path(r'^admin/login/', RedirectView.as_view(url='http://localhost:8000/oidc/authenticate/')),
    # path(r'^admin/logout/', RedirectView.as_view(url='/oidc/logout')),

    url(r'^admin/', include(wagtailadmin_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [ # Redirect home page to admin
        url(r'^$', lambda r: HttpResponseRedirect('/admin')),
    ] + urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static.static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += (
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
