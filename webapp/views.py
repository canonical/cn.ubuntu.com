import flask
import math


def build_engage_index(engage_docs):
    def engage_index():
        page = flask.request.args.get("page", default=1, type=int)
        topic = flask.request.args.get("topic", default=None, type=str)
        sort = flask.request.args.get("sort", default=None, type=str)
        posts_per_page = 15
        engage_docs.parser.parse()
        metadata = engage_docs.parser.metadata

        total_pages = math.ceil(len(metadata) / posts_per_page)

        return flask.render_template(
            "engage/index.html",
            forum_url=engage_docs.parser.api.base_url,
            metadata=metadata,
            page=page,
            topic=topic,
            sort=sort,
            posts_per_page=posts_per_page,
            total_pages=total_pages,
        )

    return engage_index


def engage_thank_you(engage_pages):
    """
    Renders an engage pages thank-you page
    i.e. whitepapers, pdfs

    If there is no current topic it can't render the page
    e.g. accessing directly

    @parameters: language (optional) and page path name
    e.g. /cloud-init-whitepaper
    @returns: a function that renders a template
    """

    def render_template(page):
        engage_pages.parser.parse()
        page_url = f"/engage/{page}"
        index_topic_data = next(
            (
                item
                for item in engage_pages.parser.metadata
                if item["path"] == page_url
            ),
            None,
        )

        if index_topic_data:
            topic_id = engage_pages.parser.url_map[page_url]
            engage_page_data = engage_pages.parser.get_topic(topic_id)
            request_url = flask.request.referrer
            resource_name = index_topic_data["type"]
            resource_url = engage_page_data["metadata"]["resource_url"]
            related = [item for item in engage_page_data["related"]]
            template = "engage/thank-you.html"

            return flask.render_template(
                template,
                request_url=request_url,
                resource_name=resource_name,
                resource_url=resource_url,
                engage_page_data=engage_page_data["metadata"],
                related=related,
            )
        else:
            return flask.abort(404)

    return render_template

