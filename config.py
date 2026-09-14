# -*- coding: utf-8 -*-
"""
配置文件管理
"""

import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """配置管理类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        'api': {
            'host': '0.0.0.0',
            'port': 8000,
            'debug': False
        },
        'video': {
            'supported_formats': ['mp4', 'mkv', 'mov', 'avi', 'flv', 'wmv'],
            'min_resolution': '720p',
            'max_resolution': '4k',
            'fps_range': [24, 60]
        },
        'languages': {
            'zh-CN': {'name': '简体中文', 'priority': 1},
            'zh-TW': {'name': '繁體中文', 'priority': 2},
            'en-US': {'name': 'English', 'priority': 3},
            'ja-JP': {'name': '日本語', 'priority': 4},
            'ko-KR': {'name': '한국어', 'priority': 5},
            'fr-FR': {'name': 'Français', 'priority': 6},
            'de-DE': {'name': 'Deutsch', 'priority': 7},
            'es-ES': {'name': 'Español', 'priority': 8},
            'ru-RU': {'name': 'Русский', 'priority': 9}
        },
        'editing': {
            'default_options': {
                'remove_silence': True,
                'add_transitions': True,
                'detect_scenes': True,
                'min_scene_duration': 1.0,
                'silence_threshold': -40,
                'auto_speed_adjust': False
            },
            'transition_types': ['fade', 'slide', 'zoom', 'cross_fade']
        },
        'subtitles': {
            'default_options': {
                'style': 'default',
                'font_size': 24,
                'position': 'bottom',
                'background': True,
                'opacity': 0.8
            },
            'output_formats': ['srt', 'vtt', 'ass'],
            'embedded': True
        },
        'processing': {
            'max_workers': 4,
            'timeout': 3600,
            'temp_dir': './temp',
            'output_dir': './output'
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }
    
    def __init__(self, config_path: str = 'config.json'):
        """初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self.DEFAULT_CONFIG.copy()
        
        # 从文件加载配置
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                self.config.update(user_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键（支持点符号）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值
        
        Args:
            key: 配置键（支持点符号）
            value: 配置值
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: str = None) -> None:
        """保存配置到文件
        
        Args:
            path: 保存路径
        """
        save_path = Path(path or self.config_path)
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    @property
    def default_editing_options(self) -> Dict:
        """获取默认编辑选项"""
        return self.get('editing.default_options')
    
    @property
    def default_subtitle_options(self) -> Dict:
        """获取默认字幕选项"""
        return self.get('subtitles.default_options')
    
    @property
    def supported_languages(self) -> Dict:
        """获取支持的语言"""
        return self.get('languages')
    
    @property
    def output_dir(self) -> str:
        """获取输出目录"""
        return self.get('processing.output_dir')
    
    @property
    def temp_dir(self) -> str:
        """获取临时目录"""
        return self.get('processing.temp_dir')
