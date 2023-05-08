from django.urls import path

from . import views

"""
Основные маршруты приложения website.
"""

app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("profile_edit", views.profile_edit, name="profile_edit"),
    path("service", views.service_view, name="service"),
    path("service/<int:pk>", views.service_info, name="service_info"),
    path("comment", views.comments, name="comment"),
    path("comment_add", views.comment_add, name="comment_add"),
    path(
        "comment/<int:pk>/update",
        views.CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("gallery", views.gallery, name="photo-gallery"),
]
