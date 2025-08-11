from pydantic import BaseModel
from typing import Optional

# define a estrutura de resposta como UserOut ou PostOut porém usado em endpoints que retorne um Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(Token):
    email: Optional[str] = None