"""
Omniscope AI - 500 Indian Benchmark Companies Assembler
Combines part1.json (133), part2.json (131), part3.json (122), part4.json (114).
Validates uniqueness, computes 11-D vectors and 384-D embeddings.
Saves to 500_companies_analysis.json
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

scratch_dir = Path(__file__).parent

parts = ["part1.json", "part2.json", "part3.json", "part4.json"]
all_raw = []

for p in parts:
    p_path = scratch_dir / p
    if not p_path.exists():
        raise FileNotFoundError(f"Missing {p_path}")
    with open(p_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} companies from {p}")
    all_raw.extend(data)

print(f"\nTotal raw companies loaded: {len(all_raw)}")
assert len(all_raw) == 500, f"Expected exactly 500 companies, got {len(all_raw)}"

# Check for duplicate names
names_seen = {}
duplicates = []
for idx, c in enumerate(all_raw):
    n = c["company"].strip().lower()
    if n in names_seen:
        duplicates.append((c["company"], names_seen[n], idx))
    else:
        names_seen[n] = idx

if duplicates:
    print(f"ERROR: Found {len(duplicates)} duplicate company names:")
    for d in duplicates:
        print(f"  '{d[0]}' at index {d[1]} and {d[2]}")
    sys.exit(1)
else:
    print("SUCCESS: All 500 company names are 100% distinct!")

# Assemble full 500 companies records
assembled = []
sector_counts = {}

for idx, c in enumerate(all_raw, 1):
    comp_id = f"comp_{idx:03d}"
    name = c["company"].strip()
    sector = c["sector"].strip()
    target_cust = c["target_customer"].strip()
    need = c["statement_of_need"].strip()
    product = c["product_name"].strip()
    category = c["product_category"].strip()
    benefit = c["statement_of_key_benefit"].strip()
    
    cvp_text = f"For {target_cust} who {need}, the {product} is a {category} that {benefit}."
    
    p = c["pestle"]
    po = c["porters"]
    
    s11 = [
        round(float(p["political"]), 2),
        round(float(p["economic"]), 2),
        round(float(p["social"]), 2),
        round(float(p["technological"]), 2),
        round(float(p["legal"]), 2),
        round(float(p["environmental"]), 2),
        round(float(po["threat_of_new_entrants"]), 2),
        round(float(po["bargaining_power_of_buyers"]), 2),
        round(float(po["bargaining_power_of_suppliers"]), 2),
        round(float(po["threat_of_substitutes"]), 2),
        round(float(po["competitive_rivalry"]), 2),
    ]
    
    # Compute 384-D embedding
    emb384 = VectorPlacementEngine.compute_384d_text_embedding(cvp_text)
    
    entry = {
        "id": comp_id,
        "company": name,
        "sector": sector,
        "target_customer": target_cust,
        "statement_of_need": need,
        "product_name": product,
        "product_category": category,
        "statement_of_key_benefit": benefit,
        "cvp": cvp_text,
        "pestle": {
            "political": s11[0],
            "economic": s11[1],
            "social": s11[2],
            "technological": s11[3],
            "legal": s11[4],
            "environmental": s11[5],
            "details": p["details"]
        },
        "porters": {
            "threat_of_new_entrants": s11[6],
            "bargaining_power_of_buyers": s11[7],
            "bargaining_power_of_suppliers": s11[8],
            "threat_of_substitutes": s11[9],
            "competitive_rivalry": s11[10],
            "details": po["details"]
        },
        "strategic_embedding_11d": s11,
        "cvp_embedding_384d": emb384
    }
    
    assembled.append(entry)
    sector_counts[sector] = sector_counts.get(sector, 0) + 1

print("\n--- SECTOR DISTRIBUTION (24 Distinct Sectors) ---")
for s, count in sorted(sector_counts.items(), key=lambda x: -x[1]):
    print(f"  {s}: {count}")

print(f"\nTotal sectors: {len(sector_counts)}")

# Save to local workspace root: 500_companies_analysis.json
out_file_root = PROJECT_ROOT / "500_companies_analysis.json"
with open(out_file_root, "w", encoding="utf-8") as f:
    json.dump(assembled, f, indent=2)

print(f"Saved {len(assembled)} companies to {out_file_root}")

# Save to artifact brain folder
brain_dir = Path(r"C:\Users\Shrey\.gemini\antigravity-ide\brain\0d9745c6-bd98-4870-a265-488b3c7a5283")
if brain_dir.exists():
    out_brain = brain_dir / "500_companies_analysis.json"
    with open(out_brain, "w", encoding="utf-8") as f:
        json.dump(assembled, f, indent=2)
    print(f"Saved copy to artifact directory: {out_brain}")

print("\nASSEMBLY COMPLETED SUCCESSFULLY!")
