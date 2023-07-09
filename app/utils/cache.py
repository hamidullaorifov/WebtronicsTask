from redis import Redis
import config

redis_client = Redis(host=config.REDIS_HOST, port=6379)

def set_value(key,value):
    redis_client.set(key,value)

def get_value(key):
    value = redis_client.get(key)
    if not value:
        return None
    return value.decode()

def set_likes(post_id,count):
    set_value(f'likes_{post_id}',count)
def set_dislikes(post_id,count):
    set_value(f'dislikes_{post_id}',count)

def get_likes(post_id):
    likes = get_value(f'likes_{post_id}')
    if not likes:
        return 0
    return int(likes)
def get_dislikes(post_id):
    dislikes = get_value(f'dislikes_{post_id}')
    if not dislikes:
        return 0
    return  int(dislikes)

def update_likes(post_id,incr):
    likes = get_likes(post_id)
    if incr:
        set_likes(post_id,likes+1)
    else:
        set_likes(post_id,likes-1)
def update_dislikes(post_id,incr):
    dislikes = get_dislikes(post_id)
    if incr:
        set_dislikes(post_id,dislikes+1)
    else:
        set_dislikes(post_id,dislikes-1)


