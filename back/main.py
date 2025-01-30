from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import Base, engine, get_db
from models import Counter
from schemas import Action

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (필요 시 제한 가능)
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

Base.metadata.create_all(bind=engine)

@app.get('/count')
def get_count(db: Session = Depends(get_db)):
    counter = db.query(Counter).first()
    if not counter:
        counter = Counter(count=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)
    return {"count": counter.count}


@app.post('/update_count')
def update_count(request: Action, db: Session = Depends(get_db)):
    action = request.action
    # 데이터를 수정하려면 Counter.count가아닌 Counter 객체를 가져와야함
    counter = db.query(Counter).first()
    if not counter:
        raise HTTPException(status_code=404, detail="count not found")
    if action == "decrease":
        counter.count -= 1
    elif action == "increase":
        counter.count += 1
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()
    db.refresh(counter)

    return {"count":counter.count}
