USE otc_kg;
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE HZ_PARTIES;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/HZ_PARTIES.csv' INTO TABLE HZ_PARTIES CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`party_id`,`party_number`,`party_name`,`party_type`,`tax_reference`,`country_code`,`province`,`city`,`industry_code`,`customer_size`,`risk_level`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE HZ_LOCATIONS;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/HZ_LOCATIONS.csv' INTO TABLE HZ_LOCATIONS CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`location_id`,`country_code`,`province_name`,`city_name`,`district_name`,`address_line1`,`postal_code`,`created_date`,`last_update_date`);
TRUNCATE TABLE HZ_CUST_ACCOUNTS;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/HZ_CUST_ACCOUNTS.csv' INTO TABLE HZ_CUST_ACCOUNTS CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`cust_account_id`,`party_id`,`account_number`,`account_name`,`customer_class_code`,`credit_classification`,`payment_term_code`,`sales_channel_code`,`region_code`,`account_status`,`open_date`,`created_date`,`last_update_date`);
TRUNCATE TABLE HZ_CUST_ACCT_SITES_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/HZ_CUST_ACCT_SITES_ALL.csv' INTO TABLE HZ_CUST_ACCT_SITES_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`cust_acct_site_id`,`cust_account_id`,`location_id`,`site_code`,`org_id`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE HZ_CUST_SITE_USES_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/HZ_CUST_SITE_USES_ALL.csv' INTO TABLE HZ_CUST_SITE_USES_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`site_use_id`,`cust_acct_site_id`,`site_use_code`,`primary_flag`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE CUST_BANK_ACCOUNTS;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/CUST_BANK_ACCOUNTS.csv' INTO TABLE CUST_BANK_ACCOUNTS CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`bank_account_id`,`cust_account_id`,`bank_name`,`branch_name`,`bank_account_num`,`account_name`,`account_type`,`is_primary`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE CUST_CREDIT_PROFILES;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/CUST_CREDIT_PROFILES.csv' INTO TABLE CUST_CREDIT_PROFILES CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`credit_profile_id`,`cust_account_id`,`credit_limit`,`currency_code`,`payment_terms`,`risk_level`,`risk_score`,`overdue_tolerance_days`,`credit_hold_flag`,`review_date`,`effective_start_date`,`effective_end_date`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE HR_EMPLOYEES;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/HR_EMPLOYEES.csv' INTO TABLE HR_EMPLOYEES CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`employee_id`,`employee_no`,`employee_name`,`gender`,`department_name`,`role_code`,`title_name`,`manager_id`,`region_code`,`hire_date`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE OE_ORDER_HEADERS_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/OE_ORDER_HEADERS_ALL.csv' INTO TABLE OE_ORDER_HEADERS_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`header_id`,`order_number`,`sold_to_org_id`,`ship_to_site_use_id`,`invoice_to_site_use_id`,`order_date`,`booked_date`,`order_type_code`,`order_currency_code`,`transactional_curr_code`,`order_amount`,`discount_amount`,`tax_amount`,`booked_flag`,`cancelled_flag`,`flow_status_code`,`salesrep_id`,`org_id`,`created_date`,`last_update_date`);
TRUNCATE TABLE OE_ORDER_LINES_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/OE_ORDER_LINES_ALL.csv' INTO TABLE OE_ORDER_LINES_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`line_id`,`header_id`,`line_number`,`inventory_item_id`,`ordered_quantity`,`unit_selling_price`,`list_price`,`discount_percent`,`line_amount`,`request_date`,`promise_date`,`actual_shipment_date`,`line_status_code`,`ship_from_org_id`,`created_date`,`last_update_date`);
TRUNCATE TABLE WSH_DELIVERY_DETAILS;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/WSH_DELIVERY_DETAILS.csv' INTO TABLE WSH_DELIVERY_DETAILS CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`delivery_detail_id`,`source_header_id`,`source_line_id`,`inventory_item_id`,`requested_quantity`,`shipped_quantity`,`released_status`,`actual_shipment_date`,`delivery_date`,`ship_from_org_id`,`ship_to_location_id`,`created_date`,`last_update_date`);
TRUNCATE TABLE RA_CUSTOMER_TRX_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/RA_CUSTOMER_TRX_ALL.csv' INTO TABLE RA_CUSTOMER_TRX_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`customer_trx_id`,`trx_number`,`trx_date`,`sold_to_customer_id`,`bill_to_site_use_id`,`cust_trx_type`,`currency_code`,`trx_amount`,`tax_amount`,`freight_amount`,`complete_flag`,`status`,`related_order_header_id`,`created_date`,`last_update_date`);
TRUNCATE TABLE RA_CUSTOMER_TRX_LINES_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/RA_CUSTOMER_TRX_LINES_ALL.csv' INTO TABLE RA_CUSTOMER_TRX_LINES_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`customer_trx_line_id`,`customer_trx_id`,`line_number`,`line_type`,`inventory_item_id`,`quantity_invoiced`,`unit_selling_price`,`extended_amount`,`tax_amount`,`related_order_line_id`,`created_date`,`last_update_date`);
TRUNCATE TABLE INVOICE_ORDER_LINK;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/INVOICE_ORDER_LINK.csv' INTO TABLE INVOICE_ORDER_LINK CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`link_id`,`customer_trx_line_id`,`order_line_id`,`delivery_detail_id`,`link_type`,`match_status`,`created_date`,`last_update_date`);
TRUNCATE TABLE AR_PAYMENT_SCHEDULES_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/AR_PAYMENT_SCHEDULES_ALL.csv' INTO TABLE AR_PAYMENT_SCHEDULES_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`payment_schedule_id`,`customer_trx_id`,`due_date`,`amount_due_original`,`amount_due_remaining`,`amount_applied`,`amount_adjusted`,`aging_bucket`,`overdue_days`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE AR_CASH_RECEIPTS_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/AR_CASH_RECEIPTS_ALL.csv' INTO TABLE AR_CASH_RECEIPTS_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`cash_receipt_id`,`receipt_number`,`receipt_date`,`payer_customer_id`,`receipt_amount`,`currency_code`,`receipt_method`,`remittance_bank_account`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE AR_RECEIVABLE_APPLICATIONS_ALL;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/AR_RECEIVABLE_APPLICATIONS_ALL.csv' INTO TABLE AR_RECEIVABLE_APPLICATIONS_ALL CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`receivable_application_id`,`cash_receipt_id`,`applied_customer_trx_id`,`amount_applied`,`apply_date`,`application_type`,`status`,`created_date`,`last_update_date`);
TRUNCATE TABLE OE_PRICE_ADJUSTMENTS;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/OE_PRICE_ADJUSTMENTS.csv' INTO TABLE OE_PRICE_ADJUSTMENTS CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`adjustment_id`,`header_id`,`line_id`,`adjustment_type`,`adjustment_reason`,`list_price`,`adjusted_price`,`adjustment_amount`,`adjustment_percent`,`approved_flag`,`approver_id`,`approval_time`,`created_by`,`created_date`,`last_update_date`);
TRUNCATE TABLE OTC_APPROVAL_LOG;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/OTC_APPROVAL_LOG.csv' INTO TABLE OTC_APPROVAL_LOG CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`approval_log_id`,`business_type`,`business_id`,`approval_level`,`approver_id`,`approval_result`,`approval_comment`,`approval_time`,`workflow_id`,`created_date`,`last_update_date`);
TRUNCATE TABLE OTC_FIELD_CHANGE_LOG;
LOAD DATA LOCAL INFILE '/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv/OTC_FIELD_CHANGE_LOG.csv' INTO TABLE OTC_FIELD_CHANGE_LOG CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '
' IGNORE 1 LINES (`change_log_id`,`table_name`,`record_id`,`field_name`,`old_value`,`new_value`,`changed_by`,`change_reason`,`change_time`,`risk_flag`,`created_date`,`last_update_date`);
SET FOREIGN_KEY_CHECKS=1;
