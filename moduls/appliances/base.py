# 文件结构建议（HKFC OS 家电系统）：
# hkfc_os/
# ├── moduls/
# │   ├── appliances/
# │   │   ├── __init__.py
# │   │   ├── base.py            # 顶层父类 Appliance
# │   │   ├── lights.py          # Light 设备功能类
# │   │   ├── washers.py         # 洗衣机类
# │   │   └── brands/
# │   │       ├── __init__.py
# │   │       ├── xiaomi.py      # 小米品牌设备
# │   │       ├── haier.py       # 海尔品牌设备
# │   │       └── ...            # 更多品牌
# │
# └─ static/
#      ├─ style.css
#      ├─ js/
#      │    └─ main.js
#      └─ images/
#           ├─ light.png
#           └─ washer.png

# ========== moduls/appliances/base.py ==========
from abc import ABC, abstractmethod
from enum import Enum

class DeviceCategory(Enum):
    VENTILATION_LIGHTING = "Ventilation and Lighting"
    KITCHEN = "Kitchen Appliance"
    ENTERTAINMENT = "Entertainment Device"
    LIVING = "Living Appliance"
    OTHER = "Other"

class Appliance(ABC):
    def __init__(self, name: str, device_id: str, category: DeviceCategory):
        self.name = name
        self.device_id = device_id
        self.category = category
        self.online = True
        self.power_on = False

    def turn_on(self):
        self.power_on = True
        print(f"[{self.name}] 已开机")

    def turn_off(self):
        self.power_on = False
        print(f"[{self.name}] 已关机")

    def get_status(self):
        return {
            "device": self.name,
            "power": self.power_on,
            "online": self.online,
            "category": self.category.value
        }

    @abstractmethod
    def execute_command(self, command: str):
        pass





