# Modules
from django.utils.cache import patch_response_headers
from django_template_finder_view import TemplateFinder

# Local
from models import Page


class CmsTemplateFinder(TemplateFinder):
    def get_context_data(self, **kwargs):
        """
        Get context data fromt the database for the given page
        """

        # Get any existing context
        context = super(CmsTemplateFinder, self).get_context_data(**kwargs)

        # Get CMS data for this page
        clean_path = self.request.path.strip('/')
        page_set = Page.objects.filter(url=clean_path)

        # Add level_* context variables
        for index, path, in enumerate(clean_path.split('/')):
            context["level_" + str(index + 1)] = path

        # If CMS data exists, add it to context
        if page_set.exists():
            page = page_set.first()
            context['page_title'] = page.title

            for element in page.elements.all():
                context[element.name] = element.text

        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Add caching headers to the standard render_to_response from the parent
        """

        response = super(CmsTemplateFinder, self).render_to_response(
            context, **response_kwargs
        )

        patch_response_headers(response, cache_timeout=300)

        return response
