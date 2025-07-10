from typeguard import typechecked
from fastapi_class import View
from fastapi.responses import JSONResponse

from user.user import User
from user.user_service import UserService

from fastapi import APIRouter, status, HTTPException


router = APIRouter()

@View(router, path="/users")
class UserController:

    _service = UserService()

    async def get(self, email: str = ""):

        if email is "":
            return JSONResponse(
                content={"result": self._service.all()}, 
                status_code=status.HTTP_200_OK
            )
        
        return JSONResponse(
            content={"result": self._service.find_by_email(email)}, 
            status_code=status.HTTP_200_OK
        )
    
    async def post(self, user: User):
        try:
            self._service.save(user)
            return JSONResponse(
                content={"message": "ok"}, 
                status_code=status.HTTP_201_CREATED
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        
    async def put(self, user: User):
        try:
            self._service.update(user)
            return JSONResponse(
                content={"message": "ok"},
                status_code=status.HTTP_202_ACCEPTED
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

def get_user_route() -> APIRouter:
    return router