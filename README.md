# 语文全流程教学辅助系统 (Yuwen)

面向高中语文教师全流程教学的辅助系统：知识/资料库（教材解析 144 源包、81 张知识点卡、28 份单元图谱、17 年高考真题语料）、方法论/理念库（四层八份文档 + 43 条备课原则 + 审计协议 + 手法库）、九环节自动化机制与阶段 skill（`.agents/skills/`）。一切工作服务于三目标：让学生**学到更多有价值的知识、真正学懂、享受学习**（机制定义见 `work/evaluation/三目标实现机制.md`，环节地图见 `docs/workflow/教学全流程地图.md`，agent 工作规约见 `AGENTS.md`）。

## 目录结构

```
.
├── scripts/                  # 构建器（build_*）、校验器（validate_*）、检查器（checks/）
│   ├── mineru_client.py      # MinerU v4 API 客户端（submit/poll/download）
│   ├── batch_mineru.py       # 批量提交教材 PDF 到 MinerU 并整理结果
│   ├── split_by_lesson.py    # 按课切分 PDF
│   ├── split_by_unit.py      # 按单元切分 PDF
│   └── analyze.py            # 解析结果分析
├── Data/
│   ├── textbook/             # 本机教材与教师用书目录（PDF 不随公开仓库分发）
│   ├── reference/            # 课程标准及来源登记；试卷原件不随公开仓库分发
│   └── textbook_extract/     # 公开教材切分的 MinerU 整理结果；PDF 原件仅本机保留
├── work/                     # 方法论与知识库（详见 work/README.md）
│   ├── knowledge/            # 机读知识库（81 卡 / 28 图谱 / 5 册表 / 高考分析）
│   ├── principles/           # 原则注册库（机器可读理念，绑定机制节点）
│   ├── evaluation/           # 三目标机制、评估标准、收敛规则、自检报告
│   ├── 备课基本原则.md        # 43 条备课原则（人读权威文本）
│   └── 备课/                 # 审计协议、手法库、《氓》课例产物
├── .agents/skills/           # 12 个阶段 skill（备课→上课→作业→测评→反思）
├── docs/                     # 全流程地图、设计规格与实施计划
└── tests/                    # pytest + node 测试
```

## 快速开始

### 1. 配置 MinerU Token

脚本通过环境变量或本地文件读取 MinerU API token，**不要写入代码**。

```bash
# 方式一：环境变量（推荐）
export MINERU_TOKEN="sk-xxxxxxxx"

# 方式二：复制模板并填入
cp .env.example .env
# 编辑 .env 填入 MINERU_TOKEN=sk-xxxxxxxx

# 方式三：写入本地 token 文件
echo "sk-xxxxxxxx" > ~/.workbuddy/mineru_token
```

Token 申请：https://mineru.net → 个人中心 → API Keys

### 2. 批量解析教材

需先在本机 `Data/textbook/` 放入合法获得的教材或教师用书 PDF；这些原件不包含在公开仓库中。

```bash
# 解析全部册（必修 + 选择性必修 + 教师用书）
python scripts/batch_mineru.py

# 或指定某册
python scripts/batch_mineru.py 选择性必修下册
```

可通过环境变量覆盖数据目录：
```bash
YUWEN_DATA_DIR=/path/to/textbook_extract python scripts/batch_mineru.py
```

## 文档导航

完整的备课方法论体系（四层八份文档）见 [`work/README.md`](work/README.md)。

## 注意事项

- 公开仓库不分发教材、教师用书、高考试卷及第三方参考原件；Markdown、JSON、知识卡、题目切分、来源登记和 MinerU 整理结果公开。
- 原件在 `work/knowledge/_meta/artifacts.jsonl` 中以 `repository_visibility: private_local` 登记；本机存在时仍校验文件大小与 SHA-256，公开工作树中可缺席。
- MinerU token 属敏感信息，请勿提交到代码中；本仓库已通过 `.gitignore` 排除 `.env`、`*.token`、`.workbuddy/` 等。
