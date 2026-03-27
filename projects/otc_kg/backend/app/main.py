from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from neo4j import GraphDatabase
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="OTC Knowledge Graph API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password123")

# MySQL connection
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "vv7g51Hou"),
    "database": os.getenv("MYSQL_DATABASE", "otc_kg")
}

class QueryRequest(BaseModel):
    query_type: str
    parameters: Optional[Dict[str, Any]] = {}

class QueryResult(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    message: str

def run_cypher(query: str, parameters: dict = None) -> List[Dict]:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            result = session.run(query, parameters or {})
            return [dict(record) for record in result]
    finally:
        driver.close()

def run_sql(query: str, parameters: dict = None) -> List[Dict]:
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, parameters or {})
        return cursor.fetchall()
    finally:
        conn.close()

@app.get("/")
async def root():
    return {"message": "OTC Knowledge Graph API", "status": "running"}

@app.get("/health")
async def health():
    return {"neo4j": "connected", "mysql": "connected"}

@app.get("/stats")
async def stats():
    neo4j_stats = run_cypher("MATCH (n) RETURN labels(n)[0] as label, count(*) as cnt ORDER BY label")
    mysql_stats = run_sql("SELECT TABLE_NAME as tbl, TABLE_ROWS as cnt FROM information_schema.TABLES WHERE TABLE_SCHEMA='otc_kg'")
    return {"neo4j": neo4j_stats, "mysql": mysql_stats}

# Pre-defined risk queries
RISK_QUERIES = {
    "shared_bank_accounts": """
        MATCH (a:CustomerAccount)-[:SHARES_BANK_ACCOUNT_WITH]->(b:CustomerAccount)
        RETURN a.cust_account_id AS account_a, a.account_name AS name_a,
               b.cust_account_id AS account_b, b.account_name AS name_b
        ORDER BY a.cust_account_id
        LIMIT $limit
    """,
    "high_overdue": """
        MATCH (ps:PaymentSchedule)
        WHERE ps.overdue_days > $min_days
        MATCH (i:Invoice {customer_trx_id: ps.customer_trx_id})
        MATCH (c:CustomerAccount {cust_account_id: i.sold_to_customer_id})
        RETURN c.cust_account_id, c.account_name, ps.amount_due_remaining, ps.overdue_days
        ORDER BY ps.overdue_days DESC
        LIMIT $limit
    """,
    "high_risk_orders": """
        MATCH (p:CustomerParty {risk_level: 'HIGH'})-[:HAS_ACCOUNT]->(c:CustomerAccount)-[:PLACED_ORDER]->(o:SalesOrder)
        RETURN p.party_name, p.risk_level, c.account_name, o.order_number, o.order_amount
        ORDER BY o.order_amount DESC
        LIMIT $limit
    """,
    "high_discount": """
        MATCH (l:SalesOrderLine)
        WHERE l.discount_percent > $min_discount
        MATCH (o:SalesOrder {header_id: l.header_id})
        MATCH (c:CustomerAccount {cust_account_id: o.sold_to_org_id})
        RETURN c.account_name, o.order_number, l.discount_percent, l.line_amount
        ORDER BY l.discount_percent DESC
        LIMIT $limit
    """,
    "uninvoiced_shipments": """
        MATCH (d:DeliveryDetail)
        WHERE NOT (d)<-[:GENERATED_FROM_DELIVERY]-(:InvoiceLine)
        MATCH (l:SalesOrderLine {line_id: d.source_line_id})
        MATCH (o:SalesOrder {header_id: l.header_id})
        MATCH (c:CustomerAccount {cust_account_id: o.sold_to_org_id})
        RETURN c.account_name, o.order_number, d.delivery_detail_id, d.shipped_quantity, d.actual_shipment_date
        LIMIT $limit
    """,
    "customer_journey": """
        MATCH path = (c:CustomerAccount)-[:PLACED_ORDER]->(o:SalesOrder)-[:HAS_LINE]->(l:SalesOrderLine)
                     -[:FULFILLED_BY]->(d:DeliveryDetail)-[:GENERATED_FROM_DELIVERY*0..1]->(il:InvoiceLine)
                     <-[:HAS_LINE]-(i:Invoice)-[:GENERATES_AR]->(ps:PaymentSchedule)
                     <-[:APPLIED_TO]-(cr:CashReceipt)
        WHERE c.cust_account_id = $customer_id
        RETURN path
        LIMIT $limit
    """,
    "approval_chain": """
        MATCH (e:Employee)-[r:APPROVED]->(o:SalesOrder)
        RETURN e.employee_name, e.department_name, o.order_number, o.order_amount
        ORDER BY o.order_amount DESC
        LIMIT $limit
    """,
    "exceed_credit": """
        MATCH (c:CustomerAccount)-[:HAS_CREDIT_PROFILE]->(cp:CreditProfile)
        MATCH (c)-[:PLACED_ORDER]->(o:SalesOrder)
        WHERE o.order_amount > cp.credit_limit
        RETURN c.account_name, cp.credit_limit, o.order_number, o.order_amount, o.flow_status_code
        LIMIT $limit
    """
}

