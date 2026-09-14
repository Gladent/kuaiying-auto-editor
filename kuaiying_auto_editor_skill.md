# 剪映自动剪辑 Skill

## 概述
这是一个为豆包AI设计的skill，用于自动化视频剪辑和多语言字幕生成/切换。支持中文及7种常用国际语言。

## 功能清单

### 核心功能
1. **视频分析与场景检测**
   - 自动检测场景切换点
   - 识别静音段落
   - 检测镜头抖动和模糊
   - 分析音频节奏

2. **智能剪辑**
   - 自动移除静音/无效内容
   - 智能添加转场效果
   - 自动调整视频速度以匹配音乐
   - 场景自动分割

3. **字幕处理（8种语言支持）**
   - 中文 (Chinese Simplified/Traditional)
   - 英文 (English)
   - 日文 (Japanese)
   - 韩文 (Korean)
   - 法文 (French)
   - 德文 (German)
   - 西班牙文 (Spanish)
   - 俄文 (Russian)
   - 支持实时切换和批量导出

4. **音频处理**
   - 背景音乐自动匹配
   - 音量标准化
   - 音频降噪

## 使用场景

### 场景1：快速处理直播回放
**用户输入**：直播视频文件
**Skill流程**：
1. 分析直播视频
2. 自动移除卡顿和无效段落
3. 添加开场和结尾
4. 生成中文字幕并支持8国语言切换
5. 输出成品视频

### 场景2：批量字幕翻译切换
**用户输入**：已字幕化视频 + 目标语言列表
**Skill流程**：
1. 识别现有字幕
2. 翻译为指定语言
3. 生成多语言版本
4. 供用户选择切换

### 场景3：内容创作加速
**用户输入**：原始素材文件夹 + 创作主题
**Skill流程**：
1. 整理素材顺序
2. 自动剪辑并添加效果
3. 生成多语言字幕
4. 输出不同规格版本

## 语言配置

```json
{
  "languages": {
    "zh-CN": {
      "name": "简体中文",
      "code": "zh-CN",
      "priority": 1
    },
    "zh-TW": {
      "name": "繁體中文",
      "code": "zh-TW",
      "priority": 2
    },
    "en-US": {
      "name": "English",
      "code": "en-US",
      "priority": 3
    },
    "ja-JP": {
      "name": "日本語",
      "code": "ja-JP",
      "priority": 4
    },
    "ko-KR": {
      "name": "한국어",
      "code": "ko-KR",
      "priority": 5
    },
    "fr-FR": {
      "name": "Français",
      "code": "fr-FR",
      "priority": 6
    },
    "de-DE": {
      "name": "Deutsch",
      "code": "de-DE",
      "priority": 7
    },
    "es-ES": {
      "name": "Español",
      "code": "es-ES",
      "priority": 8
    },
    "ru-RU": {
      "name": "Русский",
      "code": "ru-RU",
      "priority": 9
    }
  }
}
```

## API 接口规范

### 1. 创建剪辑任务
```
POST /api/v1/editing-tasks
Content-Type: application/json

{
  "video_file": "path/to/video.mp4",
  "task_type": "auto_edit|subtitle_generation|language_switch",
  "input_language": "zh-CN",
  "target_languages": ["en-US", "ja-JP", "ko-KR"],
  "editing_options": {
    "remove_silence": true,
    "add_transitions": true,
    "detect_scenes": true,
    "min_scene_duration": 2.0,
    "silence_threshold": -40
  },
  "subtitle_options": {
    "style": "default",
    "font_size": 24,
    "position": "bottom"
  }
}

Response:
{
  "task_id": "task_20250914_001",
  "status": "processing",
  "created_at": "2025-09-14T10:30:00Z",
  "estimated_completion": "2025-09-14T11:30:00Z"
}
```

