"""
Builder for Indian Data Part 1: Sectors 1 to 6 (Automotive, Banking, FinTech, IT Services, SaaS, Pharmaceuticals)
"""
import json
from pathlib import Path

comps = [
    # --- SECTOR 1: Automotive & Electric Mobility (22) ---
    (
        "Tata Motors Passenger Vehicles", "Automotive & Electric Mobility",
        "safety-conscious middle-class Indian families and modern urban commuters",
        "demand certified 5-star crash safety and reliable indigenous electric personal mobility",
        "Nexon EV & Bharat NCAP 5-Star SUV Range", "Electric & ICE Compact SUVs",
        "delivers certified 5-star structural crash safety, indigenous Ziptron EV powertrains, and extensive public charging ecosystem support",
        {"political": 0.68, "economic": 0.72, "social": 0.85, "technological": 0.82, "legal": 0.65, "environmental": 0.88},
        {
            "political": "Strong beneficiary of FAME-II, PM E-DRIVE, and Automotive PLI schemes; aligned with Ministry of Road Transport Bharat NCAP crash safety mandates.",
            "economic": "Exposed to automotive retail loan interest rate cycles and raw commodity swings (steel, lithium carbonate), offset by resilient domestic SUV demand.",
            "social": "Riding widespread societal shift prioritizing vehicle safety ratings over mere fuel efficiency, combined with high brand trust in the Tata conglomerate.",
            "technological": "Pioneered proprietary Ziptron high-voltage EV architecture, multi-mode regenerative braking, and in-house iRA connected vehicle telematics.",
            "legal": "Strictly adheres to BS-VI Phase 2 Real Driving Emissions (RDE), CAFÉ-II fleet emission targets, and AIS-156 EV battery pack safety certifications.",
            "environmental": "Accelerates zero tailpipe emission mobility across Tier-1/2 Indian cities, backed by closed-loop circular battery recycling initiatives."
        },
        {"threat_of_new_entrants": 0.25, "bargaining_power_of_buyers": 0.75, "bargaining_power_of_suppliers": 0.68, "threat_of_substitutes": 0.40, "competitive_rivalry": 0.86},
        {
            "threat_of_new_entrants": "Very low; multi-billion dollar manufacturing Capex, complex supply chains, and nationwide dealer networks form impenetrable entry moats.",
            "bargaining_power_of_buyers": "High; Indian car buyers actively cross-shop across Hyundai, Mahindra, and Kia with zero switching costs between showrooms.",
            "bargaining_power_of_suppliers": "Moderate-to-high; dependency on specialized lithium cell suppliers (Gotion, Tata AutoComp) and global automotive microcontrollers.",
            "threat_of_substitutes": "Moderate; metro rail expansions, electric two-wheelers, and ride-hailing services present alternatives in congested metros.",
            "competitive_rivalry": "Intense; continuous feature-war competition (panoramic sunroofs, Level-2 ADAS) and competitive pricing against domestic and global automakers."
        }
    ),
    (
        "Maruti Suzuki India", "Automotive & Electric Mobility",
        "value-focused first-time Indian car buyers and budget-conscious suburban families",
        "require ultra-high fuel efficiency, rock-bottom maintenance costs, and ubiquitous nationwide service accessibility",
        "Swift, Baleno & S-CNG Factory Lineup", "Fuel-Efficient Hatchbacks & Factory CNG Vehicles",
        "provides unmatched 25-35 km/kg fuel economy, the widest pan-India service and spare parts network with 4,000+ workshops, and unbeatable resale value",
        {"political": 0.62, "economic": 0.88, "social": 0.82, "technological": 0.68, "legal": 0.68, "environmental": 0.58},
        {
            "political": "Engages with Ministry of Petroleum & Natural Gas on City Gas Distribution (CGD) expansion and GST Council debates on hybrid vehicle taxation.",
            "economic": "Directly exposed to fuel price inflation, rural monsoon harvest cash flows, and discretionary purchasing power of entry-level Indian households.",
            "social": "Entrenched as the quintessential Indian family car brand symbolizing mobility democratisation and peace of mind across non-metro towns.",
            "technological": "Engineering focuses on ultra-lightweight HEARTECT crash platforms, factory-integrated dual-interdependent S-CNG ECUs, and Smart Hybrid systems.",
            "legal": "Adapting to mandatory 6-airbag regulations, updated pedestrian crash standards, and mandatory corporate average fuel economy (CAFÉ) penalties.",
            "environmental": "Promotes compressed natural gas (CNG) and strong-hybrid propulsion as pragmatic, mass-scale carbon reduction pathways for developing India."
        },
        {"threat_of_new_entrants": 0.20, "bargaining_power_of_buyers": 0.80, "bargaining_power_of_suppliers": 0.55, "threat_of_substitutes": 0.50, "competitive_rivalry": 0.88},
        {
            "threat_of_new_entrants": "Extremely low; 40+ years of entrenched vendor clusters in Gurugram/Gujarat and 3,500+ sales touchpoints are impossible to replicate.",
            "bargaining_power_of_buyers": "High; entry-segment buyers are hyper-sensitive to price differences of even ₹10,000-20,000 and easily compare financing schemes.",
            "bargaining_power_of_suppliers": "Low-to-moderate; Maruti commands immense supplier pricing leverage due to sheer 1.8M+ annual vehicle production volumes.",
            "threat_of_substitutes": "Moderate; public transit, pre-owned cars, two-wheelers, and electric three-wheelers compete for entry-level wallet share.",
            "competitive_rivalry": "Fierce; battling Hyundai, Tata Motors, and compact SUV crossover entrants encroaching into traditional hatchback territory."
        }
    ),
    (
        "Mahindra & Mahindra Automotive", "Automotive & Electric Mobility",
        "lifestyle adventure enthusiasts, rural landowners, and aspirational executive SUV buyers",
        "seek commanding high-seating road presence, rugged ladder-frame 4x4 off-road durability, and authentic butch SUV styling",
        "Scorpio-N, Thar 4x4 & XUV700", "Authentic Body-on-Frame & Monocoque Performance SUVs",
        "delivers legendary 4x4 go-anywhere off-road capability, potent mStallion turbo-petrol and mHawk diesel powertrains, and commanding road dominance",
        {"political": 0.65, "economic": 0.74, "social": 0.86, "technological": 0.78, "legal": 0.64, "environmental": 0.60},
        {
            "political": "Benefits from defense vehicle procurement contracts and indigenous manufacturing incentives, while navigating diesel vehicle regulatory restrictions.",
            "economic": "Strongly cushioned by dual rural-urban exposure, capturing both agricultural tractor/utility demand and affluent metro lifestyle SUV booms.",
            "social": "Capitalizes on deep-rooted cultural affinity for imposing SUV road presence, leisure road-tripping, and weekend overland expedition clubs.",
            "technological": "Developed high-output mHawk aluminium diesel engines, mStallion TGDi turbo-petrols, AdrenoX smart vehicle OS, and custom 4XPLOR terrain modes.",
            "legal": "Subject to National Green Tribunal (NGT) diesel lifespan caps in Delhi-NCR, stringent BS-VI Stage 2 SCR emissions, and RERA/factory safety compliances.",
            "environmental": "Investing ₹10,000+ Cr in dedicated born-electric INGLO EV architecture in Chakan to transition iconic SUV DNA into zero-carbon mobility."
        },
        {"threat_of_new_entrants": 0.22, "bargaining_power_of_buyers": 0.65, "bargaining_power_of_suppliers": 0.62, "threat_of_substitutes": 0.35, "competitive_rivalry": 0.82},
        {
            "threat_of_new_entrants": "Low; developing heavy-duty ladder-frame tooling, homologation, and durable 4x4 transfer cases requires deep specialized engineering.",
            "bargaining_power_of_buyers": "Moderate; cult-like emotional appeal and year-long waiting lists for Thar and Scorpio-N grant Mahindra significant pricing power.",
            "bargaining_power_of_suppliers": "Moderate; relies on specialized 4WD drivetrain vendors (BorgWarner, Dana) and high-tensile steel fabricators.",
            "threat_of_substitutes": "Low-to-moderate; rugged off-road recreation and rough rural terrain have virtually zero alternatives besides utility pickups.",
            "competitive_rivalry": "High; competes directly with Tata Safari/Harrier, Force Gurkha, Toyota Fortuner, and mid-size monocoque crossovers."
        }
    ),
    (
        "Royal Enfield (Eicher Motors)", "Automotive & Electric Mobility",
        "leisure motorcyclists, highway touring enthusiasts, and heritage lifestyle riders",
        "desire an authentic, thumping retro roadster aesthetic, relaxed long-distance riding posture, and camaraderie in an iconic riding brotherhood",
        "Classic 350, Hunter & Himalayan 450", "Middleweight Heritage & Adventure Motorcycles",
        "delivers the unmistakable exhaust beat of the refined J-series single-cylinder engine, timeless vintage British-Indian styling, and access to global riding communities",
        {"political": 0.58, "economic": 0.70, "social": 0.90, "technological": 0.72, "legal": 0.62, "environmental": 0.55},
        {
            "political": "Leverages Make in India export incentives to ship Chennai-manufactured middleweight motorcycles across Europe, North America, and LatAm.",
            "economic": "Thrives on discretionary premiumization in urban and Tier-2 India where upwardly mobile youth graduate from 100cc commuters to lifestyle leisure bikes.",
            "social": "World's oldest motorcycle brand in continuous production with intense cult fandom, annual Rider Mania festivals, and Himalayan expedition culture.",
            "technological": "Modernized J-series and Sherpa 450 liquid-cooled DOHC engines balance heritage character with electronic counter-balancers and Tripper navigation.",
            "legal": "Complies with strict decibel emission limits, dual-channel ABS mandates, and Euro-5+ / BS-VI Phase 2 onboard diagnostic standards.",
            "environmental": "Developing electric motorcycle prototypes under the Flying Flea sub-brand while optimizing waterless manufacturing plants in Oragadam."
        },
        {"threat_of_new_entrants": 0.28, "bargaining_power_of_buyers": 0.58, "bargaining_power_of_suppliers": 0.55, "threat_of_substitutes": 0.42, "competitive_rivalry": 0.80},
        {
            "threat_of_new_entrants": "Moderate-low; competitors like Honda (H'ness CB350), Triumph, and Harley-Davidson have attempted entry, but matching Enfield's soul is difficult.",
            "bargaining_power_of_buyers": "Moderate; customers exhibit fierce emotional brand loyalty and readily customize their motorcycles with OEM touring accessories.",
            "bargaining_power_of_suppliers": "Moderate; strong local supplier base in Tamil Nadu auto corridor (Gabriel, Endurance, Minda) ensures cost containment.",
            "threat_of_substitutes": "Moderate; sport bikes (KTM, Yamaha) and mid-range naked streetfighters attract younger demographic segments seeking raw speed.",
            "competitive_rivalry": "Intense; global partnerships (Bajaj-Triumph, Hero-Harley) specifically target Royal Enfield's 75%+ monopoly in the 250cc-750cc segment."
        }
    ),
    (
        "Ather Energy", "Automotive & Electric Mobility",
        "tech-savvy urban millennials, design purists, and premium eco-commuters",
        "seek a precision-engineered, connected electric scooter with sports car-like acceleration, predictive Google Maps navigation, and zero thermal degradation",
        "Ather 450X & Rizta Family Scooter", "Smart Premium Electric Scooters",
        "features an all-aluminum hybrid chassis, instantaneous 3.3-second 0-40 km/h Warp mode, Google-powered touchscreen dashboard with AutoHold, and Ather Grid fast charging",
        {"political": 0.72, "economic": 0.68, "social": 0.84, "technological": 0.92, "legal": 0.65, "environmental": 0.90},
        {
            "political": "Actively participates in Bureau of Indian Standards (BIS) interoperable light EV charging connector standard formulation and EMPS subsidy schemes.",
            "economic": "Targeting premium urban consumers willing to pay an upfront capital premium for significantly reduced operational running costs per kilometer.",
            "social": "Appeals to affluent early adopters who view electric mobility as a statement of design refinement, software intelligence, and environmental mindfulness.",
            "technological": "Pioneered proprietary AtherStack Linux-based vehicle OS, Google Maps dashboard integration, coasting regen algorithms, and fast-charging algorithms.",
            "legal": "Meets AIS-156 Amendment 3 strict battery thermal runaway standards, consumer protection warranty disclosures, and DPDP connected telematics laws.",
            "environmental": "Eliminates tailpipe toxic NOx and particulate emissions in congested Indian metros, utilizing IP67 waterproof aluminum-encased battery packs."
        },
        {"threat_of_new_entrants": 0.40, "bargaining_power_of_buyers": 0.70, "bargaining_power_of_suppliers": 0.72, "threat_of_substitutes": 0.52, "competitive_rivalry": 0.85},
        {
            "threat_of_new_entrants": "Moderate; numerous venture-funded EV startups attempt market entry, but building safe thermal management and dealer networks is challenging.",
            "bargaining_power_of_buyers": "High; urban consumers compare range, charging times, boot space, and upfront sticker prices across Ola, TVS iQube, and Bajaj Chetak.",
            "bargaining_power_of_suppliers": "High; dependent on international cell vendors (CATL, Samsung SDI) and specialized high-speed automotive grade processors.",
            "threat_of_substitutes": "High; traditional petrol scooters (Honda Activa, TVS Jupiter) still dominate 85%+ of overall two-wheeler retail volumes.",
            "competitive_rivalry": "Fierce; engaging in aggressive showroom expansion, price cuts, and warranty wars against deep-pocketed legacy OEMs and Ola Electric."
        }
    ),
    (
        "Ola Electric Mobility", "Automotive & Electric Mobility",
        "mass-market suburban commuters and budget-conscious daily college riders",
        "need hyper-affordable electric two-wheeler mobility with industry-leading battery range and aggressive digital pricing",
        "Ola S1 Pro & S1 X Generation 2", "Mass-Market Electric Two-Wheelers",
        "delivers high 190 km IDC certified battery range, 11 kW peak motor output, direct-to-home online delivery, and upcoming proprietary Bharat 4680 cell integration",
        {"political": 0.75, "economic": 0.78, "social": 0.80, "technological": 0.88, "legal": 0.70, "environmental": 0.88},
        {
            "political": "Leading recipient of Advanced Chemistry Cell (ACC) Battery PLI scheme subsidies, driving large-scale indigenous battery cell gigafactory setup in Tamil Nadu.",
            "economic": "Employs predatory price-disruption strategies to undercut Japanese petrol commuter two-wheelers and drive mass electrification adoption.",
            "social": "Captures youthful digital-first consumers attracted by hyper-modern minimalist aesthetics, digital smartphone unlocking, and Party Mode features.",
            "technological": "Developing indigenous 4680 cylindrical battery cells at the Ola Gigafactory and MoveOS multi-profile operating software.",
            "legal": "Facing intense scrutiny from Central Consumer Protection Authority (CCPA) over after-sales service delays, warranty claims, and showroom SLA compliances.",
            "environmental": "Accelerates zero-emission mass transit transition across India, reducing suburban reliance on imported fossil crude oil."
        },
        {"threat_of_new_entrants": 0.35, "bargaining_power_of_buyers": 0.78, "bargaining_power_of_suppliers": 0.60, "threat_of_substitutes": 0.55, "competitive_rivalry": 0.90},
        {
            "threat_of_new_entrants": "Moderate-low; massive gigafactory scale, automated mega-factory robotics, and direct D2C logistics create substantial barrier for newcomers.",
            "bargaining_power_of_buyers": "High; consumers are vocal on social platforms regarding service turnaround times and readily switch to legacy brands (TVS, Bajaj).",
            "bargaining_power_of_suppliers": "Moderate; heavy backward integration into software, chassis stamping, and upcoming in-house cell manufacturing mitigates vendor squeeze.",
            "threat_of_substitutes": "High; widespread availability of proven ICE scooters (Hero, Honda) that require zero charging planning.",
            "competitive_rivalry": "Extreme; waging high-stakes market share battles against TVS iQube, Bajaj Chetak, and Ather Energy across all state capitals."
        }
    ),
    (
        "Bajaj Auto", "Automotive & Electric Mobility",
        "aggressive performance youth riders and global export two-wheeler buyers",
        "demand pulse-racing street naked acceleration, muscular styling, and bulletproof mechanical reliability",
        "Pulsar & Dominar Sports Lineup", "Performance Street Motorcycles",
        "features patented DTS-i twin/triple spark liquid-cooled engines, perimeter frame handling, and engineering export presence across 70+ countries",
        {"political": 0.60, "economic": 0.72, "social": 0.82, "technological": 0.75, "legal": 0.62, "environmental": 0.62},
        {
            "political": "Benefits from foreign trade policy export duty drawdowns and bilateral export agreements into Africa, Southeast Asia, and Latin America.",
            "economic": "Hedging domestic demand cycles with significant foreign exchange earnings from two-wheeler and three-wheeler exports worldwide.",
            "social": "Created the 'Definitely Male' sports motorcycling craze in India, embedding Pulsar as an enduring status symbol for young aspirational men.",
            "technological": "Partnerships with KTM, Husqvarna, and Triumph (Speed 400) allow cross-pollination of precision liquid-cooled engineering and ride-by-wire.",
            "legal": "Complies with global homologation standards, dual-channel anti-lock braking regulations, and BS-VI onboard diagnostic monitoring.",
            "environmental": "Reviving the Chetak brand in an elegant all-metal electric avatar and pioneering the world's first mass-production CNG motorcycle (Freedom 125)."
        },
        {"threat_of_new_entrants": 0.25, "bargaining_power_of_buyers": 0.70, "bargaining_power_of_suppliers": 0.58, "threat_of_substitutes": 0.45, "competitive_rivalry": 0.85},
        {
            "threat_of_new_entrants": "Low; establishing massive 5-million vehicle manufacturing capacity and global distribution in 70 countries takes decades.",
            "bargaining_power_of_buyers": "Moderate-high; youthful buyers demand constant cosmetic updates, USD forks, and Bluetooth connectivity before committing funds.",
            "bargaining_power_of_suppliers": "Low-to-moderate; long-standing vendor relationships in the Chakan auto-belt ensure low component costs and reliable delivery.",
            "threat_of_substitutes": "Moderate; lifestyle retro roadsters (Royal Enfield) and entry-level electric bikes compete for youth transportation budgets.",
            "competitive_rivalry": "High; engaged in intense horsepower battles against TVS Apache, Yamaha MT-15, and Honda Hornet."
        }
    ),
    (
        "TVS Motor Company", "Automotive & Electric Mobility",
        "racing track enthusiasts and discerning urban commuters",
        "seek racing-derived high-rpm throttle response, razor-sharp chassis cornering, and connected smartphone telemetry",
        "Apache RTR & iQube Electric Series", "Track-Tuned Motorcycles & Smart Electric Scooters",
        "delivers race-tuned fuel injection (RT-FI), SmartXonnect Bluetooth race telemetry with lean angle displays, and reliable build quality",
        {"political": 0.62, "economic": 0.70, "social": 0.82, "technological": 0.84, "legal": 0.64, "environmental": 0.75},
        {
            "political": "Participates in government EV incentive programs and co-develops small-displacement motorcycles with BMW Motorrad under Make in India.",
            "economic": "Strong multi-segment revenue streams balancing commuter scooters (Jupiter), high-margin sports bikes (Apache), and electric two-wheelers.",
            "social": "Deep roots in competitive motorsport through TVS Racing, India's oldest factory racing team, fostering a passionate youth racing fanbase.",
            "technological": "Engineering excellence with race-tuned slipper clutches, adjustable Showa suspension, riding modes (Rain, Urban, Sport), and connected clusters.",
            "legal": "Compliance with AIS battery safety rules, automated lighting regulations, and European UNECE safety norms for export vehicles.",
            "environmental": "Accelerating transition to clean transport through the successful TVS iQube electric scooter and acquiring iconic British brand Norton to engineer EV superbikes."
        },
        {"threat_of_new_entrants": 0.26, "bargaining_power_of_buyers": 0.72, "bargaining_power_of_suppliers": 0.58, "threat_of_substitutes": 0.46, "competitive_rivalry": 0.85},
        {
            "threat_of_new_entrants": "Low; R&D capabilities, wind tunnel testing facilities in Hosur, and 1,000+ dealership networks protect incumbent position.",
            "bargaining_power_of_buyers": "Moderate-high; customers can choose between Bajaj Pulsar, Yamaha, and Ather across sports and electric categories.",
            "bargaining_power_of_suppliers": "Moderate; balanced supply chain network with specialized electronics suppliers for digital TFT dashboards.",
            "threat_of_substitutes": "Moderate; public transit and shared ride platforms offer everyday transportation alternatives.",
            "competitive_rivalry": "Intense; battling head-to-head with Bajaj in 160-310cc motorcycles and with Ather/Ola in electric scooters."
        }
    )
]

print(f"Sample contains {len(comps)} companies.")
