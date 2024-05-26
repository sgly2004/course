import os

from fastapi import UploadFile

import db_services as _dbs_
import llm_services as _llms_

from loaders import split_doc


async def upload_file(
    language: str,
    questionType: str,
    noteId: int,
    noteName: str,
    files: list[UploadFile],
):
    """
    上传多个文件并根据其内容生成问题。

    :param language: 生成问题的语言。
    :param questionType: 问题类型。
    :param noteId: 与文件关联的笔记ID。
    :param noteName: 笔记名称。
    :param files: 要上传的文件的 UploadFile 对象列表。
    :return: None
    """
    collection = []
    error_files = []

    for file in files:
        file_dict = {}
        file_dict["id"] = _dbs_.file.add_file_to_db(noteId, file.filename)
        file_dict["name"] = file.filename
        file_dict["content"] = await file.read()
        collection.append(file_dict)

    for item in collection:
        filename = item["name"]
        file_id = item["id"]
        file_content = item["content"]

        # 将文件保存到临时目录
        not os.path.isdir(f"./temp") and os.mkdir("./temp")
        with open(f"./temp/{filename}", "w+", encoding="utf-8") as f:
            f.write(file_content.decode('utf-8'))
        docs = split_doc(filename)
        # 移除临时文件
        os.remove(f"./temp/{filename}")

        # 创建 LangChain 服务实例
        langchain_service = _llms_.Chain(
            note_id=noteId,
            file_id=file_id,
            filename=filename,
            prompt_language=language,
            prompt_type="question_generate"
        )

        try:
            # 使用 LangChain 服务生成问题
            question_count = await langchain_service.agenerate_questions(
                docs,
                noteName,
                questionType,
            )
            # 处理未生成问题的情况
            if question_count == 0:
                _dbs_.file.delete_file(file_id)
                raise ("error")
        except Exception as e:
            error_files.append((filename))
        finally:
            # 设置文件的上传状态
            _dbs_.file.set_file_is_uploading_state(file_id, question_count)

    if error_files:
        error_messages = "\n".join([f"{f}" for f in error_files])
        raise Exception(
            f"Error: \n{error_messages} upload failed because no questions were generated, please check 'Best Documentation Practices' to optimize your note")
