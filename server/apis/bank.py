import db_services as _dbs_  # 导入数据库服务模块
from utils import api_result, types, bank_handler as _bh_  # 导入工具模块

# 获取题目分类
def get_categories(language: str):
    bank_structure = _bh_.generate_structure()  # 生成银行结构
    categories_structure = bank_structure[language]  # 获取特定语言的分类结构
    res = []
    for category in categories_structure:
        res.append(category)
    return api_result.success(res)  # 返回成功结果和分类列表

# 获取题库列表
def get_banks(language: str, category: str):
    bank_structure = _bh_.generate_structure()  # 生成银行结构

    if category == 'all':  # 如果分类为'all'，则获取所有分类下的银行
        res = []
        for _category in bank_structure[language]:
            res.extend(bank_structure[language][_category])
    else:
        res = bank_structure[language][category]  # 获取特定分类下的银行

    return api_result.success(res)  # 返回成功结果和银行列表

# 导入题库到笔记
def import_bank_to_note(data: types.ImportBankData):
    # 如果存在笔记名称，则创建新的笔记，否则使用现有笔记
    if data.note_name:
        if (_dbs_.note.is_duplicate(data.note_name)):
            return api_result.error("Note name already exists")  # 如果笔记名称已存在，返回错误信息
        note_id = _dbs_.note.get_inserted_note_id(data.note_name)  # 获取已插入笔记的ID
    else:
        note_id = data.note_id

    content = _bh_.get_bank_content(  # 获取题库内容
        data.language,
        data.category,
        data.bank_name
    )

    files = content['files']  # 获取文件列表
    question_type = content['question_type']  # 获取问题类型
    designated_role = content['designated_role']  # 获取指定角色

    for file_item in files:
        file_name = file_item["file_name"]  # 获取文件名
        question_count = file_item["question_count"]  # 获取问题数量
        file_id = _dbs_.file.add_file_to_db(
            note_id, file_name, question_count, "0")  # 将文件添加到数据库中

        for document_item in file_item['documents']:
            document_content = document_item['content']  # 获取文档内容
            document_id = _dbs_.document.save_doc_to_db(
                note_id, file_id, file_name, document_content)  # 将文档保存到数据库中

            for question_content in document_item['questions']:
                _dbs_.question.save_question_to_db(
                    question_content, document_id, question_type, designated_role)  # 将问题保存到数据库中

    return api_result.success("Import question bank successfully")  # 返回成功导入题库的结果
