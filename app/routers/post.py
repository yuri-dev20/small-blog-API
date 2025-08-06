from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# teste básico será deletado dps
@router.get('/')
def get_post_placeholder():
    return {'msg': 'Hello posts'}