@app.post("/query/risk")
async def query_risk(request: QueryRequest) -> QueryResult:
    query_type = request.query_type
    params = request.parameters or {}
    limit = params.get("limit", 20)
    
    if query_type not in RISK_QUERIES:
        raise HTTPException(status_code=400, detail=f"Unknown query type: {query_type}")
    
    query = RISK_QUERIES[query_type]
    
    # Set default parameters
    cypher_params = {"limit": limit}
    if query_type == "high_overdue":
        cypher_params["min_days"] = params.get("min_days", 90)
    elif query_type == "high_discount":
        cypher_params["min_discount"] = params.get("min_discount", 20)
    elif query_type == "customer_journey":
        cypher_params["customer_id"] = params.get("customer_id", 300000001)
    
    try:
        result = run_cypher(query, cypher_params)
        return QueryResult(success=True, data=result, message=f"Found {len(result)} records")
    except Exception as e:
        return QueryResult(success=False, data=[], message=str(e))

@app.post("/query/custom")
async def query_custom(query: str):
    try:
        result = run_cypher(query)
        return QueryResult(success=True, data=result, message=f"Query executed successfully")
    except Exception as e:
        return QueryResult(success=False, data=[], message=str(e))

@app.get("/customer/{customer_id}")
async def get_customer(customer_id: int):
    cypher = """
        MATCH (c:CustomerAccount {cust_account_id: $cid})
        OPTIONAL MATCH (c)-[:HAS_CREDIT_PROFILE]->(cp:CreditProfile)
        OPTIONAL MATCH (c)-[:PLACED_ORDER]->(o:SalesOrder)
        RETURN c, cp, count(o) as order_count
    """
    result = run_cypher(cypher, {"cid": customer_id})
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return result[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Import LLM modules
try:
    from app.llm.intent_classifier import classify_intent
    from app.llm.response_generator import generate_response
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

class NaturalLanguageQuery(BaseModel):
    query: str

class NLQueryResult(BaseModel):
    success: bool
    intent: Optional[str]
    confidence: float
    description: str
    data: List[Dict[str, Any]]
    natural_response: str
    suggestions: List[str]

@app.post("/query/natural", response_model=NLQueryResult)
async def query_natural(request: NaturalLanguageQuery):
    """
    自然语言查询接口
    将用户自然语言输入转换为风险查询并返回结果
    """
    if not LLM_AVAILABLE:
        raise HTTPException(status_code=503, detail="LLM module not available")
    
    user_input = request.query
    
    # Step 1: 意图识别
    intent_result = classify_intent(user_input)
    intent = intent_result["intent"]
    confidence = intent_result["confidence"]
    parameters = intent_result["parameters"]
    suggestions = intent_result["suggestions"]
    
    if not intent:
        return NLQueryResult(
            success=False,
            intent=None,
            confidence=confidence,
            description="未能识别查询意图",
            data=[],
            natural_response="抱歉，我理解不了您的查询。请尝试以下查询类型：" + ", ".join(suggestions[:5]),
            suggestions=suggestions
        )
    
    # Step 2: 执行查询
    if intent not in RISK_QUERIES:
        return NLQueryResult(
            success=False,
            intent=intent,
            confidence=confidence,
            description="查询类型暂不支持",
            data=[],
            natural_response="该查询类型暂不支持，请选择其他查询。",
            suggestions=list(RISK_QUERIES.keys())
        )
    
    query = RISK_QUERIES[intent]
    cypher_params = {"limit": parameters.get("limit", 20)}
    
    if intent == "high_overdue":
        cypher_params["min_days"] = parameters.get("min_days", 90)
    elif intent == "high_discount":
        cypher_params["min_discount"] = parameters.get("min_discount", 20)
    elif intent == "customer_journey":
        cypher_params["customer_id"] = parameters.get("customer_id", 300000001)
    
    try:
        result_data = run_cypher(query, cypher_params)
        
        # Step 3: 生成自然语言响应
        natural_response = generate_response(intent, result_data, parameters)
        
        return NLQueryResult(
            success=True,
            intent=intent,
            confidence=confidence,
            description=intent_result.get("description", ""),
            data=result_data,
            natural_response=natural_response,
            suggestions=[]
        )
        
    except Exception as e:
        return NLQueryResult(
            success=False,
            intent=intent,
            confidence=confidence,
            description="查询执行失败",
            data=[],
            natural_response=f"查询执行出错: {str(e)}",
            suggestions=[]
        )

@app.get("/query/intents")
async def list_intents():
    """列出所有支持的查询意图"""
    return {
        "intents": [
            {"key": k, "description": v.get("description", ""), "keywords": v.get("keywords", [])}
            for k, v in INTENT_KEYWORDS.items()
        ]
    }


@app.get("/graph/overview")
async def graph_overview(limit: int = 80):
    cypher = """
    MATCH (a:CustomerAccount)-[:SHARES_BANK_ACCOUNT_WITH]-(b:CustomerAccount)
    OPTIONAL MATCH (a)-[:USES_BANK_ACCOUNT]->(ba:BankAccount)
    WITH collect(DISTINCT a) + collect(DISTINCT b) + collect(DISTINCT ba) AS ns
    UNWIND ns AS n
    WITH collect(DISTINCT n)[0..$limit] AS nodes
    UNWIND nodes AS n
    OPTIONAL MATCH (n)-[r]-(m)
    WHERE m IN nodes
    RETURN collect(DISTINCT {
      id: coalesce(n.cust_account_id, n.bank_account_id, n.party_id, n.customer_trx_id, n.line_id, n.header_id, n.payment_schedule_id, n.cash_receipt_id, n.employee_id, n.location_id, n.credit_profile_id),
      label: labels(n)[0],
      name: coalesce(n.account_name, n.bank_name, n.party_name, n.order_number, n.trx_number, n.employee_name, n.address_line1, toString(coalesce(n.cust_account_id, n.bank_account_id, n.party_id))),
      props: properties(n)
    }) AS nodes,
    collect(DISTINCT CASE WHEN r IS NULL THEN NULL ELSE {
      source: coalesce(startNode(r).cust_account_id, startNode(r).bank_account_id, startNode(r).party_id, startNode(r).customer_trx_id, startNode(r).line_id, startNode(r).header_id, startNode(r).payment_schedule_id, startNode(r).cash_receipt_id, startNode(r).employee_id, startNode(r).location_id, startNode(r).credit_profile_id),
      target: coalesce(endNode(r).cust_account_id, endNode(r).bank_account_id, endNode(r).party_id, endNode(r).customer_trx_id, endNode(r).line_id, endNode(r).header_id, endNode(r).payment_schedule_id, endNode(r).cash_receipt_id, endNode(r).employee_id, endNode(r).location_id, endNode(r).credit_profile_id),
      type: type(r)
    } END) AS rels
    """
    result = run_cypher(cypher, {"limit": limit})
    if not result:
        return {"nodes": [], "edges": []}
    row = result[0]
    edges = [r for r in row.get("rels", []) if r]
    return {"nodes": row.get("nodes", []), "edges": edges}

# =========================
# v2 O2C + R2R APIs
# =========================
def run_sql_v2(query: str, parameters: tuple = ()) -> List[Dict]:
    cfg = dict(MYSQL_CONFIG)
    cfg['database'] = 'otc_kg_v2'
    conn = mysql.connector.connect(**cfg)
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, parameters)
        return cursor.fetchall()
    finally:
        conn.close()

