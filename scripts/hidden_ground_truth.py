"""Hidden ground-truth generation module for the fabricated startup dataset.

This module is intentionally NOT imported by the learning/inference pipeline
(src/marketintel/analysis.py, train_interaction_matrix.py, app.py) - only by
simulate_profit_history.py (to inject shocks) and derive_sensitivity_profiles.py
(to validate what the lag-regression recovers). Each of the 50 fabricated
startups gets a hidden PESTLE/Porter's sensitivity template - domain-consistent
by design (e.g. an import-dependent hardware startup gets high hidden
political/economic sensitivity; a domestic SaaS startup gets low PESTLE
sensitivity and higher competitive-rivalry sensitivity) - and a hidden
profit-shock lag. Neither is ever written to data/startups.json: the
*recovered* sensitivity profile, derived from the fabricated profit history in
derive_sensitivity_profiles.py, is what actually supervises the shared matrix
W - not this.

Grew from 20 to 50 startups (10 new domain archetypes x 3, on top of the
original 6 x ~3-4) after the 20-startup version produced a W with effective
rank ~5 - nowhere near enough distinct CVP directions for the 384x384
bilinear form to discriminate between genuinely different businesses (a
constructed test found unrelated CVPs, including gibberish, produced >0.98
cosine-similar output patterns). More domains, not just more instances of
existing ones, since the goal is more genuinely distinct hidden sensitivity
PATTERNS for W to learn from, not just a larger sample of similar ones.

shock_lag_days cycles through the same four candidate lags the recovery step
searches over (1, 3, 7, 14), roughly evenly across all startups, so the
recovery pipeline gets exercised against every candidate.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import CANDIDATE_LAGS, PESTLE_DIMS, PORTERS_DIMS  # noqa: E402

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
    # --- Expansion set: 30 more startups (10 new domain archetypes x 3) added
    # after the original 20 produced a matrix W with effective rank ~5 - too
    # few unique CVP directions (20) to support meaningful discrimination in a
    # 384x384 bilinear form. More domains, not just more startups per existing
    # domain, since the goal is genuinely distinct hidden sensitivity PATTERNS,
    # not more instances of patterns already represented.
    "SolarKhet": dict(
        pestle=dict(political=40, economic=25, social=20, technological=30, legal=15, environmental=75),
        porters=dict(threat_new_entrants=-30, supplier_power=-50, buyer_power=-15, threat_substitutes=-20, competitive_rivalry=-30),
    ),
    "WindLoop": dict(
        pestle=dict(political=25, economic=20, social=10, technological=45, legal=10, environmental=65),
        porters=dict(threat_new_entrants=-35, supplier_power=-30, buyer_power=-10, threat_substitutes=-25, competitive_rivalry=-25),
    ),
    "GreenGrid Storage": dict(
        pestle=dict(political=35, economic=30, social=10, technological=40, legal=15, environmental=60),
        porters=dict(threat_new_entrants=-25, supplier_power=-60, buyer_power=-20, threat_substitutes=-15, competitive_rivalry=-30),
    ),
    "CargoLane": dict(
        pestle=dict(political=-25, economic=-45, social=15, technological=30, legal=-15, environmental=-10),
        porters=dict(threat_new_entrants=-45, supplier_power=-20, buyer_power=-35, threat_substitutes=-30, competitive_rivalry=-55),
    ),
    "ColdTrail": dict(
        pestle=dict(political=-15, economic=-35, social=20, technological=35, legal=-20, environmental=-30),
        porters=dict(threat_new_entrants=-30, supplier_power=-45, buyer_power=-20, threat_substitutes=-15, competitive_rivalry=-35),
    ),
    "LastMile Express": dict(
        pestle=dict(political=-10, economic=-40, social=25, technological=25, legal=-10, environmental=-15),
        porters=dict(threat_new_entrants=-50, supplier_power=-15, buyer_power=-40, threat_substitutes=-35, competitive_rivalry=-60),
    ),
    "BasaiHomes": dict(
        pestle=dict(political=-30, economic=25, social=20, technological=20, legal=-50, environmental=0),
        porters=dict(threat_new_entrants=-30, supplier_power=-10, buyer_power=-45, threat_substitutes=-20, competitive_rivalry=-30),
    ),
    "RentEase": dict(
        pestle=dict(political=10, economic=15, social=30, technological=25, legal=-35, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-35, threat_substitutes=-25, competitive_rivalry=-40),
    ),
    "PlotVerify": dict(
        pestle=dict(political=-20, economic=10, social=15, technological=40, legal=-60, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=0, buyer_power=-20, threat_substitutes=-15, competitive_rivalry=-25),
    ),
    "TiffinNet": dict(
        pestle=dict(political=0, economic=20, social=55, technological=25, legal=-15, environmental=5),
        porters=dict(threat_new_entrants=-45, supplier_power=-10, buyer_power=-40, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    "HarvestBox": dict(
        pestle=dict(political=15, economic=30, social=40, technological=20, legal=-10, environmental=25),
        porters=dict(threat_new_entrants=-30, supplier_power=-25, buyer_power=-30, threat_substitutes=-20, competitive_rivalry=-35),
    ),
    "QuickBite Cloud Kitchens": dict(
        pestle=dict(political=-5, economic=25, social=35, technological=30, legal=-20, environmental=0),
        porters=dict(threat_new_entrants=-50, supplier_power=-15, buyer_power=-35, threat_substitutes=-40, competitive_rivalry=-55),
    ),
    "ChargeGrid": dict(
        pestle=dict(political=-35, economic=-40, social=15, technological=35, legal=-15, environmental=55),
        porters=dict(threat_new_entrants=-30, supplier_power=-55, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-30),
    ),
    "SwapStation": dict(
        pestle=dict(political=-30, economic=-35, social=20, technological=40, legal=-10, environmental=50),
        porters=dict(threat_new_entrants=-25, supplier_power=-60, buyer_power=-15, threat_substitutes=-20, competitive_rivalry=-35),
    ),
    "CampusRide": dict(
        pestle=dict(political=10, economic=-15, social=30, technological=25, legal=0, environmental=45),
        porters=dict(threat_new_entrants=-35, supplier_power=-30, buyer_power=-25, threat_substitutes=-30, competitive_rivalry=-25),
    ),
    "ShieldStack": dict(
        pestle=dict(political=0, economic=10, social=5, technological=60, legal=45, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-20, threat_substitutes=-35, competitive_rivalry=-50),
    ),
    "PhishGuard": dict(
        pestle=dict(political=0, economic=5, social=15, technological=55, legal=30, environmental=0),
        porters=dict(threat_new_entrants=-45, supplier_power=0, buyer_power=-25, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    "DataVault Compliance": dict(
        pestle=dict(political=5, economic=10, social=5, technological=50, legal=65, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=0, buyer_power=-15, threat_substitutes=-25, competitive_rivalry=-40),
    ),
    "HireLoop": dict(
        pestle=dict(political=0, economic=15, social=45, technological=35, legal=10, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-25, threat_substitutes=-30, competitive_rivalry=-45),
    ),
    "PayrollPe": dict(
        pestle=dict(political=5, economic=10, social=20, technological=30, legal=50, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-45),
    ),
    "CulturePulse": dict(
        pestle=dict(political=0, economic=5, social=40, technological=30, legal=10, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=0, buyer_power=-20, threat_substitutes=-25, competitive_rivalry=-40),
    ),
    "ClaimSwift": dict(
        pestle=dict(political=-20, economic=15, social=35, technological=40, legal=-45, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=-10, buyer_power=-25, threat_substitutes=-20, competitive_rivalry=-35),
    ),
    "CropShield": dict(
        pestle=dict(political=20, economic=-20, social=50, technological=30, legal=-40, environmental=-60),
        porters=dict(threat_new_entrants=-30, supplier_power=-10, buyer_power=-15, threat_substitutes=-20, competitive_rivalry=-25),
    ),
    "PetCare Plus": dict(
        pestle=dict(political=0, economic=15, social=45, technological=20, legal=-30, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=-5, buyer_power=-30, threat_substitutes=-25, competitive_rivalry=-35),
    ),
    "BuildMart Direct": dict(
        pestle=dict(political=-10, economic=35, social=10, technological=20, legal=-15, environmental=0),
        porters=dict(threat_new_entrants=-35, supplier_power=-30, buyer_power=-30, threat_substitutes=-20, competitive_rivalry=-45),
    ),
    "TexSource": dict(
        pestle=dict(political=-15, economic=40, social=15, technological=15, legal=-10, environmental=0),
        porters=dict(threat_new_entrants=-30, supplier_power=-35, buyer_power=-25, threat_substitutes=-15, competitive_rivalry=-40),
    ),
    "SparePartHub": dict(
        pestle=dict(political=-20, economic=30, social=10, technological=20, legal=-20, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=-25, buyer_power=-35, threat_substitutes=-30, competitive_rivalry=-50),
    ),
    "QuizArena": dict(
        pestle=dict(political=-5, economic=10, social=55, technological=45, legal=-15, environmental=0),
        porters=dict(threat_new_entrants=-50, supplier_power=0, buyer_power=-25, threat_substitutes=-45, competitive_rivalry=-55),
    ),
    "StoryStack": dict(
        pestle=dict(political=0, economic=10, social=50, technological=35, legal=-10, environmental=0),
        porters=dict(threat_new_entrants=-45, supplier_power=0, buyer_power=-20, threat_substitutes=-40, competitive_rivalry=-50),
    ),
    "CampusLeague": dict(
        pestle=dict(political=0, economic=15, social=60, technological=30, legal=0, environmental=0),
        porters=dict(threat_new_entrants=-40, supplier_power=0, buyer_power=-25, threat_substitutes=-35, competitive_rivalry=-45),
    ),
}

# Assign shock lags deterministically, cycling through the candidates so all
# four are exercised evenly across the startups.
for i, name in enumerate(HIDDEN_TEMPLATES):
    HIDDEN_TEMPLATES[name]["shock_lag_days"] = CANDIDATE_LAGS[i % len(CANDIDATE_LAGS)]

# Idiosyncratic per-startup variation, added on top of the hand-authored domain
# archetypes above. Diagnosed directly: even after growing from 20 to 50
# startups across 10 new domain archetypes, the 50x11 matrix of hand-authored
# templates had an effective rank of only ~4.3 (PC1 alone explained 35% of
# variance) - because "domain-consistent by design" meant every startup in a
# given domain was hand-written to roughly the SAME archetypal shape, just
# rescaled. That's realistic for the shared component of a business's
# sensitivity, but real businesses in the same domain aren't identical, and a
# ground-truth set this low-dimensional caps how much the shared matrix W can
# ever discriminate between businesses downstream - no fitting procedure can
# manufacture information the training targets don't contain. This adds a
# fixed, reproducible per-startup, per-dimension perturbation (std=25 on the
# -100..100 scale) representing that idiosyncratic variation - large enough to
# noticeably raise the templates' effective rank (~4.3 -> ~7-8, empirically),
# small enough that a startup's SIGN and rough magnitude on its
# domain-defining dimensions still reads as consistent with its business.
_rng = np.random.default_rng(2024)
for name, template in HIDDEN_TEMPLATES.items():
    for d in PESTLE_DIMS:
        template["pestle"][d] = float(np.clip(template["pestle"][d] + _rng.normal(0, 25), -100, 100))
    for d in PORTERS_DIMS:
        template["porters"][d] = float(np.clip(template["porters"][d] + _rng.normal(0, 25), -100, 100))
