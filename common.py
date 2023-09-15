import os
import json
import hashlib
import time

file_piece_len = 16 * 1024 * 1024

# 写json
def json_dump(content, file_path, encoding=None, not_over_write=False, **kwargs):
    file_path = ez_w_path(file_path, not_over_write)
    with open(file_path, "w", encoding=encoding) as file:
        json.dump(content, file, **kwargs)
    return file_path


# 读json
def json_load(file_path, encoding=None, **kwargs):
    with open(file_path, "r", encoding=encoding) as file:
        return json.load(file, **kwargs)


# 写文件
def file_write(content, file_path, not_over_write=False, mode="w", **kwargs):
    file_path = ez_w_path(file_path, not_over_write)
    with open(file_path, mode=mode, **kwargs) as file:
        file.write(content)
    return file_path


# 读文件
def file_read(content, file_path, **kwargs):
    with open(file_path, **kwargs) as file:
        return file.read(content)


# 不覆写路径
def not_over_write_path(path, not_over_write=True):
    if not_over_write is False:
        return path
    if os.path.exists(path):
        num = 1
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)
        file_name_start = base_name[: base_name.find(".")]
        file_name_end = base_name[base_name.find(".") :]
        while True:
            temp_path = f"{dir_name}/{file_name_start}_{num}{file_name_end}"
            if os.path.exists(temp_path):
                num += 1
            else:
                break
        return temp_path
    return path


# 不要合并文件夹路径
def not_merge_folder_path(path, not_merge_folder=True):
    if not_merge_folder is False:
        return path
    if os.path.exists(path):
        num = 1
        dir_name = os.path.dirname(path)
        base_name = os.path.basename(path)
        while True:
            temp_path = f"{dir_name}/{base_name}_{num}"
            if os.path.exists(temp_path):
                num += 1
            else:
                break
        return temp_path
    return path


# 在路径结尾添加(斜杠/反斜杠)
def path_end_add_shash(path, shash=True):
    if path[-1] == "\\" or path[-1] == "/":
        return path
    else:
        if shash:
            return path + "/"
        else:
            return path + "\\"


# 在路径结尾删除(斜杠/反斜杠)
def path_end_rmv_shash(path):
    if path[-1] == "\\" or path[-1] == "/":
        return path[:-1]
    else:
        return path


# 替换斜杠
def replace_shash(str, to_shash=True):
    if to_shash:
        return str.replace("/", "\\")
    else:
        return str.replace("\\", "/")


# 斜杠分割
def cut_shash(str, shash_type=False):
    if shash_type is False:
        str = replace_shash(str)
        return str.split("\\")
    if shash_type == "\\":
        return str.split("\\")
    if shash_type == "/":
        return str.split("/")


# 获取文件hash
def hash_file(path, hash_type, upper=True):
    if isinstance(hash_type, str):
        hash_type_list = [hash_type]
    elif isinstance(hash_type, list):
        hash_type_list = hash_type

    hash_obj_list = []
    for each_hash_type in hash_type_list:
        hash_obj_list.append(hashlib.new(each_hash_type))

    with open(path, "rb") as file:
        while True:
            piece = file.read(file_piece_len)
            for each_hash_obj in hash_obj_list:
                each_hash_obj.update(piece)
            if len(piece) < file_piece_len:
                break

    hash_str_list = []
    for each_hash_obj in hash_obj_list:
        hash_str = each_hash_obj.hexdigest()
        if upper:
            hash_str = hash_str.upper()
        hash_str_list.append(hash_str)

    if len(hash_str_list) == 1:
        return hash_str_list[0]

    return hash_str_list


# 文件内容是否相同
def file_is_same(path_1, path_2, check_type="org"):
    if os.stat(path_1).st_size != os.stat(path_1).st_size:
        return False

    if check_type == "org":
        file_1 = open(path_1, "rb")
        file_2 = open(path_2, "rb")
        piece_1 = file_1.read(file_piece_len)
        piece_2 = file_2.read(file_piece_len)
        while len(piece_1) > file_piece_len:
            if piece_1 != piece_2:
                return False
            piece_1 = file_1.read(file_piece_len)
            piece_2 = file_2.read(file_piece_len)
        else:
            if piece_1 != piece_2:
                return False
        return True

    file_1_hash = hash_file(path_1, check_type)
    file_2_hash = hash_file(path_2, check_type)
    if file_1_hash != file_2_hash:
        return False
    else:
        return True


# 创建文件所在路径文件夹
def mk_folder_dir(path):
    folder_dir = os.path.dirname(path)
    if not os.path.exists(folder_dir):
        mkdir(folder_dir)


# 递归创建文件夹
def mkdir(path):
    # path_node_list = cut_shash(os.path.realpath(path))
    path = replace_path_char(path)
    path_node_list = cut_shash(path)
    for num in range(len(path_node_list)):
        temp_path = "\\".join(path_node_list[0 : num + 1])
        if os.path.exists(temp_path):
            if os.path.isfile(temp_path):
                raise ("创建路径经过节点中有同名文件，无法创建路径")
            continue
        os.mkdir(temp_path)


# 替换路径不可用字符
def replace_path_char(path):
    path = path.replace(":", "：")
    path = path.replace("*", "＊")
    path = path.replace("?", "？")
    path = path.replace('"', "＂")
    path = path.replace("<", "＜")
    path = path.replace(">", "＞")
    path = path.replace("|", "｜")
    if path[1] == "：":
        path = path[0] + ":" + path[2:]
    return path


def ez_w_path(path, not_over_write=True):
    path = not_over_write_path(path, not_over_write)
    path = replace_path_char(path)
    mk_folder_dir(path)
    return path


# hash类型
hash_type_list = [
    "SHA1",
    "sha1",
    "MD5",
    "md5",
    "SHA256",
    "sha256",
    "SHA224",
    "sha224",
    "SHA512",
    "sha512",
    "SHA384",
    "sha384",
    "blake2b",
    "blake2s",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    # "shake_128",
    # "shake_256",
]

# 各hash类型长度
hash_type_len_list = {
    "SHA1": 40,
    "sha1": 40,
    "MD5": 32,
    "md5": 32,
    "SHA256": 64,
    "sha256": 64,
    "SHA224": 56,
    "sha224": 56,
    "SHA512": 128,
    "sha512": 128,
    "SHA384": 96,
    "sha384": 96,
    "blake2b": 128,
    "blake2s": 64,
    "sha3_224": 56,
    "sha3_256": 64,
    "sha3_384": 96,
    "sha3_512": 128,
}
