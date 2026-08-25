"""Hidden ground-truth generation module for the fabricated startup dataset.

This module is intentionally NOT imported by the learning/inference pipeline
(src/marketintel/analysis.py, train_interaction_matrix.py, app.py) - only by
simulate_profit_history.py (to inject shocks) and derive_sensitivity_profiles.py
(to validate what the lag-regression recovers). Each of the 20 fabricated
startups gets a hidden PESTLE/Porter's sensitivity template - domain-consistent
by design (e.g. an import-dependent hardware startup gets high hidden
political/economic sensitivity; a domestic SaaS startup gets low PESTLE
sensitivity and higher competitive-rivalry sensitivity) - and a hidden
profit-shock lag. Neither is ever written to data/startups.json: the
*recovered* sensitivity profile, derived from the fabricated profit history in
derive_sensitivity_profiles.py, is what actually supervises the shared matrix
W - not this.

shock_lag_days cycles through the same four candidate lags the recovery step
searches over (1, 3, 7, 14), five startups per lag, so the recovery pipeline
gets exercised against every candidate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import CANDIDATE_LAGS  # noqa: E402

HIDDEN_TEMPLATES = {
    "RupeeRail": dict(
        pestle=dict(political=-60, economic=-30, social=40, technological=50, legal=-70, environmental=5),
        porters=dict(threat_new_entrants=-50, supplier_power=-20, buyer_power=-30, threat_substitutes=-40, competitive_rivalry=-60),
    ),
    "LedgerLoop": dict(
        pestle=dict(political=10, economic=15, social=10, technological=55, legal=65, environmental=0),
        porters=dict(threat_new_entrants=-55, supplier_power=5, buyer_power=-25, threat_substitutes=-35, competitive_rivalry=-60),
    ),
    "CoverNest": dict(
        pestle=dict(political=-35, economic=-25, social=60, technological=45, legal=-55, environmental=-20),
        porters=dict(threat_new_entrants=-45, supplier_power=-15, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-40),
    ),
    "SkillSprout": dict(
        pestle=dict(political=20, economic=25, social=70, technological=50, legal=-10, environmental=0),
        porters=dict(threat_new_entrants=-50, supplier_power=5, buyer_power=-30, threat_substitutes=-40, competitive_rivalry=-55),
    ),
    "CampusOS": dict(
        pestle=dict(political=15, economic=10, social=35, technological=55, legal=20, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    "ExamAnt": dict(
        pestle=dict(political=0, economic=15, social=45, technological=65, legal=-15, environmental=10),
        porters=dict(threat_new_entrants=-55, supplier_power=0, buyer_power=-25, threat_substitutes=-50, competitive_rivalry=-60),
    ),
    "Krishimitra": dict(
        pestle=dict(political=25, economic=20, social=50, technological=55, legal=10, environmental=75),
        porters=dict(threat_new_entrants=-35, supplier_power=-40, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-30),
    ),
    "AgriChain Direct": dict(
        pestle=dict(political=-20, economic=45, social=35, technological=30, legal=-45, environmental=20),
        porters=dict(threat_new_entrants=-30, supplier_power=-25, buyer_power=-35, threat_substitutes=-20, competitive_rivalry=-40),
    ),
    "FarmYield Finance": dict(
        pestle=dict(political=-30, economic=-35, social=55, technological=50, legal=-50, environmental=-65),
        porters=dict(threat_new_entrants=-40, supplier_power=-10, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-35),
    ),
    "Wattlefy": dict(
        pestle=dict(political=-55, economic=-60, social=30, technological=40, legal=-25, environmental=45),
        porters=dict(threat_new_entrants=-30, supplier_power=-70, buyer_power=-35, threat_substitutes=-30, competitive_rivalry=-35),
    ),
    "PureDrop": dict(
        pestle=dict(political=15, economic=10, social=40, technological=25, legal=-15, environmental=-40),
        porters=dict(threat_new_entrants=-35, supplier_power=-30, buyer_power=-30, threat_substitutes=-25, competitive_rivalry=-45),
    ),
    "MotoCharge": dict(
        pestle=dict(political=-45, economic=-50, social=35, technological=45, legal=-20, environmental=60),
        porters=dict(threat_new_entrants=-40, supplier_power=-65, buyer_power=-25, threat_substitutes=-30, competitive_rivalry=-40),
    ),
    "DeskLoop": dict(
        pestle=dict(political=5, economic=10, social=10, technological=40, legal=40, environmental=0),
        porters=dict(threat_new_entrants=-45, supplier_power=0, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-55),
    ),
    "RouteIQ": dict(
        pestle=dict(political=0, economic=20, social=5, technological=55, legal=0, environmental=25),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-30, threat_substitutes=-35, competitive_rivalry=-50),
    ),
    "ClauseCraft": dict(
        pestle=dict(political=5, economic=10, social=5, technological=50, legal=60, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-25, threat_substitutes=-45, competitive_rivalry=-50),
    ),
    "PulseDesk": dict(
        pestle=dict(political=-10, economic=-15, social=0, technological=55, legal=-15, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=0, buyer_power=-25, threat_substitutes=-50, competitive_rivalry=-65),
    ),
    "VitalsBridge": dict(
        pestle=dict(political=-20, economic=-30, social=55, technological=50, legal=-35, environmental=10),
        porters=dict(threat_new_entrants=-30, supplier_power=-45, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-35),
    ),
    "TeleCare Punjab": dict(
        pestle=dict(political=25, economic=10, social=65, technological=35, legal=-30, environmental=-15),
        porters=dict(threat_new_entrants=-35, supplier_power=-10, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-30),
    ),
    "MedStock AI": dict(
        pestle=dict(political=0, economic=15, social=20, technological=50, legal=15, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=-15, buyer_power=-20, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    "GlowLine Cosmeceuticals": dict(
        pestle=dict(political=10, economic=15, social=45, technological=15, legal=-10, environmental=-25),
        porters=dict(threat_new_entrants=-50, supplier_power=-20, buyer_power=-35, threat_substitutes=-30, competitive_rivalry=-60),
    ),
}

# Assign shock lags deterministically, cycling through the candidates so all
# four are exercised evenly across the 20 startups.
for i, name in enumerate(HIDDEN_TEMPLATES):
    HIDDEN_TEMPLATES[name]["shock_lag_days"] = CANDIDATE_LAGS[i % len(CANDIDATE_LAGS)]
