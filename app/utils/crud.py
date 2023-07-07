from app.models.posts import Post,user_ractions_table
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
def get_post_by_id(db, post_id):
    return db.query(Post).filter(Post.id==id).first()

def create_user_reaction(db:Session,post_id,user_id,is_like):
    try:
        query_result = db.query(user_ractions_table).filter_by(user_id=user_id,post_id=post_id)
        if query_result.count()==0:
            reaction = user_ractions_table.insert().values(
                is_like = is_like,
                user_id = user_id,
                post_id = post_id
                )
            db.execute(reaction)
            db.commit()
        else:
            query_result.update({'is_like':is_like})
            db.commit()
        return True
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Database error")

