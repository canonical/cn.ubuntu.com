import yaml
import talisker

from canonicalwebteam.blog import build_blueprint, BlogViews, BlogAPI
from canonicalwebteam.flask_base.app import FlaskBase
from canonicalwebteam.templatefinder import TemplateFinder
from canonicalwebteam import image_template

app = FlaskBase(
    __name__,
    "cn.ubuntu.com",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
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
