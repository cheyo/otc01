# schema_v1 -> schema_v2 (O2C + R2R 标准方案) 映射清单

本文档用于指导当前 OTC 原型从 `schema_v1.sql` 迁移到 `schema_v2_o2c_r2r.sql`。

## 一、迁移状态定义

- **直接保留**：旧表可延续，只需要补字段或轻微调整
- **扩展保留**：旧表保留主体，但要新增字段或补关联维度
- **新增标准表**：旧版没有，需要在 v2 中正式新增
- **桥接增强**：用于连通 O2C 和 R2R

---

## 二、客户与主数据层

| schema_v1 表 | schema_v2 表 | 状态 | 处理说明 |
|---|---|---|---|
| HZ_PARTIES | HZ_PARTIES | 直接保留 | 保留主体，补标准字段如 party_type、created_at |
| HZ_LOCATIONS | HZ_LOCATIONS | 直接保留 | 保留地址维度，补 country/postal_code |
| HZ_CUST_ACCOUNTS | HZ_CUST_ACCOUNTS | 扩展保留 | 保留核心账户表，补站点、org、created_at 等关联维度 |
| - | HZ_CUST_ACCT_SITES_ALL | 新增标准表 | 新增客户站点表，支撑 ship-to / bill-to / usage |
| - | HZ_CUST_SITE_USES_ALL | 新增标准表 | 新增站点用途表，区分 BILL_TO、SHIP_TO |
| CUST_BANK_ACCOUNTS | CUST_BANK_ACCOUNTS | 扩展保留 | 保留银行账户主体，补户名、支行、启用状态 |
| CUST_CREDIT_PROFILES | CUST_CREDIT_PROFILES | 扩展保留 | 保留信用档案主体，补 currency/review/credit_checking |
| HR_EMPLOYEES | HR_EMPLOYEES | 扩展保留 | 保留员工主体，补 org_id、manager_id |
| - | HR_OPERATING_UNITS | 新增标准表 | 新增业务组织维度 |
| - | RA_SALESREPS_ALL | 新增标准表 | 新增销售员维度 |
| - | INV_ORGANIZATION_UNITS | 新增标准表 | 新增库存组织维度 |
| - | MTL_SYSTEM_ITEMS_B | 新增标准表 | 新增物料主数据 |

---

## 三、订单与价格层

| schema_v1 表 | schema_v2 表 | 状态 | 处理说明 |
|---|---|---|---|
| OE_ORDER_HEADERS_ALL | OE_ORDER_HEADERS_ALL | 扩展保留 | 保留订单头，补 sold_to/bill_to/ship_to/org/salesrep/type |
| OE_ORDER_LINES_ALL | OE_ORDER_LINES_ALL | 扩展保留 | 保留订单行，补 inventory_org、schedule 日期、状态 |
| OE_PRICE_ADJUSTMENTS | OE_PRICE_ADJUSTMENTS | 扩展保留 | 保留价格调整，补 adjustment_type、approver_id |
| - | OE_TRANSACTION_TYPES_ALL | 新增标准表 | 订单类型标准维表 |
| - | OE_ORDER_HOLDS_ALL | 新增标准表 | 订单冻结、信用冻结、审批控制 |

---

## 四、履约与发运层

| schema_v1 表 | schema_v2 表 | 状态 | 处理说明 |
|---|---|---|---|
| WSH_DELIVERY_DETAILS | WSH_DELIVERY_DETAILS | 扩展保留 | 保留发运行主体，补 delivery_id、inventory_item_id |
| - | WSH_NEW_DELIVERIES | 新增标准表 | 新增发运单头 |
| - | WSH_DELIVERY_ASSIGNMENTS | 新增标准表 | 新增发运行到发运单分配关系 |

---

## 五、发票与应收层

