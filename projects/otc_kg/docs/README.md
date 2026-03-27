# OTC KG 项目骨架

本目录包含一个可在本机执行的第一版实现：

## 内容
- `mysql/schema_v1.sql`：MySQL 建库建表脚本
- `generator/scripts/generate_sample_data.py`：生成中国化 OTC 样本 CSV 数据
- `generator/output/sample_csv/`：脚本输出目录

## 当前样本规模
这是第一版可执行样本，不是 50 万正式版：
- 客户主体：1000
- 订单头：3000
- 订单行：按业务规律自动放大
- 发票、AR、收款：按履约链自动生成

## 执行步骤
### 1. 生成 CSV
```bash
python3 projects/otc_kg/generator/scripts/generate_sample_data.py
```

### 2. 建库建表
```bash
mysql -u root -p'vv7g51Hou' < projects/otc_kg/mysql/schema_v1.sql
```

### 3. 导入 CSV
建议后续使用 `LOAD DATA LOCAL INFILE` 或 Python 批量写入。

## 下一步
- 扩展到 50 万+ 正式规模
- 补充风险注入审计表
- 生成 Neo4j 导入 CSV
- 开发 Web 系统与自然语言查询层
