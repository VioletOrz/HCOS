from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from moduls.User import load_db, register_user, login, SuperAdmin, FamilyAdmin
from moduls.appliances.brands.haier import HaierWasher
from moduls.appliances.brands.xiaomi import XiaomiLight

app = Flask(__name__)
app.secret_key = 'your_secret_key'

root_admin = SuperAdmin()

# 首页
@app.route('/')
def home():
    return render_template('index.html')

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        login_by_phone = request.form.get('mode') == 'phone'

        user = login(account, password, login_by_phone)
        if user:
            flash('登录成功', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名/手机号或密码错误', 'error')

    return render_template('login.html')

# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']

        users_before = len(load_db())
        register_user(username, password, phone)
        users_after = len(load_db())

        if users_after > users_before:
            flash('注册成功！请登录', 'success')
            return redirect(url_for('login_user'))
        else:
            flash('注册失败，请检查输入或手机号是否重复', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

# 控制面板
@app.route('/dashboard')
def dashboard():
    appliances = [
        XiaomiLight("客厅灯", "light-001"),
        HaierWasher("洗衣机", "washer-123")
    ]
    users = load_db()
    return render_template('dashboard.html', appliances=appliances, users=users, current_user=root_admin)

# 家电控制
@app.route('/appliance/<device_id>/control', methods=['POST'])
def control_appliance(device_id):
    action = request.form['action']
    if device_id == "light-001":
        appliance = XiaomiLight("客厅灯", "light-001")
    elif device_id == "washer-123":
        appliance = HaierWasher("洗衣机", "washer-123")
    else:
        flash("未知设备", "error")
        return redirect(url_for('dashboard'))

    if action == "turn_on":
        appliance.turn_on()
    elif action == "turn_off":
        appliance.turn_off()

    flash(f"{appliance.name} {action} 操作已执行", 'success')
    return redirect(url_for('dashboard'))

# 用户管理（注销、升级/降级）
@app.route('/user/<username>/action', methods=['POST'])
def manage_user(username):
    action = request.form['action']
    users = load_db()
    if action == 'delete':
        users = [u for u in users if u.username != username]
        from moduls.User import save_db
        save_db(users)
        flash(f"用户 {username} 已注销", 'success')
    elif action == 'promote':
        from moduls.User import promote_to_family_admin
        promote_to_family_admin(username, root_admin)
        flash(f"用户 {username} 已升级为家庭管理员", 'success')
    elif action == 'demote':
        for u in users:
            if isinstance(u, FamilyAdmin) and u.username == username:
                from moduls.User import User, save_db
                users.remove(u)
                users.append(User(u.username, u.password_hash, u.phone))
                save_db(users)
                flash(f"用户 {username} 已取消管理员权限", 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
