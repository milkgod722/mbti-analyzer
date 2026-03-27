# MBTI 人格分析报告

## {{type}} — {{role}}
{{summary}}

---

## 📊 维度分析

| 维度 | 倾向 | 描述 |
|------|------|------|
| **EI** {{EI.percentage}}% | {{EI.primary}} | {{EI.label}} — {{EI.description}} |
| **SN** {{SN.percentage}}% | {{SN.primary}} | {{SN.label}} — {{SN.description}} |
| **TF** {{TF.percentage}}% | {{TF.primary}} | {{TF.label}} — {{TF.description}} |
| **JP** {{JP.percentage}}% | {{JP.primary}} | {{JP.label}} — {{JP.description}} |

{{#if moderate}}
> 💡 你的多个维度呈现中等偏好，说明你具有良好的适应性，可以根据不同情境灵活切换倾向。
{{/if}}

---

## 🔤 四字母解读

- **{{E/I}}** — {{#if (eq letter_profile.EI "E")}}外向型：从外部世界和人际互动中获取能量{{else}}内向型：从独处和内心世界中获取能量{{/if}}
- **{{S/N}}** — {{#if (eq letter_profile.SN "S")}}感觉型：关注具体事实和现实细节{{else}}直觉型：关注可能性、模式和抽象联系{{/if}}
- **{{T/F}}** — {{#if (eq letter_profile.TF "T")}}思考型：依据逻辑和客观标准做决策{{else}}情感型：依据个人价值观和他人感受做决策{{/if}}
- **{{J/P}}** — {{#if (eq letter_profile.JP "J")}}判断型：喜欢有计划、有结构的生活方式{{else}}知觉型：喜欢灵活、开放、随性的生活方式{{/if}}

---

## 💼 职业倾向

> 参考 {{type}} 类型在职业发展上的常见优势与适合领域。
> 详见 `references/mbti_types.md` 中的完整职业对照表。

---

## 🧭 报告使用说明

本报告基于 MBTI® 人格理论框架。MBTI 是一种性格分类工具，而非能力评估。

- **局限性**：不测量智力、技能或专业能力
- **适用场景**：自我认知、个人成长、人际沟通、职业规划
- **注意事项**：性格类型是倾向而非标签；同类型的人也会有差异；你的类型可能随时间和经历发生变化

---

*报告由 AI MBTI 分析引擎生成 | MBTI® 是 Myers-Briggs Company 的注册商标*
