# ======================= moduls/User.py 类定义 ========================

import json
import os
import bcrypt
from cryptography.fernet import Fernet

class User:
    """用户类，包含用户名、密码哈希和手机号"""
    def __init__(self, username, password_hash, phone):
        self.username = username
        self.password_hash = password_hash
        self.phone = phone
        self.is_super_admin = False
        self.is_family_admin = False

    def __repr__(self):
        return f"<User {self.username} | {self.phone}>"

    def to_dict(self):
        return {
            'type': 'User',
            'username': self.username,
            'password_hash': self.password_hash.decode(),
            'phone': self.phone
        }

class FamilyAdmin(User):
    def __init__(self, username, password_hash, phone):
        super().__init__(username, password_hash, phone)
        self.is_family_admin = True

    def __repr__(self):
        return f"<FamilyAdmin {self.username} | {self.phone}>"

    def to_dict(self):
        return {
            'type': 'FamilyAdmin',
            'username': self.username,
            'password_hash': self.password_hash.decode(),
            'phone': self.phone
        }

class SuperAdmin(User):
    def __init__(self):
        super().__init__("root", bcrypt.hashpw(b"supersecure", bcrypt.gensalt()), phone=None)
        self.is_super_admin = True

    def __repr__(self):
        return "<SuperAdmin root>"

# =================== 数据库加密相关 ====================

DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DB_FILE = os.path.join(DATA_DIR, 'users.hcdb')
KEY_FILE = os.path.join(DATA_DIR, 'secret.key')

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)

def load_key():
    with open(KEY_FILE, 'rb') as f:
        return f.read()

def encrypt_data(data: dict) -> bytes:
    fernet = Fernet(load_key())
    return fernet.encrypt(json.dumps(data).encode())

def decrypt_data(data: bytes) -> dict:
    fernet = Fernet(load_key())
    return json.loads(fernet.decrypt(data).decode())

def save_db(user_list):
    data = [user.to_dict() for user in user_list]
    encrypted = encrypt_data({'users': data})
    with open(DB_FILE, 'wb') as f:
        f.write(encrypted)

def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'rb') as f:
        encrypted = f.read()
        raw_data = decrypt_data(encrypted)
        users = []
        for entry in raw_data['users']:
            password_hash = entry['password_hash'].encode()
            phone = entry.get('phone', '')
            if entry['type'] == 'User':
                users.append(User(entry['username'], password_hash, phone))
            elif entry['type'] == 'FamilyAdmin':
                users.append(FamilyAdmin(entry['username'], password_hash, phone))
        return users
    
def clear_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("数据库已清空（文件已删除）。")
    else:
        print("数据库文件不存在，无需清空。")

# =================== 系统操作逻辑 ====================

def register_user(username, raw_password, phone, as_admin=False, super_admin=None):
    if not (phone.isdigit() and len(phone) == 11):
        print("手机号必须为11位数字")
        return

    users = load_db()
    # 手机号唯一性校验 - 新增
    if any(u.phone == phone for u in users):
        print("该手机号已被注册")
        return
    if any(u.username == username for u in users):
        print("用户名已存在")
        return

    password_hash = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())

    if as_admin:
        if not isinstance(super_admin, SuperAdmin):
            print("只有超级管理员才能注册管理员账号")
            return
        new_user = FamilyAdmin(username, password_hash, phone)
    else:
        new_user = User(username, password_hash, phone)

    users.append(new_user)
    save_db(users)
    print(f"注册成功: {new_user}")

# 修改登录函数，支持用手机号登录 - 新增参数 login_by_phone
def login(account, password, login_by_phone=False):
    # 超级管理员只支持用户名登录
    if not login_by_phone and account == 'root':
        root = SuperAdmin()
        if bcrypt.checkpw(password.encode(), root.password_hash):
            print("登录成功：超级管理员")
            return root
        else:
            print("密码错误")
            return None

    users = load_db()

    if login_by_phone:
        # 手机号登录
        for user in users:
            if user.phone == account and bcrypt.checkpw(password.encode(), user.password_hash):
                print(f"登录成功：{user}")
                return user
    else:
        # 用户名登录
        for user in users:
            if user.username == account and bcrypt.checkpw(password.encode(), user.password_hash):
                print(f"登录成功：{user}")
                return user

    print("用户名/手机号或密码错误")
    return None

def promote_to_family_admin(target_username, super_admin):
    if not isinstance(super_admin, SuperAdmin):
        print("只有超级管理员才能升级用户权限")
        return

    users = load_db()
    for i, user in enumerate(users):
        if isinstance(user, User) and user.username == target_username:
            users[i] = FamilyAdmin(user.username, user.password_hash, user.phone)
            save_db(users)
            print(f"{target_username} 已升级为家庭管理员")
            return
    print("未找到该普通用户或已是管理员")

# ======================= 示例使用 =======================

if __name__ == '__main__':

    clear_database()
    
    generate_key()
    root = SuperAdmin()

    print("注册普通账号：")
    register_user("alice", "123456", "13812345678")

    print("\n超级管理员注册家庭管理员：")
    register_user("bob", "admin123", "13987654321", as_admin=True, super_admin=root)

    print("\n手机号注册重复测试：")
    register_user("alice2", "123456", "13812345678")  # 手机号重复，注册失败

    print("\n登录测试 - 用户名登录：")
    login("alice", "123456")

    print("\n登录测试 - 手机号登录：")
    login("13987654321", "admin123", login_by_phone=True)

    print("\n登录超级管理员：")
    login("root", "supersecure")

    print("\n升级权限测试：")
    promote_to_family_admin("alice", root)

    print("\n最终用户数据库：")
    for u in load_db():
        print(u)
