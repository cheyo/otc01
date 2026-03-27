#!/usr/bin/env python3
import csv
from pathlib import Path
import mysql.connector

MYSQL = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'vv7g51Hou',
    'database': 'otc_kg',
}
OUT = Path('/root/.openclaw/workspace/projects/otc_kg/neo4j/import')
OUT.mkdir(parents=True, exist_ok=True)

conn = mysql.connector.connect(**MYSQL)
cur = conn.cursor(dictionary=True)

def dump_query(name, query, headers):
    cur.execute(query)
    rows = cur.fetchall()
    with open(OUT / f'{name}.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for r in rows:
            w.writerow([r.get(h, '') for h in headers])
    print(name, len(rows))

# nodes

dump_query('nodes_customer_party',
           "SELECT party_id, party_name, party_type, tax_reference, industry_code, customer_size, risk_level, province, city, status FROM HZ_PARTIES",
           ['party_id','party_name','party_type','tax_reference','industry_code','customer_size','risk_level','province','city','status'])

dump_query('nodes_customer_account',
           "SELECT cust_account_id, party_id, account_number, account_name, payment_term_code, region_code, account_status FROM HZ_CUST_ACCOUNTS",
           ['cust_account_id','party_id','account_number','account_name','payment_term_code','region_code','account_status'])

dump_query('nodes_address',
           "SELECT location_id, province_name, city_name, district_name, address_line1, postal_code FROM HZ_LOCATIONS",
           ['location_id','province_name','city_name','district_name','address_line1','postal_code'])

dump_query('nodes_bank_account',
           "SELECT bank_account_id, bank_name, branch_name, bank_account_num, account_name, account_type, status FROM CUST_BANK_ACCOUNTS",
           ['bank_account_id','bank_name','branch_name','bank_account_num','account_name','account_type','status'])

dump_query('nodes_credit_profile',
           "SELECT credit_profile_id, cust_account_id, credit_limit, currency_code, payment_terms, risk_level, risk_score, credit_hold_flag, status FROM CUST_CREDIT_PROFILES",
           ['credit_profile_id','cust_account_id','credit_limit','currency_code','payment_terms','risk_level','risk_score','credit_hold_flag','status'])

dump_query('nodes_sales_order',
           "SELECT header_id, order_number, sold_to_org_id, order_date, booked_date, order_amount, discount_amount, tax_amount, flow_status_code, salesrep_id FROM OE_ORDER_HEADERS_ALL",
           ['header_id','order_number','sold_to_org_id','order_date','booked_date','order_amount','discount_amount','tax_amount','flow_status_code','salesrep_id'])

dump_query('nodes_sales_order_line',
           "SELECT line_id, header_id, line_number, inventory_item_id, ordered_quantity, unit_selling_price, list_price, discount_percent, line_amount, line_status_code FROM OE_ORDER_LINES_ALL",
           ['line_id','header_id','line_number','inventory_item_id','ordered_quantity','unit_selling_price','list_price','discount_percent','line_amount','line_status_code'])

dump_query('nodes_delivery_detail',
           "SELECT delivery_detail_id, source_header_id, source_line_id, inventory_item_id, requested_quantity, shipped_quantity, released_status, actual_shipment_date FROM WSH_DELIVERY_DETAILS",
           ['delivery_detail_id','source_header_id','source_line_id','inventory_item_id','requested_quantity','shipped_quantity','released_status','actual_shipment_date'])

dump_query('nodes_invoice',
           "SELECT customer_trx_id, trx_number, trx_date, sold_to_customer_id, cust_trx_type, trx_amount, tax_amount, status FROM RA_CUSTOMER_TRX_ALL",
           ['customer_trx_id','trx_number','trx_date','sold_to_customer_id','cust_trx_type','trx_amount','tax_amount','status'])

dump_query('nodes_invoice_line',
           "SELECT customer_trx_line_id, customer_trx_id, line_number, line_type, inventory_item_id, quantity_invoiced, unit_selling_price, extended_amount, tax_amount FROM RA_CUSTOMER_TRX_LINES_ALL",
           ['customer_trx_line_id','customer_trx_id','line_number','line_type','inventory_item_id','quantity_invoiced','unit_selling_price','extended_amount','tax_amount'])

dump_query('nodes_payment_schedule',
           "SELECT payment_schedule_id, customer_trx_id, due_date, amount_due_original, amount_due_remaining, amount_applied, overdue_days, aging_bucket, status FROM AR_PAYMENT_SCHEDULES_ALL",
           ['payment_schedule_id','customer_trx_id','due_date','amount_due_original','amount_due_remaining','amount_applied','overdue_days','aging_bucket','status'])

dump_query('nodes_cash_receipt',
           "SELECT cash_receipt_id, receipt_number, receipt_date, payer_customer_id, receipt_amount, receipt_method, remittance_bank_account, status FROM AR_CASH_RECEIPTS_ALL",
           ['cash_receipt_id','receipt_number','receipt_date','payer_customer_id','receipt_amount','receipt_method','remittance_bank_account','status'])

dump_query('nodes_employee',
           "SELECT employee_id, employee_no, employee_name, department_name, role_code, title_name, region_code, status FROM HR_EMPLOYEES",
           ['employee_id','employee_no','employee_name','department_name','role_code','title_name','region_code','status'])

# relations

dump_query('rels_has_account',
           "SELECT party_id AS src, cust_account_id AS dst FROM HZ_CUST_ACCOUNTS",
           ['src','dst'])

dump_query('rels_located_at',
           "SELECT s.cust_account_id AS src, s.location_id AS dst FROM HZ_CUST_ACCT_SITES_ALL s",
           ['src','dst'])

dump_query('rels_uses_bank_account',
           "SELECT cust_account_id AS src, bank_account_id AS dst FROM CUST_BANK_ACCOUNTS",
           ['src','dst'])

dump_query('rels_has_credit_profile',
           "SELECT cust_account_id AS src, credit_profile_id AS dst FROM CUST_CREDIT_PROFILES",
           ['src','dst'])

dump_query('rels_placed_order',
           "SELECT sold_to_org_id AS src, header_id AS dst FROM OE_ORDER_HEADERS_ALL",
           ['src','dst'])

dump_query('rels_order_has_line',
           "SELECT header_id AS src, line_id AS dst FROM OE_ORDER_LINES_ALL",
           ['src','dst'])

dump_query('rels_fulfilled_by',
           "SELECT source_line_id AS src, delivery_detail_id AS dst FROM WSH_DELIVERY_DETAILS",
           ['src','dst'])

dump_query('rels_billed_as',
           "SELECT sold_to_customer_id AS src, customer_trx_id AS dst FROM RA_CUSTOMER_TRX_ALL",
           ['src','dst'])

dump_query('rels_invoice_has_line',
           "SELECT customer_trx_id AS src, customer_trx_line_id AS dst FROM RA_CUSTOMER_TRX_LINES_ALL",
           ['src','dst'])

dump_query('rels_generated_from_order_line',
           "SELECT customer_trx_line_id AS src, order_line_id AS dst FROM INVOICE_ORDER_LINK WHERE order_line_id IS NOT NULL",
           ['src','dst'])

dump_query('rels_generated_from_delivery',
           "SELECT customer_trx_line_id AS src, delivery_detail_id AS dst FROM INVOICE_ORDER_LINK WHERE delivery_detail_id IS NOT NULL",
           ['src','dst'])

dump_query('rels_generates_ar',
           "SELECT customer_trx_id AS src, payment_schedule_id AS dst FROM AR_PAYMENT_SCHEDULES_ALL",
           ['src','dst'])

dump_query('rels_made_payment',
           "SELECT payer_customer_id AS src, cash_receipt_id AS dst FROM AR_CASH_RECEIPTS_ALL",
           ['src','dst'])

dump_query('rels_applied_to',
           "SELECT cash_receipt_id AS src, applied_customer_trx_id AS dst, amount_applied, apply_date, status FROM AR_RECEIVABLE_APPLICATIONS_ALL",
           ['src','dst','amount_applied','apply_date','status'])

dump_query('rels_approved_order',
           "SELECT approver_id AS src, business_id AS dst FROM OTC_APPROVAL_LOG WHERE business_type='ORDER'",
           ['src','dst'])

dump_query('rels_shares_bank_account_with',
           "SELECT a1.cust_account_id AS src, a2.cust_account_id AS dst FROM CUST_BANK_ACCOUNTS a1 JOIN CUST_BANK_ACCOUNTS a2 ON a1.bank_account_num = a2.bank_account_num AND a1.cust_account_id < a2.cust_account_id",
           ['src','dst'])

cur.close()
conn.close()
print('done')