### 2. 查询任务状态
```
GET /api/v1/editing-tasks/{task_id}

Response:
{
  "task_id": "task_20250914_001",
  "status": "completed",
  "progress": 100,
  "output_files": {
    "zh-CN": "output/video_zh_CN.mp4",
    "en-US": "output/video_en_US.mp4",
    "ja-JP": "output/video_ja_JP.mp4"
  },
  "duration": 3600,
  "completed_at": "2025-09-14T11:30:00Z"
}
```

### 3. 字幕切换
```
POST /api/v1/editing-tasks/{task_id}/switch-subtitle
Content-Type: application/json

{
  "language": "en-US"
}

Response:
{
  "task_id": "task_20250914_001",
  "current_language": "en-US",
  "switched_at": "2025-09-14T11:35:00Z"
}
```

## 参数说明

### editing_options
| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| remove_silence | boolean | 是否移除静音段落 | true |
| add_transitions | boolean | 是否添加转场效果 | true |
| detect_scenes | boolean | 是否检测场景 | true |
| min_scene_duration | float | 最小场景时长(秒) | 1.0 |
| silence_threshold | float | 静音阈值(dB) | -40 |
| auto_speed_adjust | boolean | 自动调整速度 | false |

### subtitle_options
| 参数 | 类型 | 说明 | 默认值 |
|------|------|------|--------|
| style | string | 字幕样式 | "default" |
| font_size | int | 字体大小 | 24 |
| position | string | 字幕位置 | "bottom" |
| background | boolean | 是否有背景 | true |
| opacity | float | 透明度(0-1) | 0.8 |

## 工作流程图

```
输入视频
  ↓
[视频分析] → 场景检测 → 静音识别 → 质量评估
  ↓
[自动剪辑] → 移除冗余 → 添加转场 → 调整速度
  ↓
[语音识别] → 生成字幕 → 翻译处理
  ↓
[字幕生成] 
  ├→ 中文字幕
  ├→ 英文字幕
  ├→ 日文字幕
  ├→ 韩文字幕
  ├→ 法文字幕
  ├→ 德文字幕
  ├→ 西班牙文字幕
  └→ 俄文字幕
  ↓
[动态切换] → 用户选择语言 → 实时切换显示
  ↓
输出成品视频
```

## 错误处理

| 错误码 | 描述 | 解决方案 |
|--------|------|--------|
| 4001 | 视频格式不支持 | 使用支持的格式: MP4, MKV, MOV |
| 4002 | 文件过大 | 压缩视频或分割处理 |
| 4003 | 语言不支持 | 从支持的8种语言中选择 |
| 5001 | 处理超时 | 检查服务器状态或重试 |
| 5002 | 内存不足 | 关闭其他应用或使用更大的服务器 |

## 豆包执行指令

当你（豆包）接收到用户的这个skill时，按以下步骤执行：

1. **解析用户需求**
   - 提取视频文件路径
   - 确认目标语言列表
   - 获取编辑偏好设置

2. **调用编辑引擎**
   - 初始化视频处理模块
   - 执行场景检测和分析
   - 应用自动剪辑规则

3. **生成多语言字幕**
   - 进行语音识别
   - 翻译至各种语言
   - 同步字幕时间轴

4. **输出与验证**
   - 生成预览版本
   - 验证质量
   - 提供下载链接

5. **用户交互**
   - 提供字幕切换选项
   - 实时预览不同语言版本
   - 支持参数微调和重新处理

## 示例命令

```
豆包，请帮我处理这个视频文件：/videos/livestream.mp4
需求：
1. 自动剪辑，移除静音段落
2. 生成中文字幕，并支持英文、日文、韩文切换
3. 添加转场效果
4. 输出为高清版本

我的输入语言是中文。
```

## 支持的视频格式

- MP4, MKV, MOV, AVI, FLV, WMV
- 分辨率: 720p 至 4K
- 帧率: 24fps ~ 60fps

## 字幕输出格式

- SRT (SubRip)
- VTT (WebVTT)
- ASS (Advanced SubStation Alpha)
- 内嵌字幕 (硬字幕)
