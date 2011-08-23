from django.http import HttpResponse
from django.shortcuts import render_to_response
from blogengine.models import Post
from django.template import Context, loader, RequestContext
from django.conf import settings


common_template_vars = {
                        'MEDIA_URL' : settings.MEDIA_URL, 
                        'SITE_ROOT' : settings.SITE_ROOT
                        }

# list recent blog posts
def posts_recent(request):
    
    # get the ten most recent posts
    recent_posts = Post.objects.order_by('-pub_date')[:10]
    
    template_vars = {
        'recent_posts': recent_posts,
    }
    
    template_vars.update(common_template_vars)
    
    return render_to_response("blog/recent.html", template_vars, context_instance=RequestContext(request))
    
def post_edit(request, slug):
    if request.user.has_perm('change_post'):
        t = loader.get_template('blog/edit_post.html')
        
        # if the slug is 'NEW-POST', this is a new post
        if slug == 'NEW-POST':
            p = Post()
        else:
            try:
               post = Post.objects.get(slug=slug)
            except:       
               post = False
        


        updated = False

        # if this is a form post, get the posted values 
        if request.POST:
           post.title = request.POST['post_title']
           
           # get the slug value from the form - if it doesn't 
           # match the value from the URI, it will need to be changed
           
          
           
           post.pub_date = request.POST['post_pub_date']
           post.body = request.POST['post_body']
           
           # TODO - validation..
           post.save()
           updated = True
           
           
           if request.is_ajax():
               return HttpResponse('1')

        context = {
           'slug': slug,
           'snippet' : snippet,
           'updated' : updated
        }
        context.update(common_template_vars)

        c = RequestContext(request, context)
        return HttpResponse(t.render(c))
    else:
        return HttpResponse('user not authenticated, or does not have permission to edit the snippet');


    
