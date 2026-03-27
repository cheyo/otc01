CREATE CONSTRAINT customer_party_id IF NOT EXISTS FOR (n:CustomerParty) REQUIRE n.party_id IS UNIQUE;
CREATE CONSTRAINT customer_account_id IF NOT EXISTS FOR (n:CustomerAccount) REQUIRE n.cust_account_id IS UNIQUE;
CREATE CONSTRAINT address_id IF NOT EXISTS FOR (n:Address) REQUIRE n.location_id IS UNIQUE;
CREATE CONSTRAINT bank_account_id IF NOT EXISTS FOR (n:BankAccount) REQUIRE n.bank_account_id IS UNIQUE;
CREATE CONSTRAINT credit_profile_id IF NOT EXISTS FOR (n:CreditProfile) REQUIRE n.credit_profile_id IS UNIQUE;
CREATE CONSTRAINT sales_order_id IF NOT EXISTS FOR (n:SalesOrder) REQUIRE n.header_id IS UNIQUE;
CREATE CONSTRAINT sales_order_line_id IF NOT EXISTS FOR (n:SalesOrderLine) REQUIRE n.line_id IS UNIQUE;
CREATE CONSTRAINT delivery_detail_id IF NOT EXISTS FOR (n:DeliveryDetail) REQUIRE n.delivery_detail_id IS UNIQUE;
CREATE CONSTRAINT invoice_id IF NOT EXISTS FOR (n:Invoice) REQUIRE n.customer_trx_id IS UNIQUE;
CREATE CONSTRAINT invoice_line_id IF NOT EXISTS FOR (n:InvoiceLine) REQUIRE n.customer_trx_line_id IS UNIQUE;
CREATE CONSTRAINT payment_schedule_id IF NOT EXISTS FOR (n:PaymentSchedule) REQUIRE n.payment_schedule_id IS UNIQUE;
CREATE CONSTRAINT cash_receipt_id IF NOT EXISTS FOR (n:CashReceipt) REQUIRE n.cash_receipt_id IS UNIQUE;
CREATE CONSTRAINT employee_id IF NOT EXISTS FOR (n:Employee) REQUIRE n.employee_id IS UNIQUE;

// Import sample using Neo4j Browser after placing CSV under import dir or via LOAD CSV from file URL if enabled.
// Example:
// LOAD CSV WITH HEADERS FROM 'file:///nodes_customer_party.csv' AS row
// MERGE (n:CustomerParty {party_id: toInteger(row.party_id)})
// SET n.party_name = row.party_name, n.risk_level = row.risk_level;
