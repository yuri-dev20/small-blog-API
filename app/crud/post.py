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

# READ posts
def crud_read_all_posts(db: Session, user_id: int):
    user = db.get(User, user_id)

    if not user:
        return None
    # isso diz 'execute uma query SQL JOIN buscando todos os posts que pertencem ao usuário de id tal'
    return db.execute(select(Post).where(Post.owner_id == user_id)).scalars().all()

# READ post
def crud_read_post(db: Session, user_id: int, post_id: int):
    user = db.get(User, user_id)

    if not user:
        return None
    
    return db.execute(select(Post).where((Post.owner_id == user_id) & (Post.id == post_id))).scalar_one_or_none()

# UPDATE post
def crud_update_post(db: Session, user_id: int, post_id: int, post_update_data: PostUpdate):
    user = db.get(User, user_id)

    if not user:
        return None
    
    post = db.execute(select(Post).where((Post.owner_id == user_id) & (Post.id == post_id))).scalar_one_or_none()

    if not post:
        return None

    if post_update_data.title is not None:
        post.title = post_update_data.title
    
    if post_update_data.text is not None:
        post.text = post_update_data.text

    db.commit()
    db.refresh(post)

    return post

# DELETE post