import db_services as _dbs_  # 导入数据库服务模块
from utils import api_result  # 导入工具模块

# 根据文件ID获取问题数量
def get_question_count(file_id: str):
    res = _dbs_.file.get_question_count(file_id)  # 获取问题数量
    if res != 0:
        return api_result.success(res)  # 如果问题数量不为0，返回成功结果

# 删除文件
def delete_file(file_id: str):
    _dbs_.file.delete_file(file_id)  # 删除文件
    return api_result.success("delete file success")  # 返回删除成功的结果

# 获取正在上传的文件列表
def get_uploading_files():
    res = _dbs_.file.get_uploading_files()  # 获取正在上传的文件列表
    return res  # 返回文件列表
