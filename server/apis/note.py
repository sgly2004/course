import os  # 导入操作系统模块
import db_services as _dbs_  # 导入数据库服务模块

from fastapi import File, Form, UploadFile  # 导入FastAPI的文件、表单和上传文件模块

from utils import api_result, types, upload_file  # 导入工具模块

# 获取所有笔记列表
def get_notes():
    res = _dbs_.note.get_all_notes()  # 获取所有笔记
    return api_result.success(res)  # 返回成功结果和笔记列表

# 根据笔记ID获取笔记信息
def get_note(id: int):
    res = _dbs_.note.get_note_by_id(id)  # 根据笔记ID获取笔记信息
    return api_result.success(res)  # 返回成功结果和笔记信息

# 根据笔记ID获取文件列表
def get_files_by_id(id: int):
    res = _dbs_.note.get_all_files_by_id(id)  # 根据笔记ID获取文件列表
    return api_result.success(res)  # 返回成功结果和文件列表

# 根据笔记ID获取问题列表
def get_questions_by_note_id(note_id: int):
    LIMIT_QUESTIONS = int(os.environ["QUESTION_AMOUNT"])  # 获取问题数量限制

    expired_questions = _dbs_.question.get_expired_questions(
        note_id, LIMIT_QUESTIONS)  # 获取过期问题
    gap = 0 if LIMIT_QUESTIONS - \
        len(expired_questions) < 0 else LIMIT_QUESTIONS - len(expired_questions)  # 计算剩余问题数量

    today_questions = _dbs_.question.get_today_questions(note_id, gap)  # 获取当天问题
    gap = 0 if gap - \
        len(today_questions) < 0 else gap - len(today_questions)  # 计算剩余问题数量

    supplement_questions = _dbs_.question.get_supplement_questions(
        note_id,
        gap
    )  # 获取补充问题

    return api_result.success({
        "expired": expired_questions,  # 过期问题
        "today":  today_questions,  # 当天问题
        "supplement": supplement_questions  # 补充问题
    })

# 添加新笔记
async def add_note(
    language: str = Form(),
    noteName: str = Form(),
    questionType: str = Form(),
    uploadType: str = Form(),
    files: list[UploadFile] = File(default=None),
    notionId: str = Form(default=None),
):
    # 检查是否重复笔记名称
    if (_dbs_.note.is_duplicate(noteName)):
        return api_result.error("The same note name cannot be created repeatedly")  # 返回错误信息

    # 处理'files'上传类型
    if uploadType == 'files':
        return await _handle_files_upload(
            language=language,
            noteName=noteName,
            noteId=_dbs_.note.get_inserted_note_id(noteName),
            questionType=questionType,
            files=files
        )

    # 处理'notion'上传类型
    if uploadType == 'notion':
        return await _handle_notion_upload(notionId)

    return api_result.success("Note added successfully")  # 返回成功信息

# 添加新文件到笔记
async def add_file(
    noteId: int = Form(),
    noteName: str = Form(),
    language: str = Form(),
    questionType: str = Form(),
    uploadType: str = Form(),
    files: list[UploadFile] = File(default=None),
    notionId: str = Form(default=None)
):
    # 处理'files'上传类型
    if uploadType == 'files':
        # 检查同一笔记中是否有重复文件名
        for file in files:
            if (_dbs_.file.is_duplicate(noteId, file.filename)):
                return api_result.error(f"The same file {file.filename} cannot be uploaded under one note")  # 返回错误信息

        return await _handle_files_upload(
            language=language,
            noteName=noteName,
            noteId=noteId,
            questionType=questionType,
            files=files
        )

    # TODO 处理notion数据库
    if uploadType == 'notion':
        return await _handle_notion_upload(notionId)

    return api_result.success("Files added successfully")  # 返回成功信息

# 根据笔记ID删除笔记
def delete_note(id: int):
    _dbs_.note.delete_note(id)  # 删除笔记
    return api_result.success("Note deleted successfully")  # 返回成功信息

# 更新笔记图标
def update_note_icon(data: types.Icon):
    _dbs_.note.update_icon(data)  # 更新笔记图标
    return api_result.success("Icon updated successfully")  # 返回成功信息

# 处理文件上传
async def _handle_files_upload(language, noteName, noteId, questionType, files):
    # 检查是否上传了文件
    if not files:
        return api_result.error("At least one file must be uploaded")  # 返回错误信息

    # 检查一次性上传的文件数是否超过三个
    if len(files) > 3:
        return api_result.error("You cannot upload more than three files at once")  # 返回错误信息

    try:
        # 调用上传文件函数
        await upload_file(
            language=language,
            questionType=questionType,
            noteId=noteId,
            noteName=noteName,
            files=files
        )
        return api_result.success("Files uploaded successfully")  # 返回成功信息
    except Exception as e:
        return api_result.error(str(e))  # 返回错误信息

# 处理notion上传
async def _handle_notion_upload(notionId):
    # TODO: 在此处理notion数据库情况
    if notionId:
        pass
    return api_result.success("Notion upload handled successfully")  # 返回成功信息
