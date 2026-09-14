# 剪映自动剪辑工具 (Kuaiying Auto Editor)

一个强大的视频自动剪辑和多语言字幕生成工具，支持8种常用语言的字幕切换。

## 功能特性

### 🎬 核心功能
- **自动场景检测** - 智能识别视频中的场景切换点
- **智能静音移除** - 自动删除无声或噪音段落
- **转场效果添加** - 自动为场景变化添加过渡效果
- **视频加速匹配** - 根据背景音乐自动调整播放速度

### 📝 字幕功能
- **语音识别** - 自动提取视频中的语音内容
- **8国语言支持**：
  - 中文（简体和繁体）
  - 英文
  - 日文
  - 韩文
  - 法文
  - 德文
  - 西班牙文
  - 俄文
- **实时字幕切换** - 支持视频播放过程中动态切换字幕语言
- **多格式导出** - 支持 SRT、VTT、ASS 等格式

### 🎵 音频处理
- **背景音乐匹配** - 自动选择与视频内容匹配的背景音乐
- **音量标准化** - 统一视频中的音频电平
- **音频降噪** - 清除环境噪音提高清晰度

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```python
import asyncio
from main import KuaiyingAutoEditor

async def main():
    editor = KuaiyingAutoEditor()
    
    # 处理视频
    result = await editor.process_video(
        video_file='/path/to/video.mp4',
        input_language='zh-CN',
        target_languages=['zh-CN', 'en-US', 'ja-JP', 'ko-KR'],
        editing_options={
            'remove_silence': True,
            'add_transitions': True,
            'detect_scenes': True
        }
    )
    
    print(result)
    
    # 切换字幕语言
    switch_result = await editor.switch_subtitle(result['task_id'], 'en-US')
    print(switch_result)

if __name__ == '__main__':
    asyncio.run(main())
```

## 项目结构

```
kuaiying-auto-editor/
├── main.py                      # 主程序入口
├── config.py                    # 配置管理
├── video_processor.py           # 视频处理模块
├── subtitle_generator.py        # 字幕生成模块
├── language_manager.py          # 语言管理模块
├── config.json                  # 配置文件
├── requirements.txt             # 依赖列表
├── README.md                    # 说明文档
├── kuaiying_auto_editor_skill.md # Skill规范
└── tests/                       # 测试目录
```

## API 接口

### 创建编辑任务

```bash
curl -X POST http://localhost:8000/api/v1/editing-tasks \
  -H "Content-Type: application/json" \
  -d '{
    "video_file": "/path/to/video.mp4",
    "input_language": "zh-CN",
    "target_languages": ["en-US", "ja-JP"],
    "editing_options": {
      "remove_silence": true,
      "add_transitions": true
    }
  }'
```

### 查询任务状态

```bash
curl http://localhost:8000/api/v1/editing-tasks/task_20250914_001
```

### 切换字幕

```bash
curl -X POST http://localhost:8000/api/v1/editing-tasks/task_20250914_001/switch-subtitle \
  -H "Content-Type: application/json" \
  -d '{"language": "en-US"}'
```

## 配置说明

### 编辑选项

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `remove_silence` | bool | 移除静音段落 | true |
| `add_transitions` | bool | 添加转场效果 | true |
| `detect_scenes` | bool | 检测场景 | true |
| `min_scene_duration` | float | 最小场景时长(秒) | 1.0 |
| `silence_threshold` | float | 静音阈值(dB) | -40 |
| `auto_speed_adjust` | bool | 自动调速 | false |

### 字幕选项

| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| `style` | string | 字幕样式 | "default" |
| `font_size` | int | 字体大小 | 24 |
| `position` | string | 位置 | "bottom" |
| `background` | bool | 背景 | true |
| `opacity` | float | 透明度 | 0.8 |

## 支持的视频格式

- MP4, MKV, MOV, AVI, FLV, WMV
- 分辨率: 720p ~ 4K
- 帧率: 24fps ~ 60fps

## 错误处理

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| 4001 | 视频格式不支持 | 转换为支持的格式 |
| 4002 | 文件过大 | 压缩视频或分割处理 |
| 4003 | 语言不支持 | 从支持的8种语言中选择 |
| 5001 | 处理超时 | 检查服务器或重试 |
| 5002 | 内存不足 | 使用更大的服务器 |

## 技术栈

- **Python 3.8+**
- **OpenCV** - 视频处理
- **MoviePy** - 视频编辑
- **SpeechRecognition** - 语音识别
- **Google Translate API** - 多语言翻译
- **FastAPI** - Web框架（可选）

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- GitHub: [@Gladent](https://github.com/Gladent)
- Email: support@kuaiying-editor.com

---

**注意**: 这是一个演示项目。某些功能（如语音识别、翻译）的完整实现需要集成第三方API。
