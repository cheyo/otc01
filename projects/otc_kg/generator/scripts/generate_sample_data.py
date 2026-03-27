#!/usr/bin/env python3
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
BASE = Path('/root/.openclaw/workspace/projects/otc_kg/generator/output/sample_csv')
BASE.mkdir(parents=True, exist_ok=True)

surnames = ['王','李','张','刘','陈','杨','黄','赵','吴','周','徐','孙','马','朱','胡','郭']
given = ['伟','磊','娜','静','敏','杰','涛','洋','婷','超','勇','军','艳','斌','雪','颖','峰','凯','琳','倩']
provinces = [('广东省','深圳市',['南山区','福田区','宝安区']),('浙江省','杭州市',['余杭区','滨江区','西湖区']),('江苏省','苏州市',['工业园区','虎丘区','吴中区']),('北京市','北京市',['朝阳区','海淀区','丰台区']),('上海市','上海市',['浦东新区','闵行区','徐汇区'])]
roads = ['科技南一道','文一西路','星湖街','建国路','张江路','高新南七道','人民路','创新大道']
brand = ['云启','明川','远辰','嘉禾','启元','恒越','智联','安拓','融信','华盛']
industry = ['科技','电子','制造','供应链','医疗','贸易','物流','材料']
suffix = ['有限公司','科技有限公司','制造有限公司','供应链有限公司','贸易有限公司']
banks = ['中国工商银行','中国建设银行','中国农业银行','中国银行','招商银行','交通银行','中信银行','兴业银行','浦发银行','平安银行']
depts = ['华东销售部','华南销售部','信用管理部','应收管理部','财务共享中心','风险控制部']
roles = ['SALES','FINANCE','APPROVER','CREDIT']

OBS_DATE = datetime(2026,3,31)

def dt(days_back=900):
    return (OBS_DATE - timedelta(days=random.randint(0, days_back), hours=random.randint(0,23), minutes=random.randint(0,59))).strftime('%Y-%m-%d %H:%M:%S')

def cn_name():
    return random.choice(surnames) + random.choice(given) + (random.choice(given) if random.random() < 0.5 else '')

def company_name():
    prov, city, _ = random.choice(provinces)
    city_short = city.replace('市','')
    return f"{city_short}{random.choice(brand)}{random.choice(industry)}{random.choice(suffix)}"

def address_record(i):
    prov, city, districts = random.choice(provinces)
    district = random.choice(districts)
    road = random.choice(roads)
    no = random.randint(1,999)
    return prov, city, district, f"{prov}{city}{district}{road}{no}号", f"{random.randint(100000,999999)}"

