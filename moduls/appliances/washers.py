# ========== appliances/washers.py ==========
from .base import Appliance, DeviceCategory

class WashingMachine(Appliance):
    def __init__(self, name, device_id):
        super().__init__(name, device_id, DeviceCategory.LIVING)
        self.current_mode = None

    def start_wash(self, mode: str):
        self.current_mode = mode
        print(f"[{self.name}] 开始洗衣，模式：{mode}")

    def pause(self):
        print(f"[{self.name}] 暂停洗衣")

    def execute_command(self, command: str):
        print(f"[{self.name}] 执行命令: {command}")
