from fastapi import FastAPI, File, Form, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

import apis as _apis_  # 导入 API 实现
import db_services as _dbs_  # 导入数据库服务
from utils import types  # 导入类型定义

app = FastAPI()  # 创建 FastAPI 应用实例

# 在应用启动时执行的操作
@app.on_event('startup')
def startup():
    _dbs_.profile.set_profile_to_env()  # 设置配置文件

# 在应用关闭时执行的操作
@app.on_event("shutdown")
def shutdown_event():
    pass

# -------- Profile APIs --------

# 获取用户配置信息
@app.get("/profile")
def get_profile():
    return _apis_.profile.get_profile()

# 更新用户配置信息
@app.put("/profile")
def set_profile(data: types.Profile):
    return _apis_.profile.set_profile(data)

# 检查 Low-Level Management API 状态
@app.get("/profile/auth/llm")
def check_llm_api_state():
    return _apis_.profile.check_llm_api_state()

# 导出 MySQL 数据
@app.get("/profile/data")
def get_mysql_data(isProfile: bool, isNotes: bool):
    return _apis_.profile.export_data(isProfile, isNotes)

# 导入 MySQL 数据
@app.post("/profile/data")
def set_mysql_data(file: UploadFile = File()):
    return _apis_.profile.import_data(file)

# -------- Note APIs --------

# 获取所有笔记
@app.get("/note/notes")
def get_notes():
    return _apis_.note.get_notes()

# 添加新笔记
@app.post("/note")
async def add_note(
    language: str = Form(),
    noteName: str = Form(),
    questionType: str = Form(),
    uploadType: str = Form(),
    files: list[UploadFile] = File(default=None),
    notionId: str = Form(default=None),
):
    return await _apis_.note.add_note(
        language=language,
        noteName=noteName,
        questionType=questionType,
        uploadType=uploadType,
        files=files,
        notionId=notionId
    )

# 根据ID获取笔记
@app.get("/note/{id}")
def get_note(id: int):
    return _apis_.note.get_note(id)

# 根据ID获取笔记的文件
@app.get("/note/{id}/files")
def get_files_by_id(id: int):
    return _apis_.note.get_files_by_id(id)

# 向笔记添加文件
@app.post("/note/{id}/file")
async def add_files_to_note(
    id: int,
    language: str = Form(),
    noteName: str = Form(),
    questionType: str = Form(),
    uploadType: str = Form(),
    files: list[UploadFile] = File(default=None),
    notionId: str = Form(default=None)
):
    return await _apis_.note.add_file(
        noteId=id,
        language=language,
        noteName=noteName,
        questionType=questionType,
        uploadType=uploadType,
        files=files,
        notionId=notionId
    )

# 根据笔记ID获取相关问题
@app.get("/note/{id}/questions")
def get_questions_by_note_id(id: int):
    return _apis_.note.get_questions_by_note_id(id)

# 删除笔记
@app.delete("/note/{id}")
def delete_note(id: int):
    return _apis_.note.delete_note(id)

# 更新笔记图标
@app.patch("/note/icon")
def update_note_icon(data: types.Icon):
    return _apis_.note.update_note_icon(data)

# -------- File APIs --------

# 删除文件
@app.delete("/file")
def delete_file(id: int):
    return _apis_.file.delete_file(id)

# 根据ID获取问题数量
@app.get("/file/{id}/questionCount")
def get_quesiton_count(id: int):
    return _apis_.file.get_question_count(id)

# 文件上传 WebSocket
@app.websocket("/ws/file/uploading")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            uploading_files = {"data": _apis_.file.get_uploading_files()}
            await websocket.send_json(uploading_files)
    except WebSocketDisconnect:
        pass

# -------- Question APIs --------

# 提交问题
@app.post("/question/examine")
async def examine_question(data: types.AnswerQuestion):
    return StreamingResponse(
        _apis_.question.examine_question(data),
        media_type="text/event-stream"
    )

# 获取最后一个问题的答案
@app.get("/question/{id}/lastAnswer")
def get_last_answer(id: int):
    return _apis_.question.get_last_answer(id)

# 获取问题的文档
@app.get("/question/{id}/document")
def get_document(id: int):
    return _apis_.question.get_document(id)

# 获取随机问题
@app.get("/question/random")
def get_random_question():
    return _apis_.question.get_random_question()