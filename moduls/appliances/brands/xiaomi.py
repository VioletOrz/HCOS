# ========== moduls/appliances/brands/xiaomi.py ==========
from moduls.appliances.lights import Light

class XiaomiLight(Light):
    def execute_command(self, command: str):
        print(f"[小米灯 {self.name}] 通过米家协议执行命令: {command}")

