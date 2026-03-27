"""
自然语言意图识别模块
将用户输入的自然语言转换为预定义的风险查询类型
"""

import re
from typing import Dict, Any, Optional

# 意图关键词映射
INTENT_KEYWORDS = {
    "shared_bank_accounts": {
        "keywords": ["共享银行", "相同银行", "共用账户", "银行账户", "关联客户", "可疑关联"],
        "description": "识别共享银行账户的可疑客户群"
    },
    "high_overdue": {
        "keywords": ["逾期", "超期", "欠款", "未收款", "账龄", "应收", " overdue", "逾期天数"],
        "description": "查询高逾期的应收账款"
    },
    "high_risk_orders": {
        "keywords": ["高风险", "风险客户", "高风险订单", "风险等级"],
        "description": "查看高风险客户的订单"
    },
    "high_discount": {
        "keywords": ["折扣", "大额折扣", "高折扣", "优惠", "降价"],
        "description": "识别大额折扣订单"
    },
    "uninvoiced_shipments": {
        "keywords": ["未开票", "发货未开票", "开票", "发票缺失"],
        "description": "发货但未开票的交易"
    },
    "exceed_credit": {
        "keywords": ["超信用", "超额", "信用额度", "超限", "超过额度"],
        "description": "订单金额超过信用额度"
    },
    "approval_chain": {
        "keywords": ["审批", "审批链", "审批人", "审批记录", "审批链路"],
        "description": "订单审批穿透分析"
    },
    "customer_journey": {
        "keywords": ["客户旅程", "全链路", "交易链路", "客户追踪", "订单追踪"],
        "description": "客户OTC全链路追踪"
    }
}

def classify_intent(user_input: str) -> Dict[str, Any]:
    """
    根据用户输入识别查询意图
    
    Args:
        user_input: 用户自然语言输入
        
    Returns:
        {
            "intent": str,  # 识别到的意图类型
            "confidence": float,  # 置信度 0-1
            "parameters": dict,  # 提取的参数
            "suggestions": list  # 建议查询
        }
    """
    user_input = user_input.lower()
    scores = {}
    
    # 计算每个意图的匹配分数
    for intent, config in INTENT_KEYWORDS.items():
        score = 0
        for keyword in config["keywords"]:
            if keyword.lower() in user_input:
                score += 1
        scores[intent] = score / len(config["keywords"])
    
    # 找出最高分的意图
    if scores:
        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]
    else:
        best_intent = None
        best_score = 0
    
    # 提取参数
    parameters = extract_parameters(user_input)
    
    # 生成建议
    suggestions = []
    if best_score < 0.3:
        # 置信度低，提供所有选项
        suggestions = list(INTENT_KEYWORDS.keys())[:5]
    
    return {
        "intent": best_intent if best_score >= 0.3 else None,
        "confidence": best_score,
        "parameters": parameters,
        "suggestions": suggestions,
        "description": INTENT_KEYWORDS.get(best_intent, {}).get("description", "")
    }

def extract_parameters(user_input: str) -> Dict[str, Any]:
    """从用户输入中提取参数"""
    params = {}
    
    # 提取数字参数
    # 逾期天数
    overdue_match = re.search(r'(\d+)\s*天', user_input)
    if overdue_match:
        params["min_days"] = int(overdue_match.group(1))
    
    # 折扣百分比
    discount_match = re.search(r'(\d+)\s*%', user_input)
    if discount_match:
        params["min_discount"] = int(discount_match.group(1))
    
    # 限制数量
    limit_match = re.search(r'(\d+)\s*条|前\s*(\d+)', user_input)
    if limit_match:
        params["limit"] = int(limit_match.group(1) or limit_match.group(2))
    else:
        params["limit"] = 20
    
    # 客户ID
    customer_match = re.search(r'客户\s*(\d+)', user_input)
    if customer_match:
        params["customer_id"] = int(customer_match.group(1))
    
    return params

def get_query_description(intent: str) -> str:
    """获取查询描述"""
    return INTENT_KEYWORDS.get(intent, {}).get("description", "未知查询")

# 示例用法
if __name__ == "__main__":
    test_inputs = [
        "查一下共享银行账户的客户",
        "看看逾期超过90天的应收",
        "高风险客户的订单有哪些",
        "折扣超过20%的订单",
        "发货了但没开票的",
        "超过信用额度的订单",
        "审批记录"
    ]
    
    for input_text in test_inputs:
        result = classify_intent(input_text)
        print(f"输入: {input_text}")
        print(f"意图: {result['intent']}, 置信度: {result['confidence']:.2f}")
        print(f"参数: {result['parameters']}")
        print()
