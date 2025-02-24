from http.client import HTTPResponse
from tokenize import Comment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.analytics.models import PageVisit
from apps.blog.models import Blog, Comment
from django.views.decorators.http import require_POST


def blog_list_view(request):
    context = {}
    blogs = Blog.published().prefetch_related("categories").order_by("-publish_at")
    paginator = Paginator(blogs, 10)
    page = request.GET.get("page")
    try:
        paginated_blogs = paginator.page(page)
    except PageNotAnInteger:
        paginated_blogs = paginator.page(1)
    except EmptyPage:
        paginated_blogs = paginator.page(paginator.num_pages)
    context["blogs"] = paginated_blogs

    PageVisit.create_object(request)
    return render(request, "blog/list.html", context)


def blog_detail_view(request, slug):
    context = {}
    blog = Blog.objects.get(slug=slug)
    context["blog"] = blog
    context["related_posts"] = (
        Blog.published().exclude(id=blog.id).order_by("-publish_at")[:5]
    )
    if request.user.is_authenticated:
        context["has_commented"] = blog.comments.filter(user=request.user).exists()

    PageVisit.create_object(request, blog.id)
    return render(request, "blog/detail.html", context)


@require_POST
def edit_comment(request):
    comment_id = request.POST.get("comment_id")
    comment_text = request.POST.get("comment")
    comment = get_object_or_404(Comment, id=comment_id)
    comment.text = comment_text
    comment.save()
    return redirect("blog", slug=Blog.objects.get(id=comment_id).slug)


@require_POST
def delete_comment(request):
    comment_id = request.POST.get("comment_id")
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect("blog", slug=Blog.objects.get(id=comment_id).slug)
