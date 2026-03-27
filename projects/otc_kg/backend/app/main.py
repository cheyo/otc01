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
