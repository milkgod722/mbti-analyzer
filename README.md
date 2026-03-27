# MBTI Analyzer Skill

MBTI 人格测试分析与报告生成 Skill，支持 OpenClaw 等 Agent。

## 功能

- **40 题测试答案分析**：输入 40 题评分（1-5 分），自动推断 MBTI 类型并生成报告
- **直接类型分析**：直接指定 4 字 MBTI 类型（如 `INTJ`、`ENFP`），生成完整报告
- **多语言支持**：自动识别输入语言，中文/英文报告
- **结构化输出**：维度百分比、角色定位、职业倾向、适应性说明

## 目录结构

```
mbti-analyzer/
├── SKILL.md                      # Skill 入口说明
├── scripts/
│   └── analyze_mbti.py          # 核心分析引擎
├── references/
│   └── mbti_types.md            # 16 型人格详解 + 职业倾向表
└── assets/
    └── report_template.md       # 中文报告模板
```

## 使用方法

### 方式一：40 题答案分析

```json
{
  "answers": [4, 5, 3, 2, 1, 4, 5, 3, 2, 4, 3, 4, 5, 2, 1, 3, 4, 5, 2, 3, 4, 3, 2, 5, 4, 3, 4, 2, 1, 5, 3, 4, 5, 2, 4, 3, 2, 4, 5, 1]
}
```

### 方式二：直接指定类型

```json
{"type": "INTJ"}
```

### 运行脚本

```bash
python3 scripts/analyze_mbti.py <<< '{"type": "INTJ"}'
```

## 输出示例

```json
{
  "type": "INTJ",
  "role": "Architect",
  "summary": "Strategic thinkers with a drive for self-improvement",
  "dimensions": {
    "EI": { "percentage": 10, "primary": "I", "moderate": false, "description": "10% I" },
    "SN": { "percentage": 10, "primary": "N", "moderate": false, "description": "10% N" },
    "TF": { "percentage": 90, "primary": "T", "moderate": false, "description": "90% T" },
    "JP": { "percentage": 90, "primary": "J", "moderate": false, "description": "90% J" }
  }
}
```

## 支持的 MBTI 类型

INTJ · INTP · ENTJ · ENTP · INFJ · INFP · ENFJ · ENFP ·  
ISTJ · ISFJ · ESTJ · ESFJ · ISTP · ISFP · ESTP · ESFP

## 安装

将此目录作为 skill 加载到 OpenClaw：

```bash
# 通过 ClawHub 安装
clawhub install mbti-analyzer --dir ./skills

# 或将文件放入 OpenClaw workspace skills 目录
cp -r mbti-analyzer /path/to/workspace/skills/
```

## 技术细节

- **分析维度**：EI（外向/内向）、SN（感觉/直觉）、TF（思考/情感）、JP（判断/知觉）
- **评分规则**：每维度取前 10 题，选项 >3 记为该侧偏好，计算百分比
- **中度偏好**：40-60% 区间为中等偏好，报告将注明适应性说明
- **依赖**：Python 3，无第三方依赖

## License

MIT
