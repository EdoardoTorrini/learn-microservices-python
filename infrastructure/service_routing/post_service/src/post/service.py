from sqlalchemy.orm import Session

from post.model import Post
from post.dto import PostDTO

from datetime import datetime


class PostService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Post).all()
    
    @staticmethod
    def get_post_by_id(db: Session, uuid: str):
        return db.query(Post).filter(Post.post_uuid == uuid).first()
    
    @staticmethod
    def create(db: Session, post: PostDTO) -> Post:
        new_post = Post(
            post_uuid=post.uuid,
            user_uuid=post.user_uuid,
            content=post.content
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post