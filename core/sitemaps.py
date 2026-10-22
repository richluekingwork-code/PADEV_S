from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import (
    Program, Project, NewsUpdate, SuccessStory,
    Publication, ProcurementOpportunity, Career,
    HeroSlide, ProgramStructure,
)


class ProgramSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Program.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class NewsUpdateSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return NewsUpdate.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class SuccessStorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return SuccessStory.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class PublicationSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Publication.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class ProcurementSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ProcurementOpportunity.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CareerSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Career.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class HeroSlideSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return HeroSlide.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class ProgramStructureSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ProgramStructure.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at


class StaticViewSitemap(Sitemap):
    """The fixed pages (home, about, team, ...) that have no model behind them."""
    changefreq = "monthly"

    def items(self):
        return [
            'home', 'about', 'team', 'contact', 'program_list', 'project_list',
            'news_list', 'publication_list', 'procurement_list', 'career_list',
        ]

    def location(self, item):
        return reverse(f'core:{item}')

    def priority(self, item):
        return 1.0 if item == 'home' else 0.9
