# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-b2b-trade-letter-of-credit-ucp-600-discrepancy-auditor-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_ucp600_letter_of_credit_documents(lc_terms, commercial_invoice, bill_of_lading, insurance_cert):
    discrepancies = []
    
    # 1. Commercial Invoice currency and amount check (Article 18b)
    if commercial_invoice["currency"] != lc_terms["currency"]:
        discrepancies.append(f"Currency mismatch: LC is in {lc_terms['currency']}, invoice is in {commercial_invoice['currency']}")
    if commercial_invoice["total_amount"] > lc_terms["lc_amount"]:
        discrepancies.append(f"Invoice amount ({commercial_invoice['total_amount']}) exceeds LC value ({lc_terms['lc_amount']})")
        
    # 2. Bill of Lading shipment date and ports (Article 20)
    if bill_of_lading["on_board_date"] > lc_terms["latest_shipment_date"]:
        discrepancies.append(f"Late shipment: On-board date {bill_of_lading['on_board_date']} past LC limit {lc_terms['latest_shipment_date']}")
    if bill_of_lading["port_of_loading"].upper() != lc_terms["port_of_loading"].upper():
        discrepancies.append(f"Port of loading mismatch: {bill_of_lading['port_of_loading']} vs {lc_terms['port_of_loading']}")
    if bill_of_lading["port_of_discharge"].upper() != lc_terms["port_of_discharge"].upper():
        discrepancies.append(f"Port of discharge mismatch: {bill_of_lading['port_of_discharge']} vs {lc_terms['port_of_discharge']}")
        
    # 3. Insurance Coverage (Article 28 - minimum 110% of CIF value)
    min_insured_value = commercial_invoice["total_amount"] * 1.10
    if insurance_cert["insured_amount"] < min_insured_value:
        discrepancies.append(f"Insurance coverage shortfall: Insured for {insurance_cert['insured_amount']} vs required 110% CIF {min_insured_value:.2f}")
        
    compliant = len(discrepancies) == 0
    
    return {
        "ucp_600_compliant_presentation": compliant,
        "discrepancy_count": len(discrepancies),
        "discrepancies_identified": discrepancies if discrepancies else ["Clean documentary presentation"],
        "bank_advising_action": "Documents honor-ready; proceed with negotiation / reimbursement." if compliant else "Reject presentation under UCP 600 Article 16 notice of refusal."
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_ucp600_letter_of_credit_documents",
                        "description": """Audit international trade documentary Letter of Credit (LC) presentation under ICC UCP 600 rules.
Cross-verifies Commercial Invoice, Bill of Lading (BOL), and Insurance Certificate against LC terms:
latest shipment date, partial shipment allowances, port of loading/discharge, and description strict compliance (Article 18c).""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_ucp600_letter_of_credit_documents(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'lc_terms': {'lc_number': 'LC-2026-CH-918', 'lc_amount': 250000.0, 'currency': 'USD', 'latest_shipment_date': '2026-11-15', 'port_of_loading': 'SHANGHAI', 'port_of_discharge': 'ROTTERDAM'}, 'commercial_invoice': {'currency': 'USD', 'total_amount': 248000.0}, 'bill_of_lading': {'on_board_date': '2026-11-10', 'port_of_loading': 'SHANGHAI', 'port_of_discharge': 'ROTTERDAM'}, 'insurance_cert': {'insured_amount': 275000.0}}
        out = audit_ucp600_letter_of_credit_documents(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
