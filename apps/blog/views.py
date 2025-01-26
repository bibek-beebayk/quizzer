from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils import timezone

from apps.blog.models import Blog


def blog_list_view(request):
    context = {}
    blogs = (
        Blog.objects.select_related("category")
        .filter(publish_at__lte=timezone.now())
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
    return render(request, "blog/list.html", context)
