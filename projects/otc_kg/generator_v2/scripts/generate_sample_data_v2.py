#!/usr/bin/env python3
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUT = Path('/root/.openclaw/workspace/projects/otc_kg/generator_v2/output/sample_csv_v2')
OUT.mkdir(parents=True, exist_ok=True)
random.seed(20260327)

COUNTRIES = ['CN']
PROVINCES = ['北京', '上海', '广东', '江苏', '浙江', '四川']
CITIES = ['北京', '上海', '深圳', '广州', '苏州', '杭州', '成都']
BANKS = ['工商银行', '建设银行', '农业银行', '招商银行', '中国银行']
DEPTS = ['销售部', '财务部', '风控部', '供应链部']
ITEM_TYPES = ['FG', 'RM', 'SERVICE']
PAY_TERMS = ['NET30', 'NET60', 'NET90', 'PREPAID']
RISK_LEVELS = ['LOW', 'MEDIUM', 'HIGH']
TRX_TYPES = [('INV_STANDARD', 'INV'), ('INV_EXPORT', 'INV'), ('CM_STANDARD', 'CM')]
RECEIPT_METHODS = [('BANK_TRANSFER', 'BANK'), ('CHEQUE', 'OFFLINE'), ('LOCKBOX', 'AUTO')]


def write_csv(name, rows, headers):
    with open(OUT / f'{name}.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)

# master data
parties = []
locations = []
accounts = []
sites = []
site_uses = []
bank_accounts = []
credit_profiles = []
orgs = []
employees = []
salesreps = []
inv_orgs = []
items = []
trx_types_rows = []
batch_sources = []
receipt_methods_rows = []
gl_ledgers = []
gl_periods = []
gl_ccids = []

for i in range(1, 6):
    orgs.append({'org_id': i, 'org_code': f'OU{i:03d}', 'org_name': f'中国业务单元{i}', 'legal_entity_name': '示例集团', 'country_code': 'CN'})
    inv_orgs.append({'inventory_org_id': i, 'org_code': f'INV{i:03d}', 'org_name': f'库存组织{i}', 'org_type': 'WAREHOUSE'})

for i in range(1, 61):
    employees.append({'employee_id': i, 'employee_name': f'员工{i:03d}', 'department_name': random.choice(DEPTS), 'role_code': random.choice(['SALES','FIN','RISK','OPS']), 'org_id': random.randint(1,5), 'manager_id': '', 'status': 'ACTIVE'})
for i in range(1, 31):
    salesreps.append({'salesrep_id': i, 'employee_id': i, 'salesrep_number': f'SR{i:03d}', 'salesrep_name': f'销售{i:03d}', 'org_id': random.randint(1,5), 'status': 'ACTIVE'})
for i in range(1, 201):
    items.append({'inventory_item_id': i, 'organization_id': random.randint(1,5), 'item_number': f'ITEM{i:05d}', 'item_description': f'商品{i:05d}', 'item_type': random.choice(ITEM_TYPES), 'uom_code': 'EA', 'list_price': round(random.uniform(50, 2000), 2), 'active_flag': 'Y'})

for i in range(1, 4):
    batch_sources.append({'batch_source_id': i, 'source_name': f'来源{i}', 'source_type': 'MANUAL'})
for i, (name, cls) in enumerate(TRX_TYPES, 1):
    trx_types_rows.append({'cust_trx_type_id': i, 'trx_type_name': name, 'trx_class': cls, 'accounting_affect_flag': 'Y'})
for i, (name, t) in enumerate(RECEIPT_METHODS, 1):
    receipt_methods_rows.append({'receipt_method_id': i, 'receipt_method_name': name, 'method_type': t})

ledger_id = 1
gl_ledgers.append({'ledger_id': ledger_id, 'ledger_name': '中国主账簿', 'currency_code': 'CNY', 'calendar_name': 'Monthly', 'chart_of_accounts_name': '中国会计科目表'})
start = datetime(2025, 1, 1)
for i in range(12):
    dt = start + timedelta(days=30*i)
    gl_periods.append({'period_name': f'{dt.year}-{dt.month:02d}', 'period_year': dt.year, 'period_num': dt.month, 'start_date': f'{dt.year}-{dt.month:02d}-01', 'end_date': f'{dt.year}-{dt.month:02d}-28', 'status': 'OPEN'})
accounts_coa = [('1001','现金'), ('1122','应收账款'), ('6001','主营业务收入'), ('2221','应交税费'), ('1405','库存商品')]
for i, (acct, _) in enumerate(accounts_coa, 1):
    gl_ccids.append({'code_combination_id': i, 'segment1_company': '100', 'segment2_department': f'{10+i}', 'segment3_account': acct, 'segment4_product': '000', 'segment5_intercompany': '000', 'enabled_flag': 'Y'})

for i in range(1, 101):
    pid = 100000 + i
    aid = 300000 + i
    lid = 500000 + i
    site_id = 600000 + i
    parties.append({'party_id': pid, 'party_name': f'{random.choice(CITIES)}示例客户{i:03d}有限公司', 'party_type': 'ORGANIZATION', 'tax_reference': f'TAX{i:08d}', 'industry_code': random.choice(['MFG','TRADE','MED','TECH']), 'risk_level': random.choice(RISK_LEVELS), 'province': random.choice(PROVINCES), 'city': random.choice(CITIES), 'created_at': '2025-01-01 00:00:00'})
    locations.append({'location_id': lid, 'country': 'CN', 'province_name': random.choice(PROVINCES), 'city_name': random.choice(CITIES), 'district_name': f'区{i%10}', 'address_line1': f'示例路{i}号', 'postal_code': f'{200000+i:06d}'})
    accounts.append({'cust_account_id': aid, 'party_id': pid, 'account_number': f'CUST{aid}', 'account_name': f'{random.choice(CITIES)}示例客户{i:03d}有限公司', 'account_status': 'ACTIVE', 'payment_term_code': random.choice(PAY_TERMS), 'region_code': random.choice(CITIES), 'created_at': '2025-01-01 00:00:00'})
    sites.append({'cust_acct_site_id': site_id, 'cust_account_id': aid, 'location_id': lid, 'site_code': f'SITE{site_id}', 'status': 'ACTIVE'})
    site_uses.append({'site_use_id': site_id*10+1, 'cust_acct_site_id': site_id, 'site_use_code': 'BILL_TO', 'primary_flag': 'Y', 'status': 'ACTIVE'})
    site_uses.append({'site_use_id': site_id*10+2, 'cust_acct_site_id': site_id, 'site_use_code': 'SHIP_TO', 'primary_flag': 'Y', 'status': 'ACTIVE'})
    bank_accounts.append({'bank_account_id': 700000+i, 'cust_account_id': aid, 'bank_name': random.choice(BANKS), 'bank_account_num': f'6222{random.randint(10000000,99999999)}', 'account_holder_name': f'示例客户{i:03d}', 'bank_branch_name': f'{random.choice(CITIES)}分行', 'active_flag': 'Y'})
    credit_profiles.append({'credit_profile_id': 800000+i, 'cust_account_id': aid, 'credit_limit': round(random.uniform(50000,500000),2), 'currency_code': 'CNY', 'risk_level': random.choice(RISK_LEVELS), 'risk_score': round(random.uniform(40,95),2), 'credit_checking': 'Y', 'review_date': '2025-12-31'})

# transactions
order_headers = []
order_lines = []
holds = []
price_adjustments = []
deliveries = []
delivery_details = []
delivery_assignments = []
trx_headers = []
trx_lines = []
invoice_links = []
tax_lines = []
payment_schedules = []
cash_receipts = []
applications = []
xla_headers = []
xla_lines = []
xla_links = []
gl_headers = []
gl_lines = []
gl_import_refs = []
gl_balances = []

order_id = line_id = delivery_id = dd_id = trx_id = trx_line_id = ps_id = cash_id = app_id = xh = xl = ghj = gjl = gir = tax_id = 1
for i in range(1, 201):
    cust = random.choice(accounts)
    order_amt = 0
    order_date = datetime(2025, random.randint(1, 12), random.randint(1, 25), 10, 0, 0)
    order_headers.append({'header_id': order_id, 'order_number': f'SO{order_id:06d}', 'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'), 'sold_to_org_id': cust['cust_account_id'], 'ship_to_org_id': cust['cust_account_id'], 'bill_to_org_id': cust['cust_account_id'], 'org_id': random.randint(1,5), 'salesrep_id': random.randint(1,30), 'transaction_type_id': 1, 'currency_code': 'CNY', 'order_amount': 0, 'flow_status_code': 'BOOKED', 'order_type_code': 'STANDARD', 'approval_status': 'APPROVED'})
    if random.random() < 0.08:
        holds.append({'hold_id': i, 'header_id': order_id, 'line_id': '', 'hold_type_code': 'CREDIT_HOLD', 'hold_reason': '信用额度校验', 'released_flag': random.choice(['Y','N']), 'hold_date': order_date.strftime('%Y-%m-%d %H:%M:%S'), 'release_date': ''})
    delivery_id += 1
    deliveries.append({'delivery_id': delivery_id, 'delivery_name': f'DEL{delivery_id:06d}', 'organization_id': random.randint(1,5), 'status_code': 'CLOSED', 'initial_pickup_date': order_date.strftime('%Y-%m-%d %H:%M:%S'), 'ultimate_dropoff_date': (order_date + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')})
    for ln in range(1, random.randint(2, 4)):
        item = random.choice(items)
        qty = random.randint(1, 20)
        price = float(item['list_price'])
        discount = random.choice([0, 5, 10, 15, 25])
        line_amt = round(qty * price * (1 - discount/100), 2)
        order_amt += line_amt
        order_lines.append({'line_id': line_id, 'header_id': order_id, 'line_number': ln, 'inventory_item_id': item['inventory_item_id'], 'inventory_org_id': item['organization_id'], 'ordered_quantity': qty, 'unit_selling_price': price, 'line_amount': line_amt, 'discount_percent': discount, 'request_date': order_date.date().isoformat(), 'promise_date': (order_date + timedelta(days=3)).date().isoformat(), 'flow_status_code': 'AWAITING_SHIPPING'})
        if discount >= 20:
            price_adjustments.append({'adjustment_id': len(price_adjustments)+1, 'header_id': order_id, 'line_id': line_id, 'adjustment_type_code': 'DISCOUNT', 'adjustment_percent': discount, 'adjustment_amount': round(qty*price*discount/100,2), 'reason_code': 'PROMO', 'approved_flag': 'Y', 'approver_id': random.randint(1,60)})
        dd_id += 1
        delivery_details.append({'delivery_detail_id': dd_id, 'source_header_id': order_id, 'source_line_id': line_id, 'delivery_id': delivery_id, 'inventory_item_id': item['inventory_item_id'], 'shipped_quantity': qty, 'requested_quantity': qty, 'released_status': 'C', 'actual_shipment_date': (order_date + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S')})
        delivery_assignments.append({'assignment_id': len(delivery_assignments)+1, 'delivery_id': delivery_id, 'delivery_detail_id': dd_id, 'assigned_date': (order_date + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')})
        trx_headers.append({'customer_trx_id': trx_id, 'trx_number': f'INV{trx_id:06d}', 'trx_date': (order_date + timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S'), 'sold_to_customer_id': cust['cust_account_id'], 'bill_to_customer_id': cust['cust_account_id'], 'batch_source_id': 1, 'cust_trx_type_id': 1, 'org_id': random.randint(1,5), 'currency_code': 'CNY', 'trx_amount': line_amt, 'status': 'OPEN'})
        trx_lines.append({'customer_trx_line_id': trx_line_id, 'customer_trx_id': trx_id, 'line_number': 1, 'inventory_item_id': item['inventory_item_id'], 'quantity_invoiced': qty, 'unit_selling_price': round(price*(1-discount/100),2), 'extended_amount': line_amt, 'line_type': 'LINE'})
        invoice_links.append({'link_id': len(invoice_links)+1, 'customer_trx_line_id': trx_line_id, 'order_line_id': line_id, 'delivery_detail_id': dd_id, 'header_id': order_id})
        tax_amt = round(line_amt * 0.13, 2)
        tax_lines.append({'tax_line_id': tax_id, 'customer_trx_id': trx_id, 'customer_trx_line_id': trx_line_id, 'tax_type_code': 'VAT', 'tax_rate': 0.13, 'taxable_amount': line_amt, 'tax_amount': tax_amt})
        overdue = random.choice([0, 0, 15, 45, 90, 120])
        due_date = order_date + timedelta(days=30)
        payment_schedules.append({'payment_schedule_id': ps_id, 'customer_trx_id': trx_id, 'due_date': due_date.date().isoformat(), 'amount_due_original': line_amt + tax_amt, 'amount_due_remaining': 0 if overdue == 0 else line_amt + tax_amt, 'amount_applied': line_amt + tax_amt if overdue == 0 else 0, 'status': 'CLOSED' if overdue == 0 else 'OPEN', 'overdue_days': overdue})
        cash_receipts.append({'cash_receipt_id': cash_id, 'receipt_number': f'RCPT{cash_id:06d}', 'receipt_date': (due_date + timedelta(days=max(overdue,0))).strftime('%Y-%m-%d %H:%M:%S'), 'payer_customer_id': cust['cust_account_id'], 'receipt_method_id': 1, 'ce_bank_account_id': '', 'receipt_amount': line_amt + tax_amt, 'status': 'CLEARED'})
        applications.append({'receivable_application_id': app_id, 'cash_receipt_id': cash_id, 'applied_customer_trx_id': trx_id, 'payment_schedule_id': ps_id, 'amount_applied': line_amt + tax_amt, 'application_date': (due_date + timedelta(days=max(overdue,0))).strftime('%Y-%m-%d %H:%M:%S'), 'status': 'APP'})
        period = f"{order_date.year}-{order_date.month:02d}"
        xla_headers.append({'ae_header_id': xh, 'application_id': 222, 'entity_code': 'RA_CUSTOMER_TRX', 'source_id': trx_id, 'accounting_date': order_date.date().isoformat(), 'period_name': period, 'ledger_id': 1, 'accounting_status': 'FINAL'})
        xla_lines.append({'ae_line_id': xl, 'ae_header_id': xh, 'line_num': 1, 'code_combination_id': 2, 'entered_dr': line_amt + tax_amt, 'entered_cr': 0, 'accounted_dr': line_amt + tax_amt, 'accounted_cr': 0, 'description': f'应收发票 {trx_id}'})
        xl += 1
        xla_lines.append({'ae_line_id': xl, 'ae_header_id': xh, 'line_num': 2, 'code_combination_id': 3, 'entered_dr': 0, 'entered_cr': line_amt, 'accounted_dr': 0, 'accounted_cr': line_amt, 'description': f'收入 {trx_id}'})
        xl += 1
        xla_lines.append({'ae_line_id': xl, 'ae_header_id': xh, 'line_num': 3, 'code_combination_id': 4, 'entered_dr': 0, 'entered_cr': tax_amt, 'accounted_dr': 0, 'accounted_cr': tax_amt, 'description': f'税额 {trx_id}'})
        xla_links.append({'distribution_link_id': len(xla_links)+1, 'ae_header_id': xh, 'ae_line_id': xl-2, 'source_distribution_type': 'RA_CUST_TRX_LINE_GL_DIST', 'source_distribution_id': trx_line_id, 'source_trx_id': trx_id})
        ghj += 1
        gl_headers.append({'je_header_id': ghj, 'ledger_id': 1, 'period_name': period, 'je_source_name': 'Receivables', 'je_category_name': 'Sales', 'accounting_date': order_date.date().isoformat(), 'currency_code': 'CNY', 'status': 'P', 'total_dr': line_amt + tax_amt, 'total_cr': line_amt + tax_amt})
        for ccid, dr, cr, desc in [(2, line_amt+tax_amt, 0, '应收账款'), (3, 0, line_amt, '主营业务收入'), (4, 0, tax_amt, '销项税额')]:
            gjl += 1
            gl_lines.append({'je_line_id': gjl, 'je_header_id': ghj, 'line_num': gjl, 'code_combination_id': ccid, 'entered_dr': dr, 'entered_cr': cr, 'accounted_dr': dr, 'accounted_cr': cr, 'description': desc})
            gl_import_refs.append({'import_reference_id': gir+1, 'je_header_id': ghj, 'je_line_id': gjl, 'ae_header_id': xh, 'ae_line_id': xl-2, 'reference_table_name': 'RA_CUSTOMER_TRX_ALL', 'reference_id': trx_id})
            gir += 1
        tax_id += 1
        trx_id += 1
        trx_line_id += 1
        ps_id += 1
        cash_id += 1
        app_id += 1
        xh += 1
        line_id += 1
    order_headers[-1]['order_amount'] = round(order_amt,2)
    order_id += 1

for idx, cc in enumerate(gl_ccids, 1):
    gl_balances.append({'balance_id': idx, 'ledger_id': 1, 'period_name': '2025-12', 'code_combination_id': cc['code_combination_id'], 'begin_balance_dr': 0, 'begin_balance_cr': 0, 'period_net_dr': round(random.uniform(10000,50000),2), 'period_net_cr': round(random.uniform(10000,50000),2), 'end_balance_dr': round(random.uniform(1000,30000),2), 'end_balance_cr': round(random.uniform(1000,30000),2)})

files = {
 'HZ_PARTIES': (parties, list(parties[0].keys())),
 'HZ_LOCATIONS': (locations, list(locations[0].keys())),
 'HZ_CUST_ACCOUNTS': (accounts, list(accounts[0].keys())),
 'HZ_CUST_ACCT_SITES_ALL': (sites, list(sites[0].keys())),
 'HZ_CUST_SITE_USES_ALL': (site_uses, list(site_uses[0].keys())),
 'CUST_BANK_ACCOUNTS': (bank_accounts, list(bank_accounts[0].keys())),
 'CUST_CREDIT_PROFILES': (credit_profiles, list(credit_profiles[0].keys())),
 'HR_OPERATING_UNITS': (orgs, list(orgs[0].keys())),
 'HR_EMPLOYEES': (employees, list(employees[0].keys())),
 'RA_SALESREPS_ALL': (salesreps, list(salesreps[0].keys())),
 'INV_ORGANIZATION_UNITS': (inv_orgs, list(inv_orgs[0].keys())),
 'MTL_SYSTEM_ITEMS_B': (items, list(items[0].keys())),
 'OE_TRANSACTION_TYPES_ALL': ([{'transaction_type_id':1,'transaction_type_code':'STD','transaction_type_name':'标准销售订单','category_code':'ORDER'}], ['transaction_type_id','transaction_type_code','transaction_type_name','category_code']),
 'OE_ORDER_HEADERS_ALL': (order_headers, list(order_headers[0].keys())),
 'OE_ORDER_LINES_ALL': (order_lines, list(order_lines[0].keys())),
 'OE_ORDER_HOLDS_ALL': (holds if holds else [{'hold_id':'','header_id':'','line_id':'','hold_type_code':'','hold_reason':'','released_flag':'','hold_date':'','release_date':''}], ['hold_id','header_id','line_id','hold_type_code','hold_reason','released_flag','hold_date','release_date']),
 'OE_PRICE_ADJUSTMENTS': (price_adjustments if price_adjustments else [{'adjustment_id':'','header_id':'','line_id':'','adjustment_type_code':'','adjustment_percent':'','adjustment_amount':'','reason_code':'','approved_flag':'','approver_id':''}], ['adjustment_id','header_id','line_id','adjustment_type_code','adjustment_percent','adjustment_amount','reason_code','approved_flag','approver_id']),
 'WSH_NEW_DELIVERIES': (deliveries, list(deliveries[0].keys())),
 'WSH_DELIVERY_DETAILS': (delivery_details, list(delivery_details[0].keys())),
 'WSH_DELIVERY_ASSIGNMENTS': (delivery_assignments, list(delivery_assignments[0].keys())),
 'RA_BATCH_SOURCES_ALL': (batch_sources, list(batch_sources[0].keys())),
 'RA_CUST_TRX_TYPES_ALL': (trx_types_rows, list(trx_types_rows[0].keys())),
 'RA_CUSTOMER_TRX_ALL': (trx_headers, list(trx_headers[0].keys())),
 'RA_CUSTOMER_TRX_LINES_ALL': (trx_lines, list(trx_lines[0].keys())),
 'INVOICE_ORDER_LINK': (invoice_links, list(invoice_links[0].keys())),
 'ZX_TAX_LINES': (tax_lines, list(tax_lines[0].keys())),
 'AR_PAYMENT_SCHEDULES_ALL': (payment_schedules, list(payment_schedules[0].keys())),
 'AR_RECEIPT_METHODS': (receipt_methods_rows, list(receipt_methods_rows[0].keys())),
 'AR_CASH_RECEIPTS_ALL': (cash_receipts, list(cash_receipts[0].keys())),
 'AR_RECEIVABLE_APPLICATIONS_ALL': (applications, list(applications[0].keys())),
 'GL_LEDGERS': (gl_ledgers, list(gl_ledgers[0].keys())),
 'GL_PERIODS': (gl_periods, list(gl_periods[0].keys())),
 'GL_CODE_COMBINATIONS': (gl_ccids, list(gl_ccids[0].keys())),
 'XLA_AE_HEADERS': (xla_headers, list(xla_headers[0].keys())),
 'XLA_AE_LINES': (xla_lines, list(xla_lines[0].keys())),
 'XLA_DISTRIBUTION_LINKS': (xla_links, list(xla_links[0].keys())),
 'GL_JE_SOURCES': ([{'je_source_name':'Receivables','user_je_source_name':'应收模块'}], ['je_source_name','user_je_source_name']),
 'GL_JE_CATEGORIES': ([{'je_category_name':'Sales','user_je_category_name':'销售收入'}], ['je_category_name','user_je_category_name']),
 'GL_JE_HEADERS': (gl_headers, list(gl_headers[0].keys())),
 'GL_JE_LINES': (gl_lines, list(gl_lines[0].keys())),
 'GL_IMPORT_REFERENCES': (gl_import_refs, list(gl_import_refs[0].keys())),
 'GL_BALANCES': (gl_balances, list(gl_balances[0].keys())),
}

for name, (rows, headers) in files.items():
    write_csv(name, rows, headers)

print(f'Generated {len(files)} CSV files in {OUT}')
