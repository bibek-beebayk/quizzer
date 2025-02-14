from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone

from apps.analytics.models import PageVisit
from apps.blog.models import Blog


def blog_list_view(request):
    context = {}
    blogs = (
        Blog.published().prefetch_related("categories")
        .order_by("-publish_at")
    )
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
    context["related_posts"] = Blog.published().exclude(id=blog.id).order_by("-publish_at")[:5]
    if request.user.is_authenticated:
        context["has_commented"] = blog.comments.filter(user=request.user).exists()
    
    PageVisit.create_object(request, blog.id)
    return render(request, "blog/detail.html", context)

