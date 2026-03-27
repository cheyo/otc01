"""
查询结果解释生成模块
将图查询结果转换为自然语言描述
"""

from typing import List, Dict, Any

def generate_response(intent: str, results: List[Dict[str, Any]], parameters: Dict[str, Any]) -> str:
    """
    根据查询结果生成自然语言响应
    
    Args:
        intent: 查询意图
        results: 查询结果
        parameters: 查询参数
        
    Returns:
        自然语言描述
    """
    count = len(results)
    
    response_templates = {
        "shared_bank_accounts": f"发现 {count} 组客户共享银行账户，这些客户可能存在关联关系或属于同一集团。",
        "high_overdue": f"查询到 {count} 笔逾期超过 {parameters.get('min_days', 90)} 天的应收账款，建议重点关注催收。",
        "high_risk_orders": f"高风险客户共产生 {count} 笔订单，建议评估信用风险并加强监控。",
        "high_discount": f"发现 {count} 笔折扣超过 {parameters.get('min_discount', 20)}% 的订单，需关注折扣审批合规性。",
        "uninvoiced_shipments": f"存在 {count} 笔已发货但未开票的交易，可能影响收入确认及时性。",
        "exceed_credit": f"{count} 笔订单金额超过客户信用额度，存在授信控制风险。",
        "approval_chain": f"查询到 {count} 条审批记录。",
        "customer_journey": f"客户全链路追踪完成，共涉及 {count} 个节点。"
    }
    
    base_response = response_templates.get(intent, f"查询完成，共找到 {count} 条记录。")
    
    # 添加关键数据摘要
    summary = generate_summary(intent, results)
    if summary:
        base_response += f"\n\n关键发现：\n{summary}"
    
    return base_response

def generate_summary(intent: str, results: List[Dict[str, Any]]) -> str:
    """生成结果摘要"""
    if not results:
        return ""
    
    summaries = []
    
    if intent == "shared_bank_accounts":
        # 统计涉及的客户数
        accounts = set()
        for r in results:
            accounts.add(r.get("account_a"))
            accounts.add(r.get("account_b"))
        summaries.append(f"- 涉及 {len(accounts)} 个客户账户")
        
    elif intent == "high_overdue":
        # 统计总金额
        total = sum(r.get("amount_due_remaining", 0) for r in results)
        max_overdue = max(r.get("overdue_days", 0) for r in results) if results else 0
        summaries.append(f"- 逾期总金额: {total:,.2f} 元")
        summaries.append(f"- 最长逾期: {max_overdue} 天")
        
    elif intent == "high_risk_orders":
        total = sum(r.get("order_amount", 0) for r in results)
        summaries.append(f"- 订单总金额: {total:,.2f} 元")
        
    elif intent == "high_discount":
        max_discount = max(r.get("discount_percent", 0) for r in results) if results else 0
        summaries.append(f"- 最高折扣: {max_discount:.2f}%")
        
    return "\n".join(summaries)

def format_table_data(results: List[Dict[str, Any]], max_rows: int = 10) -> str:
    """格式化表格数据为文本"""
    if not results:
        return "无数据"
    
    # 获取表头
    headers = list(results[0].keys())
    
    # 格式化
    lines = []
    lines.append(" | ".join(headers))
    lines.append("-" * (sum(len(h) for h in headers) + 3 * len(headers)))
    
    for row in results[:max_rows]:
        values = [str(row.get(h, "")) for h in headers]
        lines.append(" | ".join(values))
    
    if len(results) > max_rows:
        lines.append(f"... 还有 {len(results) - max_rows} 条记录")
    
    return "\n".join(lines)
