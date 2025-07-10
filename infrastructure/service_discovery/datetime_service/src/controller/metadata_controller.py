from fastapi_class import View
from fastapi import APIRouter, status, Request, routing
from fastapi.responses import JSONResponse

import os


router = APIRouter()


@View(router, path="/metadata")
class MetadataController:

    async def get(self, request: Request):
        
        return JSONResponse(
            content={
                "service": os.getenv("CONSUL_NAME_SERVICE"),
                "endpoints": [
                    {
                        "path": route.path,
                        "methods": list(route.methods),
                        "name": route.name
                    }
                    for route in request.app.routes if isinstance(route, routing.APIRoute)
                ]
            },
            status_code=status.HTTP_200_OK
        )

def get_metadata_route() -> APIRouter:
    return router