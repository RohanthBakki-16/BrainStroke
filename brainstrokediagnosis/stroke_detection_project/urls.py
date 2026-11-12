from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve
from django.http import HttpResponse

def robots_txt(request):
    """Serve robots.txt allowing public landing and indexing, blocking protected patient data."""
    lines = [
        "User-agent: *",
        "Allow: /login/",
        "Allow: /register/",
        "Allow: /static/",
        "Disallow: /dashboard/",
        "Disallow: /diagnosis/",
        "Disallow: /admin/",
        "Disallow: /media/",
        "",
        "Sitemap: https://brainstroke-0w0m.onrender.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def sitemap_xml(request):
    """Serve public XML sitemap for Google Search Console."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://brainstroke-0w0m.onrender.com/login/</loc>
        <lastmod>2026-11-12</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://brainstroke-0w0m.onrender.com/register/</loc>
        <lastmod>2026-11-12</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>"""
    return HttpResponse(xml, content_type="application/xml")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('', include('accounts.urls')),
    path('diagnosis/', include('diagnosis.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    # Static and Media files serving fallbacks
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