| schema_v1 表 | schema_v2 表 | 状态 | 处理说明 |
|---|---|---|---|
| RA_CUSTOMER_TRX_ALL | RA_CUSTOMER_TRX_ALL | 扩展保留 | 保留发票头，补 batch_source/type/org 等维度 |
| RA_CUSTOMER_TRX_LINES_ALL | RA_CUSTOMER_TRX_LINES_ALL | 扩展保留 | 保留发票行，补 item/price/line_type |
| INVOICE_ORDER_LINK | INVOICE_ORDER_LINK | 扩展保留 | 保留桥接，补 header_id 等冗余关联 |
| AR_PAYMENT_SCHEDULES_ALL | AR_PAYMENT_SCHEDULES_ALL | 扩展保留 | 保留应收计划，补金额拆分字段 |
| AR_ADJUSTMENTS_ALL | AR_ADJUSTMENTS_ALL | 扩展保留 | 保留调整，补 type/reason/creator |
| RA_CREDIT_MEMO_ALL | RA_CREDIT_MEMO_ALL | 扩展保留 | 保留贷项通知单，补编号/日期/状态 |
| - | RA_BATCH_SOURCES_ALL | 新增标准表 | 发票来源维表 |
| - | RA_CUST_TRX_TYPES_ALL | 新增标准表 | 发票类型维表 |
| - | ZX_TAX_LINES | 新增标准表 | 税务行表，支持税额和税率分析 |

---

## 六、收款与银行层

| schema_v1 表 | schema_v2 表 | 状态 | 处理说明 |
|---|---|---|---|
| AR_CASH_RECEIPTS_ALL | AR_CASH_RECEIPTS_ALL | 扩展保留 | 保留收款主体，补 receipt_method/ce_bank_account |
| AR_RECEIVABLE_APPLICATIONS_ALL | AR_RECEIVABLE_APPLICATIONS_ALL | 扩展保留 | 保留核销主体，补 payment_schedule_id |
| - | AR_RECEIPT_METHODS | 新增标准表 | 新增收款方式维度 |
| - | CE_BANK_ACCOUNTS | 新增标准表 | 新增企业银行账户 |
| - | CE_STATEMENT_HEADERS | 新增标准表 | 新增银行对账单头 |
| - | CE_STATEMENT_LINES | 新增标准表 | 新增银行对账单行 |

---

## 七、风控增强层

| schema_v1 表 | schema_v2 表 | 状态 | 处理说明 |
|---|---|---|---|
| OTC_APPROVAL_LOG | OTC_APPROVAL_LOG | 直接保留 | 保留审批日志 |
| OTC_FIELD_CHANGE_LOG | OTC_FIELD_CHANGE_LOG | 直接保留 | 保留字段变更日志 |
| - | OTC_RISK_EVENTS | 新增标准表 | 新增标准风险事件表，统一管理风险输出 |

---

## 八、R2R 核心层（schema_v1 无，需要新增）

| schema_v2 表 | 用途 |
|---|---|
| GL_LEDGERS | 账簿主数据 |
| GL_PERIODS | 会计期间 |
| GL_CODE_COMBINATIONS | 科目组合 |
| XLA_AE_HEADERS | 子账会计头 |
| XLA_AE_LINES | 子账会计行 |
| XLA_DISTRIBUTION_LINKS | 子账到业务分配桥接 |
| GL_JE_SOURCES | 总账来源 |
| GL_JE_CATEGORIES | 总账类别 |
| GL_JE_HEADERS | 总账凭证头 |
| GL_JE_LINES | 总账凭证行 |
| GL_IMPORT_REFERENCES | 子账到总账桥接 |
| GL_BALANCES | 总账余额 |

---

## 九、建议实施顺序

### Phase 1: 表结构切换
1. 保留并扩展现有 O2C 主表
2. 新增主数据、站点、发运头、税行、收款方式等标准配套表
3. 新增 R2R 核心表与 XLA 桥接表

### Phase 2: 数据生成升级
1. 升级客户主数据生成逻辑
2. 新增物料、组织、销售员、站点数据
3. 新增发票来源、税行、总账、子账样本

### Phase 3: 图谱映射升级
1. 扩展 Neo4j 节点：Ledger、JournalEntry、AccountCombination、SubledgerEntry
2. 扩展关系：POSTED_TO、ACCOUNTED_AS、BALANCES_TO 等

### Phase 4: 应用升级
1. 新增 O2C 到 R2R 全链路查询
2. 新增凭证和余额可视化
3. 新增从业务单据追溯总账的风险分析视图
