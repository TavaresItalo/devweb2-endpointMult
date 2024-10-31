from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Operands(BaseModel) :
    op1 : float
    op2 : float

@app.post("/mult")
async def multiply(operands: Operands) :
    result = operands.op1 * operands.op2
    return {"result" : result}