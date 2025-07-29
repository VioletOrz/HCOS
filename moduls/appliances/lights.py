# ========== moduls/appliances/lights.py ==========
from .base import Appliance, DeviceCategory

class Light(Appliance):
    def __init__(self, name, device_id):
        super().__init__(name, device_id, DeviceCategory.VENTILATION_LIGHTING)
        self.brightness = 100
        self.color = (255, 255, 255)

    def set_brightness(self, level: int):
        self.brightness = level
        print(f"[{self.name}] 设置亮度为 {level}%")

    def set_color(self, rgb: tuple):
        self.color = rgb
        print(f"[{self.name}] 设置颜色为 RGB{rgb}")

    def execute_command(self, command: str):
        print(f"[{self.name}] 执行命令: {command}")