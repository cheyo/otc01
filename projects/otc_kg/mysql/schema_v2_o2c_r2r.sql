-- OTC KG v2: Standard O2C + R2R schema blueprint
CREATE DATABASE IF NOT EXISTS otc_kg_v2 CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE otc_kg_v2;

-- =========================
-- O2C Master Data
-- =========================
CREATE TABLE IF NOT EXISTS HZ_PARTIES (
  party_id BIGINT PRIMARY KEY,
  party_name VARCHAR(240) NOT NULL,
  party_type VARCHAR(30) NOT NULL DEFAULT 'ORGANIZATION',
  tax_reference VARCHAR(60),
  industry_code VARCHAR(30),
  risk_level VARCHAR(30),
  province VARCHAR(60),
  city VARCHAR(60),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS HZ_LOCATIONS (
  location_id BIGINT PRIMARY KEY,
  country VARCHAR(30) DEFAULT 'CN',
  province_name VARCHAR(60),
  city_name VARCHAR(60),
  district_name VARCHAR(60),
  address_line1 VARCHAR(255),
  postal_code VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS HZ_CUST_ACCOUNTS (
  cust_account_id BIGINT PRIMARY KEY,
  party_id BIGINT NOT NULL,
  account_number VARCHAR(60) NOT NULL,
  account_name VARCHAR(240) NOT NULL,
  account_status VARCHAR(30) DEFAULT 'ACTIVE',
  payment_term_code VARCHAR(30),
  region_code VARCHAR(60),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY idx_hca_party_id (party_id)
);

CREATE TABLE IF NOT EXISTS HZ_CUST_ACCT_SITES_ALL (
  cust_acct_site_id BIGINT PRIMARY KEY,
  cust_account_id BIGINT NOT NULL,
  location_id BIGINT NOT NULL,
  site_code VARCHAR(60) NOT NULL,
  status VARCHAR(30) DEFAULT 'ACTIVE',
  KEY idx_hcasa_account (cust_account_id),
  KEY idx_hcasa_location (location_id)
);

CREATE TABLE IF NOT EXISTS HZ_CUST_SITE_USES_ALL (
  site_use_id BIGINT PRIMARY KEY,
  cust_acct_site_id BIGINT NOT NULL,
  site_use_code VARCHAR(30) NOT NULL,
  primary_flag CHAR(1) DEFAULT 'N',
  status VARCHAR(30) DEFAULT 'ACTIVE',
  KEY idx_hcsua_site (cust_acct_site_id),
  KEY idx_hcsua_use (site_use_code)
);

CREATE TABLE IF NOT EXISTS CUST_BANK_ACCOUNTS (
  bank_account_id BIGINT PRIMARY KEY,
  cust_account_id BIGINT NOT NULL,
  bank_name VARCHAR(240) NOT NULL,
  bank_account_num VARCHAR(80) NOT NULL,
  account_holder_name VARCHAR(240),
  bank_branch_name VARCHAR(240),
  active_flag CHAR(1) DEFAULT 'Y',
  KEY idx_cba_account (cust_account_id),
  KEY idx_cba_bank_num (bank_account_num)
);

CREATE TABLE IF NOT EXISTS CUST_CREDIT_PROFILES (
  credit_profile_id BIGINT PRIMARY KEY,
  cust_account_id BIGINT NOT NULL,
  credit_limit DECIMAL(18,2) NOT NULL,
  currency_code VARCHAR(10) DEFAULT 'CNY',
  risk_level VARCHAR(30),
  risk_score DECIMAL(10,2),
  credit_checking VARCHAR(30) DEFAULT 'Y',
  review_date DATE,
  KEY idx_ccp_account (cust_account_id)
);

CREATE TABLE IF NOT EXISTS HR_OPERATING_UNITS (
  org_id BIGINT PRIMARY KEY,
  org_code VARCHAR(30) NOT NULL,
  org_name VARCHAR(240) NOT NULL,
  legal_entity_name VARCHAR(240),
  country_code VARCHAR(30) DEFAULT 'CN'
);

CREATE TABLE IF NOT EXISTS HR_EMPLOYEES (
  employee_id BIGINT PRIMARY KEY,
  employee_name VARCHAR(240) NOT NULL,
  department_name VARCHAR(120),
  role_code VARCHAR(60),
  org_id BIGINT,
  manager_id BIGINT,
  status VARCHAR(30) DEFAULT 'ACTIVE',
  KEY idx_emp_org (org_id)
);

CREATE TABLE IF NOT EXISTS RA_SALESREPS_ALL (
  salesrep_id BIGINT PRIMARY KEY,
  employee_id BIGINT,
  salesrep_number VARCHAR(60),
  salesrep_name VARCHAR(240),
  org_id BIGINT,
  status VARCHAR(30) DEFAULT 'ACTIVE',
  KEY idx_salesrep_emp (employee_id)
);

CREATE TABLE IF NOT EXISTS INV_ORGANIZATION_UNITS (
  inventory_org_id BIGINT PRIMARY KEY,
  org_code VARCHAR(30),
  org_name VARCHAR(240),
  org_type VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS MTL_SYSTEM_ITEMS_B (
  inventory_item_id BIGINT PRIMARY KEY,
  organization_id BIGINT,
  item_number VARCHAR(60),
  item_description VARCHAR(240),
  item_type VARCHAR(30),
  uom_code VARCHAR(30),
  list_price DECIMAL(18,2),
  active_flag CHAR(1) DEFAULT 'Y',
  KEY idx_items_org (organization_id)
);

-- =========================
-- O2C Order Management
-- =========================
CREATE TABLE IF NOT EXISTS OE_TRANSACTION_TYPES_ALL (
  transaction_type_id BIGINT PRIMARY KEY,
  transaction_type_code VARCHAR(30),
  transaction_type_name VARCHAR(120),
  category_code VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS OE_ORDER_HEADERS_ALL (
  header_id BIGINT PRIMARY KEY,
  order_number VARCHAR(60) NOT NULL,
  order_date DATETIME NOT NULL,
  sold_to_org_id BIGINT NOT NULL,
  ship_to_org_id BIGINT,
  bill_to_org_id BIGINT,
  org_id BIGINT,
  salesrep_id BIGINT,
  transaction_type_id BIGINT,
  currency_code VARCHAR(10) DEFAULT 'CNY',
  order_amount DECIMAL(18,2) NOT NULL,
  flow_status_code VARCHAR(30),
  order_type_code VARCHAR(30),
  approval_status VARCHAR(30),
  KEY idx_oeh_sold_to (sold_to_org_id),
  KEY idx_oeh_order_number (order_number),
  KEY idx_oeh_order_date (order_date)
);

CREATE TABLE IF NOT EXISTS OE_ORDER_LINES_ALL (
  line_id BIGINT PRIMARY KEY,
  header_id BIGINT NOT NULL,
  line_number INT NOT NULL,
  inventory_item_id BIGINT,
  inventory_org_id BIGINT,
  ordered_quantity DECIMAL(18,4) NOT NULL,
  unit_selling_price DECIMAL(18,2) NOT NULL,
  line_amount DECIMAL(18,2) NOT NULL,
  discount_percent DECIMAL(8,2) DEFAULT 0,
  request_date DATE,
  promise_date DATE,
  flow_status_code VARCHAR(30),
  KEY idx_oel_header (header_id),
  KEY idx_oel_item (inventory_item_id)
);

CREATE TABLE IF NOT EXISTS OE_ORDER_HOLDS_ALL (
  hold_id BIGINT PRIMARY KEY,
  header_id BIGINT,
  line_id BIGINT,
  hold_type_code VARCHAR(30),
  hold_reason VARCHAR(240),
  released_flag CHAR(1) DEFAULT 'N',
  hold_date DATETIME,
  release_date DATETIME,
  KEY idx_hold_header (header_id),
  KEY idx_hold_line (line_id)
);

CREATE TABLE IF NOT EXISTS OE_PRICE_ADJUSTMENTS (
  adjustment_id BIGINT PRIMARY KEY,
  header_id BIGINT,
  line_id BIGINT,
  adjustment_type_code VARCHAR(30),
  adjustment_percent DECIMAL(8,2),
  adjustment_amount DECIMAL(18,2),
  reason_code VARCHAR(60),
  approved_flag CHAR(1) DEFAULT 'N',
  approver_id BIGINT,
  KEY idx_opa_header (header_id),
  KEY idx_opa_line (line_id)
);

-- =========================
-- O2C Shipping / Fulfillment
-- =========================
CREATE TABLE IF NOT EXISTS WSH_NEW_DELIVERIES (
  delivery_id BIGINT PRIMARY KEY,
  delivery_name VARCHAR(60),
  organization_id BIGINT,
  status_code VARCHAR(30),
  initial_pickup_date DATETIME,
  ultimate_dropoff_date DATETIME
);

CREATE TABLE IF NOT EXISTS WSH_DELIVERY_DETAILS (
  delivery_detail_id BIGINT PRIMARY KEY,
  source_header_id BIGINT,
  source_line_id BIGINT,
  delivery_id BIGINT,
  inventory_item_id BIGINT,
  shipped_quantity DECIMAL(18,4),
  requested_quantity DECIMAL(18,4),
  released_status VARCHAR(30),
  actual_shipment_date DATETIME,
  KEY idx_wdd_source_line (source_line_id),
  KEY idx_wdd_delivery (delivery_id)
);

CREATE TABLE IF NOT EXISTS WSH_DELIVERY_ASSIGNMENTS (
  assignment_id BIGINT PRIMARY KEY,
  delivery_id BIGINT NOT NULL,
  delivery_detail_id BIGINT NOT NULL,
  assigned_date DATETIME,
  KEY idx_wda_delivery (delivery_id),
  KEY idx_wda_detail (delivery_detail_id)
);

-- =========================
-- O2C Invoicing / AR
-- =========================
CREATE TABLE IF NOT EXISTS RA_BATCH_SOURCES_ALL (
  batch_source_id BIGINT PRIMARY KEY,
  source_name VARCHAR(120),
  source_type VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS RA_CUST_TRX_TYPES_ALL (
  cust_trx_type_id BIGINT PRIMARY KEY,
  trx_type_name VARCHAR(120),
  trx_class VARCHAR(30),
  accounting_affect_flag CHAR(1) DEFAULT 'Y'
);

CREATE TABLE IF NOT EXISTS RA_CUSTOMER_TRX_ALL (
  customer_trx_id BIGINT PRIMARY KEY,
  trx_number VARCHAR(60) NOT NULL,
  trx_date DATETIME NOT NULL,
  sold_to_customer_id BIGINT NOT NULL,
  bill_to_customer_id BIGINT,
  batch_source_id BIGINT,
  cust_trx_type_id BIGINT,
  org_id BIGINT,
  currency_code VARCHAR(10) DEFAULT 'CNY',
  trx_amount DECIMAL(18,2) NOT NULL,
  status VARCHAR(30),
  KEY idx_rcta_customer (sold_to_customer_id),
  KEY idx_rcta_trx_number (trx_number)
);

CREATE TABLE IF NOT EXISTS RA_CUSTOMER_TRX_LINES_ALL (
  customer_trx_line_id BIGINT PRIMARY KEY,
  customer_trx_id BIGINT NOT NULL,
  line_number INT,
  inventory_item_id BIGINT,
  quantity_invoiced DECIMAL(18,4),
  unit_selling_price DECIMAL(18,2),
  extended_amount DECIMAL(18,2),
  line_type VARCHAR(30),
  KEY idx_rctla_trx (customer_trx_id)
);

CREATE TABLE IF NOT EXISTS INVOICE_ORDER_LINK (
  link_id BIGINT PRIMARY KEY,
  customer_trx_line_id BIGINT NOT NULL,
  order_line_id BIGINT,
  delivery_detail_id BIGINT,
  header_id BIGINT,
  KEY idx_iol_trx_line (customer_trx_line_id),
  KEY idx_iol_order_line (order_line_id)
);

CREATE TABLE IF NOT EXISTS ZX_TAX_LINES (
  tax_line_id BIGINT PRIMARY KEY,
  customer_trx_id BIGINT,
  customer_trx_line_id BIGINT,
  tax_type_code VARCHAR(30),
  tax_rate DECIMAL(8,4),
  taxable_amount DECIMAL(18,2),
  tax_amount DECIMAL(18,2),
  KEY idx_zx_trx (customer_trx_id)
);

CREATE TABLE IF NOT EXISTS AR_PAYMENT_SCHEDULES_ALL (
  payment_schedule_id BIGINT PRIMARY KEY,
  customer_trx_id BIGINT NOT NULL,
  due_date DATE NOT NULL,
  amount_due_original DECIMAL(18,2),
  amount_due_remaining DECIMAL(18,2),
  amount_applied DECIMAL(18,2),
  status VARCHAR(30),
  overdue_days INT DEFAULT 0,
  KEY idx_aps_trx (customer_trx_id),
  KEY idx_aps_due_date (due_date)
);

CREATE TABLE IF NOT EXISTS AR_ADJUSTMENTS_ALL (
  adjustment_id BIGINT PRIMARY KEY,
  customer_trx_id BIGINT,
  payment_schedule_id BIGINT,
  adjustment_type VARCHAR(30),
  adjustment_amount DECIMAL(18,2),
  reason_code VARCHAR(60),
  created_by BIGINT,
  creation_date DATETIME,
  KEY idx_adj_trx (customer_trx_id)
);

CREATE TABLE IF NOT EXISTS RA_CREDIT_MEMO_ALL (
  credit_memo_id BIGINT PRIMARY KEY,
  customer_trx_id BIGINT,
  credit_memo_number VARCHAR(60),
  credit_memo_date DATETIME,
  amount DECIMAL(18,2),
  reason_code VARCHAR(60),
  status VARCHAR(30),
  KEY idx_cm_trx (customer_trx_id)
);

-- =========================
-- O2C Receipts / Cash / Bank
-- =========================
CREATE TABLE IF NOT EXISTS AR_RECEIPT_METHODS (
  receipt_method_id BIGINT PRIMARY KEY,
  receipt_method_name VARCHAR(120),
  method_type VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS CE_BANK_ACCOUNTS (
  ce_bank_account_id BIGINT PRIMARY KEY,
  bank_name VARCHAR(240),
  bank_account_num VARCHAR(80),
  currency_code VARCHAR(10) DEFAULT 'CNY',
  account_owner_name VARCHAR(240)
);

CREATE TABLE IF NOT EXISTS AR_CASH_RECEIPTS_ALL (
  cash_receipt_id BIGINT PRIMARY KEY,
  receipt_number VARCHAR(60) NOT NULL,
  receipt_date DATETIME NOT NULL,
  payer_customer_id BIGINT NOT NULL,
  receipt_method_id BIGINT,
  ce_bank_account_id BIGINT,
  receipt_amount DECIMAL(18,2) NOT NULL,
  status VARCHAR(30),
  KEY idx_acr_customer (payer_customer_id),
  KEY idx_acr_receipt_number (receipt_number)
);

CREATE TABLE IF NOT EXISTS AR_RECEIVABLE_APPLICATIONS_ALL (
  receivable_application_id BIGINT PRIMARY KEY,
  cash_receipt_id BIGINT NOT NULL,
  applied_customer_trx_id BIGINT NOT NULL,
  payment_schedule_id BIGINT,
  amount_applied DECIMAL(18,2) NOT NULL,
  application_date DATETIME,
  status VARCHAR(30),
  KEY idx_araa_receipt (cash_receipt_id),
  KEY idx_araa_trx (applied_customer_trx_id)
);

CREATE TABLE IF NOT EXISTS CE_STATEMENT_HEADERS (
  statement_header_id BIGINT PRIMARY KEY,
  ce_bank_account_id BIGINT,
  statement_number VARCHAR(60),
  statement_date DATE,
  opening_balance DECIMAL(18,2),
  closing_balance DECIMAL(18,2)
);

CREATE TABLE IF NOT EXISTS CE_STATEMENT_LINES (
  statement_line_id BIGINT PRIMARY KEY,
  statement_header_id BIGINT,
  trx_date DATE,
  amount DECIMAL(18,2),
  dr_cr_flag CHAR(1),
  reference_text VARCHAR(240),
  reconciliation_status VARCHAR(30),
  KEY idx_csl_header (statement_header_id)
);

-- =========================
-- R2R Core
-- =========================
CREATE TABLE IF NOT EXISTS GL_LEDGERS (
  ledger_id BIGINT PRIMARY KEY,
  ledger_name VARCHAR(240) NOT NULL,
  currency_code VARCHAR(10) DEFAULT 'CNY',
  calendar_name VARCHAR(120),
  chart_of_accounts_name VARCHAR(240)
);

CREATE TABLE IF NOT EXISTS GL_PERIODS (
  period_name VARCHAR(30) PRIMARY KEY,
  period_year INT,
  period_num INT,
  start_date DATE,
  end_date DATE,
  status VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS GL_CODE_COMBINATIONS (
  code_combination_id BIGINT PRIMARY KEY,
  segment1_company VARCHAR(30),
  segment2_department VARCHAR(30),
  segment3_account VARCHAR(30),
  segment4_product VARCHAR(30),
  segment5_intercompany VARCHAR(30),
  enabled_flag CHAR(1) DEFAULT 'Y'
);

CREATE TABLE IF NOT EXISTS XLA_AE_HEADERS (
  ae_header_id BIGINT PRIMARY KEY,
  application_id BIGINT,
  entity_code VARCHAR(60),
  source_id BIGINT,
  accounting_date DATE,
  period_name VARCHAR(30),
  ledger_id BIGINT,
  accounting_status VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS XLA_AE_LINES (
  ae_line_id BIGINT PRIMARY KEY,
  ae_header_id BIGINT NOT NULL,
  line_num INT,
  code_combination_id BIGINT,
  entered_dr DECIMAL(18,2),
  entered_cr DECIMAL(18,2),
  accounted_dr DECIMAL(18,2),
  accounted_cr DECIMAL(18,2),
  description VARCHAR(240),
  KEY idx_xla_lines_header (ae_header_id)
);

CREATE TABLE IF NOT EXISTS XLA_DISTRIBUTION_LINKS (
  distribution_link_id BIGINT PRIMARY KEY,
  ae_header_id BIGINT NOT NULL,
  ae_line_id BIGINT NOT NULL,
  source_distribution_type VARCHAR(60),
  source_distribution_id BIGINT,
  source_trx_id BIGINT,
  KEY idx_xdl_header (ae_header_id),
  KEY idx_xdl_line (ae_line_id)
);

CREATE TABLE IF NOT EXISTS GL_JE_SOURCES (
  je_source_name VARCHAR(60) PRIMARY KEY,
  user_je_source_name VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS GL_JE_CATEGORIES (
  je_category_name VARCHAR(60) PRIMARY KEY,
  user_je_category_name VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS GL_JE_HEADERS (
  je_header_id BIGINT PRIMARY KEY,
  ledger_id BIGINT NOT NULL,
  period_name VARCHAR(30) NOT NULL,
  je_source_name VARCHAR(60),
  je_category_name VARCHAR(60),
  accounting_date DATE,
  currency_code VARCHAR(10) DEFAULT 'CNY',
  status VARCHAR(30),
  total_dr DECIMAL(18,2),
  total_cr DECIMAL(18,2),
  KEY idx_gljh_ledger (ledger_id),
  KEY idx_gljh_period (period_name)
);

CREATE TABLE IF NOT EXISTS GL_JE_LINES (
  je_line_id BIGINT PRIMARY KEY,
  je_header_id BIGINT NOT NULL,
  line_num INT,
  code_combination_id BIGINT NOT NULL,
  entered_dr DECIMAL(18,2),
  entered_cr DECIMAL(18,2),
  accounted_dr DECIMAL(18,2),
  accounted_cr DECIMAL(18,2),
  description VARCHAR(240),
  KEY idx_gljl_header (je_header_id),
  KEY idx_gljl_ccid (code_combination_id)
);

CREATE TABLE IF NOT EXISTS GL_IMPORT_REFERENCES (
  import_reference_id BIGINT PRIMARY KEY,
  je_header_id BIGINT NOT NULL,
  je_line_id BIGINT NOT NULL,
  ae_header_id BIGINT,
  ae_line_id BIGINT,
  reference_table_name VARCHAR(60),
  reference_id BIGINT,
  KEY idx_gir_header (je_header_id),
  KEY idx_gir_ae (ae_header_id)
);

CREATE TABLE IF NOT EXISTS GL_BALANCES (
  balance_id BIGINT PRIMARY KEY,
  ledger_id BIGINT NOT NULL,
  period_name VARCHAR(30) NOT NULL,
  code_combination_id BIGINT NOT NULL,
  begin_balance_dr DECIMAL(18,2),
  begin_balance_cr DECIMAL(18,2),
  period_net_dr DECIMAL(18,2),
  period_net_cr DECIMAL(18,2),
  end_balance_dr DECIMAL(18,2),
  end_balance_cr DECIMAL(18,2),
  KEY idx_glb_period (period_name),
  KEY idx_glb_ccid (code_combination_id)
);

-- =========================
-- Risk / Control Extension
-- =========================
CREATE TABLE IF NOT EXISTS OTC_APPROVAL_LOG (
  approval_log_id BIGINT PRIMARY KEY,
  business_type VARCHAR(60),
  business_id BIGINT,
  approver_id BIGINT,
  approval_action VARCHAR(30),
  approval_date DATETIME,
  comments VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS OTC_FIELD_CHANGE_LOG (
  change_log_id BIGINT PRIMARY KEY,
  table_name VARCHAR(120),
  record_id BIGINT,
  field_name VARCHAR(120),
  old_value VARCHAR(500),
  new_value VARCHAR(500),
  changed_by BIGINT,
  changed_at DATETIME,
  risk_flag CHAR(1) DEFAULT 'N'
);

CREATE TABLE IF NOT EXISTS OTC_RISK_EVENTS (
  risk_event_id BIGINT PRIMARY KEY,
  risk_code VARCHAR(30),
  business_type VARCHAR(60),
  business_id BIGINT,
  cust_account_id BIGINT,
  risk_level VARCHAR(30),
  risk_score DECIMAL(10,2),
  detected_at DATETIME,
  event_desc VARCHAR(500)
);
