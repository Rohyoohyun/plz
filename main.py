from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import randint
from models import DiceRoll, Base

# FastAPI 앱 생성
app = FastAPI()

# MySQL 데이터베이스 연결 설정 (docker-compose에서 MySQL 설정에 맞춰야 합니다)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rootpassword@mysql:3306/dice_db"

# SQLAlchemy 엔진 및 세션 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/generate")
def generate_numbers():
    # 랜덤 주사위 값 3개 생성
    roll_1 = randint(1, 6)
    roll_2 = randint(1, 6)
    roll_3 = randint(1, 6)
    total = roll_1 + roll_2 + roll_3

    # 데이터베이스에 저장
    db = SessionLocal()
    new_roll = DiceRoll(roll_1=roll_1, roll_2=roll_2, roll_3=roll_3, total=total)
    db.add(new_roll)
    db.commit()
    db.refresh(new_roll)
    db.close()

    return {"message": "Numbers generated and saved!", "dice_rolls": [roll_1, roll_2, roll_3], "total": total}

@app.get("/sum")
def sum_numbers():
    # 데이터베이스에서 최근 주사위 값 조회
    db = SessionLocal()
    last_roll = db.query(DiceRoll).order_by(DiceRoll.id.desc()).first()
    db.close()
    
    if last_roll:
        return {"dice_rolls": [last_roll.roll_1, last_roll.roll_2, last_roll.roll_3], "total": last_roll.total}
    else:
        return {"message": "No numbers found. Please generate numbers first."}
