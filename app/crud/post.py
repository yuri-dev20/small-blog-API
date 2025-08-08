from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostUpdate
from app.models.post import Post
from app.models.user import User

# CRUD

# CREATE post
def crud_create_post(db: Session, user_id: int, new_post: PostCreate):
    # Verificando se usuário dono do post que será criado existe
    user = db.get(User, user_id)

    if not user:
        return None
    
    post = Post(title=new_post.title, text=new_post.text, owner_id=user_id)

    db.add(post)
    db.commit()
    db.refresh(post)

    return post
    
# GET post
# GET posts
# UPDATE post
# DELETE post