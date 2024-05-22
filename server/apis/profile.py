from fastapi import File, UploadFile  # 导入FastAPI的文件和上传文件模块
from fastapi.responses import FileResponse, JSONResponse  # 导入FastAPI的文件响应和JSON响应模块

import db_services as _dbs_  # 导入数据库服务模块
import llm_services as _llms_  # 导入LLM服务模块

from utils import api_result, types  # 导入工具模块

# 获取用户配置文件
def get_profile():
    data = _dbs_.profile.get_profile()  # 获取用户配置数据
    return api_result.success(data)  # 返回成功结果和数据

# 设置用户配置文件
def set_profile(data: types.Profile):
    _dbs_.profile.set_profile(data)  # 设置用户配置数据
    _dbs_.profile.set_profile_to_env()  # 将配置数据设置到环境中
    return api_result.success()  # 返回成功结果

# 检查LLM API状态
def check_llm_api_state():
    try:
        payment = _llms_.check_llm_api_state()  # 检查LLM API状态
    except Exception as e:
        return api_result.error(str(e))  # 如果出现异常，返回错误信息

    return api_result.success(payment)  # 返回成功结果和支付信息

# 导出数据
def export_data(isProfile: bool, isNotes: bool):
    if (isProfile == False and isNotes == False):
        return api_result.error("Must export at least one type data")  # 如果未选择导出任何类型数据，返回错误信息

    try:
        _dbs_.profile.export_data(isProfile, isNotes)  # 导出数据
    except Exception as e:
        return api_result.error(str(e))  # 如果出现异常，返回错误信息

    return FileResponse("data.xlsx", headers={  # 返回文件响应，以Excel文件形式下载导出的数据
        "Content-Disposition": "attachment; filename=data.xlsx"
    })

# 导入数据
def import_data(file: UploadFile = File()):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return api_result.error("Only .xlsx files are allowed")  # 如果文件类型不是.xlsx，返回错误信息

    file_path = "data.xlsx"
    with open(file_path, "wb") as f:
        f.write(file.file.read())  # 将上传的文件写入本地

    try:
        _dbs_.profile.import_data()  # 导入数据
    except Exception as e:
        return api_result.error(str(e))  # 如果出现异常，返回错误信息

    return api_result.success("File uploaded and saved as data.xlsx")  # 返回成功结果
