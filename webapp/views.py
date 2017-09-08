# Modules
from django.utils.cache import patch_response_headers
from django_template_finder_view import TemplateFinder


class CmsTemplateFinder(TemplateFinder):
    def get_context_data(self, **kwargs):
        """
        Get context data fromt the database for the given page
        """

        # Get any existing context
        context = super(CmsTemplateFinder, self).get_context_data(**kwargs)

        # Add level_* context variables
        clean_path = self.request.path.strip('/')
        for index, path, in enumerate(clean_path.split('/')):
            context["level_" + str(index + 1)] = path

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
