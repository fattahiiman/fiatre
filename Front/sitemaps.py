from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from Episode.models import *
from Subscription.models import *

class StaticPagesViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['about_us' , 'terms' , 'faq']

    def location(self, item):
        return reverse(item)

class EpisodesViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Episode.objects.all()

    def lastmod(self, obj):
       return obj.updated_at


class CategoriesViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
       return obj.updated_at


class SubscriptionPlansViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Type.objects.all()

    def lastmod(self, obj):
       return obj.updated_at