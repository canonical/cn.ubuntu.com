# System
import json

# Local
from website.models import Element, Page


def import_page_from_json_file(filepath):
    """
    Given a list of files containing JSON data for pages
    import data to database for any new pages
    """

    with open(filepath) as page_file:
        data = json.load(page_file)
        import_new_page(data)


def import_new_page(page_data):
    """
    Given a data object for a new CMS page
    (containing 1 Page and many Elements)
    import it as long as the page doesn't currently exist
    """

    # Split the data into the Page and the Elements
    page = next(
        (item for item in page_data if item['model'] == 'website.page'),
        None
    )
    elements = [
        item for item in page_data if item['model'] == 'website.element'
    ]

    # Create the page
    ##

    print(
        "Creating page {}: {}".format(
            page['fields']['url'],
            page['fields']['title']
        )
    )
    (page, created) = Page.objects.get_or_create(**page['fields'])

    # Stop if page already existed
    if not created:
        print("Page already exists. Moving on.")
        return False

    # Create the elements for the page
    ##
    for item in elements:
        fields = item['fields']
        fields['page'] = page

        print("Creating element: " + fields['name'])

        Element.objects.get_or_create(**fields)
