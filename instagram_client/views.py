import json
import os
import urllib

from django.http.response import HttpResponse
from django.shortcuts import redirect
from instagram import InstagramAPI

import settings

def photos(request, code=None):
    code = request.GET.get('code', None)
    client_id = settings.INSTAGRAM_CLIENT_ID
    client_secret = settings.INSTAGRAM_CLIENT_SECRET
    redirect_uri = settings.INSTAGRAM_REDIRECT_URI
    api = InstagramAPI(client_id=client_id, client_secret=client_secret,
        redirect_uri=redirect_uri)
    if not code:
        redirect_url = api.get_authorize_login_url()
        return redirect(redirect_url)

    access_token = api.exchange_code_for_access_token(code)
    api = InstagramAPI(access_token=access_token[0])
    media = api.user_recent_media(user_id=access_token[1]['id'], count=10)

    # create the base dir for all the downloads
    if not os.path.exists(settings.BASE_PHOTOS_DIR):
        os.makedirs(settings.BASE_PHOTOS_DIR)

    user_dir = os.path.join(settings.BASE_PHOTOS_DIR, access_token[1]['username'])
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    os.chdir(user_dir)

    metadata = []

    for md in media[0]:
        if not md.type == 'image':
            continue
        url = md.get_standard_resolution_url()
        filename = url.split('/')[-1]
        try:
            f = open(filename,'wb') 
            f.write(urllib.urlopen(url).read())
            f.close()
            metadata.append({
                'filename': filename,    
                'url': url,
                'created_time': str(md.created_time),
                'caption': md.caption
            })
        except IOError as e:
            print e.message
            
    with open('metadata.json', 'w+') as fp:
        json.dump(metadata, fp)

    return HttpResponse('<h3>Your photos have been downloaded to %s !<h3>' % user_dir)
