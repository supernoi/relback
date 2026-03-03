"""
backup_tags: Interface Adapter / Presenter layer for backup status display.

Clean Architecture note:
  These template tags are strictly presentational. They know about DaisyUI
  CSS classes and Material Icons — they must NEVER contain business logic
  (no status transitions, no threshold calculations, no DB queries).

Usage:
    {% load backup_tags %}

    {# Render a DaisyUI badge for a BackupStatusValue or raw string #}
    {% backup_badge job.status %}

    {# Compact variant (icon only, no label text) #}
    {% backup_badge job.status compact=True %}
"""
from django.utils.html import format_html
from django import template

register = template.Library()


# ---------------------------------------------------------------------------
# Status → presentation mapping
# Keys match BackupStatusValue enum values (and their .value strings).
# DaisyUI classes used: badge-success, badge-info, badge-warning, badge-error,
# badge-neutral.  INTERRUPTED uses badge-ghost + violet inline style since
# it has no DaisyUI built-in semantic token (custom color in tailwind.config.js).
# ---------------------------------------------------------------------------
_STATUS_CONFIG: dict[str, dict] = {
    "COMPLETED": {
        "badge_class": "badge-success",
        "icon": "check_circle",
        "label": "Completed",
        "style": "",
    },
    "RUNNING": {
        "badge_class": "badge-info",
        "icon": "sync",
        "label": "Running",
        "style": "",
    },
    "WARNING": {
        "badge_class": "badge-warning",
        "icon": "warning",
        "label": "Warning",
        "style": "",
    },
    "FAILED": {
        "badge_class": "badge-error",
        "icon": "error_outline",
        "label": "Failed",
        "style": "",
    },
    "INTERRUPTED": {
        # No DaisyUI built-in — uses ghost base + violet from tailwind.config.js
        # backup.interrupted token: #7c3aed (light) / #a78bfa (dark)
        "badge_class": "badge-ghost",
        "icon": "block",
        "label": "Interrupted",
        "style": "color:#a78bfa;border-color:#a78bfa;",
    },
    "UNKNOWN": {
        "badge_class": "badge-neutral",
        "icon": "help_outline",
        "label": "Unknown",
        "style": "",
    },
}

_DEFAULT_CONFIG = _STATUS_CONFIG["UNKNOWN"]


@register.simple_tag
def backup_badge(status, compact: bool = False) -> str:
    """Render a DaisyUI badge for a backup job status.

    Args:
        status: A ``BackupStatusValue`` enum member OR its raw string value
                (e.g. ``"COMPLETED"``).  Handles both because templates may
                receive either from the context.
        compact: When True, renders icon only (no label text) — useful in
                 narrow table columns.

    Returns:
        Safe HTML string: ``<span class="badge …">…</span>``

    Example::

        {% backup_badge job.status %}
        {% backup_badge job.status compact=True %}
    """
    # Normalise: enum members expose .value; raw strings are used as-is.
    key = getattr(status, "value", str(status)).upper()
    cfg = _STATUS_CONFIG.get(key, _DEFAULT_CONFIG)

    badge_class = cfg["badge_class"]
    icon = cfg["icon"]
    label = cfg["label"]
    inline_style = cfg["style"]

    style_attr = format_html(' style="{}"', inline_style) if inline_style else ""

    if compact:
        return format_html(
            '<span class="badge badge-sm {cls}" title="{title}"{style}>'
            '<i class="material-icons" style="font-size:12px;vertical-align:middle;">{icon}</i>'
            "</span>",
            cls=badge_class,
            title=label,
            style=style_attr,
            icon=icon,
        )

    return format_html(
        '<span class="badge badge-sm {cls}"{style}>'
        '<i class="material-icons md-me-1" style="font-size:12px;vertical-align:middle;">{icon}</i>'
        "{label}"
        "</span>",
        cls=badge_class,
        style=style_attr,
        icon=icon,
        label=label,
    )
