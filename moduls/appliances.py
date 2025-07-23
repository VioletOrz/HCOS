# ========== main.py 示例使用 ==========
from appliances.brands.xiaomi import XiaomiLight
from appliances.brands.haier import HaierWasher

if __name__ == '__main__':
    dev1 = XiaomiLight("客厅吊灯", "light-001")
    dev2 = HaierWasher("阳台洗衣机", "washer-123")

    dev1.turn_on()
    dev1.set_brightness(70)
    dev1.set_color((200, 180, 255))
    dev1.execute_command("schedule_on 18:00")

    print("\n")
    dev2.turn_on()
    dev2.start_wash("快洗15分钟")
    dev2.execute_command("pause")

    print("\n设备状态：")
    print(dev1.get_status())
    print(dev2.get_status())