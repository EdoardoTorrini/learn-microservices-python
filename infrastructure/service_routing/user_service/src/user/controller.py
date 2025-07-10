from fastapi import APIRouter, status, routing, Depends
from fastapi.responses import JSONResponse
from fastapi_class import View

from sqlalchemy.orm import Session

from user.model import User
from user.dto import UserDTO
from user.config import get_db
from user.service import UserService



router = APIRouter()

@View(router, path="/users")
class UserController:

    async def get(self, uuid: str = None, db: Session = Depends(get_db)):
        if uuid is None:
            return JSONResponse(
                content=[ dict(UserDTO(uuid=user.user_uuid, nickname=user.nickname, birthday=user.birthday.strftime("%d-%m-%Y"))) for user in UserService.get_all(db) ],
                status_code=status.HTTP_200_OK
            )
        
        user = UserService.get_user_by_id(db, uuid)
        if user is None:
            return JSONResponse(content={"message": "user not found"}, status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(
            content=dict(UserDTO(uuid=user.user_uuid, nickname=user.nickname, birthday=user.birthday.strftime("%d-%m-%Y"))),
            status_code=status.HTTP_200_OK
        )

    async def post(self, user: UserDTO, db: Session = Depends(get_db)):
        try:
            
            new = UserService.create(db, user)
            return JSONResponse(
                content={"message": "new user create", "uuid": new.user_uuid},
                status_code=status.HTTP_201_CREATED
            )

        except Exception as e:
            print(f"[-] error in create new user: {str(e)}", flush=True)
            return JSONResponse(
                content={"message": "generic error"},
                status_code=status.HTTP_400_BAD_REQUEST
            )


def get_user_router() -> APIRouter:
    return router