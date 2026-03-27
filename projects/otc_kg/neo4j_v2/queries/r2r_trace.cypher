MATCH (c:CustomerAccount)-[:PLACED_ORDER]->(o:SalesOrder)-[:BILLED_AS]->(i:Invoice)-[:ACCOUNTED_AS]->(x:SubledgerEntry)-[:POSTED_TO]->(j:JournalEntry)-[:HITS_ACCOUNT]->(g:GLAccount)
RETURN c.name, o.order_number, i.trx_number, x.id, j.id, g.account
LIMIT 20;
