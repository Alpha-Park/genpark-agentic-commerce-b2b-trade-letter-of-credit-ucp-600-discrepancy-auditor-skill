# genpark-agentic-commerce-b2b-trade-letter-of-credit-ucp-600-discrepancy-auditor-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

ICC UCP 600 documentary letter of credit (LC) compliance, bill of lading date/port discrepancy checker.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `audit_ucp600_letter_of_credit_documents`
- **Category**: `agentic_commerce`

### Method Documentation
Audit international trade documentary Letter of Credit (LC) presentation under ICC UCP 600 rules.
Cross-verifies Commercial Invoice, Bill of Lading (BOL), and Insurance Certificate against LC terms:
latest shipment date, partial shipment allowances, port of loading/discharge, and description strict compliance (Article 18c).

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "audit_ucp600_letter_of_credit_documents",
    "arguments": {
    "lc_terms": {
        "lc_number": "LC-2026-CH-918",
        "lc_amount": 250000.0,
        "currency": "USD",
        "latest_shipment_date": "2026-11-15",
        "port_of_loading": "SHANGHAI",
        "port_of_discharge": "ROTTERDAM"
    },
    "commercial_invoice": {
        "currency": "USD",
        "total_amount": 248000.0
    },
    "bill_of_lading": {
        "on_board_date": "2026-11-10",
        "port_of_loading": "SHANGHAI",
        "port_of_discharge": "ROTTERDAM"
    },
    "insurance_cert": {
        "insured_amount": 275000.0
    }
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
