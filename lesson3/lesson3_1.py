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
        self.user_input = ""

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # inlet 是進入點（pre-processing），用來在請求被送到後端之前檢查或修改內容。
        # body: API 請求的原始資料
        # __user__: 代表當前使用者資料，通常包含角色(role)和自訂閥值(valves)
        
        # print(body.get("messages", [])[-1].get("content", "") if body.get("messages") else "")
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # outlet 是離開點（post-processing），在 API 處理完成後可用來檢查或修改回應內容。
        messages = body.get("messages")
        user_input = ""
        assistant_output = ""

        # for msg in reversed(messages):
        #     if msg.get("role") == "user" and not user_input:
        #         user_input = msg.get("content", "")
        #     elif msg.get("role") == "assistant" and not assistant_output:
        #         assistant_output = msg.get("content", "")
        #     if user_input and assistant_output:
        #         break
        
        # print(f"使用者輸入: {user_input}")
        # print(f"模型輸出: {assistant_output}")

        # for msg in messages:
        #     if msg.get("role") == "assistant":
        #         msg["content"] = "Hello World !!"
 
        for msg in messages:
            if msg.get("role") == "assistant":
                msg["content"] = msg.get("content", "") + "\n\n天天開心"
        
        return body