def write_csv(name, headers, rows):
    with open(BASE / f'{name}.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

N_CUSTOMERS = 1000
N_EMP = 120

parties=[]; locations=[]; accounts=[]; acct_sites=[]; site_uses=[]; bank_accounts=[]; credit_profiles=[]; employees=[]
order_headers=[]; order_lines=[]; deliveries=[]; invoices=[]; invoice_lines=[]; invoice_links=[]; pay_sched=[]; receipts=[]; apps=[]; price_adj=[]; appr=[]; changes=[]

for i in range(1, N_CUSTOMERS+1):
    party_id = 100000000 + i
    party_number = f'PTY{party_id}'
    pname = company_name() if random.random() > 0.05 else cn_name()
    risk = random.choices(['LOW','MEDIUM','HIGH'], weights=[70,20,10])[0]
    prov, city, district, addr, postcode = address_record(i)
    created = dt()
    parties.append([party_id, party_number, pname, 'ORGANIZATION', f'9144{random.randint(100000000000,999999999999)}', 'CN', prov, city, random.choice(industry), random.choice(['SMALL','MEDIUM','LARGE','KEY']), risk, 'ACTIVE', created, created])
    location_id = 200000000 + i
    locations.append([location_id,'CN',prov,city,district,addr,postcode,created,created])
    acc_id = 300000000 + i
    acct_no = f'CUST{acc_id}'
    pay_term = random.choices(['NET30','NET60','NET90','PREPAID'], weights=[50,25,10,15])[0]
    accounts.append([acc_id,party_id,acct_no,pname,'STANDARD',risk,pay_term,random.choice(['DIRECT','PARTNER','ONLINE']), city.replace('市',''),'ACTIVE',created,created,created])
    site_id = 400000000 + i
    acct_sites.append([site_id,acc_id,location_id,f'SITE{site_id}',random.randint(1,5),'ACTIVE',created,created])
    su1 = 500000000 + i*2
    su2 = su1 + 1
    site_uses.append([su1,site_id,'BILL_TO','Y','ACTIVE',created,created])
    site_uses.append([su2,site_id,'SHIP_TO','Y','ACTIVE',created,created])
    shared_bank_suffix = i if random.random() > 0.01 else max(1, i-1)
    bank_acc_id = 600000000 + i
    bank_name = random.choice(banks)
    branch = bank_name + city.replace('市','') + district.replace('区','').replace('新区','') + '支行'
    bank_accounts.append([bank_acc_id,acc_id,bank_name,branch,f'6222{shared_bank_suffix:014d}',pname,'PUBLIC','Y','ACTIVE',created,created])
    limit_map = {'SMALL':(50000,200000),'MEDIUM':(200000,1000000),'LARGE':(1000000,5000000),'KEY':(5000000,20000000)}
    size = parties[-1][9]
    low, high = limit_map[size]
    credit_limit = round(random.uniform(low, high),2)
    score = round(random.uniform(40,95) if risk!='HIGH' else random.uniform(10,60),2)
    credit_profiles.append([700000000+i,acc_id,credit_limit,'CNY',pay_term,risk,score,random.choice([0,0,0,15,30]),'N',created,created,None,'ACTIVE',created,created])

for i in range(1, N_EMP+1):
    emp_id = 800000000+i
    created = dt(1500)
    employees.append([emp_id,f'EMP{emp_id}',cn_name(),random.choice(['男','女']),random.choice(depts),random.choice(roles),'专员',None,random.choice(['华东','华南','华北','西南']),'2023-01-01 09:00:00','ACTIVE',created,created])

line_id_seq = 1000000000
ship_id_seq = 1100000000
inv_id_seq = 1200000000
inv_line_id_seq = 1300000000
link_id_seq = 1400000000
ps_id_seq = 1500000000
receipt_id_seq = 1600000000
app_id_seq = 1700000000
adj_id_seq = 1800000000
appr_id_seq = 1900000000
chg_id_seq = 2000000000

for i in range(1, 3001):
    header_id = 900000000 + i
    acc = random.choice(accounts)
    risk = next(cp for cp in credit_profiles if cp[1] == acc[0])[5]
    order_date = datetime.strptime(dt(720), '%Y-%m-%d %H:%M:%S')
    booked_date = order_date + timedelta(days=random.randint(0,3))
    salesrep = random.choice(employees)[0]
    site_bill = 500000000 + (acc[0]-300000000+1)*2
    site_ship = site_bill + 1
    num_lines = random.choices([1,2,3,4,5], weights=[45,25,15,10,5])[0]
    line_rows = []
    total = 0.0; disc_total = 0.0; tax_total=0.0
    high_discount_order = random.random() < 0.02
    for ln in range(1, num_lines+1):
        qty = round(random.uniform(1,20),2)
        list_price = round(random.uniform(100,10000),2)
        disc_pct = round(random.uniform(20,45),2) if high_discount_order and ln==1 else round(random.choice([0,0,0,2,5,8,10,12]),2)
        unit = round(list_price*(1-disc_pct/100),2)
        amount = round(qty*unit,2)
        tax = round(amount*0.13,2)
        req = booked_date + timedelta(days=random.randint(1,10))
        promise = req + timedelta(days=random.randint(0,3))
        line_id_seq += 1
        line_status = random.choice(['AWAITING_SHIPPING','SHIPPED','INVOICED'])
        line_rows.append([line_id_seq,header_id,ln,random.randint(10000,99999),qty,unit,list_price,disc_pct,amount,req.strftime('%Y-%m-%d %H:%M:%S'),promise.strftime('%Y-%m-%d %H:%M:%S'),None,line_status,random.randint(1,5),order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
        total += amount; disc_total += round(qty*(list_price-unit),2); tax_total += tax
        if disc_pct > 0:
            adj_id_seq += 1
            approved = 'N' if disc_pct >= 20 else 'Y'
            approver = random.choice(employees)[0] if approved=='Y' else None
            price_adj.append([adj_id_seq,header_id,line_id_seq,'DISCOUNT','促销折扣' if approved=='Y' else '人工改价',list_price,unit,round(qty*(list_price-unit),2),disc_pct,approved,approver,booked_date.strftime('%Y-%m-%d %H:%M:%S') if approver else None,salesrep,order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
    status = random.choices(['ENTERED','BOOKED','CLOSED','CANCELLED'], weights=[5,20,65,10])[0]
    order_headers.append([header_id,f'SO{order_date.strftime("%Y%m%d")}{i:06d}',acc[0],site_ship,site_bill,order_date.strftime('%Y-%m-%d %H:%M:%S'),booked_date.strftime('%Y-%m-%d %H:%M:%S'),'STANDARD','CNY','CNY',round(total+tax_total,2),round(disc_total,2),round(tax_total,2),'Y' if status!='ENTERED' else 'N','Y' if status=='CANCELLED' else 'N',status,salesrep,random.randint(1,5),order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
    order_lines.extend(line_rows)

    # approval logs
    if total > 500000 or high_discount_order:
        levels = 2 if total > 500000 else 1
        for lv in range(1, levels+1):
            appr_id_seq += 1
            appr.append([appr_id_seq,'ORDER',header_id,lv,random.choice(employees)[0],'APPROVED','自动生成审批', (booked_date+timedelta(hours=lv)).strftime('%Y-%m-%d %H:%M:%S'), f'WF{header_id}', order_date.strftime('%Y-%m-%d %H:%M:%S'), order_date.strftime('%Y-%m-%d %H:%M:%S')])

    # deliveries / invoices / ar
    if status != 'CANCELLED':
        for lr in line_rows:
            line_id = lr[0]
            qty = lr[4]
            shipped_qty = qty if random.random() > 0.15 else round(qty*random.uniform(0.4,0.9),2)
            ship_date = booked_date + timedelta(days=random.randint(1,15))
            ship_id_seq += 1
            deliveries.append([ship_id_seq,header_id,line_id,lr[3],qty,shipped_qty,'SHIPPED' if shipped_qty>0 else 'READY',ship_date.strftime('%Y-%m-%d %H:%M:%S'),(ship_date+timedelta(days=random.randint(1,5))).strftime('%Y-%m-%d %H:%M:%S'),lr[13],200000000+(acc[0]-300000000),order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
            delayed_invoice = random.random() < 0.02
            if shipped_qty > 0 and random.random() > (0.08 if not delayed_invoice else 1.0):
                inv_id_seq += 1
                trx_date = ship_date + timedelta(days=random.randint(0,10))
                line_amt = round(shipped_qty*lr[5],2)
                if random.random() < 0.01:
                    line_amt = round(line_amt*random.uniform(1.05,1.2),2)
                tax = round(line_amt*0.13,2)
                invoices.append([inv_id_seq,f'INV{trx_date.strftime("%Y%m%d")}{inv_id_seq-1200000000:06d}',trx_date.strftime('%Y-%m-%d %H:%M:%S'),acc[0],site_bill,'INVOICE','CNY',round(line_amt+tax,2),tax,0,'Y',random.choice(['OPEN','CLOSED']),header_id,order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
                inv_line_id_seq += 1
                invoice_lines.append([inv_line_id_seq,inv_id_seq,1,'LINE',lr[3],shipped_qty,lr[5],line_amt,tax,line_id,order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
                link_id_seq += 1
                invoice_links.append([link_id_seq,inv_line_id_seq,line_id,ship_id_seq,'DELIVERY_TO_INVOICE','FULL',order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
                ps_id_seq += 1
                due = trx_date + timedelta(days=30 if acc[6]=='NET30' else 60 if acc[6]=='NET60' else 90 if acc[6]=='NET90' else 0)
                overdue = max((OBS_DATE - due).days, 0)
                remain = round((line_amt+tax) * (0 if random.random()<0.45 else random.uniform(0.1,1.0)),2)
                applied = round((line_amt+tax)-remain,2)
                bucket = 'CURRENT' if overdue<=0 else '1_30' if overdue<=30 else '31_60' if overdue<=60 else '61_90' if overdue<=90 else 'GT_90'
                pay_sched.append([ps_id_seq,inv_id_seq,due.strftime('%Y-%m-%d %H:%M:%S'),round(line_amt+tax,2),remain,applied,0,bucket,overdue,'OPEN' if remain>0 else 'CLOSED',order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
                if applied > 0:
                    receipt_id_seq += 1
                    rdate = trx_date + timedelta(days=random.randint(0,120))
                    rem_bank = bank_accounts[(acc[0]-300000001)][4]
                    receipts.append([receipt_id_seq,f'RCT{rdate.strftime("%Y%m%d")}{receipt_id_seq-1600000000:06d}',rdate.strftime('%Y-%m-%d %H:%M:%S'),acc[0],applied,'CNY','BANK_TRANSFER',rem_bank,'APPLIED',order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
                    app_id_seq += 1
                    apps.append([app_id_seq,receipt_id_seq,inv_id_seq,applied,(rdate+timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),'CASH','APPLIED',order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])
                if random.random() < 0.01:
                    chg_id_seq += 1
                    changes.append([chg_id_seq,'OE_ORDER_LINES_ALL',line_id,'unit_selling_price',str(lr[5]),str(round(lr[5]*random.uniform(0.8,0.98),2)),salesrep,'人工价格调整',(trx_date-timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),'Y',order_date.strftime('%Y-%m-%d %H:%M:%S'),order_date.strftime('%Y-%m-%d %H:%M:%S')])

write_csv('HZ_PARTIES',['party_id','party_number','party_name','party_type','tax_reference','country_code','province','city','industry_code','customer_size','risk_level','status','created_date','last_update_date'], parties)
write_csv('HZ_LOCATIONS',['location_id','country_code','province_name','city_name','district_name','address_line1','postal_code','created_date','last_update_date'], locations)
write_csv('HZ_CUST_ACCOUNTS',['cust_account_id','party_id','account_number','account_name','customer_class_code','credit_classification','payment_term_code','sales_channel_code','region_code','account_status','open_date','created_date','last_update_date'], accounts)
write_csv('HZ_CUST_ACCT_SITES_ALL',['cust_acct_site_id','cust_account_id','location_id','site_code','org_id','status','created_date','last_update_date'], acct_sites)
write_csv('HZ_CUST_SITE_USES_ALL',['site_use_id','cust_acct_site_id','site_use_code','primary_flag','status','created_date','last_update_date'], site_uses)
write_csv('CUST_BANK_ACCOUNTS',['bank_account_id','cust_account_id','bank_name','branch_name','bank_account_num','account_name','account_type','is_primary','status','created_date','last_update_date'], bank_accounts)
write_csv('CUST_CREDIT_PROFILES',['credit_profile_id','cust_account_id','credit_limit','currency_code','payment_terms','risk_level','risk_score','overdue_tolerance_days','credit_hold_flag','review_date','effective_start_date','effective_end_date','status','created_date','last_update_date'], credit_profiles)
write_csv('HR_EMPLOYEES',['employee_id','employee_no','employee_name','gender','department_name','role_code','title_name','manager_id','region_code','hire_date','status','created_date','last_update_date'], employees)
write_csv('OE_ORDER_HEADERS_ALL',['header_id','order_number','sold_to_org_id','ship_to_site_use_id','invoice_to_site_use_id','order_date','booked_date','order_type_code','order_currency_code','transactional_curr_code','order_amount','discount_amount','tax_amount','booked_flag','cancelled_flag','flow_status_code','salesrep_id','org_id','created_date','last_update_date'], order_headers)
write_csv('OE_ORDER_LINES_ALL',['line_id','header_id','line_number','inventory_item_id','ordered_quantity','unit_selling_price','list_price','discount_percent','line_amount','request_date','promise_date','actual_shipment_date','line_status_code','ship_from_org_id','created_date','last_update_date'], order_lines)
write_csv('WSH_DELIVERY_DETAILS',['delivery_detail_id','source_header_id','source_line_id','inventory_item_id','requested_quantity','shipped_quantity','released_status','actual_shipment_date','delivery_date','ship_from_org_id','ship_to_location_id','created_date','last_update_date'], deliveries)
write_csv('RA_CUSTOMER_TRX_ALL',['customer_trx_id','trx_number','trx_date','sold_to_customer_id','bill_to_site_use_id','cust_trx_type','currency_code','trx_amount','tax_amount','freight_amount','complete_flag','status','related_order_header_id','created_date','last_update_date'], invoices)
write_csv('RA_CUSTOMER_TRX_LINES_ALL',['customer_trx_line_id','customer_trx_id','line_number','line_type','inventory_item_id','quantity_invoiced','unit_selling_price','extended_amount','tax_amount','related_order_line_id','created_date','last_update_date'], invoice_lines)
write_csv('INVOICE_ORDER_LINK',['link_id','customer_trx_line_id','order_line_id','delivery_detail_id','link_type','match_status','created_date','last_update_date'], invoice_links)
write_csv('AR_PAYMENT_SCHEDULES_ALL',['payment_schedule_id','customer_trx_id','due_date','amount_due_original','amount_due_remaining','amount_applied','amount_adjusted','aging_bucket','overdue_days','status','created_date','last_update_date'], pay_sched)
write_csv('AR_CASH_RECEIPTS_ALL',['cash_receipt_id','receipt_number','receipt_date','payer_customer_id','receipt_amount','currency_code','receipt_method','remittance_bank_account','status','created_date','last_update_date'], receipts)
write_csv('AR_RECEIVABLE_APPLICATIONS_ALL',['receivable_application_id','cash_receipt_id','applied_customer_trx_id','amount_applied','apply_date','application_type','status','created_date','last_update_date'], apps)
write_csv('OE_PRICE_ADJUSTMENTS',['adjustment_id','header_id','line_id','adjustment_type','adjustment_reason','list_price','adjusted_price','adjustment_amount','adjustment_percent','approved_flag','approver_id','approval_time','created_by','created_date','last_update_date'], price_adj)
write_csv('OTC_APPROVAL_LOG',['approval_log_id','business_type','business_id','approval_level','approver_id','approval_result','approval_comment','approval_time','workflow_id','created_date','last_update_date'], appr)
write_csv('OTC_FIELD_CHANGE_LOG',['change_log_id','table_name','record_id','field_name','old_value','new_value','changed_by','change_reason','change_time','risk_flag','created_date','last_update_date'], changes)

print('sample csv generated to', BASE)
print('counts:', {
    'HZ_PARTIES': len(parties),
    'OE_ORDER_HEADERS_ALL': len(order_headers),
    'OE_ORDER_LINES_ALL': len(order_lines),
    'RA_CUSTOMER_TRX_ALL': len(invoices),
    'AR_CASH_RECEIPTS_ALL': len(receipts)
})