@app.get('/stats/v2')
async def stats_v2():
    mysql_stats = {
        'customers': run_sql_v2('SELECT COUNT(*) c FROM HZ_CUST_ACCOUNTS')[0]['c'],
        'orders': run_sql_v2('SELECT COUNT(*) c FROM OE_ORDER_HEADERS_ALL')[0]['c'],
        'invoices': run_sql_v2('SELECT COUNT(*) c FROM RA_CUSTOMER_TRX_ALL')[0]['c'],
        'receipts': run_sql_v2('SELECT COUNT(*) c FROM AR_CASH_RECEIPTS_ALL')[0]['c'],
        'xla_entries': run_sql_v2('SELECT COUNT(*) c FROM XLA_AE_HEADERS')[0]['c'],
        'journal_entries': run_sql_v2('SELECT COUNT(*) c FROM GL_JE_HEADERS')[0]['c'],
        'balances': run_sql_v2('SELECT COUNT(*) c FROM GL_BALANCES')[0]['c'],
    }
    neo4j_stats = run_cypher('MATCH (n) RETURN labels(n)[0] AS label, count(*) AS cnt ORDER BY label')
    return {'mysql': mysql_stats, 'neo4j': neo4j_stats}

@app.get('/query/o2c-r2r/trace')
async def query_o2c_r2r_trace(limit: int = 20):
    sql = """
    SELECT c.account_name AS customer_name,
           o.order_number,
           i.trx_number,
           x.ae_header_id,
           j.je_header_id,
           gcc.segment3_account AS gl_account,
           j.period_name
    FROM OE_ORDER_HEADERS_ALL o
    JOIN HZ_CUST_ACCOUNTS c ON o.sold_to_org_id = c.cust_account_id
    JOIN INVOICE_ORDER_LINK iol ON iol.header_id = o.header_id
    JOIN RA_CUSTOMER_TRX_LINES_ALL itl ON iol.customer_trx_line_id = itl.customer_trx_line_id
    JOIN RA_CUSTOMER_TRX_ALL i ON itl.customer_trx_id = i.customer_trx_id
    JOIN XLA_AE_HEADERS x ON x.source_id = i.customer_trx_id AND x.entity_code='RA_CUSTOMER_TRX'
    JOIN GL_IMPORT_REFERENCES gir ON gir.ae_header_id = x.ae_header_id
    JOIN GL_JE_HEADERS j ON gir.je_header_id = j.je_header_id
    JOIN GL_JE_LINES gjl ON gjl.je_header_id = j.je_header_id
    JOIN GL_CODE_COMBINATIONS gcc ON gjl.code_combination_id = gcc.code_combination_id
    ORDER BY o.header_id, i.customer_trx_id
    LIMIT %s
    """
    data = run_sql_v2(sql, (limit,))
    return {'success': True, 'message': '标准版 O2C-R2R 穿透查询完成', 'data': data}

