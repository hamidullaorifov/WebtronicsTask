from app.models.posts import Post,user_ractions_table
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.utils.cache import update_likes,update_dislikes
def get_post_by_id(db, post_id):
    return db.query(Post).filter(Post.id==id).first()

def create_user_reaction(db:Session,post_id,user_id,is_like):
    try:
        query_result = db.query(user_ractions_table).filter_by(user_id=user_id,post_id=post_id)

        # Check user already reacted to post
        if query_result.count()==0:
            reaction = user_ractions_table.insert().values(
                is_like = is_like,
                user_id = user_id,
                post_id = post_id
                )
            db.execute(reaction)
            db.commit()
            if is_like:
                update_likes(post_id=post_id,incr=True)
                print("updated by cache")
            else:
                update_dislikes(post_id=post_id,incr=True)
                print("updated by cache")
        else:
            user_before_liked = query_result.filter_by(is_like=True).count()>0

            # If user before liked post and now dislike
            if user_before_liked and not is_like:
                update_dislikes(post_id,incr=True)
                update_likes(post_id,incr=False)

            # If user before disliked post and now like
            elif not user_before_liked and is_like:
                update_dislikes(post_id,incr=False)
                update_likes(post_id,incr=True)
            query_result.update({'is_like':is_like})
            db.commit()
        return True
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")

