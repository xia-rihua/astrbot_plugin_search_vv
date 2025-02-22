from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import os
import logging
import random
import glob

logger = logging.getLogger(__name__)

@register("astrbot_plugin_search_vv", "DUAAAA", "这是VV表情搜索插件", "1.0.0", "repo url")
class VVPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.vv_dir = "data/plugins/deepvv/vv"
        os.makedirs(self.vv_dir, exist_ok=True)  # 确保图片目录存在

    @filter.command("vv")
    async def vv_command(self, event: AstrMessageEvent):
        message_str = event.message_str.strip()
        parts = message_str.split(" ", 1)

        # 参数有效性检查
        if len(parts) < 2:
            yield event.make_result().message("请提供图片名称，格式：/vv 图片名")
            return

        keyword = parts[1].strip()
        supported_exts = ['.jpg', '.png', '.webp', '.jpeg']
        matched_files = []

        # 使用 glob 模块进行模糊匹配
        for ext in supported_exts:
            pattern = os.path.join(self.vv_dir, f"*{keyword}*{ext}")
            matched_files.extend(glob.glob(pattern))

        # 处理查找结果
        if matched_files:
            selected = random.choice(matched_files)
            # 发送图片文件
            yield event.chain_result([Image(selected)])
        else:
            yield event.make_result().message(f"未找到相关图片：{keyword}")
