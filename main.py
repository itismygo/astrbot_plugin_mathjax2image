from astrbot.api.event import filter
import astrbot.api.message_components as Comp
from astrbot.api.star import Context, Star, register , StarTools
from astrbot import logger
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import (
    AiocqhttpMessageEvent,
)
from astrbot.core.config.astrbot_config import AstrBotConfig
from .m2i import m2ipy # 假设 m2ipy 是一个函数
import os
from pathlib import Path
import re
import sys
#调用llm生成数学文章并渲染
@register("astrbot_plugin_mathjax2image", "Willixrain", "调用llm生成支持mathjax渲染文章的图片", "1.0.0")
class mj2i(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.system_prompt_template = config.get(
            "system_prompt_template", "写一篇文章，用markdown格式。其中数学公式用mathjax格式。由于要进行markdown转html渲染，\之类的要改成\\,美元符号之间不要有中文字符。不同段用分割线分割。美元符号之间不要有中文字符"
        )
        self.wenzhang = config.get(
            "wenzhang", "用markdown格式"
        )
    

    
        
        
    #llm数学文章渲染
    @filter.command("mj2i")
    async def m2i(self, event: AiocqhttpMessageEvent):

        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        logger.info(f"获取用户指令：{message_str}")
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        message_str = message_str[4:]  # 从第6个字符开始取到最后
        contexts: list[dict] = [ {'role': 'user', 'content': message_str}]
        yield event.plain_result("正在生成")
        llm_respond = await self.get_llm_respond(message_str,contexts)
        llm_respond = await self.filter_llm_thought_tags(llm_respond)
        if llm_respond:
            #生成渲染出来的图片保存在本地
            try:
                opath = m2ipy(llm_respond)
            except Exception as e:
                logger.error(f"调用 m2ipy 渲染文章失败: {e}")
                yield event.plain_result(f"文章渲染失败: {e}")
                return # 渲染失败，提前返回

            try:
                logger.info(opath)

                # 检查文件是否存在，虽然 m2ipy 成功了，但文件创建仍可能失败
                if not opath.exists():
                     logger.error(f"渲染后的图片文件未生成: {opath}")
                     yield event.chain_result([Comp.Text("文章图片文件未生成，请检查日志。")])
                     return # 文件不存在，提前返回

                chain = [
                    Comp.Image.fromFileSystem(str(opath)), # 从本地文件目录发送图片
                ]
                yield event.chain_result(chain)

            except Exception as e:
                logger.error(f"发送文章图片失败: {e}")
                yield event.plain_result(f"发送文章图片失败: {e}")

        else:
            yield event.plain_result("文章生成失败")
            
    
    @filter.command("wz")
    async def wz(self, event: AiocqhttpMessageEvent):

        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        logger.info(f"获取用户指令：{message_str}")
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_str)
        message_str = message_str[2:]  # 从第6个字符开始取到最后
        contexts: list[dict] = [ {'role': 'user', 'content': message_str}]

        
        llm_respond = await self.get_llm_responds(message_str,contexts)
        llm_respond = await self.filter_llm_thought_tags(llm_respond)
        if llm_respond:
            #生成渲染出来的图片保存在本地
            try:
                opath = m2ipy(llm_respond)
            except Exception as e:
                logger.error(f"调用 m2ipy 渲染文章失败: {e}")
                yield event.plain_result(f"文章渲染失败: {e}")
                return # 渲染失败，提前返回

            try:
                # 检查文件是否存在
                if not opath.exists():
                     logger.error(f"渲染后的图片文件未生成: {opath}")
                     yield event.chain_result([Comp.Text("文章图片文件未生成，请检查日志。")])
                     return # 文件不存在，提前返回

                chain = [
                    Comp.Image.fromFileSystem(str(opath)), # 从本地文件目录发送图片
                ]
                yield event.chain_result(chain)

            except Exception as e:
                logger.error(f"发送文章图片失败: {e}")
                yield event.plain_result(f"发送文章图片失败: {e}")

        else:
            yield event.plain_result("文章生成失败")
            
            
    @filter.command("m2i")
    async def m2iz(self, event: AiocqhttpMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        logger.info(f"获取用户指令：{message_str}")
        logger.info(f"待处理的MathJax字符串: {message_content}")

        # 修正：调用 self.ffm 时，将切片后的字符串作为参数
        # 并且 ffm 现在是类的方法，需要 self 参数
        # ffm 只是字符串处理，不太会出错，不加try
        formatted_mathjax_str = await self.ffm(message_content)

        # 调用 m2ipy 函数，这个函数应该接收处理后的字符串
        # 确保 m2ipy 函数存在并能正确处理 formatted_mathjax_str
        try:
            opath = m2ipy(formatted_mathjax_str) # 假设 m2ipy 是一个全局函数或导入的函数
        except Exception as e:
            logger.error(f"调用 m2ipy 转换公式失败: {e}")
            yield event.chain_result([Comp.Text(f"转换公式失败: {e}")])
            return # 转换失败，提前返回

        try:
            # 检查文件是否存在
            if not opath.exists():
                 logger.error(f"公式图片文件未生成: {opath}")
                 yield event.chain_result([Comp.Text("公式图片文件未生成，请检查日志。")])
                 return # 文件不存在，提前返回

            logger.info(f"准备发送图片: {opath}")
            chain = [
                Comp.Image.fromFileSystem(str(opath)), # 从本地文件目录发送图片
            ]
            yield event.chain_result(chain)

        except Exception as e:
            logger.error(f"发送公式图片失败: {e}")
            yield event.chain_result([Comp.Text(f"发送公式图片失败: {e}")])


    # 修正：将 ffm 定义为类的方法，并添加 self 参数
    async def ffm(self, raw_input_string):
        # 这里的逻辑是替换反斜杠，确保在某些环境下不会被误解析
        # MathJax/LaTeX 本身需要双反斜杠来表示一个字面反斜杠（例如 \\newline）
        # 如果你的输入已经是标准的 LaTeX 格式，可能不需要这个替换
        # 但如果用户输入的是单反斜杠，并且需要转义，这个替换是必要的
        # 比如用户输入 \frac，这里会变成 \\frac
        # 如果用户输入 \\frac，这里会变成 \\\\frac
        # 请根据 m2ipy 实际需要的输入格式调整这里的逻辑
        # 假设 m2ipy 需要标准的 LaTeX 字符串
        # 这个替换逻辑可能需要根据实际情况调整，例如只替换单个反斜杠为双反斜杠
        # formatted_string = raw_input_string.replace('\\', '\\\\')
        # 简单的反斜杠转义可能更像这样，但要小心处理已有的双反斜杠
        # 一个更安全的做法是只处理用户输入，如果用户输入的是 \\ 就不动，输入的是 \ 才转义
        # 这里保留你原来的替换逻辑，但要注意其影响
        formatted_string = raw_input_string.replace('\\', '\\\\')

        logger.info(f"ffm 处理后的字符串: {formatted_string}")
        return formatted_string

    #调用llm生成markdown数学文章
    async def get_llm_respond(
        self, message_str:str,contexts: list[dict]
    ) -> str | None:
        """调用llm回复"""
        try:
 
            system_prompt = self.system_prompt_template
            llm_response = await self.context.get_using_provider().text_chat(
                system_prompt=system_prompt,
                prompt="以下是文章围绕的话题",
                contexts=contexts,
            )
            return llm_response.completion_text

        except Exception as e:
            logger.info(system_prompt) # 记录用于LLM调用的system_prompt
            logger.error(f"LLM 调用失败：{e}")
            # 这里不向用户发送消息，因为调用者会检查返回值 None
            return None
            
    async def filter_llm_thought_tags(self,llm_response: str) -> str:
        # 正则表达式模式保持不变
        # r'<think>.*?</think>\s*' 匹配<think>标签、其所有内容、闭合标签以及之后的所有空白
        pattern = r'<think>.*?</think>\s*'
        
        # 使用re.sub执行替换，re.DOTALL确保可以匹配换行符
        cleaned_response = re.sub(pattern, '', llm_response, flags=re.DOTALL)
        
        return cleaned_response
            
            
            
    async def get_llm_responds(
        self, message_str:str,contexts: list[dict]
    ) -> str | None:
        """调用llm回复"""
        try:
 
            system_prompt = self.wenzhang
            llm_responses = await self.context.get_using_provider().text_chat(
                system_prompt=system_prompt,
                prompt="以下是文章围绕的话题",
                contexts=contexts,
            )
            return llm_responses.completion_text

        except Exception as e:
            logger.info(system_prompt) # 记录用于LLM调用的system_prompt
            logger.error(f"LLM 调用失败：{e}")
            # 这里不向用户发送消息，因为调用者会检查返回值 None
            return None
            
    
    
    
        


    


