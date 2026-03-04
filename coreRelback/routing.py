"""
WebSocket URL routing (Phase 18).
"""
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/reports/", consumers.ReportsJobsConsumer.as_asgi()),
]
