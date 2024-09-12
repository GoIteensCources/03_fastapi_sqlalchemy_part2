import fastapi as fa
from fastapi import status, HTTPException, Query, Depends
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session, User
from sqlalchemy import select


app = fa.FastAPI(debug=True)


async def get_session():
    async with async_session() as sess:
        yield sess


@app.get("/users")
async def get_all(session: AsyncSession = Depends(get_session)):
    stmt = select(User)
    result = await session.execute(stmt)
    user = result.scalars().all()
    return {"all_users": user}


@app.get("/user/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(User).filter_by(id=user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(user)
    return {"user": user}


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(name: str = Query(), age: int = Query(), session: AsyncSession = Depends(get_session)):
    new_user = User(name=name, age=age)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {"new_user": new_user}


@app.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(name: str):
    users_name = [i["name"] for i in users]
    if name not in users_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User {name} not exists")
    id_ = users_name.index(name)
    users.pop(id_)
    return {"mess": f"{name} deleted"}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
