"""
Sector 1 to 6 Definitions for 500 Indian Benchmark Companies
"""

SECTORS_BATCH_1 = [
    # Sector 1: Automotive & Electric Mobility (22 companies)
    {
        "company": "Tata Motors Passenger Vehicles",
        "sector": "Automotive & Electric Mobility",
        "target_customer": "safety-conscious middle-class Indian families and modern urban commuters",
        "statement_of_need": "demand certified 5-star crash safety and reliable indigenous electric personal mobility",
        "product_name": "Nexon EV & Bharat NCAP 5-Star SUV Range",
        "product_category": "Electric & ICE Compact SUVs",
        "statement_of_key_benefit": "delivers certified 5-star structural crash safety, indigenous Ziptron EV powertrains, and extensive public charging ecosystem support",
        "pestle": {
            "political": 0.68, "economic": 0.72, "social": 0.85, "technological": 0.82, "legal": 0.65, "environmental": 0.88,
            "details": {
                "political": "Strong beneficiary of FAME-II, PM E-DRIVE, and Automotive PLI schemes; aligned with Ministry of Road Transport Bharat NCAP crash safety mandates.",
                "economic": "Exposed to automotive retail loan interest rate cycles and raw commodity swings (steel, lithium carbonate), offset by resilient domestic SUV demand.",
                "social": "Riding widespread societal shift prioritizing vehicle safety ratings over mere fuel efficiency, combined with high brand trust in the Tata conglomerate.",
                "technological": "Pioneered proprietary Ziptron high-voltage EV architecture, multi-mode regenerative braking, and in-house iRA connected vehicle telematics.",
                "legal": "Strictly adheres to BS-VI Phase 2 Real Driving Emissions (RDE), CAFÉ-II fleet emission targets, and AIS-156 EV battery pack safety certifications.",
                "environmental": "Accelerates zero tailpipe emission mobility across Tier-1/2 Indian cities, backed by closed-loop circular battery recycling initiatives."
            }
        },
        "porters": {
            "threat_of_new_entrants": 0.25, "bargaining_power_of_buyers": 0.75, "bargaining_power_of_suppliers": 0.68, "threat_of_substitutes": 0.40, "competitive_rivalry": 0.86,
            "details": {
                "threat_of_new_entrants": "Very low; multi-billion dollar manufacturing Capex, complex supply chains, and nationwide dealer networks form impenetrable entry moats.",
                "bargaining_power_of_buyers": "High; Indian car buyers actively cross-shop across Hyundai, Mahindra, and Kia with zero switching costs between showrooms.",
                "bargaining_power_of_suppliers": "Moderate-to-high; dependency on specialized lithium cell suppliers (Gotion, Tata AutoComp) and global automotive microcontrollers.",
                "threat_of_substitutes": "Moderate; metro rail expansions, electric two-wheelers, and ride-hailing services present alternatives in congested metros.",
                "competitive_rivalry": "Intense; continuous feature-war competition (panoramic sunroofs, Level-2 ADAS) and competitive pricing against domestic and global automakers."
            }
        }
    },
    {
        "company": "Maruti Suzuki India",
        "sector": "Automotive & Electric Mobility",
        "target_customer": "value-focused first-time Indian car buyers and budget-conscious suburban families",
        "statement_of_need": "require ultra-high fuel efficiency, rock-bottom maintenance costs, and ubiquitous nationwide service accessibility",
        "product_name": "Swift, Baleno & S-CNG Factory Lineup",
        "product_category": "Fuel-Efficient Hatchbacks & Factory CNG Vehicles",
        "statement_of_key_benefit": "provides unmatched 25-35 km/kg fuel economy, the widest pan-India service and spare parts network with 4,000+ workshops, and unbeatable resale value",
        "pestle": {
            "political": 0.62, "economic": 0.88, "social": 0.82, "technological": 0.68, "legal": 0.68, "environmental": 0.58,
            "details": {
                "political": "Engages with Ministry of Petroleum & Natural Gas on City Gas Distribution (CGD) expansion and GST Council debates on hybrid vehicle taxation.",
                "economic": "Directly exposed to fuel price inflation, rural monsoon harvest cash flows, and discretionary purchasing power of entry-level Indian households.",
                "social": "Entrenched as the quintessential Indian family car brand symbolizing mobility democratisation and peace of mind across non-metro towns.",
                "technological": "Engineering focuses on ultra-lightweight HEARTECT crash platforms, factory-integrated dual-interdependent S-CNG ECUs, and Smart Hybrid systems.",
                "legal": "Adapting to mandatory 6-airbag regulations, updated pedestrian crash standards, and mandatory corporate average fuel economy (CAFÉ) penalties.",
                "environmental": "Promotes compressed natural gas (CNG) and strong-hybrid propulsion as pragmatic, mass-scale carbon reduction pathways for developing India."
            }
        },
        "porters": {
            "threat_of_new_entrants": 0.20, "bargaining_power_of_buyers": 0.80, "bargaining_power_of_suppliers": 0.55, "threat_of_substitutes": 0.50, "competitive_rivalry": 0.88,
            "details": {
                "threat_of_new_entrants": "Extremely low; 40+ years of entrenched vendor clusters in Gurugram/Gujarat and 3,500+ sales touchpoints are impossible to replicate.",
                "bargaining_power_of_buyers": "High; entry-segment buyers are hyper-sensitive to price differences of even ₹10,000-20,000 and easily compare financing schemes.",
                "bargaining_power_of_suppliers": "Low-to-moderate; Maruti commands immense supplier pricing leverage due to sheer 1.8M+ annual vehicle production volumes.",
                "threat_of_substitutes": "Moderate; public transit, pre-owned cars, two-wheelers, and electric three-wheelers compete for entry-level wallet share.",
                "competitive_rivalry": "Fierce; battling Hyundai, Tata Motors, and compact SUV crossover entrants encroaching into traditional hatchback territory."
            }
        }
    },
    {
        "company": "Mahindra & Mahindra Automotive",
        "sector": "Automotive & Electric Mobility",
        "target_customer": "lifestyle adventure enthusiasts, rural landowners, and aspirational executive SUV buyers",
        "statement_of_need": "seek commanding high-seating road presence, rugged ladder-frame 4x4 off-road durability, and authentic butch SUV styling",
        "product_name": "Scorpio-N, Thar 4x4 & XUV700",
        "product_category": "Authentic Body-on-Frame & Monocoque Performance SUVs",
        "statement_of_key_benefit": "delivers legendary 4x4 go-anywhere off-road capability, potent mStallion turbo-petrol and mHawk diesel powertrains, and commanding road dominance",
        "pestle": {
            "political": 0.65, "economic": 0.74, "social": 0.86, "technological": 0.78, "legal": 0.64, "environmental": 0.60,
            "details": {
                "political": "Benefits from defense vehicle procurement contracts and indigenous manufacturing incentives, while navigating diesel vehicle regulatory restrictions.",
                "economic": "Strongly cushioned by dual rural-urban exposure, capturing both agricultural tractor/utility demand and affluent metro lifestyle SUV booms.",
                "social": "Capitalizes on deep-rooted cultural affinity for imposing SUV road presence, leisure road-tripping, and weekend overland expedition clubs.",
                "technological": "Developed high-output mHawk aluminium diesel engines, mStallion TGDi turbo-petrols, AdrenoX smart vehicle OS, and custom 4XPLOR terrain modes.",
                "legal": "Subject to National Green Tribunal (NGT) diesel lifespan caps in Delhi-NCR, stringent BS-VI Stage 2 SCR emissions, and RERA/factory safety compliances.",
                "environmental": "Investing ₹10,000+ Cr in dedicated born-electric INGLO EV architecture in Chakan to transition iconic SUV DNA into zero-carbon mobility."
            }
        },
        "porters": {
            "threat_of_new_entrants": 0.22, "bargaining_power_of_buyers": 0.65, "bargaining_power_of_suppliers": 0.62, "threat_of_substitutes": 0.35, "competitive_rivalry": 0.82,
            "details": {
                "threat_of_new_entrants": "Low; developing heavy-duty ladder-frame tooling, homologation, and durable 4x4 transfer cases requires deep specialized engineering.",
                "bargaining_power_of_buyers": "Moderate; cult-like emotional appeal and year-long waiting lists for Thar and Scorpio-N grant Mahindra significant pricing power.",
                "bargaining_power_of_suppliers": "Moderate; relies on specialized 4WD drivetrain vendors (BorgWarner, Dana) and high-tensile steel fabricators.",
                "threat_of_substitutes": "Low-to-moderate; rugged off-road recreation and rough rural terrain have virtually zero alternatives besides utility pickups.",
                "competitive_rivalry": "High; competes directly with Tata Safari/Harrier, Force Gurkha, Toyota Fortuner, and mid-size monocoque crossovers."
            }
        }
    },
    {
        "company": "Royal Enfield (Eicher Motors)",
        "sector": "Automotive & Electric Mobility",
        "target_customer": "leisure motorcyclists, highway touring enthusiasts, and heritage lifestyle riders",
        "statement_of_need": "desire an authentic, thumping retro roadster aesthetic, relaxed long-distance riding posture, and camaraderie in an iconic riding brotherhood",
        "product_name": "Classic 350, Hunter & Himalayan 450",
        "product_category": "Middleweight Heritage & Adventure Motorcycles",
        "statement_of_key_benefit": "delivers the unmistakable exhaust beat of the refined J-series single-cylinder engine, timeless vintage British-Indian styling, and access to global riding communities",
        "pestle": {
            "political": 0.58, "economic": 0.70, "social": 0.90, "technological": 0.72, "legal": 0.62, "environmental": 0.55,
            "details": {
                "political": "Leverages Make in India export incentives to ship Chennai-manufactured middleweight motorcycles across Europe, North America, and LatAm.",
                "economic": "Thrives on discretionary premiumization in urban and Tier-2 India where upwardly mobile youth graduate from 100cc commuters to lifestyle leisure bikes.",
                "social": "World's oldest motorcycle brand in continuous production with intense cult fandom, annual Rider Mania festivals, and Himalayan expedition culture.",
                "technological": "Modernized J-series and Sherpa 450 liquid-cooled DOHC engines balance heritage character with electronic counter-balancers and Tripper navigation.",
                "legal": "Complies with strict decibel emission limits, dual-channel ABS mandates, and Euro-5+ / BS-VI Phase 2 onboard diagnostic standards.",
                "environmental": "Developing electric motorcycle prototypes under the Flying Flea sub-brand while optimizing waterless manufacturing plants in Oragadam."
            }
        },
        "porters": {
            "threat_of_new_entrants": 0.28, "bargaining_power_of_buyers": 0.58, "bargaining_power_of_suppliers": 0.55, "threat_of_substitutes": 0.42, "competitive_rivalry": 0.80,
            "details": {
                "threat_of_new_entrants": "Moderate-low; competitors like Honda (H'ness CB350), Triumph, and Harley-Davidson have attempted entry, but matching Enfield's soul is difficult.",
                "bargaining_power_of_buyers": "Moderate; customers exhibit fierce emotional brand loyalty and readily customize their motorcycles with OEM touring accessories.",
                "bargaining_power_of_suppliers": "Moderate; strong local supplier base in Tamil Nadu auto corridor (Gabriel, Endurance, Minda) ensures cost containment.",
                "threat_of_substitutes": "Moderate; sport bikes (KTM, Yamaha) and mid-range naked streetfighters attract younger demographic segments seeking raw speed.",
                "competitive_rivalry": "Intense; global partnerships (Bajaj-Triumph, Hero-Harley) specifically target Royal Enfield's 75%+ monopoly in the 250cc-750cc segment."
            }
        }
    },
    {
        "company": "Ather Energy",
        "sector": "Automotive & Electric Mobility",
        "target_customer": "tech-savvy urban millennials, design purists, and premium eco-commuters",
        "statement_of_need": "seek a precision-engineered, connected electric scooter with sports car-like acceleration, predictive Google Maps navigation, and zero thermal degradation",
        "product_name": "Ather 450X & Rizta Family Scooter",
        "product_category": "Smart Premium Electric Scooters",
        "statement_of_key_benefit": "features an all-aluminum hybrid chassis, instantaneous 3.3-second 0-40 km/h Warp mode, Google-powered touchscreen dashboard with AutoHold, and Ather Grid fast charging",
        "pestle": {
            "political": 0.72, "economic": 0.68, "social": 0.84, "technological": 0.92, "legal": 0.65, "environmental": 0.90,
            "details": {
                "political": "Actively participates in Bureau of Indian Standards (BIS) interoperable light EV charging connector standard formulation and EMPS subsidy schemes.",
                "economic": "Targeting premium urban consumers willing to pay an upfront capital premium for significantly reduced operational running costs per kilometer.",
                "social": "Appeals to affluent early adopters who view electric mobility as a statement of design refinement, software intelligence, and environmental mindfulness.",
                "technological": "Pioneered proprietary AtherStack Linux-based vehicle OS, Google Maps dashboard integration, coasting regen algorithms, and fast-charging algorithms.",
                "legal": "Meets AIS-156 Amendment 3 strict battery thermal runaway standards, consumer protection warranty disclosures, and DPDP connected telematics laws.",
                "environmental": "Eliminates tailpipe toxic NOx and particulate emissions in congested Indian metros, utilizing IP67 waterproof aluminum-encased battery packs."
            }
        },
        "porters": {
            "threat_of_new_entrants": 0.40, "bargaining_power_of_buyers": 0.70, "bargaining_power_of_suppliers": 0.72, "threat_of_substitutes": 0.52, "competitive_rivalry": 0.85,
            "details": {
                "threat_of_new_entrants": "Moderate; numerous venture-funded EV startups attempt market entry, but building safe thermal management and dealer networks is challenging.",
                "bargaining_power_of_buyers": "High; urban consumers compare range, charging times, boot space, and upfront sticker prices across Ola, TVS iQube, and Bajaj Chetak.",
                "bargaining_power_of_suppliers": "High; dependent on international cell vendors (CATL, Samsung SDI) and specialized high-speed automotive grade processors.",
                "threat_of_substitutes": "High; traditional petrol scooters (Honda Activa, TVS Jupiter) still dominate 85%+ of overall two-wheeler retail volumes.",
                "competitive_rivalry": "Fierce; engaging in aggressive showroom expansion, price cuts, and warranty wars against deep-pocketed legacy OEMs and Ola Electric."
            }
        }
    }
]
