from sqlalchemy.orm import Session

from comment.model import Comment
from comment.dto import CommentDTO

from datetime import datetime


class CommentService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Comment).all()
    
    @staticmethod
    def get_comment_by_id(db: Session, uuid: str):
        return db.query(Comment).filter(Comment.comment_uuid == uuid).first()
    
    @staticmethod
    def create(db: Session, comment: CommentDTO) -> Comment:
        new_comment = Comment(
            comment_uuid=comment.uuid,
            post_uuid=comment.post_uuid,
            content=comment.content
        )

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment