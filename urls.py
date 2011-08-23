from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    # GAE related from test-app
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    
    # enable admin urls
    (r'^admin/', include(admin.site.urls)),
    
    # TODO: move blog related URL's into blogengine/urls.py
    # blog - recent posts
    ('^$', 'blogengine.views.posts_recent'),
    
    # blog - edit post 
    (r'^post/edit/(?P<slug>[\w-]+)', 'blogengine.views.post_edit'),
    
    # blog - delete post 
    (r'^post/delete/(?P<slug>[\w-]+)', 'blogengine.views.post_delete_confirm'),
    (r'^post/delete-confirmed/(?P<slug>[\w-]+)', 'blogengine.views.post_delete'),
    
    # blog - view post
    (r'^post/view/(?P<slug>[\w-]+)', 'blogengine.views.post_view'),
    
    # gae bootstrap initial user
    (r'^gae-bootstrap/', 'blogengine.views.gae_bootstrap'),
)
