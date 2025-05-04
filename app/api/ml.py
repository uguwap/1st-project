from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ml.predict_comment import predict_comment

router = APIRouter(prefix="/ml", tags=["ML"])


class CommentRequest(BaseModel):
    city: str
    source: str
    insect_type: str
    treatment: str


@router.post("/predict-comment")
async def predict_comment_route(request: CommentRequest):
    try:
        prediction = predict_comment(
            city=request.city,
            source=request.source,
            insect_type=request.insect_type,
            treatment=request.treatment,
        )
        return {"predicted_comment": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))