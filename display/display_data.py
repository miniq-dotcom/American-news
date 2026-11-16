import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
import os
import json
from pathlib import Path
from typing import Any
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

# 创建FastAPI实例
app = FastAPI(title="American News")

# 挂载静态文件的存放目录
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# 数据模型
class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any   # 任意类型的数据

# 定义操作函数
@app.get("/")
def root():
    return FileResponse(BASE_DIR / "static/index.html")

@app.get("/api/news")
def get_news() -> ApiResponse:
    with open(BASE_DIR / "data/news.json", "r", encoding='utf-8') as f:
        news_list = json.load(f)
    return ApiResponse(code=200, message="加载新闻成功", data=news_list)


# with open("../data/news.json", 'w', encoding="utf-8") as f:
#     json.dump(news_list, f, ensure_ascii=False, indent=4)


# 启动项目
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)