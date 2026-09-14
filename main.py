#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映自动剪辑工具 - 主程序
支持8种语言的字幕生成和切换
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
import asyncio

from video_processor import VideoProcessor
from subtitle_generator import SubtitleGenerator
from language_manager import LanguageManager
from config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class KuaiyingAutoEditor:
    """剪映自动剪辑主类"""
    
    def __init__(self, config_path: str = 'config.json'):
        """初始化编辑器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = Config(config_path)
        self.video_processor = VideoProcessor(self.config)
        self.subtitle_generator = SubtitleGenerator(self.config)
        self.language_manager = LanguageManager(self.config)
        self.tasks = {}
        
    async def process_video(
        self,
        video_file: str,
        input_language: str = 'zh-CN',
        target_languages: Optional[List[str]] = None,
        editing_options: Optional[Dict] = None,
        subtitle_options: Optional[Dict] = None
    ) -> Dict:
        """处理视频文件
        
        Args:
            video_file: 视频文件路径
            input_language: 输入语言
            target_languages: 目标语言列表
            editing_options: 编辑选项
            subtitle_options: 字幕选项
            
        Returns:
            处理结果字典
        """
        try:
            logger.info(f"开始处理视频: {video_file}")
            
            # 验证视频文件
            if not os.path.exists(video_file):
                raise FileNotFoundError(f"视频文件不存在: {video_file}")
            
            # 生成任务ID
            task_id = self._generate_task_id()
            
            # 创建任务记录
            task = {
                'task_id': task_id,
                'video_file': video_file,
                'input_language': input_language,
                'target_languages': target_languages or ['zh-CN', 'en-US'],
                'editing_options': editing_options or self.config.default_editing_options,
                'subtitle_options': subtitle_options or self.config.default_subtitle_options,
                'status': 'processing',
                'progress': 0
            }
            self.tasks[task_id] = task
            
            # 步骤1: 视频分析
            logger.info(f"[{task_id}] 正在分析视频...")
            task['progress'] = 10
            video_info = await self.video_processor.analyze_video(video_file)
            logger.info(f"[{task_id}] 视频信息: {video_info['duration']}s, {video_info['resolution']}")
            
            # 步骤2: 自动剪辑
            logger.info(f"[{task_id}] 正在执行自动剪辑...")
            task['progress'] = 30
            edited_video = await self.video_processor.auto_edit(
                video_file,
                task['editing_options']
            )
            logger.info(f"[{task_id}] 剪辑完成: {edited_video}")
            
            # 步骤3: 语音识别和字幕生成
            logger.info(f"[{task_id}] 正在进行语音识别...")
            task['progress'] = 50
            transcript = await self.subtitle_generator.transcribe(
                edited_video,
                input_language
            )
            logger.info(f"[{task_id}] 识别完成，共 {len(transcript)} 个字幕")
            
            # 步骤4: 多语言字幕生成
            logger.info(f"[{task_id}] 正在生成多语言字幕...")
            task['progress'] = 70
            subtitles = {}
            for lang in task['target_languages']:
                logger.info(f"[{task_id}] 生成 {lang} 字幕...")
                subtitles[lang] = await self.subtitle_generator.generate_subtitle(
                    transcript,
                    input_language,
                    lang,
                    task['subtitle_options']
                )
            
            # 步骤5: 输出视频
            logger.info(f"[{task_id}] 正在输出成品视频...")
            task['progress'] = 90
            output_files = await self.video_processor.create_output_videos(
                edited_video,
                subtitles,
                task['subtitle_options']
            )
            
            # 完成
            task['status'] = 'completed'
            task['progress'] = 100
            task['output_files'] = output_files
            task['subtitles'] = subtitles
            
            logger.info(f"[{task_id}] 处理完成！")
            logger.info(f"[{task_id}] 输出文件: {output_files}")
            
            return {
                'success': True,
                'task_id': task_id,
                'output_files': output_files,
                'subtitles': subtitles,
                'message': '视频处理完成'
            }
            
        except Exception as e:
            logger.error(f"处理失败: {str(e)}", exc_info=True)
            if 'task_id' in locals():
                self.tasks[task_id]['status'] = 'failed'
                self.tasks[task_id]['error'] = str(e)
            return {
                'success': False,
                'error': str(e),
                'message': '视频处理失败'
            }
    
    async def switch_subtitle(self, task_id: str, language: str) -> Dict:
        """切换字幕语言
        
        Args:
            task_id: 任务ID
            language: 目标语言
            
        Returns:
            切换结果
        """
        if task_id not in self.tasks:
            return {'success': False, 'error': '任务ID不存在'}
        
        task = self.tasks[task_id]
        
        if language not in task['subtitles']:
            return {'success': False, 'error': f'语言 {language} 不可用'}
        
        # 更新当前字幕
        task['current_language'] = language
        logger.info(f"[{task_id}] 字幕已切换为: {language}")
        
        return {
            'success': True,
            'task_id': task_id,
            'current_language': language,
            'message': f'已切换为{self.language_manager.get_language_name(language)}字幕'
        }
    
    def get_task_status(self, task_id: str) -> Dict:
        """获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态
        """
        if task_id not in self.tasks:
            return {'success': False, 'error': '任务ID不存在'}
        
        return {
            'success': True,
            'task': self.tasks[task_id]
        }
    
    def _generate_task_id(self) -> str:
        """生成任务ID"""
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        counter = len(self.tasks)
        return f"task_{timestamp}_{counter}"
    
    def list_supported_languages(self) -> List[Dict]:
        """列出支持的语言"""
        return self.language_manager.get_all_languages()


async def main():
    """主函数"""
    editor = KuaiyingAutoEditor()
    
    # 示例: 处理视频
    # result = await editor.process_video(
    #     video_file='/path/to/video.mp4',
    #     input_language='zh-CN',
    #     target_languages=['zh-CN', 'en-US', 'ja-JP', 'ko-KR'],
    #     editing_options={
    #         'remove_silence': True,
    #         'add_transitions': True,
    #         'detect_scenes': True
    #     }
    # )
    # print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 打印支持的语言
    print("支持的语言:")
    for lang in editor.list_supported_languages():
        print(f"  {lang['name']} ({lang['code']})")


if __name__ == '__main__':
    asyncio.run(main())
