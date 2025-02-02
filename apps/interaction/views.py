from apps.interaction.models import Comment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType


from apps.blog.models import Blog


@login_required
@require_POST
def add_blog_comment(request, blog_id):
    comment_text = request.POST.get("comment")
    blog = Blog.objects.get(id=blog_id)
    content_type = ContentType.objects.get_for_model(Blog)
    Comment.objects.create(
        user=request.user,
        content_type=content_type,
        object_id=blog_id,
        text=comment_text,
    )
    return redirect("blog", blog.slug)
