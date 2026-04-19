"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    # 這個類別代表一個過濾器（Filter），通常用於在 WebUI 或聊天接口中先檢查
    # 請求內容是否符合條件，再決定是否允許繼續處理。

    class Valves(BaseModel):
        # 系統層級的設定
        priority: int = Field(
            default=0,
            description="Priority level for the filter operations."
        )
        max_turns: int = Field(
            default=8,
            description="Maximum allowable conversation turns for a user."
        )

    class UserValves(BaseModel):
        # 使用者層級的設定
        max_turns: int = Field(
            default=4,
            description="Maximum allowable conversation turns for a user."
        )

    def __init__(self):
        # 初始化 Filter 時建立一個 Valves 物件，保存系統預設值。
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # inlet 是進入點（pre-processing），用來在請求被送到後端之前檢查或修改內容。
        # body: API 請求的原始資料
        # __user__: 代表當前使用者資料，通常包含角色(role)和自訂閥值(valves)
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")

        # 如果使用者角色是 user 或 admin，就套用對話輪數限制
        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])

            # 取系統設定和使用者設定之中較低的限制
            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
            if len(messages) > max_turns:
                # 超過上限時，直接丟出例外中斷處理
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {max_turns}"
                )

        # 經過驗證後，回傳原始請求內容
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # outlet 是離開點（post-processing），在 API 處理完成後可用來檢查或修改回應內容。
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        # 這裡目前沒有更動回應資料，直接回傳原始 body
        return body
