from fastapi import Request, status
from fastapi.responses import JSONResponse 
from sqlalchemy.exc import IntegrityError

import logging 


logger = logging.getLogger(__name__)


async def unexcepted_exception_handler( request:Request, exc:Exception ):
    # log the real error internally
    logger.exception(
        "Unexcepted Error: %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
        content= {
            "sucess": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An Unexpeccted Error Occured",
                "details": None
            }
        }
    )

async def integrity_error_handler(
        request: Request,
        exc: IntegrityError
):
    return JSONResponse(
        status_code= 409,
        content= {
            "success": False,
            "error" : {
                "code":"DATABASE_CONFLICT",
                "message": "The requested data conflicts with exsisting data",
            },
        }
    )