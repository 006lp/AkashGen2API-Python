import json
import time
import aiohttp
import asyncio
import re
from typing import Dict, Any, Optional
from app.utils.config import Config

class AkashService:
    BASE_URL = "https://chat.akash.network/api"
    
    @staticmethod
    async def generate_image(prompt: str) -> Dict[str, Any]:
        """调用Akash API生成图像"""
        chat_url = f"{AkashService.BASE_URL}/chat"
        
        # 准备请求头
        headers = {
            "authority": "chat.akash.network",
            "method": "POST",
            "path": "/api/chat",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "cookie": f"session_token={Config.SESSION_TOKEN};",
            "dnt": "1",
            "origin": "https://chat.akash.network",
            "pragma": "no-cache",
            "referer": "https://chat.akash.network/",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
        }
        
        # 准备请求体
        payload = {
            "id": f"req_{int(time.time())}",
            "messages": [{"role": "user", "content": prompt}],
            "model": "AkashGen",
            "system": "",
            "temperature": 0.85,
            "topP": 1
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(chat_url, headers=headers, json=payload) as response:
                if response.status != 200:
                    return {"error": f"Error from Akash API: {response.status}"}
                
                # 解析响应
                text = await response.text()
                lines = text.strip().split('\n')
                
                # 提取jobId
                job_id = None
                for line in lines:
                    if line.startswith('0:'):
                        match = re.search(r"jobId='([^']+)'", line)
                        if match:
                            job_id = match.group(1)
                            break
                
                if not job_id:
                    return {"error": "Failed to extract jobId from response"}
                
                # 提取prompt
                prompt_match = re.search(r"prompt='([^']+)'", text)
                prompt_text = prompt_match.group(1) if prompt_match else prompt
                
                # 提取negative prompt
                negative_match = re.search(r"negative='([^']+)'", text)
                negative_text = negative_match.group(1) if negative_match else ""
                
                # 等待图像生成完成
                image_data = await AkashService.wait_for_image(job_id)
                
                return {
                    "job_id": job_id,
                    "prompt": prompt_text,
                    "negative": negative_text,
                    "image_data": image_data.get("result", ""),
                    "status": image_data.get("status", "error"),
                    "worker_info": {
                        "name": image_data.get("worker_name", ""),
                        "city": image_data.get("worker_city", ""),
                        "country": image_data.get("worker_country", ""),
                        "gpu": image_data.get("worker_gpu", "")
                    }
                }
    
    @staticmethod
    async def wait_for_image(job_id: str) -> Dict[str, Any]:
        """等待图像生成完成并获取结果"""
        status_url = f"{AkashService.BASE_URL}/image-status?ids={job_id}"
        
        headers = {
            "authority": "chat.akash.network",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "cookie": f"session_token={Config.SESSION_TOKEN};",
            "dnt": "1",
            "referer": "https://chat.akash.network/",
            "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Microsoft Edge\";v=\"133\", \"Chromium\";v=\"133\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
        }
        
        max_retries = 60  # 最多等待60秒
        
        async with aiohttp.ClientSession() as session:
            for _ in range(max_retries):
                async with session.get(status_url, headers=headers) as response:
                    if response.status != 200:
                        await asyncio.sleep(1)
                        continue
                    
                    data = await response.json()
                    if not data or len(data) == 0:
                        await asyncio.sleep(1)
                        continue
                    
                    status = data[0].get("status", "")
                    if status == "completed":
                        return data[0]
                    
                    if status == "error":
                        return {"status": "error", "result": ""}
                    
                    # 如果还在处理中，等待后再试
                    await asyncio.sleep(1)
            
            return {"status": "timeout", "result": ""}
