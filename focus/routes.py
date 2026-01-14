
from http import HTTPStatus

from loguru import logger
from fastapi import APIRouter

from focus import ModelRequest, ModelResponse
from focus.modules.handler import ExtrClsHandler


router = APIRouter()
extr_cls_handler = ExtrClsHandler()

def init_routes():
    @router.get("/", status_code=HTTPStatus.OK)
    async def root():
        logger.warning("Router healh Interaction.")
        return {"healthy": HTTPStatus.OK}

    @router.post("/model", status_code=HTTPStatus.OK, response_model=ModelResponse)
    async def model(annot_req: ModelRequest):
        logger.warning("Router model Interaction.")
        model_res = extr_cls_handler(text=annot_req.text)
        response = ModelResponse(
            req_id=annot_req.req_id,
            card=model_res.card,
            azs=model_res.azs,
            trk=model_res.trk,
            fuel=model_res.fuel,
            topic=model_res.topic,
            sub=model_res.sub,
        )
        return response
