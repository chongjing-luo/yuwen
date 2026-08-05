# 语文备课系统 (Yuwen)

面向高中语文教学的知识点提取与备课方法论系统。基于 6 本统编高中语文教材（144 课），使用 MinerU API 进行 PDF→Markdown 解析，并沉淀四层八份完整备课方法论文档。

## 目录结构

```
.
├── scripts/                  # Python 工具脚本
│   ├── mineru_client.py      # MinerU v4 API 客户端（submit/poll/download）
│   ├── batch_mineru.py       # 批量提交教材 PDF 到 MinerU 并整理结果
│   ├── split_by_lesson.py    # 按课切分 PDF
│   ├── split_by_unit.py      # 按单元切分 PDF
│   └── analyze.py            # 解析结果分析
├── Data/
│   ├── textbook/             # 原始教材 PDF（6 本）
│   └── textbook_extract/     # 切分后的 PDF + MinerU 解析结果（mineru_result/）
├── work/                     # 备课方法论文档体系（详见 work/README.md）
│   ├── 课程与教学理论方法论（语文版/通用版）.md
│   ├── 备课方法论（语文版/通用版）.md
│   ├── 教学环节技术与技巧（语文版/通用版）.md
│   ├── PPT设计与演示方法论（语文版/通用版）.md
│   └── 语文备课系统_知识点提取研究计划.md
├── textbook_extract/         # 教材编排逻辑梳理
└── output/                   # 脚本输出
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

- `Data/` 下含教材 PDF 及解析数据，体积较大。
- MinerU token 属敏感信息，请勿提交到代码中；本仓库已通过 `.gitignore` 排除 `.env`、`*.token`、`.workbuddy/` 等。
