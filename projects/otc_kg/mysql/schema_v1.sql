CREATE DATABASE IF NOT EXISTS otc_kg DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE otc_kg;

CREATE TABLE IF NOT EXISTS HZ_PARTIES (
    party_id BIGINT NOT NULL PRIMARY KEY,
    party_number VARCHAR(50) NOT NULL,
    party_name VARCHAR(200) NOT NULL,
    party_type VARCHAR(30) NOT NULL,
    tax_reference VARCHAR(100) NULL,
    country_code VARCHAR(10) NOT NULL DEFAULT 'CN',
    province VARCHAR(100) NULL,
    city VARCHAR(100) NULL,
    industry_code VARCHAR(50) NULL,
    customer_size VARCHAR(30) NULL,
    risk_level VARCHAR(20) NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_hz_parties_party_number (party_number),
    KEY idx_hz_parties_party_name (party_name),
    KEY idx_hz_parties_tax_reference (tax_reference),
    KEY idx_hz_parties_industry_code (industry_code),
    KEY idx_hz_parties_risk_level (risk_level),
    KEY idx_hz_parties_province_city (province, city)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS HZ_LOCATIONS (
    location_id BIGINT NOT NULL PRIMARY KEY,
    country_code VARCHAR(10) NOT NULL DEFAULT 'CN',
    province_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    district_name VARCHAR(100) NULL,
    address_line1 VARCHAR(200) NOT NULL,
    postal_code VARCHAR(20) NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_hz_locations_region (province_name, city_name, district_name),
    KEY idx_hz_locations_postal_code (postal_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS HZ_CUST_ACCOUNTS (
    cust_account_id BIGINT NOT NULL PRIMARY KEY,
    party_id BIGINT NOT NULL,
    account_number VARCHAR(50) NOT NULL,
    account_name VARCHAR(200) NOT NULL,
    customer_class_code VARCHAR(50) NULL,
    credit_classification VARCHAR(50) NULL,
    payment_term_code VARCHAR(50) NULL,
    sales_channel_code VARCHAR(50) NULL,
    region_code VARCHAR(50) NULL,
    account_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    open_date DATETIME NOT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_hz_cust_accounts_account_number (account_number),
    KEY idx_hz_cust_accounts_party_id (party_id),
    KEY idx_hz_cust_accounts_status (account_status),
    KEY idx_hz_cust_accounts_region (region_code),
    KEY idx_hz_cust_accounts_payment_term (payment_term_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS HZ_CUST_ACCT_SITES_ALL (
    cust_acct_site_id BIGINT NOT NULL PRIMARY KEY,
    cust_account_id BIGINT NOT NULL,
    location_id BIGINT NOT NULL,
    site_code VARCHAR(50) NOT NULL,
    org_id BIGINT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_hz_cust_acct_sites_site_code (site_code),
    KEY idx_hz_cust_acct_sites_account_id (cust_account_id),
    KEY idx_hz_cust_acct_sites_location_id (location_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS HZ_CUST_SITE_USES_ALL (
    site_use_id BIGINT NOT NULL PRIMARY KEY,
    cust_acct_site_id BIGINT NOT NULL,
    site_use_code VARCHAR(30) NOT NULL,
    primary_flag CHAR(1) NOT NULL DEFAULT 'N',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_hz_cust_site_uses_site_id (cust_acct_site_id),
    KEY idx_hz_cust_site_uses_code (site_use_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS CUST_BANK_ACCOUNTS (
    bank_account_id BIGINT NOT NULL PRIMARY KEY,
    cust_account_id BIGINT NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    branch_name VARCHAR(100) NULL,
    bank_account_num VARCHAR(100) NOT NULL,
    account_name VARCHAR(200) NOT NULL,
    account_type VARCHAR(30) NOT NULL DEFAULT 'PUBLIC',
    is_primary CHAR(1) NOT NULL DEFAULT 'Y',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_cust_bank_accounts_cust_account_id (cust_account_id),
    KEY idx_cust_bank_accounts_bank_account_num (bank_account_num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS CUST_CREDIT_PROFILES (
    credit_profile_id BIGINT NOT NULL PRIMARY KEY,
    cust_account_id BIGINT NOT NULL,
    credit_limit DECIMAL(18,2) NOT NULL,
    currency_code VARCHAR(10) NOT NULL DEFAULT 'CNY',
    payment_terms VARCHAR(50) NULL,
    risk_level VARCHAR(20) NULL,
    risk_score DECIMAL(8,2) NULL,
    overdue_tolerance_days INT NOT NULL DEFAULT 0,
    credit_hold_flag CHAR(1) NOT NULL DEFAULT 'N',
    review_date DATETIME NULL,
    effective_start_date DATETIME NOT NULL,
    effective_end_date DATETIME NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_cust_credit_profiles_account_id (cust_account_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS HR_EMPLOYEES (
    employee_id BIGINT NOT NULL PRIMARY KEY,
    employee_no VARCHAR(50) NOT NULL,
    employee_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NULL,
    department_name VARCHAR(100) NOT NULL,
    role_code VARCHAR(50) NOT NULL,
    title_name VARCHAR(100) NULL,
    manager_id BIGINT NULL,
    region_code VARCHAR(50) NULL,
    hire_date DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_hr_employees_employee_no (employee_no),
    KEY idx_hr_employees_role (role_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS OE_ORDER_HEADERS_ALL (
    header_id BIGINT NOT NULL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL,
    sold_to_org_id BIGINT NOT NULL,
    ship_to_site_use_id BIGINT NULL,
    invoice_to_site_use_id BIGINT NULL,
    order_date DATETIME NOT NULL,
    booked_date DATETIME NULL,
    order_type_code VARCHAR(50) NULL,
    order_currency_code VARCHAR(10) NOT NULL DEFAULT 'CNY',
    transactional_curr_code VARCHAR(10) NULL,
    order_amount DECIMAL(18,2) NOT NULL,
    discount_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    tax_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    booked_flag CHAR(1) NOT NULL DEFAULT 'N',
    cancelled_flag CHAR(1) NOT NULL DEFAULT 'N',
    flow_status_code VARCHAR(30) NOT NULL,
    salesrep_id BIGINT NULL,
    org_id BIGINT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_oe_order_headers_order_number (order_number),
    KEY idx_oe_order_headers_sold_to_org_id (sold_to_org_id),
    KEY idx_oe_order_headers_order_date (order_date),
    KEY idx_oe_order_headers_status (flow_status_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS OE_ORDER_LINES_ALL (
    line_id BIGINT NOT NULL PRIMARY KEY,
    header_id BIGINT NOT NULL,
    line_number INT NOT NULL,
    inventory_item_id BIGINT NOT NULL,
    ordered_quantity DECIMAL(18,2) NOT NULL,
    unit_selling_price DECIMAL(18,2) NOT NULL,
    list_price DECIMAL(18,2) NOT NULL,
    discount_percent DECIMAL(8,2) NOT NULL DEFAULT 0,
    line_amount DECIMAL(18,2) NOT NULL,
    request_date DATETIME NULL,
    promise_date DATETIME NULL,
    actual_shipment_date DATETIME NULL,
    line_status_code VARCHAR(30) NOT NULL,
    ship_from_org_id BIGINT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_oe_order_lines_header_line (header_id, line_number),
    KEY idx_oe_order_lines_header_id (header_id),
    KEY idx_oe_order_lines_item_id (inventory_item_id),
    KEY idx_oe_order_lines_status (line_status_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS WSH_DELIVERY_DETAILS (
    delivery_detail_id BIGINT NOT NULL PRIMARY KEY,
    source_header_id BIGINT NOT NULL,
    source_line_id BIGINT NOT NULL,
    inventory_item_id BIGINT NOT NULL,
    requested_quantity DECIMAL(18,2) NOT NULL,
    shipped_quantity DECIMAL(18,2) NOT NULL DEFAULT 0,
    released_status VARCHAR(30) NOT NULL,
    actual_shipment_date DATETIME NULL,
    delivery_date DATETIME NULL,
    ship_from_org_id BIGINT NULL,
    ship_to_location_id BIGINT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_wsh_delivery_details_source_header (source_header_id),
    KEY idx_wsh_delivery_details_source_line (source_line_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS RA_CUSTOMER_TRX_ALL (
    customer_trx_id BIGINT NOT NULL PRIMARY KEY,
    trx_number VARCHAR(50) NOT NULL,
    trx_date DATETIME NOT NULL,
    sold_to_customer_id BIGINT NOT NULL,
    bill_to_site_use_id BIGINT NULL,
    cust_trx_type VARCHAR(30) NOT NULL,
    currency_code VARCHAR(10) NOT NULL DEFAULT 'CNY',
    trx_amount DECIMAL(18,2) NOT NULL,
    tax_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    freight_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    complete_flag CHAR(1) NOT NULL DEFAULT 'Y',
    status VARCHAR(30) NOT NULL,
    related_order_header_id BIGINT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_ra_customer_trx_all_trx_number (trx_number),
    KEY idx_ra_customer_trx_all_customer_id (sold_to_customer_id),
    KEY idx_ra_customer_trx_all_trx_date (trx_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS RA_CUSTOMER_TRX_LINES_ALL (
    customer_trx_line_id BIGINT NOT NULL PRIMARY KEY,
    customer_trx_id BIGINT NOT NULL,
    line_number INT NOT NULL,
    line_type VARCHAR(30) NOT NULL,
    inventory_item_id BIGINT NULL,
    quantity_invoiced DECIMAL(18,2) NOT NULL DEFAULT 0,
    unit_selling_price DECIMAL(18,2) NOT NULL DEFAULT 0,
    extended_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    tax_amount DECIMAL(18,2) NOT NULL DEFAULT 0,
    related_order_line_id BIGINT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_ra_customer_trx_lines_trx_line (customer_trx_id, line_number),
    KEY idx_ra_customer_trx_lines_trx_id (customer_trx_id),
    KEY idx_ra_customer_trx_lines_order_line (related_order_line_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS INVOICE_ORDER_LINK (
    link_id BIGINT NOT NULL PRIMARY KEY,
    customer_trx_line_id BIGINT NOT NULL,
    order_line_id BIGINT NULL,
    delivery_detail_id BIGINT NULL,
    link_type VARCHAR(30) NOT NULL,
    match_status VARCHAR(20) NOT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_invoice_order_link_trx_line (customer_trx_line_id),
    KEY idx_invoice_order_link_order_line (order_line_id),
    KEY idx_invoice_order_link_delivery_detail (delivery_detail_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS AR_PAYMENT_SCHEDULES_ALL (
    payment_schedule_id BIGINT NOT NULL PRIMARY KEY,
    customer_trx_id BIGINT NOT NULL,
    due_date DATETIME NOT NULL,
    amount_due_original DECIMAL(18,2) NOT NULL,
    amount_due_remaining DECIMAL(18,2) NOT NULL,
    amount_applied DECIMAL(18,2) NOT NULL DEFAULT 0,
    amount_adjusted DECIMAL(18,2) NOT NULL DEFAULT 0,
    aging_bucket VARCHAR(30) NULL,
    overdue_days INT NOT NULL DEFAULT 0,
    status VARCHAR(30) NOT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_ar_payment_schedules_trx_id (customer_trx_id),
    KEY idx_ar_payment_schedules_due_date (due_date),
    KEY idx_ar_payment_schedules_overdue_days (overdue_days)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS AR_CASH_RECEIPTS_ALL (
    cash_receipt_id BIGINT NOT NULL PRIMARY KEY,
    receipt_number VARCHAR(50) NOT NULL,
    receipt_date DATETIME NOT NULL,
    payer_customer_id BIGINT NOT NULL,
    receipt_amount DECIMAL(18,2) NOT NULL,
    currency_code VARCHAR(10) NOT NULL DEFAULT 'CNY',
    receipt_method VARCHAR(30) NOT NULL,
    remittance_bank_account VARCHAR(100) NULL,
    status VARCHAR(30) NOT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    UNIQUE KEY uk_ar_cash_receipts_receipt_number (receipt_number),
    KEY idx_ar_cash_receipts_payer_customer_id (payer_customer_id),
    KEY idx_ar_cash_receipts_receipt_date (receipt_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS AR_RECEIVABLE_APPLICATIONS_ALL (
    receivable_application_id BIGINT NOT NULL PRIMARY KEY,
    cash_receipt_id BIGINT NOT NULL,
    applied_customer_trx_id BIGINT NOT NULL,
    amount_applied DECIMAL(18,2) NOT NULL,
    apply_date DATETIME NOT NULL,
    application_type VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_ar_receivable_apps_cash_receipt_id (cash_receipt_id),
    KEY idx_ar_receivable_apps_customer_trx_id (applied_customer_trx_id),
    KEY idx_ar_receivable_apps_apply_date (apply_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS OE_PRICE_ADJUSTMENTS (
    adjustment_id BIGINT NOT NULL PRIMARY KEY,
    header_id BIGINT NOT NULL,
    line_id BIGINT NULL,
    adjustment_type VARCHAR(30) NOT NULL,
    adjustment_reason VARCHAR(100) NULL,
    list_price DECIMAL(18,2) NOT NULL,
    adjusted_price DECIMAL(18,2) NOT NULL,
    adjustment_amount DECIMAL(18,2) NOT NULL,
    adjustment_percent DECIMAL(8,2) NOT NULL DEFAULT 0,
    approved_flag CHAR(1) NOT NULL DEFAULT 'N',
    approver_id BIGINT NULL,
    approval_time DATETIME NULL,
    created_by BIGINT NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_oe_price_adjustments_header_id (header_id),
    KEY idx_oe_price_adjustments_line_id (line_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS OTC_APPROVAL_LOG (
    approval_log_id BIGINT NOT NULL PRIMARY KEY,
    business_type VARCHAR(30) NOT NULL,
    business_id BIGINT NOT NULL,
    approval_level INT NOT NULL,
    approver_id BIGINT NOT NULL,
    approval_result VARCHAR(20) NOT NULL,
    approval_comment VARCHAR(200) NULL,
    approval_time DATETIME NOT NULL,
    workflow_id VARCHAR(50) NULL,
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_otc_approval_log_business (business_type, business_id),
    KEY idx_otc_approval_log_approver_id (approver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS OTC_FIELD_CHANGE_LOG (
    change_log_id BIGINT NOT NULL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    old_value VARCHAR(200) NULL,
    new_value VARCHAR(200) NULL,
    changed_by BIGINT NOT NULL,
    change_reason VARCHAR(200) NULL,
    change_time DATETIME NOT NULL,
    risk_flag CHAR(1) NOT NULL DEFAULT 'N',
    created_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL,
    KEY idx_otc_field_change_log_table_record (table_name, record_id),
    KEY idx_otc_field_change_log_changed_by (changed_by),
    KEY idx_otc_field_change_log_risk_flag (risk_flag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
