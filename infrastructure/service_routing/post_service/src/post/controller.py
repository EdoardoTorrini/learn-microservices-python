from fastapi import APIRouter, status, routing, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View

from sqlalchemy.orm import Session

from post.model import Post
from post.dto import PostDTO
from post.config import get_db
from post.service import PostService


router = APIRouter()

@View(router, path="/posts")
class PostController:

    async def get(self, uuid: str = None, db: Session = Depends(get_db)):
        if uuid is None:
            return JSONResponse(
                content=[ dict(PostDTO(uuid=post.post_uuid, user_uuid=post.user_uuid, content=post.content)) for post in PostService.get_all(db) ],
                status_code=status.HTTP_200_OK
            )
        
        post = PostService.get_post_by_id(db, uuid)
        if post is None:
            return JSONResponse(content={"message": "post not found"}, status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(
            content=dict(PostDTO(uuid=post.post_uuid, user_uuid=post.user_uuid, content=post.content),
            status_code=status.HTTP_200_OK
        ))

    async def post(self, post: PostDTO, db: Session = Depends(get_db)):
        try:
            
            new = PostService.create(db, post)
            return JSONResponse(
                content={"message": "new post create", "uuid": new.post_uuid},
                status_code=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"[-] error in create new post: {str(e)}", flush=True)
            return JSONResponse(
                content={"message": "generic error"},
                status_code=status.HTTP_400_BAD_REQUEST
            )


def get_post_router() -> APIRouter:
    return router