from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix='/users', 
    tags=['Users'])

# teste básico será deletado dps
@router.get('/')
def get_user_placeholder():
    return {'msg': 'Hello user'}