from fastapi import FastAPI
from redis import Redis
import random

app = FastAPI()
redis = Redis(host="redis", port=6379, decode_responses=True)  # Redis 연결 설정

@app.get("/generate")
def generate_numbers():
    # 랜덤 숫자 3개 생성
    dice_rolls = [random.randint(1, 6) for _ in range(3)]
    # Redis에 저장
    redis.set("dice_rolls", ",".join(map(str, dice_rolls)))
    return {"message": "Numbers generated and saved!", "dice_rolls": dice_rolls}

@app.get("/sum")
def sum_numbers():
    # Redis에서 저장된 값을 가져옴
    dice_rolls = redis.get("dice_rolls")
    if dice_rolls:
        dice_list = list(map(int, dice_rolls.split(",")))
        total = sum(dice_list)
        return {"dice_rolls": dice_list, "total": total}
    else:
        return {"message": "No numbers found. Please generate numbers first."}