@app.get('/query/gl-impact')
async def query_gl_impact(limit: int = 20):
    sql = """
    SELECT i.trx_number,
           j.je_header_id,
           gcc.segment3_account AS gl_account,
           gjl.accounted_dr,
           gjl.accounted_cr,
           j.period_name
    FROM RA_CUSTOMER_TRX_ALL i
    JOIN XLA_AE_HEADERS x ON x.source_id = i.customer_trx_id AND x.entity_code='RA_CUSTOMER_TRX'
    JOIN GL_IMPORT_REFERENCES gir ON gir.ae_header_id = x.ae_header_id
    JOIN GL_JE_HEADERS j ON gir.je_header_id = j.je_header_id
    JOIN GL_JE_LINES gjl ON gjl.je_header_id = j.je_header_id
    JOIN GL_CODE_COMBINATIONS gcc ON gjl.code_combination_id = gcc.code_combination_id
    ORDER BY i.customer_trx_id
    LIMIT %s
    """
    data = run_sql_v2(sql, (limit,))
    return {'success': True, 'message': '发票到总账影响查询完成', 'data': data}

@app.get('/graph/overview/v2')
async def graph_overview_v2(limit: int = 120):
    nodes = run_cypher("""
    MATCH (c:CustomerAccount)-[:PLACED_ORDER]->(o:SalesOrder)-[:BILLED_AS]->(i:Invoice)-[:ACCOUNTED_AS]->(x:SubledgerEntry)-[:POSTED_TO]->(j:JournalEntry)-[:HITS_ACCOUNT]->(g:GLAccount)
    WITH collect(DISTINCT c)+collect(DISTINCT o)+collect(DISTINCT i)+collect(DISTINCT x)+collect(DISTINCT j)+collect(DISTINCT g) AS ns
    UNWIND ns[0..$limit] AS n
    RETURN coalesce(n.id, id(n)) AS id,
           labels(n)[0] AS label,
           coalesce(n.name, n.order_number, n.trx_number, n.account, toString(coalesce(n.id,id(n)))) AS name,
           properties(n) AS props
    """, {'limit': limit})
    edges = run_cypher("""
    MATCH (c:CustomerAccount)-[r1:PLACED_ORDER]->(o:SalesOrder)-[r2:BILLED_AS]->(i:Invoice)-[r3:ACCOUNTED_AS]->(x:SubledgerEntry)-[r4:POSTED_TO]->(j:JournalEntry)-[r5:HITS_ACCOUNT]->(g:GLAccount)
    WITH collect(DISTINCT {source:c.id,target:o.id,type:type(r1)})+
         collect(DISTINCT {source:o.id,target:i.id,type:type(r2)})+
         collect(DISTINCT {source:i.id,target:x.id,type:type(r3)})+
         collect(DISTINCT {source:x.id,target:j.id,type:type(r4)})+
         collect(DISTINCT {source:j.id,target:g.id,type:type(r5)}) AS es
    UNWIND es[0..$limit] AS e
    RETURN e.source AS source, e.target AS target, e.type AS type
    """, {'limit': limit})
    return {'nodes': nodes, 'edges': edges}
