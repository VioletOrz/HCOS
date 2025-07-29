# ========== moduls/appliances/brands/haier.py ==========
from moduls.appliances.washers import WashingMachine

class HaierWasher(WashingMachine):
    def start_wash(self, mode: str):
        print(f"[海尔洗衣机 {self.name}] 云指令启动模式：{mode}")

    def execute_command(self, command: str):
        print(f"[海尔洗衣机 {self.name}] 与服务器同步执行: {command}")
