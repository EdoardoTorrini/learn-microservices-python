from fastapi import APIRouter, status, routing, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View

from sqlalchemy.orm import Session

from comment.model import Comment
from comment.dto import CommentDTO
from comment.config import get_db
from comment.service import CommentService


router = APIRouter()

@View(router, path="/comments")
class CommentController:

    async def get(self, uuid: str = None, db: Session = Depends(get_db)):
        if uuid is None:
            return JSONResponse(
                content=[ dict(CommentDTO(uuid=com.comment_uuid, post_uuid=com.post_uuid, content=com.content)) for com in CommentService.get_all(db) ],
                status_code=status.HTTP_200_OK
            )
        
        comment = CommentService.get_comment_by_id(db, uuid)
        if comment is None:
            return JSONResponse(content={"message": "comment not found"}, status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(
            content=dict(CommentDTO(uuid=comment.comment_uuid, post_uuid=comment.post_uuid, content=comment.content),
            status_code=status.HTTP_200_OK
        ))

    async def post(self, comment: CommentDTO, db: Session = Depends(get_db)):
        try:
            
            new = CommentService.create(db, comment)
            return JSONResponse(
                content={"message": "new comment create", "uuid": new.comment_uuid},
                status_code=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"[-] error in create new comment: {str(e)}", flush=True)
            return JSONResponse(
                content={"message": "generic error"},
                status_code=status.HTTP_400_BAD_REQUEST
            )


def get_comment_router() -> APIRouter:
    return router