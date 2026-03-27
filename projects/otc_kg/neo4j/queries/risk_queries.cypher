// Q1: 共享银行账户客户群 - 识别可疑关联客户
MATCH (a:CustomerAccount)-[:SHARES_BANK_ACCOUNT_WITH]->(b:CustomerAccount)
RETURN a.cust_account_id AS account_a, a.account_name AS name_a,
       b.cust_account_id AS account_b, b.account_name AS name_b
ORDER BY a.cust_account_id
LIMIT 20;

// Q2: 客户OTC全链路追踪 - 从客户到收款的完整路径
MATCH path = (c:CustomerAccount)-[:PLACED_ORDER]->(o:SalesOrder)-[:HAS_LINE]->(l:SalesOrderLine)-[:FULFILLED_BY]->(d:DeliveryDetail)-[:GENERATED_FROM_DELIVERY*0..1]->(il:InvoiceLine)<-[:HAS_LINE]-(i:Invoice)-[:GENERATES_AR]->(ps:PaymentSchedule)<-[:APPLIED_TO]-(cr:CashReceipt)
WHERE c.cust_account_id = 300000001
RETURN path
LIMIT 5;

// Q3: 高逾期应收客户列表 - overdue_days > 90
MATCH (ps:PaymentSchedule)
WHERE ps.overdue_days > 90
MATCH (i:Invoice {customer_trx_id: ps.customer_trx_id})
MATCH (c:CustomerAccount {cust_account_id: i.sold_to_customer_id})
RETURN c.cust_account_id, c.account_name, ps.amount_due_remaining, ps.overdue_days
ORDER BY ps.overdue_days DESC
LIMIT 20;

// Q4: 审批订单穿透 - 查看订单审批链
MATCH (e:Employee)-[r:APPROVED]->(o:SalesOrder)
RETURN e.employee_name, e.department_name, o.order_number, o.order_amount
ORDER BY o.order_amount DESC
LIMIT 20;

// Q5: 收款核销路径查询 - 一笔收款核销了哪些发票
MATCH (cr:CashReceipt)-[r:APPLIED_TO]->(i:Invoice)
WHERE cr.cash_receipt_id = 1600000001
RETURN cr.receipt_number, cr.receipt_amount, i.trx_number, i.trx_amount, r.amount_applied;

// Q6: 高风险客户订单分析 - risk_level = 'HIGH' 的客户的订单
MATCH (p:CustomerParty {risk_level: 'HIGH'})-[:HAS_ACCOUNT]->(c:CustomerAccount)-[:PLACED_ORDER]->(o:SalesOrder)
RETURN p.party_name, p.risk_level, c.account_name, o.order_number, o.order_amount, o.flow_status_code
ORDER BY o.order_amount DESC
LIMIT 20;

// Q7: 未开票发货 - 发货了但没有对应发票
MATCH (d:DeliveryDetail)
WHERE NOT (d)<-[:GENERATED_FROM_DELIVERY]-(:InvoiceLine)
MATCH (l:SalesOrderLine {line_id: d.source_line_id})
MATCH (o:SalesOrder {header_id: l.header_id})
MATCH (c:CustomerAccount {cust_account_id: o.sold_to_org_id})
RETURN c.account_name, o.order_number, d.delivery_detail_id, d.shipped_quantity, d.actual_shipment_date
LIMIT 20;

// Q8: 大额折扣订单 - discount_percent > 20%
MATCH (l:SalesOrderLine)
WHERE l.discount_percent > 20
MATCH (o:SalesOrder {header_id: l.header_id})
MATCH (c:CustomerAccount {cust_account_id: o.sold_to_org_id})
RETURN c.account_name, o.order_number, l.line_id, l.discount_percent, l.line_amount
ORDER BY l.discount_percent DESC
LIMIT 20;

// Q9: 客户信用档案与订单对比 - 订单金额超过信用额度
MATCH (c:CustomerAccount)-[:HAS_CREDIT_PROFILE]->(cp:CreditProfile)
MATCH (c)-[:PLACED_ORDER]->(o:SalesOrder)
WHERE o.order_amount > cp.credit_limit
RETURN c.account_name, cp.credit_limit, o.order_number, o.order_amount, o.flow_status_code
LIMIT 20;

// Q10: 风险客户网络 - 共享银行账户的客户扩展网络
MATCH (a:CustomerAccount)-[:SHARES_BANK_ACCOUNT_WITH]-(b:CustomerAccount)
MATCH (a)-[:PLACED_ORDER]->(oa:SalesOrder)
MATCH (b)-[:PLACED_ORDER]->(ob:SalesOrder)
RETURN a.account_name, oa.order_number, oa.order_amount, b.account_name, ob.order_number, ob.order_amount
LIMIT 20;
