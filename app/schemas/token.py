from pydantic import BaseModel

# define a estrutura de resposta como UserOut ou PostOut porém usado em endpoints que retorne um Token
class Token(BaseModel):
    access_token: str
    token_type: str