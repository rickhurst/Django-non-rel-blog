from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from blogengine.models import Post
from django.template import Context, loader, RequestContext
from django.conf import settings


common_template_vars = {
                        'MEDIA_URL' : settings.MEDIA_URL, 
                        'SITE_ROOT' : settings.SITE_ROOT,
                        'SITE_TITLE' : settings.SITE_TITLE,
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

# display post edit form
# handles postback of form content for updating of new and existing posts
def post_edit(request, slug):
    if request.user.has_perm('change_post'):
        t = loader.get_template('blog/edit_post.html')
        
        from datetime import datetime
        
        form_errors = [] # list to store form error messages
        
        # if the slug is 'NEW-POST', this is a new post
        if slug == 'NEW-POST':
            post = Post()
            post.slug_for_form = "NEW-POST"
            post.pub_date = datetime.now()
        else:
            try:
               post = Post.objects.get(slug=slug)
               post.slug_for_form = post.slug
            except:       
               post = False

        updated = False

        # if this is a form post, get the posted values 
        if request.POST:

            post.title = request.POST['post_title']
            
            if post.title == '':
                form_errors.append('You must provide a post title')
           
            # get the slug value from the form - if it doesn't 
            # match the value from the URI, it will need to be changed
            post.slug = request.POST['post_slug']
            
            # TODO: check slug doesn't already exist
            
            # create a slug from the post title if there isn't one provided
            if post.slug == '':
                slug = post.title
                slug = slug.replace(' ', '-')
                slug = slug.replace('(', '')
                slug = slug.replace(')', '')
                slug = slug.lower()
                # TODO: run this string through a method to replace all but specified character set.
                post.slug = slug 


            date_string = request.POST['post_pub_date']

            try: 
               post.pub_date = datetime.strptime(date_string, '%d/%m/%Y')
            except:
               form_errors.append('You must provide a valid date in the format dd/mm/yyyy')
   

            post.body = request.POST['post_body']

            # TODO - more validation..
            if len(form_errors) == 0:
                post.save()
                post.slug_for_form = post.slug
                updated = True

            # if the request was made via AJAX - return 1 as a success code
            # TODO: handle failures and pass form errors back as JSON
            if request.is_ajax():
               return HttpResponse('1')

        template_vars = {
           'slug': slug,
           'post' : post,
           'updated' : updated,
           'form_errors' : form_errors
        }
        
        template_vars.update(common_template_vars)

        c = RequestContext(request, template_vars)
        return HttpResponse(t.render(c))
    else:
        return HttpResponse('user not authenticated, or does not have permission to edit the post');
        
# display confirm for post delete (fallback for non-javascript enabled)      
def post_delete_confirm(request, slug):
    if request.user.has_perm('change_post'):
        try:
           post = Post.objects.get(slug=slug)
        except:       
           post = False
    
        template_vars = {
            'post': post,
        }

        template_vars.update(common_template_vars)
    
        return render_to_response("blog/delete_post_confirm.html", template_vars, context_instance=RequestContext(request))
    else:
        return HttpResponse('user not authenticated, or does not have permission to edit the post');
    
# delete post     
def post_delete(request, slug):
    if request.user.has_perm('change_post'):
        try:
            post = Post.objects.get(slug=slug)
            post.delete()
        except:       
            post = False
        
        template_vars = {}
        template_vars.update(common_template_vars)

        return render_to_response("blog/delete_post_deleted.html", template_vars, context_instance=RequestContext(request))
    else:
        return HttpResponse('user not authenticated, or does not have permission to edit the post');
        
# view post
def post_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except:       
        post = False
        
    if post:
        template_vars = {
            'post': post
        }
        template_vars.update(common_template_vars)
        return render_to_response("blog/view.html", template_vars, context_instance=RequestContext(request))
    else:
        raise Http404

# add blogadmin user to the db
# there must be a better way of doing this?
# after running this script, you will need to update
# the user record in GAE admin so that the user is staff/ superuser
# and then change the password from within django admin
def gae_bootstrap(request):
    from django.contrib.auth.models import User
    try:
      u = User.objects.get(username__exact='blogadmin')
      return HttpResponse('user exists');
    except:
      
      user = User.objects.create_user('blogadmin','rick.hurst@gmail.com', 'changemequick')
      return HttpResponse('added user');



    
