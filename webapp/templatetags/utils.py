from django import template
from django.template.loader_tags import do_extends

register = template.Library()


class ExtendsWithArgsNode(template.Node):
    def __init__(self, node, arguments):
        self.node = node
        self.arguments = arguments

    def render(self, context):
        extra_context = {}

        for item in self.arguments:
            if "=" not in item:
                continue

            key, value = item.split("=")

            if value == "":
                extra_context[key] = value
            elif value[0] in ('"', "'") and value[-1] in ('"', "'"):
                # It's a string
                extra_context[key] = value[1:-1]
            else:
                # It's a variable
                try:
                    variable = template.Variable(value)
                    extra_context[key] = variable.resolve(context)
                except template.VariableDoesNotExist:
                    extra_context[key] = ""

        context.update(extra_context)
        self.node.origin = self.origin
        return self.node.render(context)


@register.tag
def extends_with_args(parser, token):
    """
    Parse extends_with_args extension declarations.
    Arguments are made available in context to the extended template
    and its includes.
    E.g.:

    {% extends_with_args "base.html" foo="bar" baz="toto" %}
    """

    all_arguments = token.split_contents()
    token.contents = " ".join(all_arguments[:2])

    # Use do_extends to parse the tag
    return ExtendsWithArgsNode(do_extends(parser, token), all_arguments[2:])
