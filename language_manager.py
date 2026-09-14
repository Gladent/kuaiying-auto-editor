# -*- coding: utf-8 -*-
"""
语言管理模块
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class LanguageManager:
    """语言管理类"""
    
    def __init__(self, config):
        """初始化语言管理器
        
        Args:
            config: 配置对象
        """
        self.config = config
        self.languages = config.get('languages', {})
    
    def get_language_name(self, language_code: str) -> str:
        """获取语言名称
        
        Args:
            language_code: 语言代码
            
        Returns:
            语言名称
        """
        if language_code in self.languages:
            return self.languages[language_code]['name']
        return language_code
    
    def is_supported(self, language_code: str) -> bool:
        """检查语言是否支持
        
        Args:
            language_code: 语言代码
            
        Returns:
            是否支持
        """
        return language_code in self.languages
    
    def get_all_languages(self) -> List[Dict]:
        """获取所有支持的语言
        
        Returns:
            语言列表
        """
        languages = []
        for code, info in self.languages.items():
            languages.append({
                'code': code,
                'name': info['name'],
                'priority': info.get('priority', 999)
            })
        # 按优先级排序
        languages.sort(key=lambda x: x['priority'])
        return languages
    
    def get_language_by_priority(self, priority: int) -> Optional[Dict]:
        """根据优先级获取语言
        
        Args:
            priority: 优先级
            
        Returns:
            语言信息
        """
        for code, info in self.languages.items():
            if info.get('priority') == priority:
                return {'code': code, 'name': info['name']}
        return None
    
    def validate_language_list(self, language_codes: List[str]) -> List[str]:
        """验证语言列表，移除不支持的语言
        
        Args:
            language_codes: 语言代码列表
            
        Returns:
            有效的语言代码列表
        """
        valid_languages = []
        for code in language_codes:
            if self.is_supported(code):
                valid_languages.append(code)
            else:
                logger.warning(f"不支持的语言: {code}")
        return valid_languages
