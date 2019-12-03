"""Additional in template functions for the lattedb module
"""
from django import template


register = template.Library()  # pylint: disable=C0103


@register.inclusion_tag("progress-bar.html")
def render_progress_bar(danger, warning, info, success, total):
    if total > 0:
        context = {
            "danger": danger / total * 100,
            "warning": warning / total * 100,
            "info": info / total * 100,
            "success": success / total * 100,
            "total": total,
        }
    else:
        context = {
            "danger": 0,
            "warning": 0,
            "info": 0,
            "success": 0,
            "total": 0,
        }

    return context
