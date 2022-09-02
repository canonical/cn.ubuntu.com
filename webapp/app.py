import os

import flask
import talisker
import yaml
from canonicalwebteam import image_template
from canonicalwebteam.blog import BlogAPI, BlogViews, build_blueprint
from canonicalwebteam.discourse import DiscourseAPI, EngagePages
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder

from webapp.views import (
    build_engage_index,
    build_engage_page,
    engage_thank_you,
)

app = FlaskBase(
    __name__,
    "cn.ubuntu.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)


# Engage pages and takeovers from Discourse
# This section needs to provide takeover data for /
session = talisker.requests.get_session()

discourse_api = DiscourseAPI(
    base_url="https://discourse.ubuntu.com/",
    session=session,
    api_key=os.getenv("DISCOURSE_API_KEY"),
    api_username=os.getenv("DISCOURSE_API_USERNAME"),
    get_topics_query_id=14,
)


takeovers_path = "/takeovers"
discourse_takeovers = EngagePages(
    api=discourse_api,
    page_type="takeovers",
    category_id=111,
    exclude_topics=[29331, 29444],
)

engage_path = "/engage"
engage_pages = EngagePages(
    api=discourse_api,
    category_id=110,
    page_type="engage-pages",
    exclude_topics=[29444, 29331],
)

app.add_url_rule(engage_path, view_func=build_engage_index(engage_pages))
app.add_url_rule("/engage/<page>", view_func=build_engage_page(engage_pages))
app.add_url_rule(
    "/engage/<page>/thank-you",
    view_func=engage_thank_you(engage_pages),
)


def takeovers_json():
    active_takeovers = discourse_takeovers.parse_active_takeovers()
    takeovers = sorted(
        active_takeovers,
        key=lambda takeover: takeover["publish_date"],
        reverse=True,
    )
    response = flask.jsonify(takeovers)
    response.cache_control.max_age = "300"
    response.cache_control._set_cache_value(
        "stale-while-revalidate", "360", int
    )
    response.cache_control._set_cache_value("stale-if-error", "600", int)

    return response


def takeovers_index():
    all_takeovers = discourse_takeovers.get_index()
    all_takeovers.sort(
        key=lambda takeover: takeover["active"] == "true", reverse=True
    )
    active_count = len(
        [
            takeover
            for takeover in all_takeovers
            if takeover["active"] == "true"
        ]
    )

    return flask.render_template(
        "takeovers/index.html",
        takeovers=all_takeovers,
        active_count=active_count,
    )


app.add_url_rule("/takeovers.json", view_func=takeovers_json)
app.add_url_rule("/takeovers", view_func=takeovers_index)


template_finder_view = TemplateFinder.as_view("template_finder")
session = talisker.requests.get_session()
app.add_url_rule("/", view_func=template_finder_view)
app.add_url_rule("/<path:subpath>", view_func=template_finder_view)

blog_views = BlogViews(
    api=BlogAPI(session=session, thumbnail_width=354, thumbnail_height=199),
    tag_ids=[3265],
    blog_title="博客",
    per_page=11,
)
app.register_blueprint(build_blueprint(blog_views), url_prefix="/blog")

# read releases.yaml
with open("releases.yaml") as releases:
    releases = yaml.load(releases, Loader=yaml.FullLoader)


# Template context
@app.context_processor
def context():
    return {"releases": releases}


# Image template
@app.context_processor
def utility_processor():
    return {"image": image_template}
