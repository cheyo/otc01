# OTC Knowledge Graph Platform

基于 Oracle ETRM 标准表的 OTC (Order to Cash) 流程知识图谱风险分析平台。

## 项目概述

本项目构建了一套完整的 OTC 业务数据模拟与风险挖掘系统：

- **数据层**: MySQL 存储符合 Oracle ETRM 语义的 OTC 业务数据
- **图谱层**: Neo4j 存储业务实体和风险关系的知识图谱
- **服务层**: FastAPI 提供风险查询 API
- **展示层**: Vue.js 单页应用提供风险分析界面

## 当前样本规模

| 实体类型 | 数量 |
|---------|------|
| 客户主体 (CustomerParty) | 1,000 |
| 客户账户 (CustomerAccount) | 1,000 |
| 销售订单 (SalesOrder) | 3,000 |
| 订单行 (SalesOrderLine) | 6,000 |
| 发票 (Invoice) | 4,943 |
| 收款 (CashReceipt) | 4,943 |

## 技术栈

- **数据库**: MySQL 8.0
- **图数据库**: Neo4j 5.26
- **后端**: Python 3.11 + FastAPI
- **前端**: Vue 3 (CDN 版本)

## 快速开始

### 1. 启动后端服务

```bash
cd projects/otc_kg/backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. 访问前端页面

打开浏览器访问 `projects/otc_kg/frontend/index.html`

或通过 HTTP 服务器:

```bash
cd projects/otc_kg/frontend
python -m http.server 8080
# 访问 http://localhost:8080
```

### 3. API 端点

- `GET /health` - 健康检查
- `GET /stats` - 数据统计
- `POST /query/risk` - 执行预定义风险查询
- `POST /query/custom` - 执行自定义 Cypher 查询

## 风险查询场景

平台支持以下预定义风险查询：

1. **共享银行账户** - 识别共享银行账户的可疑客户群
2. **高逾期应收** - 查询逾期超过90天的应收账款
3. **高风险订单** - 查看高风险客户的订单
4. **大额折扣** - 识别折扣超过20%的订单
5. **未开票发货** - 发货但未开票的交易
6. **超信用订单** - 订单金额超过信用额度
7. **审批链路** - 订单审批穿透分析

## 项目结构

```
projects/otc_kg/
├── mysql/                    # MySQL 相关
│   ├── schema_v1.sql         # 建库建表脚本
│   └── load_sample.sql       # 数据导入脚本
├── neo4j/                    # Neo4j 相关
│   ├── import/               # 导入 CSV 文件
│   ├── export_mysql_to_neo4j.py  # 导出脚本
│   ├── load_sample.cypher    # 导入 Cypher
│   └── queries/              # 风险查询脚本
├── generator/                # 数据生成器
│   ├── scripts/              # 生成脚本
│   ├── dictionaries/         # 中文字典
│   └── output/               # 输出目录
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   └── main.py           # 主应用
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Vue.js 前端
│   └── index.html
└── docs/                     # 文档
```

## 数据生成

运行数据生成脚本：

```bash
python3 projects/otc_kg/generator/scripts/generate_sample_data.py
```

## 图谱导入

```bash
# 导出 MySQL 数据到 Neo4j CSV
python3 projects/otc_kg/neo4j/export_mysql_to_neo4j.py

# 导入到 Neo4j
docker exec neo4j cypher-shell -u neo4j -p password123 -f /var/lib/neo4j/import/load_sample.cypher
```

## 配置

后端配置文件 `backend/.env`:

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=otc_kg
```

## GitHub Repository

https://github.com/cheyo/otc01

## License

MIT