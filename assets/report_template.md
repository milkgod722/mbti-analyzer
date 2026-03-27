# MBTI 人格分析报告

## {{type}} — {{role}}
{{summary}}

---

## 📊 维度分析

| 维度 | 倾向 | 强度 | 描述 |
|------|------|------|------|
| **EI** {{EI.percentage}}% | {{EI.primary}} | {{EI.strength_description}} | {{EI.label}} — {{EI.description}} |
| **SN** {{SN.percentage}}% | {{SN.primary}} | {{SN.strength_description}} | {{SN.label}} — {{SN.description}} |
| **TF** {{TF.percentage}}% | {{TF.primary}} | {{TF.strength_description}} | {{TF.label}} — {{TF.description}} |
| **JP** {{JP.percentage}}% | {{JP.primary}} | {{JP.strength_description}} | {{JP.label}} — {{JP.description}} |

{{#if has_moderate_dimensions}}
> 💡 {{adaptability_note}}
{{/if}}

{{#each dimensions}}
{{#if balance_note}}
> ⚖️ **{{@key}}**: {{balance_note}}
{{/if}}
{{/each}}

---

## 🔤 四字母解读

- **{{E/I}}** — {{#if (eq letter_profile.EI "E")}}外向型：从外部世界和人际互动中获取能量{{else}}内向型：从独处和内心世界中获取能量{{/if}}
- **{{S/N}}** — {{#if (eq letter_profile.SN "S")}}感觉型：关注具体事实和现实细节{{else}}直觉型：关注可能性、模式和抽象联系{{/if}}
- **{{T/F}}** — {{#if (eq letter_profile.TF "T")}}思考型：依据逻辑和客观标准做决策{{else}}情感型：依据个人价值观和他人感受做决策{{/if}}
- **{{J/P}}** — {{#if (eq letter_profile.JP "J")}}判断型：喜欢有计划、有结构的生活方式{{else}}知觉型：喜欢灵活、开放、随性的生活方式{{/if}}

---

## 🧠 认知功能分析

你的认知功能栈决定了你处理信息和做决策的独特方式：

| 位置 | 功能 | 名称 | 说明 |
|------|------|------|------|
{{#each cognitive_functions.functions}}
| **{{position}}** | {{code}} | {{name}} | {{description}} |
{{/each}}

### 功能栈详解

1. **主导功能 ({{cognitive_functions.stack.[0]}})**
   - 这是你最强大、最自然的心理过程
   - 你在压力下会本能依赖这个功能
   - 通常在童年时期就开始发展

2. **辅助功能 ({{cognitive_functions.stack.[1]}})**
   - 支持和平衡你的主导功能
   - 提供不同的视角和能力
   - 青少年时期逐渐成熟

3. **第三功能 ({{cognitive_functions.stack.[2]}})**
   - 较弱但在成年后逐渐发展
   - 可能在休闲或放松时显现
   - 是个人成长的中期目标

4. **劣势功能 ({{cognitive_functions.stack.[3]}})**
   - 你最不成熟的心理过程
   - 压力大时可能以负面方式表现
   - 发展此功能是长期成长的关键

{{#if cognitive_functions.growth_area}}
### 🌱 成长建议

{{cognitive_functions.growth_area.advice}}
{{/if}}

---

## 💼 职业倾向

> 参考 {{type}} 类型在职业发展上的常见优势与适合领域。
> 详见 `references/mbti_types.md` 中的完整职业对照表。

### 你的职业优势
{{#if (eq letter_profile.TF "T")}}
- 逻辑分析能力强，善于客观评估
- 决策果断，不易受情绪影响
{{else}}
- 善于理解他人需求，人际敏感度高
- 能够在团队中创造和谐氛围
{{/if}}

{{#if (eq letter_profile.JP "J")}}
- 组织规划能力出色
- 执行力强，注重成果交付
{{else}}
- 适应性强，应变能力好
- 善于发现新机会和可能性
{{/if}}

---

## 💬 沟通风格

### 你的沟通特点

{{#if (eq letter_profile.EI "E")}}
**外向型沟通者**
- 喜欢通过交谈来思考和处理信息
- 善于群体讨论和头脑风暴
- 可能需要注意给内向者留出思考空间
{{else}}
**内向型沟通者**
- 倾向于先思考后发言
- 更喜欢一对一深度交流
- 可能需要主动表达观点以免被忽视
{{/if}}

{{#if (eq letter_profile.SN "S")}}
**具体型表达**
- 偏好用实例和数据支持观点
- 注重细节和实际应用
- 与直觉型沟通时可尝试讨论更多可能性
{{else}}
**概念型表达**
- 善于描述愿景和大方向
- 喜欢探讨理论和创意
- 与感觉型沟通时应提供更多具体例子
{{/if}}

### 提升沟通效果的建议

1. **了解对方类型**：不同类型有不同的沟通偏好
2. **调整你的风格**：根据对方需求灵活调整
3. **倾听与确认**：确保你理解了对方的真正意思
4. **尊重差异**：不同不代表错误

---

## 💕 关系与相处

### 你在关系中的模式

{{#if (eq letter_profile.TF "T")}}
- 用行动和解决问题来表达关心
- 可能需要更多地用语言表达情感
- 重视伴侣/朋友的能力和独立性
{{else}}
- 善于感知和回应他人的情感需求
- 重视关系中的情感连接
- 可能需要学会适度设立界限
{{/if}}

### 最佳伴侣类型参考

> 详见 `references/mbti_types.md` 中的关系兼容性矩阵。

**关系中的成长点：**
- 发展你的劣势功能可以帮助你更好地理解不同类型的人
- 与互补类型的相处是个人成长的机会

---

## 🚀 个人成长建议

### 发挥你的优势

{{#if (eq letter_profile.SN "N")}}
- 利用你的创意和洞察力解决复杂问题
- 在需要战略思维的领域发光发热
{{else}}
- 发挥你对细节的敏感和实践能力
- 在需要可靠执行的领域展现价值
{{/if}}

### 需要注意的盲点

{{#if (eq letter_profile.JP "J")}}
- 过于追求计划和控制可能错失机会
- 学会接受适度的不确定性
{{else}}
- 过于开放可能导致缺乏执行力
- 培养适当的结构和时间管理能力
{{/if}}

### 成长路径

1. **短期（1-6个月）**：觉察你的偏好模式，了解它们如何影响日常
2. **中期（6-18个月）**：有意识地在舒适区外练习，发展第三功能
3. **长期（2年+）**：逐步整合劣势功能，成为更完整的自己

---

## 🧭 报告使用说明

本报告基于 MBTI® 人格理论框架。MBTI 是一种性格分类工具，而非能力评估。

- **局限性**：不测量智力、技能或专业能力
- **适用场景**：自我认知、个人成长、人际沟通、职业规划
- **注意事项**：性格类型是倾向而非标签；同类型的人也会有差异；你的类型可能随时间和经历发生变化

### 进一步探索

- 阅读 `references/mbti_types.md` 了解所有类型的详细信息
- 了解认知功能理论可以帮助你更深入理解自己
- 与不同类型的人交流，拓展你的视角

---

*报告由 AI MBTI 分析引擎生成 | MBTI® 是 Myers-Briggs Company 的注册商标*
