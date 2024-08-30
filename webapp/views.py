import flask
import math
import re

#  Packages
import talisker.requests
from requests import Session

session = talisker.requests.get_session()


def build_engage_index(engage_docs):
    def engage_index():
        page = flask.request.args.get("page", default=1, type=int)
        topic = flask.request.args.get("topic", default=None, type=str)
        sort = flask.request.args.get("sort", default=None, type=str)
        posts_per_page = 15
        metadata = engage_docs.get_index()

        total_pages = math.ceil(len(metadata) / posts_per_page)

        return flask.render_template(
            "engage/index.html",
            forum_url=engage_docs.api.base_url,
            metadata=metadata,
            page=page,
            topic=topic,
            sort=sort,
            posts_per_page=posts_per_page,
            total_pages=total_pages,
        )

    return engage_index


def build_engage_page(engage_pages):
    def engage_page(page):
        path = f"/engage/{page}"
        metadata = engage_pages.get_engage_page(path)
        if not metadata:
            flask.abort(404)
        else:
            return flask.render_template(
                "engage/base_engage.html",
                forum_url=engage_pages.api.base_url,
                metadata=metadata,
            )

    return engage_page


def match_tags(tags_1, tags_2):
    for tag_1 in tags_1:
        for tag_2 in tags_2:
            if tag_1.strip().lower() == tag_2.strip().lower():
                return True
            else:
                continue

    return False


def engage_thank_you(engage_pages):
    """
    Renders an engage pages thank-you page
    i.e. whitepapers, pdfs

    If there is no current topic it can't render the page
    e.g. accessing directly
    """

    def render_template(page):
        path = f"/engage/{page}"
        metadata = engage_pages.get_engage_page(path)
        all_engage_pages = engage_pages.get_index()
        if not metadata:
            flask.abort(404)

        total_num_related = 3
        related = []
        for item in all_engage_pages:
            # Match language and match tags
            if match_tags(
                item["tags"].split(","), metadata["tags"].split(",")
            ):
                related.append(item)
            if len(related) < total_num_related:
                # we can only fit 3 related posts, no need to finish the loop
                break

        template = "engage/thank-you.html"

        return flask.render_template(
            template,
            request_url=flask.request.referrer,
            metadata=metadata,
            resource_name=metadata["type"],
            resource_url=metadata["resource_url"],
            related=related,
        )

    return render_template

def build_engage_pages_sitemap(engage_pages):
    """
    Create sitemaps for each engage page
    """

    def ep_sitemap():
        links = []
        (
            metadata,
            count,
            active_count,
            current_total,
        ) = engage_pages.get_index()

        if len(metadata) == 0:
            flask.abort(404)

        for page in metadata:
            links.append(
                {
                    "url": f'https://cn.ubuntu.com{page["path"]}',
                    "last_updated": page["updated"].strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                }
            )

        xml_sitemap = flask.render_template("sitemap.xml", links=links)

        response = flask.make_response(xml_sitemap)
        response.headers["Content-Type"] = "application/xml"
        response.headers["Cache-Control"] = "public, max-age=43200"

        return response

    return ep_sitemap

def sitemap_index():
    xml_sitemap = flask.render_template("sitemap_index.xml")
    response = flask.make_response(xml_sitemap)

    response.headers["Content-Type"] = "application/xml"
    return response


class BlogView(flask.views.View):
    def __init__(self, blog_views):
        self.blog_views = blog_views

class BlogSitemapIndex(BlogView):
    def dispatch_request(self):

        response = session.get(
            "https://admin.insights.ubuntu.com/sitemap_index.xml"
        )

        xml = response.text.replace(
            "https://admin.insights.ubuntu.com/",
            "https://cn.ubuntu.com/blog/sitemap/",
        )
        xml = re.sub(r"<\?xml-stylesheet.*\?>", "", xml)

        response = flask.make_response(xml)
        response.headers["Content-Type"] = "application/xml"
        return response


class BlogSitemapPage(BlogView):
    def dispatch_request(self, slug):
        response = session.get(f"https://admin.insights.ubuntu.com/{slug}.xml")

        if response.status_code == 404:
            return flask.abort(404)

        xml = response.text.replace(
            "https://admin.insights.ubuntu.com/", "https://cn.ubuntu.com/blog/"
        )
        xml = re.sub(r"<\?xml-stylesheet.*\?>", "", xml)

        response = flask.make_response(xml)
        response.headers["Content-Type"] = "application/xml"
        return response