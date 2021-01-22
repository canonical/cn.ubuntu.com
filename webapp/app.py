import os

import flask
import talisker
import yaml
from canonicalwebteam import image_template
from canonicalwebteam.blog import BlogAPI, BlogViews, build_blueprint
from canonicalwebteam.discourse import DiscourseAPI, EngagePages, EngageParser
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder

from webapp.views import build_engage_index, engage_thank_you

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
authenticated_session = talisker.requests.get_session()

authenticated_discourse_api = DiscourseAPI(
    base_url="https://discourse.ubuntu.com/",
    session=authenticated_session,
    api_key=os.getenv("DISCOURSE_API_KEY"),
    api_username=os.getenv("DISCOURSE_API_USERNAME"),
)

engage_path = "/engage"
engage_pages = EngagePages(
    parser=EngageParser(
        api=authenticated_discourse_api,
        index_topic_id=19117,
        url_prefix=engage_path,
    ),
    document_template="/engage/base_engage.html",
    url_prefix=engage_path,
    blueprint_name="engage-pages",
)

app.add_url_rule(engage_path, view_func=build_engage_index(engage_pages))


def get_takeovers():
    takeovers = {}

    engage_pages.parser.parse()
    takeovers["sorted"] = sorted(
        engage_pages.parser.takeovers,
        key=lambda takeover: takeover["publish_date"],
        reverse=True,
    )
    takeovers["active"] = [
        takeover
        for takeover in engage_pages.parser.takeovers
        if takeover["active"] == "true"
    ]

    return takeovers


def takeovers_json():
    takeovers = get_takeovers()
    response = flask.jsonify(takeovers["active"])
    response.cache_control.max_age = "300"
    response.cache_control._set_cache_value(
        "stale-while-revalidate", "360", int
    )
    response.cache_control._set_cache_value("stale-if-error", "600", int)

    return response


def takeovers_index():
    takeovers = get_takeovers()

    return flask.render_template(
        "takeovers/index.html",
        takeovers=takeovers,
    )


app.add_url_rule("/takeovers.json", view_func=takeovers_json)
app.add_url_rule("/takeovers", view_func=takeovers_index)
engage_pages.init_app(app)

app.add_url_rule(
    "/engage/<page>/thank-you",
    view_func=engage_thank_you(engage_pages),
)


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
