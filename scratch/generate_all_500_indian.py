#!/usr/bin/env python3
"""
Omniscope AI - 500 Indian Benchmark Companies Generator
-------------------------------------------------------
Generates exactly 500 distinct, authentic Indian companies across 24 sectors.
Each company features:
  - Differentiated Customer Value Proposition (CVP)
  - Non-vague, ecosystem-specific PESTLE analysis calibrated for the Indian economy
  - Porter's 5 Forces analysis tailored to Indian industry competitive dynamics
  - 11-Dimensional Strategic Vector
  - 384-Dimensional CVP Text Embedding (VectorPlacementEngine)
"""

import json
import math
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))
from chatbot_engine import VectorPlacementEngine


def make_comp(id_num, company, sector, target_customer, statement_of_need,
              product_name, product_category, statement_of_key_benefit,
              p_scores, p_details, porters_scores, porters_details):
    cvp_text = f"For {target_customer} who {statement_of_need}, the {product_name} is a {product_category} that {statement_of_key_benefit}."
    
    # 11D vector: [political, economic, social, technological, legal, environmental,
    #               threat_of_new_entrants, bargaining_power_of_buyers, bargaining_power_of_suppliers, threat_of_substitutes, competitive_rivalry]
    s11 = [
        round(p_scores["political"], 2),
        round(p_scores["economic"], 2),
        round(p_scores["social"], 2),
        round(p_scores["technological"], 2),
        round(p_scores["legal"], 2),
        round(p_scores["environmental"], 2),
        round(porters_scores["threat_of_new_entrants"], 2),
        round(porters_scores["bargaining_power_of_buyers"], 2),
        round(porters_scores["bargaining_power_of_suppliers"], 2),
        round(porters_scores["threat_of_substitutes"], 2),
        round(porters_scores["competitive_rivalry"], 2),
    ]
    
    cvp_384d = VectorPlacementEngine.compute_384d_text_embedding(cvp_text)
    
    pestle_dict = {
        "political": s11[0],
        "economic": s11[1],
        "social": s11[2],
        "technological": s11[3],
        "legal": s11[4],
        "environmental": s11[5],
        "details": p_details
    }
    
    porters_dict = {
        "threat_of_new_entrants": s11[6],
        "bargaining_power_of_buyers": s11[7],
        "bargaining_power_of_suppliers": s11[8],
        "threat_of_substitutes": s11[9],
        "competitive_rivalry": s11[10],
        "details": porters_details
    }
    
    return {
        "id": f"comp_{id_num:03d}",
        "company": company,
        "sector": sector,
        "target_customer": target_customer,
        "statement_of_need": statement_of_need,
        "product_name": product_name,
        "product_category": product_category,
        "statement_of_key_benefit": statement_of_key_benefit,
        "cvp": cvp_text,
        "pestle": pestle_dict,
        "porters": porters_dict,
        "strategic_embedding_11d": s11,
        "cvp_embedding_384d": cvp_384d
    }

print("Base generator helper defined successfully.")
