from django import template
register = template.Library()


@register.tag(name="Split_String")
def Do_Split_String(parser, token):
    try:
        tag_name, stringValue, KeyValue = token.split_contents()
        print(tag_name, stringValue, KeyValue)
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return stringValue.split(KeyValue[1:-1])[0]


@register.filter('list')
def do_list(value, startindex):
    return range(int(startindex), int(value)) if int(startindex) == 0 else range(1, int(value) + 1)


@register.filter('NumberCompare')
def do_compare(value, description):
    if eval('%s>%s' % (value, description)):
        result = 'greater'
    elif eval('%s<%s' % (value, description)):
        result = 'less'
    else:
        result = 'equal'
    return result

@register.filter('GetDictValue')
def get_value(dict, key):
    return dict[key]