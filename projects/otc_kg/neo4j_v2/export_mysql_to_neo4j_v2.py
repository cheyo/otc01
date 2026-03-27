#!/usr/bin/env python3
import csv
import subprocess
from pathlib import Path

OUT = Path('/root/.openclaw/workspace/projects/otc_kg/neo4j_v2/import')
OUT.mkdir(parents=True, exist_ok=True)
MYSQL = ["mysql", "-N", "-B", "-uroot", "-pvv7g51Hou", "-D", "otc_kg_v2", "-e"]

def fetch(sql):
    res = subprocess.run(MYSQL + [sql], capture_output=True, text=True, check=True)
    lines = [line.split('\t') for line in res.stdout.strip().splitlines() if line.strip()]
    return lines

def write(name, headers, sql):
    rows = fetch(sql)
    with open(OUT / name, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

write('customer_accounts.csv', ['id','name','status','region_code'], "SELECT cust_account_id, account_name, account_status, region_code FROM HZ_CUST_ACCOUNTS")
write('bank_accounts.csv', ['id','bank_name','bank_account_num'], "SELECT bank_account_id, bank_name, bank_account_num FROM CUST_BANK_ACCOUNTS")
write('sales_orders.csv', ['id','order_number','order_amount','flow_status_code'], "SELECT header_id, order_number, order_amount, flow_status_code FROM OE_ORDER_HEADERS_ALL")
write('invoices.csv', ['id','trx_number','trx_amount','status'], "SELECT customer_trx_id, trx_number, trx_amount, status FROM RA_CUSTOMER_TRX_ALL")
write('receipts.csv', ['id','receipt_number','receipt_amount','status'], "SELECT cash_receipt_id, receipt_number, receipt_amount, status FROM AR_CASH_RECEIPTS_ALL")
write('xla_headers.csv', ['id','entity_code','source_id','period_name'], "SELECT ae_header_id, entity_code, source_id, period_name FROM XLA_AE_HEADERS")
write('gl_headers.csv', ['id','je_source_name','je_category_name','period_name','total_dr','total_cr'], "SELECT je_header_id, je_source_name, je_category_name, period_name, total_dr, total_cr FROM GL_JE_HEADERS")
write('gl_accounts.csv', ['id','segment1_company','segment2_department','segment3_account','segment4_product'], "SELECT code_combination_id, segment1_company, segment2_department, segment3_account, segment4_product FROM GL_CODE_COMBINATIONS")
write('gl_balances.csv', ['id','period_name','code_combination_id','end_balance_dr','end_balance_cr'], "SELECT balance_id, period_name, code_combination_id, end_balance_dr, end_balance_cr FROM GL_BALANCES")
write('rel_customer_bank.csv', ['source','target'], "SELECT cust_account_id, bank_account_id FROM CUST_BANK_ACCOUNTS")
write('rel_customer_order.csv', ['source','target'], "SELECT sold_to_org_id, header_id FROM OE_ORDER_HEADERS_ALL")
write('rel_order_invoice.csv', ['source','target'], "SELECT DISTINCT iol.header_id, rctl.customer_trx_id FROM INVOICE_ORDER_LINK iol JOIN RA_CUSTOMER_TRX_LINES_ALL rctl ON iol.customer_trx_line_id=rctl.customer_trx_line_id")
write('rel_customer_receipt.csv', ['source','target'], "SELECT payer_customer_id, cash_receipt_id FROM AR_CASH_RECEIPTS_ALL")
write('rel_receipt_invoice.csv', ['source','target'], "SELECT cash_receipt_id, applied_customer_trx_id FROM AR_RECEIVABLE_APPLICATIONS_ALL")
write('rel_invoice_xla.csv', ['source','target'], "SELECT source_id, ae_header_id FROM XLA_AE_HEADERS WHERE entity_code='RA_CUSTOMER_TRX'")
write('rel_xla_gl.csv', ['source','target'], "SELECT DISTINCT ae_header_id, je_header_id FROM GL_IMPORT_REFERENCES WHERE ae_header_id IS NOT NULL")
write('rel_glheader_gllineacct.csv', ['source','target'], "SELECT DISTINCT je_header_id, code_combination_id FROM GL_JE_LINES")
write('rel_glacct_balance.csv', ['source','target'], "SELECT code_combination_id, balance_id FROM GL_BALANCES")
print('v2 export complete')
