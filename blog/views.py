from django.shortcuts import render

# Create your views here.
def blog_list(request):
    # Try without status filter first
    posts_list = BlogPost.objects.all().order_by('-created_at')    
    # Now add status filter
    posts_list = posts_list.filter(status='published')    
    category_slug = request.GET.get('category')
    posts_list = BlogPost.objects.filter(status='published').order_by('-created_at')
    
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        posts_list = posts_list.filter(category=category)
        current_category = category

    else:
        current_category = None
    
    # Get featured post (using the first published post as featured)
    featured_post = BlogPost.objects.filter(
        status='published',
        featured_image__isnull=False
    ).first()
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    page = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    categories = BlogCategory.objects.all()
    
    context = {
        'posts': posts,
        'featured_post': featured_post,
        'categories': categories,
        'current_category': current_category,
    }
 
    return render(request, 'landing/blog/list.html', context)
