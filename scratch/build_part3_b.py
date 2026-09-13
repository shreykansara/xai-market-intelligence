"""
Omniscope AI - Part 3B Generator
Builds Sectors 16, 17, 18 (62 companies):
- Sector 16: Metals, Mining & Heavy Materials (20 companies)
- Sector 17: Infrastructure, EPC & Capital Goods (22 companies)
- Sector 18: Real Estate & Commercial Development (20 companies)
Combines with scratch/part3_a.json to produce scratch/part3.json (122 companies).
"""
import json
from pathlib import Path

part3_b = []

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    part3_b.append({
        "company": name,
        "sector": sector,
        "target_customer": customer,
        "statement_of_need": need,
        "product_name": product,
        "product_category": category,
        "statement_of_key_benefit": benefit,
        "pestle": {
            "political": p_scores[0], "economic": p_scores[1], "social": p_scores[2],
            "technological": p_scores[3], "legal": p_scores[4], "environmental": p_scores[5],
            "details": p_det
        },
        "porters": {
            "threat_of_new_entrants": po_scores[0], "bargaining_power_of_buyers": po_scores[1],
            "bargaining_power_of_suppliers": po_scores[2], "threat_of_substitutes": po_scores[3],
            "competitive_rivalry": po_scores[4],
            "details": po_det
        }
    })

# ==============================================================================
# SECTOR 16: Metals, Mining & Heavy Materials (20 companies)
# ==============================================================================
sector16_data = [
    (
        "Tata Steel", "Metals, Mining & Heavy Materials",
        "automotive manufacturers, construction developers, and industrial infrastructure builders",
        "need premium high-strength structural steel, corrosion-resistant TMT rebars, and precision automotive cold-rolled steel coils",
        "Tata Tiscon TMT Rebars & Tata Steelium Cold-Rolled Coils", "Integrated Primary Steel Manufacturing & Brand Infrastructure Steel",
        "is India's premier integrated steel producer with 100% captive iron ore self-sufficiency, delivering iconic Tiscon 550D earthquake-resistant TMT rebars",
        [0.82, 0.94, 0.96, 0.94, 0.88, 0.78],
        {"political": "Founded in Jamshedpur in 1907; the bedrock of India's industrial independence and a key partner in the National Steel Policy 2030.", "economic": "Lowest cost of crude steel production in India driven by 100% captive iron ore mines in Jharkhand and Odisha, generating strong operating margins.", "social": "Legendary corporate citizenship: pioneered the 8-hour workday, paid maternity leave, and established the planned modern city of Jamshedpur.", "technological": "State-of-the-art Kalinganagar blast furnaces, continuous thin slab casting, and AI-driven predictive blast furnace thermal modeling.", "legal": "Mines and Minerals (Development and Regulation) Act (MMDR) compliance, forest clearances, and SEBI corporate governance.", "environmental": "Pioneering green steel technologies, CO2 capture pilot plants in Jamshedpur, and transitioning European assets to electric arc furnaces."},
        [0.18, 0.48, 0.28, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; developing a 10-million-ton integrated steel plant with blast furnaces and captive iron ore mines requires tens of thousands of crores.", "bargaining_power_of_buyers": "Moderate; automotive clients require specialized grade certifications, while retail TMT consumers trust the Tata Tiscon brand.", "bargaining_power_of_suppliers": "Low; 100% captive iron ore mines insulate Tata Steel from merchant raw material price spikes.", "threat_of_substitutes": "Low; steel has no structural substitute in heavy skyscrapers, bridges, and vehicle chassis.", "competitive_rivalry": "Moderate; oligopoly competition with JSW Steel and JSPL."}
    ),
    (
        "JSW Steel", "Metals, Mining & Heavy Materials",
        "domestic and international engineering fabricators, automotive giants, and solar project developers",
        "demand high-volume, cost-competitive hot-rolled coils, color-coated galvanized sheets, and specialized electrical steel",
        "JSW Neosteel TMT & JSW Colouron+ Coated Sheets", "High-Efficiency Coastal & Integrated Steel Manufacturing",
        "stands as India's largest steelmaker by domestic capacity (28+ MTPA), operating the world's sixth-largest single-site steel plant in Vijayanagar",
        [0.80, 0.94, 0.96, 0.95, 0.86, 0.76],
        {"political": "Direct beneficiary of National Infrastructure Pipeline (NIP) and national steel production linked incentive (PLI) for specialty steel.", "economic": "Industry benchmark in low capital expenditure cost per ton and hyper-fast project execution, producing superior return on capital employed.", "social": "Major driver of regional prosperity in Bellary, Karnataka and Dolvi, Maharashtra, providing community hospitals and schools.", "technological": "Corex and Blast Furnace hybrid smelting, pairing with JFE Steel Japan to produce specialized Cold Rolled Grain Oriented (CRGO) electrical steel.", "legal": "MMDR mineral auction compliance, environmental stack clearances, and competition commission adherence.", "environmental": "Committed to reducing CO2 emissions intensity by 42% by 2030; recycling 100% of blast furnace slag into green slag cement."},
        [0.20, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; massive scale economies and coastal port logistical berths prevent new entrants from matching JSW's conversion costs.", "bargaining_power_of_buyers": "Moderate; steel prices track international hot-rolled coil benchmarks.", "bargaining_power_of_suppliers": "Moderate; procures iron ore via commercial e-auctions and imports metallurgical coking coal from Australia.", "threat_of_substitutes": "Low for heavy structural applications.", "competitive_rivalry": "Intense rivalry with Tata Steel and JSPL for domestic market share leadership."}
    ),
    (
        "Jindal Steel & Power (JSPL)", "Metals, Mining & Heavy Materials",
        "Indian Railways, high-speed rail corridors, metro systems, and heavy structural engineering developers",
        "require ultra-long, head-hardened 1080-grade railway tracks, heavy structural steel columns, and customized thick steel plates",
        "Head-Hardened 1080 Grade Rails & Heavy Structural Steel Plates", "Specialized Rail Manufacturing & Integrated Steelmaking",
        "pioneered long-rail manufacturing in India, supplying 260-meter long flash-butt welded rails to Indian Railways and the Dedicated Freight Corridor",
        [0.82, 0.92, 0.95, 0.94, 0.86, 0.78],
        {"political": "Sole private sector rail supplier approved by Indian Railways and Research Designs and Standards Organisation (RDSO).", "economic": "Turned net debt-free with superior EBITDA per ton, supported by low-cost direct reduced iron (DRI) sponge iron manufacturing in Angul.", "social": "Drives massive regional employment in Raigarh and Angul, constructing educational institutions and women livelihood centers.", "technological": "India's only coal gasification-based DRI steel plant, producing clean synthesis gas from high-ash domestic coal to smelt steel.", "legal": "RDSO rail quality certifications, commercial coal mine auction compliance, and factory safety laws.", "environmental": "Coal gasification produces clean DRI with low particulate pollution compared to traditional thermal blast furnace methods."},
        [0.18, 0.45, 0.35, 0.20, 0.62],
        {"threat_of_new_entrants": "Low; rolling specialized 260-meter head-hardened rails requires proprietary universal rail mills and RDSO approvals.", "bargaining_power_of_buyers": "Moderate; Indian Railways is the dominant single buyer of rails, but relies on JSPL to break SAIL's former monopoly.", "bargaining_power_of_suppliers": "Low to moderate; captive thermal coal blocks and regional iron ore procurement.", "threat_of_substitutes": "Low; steel rails are non-substitutable for rail transport.", "competitive_rivalry": "Low in specialized heavy rails; moderate in commercial plates and rebars."}
    ),
    (
        "Steel Authority of India (SAIL)", "Metals, Mining & Heavy Materials",
        "public infrastructure projects, Indian defense forces, railways, and national capital goods fabricators",
        "need high-volume structural steel, defense naval armor steel plates, heavy forgings, and standardized infrastructure beams",
        "Bhilai, Bokaro, Rourkela Steel Plates & DMR 249A Defense Steel", "Maharatna Sovereign Integrated Steel Producer",
        "stands as India's apex public steelmaker with 5 integrated steel plants, supplying specialized DMR 249A steel for India's indigenous aircraft carriers",
        [0.86, 0.92, 0.96, 0.90, 0.88, 0.75],
        {"political": "Maharatna PSU under Ministry of Steel; historic pillar of India's heavy industrialization and critical supplier to defense and nuclear projects.", "economic": "100% captive iron ore mines in Jharkhand and Odisha provide secure raw material economics; substantial dividend contributor to the national exchequer.", "social": "Built and manages massive industrial townships (Bhilai, Bokaro, Rourkela, Durgapur) providing subsidized housing, schools, and hospitals to lakhs.", "technological": "Modernized blast furnaces, vacuum degassers, automated ladle refining furnaces, and wide plate rolling mills.", "legal": "Public sector procurement guidelines, statutory MMDR mineral leasing laws, and environmental regulatory compliances.", "environmental": "Major investments into dry fog dust suppression, continuous ambient air monitoring, and blast furnace gas heat recovery."},
        [0.15, 0.40, 0.25, 0.20, 0.65],
        {"threat_of_new_entrants": "Zero; sovereign integrated steel mega-plants with township infrastructure cannot be duplicated.", "bargaining_power_of_buyers": "Moderate; government departments and railways procure under long-term PSU agreements.", "bargaining_power_of_suppliers": "Low; captive iron ore mines eliminate merchant market dependence.", "threat_of_substitutes": "Low for essential structural steel.", "competitive_rivalry": "Moderate; competes with Tata Steel and JSW in open market commercial steel sales."}
    ),
    (
        "Hindalco Industries", "Metals, Mining & Heavy Materials",
        "global automotive giants, beverage can packaging makers, aerospace manufacturers, and electrical utilities",
        "require ultra-lightweight aluminum sheet solutions, beverage can recycling, and high-purity electrical conductor grade aluminum",
        "Novelis Recycled Aluminum Sheets & Maxloader Commercial Aluminum", "Global Aluminum Rolled Products & Copper Refining",
        "is the world's largest aluminum company by revenue and the global leader in aluminum beverage can recycling with Novelis, operating 50+ plants globally",
        [0.80, 0.94, 0.96, 0.96, 0.86, 0.88],
        {"political": "Key industry partner for Make in India lightweight transport, high-speed Vande Bharat aluminum trainsets, and defense metal alloys.", "economic": "Resilient business model: Novelis downstream conversion premiums cushion against volatile London Metal Exchange (LME) aluminum spot prices.", "social": "Drives rural community development and bauxite mining welfare across tribal belts of Odisha, Jharkhand, and Madhya Pradesh.", "technological": "Automated closed-loop aluminum can recycling, continuous automotive sheet heat-treatment lines, and specialized copper cathodes.", "legal": "LME trading compliance, global anti-dumping defense, and environmental mining statutory approvals.", "environmental": "Novelis uses over 61% recycled aluminum scrap, cutting carbon emissions by 95% compared to primary virgin smelting."},
        [0.18, 0.45, 0.35, 0.22, 0.58],
        {"threat_of_new_entrants": "Low; building an integrated bauxite-to-alumina-to-smelter chain with captive power requires billions of dollars in capex.", "bargaining_power_of_buyers": "Moderate; global automotive (Ford, Audi) and can makers (Ball) demand strict tolerances and long-term contracts.", "bargaining_power_of_suppliers": "Low; backward-integrated into captive bauxite mines and captive thermal/renewable power.", "threat_of_substitutes": "Moderate from carbon fiber and high-strength steel in automotive.", "competitive_rivalry": "Low to moderate; global leader in rolled aluminum sheets alongside NALCO and Vedanta domestically."}
    ),
    (
        "Vedanta Limited", "Metals, Mining & Heavy Materials",
        "industrial manufacturers across zinc, aluminum, oil & gas, copper, iron ore, and power sectors",
        "need large-scale, low-cost raw natural resource commodities and base metals to power industrial manufacturing operations",
        "Diversified Natural Resources Portfolio (Zinc, Aluminum, Oil, Copper)", "Diversified Natural Resources & Critical Metals Conglomerate",
        "is India's largest diversified natural resources conglomerate, holding world-leading low-cost positions in zinc, lead, silver, and aluminum smelting",
        [0.82, 0.92, 0.95, 0.92, 0.86, 0.72],
        {"political": "Major contributor to national mineral royalties and oil profit sharing; active participant in commercial mineral auction reforms.", "economic": "Generates immense operating cash flows across diversified metals and energy; high dividend payout yields to institutional shareholders.", "social": "Anil Agarwal Foundation funds the Nand Ghar initiative, modernizing thousands of rural anganwadis for early child nutrition.", "technological": "Sub-surface underground automated mining loaders, wireless blasting telemetry, and modern aluminum potline smelting technology in Jharsuguda.", "legal": "Compliance with MMDR mineral auction laws, Supreme Court environmental rulings, and international human rights audits.", "environmental": "Committed to net-zero carbon operations by 2050; utilizing renewable energy power purchase agreements across smelters."},
        [0.20, 0.48, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; natural resource concessions require statutory government bidding and decades of geological development.", "bargaining_power_of_buyers": "Moderate; base metals trade at LME spot pricing with standardized delivery specifications.", "bargaining_power_of_suppliers": "Low; operates captive mines and processing mills.", "threat_of_substitutes": "Low; essential base metals have no direct functional substitutes.", "competitive_rivalry": "Moderate; competes with Hindalco in aluminum, and ONGC in oil & gas."}
    ),
    (
        "National Aluminium Company (NALCO)", "Metals, Mining & Heavy Materials",
        "international alumina smelters, domestic aluminum fabricators, and electrical cable manufacturers",
        "require ultra-low-cost, high-purity chemical grade metallurgical alumina and primary aluminum ingots and wire rods",
        "Metallurgical Alumina & High-Purity Aluminum Wire Rods", "Navratna Bauxite Mining & Low-Cost Alumina Refining",
        "is globally recognized as the lowest-cost producer of metallurgical alumina, leveraging the world's richest bauxite reserves at Panchpatmali, Odisha",
        [0.84, 0.92, 0.96, 0.90, 0.88, 0.82],
        {"political": "Navratna public sector enterprise under Ministry of Mines; key foreign exchange earner exporting surplus alumina globally.", "economic": "Extraordinary profit margins on alumina exports driven by near-zero bauxite transport costs via an automated overland conveyor belt.", "social": "Extensive community welfare in Koraput and Angul, funding tribal education, healthcare, and infrastructure development.", "technological": "14.6 km long single-flight curved overland conveyor belt transporting bauxite from hilltop mines down to the Damanjodi refinery.", "legal": "MMDR statutory mining lease renewals, environmental forest clearances, and public sector governance.", "environmental": "High-density red mud dry stacking to eliminate wet tailing dam hazards and extensive afforestation of mined bauxite plateaus."},
        [0.15, 0.40, 0.25, 0.20, 0.52],
        {"threat_of_new_entrants": "Zero; access to high-grade Panchpatmali bauxite reserves is a sovereign statutory allocation.", "bargaining_power_of_buyers": "Moderate; alumina sold through transparent international spot and term tenders at LME-linked pricing.", "bargaining_power_of_suppliers": "Low; captive bauxite mines provide 100% internal raw material security.", "threat_of_substitutes": "Low; alumina is the mandatory chemical intermediate to produce aluminum metal.", "competitive_rivalry": "Low globally due to unmatched cost quartile position."}
    ),
    (
        "Hindustan Zinc", "Metals, Mining & Heavy Materials",
        "steel galvanizing mills, automotive battery manufacturers, solar panel mounting fabricators, and silver buyers",
        "need ultra-pure zinc for steel corrosion prevention, refined lead for batteries, and high-purity refined silver bullion",
        "HZL Special High Grade Zinc & 99.99% Pure Refined Silver Bullion", "Integrated Zinc, Lead & Silver Mining and Smelting",
        "stands as the world's second-largest integrated zinc producer and the 5th-largest silver producer, operating the legendary Rampura Agucha underground mine",
        [0.82, 0.94, 0.96, 0.95, 0.88, 0.82],
        {"political": "Strategic enterprise where Government of India retains a valuable 29.5% stake; key contributor to national mineral wealth.", "economic": "Phenomenal profitability with EBITDA margins consistently >50%; lowest-cost zinc producer in the first global cost decile.", "social": "Runs extensive grassroots skill training, zinc football academies, and rural health clinics across Rajasthan.", "technological": "World-class digital underground mines with automated tele-remote drilling, battery-electric mining vehicles, and shaft hoisting systems.", "legal": "MMDR mineral concession compliance, London Bullion Market Association (LBMA) silver certification, and safety audits.", "environmental": "Water-positive company (certified 2.4x water positive), generating captive solar power and converting zinc tailings into paste fill."},
        [0.12, 0.40, 0.25, 0.18, 0.48],
        {"threat_of_new_entrants": "Zero; Rampura Agucha and Sindesar Khurd contain the world's richest zinc-lead geological ore bodies.", "bargaining_power_of_buyers": "Low to moderate; steelmakers must galvanize steel with zinc to prevent rust, with zero substitutes available.", "bargaining_power_of_suppliers": "Low; captive high-grade mines provide 100% ore security.", "threat_of_substitutes": "Low; hot-dip galvanization is the undisputed gold standard for steel rust prevention.", "competitive_rivalry": "Negligible domestically; holds over 75% market share in Indian primary zinc."}
    ),
    (
        "Coal India Limited", "Metals, Mining & Heavy Materials",
        "thermal power generation plants, steel producers, cement kilns, and fertilizer factories",
        "require massive, affordable coal fuel supplies to generate 75% of India's baseline electricity without crippling national energy costs",
        "Non-Coking & Coking Coal Mining & Fuel Supply Agreements", "Maharatna Sovereign Coal Mining Monolith",
        "is the world's largest coal producer, mining over 770 million tons annually across 300+ mines to fuel India's electric power stations",
        [0.88, 0.95, 0.98, 0.90, 0.88, 0.70],
        {"political": "Maharatna sovereign energy giant under Ministry of Coal; the ultimate guarantor of national grid electricity affordability.", "economic": "Generates tens of thousands of crores in operating profits and massive dividend yields; operates with zero net debt.", "social": "The single largest industrial employer in eastern India (230,000+ employees), managing hundreds of hospitals, schools, and townships.", "technological": "High-capacity draglines, continuous miners, automated computerized railway rapid loading systems (RLS), and satellite mine surveillance.", "legal": "Coal Mines (Special Provisions) Act, statutory environmental clearances, and DGMS mining safety regulations.", "environmental": "Massive tree plantation drives on overburden dumps, eco-restoration of closed mines, and commercial solar energy diversification."},
        [0.08, 0.30, 0.25, 0.15, 0.35],
        {"threat_of_new_entrants": "Practically zero; commercial coal mine bidding exists, but nobody can match Coal India's 770-million-ton mining footprint.", "bargaining_power_of_buyers": "Low; thermal power plants are physically linked to Coal India mines via long-term fuel supply agreements (FSAs).", "bargaining_power_of_suppliers": "Low; heavy earthmoving machinery procured under standardized sovereign tenders.", "threat_of_substitutes": "Low in the medium term; renewable energy requires coal power backing to maintain grid baseload stability.", "competitive_rivalry": "Low; natural sovereign monopoly supplying over 80% of domestic coal."}
    ),
    (
        "NMDC Limited", "Metals, Mining & Heavy Materials",
        "integrated steel plants, sponge iron kilns, and iron ore pellet manufacturers across India",
        "need high-grade, high-iron-content (64-65% Fe) iron ore lump and fines to maximize blast furnace productivity and minimize slag",
        "Bailadila High-Grade Iron Ore Lump & Fines", "Navratna Iron Ore Mining & Natural Resources",
        "is India's single largest iron ore producer (producing 45+ MTPA), operating the world-class Bailadila deposit with 65%+ iron purity",
        [0.85, 0.94, 0.96, 0.90, 0.88, 0.78],
        {"political": "Navratna PSU under Ministry of Steel; strategic supplier guaranteeing raw iron ore supply to domestic steel mills.", "economic": "Highest profit margins in Indian mining (>50% EBITDA margins) driven by exceptional ore grades and mechanized hill-top open-pit mining.", "social": "Extensive tribal welfare in Dantewada and Bastar, Chhattisgarh, providing free polytechnics, hospitals, and rural roads.", "technological": "Automated downhill conveyor systems transporting iron ore from hilltop mines down to railway sidings, and high-intensity magnetic separation.", "legal": "Statutory MMDR mining lease extensions, environmental clearances, and District Mineral Foundation (DMF) royalty compliance.", "environmental": "Implements zero-effluent discharge slimes dam water recycling and deep-rooted slope bio-engineering to prevent soil erosion."},
        [0.12, 0.40, 0.25, 0.18, 0.45],
        {"threat_of_new_entrants": "Zero; Bailadila and Donimalai iron ore deposits are sovereign statutory assets that cannot be duplicated.", "bargaining_power_of_buyers": "Moderate; steelmakers negotiate on domestic vs. import parity prices, but prefer NMDC's high Fe grade to cut coke consumption.", "bargaining_power_of_suppliers": "Low; standardized mining machinery.", "threat_of_substitutes": "Low; iron ore is the irreplaceable base raw material for primary steelmaking.", "competitive_rivalry": "Low to moderate; largest merchant miner with private captive miners as peers."}
    ),
    (
        "MOIL Limited", "Metals, Mining & Heavy Materials",
        "domestic steel alloy manufacturers and manganese chemical producers",
        "need high-grade manganese ore for ferromanganese and silicomanganese smelting, essential for removing sulfur and deoxidizing steel",
        "High-Grade Manganese Ore & Electrolytic Manganese Dioxide", "Miniratna Manganese Ore Mining Monolith",
        "is India's largest manganese ore producer with ~50% national market share, operating deep underground and opencast mines in Maharashtra and MP",
        [0.82, 0.88, 0.94, 0.88, 0.86, 0.75],
        {"political": "Miniratna PSU under Ministry of Steel; key player in securing domestic critical mineral independence for steel alloy production.", "economic": "Debt-free balance sheet with robust cash reserves and generous dividend payouts; high pricing power in high-grade ore categories.", "social": "Provides long-term housing, medical care, and schools for mining communities in Nagpur and Balaghat districts.", "technological": "Deep vertical underground mine shafts (up to 400m), mechanized sublevel stopping, and modern ferro-alloy beneficiation plants.", "legal": "MMDR mineral statutory leases, DGMS underground safety audits, and environmental pollution clearances.", "environmental": "Scientific reclamation of exhausted mine quarries and solar power installation meeting substantial captive energy needs."},
        [0.15, 0.45, 0.28, 0.20, 0.50],
        {"threat_of_new_entrants": "Low; underground manganese mining requires deep specialized geological engineering and long-term mineral concessions.", "bargaining_power_of_buyers": "Moderate; alloy makers purchase via MOIL's quarterly price notifications, with imported South African ore acting as a price cap.", "bargaining_power_of_suppliers": "Low; standard mining equipment and explosives.", "threat_of_substitutes": "Low; manganese is chemically mandatory in steelmaking—every ton of steel requires ~10 kg of manganese.", "competitive_rivalry": "Low; undisputed domestic market leader."}
    ),
    (
        "Gujarat Mineral Development Corporation (GMDC)", "Metals, Mining & Heavy Materials",
        "textile processing mills, chemical factories, brick kilns, and alumina plants across Gujarat",
        "need affordable merchant lignite fuel and bauxite minerals to replace expensive imported coal and natural gas",
        "Merchant Lignite Mining & Plant-Grade Bauxite", "State Merchant Mining & Mineral Exploration Enterprise",
        "is India's premier merchant lignite miner, supplying over 8 million tons of affordable solid fuel to thousands of MSME factories across Gujarat",
        [0.82, 0.90, 0.94, 0.88, 0.86, 0.72],
        {"political": "Government of Gujarat undertaking; critical economic catalyst supporting Gujarat's massive textile, ceramic, and chemical MSME sectors.", "economic": "High operating profitability driven by transparent e-auction pricing for merchant lignite, benefiting from high imported Indonesian coal tariffs.", "social": "Creates rural livelihoods in Kutch, Bhavnagar, and Surat districts, providing water conservation and rural education.", "technological": "Mechanized surface miners reducing blasting vibration, real-time GPS fleet dispatch, and automated weighbridge billing.", "legal": "State mining lease allocations, statutory DMF contributions, and compliance with MoEFCC guidelines.", "environmental": "Extensive land backfilling, topsoil preservation, and plantation of indigenous acacia and neem forests on reclaimed lignite pits."},
        [0.15, 0.48, 0.28, 0.22, 0.50],
        {"threat_of_new_entrants": "Zero in merchant lignite in Gujarat; GMDC holds statutory regional mining rights.", "bargaining_power_of_buyers": "Moderate; industrial factories purchase through transparent digital e-auctions, preferring GMDC over expensive imported fuel.", "bargaining_power_of_suppliers": "Low; heavy earthmoving machinery and contract mining operators.", "threat_of_substitutes": "Moderate from imported thermal coal and natural gas.", "competitive_rivalry": "Low; regional merchant fuel monopoly."}
    ),
    (
        "APL Apollo Tubes", "Metals, Mining & Heavy Materials",
        "architects, commercial infrastructure builders, airport developers, and residential fabricators",
        "need structural steel hollow sections and pre-galvanized tubes that replace heavy, expensive RCC and conventional structural steel beams",
        "Apollo Structural Hollow Sections & Pre-Galvanized Square Tubes", "Structural Steel Tubes & Building Material Innovations",
        "is India's largest structural steel tube manufacturer with 55% market share, revolutionizing modern architecture with patented direct-forming technology",
        [0.72, 0.92, 0.96, 0.94, 0.84, 0.78],
        {"political": "Aligned with National Steel Policy goal of increasing per capita steel consumption via modern pre-engineered structural steel.", "economic": "Rapid growth and industry-leading return on capital (ROCE >30%) driven by continuous SKU innovation and 3-tier distributor penetration.", "social": "Enabled ultra-fast construction of emergency hospitals, airports, and railway station redevelopments without messy concrete curing.", "technological": "Patented Direct Forming Technology (DFT) creating custom-sized square and rectangular hollow sections with zero tooling change downtime.", "legal": "BIS quality certifications (IS 4923) and patent protection on innovative tubular profiles.", "environmental": "Steel tubes are 100% recyclable, cut building steel weight by 20%, and eliminate wood formwork and water usage in construction."},
        [0.22, 0.50, 0.38, 0.25, 0.65],
        {"threat_of_new_entrants": "Low to moderate; replicating APL Apollo's 3.6 MTPA manufacturing capacity across 11 plants and 800+ distributors is formidable.", "bargaining_power_of_buyers": "Moderate; builders and fabricators demand Apollo tubes for dimensional precision and quick site welding.", "bargaining_power_of_suppliers": "Moderate; hot-rolled steel coils procured in massive volume from JSW Steel and Tata Steel.", "threat_of_substitutes": "Moderate from traditional RCC concrete pillars and conventional welded I-beams.", "competitive_rivalry": "Moderate; undisputed category creator and leader ahead of Surya Roshni and Hi-Tech Pipes."}
    ),
    (
        "Welspun Corp", "Metals, Mining & Heavy Materials",
        "cross-country oil and gas pipeline operators, water infrastructure boards, and offshore energy majors globally",
        "require large-diameter submerged arc welded line pipes engineered to withstand high internal pressures, corrosive sour gas, and deep ocean depths",
        "Submerged Arc Welded (LSAW/HSAW) Large-Diameter Line Pipes", "High-Specification Large-Diameter Welded Steel Pipes",
        "stands as a global top-3 large-diameter line pipe manufacturer, having supplied critical pipelines across 50+ countries including the world's deepest offshore line",
        [0.78, 0.90, 0.95, 0.94, 0.85, 0.75],
        {"political": "Major beneficiary of national water infrastructure missions (Jal Jeevan Mission) and trans-continental gas grid expansions.", "economic": "Multi-billion-dollar global order book with operations in India, USA, and Saudi Arabia; expanding into ductile iron pipes and stainless tubes.", "social": "Brings clean drinking water to millions of drought-prone villages in Gujarat and Rajasthan via mega-diameter water transmission pipes.", "technological": "Advanced JCOE pipe forming, automated inside/outside submerged arc welding, multi-layer internal/external epoxy coating, and ultrasonic testing.", "legal": "American Petroleum Institute (API 5L) certified, BIS standards, and international maritime welding approvals.", "environmental": "High-integrity anti-corrosion polyethene coating prevents pipeline ruptures and hazardous chemical spills into fragile ecosystems."},
        [0.22, 0.48, 0.42, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; large-diameter line pipe manufacturing requires specialized high-tonnage hydraulic presses and stringent oil major approvals.", "bargaining_power_of_buyers": "Moderate; oil & gas majors (Aramco, ExxonMobil, GAIL) run strict global competitive bids.", "bargaining_power_of_suppliers": "Moderate; heavy steel plate suppliers (JSW Steel, POSCO).", "threat_of_substitutes": "Low; large-diameter steel pipes are indispensable for high-pressure oil, gas, and bulk municipal water transport.", "competitive_rivalry": "Moderate globally with Jindal SAW and Europipe."}
    ),
    (
        "Ratnamani Metals & Tubes", "Metals, Mining & Heavy Materials",
        "nuclear power reactors, defense aerospace, oil refineries, and fertilizer plants",
        "demand ultra-reliable, corrosion-resistant stainless steel seamless tubes and titanium/nickel alloy pipes engineered for extreme temperatures and pressures",
        "Stainless Steel Seamless Pipes & Titanium Superalloy Tubes", "Specialized Critical Stainless Steel & Exotic Alloy Piping",
        "dominates India's specialized stainless steel and nickel alloy pipe industry, trusted as the sole supplier for India's nuclear power reactors and defense space missions",
        [0.78, 0.90, 0.95, 0.95, 0.86, 0.75],
        {"political": "Critical indigenous supplier for Nuclear Power Corporation of India (NPCIL), ISRO rocket engines, and Indian Navy warships under Make in India.", "economic": "Consistent, high-margin niche engineering business with zero net debt and pristine working capital management.", "social": "Secures critical national infrastructure, preventing lethal radioactive leaks in nuclear power stations and toxic refinery blowouts.", "technological": "High-tonnage cold pilgering mills, bright annealing furnaces, eddy-current non-destructive testing, and specialized titanium extrusion.", "legal": "Stringent global nuclear and aerospace certifications (ASME Section III, PED, ISO 9001), and defense clearances.", "environmental": "Closed-loop acid pickling plants with zero toxic effluent discharge and 100% recycling of specialized alloy scrap."},
        [0.20, 0.45, 0.42, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; qualifying for nuclear reactor steam generators and space flight takes over a decade of continuous destructive testing.", "bargaining_power_of_buyers": "Moderate; high-end industrial buyers evaluate technical metallurgical zero-defect track records above price.", "bargaining_power_of_suppliers": "Moderate; specialized stainless steel and superalloy round billet suppliers (Outokumpu, Jindal Stainless).", "threat_of_substitutes": "Low; critical nuclear and cryogenic applications have zero material alternatives.", "competitive_rivalry": "Low to moderate; undisputed domestic leader in specialized stainless steel piping."}
    ),
    (
        "Jindal Stainless", "Metals, Mining & Heavy Materials",
        "railway coach builders, automotive exhaust fabricators, architecture infrastructure, and cookware industries",
        "need corrosion-resistant, high-strength stainless steel sheets and coils in 200, 300, and 400 series alloys to replace rust-prone carbon steel",
        "JSL Series Stainless Steel Sheets & Rail Coach Stainless Panels", "Integrated Stainless Steel Smelting & Coiling Monolith",
        "is India's largest stainless steel producer (3 MTPA capacity) and ranks among the top 5 globally, supplying stainless steel for Indian Railways Vande Bharat trains",
        [0.80, 0.92, 0.96, 0.94, 0.86, 0.80],
        {"political": "Advocates for domestic manufacturing protections against subsidized Chinese and Indonesian stainless steel dumping.", "economic": "Consolidated Jindal Stainless into a unified mega-entity, achieving massive scale economies in Jajpur, Odisha and Hisar, Haryana.", "social": "Transformed Indian passenger rail safety: stainless steel coaches do not crush or telescope upon collision, saving thousands of passenger lives.", "technological": "Argon Oxygen Decarburization (AOD) converter refining, automated steckel mill rolling, and skin-pass temper mills.", "legal": "BIS mandatory quality certifications, international ASTM/EN standards, and anti-dumping trade petitions.", "environmental": "Committed to achieving Net Zero emissions by 2050; building green hydrogen generation at Jajpur to power stainless annealing furnaces."},
        [0.18, 0.48, 0.38, 0.22, 0.60],
        {"threat_of_new_entrants": "Low; integrated stainless steel refining requires AOD converters, ferrochrome facilities, and deep working capital.", "bargaining_power_of_buyers": "Moderate; railway tenders negotiate on volume, while industrial buyers require reliable surface finish.", "bargaining_power_of_suppliers": "Moderate; nickel, ferrochrome, and stainless steel scrap prices fluctuate with global commodity cycles.", "threat_of_substitutes": "Moderate from carbon steel in low-cost applications, but stainless is preferred for lifecycle rust resistance.", "competitive_rivalry": "Low to moderate domestically; dominates the organized Indian stainless steel landscape."}
    ),
    (
        "Shyam Metalics and Energy", "Metals, Mining & Heavy Materials",
        "construction developers, secondary steel mills, and aluminum packaging fabricators",
        "need reliable, cost-effective intermediate steel products (pellets, sponge iron, billets) and finished structural TMT bars and aluminum foil",
        "SEL Tiger TMT Rebars, Ferro Alloys & Aluminum Foil", "Integrated Intermediate & Finished Metal Products",
        "operates ultra-efficient integrated metal plants in West Bengal and Odisha with captive power, leading in sponge iron and expanding into specialized aluminum foil",
        [0.76, 0.90, 0.94, 0.90, 0.84, 0.74],
        {"political": "Supports eastern regional industrialization and circular metal manufacturing under Make in India.", "economic": "Ultra-low cost structure powered by 100% captive power plants running on waste heat recovery; robust net cash balance sheet.", "social": "Provides tens of thousands of industrial manufacturing jobs in Sambalpur, Odisha and Jamuria, West Bengal.", "technological": "Rotary kiln sponge iron reduction, waste-heat-recovery boilers, and modern automated continuous casting billet mills.", "legal": "Factory safety regulations, environmental air emission compliances, and corporate listing governance.", "environmental": "Generates hundreds of megawatts of clean electricity solely by capturing hot exhaust gases from sponge iron kilns."},
        [0.25, 0.52, 0.38, 0.25, 0.68],
        {"threat_of_new_entrants": "Moderate; secondary steel has lower entry hurdles, but Shyam's integrated waste-heat-power scale is difficult to match.", "bargaining_power_of_buyers": "Moderate to high; intermediate billets and pellets trade transparently on commodity spot markets.", "bargaining_power_of_suppliers": "Moderate; iron ore fines procured from Odisha merchant mines and coal from Coal India e-auctions.", "threat_of_substitutes": "Low for primary and secondary construction steel.", "competitive_rivalry": "High with regional secondary steel producers in Eastern India."}
    ),
    (
        "Mishra Dhatu Nigam (MIDHANI)", "Metals, Mining & Heavy Materials",
        "strategic sovereign sectors: Indian Space Research Organisation (ISRO), DRDO, Indian Navy, and aeronautical programs",
        "require sovereign, ultra-high-strength superalloys, titanium alloys, maraging steel, and ballistic armor resistant to extreme temperatures and missile impacts",
        "Maraging Steel, Titanium Superalloys & Ballistic Armor Plates", "Specialized Strategic Superalloys & Defense Metallurgical Materials",
        "stands as India's premier strategic metals enterprise, manufacturing the specialized rocket motor casing maraging steel for ISRO's Chandrayaan and Gaganyaan",
        [0.88, 0.88, 0.92, 0.98, 0.90, 0.75],
        {"political": "Miniratna Schedule-A PSU under Ministry of Defence; critical sovereign pillar preventing foreign missile technology embargoes.", "economic": "Protected, high-margin sovereign order book; sole domestic certified producer of critical space-grade and defense-grade specialized alloys.", "social": "Secures national defense readiness and enables India's lunar and human spaceflight missions with sovereign metallurgical pride.", "technological": "Vacuum Induction Melting (VIM), Vacuum Arc Remelting (VAR), and Electro Slag Remelting (ESR) creating defect-free atomic crystal superalloys.", "legal": "Highest-tier defense secrecy certifications, DGQA military quality approvals, and international spaceflight metallurgy compliance.", "environmental": "High-efficiency electric induction melting with complete zero toxic air emission scrubbing."},
        [0.10, 0.35, 0.30, 0.15, 0.40],
        {"threat_of_new_entrants": "Zero; space and missile-grade superalloy metallurgical approvals require sovereign security clearances that private entrants cannot obtain.", "bargaining_power_of_buyers": "Low; ISRO and DRDO rely exclusively on MIDHANI for rocket casings and nuclear submarine components.", "bargaining_power_of_suppliers": "Moderate; specialized elemental inputs (nickel, cobalt, molybdenum, titanium sponge).", "threat_of_substitutes": "Zero; space propulsion requires exact metallurgical thermodynamic resilience.", "competitive_rivalry": "Zero; undisputed sovereign monopoly in strategic superalloys."}
    ),
    (
        "KIOCL Limited", "Metals, Mining & Heavy Materials",
        "international blast furnace steelmakers and domestic pellet consumers",
        "need high-quality, uniform iron ore pellets with high mechanical cold crushing strength for efficient blast furnace and DRI operations",
        "Blast Furnace & Direct Reduction Grade Iron Ore Pellets", "Export-Oriented Iron Ore Pelletization Infrastructure",
        "operates a 3.5 MTPA coastal pellet plant in Mangaluru port, exporting world-class iron ore pellets globally with dedicated deep-draft jetty berths",
        [0.80, 0.88, 0.92, 0.88, 0.86, 0.75],
        {"political": "Mini-Ratna Schedule-A public enterprise under Ministry of Steel; key export vehicle for value-added processed iron ore.", "economic": "Coastal port location provides unbeatable sea freight economics for exporting pellets to China, Japan, and Middle Eastern DRI plants.", "social": "Drives maritime trade and economic activity around New Mangalore Port, supporting regional port logistics employment.", "technological": "High-efficiency traveling grate pelletizing furnace, automated bentonite mixing, and disc pelletizers producing uniform 9-16mm spheres.", "legal": "Environmental coastal zone compliances, export trade regulations, and public sector governance.", "environmental": "Dust extraction systems, closed conveyor galleries, and water mist spraying across iron ore concentrate stockyards."},
        [0.22, 0.52, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; building port-based pelletization plants with dedicated marine loading arms requires significant capital.", "bargaining_power_of_buyers": "Moderate; international buyers negotiate pellet premiums over Platts iron ore index.", "bargaining_power_of_suppliers": "Moderate; iron ore fines procured from NMDC and merchant miners.", "threat_of_substitutes": "Moderate from iron ore lump and sinter feed.", "competitive_rivalry": "Moderate with domestic pellet producers (Jindal SAW, ArcelorMittal Nippon Steel)."}
    ),
    (
        "Godawari Power & Ispat", "Metals, Mining & Heavy Materials",
        "secondary steel rolling mills, forging units, and export pellet traders",
        "demand high-grade iron ore pellets, high-tensile wire rods, and ferro alloys produced with captive raw material security",
        "High-Grade Iron Ore Pellets & High-Tensile Steel Wire Rods", "Integrated Pelletization, Sponge Iron & Wire Rod Manufacturing",
        "operates an end-to-end integrated steel business in Raipur with captive high-grade iron ore mines, turning 100% net debt-free with stellar return on equity",
        [0.76, 0.90, 0.94, 0.90, 0.84, 0.74],
        {"political": "Supports Chhattisgarh state industrial development; holds long-term statutory captive iron ore mining concessions (Ari Dongri).", "economic": "Captive iron ore mine provides extreme cost cushions, enabling industry-leading profit margins on pellet sales and wire rods.", "social": "Major local employer in Raipur and Bastar, funding rural drinking water schemes and community schools.", "technological": "Direct-reduced iron rotary kilns, waste-heat power generation, and automated high-speed wire rod rolling mills.", "legal": "MMDR captive mining compliance, environmental pollution control board approvals, and listing governance.", "environmental": "70 MW captive solar power installations and 100% recycling of waste heat gases to generate clean industrial electricity."},
        [0.24, 0.50, 0.32, 0.25, 0.65],
        {"threat_of_new_entrants": "Low; captive high-grade iron ore mines create an insurmountable raw material cost barrier for new secondary mills.", "bargaining_power_of_buyers": "Moderate; pellet prices track global indices, while wire rods serve diverse regional engineering clients.", "bargaining_power_of_suppliers": "Low; captive iron ore self-sufficiency.", "threat_of_substitutes": "Low for essential structural wires and pellets.", "competitive_rivalry": "Moderate; competes with Sarda Energy and Shyam Metalics in central India."}
    )
]

for item in sector16_data:
    add_c(*item)

print(f"Sector 16 added: {len(sector16_data)} companies. Total: {len(part3_b)}")

# ==============================================================================
# SECTOR 17: Infrastructure, EPC & Capital Goods (22 companies)
# ==============================================================================
sector17_data = [
    (
        "Larsen & Toubro (L&T)", "Infrastructure, EPC & Capital Goods",
        "national governments, global energy conglomerates, city metro authorities, and defense forces across 30+ countries",
        "require turnkey, ultra-complex mega-engineering, procurement, and construction (EPC) for nuclear plants, bullet trains, and deep offshore energy",
        "Mega-EPC Infrastructure, Bullet Train Viaducts & Defense Warships", "India's Apex Engineering, Construction & Capital Goods Conglomerate",
        "stands as India's premier engineering titan with an order book exceeding Rs 4,75,000 Cr, building the Mumbai-Ahmedabad bullet train and coastal sea bridges",
        [0.85, 0.96, 0.98, 0.98, 0.88, 0.85],
        {"political": "National nation-builder; the default engineering partner for every historic Indian megaproject (Statue of Unity, Ram Mandir, Atal Setu).", "economic": "Massive consolidated revenue (>Rs 2,20,000 Cr); unmatched balance sheet bonding capacity required to bid on multi-billion dollar sovereign tenders.", "social": "Trains hundreds of thousands of skilled construction tradesmen through L&T Construction Skills Training Institutes across India.", "technological": "Heavy civil 3D automated launching gantries for bullet train viaducts, nuclear reactor pressure vessels, and robotic modular manufacturing.", "legal": "Strict adherence to FIDIC international contracts, defense procurement procedures (DPP), and public listing governance.", "environmental": "Pioneered green hydrogen electrolyzer manufacturing with McPhy; constructs IGBC-certified green infrastructure and metro rail networks."},
        [0.12, 0.45, 0.35, 0.18, 0.55],
        {"threat_of_new_entrants": "Practically impossible; executing multi-billion-dollar complex infrastructure requires decades of engineering credentials and bank bonding.", "bargaining_power_of_buyers": "Moderate; sovereign clients negotiate milestone payments, but L&T is often the only qualified domestic bidder for mega projects.", "bargaining_power_of_suppliers": "Low; massive bulk buyer of cement, steel, and heavy machinery, commanding steep OEM discounts.", "threat_of_substitutes": "Low; complex civil engineering and nuclear construction have no substitute.", "competitive_rivalry": "Low to moderate; operates in a league of its own ahead of all domestic infrastructure contractors."}
    ),
    (
        "Adani Ports and Special Economic Zone (APSEZ)", "Infrastructure, EPC & Capital Goods",
        "international shipping lines, global trade shippers, and domestic container cargo logistics",
        "need deep-draft maritime ports, fast vessel turnaround times, integrated multi-modal rail logistics, and special economic zone infrastructure",
        "Mundra Port Mega-Terminal & National Port Network", "India's Largest Commercial Port Developer & Integrated Logistics Operator",
        "handles ~27% of India's total maritime cargo across 15 strategically located coastal ports, operating Mundra—India's largest commercial port",
        [0.85, 0.96, 0.98, 0.95, 0.88, 0.80],
        {"political": "Key policy stakeholder in Sagarmala coastal shipping initiative; strategic owner of major deep-water ports across India's coastline and overseas (Haifa, Israel).", "economic": "Industry-leading EBITDA margins (>70%) on port operations; high cash generation funded by long-term vessel handling and container tariffs.", "social": "Drives economic development of Kutch and coastal regions, generating hundreds of thousands of direct and indirect maritime jobs.", "technological": "Automated ship-to-shore gantry cranes, AI-driven container yard management, and pan-India double-stack container train operations.", "legal": "Major Port Authorities Act, concession agreements with maritime boards, and coastal regulation zone (CRZ) clearances.", "environmental": "Targeting carbon neutrality by 2025; massive coastal mangrove conservation (over 30,000 hectares preserved) and electrified port equipment."},
        [0.12, 0.42, 0.28, 0.18, 0.50],
        {"threat_of_new_entrants": "Practically impossible; developing deep-draft coastal ports requires coastal land, marine breakwaters, and decades-long concessions.", "bargaining_power_of_buyers": "Moderate; global container shipping liners (MSC, Maersk) evaluate turnaround speed, where APSEZ provides the fastest vessel clearance in India.", "bargaining_power_of_suppliers": "Low; standardized marine equipment (ZPMC cranes) and civil dredging contractors.", "threat_of_substitutes": "Low; maritime shipping carries 95% of India's trade by volume.", "competitive_rivalry": "Low to moderate; dominates private commercial port operations ahead of state-run Major Port Trusts."}
    ),
    (
        "GMR Airports Infrastructure", "Infrastructure, EPC & Capital Goods",
        "commercial airlines, 100+ million air passengers annually, and airport concession retail/cargo businesses",
        "demand world-class airport terminal operations, fast baggage transit, rapid flight turnarounds, and luxurious passenger retail experiences",
        "Delhi IGI Airport Terminal 3/4 & Rajiv Gandhi Hyderabad Airport", "Mega-Airport Concessionaire & Aviation Infrastructure Operator",
        "operates Delhi IGI Airport—India's busiest hub handling 72+ million passengers annually—ranked among the world's best mega-airports by Skytrax",
        [0.85, 0.94, 0.98, 0.94, 0.88, 0.82],
        {"political": "Strategic partner for Ministry of Civil Aviation; flagship operator under long-term public-private partnership (PPP) concession agreements.", "economic": "Dual revenue model: regulated aeronautical tariffs (UDF/landing fees) plus booming, high-margin non-aero revenue (duty-free shopping, luxury retail, aero-city real estate).", "social": "Delhi and Hyderabad airports serve as India's premier international gateways to the world, transforming regional tourism and commercial connectivity.", "technological": "DigiYatra biometric facial recognition boarding, dual elevated aircraft taxiways (Eastern Cross Taxiway), and automated baggage handling systems.", "legal": "Airports Economic Regulatory Authority of India (AERA) tariff determinations, DGCA aviation safety, and long-term AAI concession agreements.", "environmental": "Delhi IGI Airport achieved Level 4+ carbon accreditation, operating on 100% green renewable power and deploying electric airside transit vehicles."},
        [0.10, 0.40, 0.35, 0.15, 0.45],
        {"threat_of_new_entrants": "Zero; airport concessions grant exclusive 30-to-60 year geographical catchment monopolies.", "bargaining_power_of_buyers": "Low; commercial airlines must fly into Delhi and Hyderabad to maintain national and international route networks.", "bargaining_power_of_suppliers": "Moderate; specialized air traffic management and terminal construction contractors.", "threat_of_substitutes": "Low for long-distance domestic and international travel; high-speed rail will take decades to compete on trunk routes.", "competitive_rivalry": "Zero within regional catchments; competes only during open bidding for new greenfield airport concessions (Adani Airports)."}
    ),
    (
        "IRB Infrastructure Developers", "Infrastructure, EPC & Capital Goods",
        "National Highways Authority of India (NHAI), commercial truckers, and interstate road commuters",
        "need world-class, multi-lane national highways and expressways engineered for high-speed travel with automated FASTag electronic toll collection",
        "Mumbai-Pune Expressway & National Golden Quadrilateral Tollways", "Build-Operate-Transfer (BOT) Highway Infrastructure & Tollways",
        "is India's largest highway toll road developer and pioneer of BOT road assets, managing over 15,000 lane km of highways including the iconic Mumbai-Pune Expressway",
        [0.84, 0.94, 0.96, 0.92, 0.88, 0.75],
        {"political": "Key implementation partner for NHAI's Bharatmala Pariyojana; pioneered road infrastructure investment trusts (InvITs) in India.", "economic": "Long-term 20-30 year toll concession rights; toll collections rise automatically with inflation-indexed wholesale price index (WPI) toll adjustments.", "social": "Slashes intercity driving times and logistics freight transit hours across crucial economic corridors (Mumbai-Pune, Golden Quadrilateral).", "technological": "100% automated FASTag RFID electronic toll collection, intelligent traffic management systems (ITMS), and automated highway patrol telemetry.", "legal": "NHAI concession agreements, National Highways Fee Rules, and statutory Ministry of Road Transport & Highways (MoRTH) safety compliances.", "environmental": "Extensive avenue tree plantation along highway medians and recycling reclaimed asphalt pavement (RAP) in road resurfacing."},
        [0.12, 0.42, 0.30, 0.18, 0.50],
        {"threat_of_new_entrants": "Low; bidding on multi-thousand-crore Toll-Operate-Transfer (TOT) and BOT highway concessions requires massive balance sheet equity and past toll track records.", "bargaining_power_of_buyers": "Low; highway motorists have no viable bypass alternatives to reach destination cities quickly.", "bargaining_power_of_suppliers": "Low to moderate; road construction machinery and bulk asphalt/cement procurement.", "threat_of_substitutes": "Low; road freight carries over 65% of India's domestic freight cargo.", "competitive_rivalry": "Moderate during NHAI concession auctions with Ashoka Buildcon and IRB's own InvITs."}
    ),
    (
        "NCC Limited", "Infrastructure, EPC & Capital Goods",
        "state infrastructure agencies, central government ministries, and urban water boards",
        "require turnkey civil construction for high-speed expressways, underground metro lines, rural piped drinking water, and defense buildings",
        "Water & Environment EPC, Urban Metro Projects & Highway Construction", "Diversified Multi-Sector Civil Infrastructure Construction",
        "is one of India's most diversified infrastructure construction powerhouses, with an order book exceeding Rs 55,000 Cr across water, buildings, and transportation",
        [0.80, 0.90, 0.95, 0.90, 0.85, 0.72],
        {"political": "Major executor for national flagship schemes: Jal Jeevan Mission, Bharatmala, and Pradhan Mantri Awas Yojana.", "economic": "Strong financial turnaround with debt reduction and high order-to-sales visibility across diversified infrastructure verticals.", "social": "Brings clean piped tap water directly to millions of rural homes in Uttar Pradesh and Maharashtra under Jal Jeevan Mission.", "technological": "Heavy mechanization: slip-form pavers for concrete roads, pre-cast building structural erection, and water treatment filtration engineering.", "legal": "Public tender bidding norms, FIDIC civil contract compliance, and state labor welfare regulations.", "environmental": "Constructs massive sewage treatment plants (STPs) and water reclamation facilities, cleaning urban river basins."},
        [0.24, 0.52, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; mid-size contractors exist, but qualifying for multi-thousand-crore government mega-tenders requires past completion certificates.", "bargaining_power_of_buyers": "Moderate; government authorities award tenders to L1 qualified bidders under strict milestone conditions.", "bargaining_power_of_suppliers": "Low to moderate; bulk procurement of construction steel, cement, and concrete.", "threat_of_substitutes": "Low; physical infrastructure construction is mandatory for national economic expansion.", "competitive_rivalry": "High in civil bidding with Dilip Buildcon, KNR Constructions, and PNC Infratech."}
    ),
    (
        "Bharat Electronics Limited (BEL)", "Infrastructure, EPC & Capital Goods",
        "Indian Army, Indian Navy, Indian Air Force, and strategic homeland security agencies",
        "require ultra-advanced military radar systems, electronic warfare suites, missile weapon control systems, and secure defense avionics",
        "Akash Weapon System Radar, Electronic Warfare Suites & Smart Avionics", "Navratna Defense Electronics & Tactical Radar Systems",
        "stands as India's premier defense electronics company with an order book over Rs 75,000 Cr, supplying 85%+ of electronic radar systems to the armed forces",
        [0.88, 0.94, 0.98, 0.98, 0.90, 0.75],
        {"political": "Navratna PSU under Ministry of Defence; crown jewel of Atmanirbhar Bharat in military electronics and indigenization.", "economic": "Debt-free balance sheet with high return on capital employed (>30%); protected order pipeline under Defence Acquisition Procedure (Buy Indian-IDDM).", "social": "Guarantees national territorial integrity against hostile aerial threats, securing Indian airspace with advanced 3D surveillance radars.", "technological": "Active Electronically Scanned Array (AESA) radars, indigenously developed electronic warfare systems (Shakti), and secure encrypted software radios.", "legal": "Directorate General of Quality Assurance (DGQA) military clearances, defense secrecy acts, and sovereign procurement laws.", "environmental": "Operates solar-powered manufacturing complexes; RoHS compliant lead-free military electronics fabrication."},
        [0.10, 0.35, 0.30, 0.15, 0.40],
        {"threat_of_new_entrants": "Zero; sovereign military electronic clearances, defense security credentials, and DRDO R&D integration cannot be replicated by new entrants.", "bargaining_power_of_buyers": "High; Ministry of Defence sets acquisition timelines and terms, but relies completely on BEL for indigenous radar deployment.", "bargaining_power_of_suppliers": "Moderate; specialized defense semiconductor chips and microwave components.", "threat_of_substitutes": "Zero; military weapon control and tactical radars have no civilian substitutes.", "competitive_rivalry": "Negligible in core defense electronics; clear national monopoly ahead of emerging private defense entrants."}
    ),
    (
        "Hindustan Aeronautics Limited (HAL)", "Infrastructure, EPC & Capital Goods",
        "Indian Air Force, Indian Navy, Indian Army, and friendly export nations",
        "need indigenous supersonic fighter jets, combat helicopters, advanced jet trainers, and comprehensive aerospace fleet overhaul and lifecycle support",
        "LCA Tejas Mk1A Fighter Aircraft & Prachand Light Combat Helicopter", "Navratna Sovereign Aerospace Defense & Combat Aircraft Manufacturing",
        "is India's sole military aircraft manufacturer, engineering the Tejas supersonic multi-role fighter and the world's only attack helicopter capable of operating at 5,000m (Prachand)",
        [0.90, 0.95, 0.98, 0.98, 0.90, 0.75],
        {"political": "Maharatna defense aerospace powerhouse; the supreme flagship of India's aerospace sovereign defense independence.", "economic": "Historic record order backlog exceeding Rs 94,000 Cr for 83 Tejas Mk1A fighters and 156 Prachand combat helicopters, ensuring decade-long revenue visibility.", "social": "National pride: represents India's pinnacle aerospace engineering capability, inspiring thousands of young engineers across the country.", "technological": "Carbon-fiber composite airframe manufacturing, digital glass cockpits, fly-by-wire flight control computers, and indigenous gas turbine engine design.", "legal": "Centre for Military Airworthiness and Certification (CEMILAC) flight clearances, DGQA approvals, and military defense contracts.", "environmental": "Energy-efficient aircraft manufacturing hangars, solar rooftop plants, and composite lightweighting cutting aircraft fuel burn."},
        [0.08, 0.30, 0.35, 0.15, 0.35],
        {"threat_of_new_entrants": "Zero; manufacturing supersonic fighter aircraft and military combat helicopters requires sovereign capital and national security mandates.", "bargaining_power_of_buyers": "High; Indian Air Force is the primary customer and dictates technical operational requirements.", "bargaining_power_of_suppliers": "High; dependent on international jet engine suppliers (GE Aerospace F404/F414 engines) and specialized titanium forgings.", "threat_of_substitutes": "Low; imported foreign fighters (Rafale) cost 2-3x more and create strategic foreign dependence.", "competitive_rivalry": "Zero domestically; absolute sovereign monopoly in military combat aircraft manufacturing."}
    ),
    (
        "Bharat Heavy Electricals Limited (BHEL)", "Infrastructure, EPC & Capital Goods",
        "thermal and hydro power plants, Indian Railways, nuclear reactors, and heavy industrial process plants",
        "require heavy utility-scale steam and gas turbines, high-speed electric trainsets (Vande Bharat), nuclear steam generators, and industrial boilers",
        "Supercritical Thermal Turbines, Vande Bharat Trainsets & Nuclear Boilers", "Maharatna Heavy Capital Goods & Power Equipment Monolith",
        "stands as India's premier heavy capital goods manufacturer with 16 manufacturing plants, having equipped over 50% of India's total power generation capacity",
        [0.86, 0.92, 0.96, 0.94, 0.88, 0.75],
        {"political": "Maharatna PSU under Ministry of Heavy Industries; key recipient of thermal power equipment orders under India's 80 GW thermal addition plan.", "economic": "Turnaround backed by massive order inflows from NTPC for supercritical 800 MW power islands and Indian Railways for 80 Vande Bharat sleeper trainsets.", "social": "Foundational cornerstone of India's post-independence heavy industrialization, providing township infrastructure in Bhopal, Haridwar, and Trichy.", "technological": "Heavy precision rotor machining, supercritical 800 MW boilers operating at 600 deg C, and high-speed train bogie traction systems.", "legal": "CERC technical standards, boiler inspectorate compliance (IBR), and public sector procurement bidding rules.", "environmental": "Advanced Flue Gas Desulfurization (FGD) systems cutting sulfur dioxide emissions from coal power plants by over 90%."},
        [0.15, 0.40, 0.35, 0.20, 0.55],
        {"threat_of_new_entrants": "Zero; building multi-thousand-ton forging presses and heavy turbine manufacturing plants requires decades and sovereign capital.", "bargaining_power_of_buyers": "Moderate; NTPC and state utilities negotiate strictly, but government mandates domestic manufacturing for power equipment.", "bargaining_power_of_suppliers": "Moderate; specialized heavy alloy rotor forgings and boiler steel tubes.", "threat_of_substitutes": "Low; heavy steam turbines and electric train propulsion systems are technologically indispensable.", "competitive_rivalry": "Low to moderate; competes primarily with L&T in domestic supercritical thermal equipment."}
    ),
    (
        "Cummins India", "Infrastructure, EPC & Capital Goods",
        "hyperscale data centers, hospitals, commercial complexes, mining excavators, and railways",
        "need ultra-reliable, high-horsepower diesel and natural gas generator sets that provide instant backup power within seconds of grid failure",
        "High-Horsepower Diesel Generator Sets & CPCB IV+ Compliant Engines", "Heavy Industrial Engines & Prime Power Generation Equipment",
        "leads India's high-horsepower power generation market with over 50% share, delivering CPCB IV+ ultra-low-emission engines powering India's top data centers",
        [0.75, 0.92, 0.96, 0.95, 0.86, 0.82],
        {"political": "Complies with Central Pollution Control Board (CPCB IV+) strict emission norms enforced for all industrial diesel generator sets.", "economic": "Phenomenal return on capital (ROCE >35%) driven by explosive data center expansion in Mumbai, Chennai, and Noida requiring multi-megawatt backup gensets.", "social": "Guarantees that intensive care units, emergency hospital wards, and air traffic control towers maintain continuous power during blackouts.", "technological": "Advanced electronic common-rail fuel systems, selective catalytic reduction (SCR) exhaust aftertreatment, and dual-fuel hydrogen-diesel engines.", "legal": "CPCB emission certification, Bureau of Indian Standards compliance, and corporate listing governance.", "environmental": "Pioneered CPCB IV+ clean engine technology cutting nitrogen oxide (NOx) and particulate matter emissions by up to 90% compared to earlier models."},
        [0.22, 0.48, 0.40, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; designing engines that meet severe CPCB IV+ emission caps while maintaining 10-second start-up reliability requires deep engine IP.", "bargaining_power_of_buyers": "Moderate; hyperscale data centers (AWS, Microsoft) demand unyielding reliability and willingly pay a premium for Cummins engines.", "bargaining_power_of_suppliers": "Low to moderate; captive global supply chains and precision component sourcing.", "threat_of_substitutes": "Moderate from industrial battery energy storage (BESS), but batteries cannot sustain 48 hours of continuous full-load data center power.", "competitive_rivalry": "Moderate; dominates high-horsepower segments ahead of Kirloskar Oil Engines and Caterpillar."}
    ),
    (
        "Thermax Limited", "Infrastructure, EPC & Capital Goods",
        "energy-intensive industrial manufacturing plants (textiles, chemicals, refineries, food processing)",
        "require clean process heating, energy-efficient industrial boilers, waste heat recovery, and industrial water recycling solutions",
        "Biomass Industrial Boilers, Waste Heat Recovery & Industrial Water Systems", "Green Energy, Environmental Solutions & Industrial Boilers",
        "leads India in sustainable industrial energy solutions, helping thousands of manufacturing plants transition from fossil coal to clean biomass energy",
        [0.78, 0.90, 0.95, 0.94, 0.86, 0.88],
        {"political": "Direct beneficiary of National Clean Air Programme, industrial carbon emission limits, and agricultural biomass co-firing directives.", "economic": "Clean balance sheet with zero net debt; high order book driven by corporate ESG capex investments into green steam and effluent recycling.", "social": "Helps solve North India's winter air pollution crisis by turning agricultural stubble (paddy straw) into clean industrial boiler fuel pellets.", "technological": "Circulating Fluidized Bed Combustion (CFBC) boilers, absorption chillers powered by industrial waste heat, and zero-liquid discharge effluent plants.", "legal": "Indian Boiler Regulations (IBR), CPCB industrial pollution standards, and international ASME boiler codes.", "environmental": "Enables industries to achieve water-neutrality through membrane bioreactors and cuts millions of tons of industrial greenhouse gas emissions."},
        [0.22, 0.48, 0.38, 0.20, 0.62],
        {"threat_of_new_entrants": "Low; engineering custom thermodynamic heat exchangers and chemical absorption chillers has high engineering hurdles.", "bargaining_power_of_buyers": "Moderate; industrial factory owners calculate payback periods and thermal efficiency guarantees.", "bargaining_power_of_suppliers": "Moderate; boiler-grade alloy steel tubes and specialized valves.", "threat_of_substitutes": "Low; industrial process steam is indispensable for chemical, pharmaceutical, and textile manufacturing.", "competitive_rivalry": "Moderate; leading green technology player competing with Forbes Marshall and BHEL."}
    ),
    (
        "KEC International (RPG Group)", "Infrastructure, EPC & Capital Goods",
        "power utilities, railway boards, urban transit authorities, and solar developers across 100+ countries",
        "require turnkey engineering, procurement, and construction for high-voltage power transmission lines, railway overhead electrification, and urban metro viaducts",
        "765 kV / 1200 kV Power Transmission EPC & Railway 25 kV Electrification", "Global Power Transmission & Multi-Modal Infrastructure EPC",
        "is a global infrastructure EPC titan with presence in 100+ countries, having powered millions of homes through 765 kV transmission corridors and high-speed rail electrification",
        [0.80, 0.92, 0.95, 0.92, 0.85, 0.78],
        {"political": "Major executor for POWERGRID's Green Energy Corridors and Indian Railways' Mission 100% Electrification.", "economic": "Robust order book (>Rs 30,000 Cr) diversified across power transmission, railways, civil buildings, cables, and solar EPC.", "social": "Electrifies rural rail tracks and wheels renewable energy from remote solar deserts into urban power consumption centers.", "technological": "Helicopter tower erection in mountainous terrain, automated stringing of high-voltage transmission lines, and high-speed railway catenary installation.", "legal": "International FIDIC construction contracts, statutory Right of Way clearances, and safety compliances.", "environmental": "Enables the evacuation of zero-emission renewable electricity from solar parks, displacing coal power generation."},
        [0.22, 0.50, 0.38, 0.20, 0.68],
        {"threat_of_new_entrants": "Low to moderate; executing 765 kV transmission lines across difficult terrains requires heavy financial guarantees and tower fabrication assets.", "bargaining_power_of_buyers": "Moderate; utilities award contracts via competitive e-reverse auctions.", "bargaining_power_of_suppliers": "Low; in-house backward-integrated tower manufacturing plants in India, Dubai, and Brazil.", "threat_of_substitutes": "Low; high-voltage transmission lines are mandatory for bulk electricity wheeling.", "competitive_rivalry": "Direct rivalry with Kalpataru Projects International and L&T."}
    ),
    (
        "Kalpataru Projects International (KPIL)", "Infrastructure, EPC & Capital Goods",
        "global power utilities, oil and gas pipeline operators, urban transit authorities, and civil clients across 70+ countries",
        "need turnkey engineering and construction for mega power transmission lines, cross-country oil/gas pipelines, and underground metro tunnels",
        "Turnkey Power Transmission Lines, Oil & Gas Pipelines & Metro Rail EPC", "Global Infrastructure EPC & Industrial Construction Conglomerate",
        "stands as one of the world's largest specialized EPC companies following its strategic merger with JMC Projects, operating in 70+ countries",
        [0.80, 0.92, 0.95, 0.92, 0.85, 0.78],
        {"political": "Strategic EPC partner for national gas grid expansions (Urja Ganga) and interstate power transmission corridors under Make in India.", "economic": "Massive consolidated order book exceeding Rs 50,000 Cr; high revenue growth driven by international transmission and domestic water/pipeline contracts.", "social": "Builds critical physical connectivity: pipes gas to industrial clusters and connects remote rural populations to clean power grids.", "technological": "Automated pipeline welding rigs, horizontal directional drilling under riverbeds, and heavy-duty tower fabrication.", "legal": "Statutory pipeline right-of-use permissions, FIDIC international contract norms, and global labor safety certifications.", "environmental": "Trenchless pipeline installation preserving surface forests and waterways; eco-friendly precast civil construction methods."},
        [0.22, 0.50, 0.38, 0.20, 0.68],
        {"threat_of_new_entrants": "Low; executing cross-country pressurized gas pipelines and ultra-high-voltage transmission lines requires immense technical pre-qualification.", "bargaining_power_of_buyers": "Moderate; institutional clients negotiate competitive EPC margins in public tenders.", "bargaining_power_of_suppliers": "Low; captive tower fabrication plants in Gandhinagar, Raipur, and Sweden.", "threat_of_substitutes": "Low; pipelines and power lines have no engineering substitutes.", "competitive_rivalry": "Direct competition with KEC International and L&T Construction."}
    ),
    (
        "Dilip Buildcon", "Infrastructure, EPC & Capital Goods",
        "National Highways Authority of India (NHAI), state road development corporations, and commercial coal mining authorities",
        "need high-speed, early-completion highway and expressway construction, complex road tunnels, and mechanized coal overburden removal",
        "Expressway EPC Construction & Mechanized Surface Mining", "Highway Infrastructure EPC & Early Project Completion Specialist",
        "built a legendary reputation in the Indian road construction sector by completing complex national expressways months ahead of contractual deadlines",
        [0.82, 0.92, 0.95, 0.90, 0.85, 0.72],
        {"political": "Major construction partner for NHAI's flagship Bharatmala Pariyojana expressways and dedicated economic corridors.", "economic": "Earns substantial early completion bonus payments from NHAI; unique asset-heavy business model owning India's largest fleet of heavy construction machinery.", "social": "Builds world-class asphalt expressways connecting agricultural heartlands to major port cities, reducing travel times and vehicle wear.", "technological": "Vast captive fleet of GPS-tracked machinery (Caterpillar, Wirtgen), computerized asphalt batching plants, and automated slip-form paving machines.", "legal": "NHAI concession agreements, environmental forest clearances, and strict labor safety protocols on highway construction sites.", "environmental": "Cold-in-place recycling of old asphalt roads, tree transplanting along highway corridors, and solar-powered highway rest stops."},
        [0.24, 0.52, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Low to moderate; matching Dilip Buildcon's 10,000-piece captive machinery fleet and speed-execution culture is a major hurdle.", "bargaining_power_of_buyers": "Moderate; NHAI sets standard contractual milestone payments and performance metrics.", "bargaining_power_of_suppliers": "Low; massive bulk purchaser of diesel, bitumen, cement, and construction equipment.", "threat_of_substitutes": "Low; physical expressways are the backbone of domestic logistics.", "competitive_rivalry": "High in road construction bidding with PNC Infratech, GR Infraprojects, and KNR Constructions."}
    ),
    (
        "PNC Infratech", "Infrastructure, EPC & Capital Goods",
        "NHAI, state road development corporations, and urban airport authorities across Northern India",
        "require precision, high-durability concrete highway and expressway construction, runway resurfacing, and water supply projects",
        "Agra-Lucknow & Purvanchal Expressway EPC Projects", "Highway, Expressway & Airport Runway Construction",
        "has constructed landmark infrastructure including segments of the Agra-Lucknow Expressway and Yamuna Expressway, delivering top-quality concrete pavements",
        [0.82, 0.92, 0.95, 0.90, 0.85, 0.72],
        {"political": "Key highway developer for Uttar Pradesh Expressways Industrial Development Authority (UPEIDA) and NHAI.", "economic": "Conservative balance sheet with low net debt and strong operating cash flows; successful monetization of road assets via InvIT platforms.", "social": "Transformed transportation connectivity across Uttar Pradesh, reducing driving time between Delhi and Lucknow to under 5 hours.", "technological": "Heavy-duty concrete batching plants, automated slip-form concrete pavers, and high-precision laser road levelers.", "legal": "Highway concession agreements, right-of-way handover verifications, and statutory environmental clearances.", "environmental": "Utilizes fly ash from thermal power plants in road embankment filling, conserving topsoil and reducing industrial waste."},
        [0.24, 0.52, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; bidding on large expressway EPC packages requires substantial financial net worth and equipment bank guarantees.", "bargaining_power_of_buyers": "Moderate; government authorities award tenders via competitive reverse auctions.", "bargaining_power_of_suppliers": "Low to moderate; localized aggregate quarries, bulk cement, and steel rebars.", "threat_of_substitutes": "Low; multi-lane expressways are essential infrastructure.", "competitive_rivalry": "High with Dilip Buildcon, GR Infraprojects, and Ashoka Buildcon."}
    ),
    (
        "GR Infraprojects", "Infrastructure, EPC & Capital Goods",
        "NHAI, Indian Railways, and state highway authorities across 16 Indian states",
        "need high-speed road, highway, and railway civil EPC backed by in-house backward-integrated manufacturing of bitumen and road safety products",
        "HAM Highway Projects & Integrated Road Safety Manufacturing", "Backward-Integrated Highway EPC & Railway Infrastructure",
        "operates an integrated road EPC model, manufacturing its own bitumen emulsions, crash barriers, and road signs to achieve superior cost control and project delivery",
        [0.82, 0.92, 0.95, 0.90, 0.85, 0.72],
        {"political": "Strategic partner for NHAI's Hybrid Annuity Model (HAM) highway projects and railway track doubling corridors.", "economic": "Industry-leading EBITDA margins in road construction powered by 100% captive manufacturing of road signages, metal beam crash barriers, and emulsions.", "social": "Constructs critical mountain highway passes and interstate bypasses, improving passenger transit safety across northern and western states.", "technological": "In-house emulsion plants, automated cold-milling road recyclers, and computerized toll plaza architecture.", "legal": "NHAI HAM concession agreements, IRC road safety guidelines, and environmental impact compliances.", "environmental": "Rubber-modified bitumen using recycled end-of-life vehicle tires, creating longer-lasting roads and recycling rubber waste."},
        [0.24, 0.52, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; backward integration into manufacturing road safety hardware gives GR Infra a cost advantage over pure civil contractors.", "bargaining_power_of_buyers": "Moderate; NHAI HAM projects offer semi-annual inflation-indexed annuity payments with low traffic risk.", "bargaining_power_of_suppliers": "Low; in-house manufacturing of road components cuts external supplier dependence.", "threat_of_substitutes": "Low; physical road infrastructure.", "competitive_rivalry": "High in tender bidding with PNC Infratech, Dilip Buildcon, and KNR."}
    ),
    (
        "Ashoka Buildcon", "Infrastructure, EPC & Capital Goods",
        "highway authorities, commercial road users, and state power distribution corporations",
        "require build-operate-transfer (BOT) highway development, complex river bridge engineering, and power distribution infrastructure",
        "BOT & HAM Highway Concessions & Power Distribution EPC", "Highway Concessionaire, Bridge Engineering & Power EPC",
        "is one of India's leading highway developers with over 40 PPP road projects executed, operating high-density commercial tollways across western India",
        [0.82, 0.92, 0.95, 0.90, 0.85, 0.72],
        {"political": "Key participant in NHAI highway asset monetization and central power sector reforms (Revamped Distribution Sector Scheme - RDSS).", "economic": "Steady toll revenues complemented by large-scale EPC construction; successfully unlocked equity capital by divesting mature BOT toll roads to global investors.", "social": "Builds critical river bridges and bypass roads that eliminate hours of bottleneck traffic for rural and semi-urban communities.", "technological": "Heavy cable-stayed bridge engineering, mechanized cantilever construction over deep rivers, and automated electronic toll plazas.", "legal": "NHAI concession agreements, Indian Roads Congress (IRC) structural design codes, and state environmental permissions.", "environmental": "Adopts green construction practices, utilizing industrial fly ash in embankments and installing solar lighting at all toll plazas."},
        [0.25, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; executing complex cable-stayed bridges and securing long-term bank funding requires established credentials.", "bargaining_power_of_buyers": "Moderate; toll rates are statutory under National Highway rules; NHAI sets standard tender conditions.", "bargaining_power_of_suppliers": "Low to moderate; standard cement, structural steel, and bitumen procurement.", "threat_of_substitutes": "Low; essential transport corridors.", "competitive_rivalry": "Moderate to high with IRB Infrastructure and other national highway developers."}
    ),
    (
        "Titagarh Rail Systems", "Infrastructure, EPC & Capital Goods",
        "Indian Railways, urban metro rail corporations (Pune Metro, Surat Metro), and international railway networks",
        "need modern lightweight aluminum and stainless steel metro passenger coaches, high-speed Vande Bharat trainsets, and heavy freight wagons",
        "Pune Metro Aluminum Coaches, Vande Bharat Trainsets & Freight Wagons", "Modern Passenger Metro & Freight Rail Rolling Stock Manufacturing",
        "pioneered modern passenger rail manufacturing in India, delivering India's first lightweight aluminum metro trainsets and winning 80 Vande Bharat sleeper trains",
        [0.85, 0.92, 0.96, 0.95, 0.88, 0.82],
        {"political": "Crown jewel of Make in India in railways; strategic consortium partner with BHEL executing historic Vande Bharat trainset orders.", "economic": "Explosive order book growth exceeding Rs 27,000 Cr; high-margin transition from basic freight wagons to high-tech passenger metro coaches.", "social": "Modernizes urban transit for millions of daily commuters, providing European-standard air-conditioned, whisper-quiet metro travel.", "technological": "Acquired Italian coach maker Firema; automated laser welding of aerospace-grade aluminum car bodies, and regenerative braking bogies.", "legal": "Research Designs and Standards Organisation (RDSO) railway clearances, metro rail safety commissioner approvals, and international rail standards (EN 15085).", "environmental": "Lightweight aluminum coaches reduce train weight by over 30%, cutting traction electrical energy consumption by millions of kilowatt-hours annually."},
        [0.18, 0.42, 0.35, 0.20, 0.55],
        {"threat_of_new_entrants": "Low; rail carbody extrusion, laser welding, and RDSO crash-test validations require massive specialized manufacturing plants.", "bargaining_power_of_buyers": "Moderate; Indian Railways and state metro corporations negotiate tenders, but Titagarh is one of very few certified domestic manufacturers.", "bargaining_power_of_suppliers": "Moderate; specialized aluminum extrusions and imported railway electronics.", "threat_of_substitutes": "Low; urban metro systems and freight railways are the backbone of sustainable public transit.", "competitive_rivalry": "Moderate; competes with Jupiter Wagons, BEML, and Alstom India."}
    ),
    (
        "Jupiter Wagons", "Infrastructure, EPC & Capital Goods",
        "Indian Railways, logistics freight operators, and commercial fleet owners",
        "require modern, high-capacity specialized freight wagons, disc brake systems, track crossing points, and commercial electric trucks",
        "Specialized Freight Wagons, Railway Brake Systems & Jupiter EV Trucks", "Railway Freight Rolling Stock & Electric Commercial Vehicles",
        "is a dominant manufacturer of freight wagons for Indian Railways, holding over 25% market share and expanding into railway braking systems and commercial EVs",
        [0.82, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Major beneficiary of Indian Railways' Mission 3,000 MT freight loading target by 2030 and dedicated freight corridors.", "economic": "Robust order book (>Rs 7,000 Cr) with high operating leverage; backward-integrated into wheelsets and modern disc brake foundries.", "social": "Enables the mass movement of essential food grains, coal, and steel across India, reducing logistics costs for the entire economy.", "technological": "Specialized high-axle-load wagon engineering, forged alloy wheels, and lightweight commercial electric delivery truck platforms.", "legal": "RDSO quality certifications, railway safety standards, and commercial vehicle homologation approvals (ARAI).", "environmental": "Shifting freight from polluting highway diesel trucks to electrified rail freight slashes carbon emissions by up to 80%."},
        [0.22, 0.48, 0.38, 0.22, 0.60],
        {"threat_of_new_entrants": "Low; building wagon assembly lines and securing RDSO vendor registration takes years of rigorous quality audits.", "bargaining_power_of_buyers": "Moderate; Indian Railways is the primary wagon buyer, purchasing through bulk procurement tenders.", "bargaining_power_of_suppliers": "Moderate; specialized steel plates, wheelsets, and draft gear components.", "threat_of_substitutes": "Low for bulk freight movement (coal, cement, grains).", "competitive_rivalry": "Direct rivalry with Titagarh Rail Systems and Texmaco Rail."}
    ),
    (
        "BEML Limited", "Infrastructure, EPC & Capital Goods",
        "urban metro rail corporations, defense armed forces, and open-cast coal/iron ore mining conglomerates",
        "demand heavy engineering solutions: stainless steel metro cars, heavy tactical missile launchers, and high-capacity mining dump trucks",
        "Stainless Steel Metro Coaches, Heavy Mining Dumpers & Defense Tatra Trucks", "Miniratna Multi-Sector Heavy Engineering & Defense Conglomerate",
        "stands as India's pioneer in metro coach manufacturing and heavy mining dumpers, having manufactured over 2,000 modern metro cars for Delhi, Mumbai, and Bengaluru",
        [0.86, 0.92, 0.96, 0.94, 0.88, 0.75],
        {"political": "Miniratna Schedule-A public enterprise under Ministry of Defence; key recipient of Make in India urban transport and defense equipment mandates.", "economic": "Diversified across three high-growth verticals: Mining & Construction, Defence & Aerospace, and Rail & Metro, providing resilient multi-sector cash flows.", "social": "Powers the daily metro transit of millions of office workers in India's top cities and equips defense forces with heavy all-terrain mobility.", "technological": "High-tonnage hydraulic excavators, driverless Unattended Train Operation (UTO) metro trainsets, and 8x8 heavy tactical missile launcher vehicles.", "legal": "RDSO railway certifications, DGQA military quality clearances, and statutory public sector corporate governance.", "environmental": "Developed India's first indigenous electric drive mining dump truck and zero-emission battery-powered excavators."},
        [0.15, 0.40, 0.32, 0.18, 0.50],
        {"threat_of_new_entrants": "Zero; heavy multi-disciplinary engineering infrastructure across Bengaluru, KGF, and Mysuru cannot be replicated.", "bargaining_power_of_buyers": "Moderate; public sector buyers (Coal India, MoD, Metro rail boards) procure under formal tender structures.", "bargaining_power_of_suppliers": "Moderate; specialized traction motors, heavy steel forgings, and defense hydraulic systems.", "threat_of_substitutes": "Low; specialized heavy tactical vehicles and metro trainsets have no civilian substitutes.", "competitive_rivalry": "Moderate with Titagarh in metro coaches, and Caterpillar/Komatsu in mining equipment."}
    ),
    (
        "Mazagon Dock Shipbuilders", "Infrastructure, EPC & Capital Goods",
        "Indian Navy and Indian Coast Guard",
        "require stealth guided-missile destroyers, Scorpene-class diesel-electric attack submarines, and stealth frigates to secure national maritime borders",
        "Project 15B Stealth Destroyers & Kalvari-Class Scorpene Submarines", "Navratna Sovereign Defense Shipbuilder & Submarine Specialist",
        "stands as India's premier defense shipyard ('Shipbuilder to the Nation'), having built the most sophisticated stealth warships and submarines for the Indian Navy",
        [0.90, 0.96, 0.98, 0.98, 0.90, 0.78],
        {"political": "Navratna shipyard under Ministry of Defence; critical sovereign asset executing the Indian Navy's blue-water maritime security doctrine.", "economic": "Historic order book exceeding Rs 38,000 Cr; debt-free with massive cash balances and industry-leading return on equity (>35%).", "social": "Defends India's 7,500 km coastline and international sea lines of communication against hostile naval incursions.", "technological": "Underwater submarine acoustic signature dampening, automated missile vertical launch systems, and hull construction from specialized DMR-249A high-tensile steel.", "legal": "Naval Staff Qualitative Requirements (NSQR), Warship Overseeing Team (WOT) defense audits, and classified military security acts.", "environmental": "Dry dock wastewater treatment, eco-friendly hull antifouling coatings, and energy-efficient dockyard cranes."},
        [0.05, 0.30, 0.30, 0.10, 0.30],
        {"threat_of_new_entrants": "Zero; construction of military stealth destroyers and attack submarines requires sovereign classified dockyard infrastructure and nuclear/weapon clearances.", "bargaining_power_of_buyers": "High; Indian Navy is the sole domestic buyer, but relies completely on Mazagon Dock for submarine manufacturing.", "bargaining_power_of_suppliers": "Moderate to high; specialized naval weapons, combat management systems (BEL), and propulsion turbines.", "threat_of_substitutes": "Zero; naval warships and submarines have no substitutes.", "competitive_rivalry": "Zero in submarines; limited collaboration/allocation alongside Garden Reach Shipbuilders."}
    ),
    (
        "Cochin Shipyard", "Infrastructure, EPC & Capital Goods",
        "Indian Navy, international European shipowners, and national inland waterway authorities",
        "need construction of indigenous aircraft carriers, specialized zero-emission electric cargo ferries, and comprehensive commercial ship repair",
        "INS Vikrant Indigenous Aircraft Carrier & Green Hydrogen Electric Ferries", "Miniratna Premier Commercial & Defense Shipyard",
        "built INS Vikrant—India's first indigenous aircraft carrier—and operates India's largest commercial ship repair facility, pioneering electric inland ferries",
        [0.88, 0.94, 0.98, 0.96, 0.90, 0.82],
        {"political": "Miniratna Schedule-A PSU under Ministry of Ports, Shipping and Waterways; flagship builder of sovereign naval aircraft carriers.", "economic": "Dual revenue engine: high-value defense shipbuilding contracts combined with high-margin, counter-cyclical commercial vessel repairs across India.", "social": "Showcases India's entry into the elite club of 6 nations capable of designing and building a 40,000-ton aircraft carrier.", "technological": "Building automated zero-emission green hydrogen inland waterway vessels, electric catamarans for Kochi Water Metro, and ice-class commercial vessels for Europe.", "legal": "International Maritime Organization (IMO) vessel construction codes, Classification Societies (DNV, IRS) certifications, and defense standards.", "environmental": "Pioneering green maritime shipping: designed and built India's first hydrogen fuel-cell vessel and electric battery passenger catamarans."},
        [0.10, 0.35, 0.30, 0.12, 0.40],
        {"threat_of_new_entrants": "Zero; building aircraft carrier dry docks and marine ship-lift facilities takes decades and thousands of crores in public capital.", "bargaining_power_of_buyers": "Moderate; Indian Navy contracts are negotiated on cost-plus/fixed-price bases, while European commercial clients seek green fuel tech.", "bargaining_power_of_suppliers": "Moderate; marine steel plates, diesel generators, and marine propulsion propellers.", "threat_of_substitutes": "Zero; marine vessels are indispensable for global ocean trade and sovereign naval defense.", "competitive_rivalry": "Low; operates in specialized commercial repair and mega-carrier construction."}
    ),
    (
        "Garden Reach Shipbuilders & Engineers (GRSE)", "Infrastructure, EPC & Capital Goods",
        "Indian Navy, Indian Coast Guard, and international friendly maritime nations",
        "require advanced stealth guided-missile frigates, anti-submarine warfare corvettes, survey vessels, and rapid-deployment military Bailey bridges",
        "Project 17A Stealth Frigates, ASW Shallow Water Craft & Portable Bailey Bridges", "Navratna Defense Warship Construction & Engineering",
        "is a premier defense shipyard in Kolkata with over 60 years of heritage, having built over 100 warships for the Indian Navy and pioneering portable steel Bailey bridges",
        [0.88, 0.94, 0.98, 0.96, 0.90, 0.78],
        {"political": "Navratna enterprise under Ministry of Defence; critical partner for indigenization of naval combatants in Eastern India.", "economic": "Robust order book exceeding Rs 22,000 Cr for advanced stealth frigates (P-17A) and anti-submarine shallow water corvettes.", "social": "Secures the vital Bay of Bengal and Andaman & Nicobar maritime choke points against foreign submarine infiltration.", "technological": "Modular warship construction using 250-ton Goliath gantry cranes, integrated stealth radar-evasive superstructures, and tactical combat management.", "legal": "Naval quality assurance certifications, defense procurement procedures, and public sector governance.", "environmental": "Modernized shipyard with zero toxic liquid discharge and installation of captive solar generation."},
        [0.10, 0.35, 0.30, 0.12, 0.40],
        {"threat_of_new_entrants": "Zero; warship integration and defense security clearances exclude new private entrants.", "bargaining_power_of_buyers": "High; Ministry of Defence is the sole domestic buyer, but allocates orders to ensure shipyard capacity utilization.", "bargaining_power_of_suppliers": "Moderate; defense electronics (BEL), diesel marine engines, and specialized warship steel.", "threat_of_substitutes": "Zero for naval defense combatants.", "competitive_rivalry": "Low; collaborates with Mazagon Dock on national warship build allocations."}
    )
]

for item in sector17_data:
    add_c(*item)

print(f"Sector 17 added: {len(sector17_data)} companies. Total: {len(part3_b)}")

# ==============================================================================
# SECTOR 18: Real Estate & Commercial Development (20 companies)
# ==============================================================================
sector18_data = [
    (
        "DLF Limited", "Real Estate & Commercial Development",
        "ultra-high-net-worth individuals, multinational corporate tenants, and luxury home buyers",
        "need opulent, world-class luxury residential condominiums and prime Grade-A corporate tech campuses with guaranteed infrastructure and green spaces",
        "DLF Cyber City Gurugram & The Camellias Ultra-Luxury Residences", "Integrated Ultra-Luxury Residential & Grade-A Commercial Real Estate",
        "is India's largest listed real estate developer, having transformed Gurugram into a global tech hub and created 'The Camellias'—India's most coveted super-luxury address",
        [0.78, 0.94, 0.96, 0.92, 0.88, 0.80],
        {"political": "Strategic economic force in Delhi-NCR; complies strictly with Real Estate (Regulation and Development) Act (RERA) and municipal master plans.", "economic": "Turned net debt-free with tens of thousands of crores in pre-sales bookings and massive annuity rental income from DLF Cyber City (DCCDL joint venture with GIC).", "social": "The Camellias and Magnolias redefined billionaire luxury living in India; pioneered the modern corporate IT park campus culture in North India.", "technological": "Seismic Zone IV earthquake-resistant design, automated smart building management systems, and high-efficiency HVAC air purification.", "legal": "Full RERA registration, transparent land titles with zero encumbrance, and environmental impact assessment (EIA) clearances.", "environmental": "US Green Building Council (USGBC) LEED Platinum certifications across Cyber City; massive urban green belts and recycled water irrigation."},
        [0.18, 0.45, 0.32, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; acquiring thousands of contiguous acres of prime land in Gurugram and building a 40-million-sq-ft Grade-A commercial portfolio is impossible for a newcomer.", "bargaining_power_of_buyers": "Low; ultra-luxury apartments sell out in hours via invitation-only bookings with multi-crore upfront deposits.", "bargaining_power_of_suppliers": "Low; contractors (L&T, Shapoorji) compete for DLF's landmark construction contracts.", "threat_of_substitutes": "Low; location and exclusivity in DLF Golf Links have no substitutes.", "competitive_rivalry": "Low to moderate; dominates the North Indian luxury and institutional commercial market."}
    ),
    (
        "Godrej Properties", "Real Estate & Commercial Development",
        "urban home buyers, working professionals, and middle-to-luxury families across 12 Indian cities",
        "demand trustworthy, transparent homebuying with guaranteed on-time delivery, pristine corporate ethics, and contemporary architectural design",
        "Godrej Residential Townships & Luxury Urban Living", "National Multi-City Residential Real Estate Developer",
        "is India's most geographically diversified residential developer, leveraging the 126-year-old Godrej family brand of trust to lead sales bookings nationwide",
        [0.75, 0.94, 0.96, 0.92, 0.88, 0.82],
        {"political": "Strict adherence to RERA guidelines and local municipal building codes across all 12 operating states.", "economic": "Leads the Indian real estate sector in annual sales bookings (>Rs 20,000 Cr), using capital-efficient joint-development and outright land acquisition models.", "social": "The Godrej brand represents the gold standard of trust for Indian middle-class families investing their life savings into a home.", "technological": "BIM 3D architectural modeling, digital 3D virtual home walkthroughs, and mechanized aluminum formwork (Mivan) construction for rapid floor casting.", "legal": "100% RERA registered projects with flawless title deed due diligence and zero land litigation.", "environmental": "Committed to sustainable habitats: 100% of projects are IGBC/GRIHA green-building certified, with rainwater harvesting and solar lighting."},
        [0.25, 0.50, 0.35, 0.24, 0.72],
        {"threat_of_new_entrants": "Low to moderate; local developers exist, but consumers increasingly migrate to trusted corporate brands following post-RERA consolidation.", "bargaining_power_of_buyers": "Moderate; home buyers compare amenities and prices, but pay a premium for Godrej's delivery assurance.", "bargaining_power_of_suppliers": "Low; civil construction contractors compete for Godrej's continuous nationwide project pipeline.", "threat_of_substitutes": "Moderate from secondary resale homes and rival corporate developers.", "competitive_rivalry": "High with Macrotech (Lodha), Prestige, and DLF across top metro corridors."}
    ),
    (
        "Macrotech Developers (Lodha)", "Real Estate & Commercial Development",
        "homebuyers across premium luxury, aspirational mid-income, and integrated smart township segments",
        "need master-planned smart city living with integrated schools, retail, and transit, or iconic luxury residential high-rises in core Mumbai",
        "Palava Smart City & Lodha World Towers Luxury Residences", "Integrated Smart Townships & Iconic Ultra-Luxury High-Rises",
        "is India's largest residential real estate developer by sales bookings, building the 4,500-acre Palava smart city and Mumbai's iconic 76-story World Towers",
        [0.76, 0.94, 0.96, 0.92, 0.88, 0.80],
        {"political": "Major contributor to Maharashtra's integrated township policies, smart city infrastructure, and affordable housing development.", "economic": "Aggressive debt reduction transformed company to a strong investment-grade balance sheet; generates over Rs 14,000 Cr in annual pre-sales.", "social": "Palava Smart City provides 100,000+ citizens with planned urban living: walkable schools, workplaces, sports complexes, and clean air.", "technological": "High-rise structural wind-tunnel engineering, Mivan rapid concrete shuttering, and integrated smart-city digital civic governance in Palava.", "legal": "RERA registered, clear land titles, and municipal environmental clearances.", "environmental": "Palava uses 100% recycled wastewater for landscaping and flushing; certified IGBC green cities and net-zero carbon roadmap."},
        [0.22, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; master-planning a 4,500-acre smart city and constructing 75-story skyscrapers requires massive capital and civil credentials.", "bargaining_power_of_buyers": "Moderate; buyers have options across Mumbai, but Lodha offers unmatched amenities and township infrastructure.", "bargaining_power_of_suppliers": "Low; bulk procurement power over civil contractors, steel, and elevators.", "threat_of_substitutes": "Moderate from other Mumbai developers (Godrej, Oberoi).", "competitive_rivalry": "Intense rivalry with Oberoi Realty and Godrej Properties in the Mumbai Metropolitan Region."}
    ),
    (
        "Oberoi Realty", "Real Estate & Commercial Development",
        "affluent families, corporate executives, and high-net-worth individuals in the Mumbai Metropolitan Region",
        "demand flawless construction quality, pristine architectural finishes, and integrated luxury developments that consistently appreciate in value",
        "Oberoi Garden City Goregaon & Three Sixty West Worli", "Premium & Luxury Integrated Developments & Five-Star Hospitality",
        "maintains the highest operating profit margins in Indian real estate (>50% EBITDA margin), delivering architectural masterpieces like Three Sixty West Worli",
        [0.76, 0.94, 0.96, 0.94, 0.88, 0.82],
        {"political": "Compliant with Maharashtra RERA regulations and Mumbai Development Control and Promotion Regulations (DCPR 2034).", "economic": "Pristine balance sheet with minimal net debt; high recurring annuity income from Oberoi Mall, Commerz tech parks, and The Ritz-Carlton hotel.", "social": "The definitive aspirational address for Mumbai's top corporate leaders, bollywood icons, and financial titans.", "technological": "Partnered with global architectural luminaries (KPF, Larsen & Toubro for construction), high-speed smart elevators, and acoustic glass facades.", "legal": "100% RERA compliant, impeccable land title track record with zero stalled projects in company history.", "environmental": "IGBC Platinum and Gold green building certified developments, energy-efficient building envelopes, and greywater recycling systems."},
        [0.18, 0.45, 0.32, 0.20, 0.65],
        {"threat_of_new_entrants": "Very low; land parcels in prime Mumbai (Worli, Bandra, Goregaon) are exceedingly scarce and require immense capital.", "bargaining_power_of_buyers": "Low to moderate; affluent buyers willingly pay a 15-20% brand premium for Oberoi's guaranteed construction quality.", "bargaining_power_of_suppliers": "Low; premier construction contractors (L&T) build for Oberoi.", "threat_of_substitutes": "Low in the super-luxury Mumbai micro-market.", "competitive_rivalry": "Moderate; competes with Lodha and Godrej in select luxury Mumbai sub-markets."}
    ),
    (
        "Prestige Estates Projects", "Real Estate & Commercial Development",
        "homebuyers, multinational IT tenants, and retail shoppers across Bengaluru, Mumbai, NCR, and Hyderabad",
        "require master-planned luxury residential communities, modern Grade-A IT tech parks, and vibrant destination retail shopping malls",
        "Prestige Lakeside Habitat, Prestige Tech Parks & Forum Malls", "Diversified Multi-Asset Real Estate & Tech Park Developer",
        "is the undisputed real estate king of South India, having delivered over 150 million sq ft of developments and expanding aggressively into Mumbai and NCR",
        [0.76, 0.94, 0.96, 0.92, 0.88, 0.80],
        {"political": "Complies with RERA across Karnataka, Maharashtra, and NCR; active partner in urban transit-oriented developments.", "economic": "Exceptional pre-sales trajectory exceeding Rs 20,000 Cr; high annuity rental streams from Grade-A commercial tech parks and hospitality (JW Marriott).", "social": "Shaped the physical skyline of Silicon Valley Bengaluru, housing hundreds of thousands of IT professionals in modern gated communities.", "technological": "Precast concrete construction technology, smart home automation, and energy-efficient building management across commercial campuses.", "legal": "Full RERA registration, clear title due diligence, and statutory municipal environmental sanctions.", "environmental": "Extensive rainwater recharging pits, indigenous tree landscaping, and energy-efficient double-glazed glass commercial facades."},
        [0.22, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; building a 150-million-sq-ft delivered track record and relationships with global tech giants (Microsoft, Cisco) takes decades.", "bargaining_power_of_buyers": "Moderate; buyers have developer choices, but trust Prestige's delivery scale and master-community amenities.", "bargaining_power_of_suppliers": "Low; massive bulk purchasing of cement, structural steel, and interior fittings.", "threat_of_substitutes": "Moderate from other southern developers (Brigade, Sobha).", "competitive_rivalry": "Moderate in South India; competes with Lodha and Godrej in Mumbai."}
    ),
    (
        "Sobha Limited", "Real Estate & Commercial Development",
        "discerning homebuyers, corporate multinationals, and clients seeking German-standard engineering precision",
        "demand uncompromising structural quality, self-manufactured wooden interiors, and flawless architectural finishing with zero snags",
        "Sobha Dream Acres & Backward-Integrated Residential Enclaves", "Backward-Integrated Precision Residential Real Estate",
        "stands as India's only fully backward-integrated real estate developer, manufacturing its own concrete blocks, timber woodwork, metal glazing, and mattresses",
        [0.74, 0.92, 0.95, 0.94, 0.86, 0.80],
        {"political": "Full compliance with RERA; model developer cited for flawless construction safety and transparent customer delivery charters.", "economic": "Consistent, high-margin execution; backward integration eliminates contractor markups and delivers superior margin retention.", "social": "Founded by PNC Menon; runs extensive philanthropic social projects in Palakkad, Kerala, providing free homes, healthcare, and education to impoverished families.", "technological": "German precision woodworking and joinery factory, automated glazing division, precast concrete plants, and in-house Sobha Academy for construction skills.", "legal": "100% RERA compliant, impeccable land title deeds, and environmental safety clearances.", "environmental": "Zero-waste manufacturing philosophy; wood shavings recycled into briquettes, and captive solar energy powering factory operations."},
        [0.22, 0.45, 0.30, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; impossible for traditional real estate developers to duplicate Sobha's captive German manufacturing and training infrastructure.", "bargaining_power_of_buyers": "Low to moderate; customers specifically choose Sobha for its legendary zero-defect build quality and long structural durability.", "bargaining_power_of_suppliers": "Extremely low; backward-integrated manufacturing eliminates external contractor and interior vendor dependencies.", "threat_of_substitutes": "Moderate from other tier-1 branded developers.", "competitive_rivalry": "Moderate; commands a unique quality-conscious niche in Bengaluru, Kochi, and Gurugram."}
    ),
    (
        "Brigade Enterprises", "Real Estate & Commercial Development",
        "urban professionals, multinational corporations, and lifestyle shoppers in South India",
        "need integrated mixed-use master developments that combine residential towers, Grade-A tech offices, shopping malls, and hospitality under one roof",
        "Brigade Gateway Integrated Enclave & World Trade Center Bengaluru", "Integrated Mixed-Use Urban Enclaves & Commercial Offices",
        "pioneered integrated master enclaves in India with Brigade Gateway, housing the World Trade Center, Orion Mall, Columbia Asia Hospital, and Sheraton Hotel",
        [0.75, 0.92, 0.95, 0.92, 0.86, 0.80],
        {"political": "RERA compliant across Karnataka, Tamil Nadu, and Kerala; holds exclusive license for World Trade Center (WTC) developments in South India.", "economic": "Balanced portfolio: robust residential pre-sales balanced by stable annuity rentals from commercial tech parks, Orion Malls, and hotels.", "social": "Elevates urban lifestyle standards, creating walkable '15-minute city' communities where residents live, work, shop, and relax in one location.", "technological": "Smart building management systems, seismic-resistant engineering, automated parking management, and digital customer property portals.", "legal": "RERA certifications, statutory municipal layout sanctions, and fire safety compliances.", "environmental": "Extensive lake restoration projects (Brigade restored several urban Bengaluru lakes) and green-certified building campuses."},
        [0.24, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; assembling 40-acre contiguous land parcels inside core metro cities to build mixed-use enclaves requires massive capital.", "bargaining_power_of_buyers": "Moderate; buyers appreciate the convenience and capital appreciation of integrated enclave apartments.", "bargaining_power_of_suppliers": "Low to moderate; diversified civil contractors and material vendors.", "threat_of_substitutes": "Moderate from standalone residential apartments.", "competitive_rivalry": "Moderate; healthy competition with Prestige and Sobha in Bengaluru."}
    ),
    (
        "The Phoenix Mills", "Real Estate & Commercial Development",
        "global retail brands, luxury fashion houses, entertainment seekers, and urban shoppers",
        "demand grand destination shopping malls with premier international retail curation, fine dining, multiplexes, and celebratory public spaces",
        "Phoenix Palladium Mumbai & Phoenix Marketcity Malls", "India's Undisputed King of Destination Retail & Lifestyle Malls",
        "is India's premier retail-led real estate developer, operating over 11 million sq ft of destination shopping malls that generate the country's highest consumption spends",
        [0.76, 0.94, 0.96, 0.94, 0.88, 0.82],
        {"political": "Complies with municipal commercial retail regulations, fire safety codes, and local commercial establishment licensing.", "economic": "Exceptional business model: earns fixed base rentals plus a percentage of retail tenant consumption turnover, hedging inflation and driving compounding cash flows.", "social": "Phoenix Palladium and Marketcity malls are the premier weekend social, dining, and retail hubs for millions of urban families in top metros.", "technological": "Automated footfall thermal tracking cameras, AI tenant sales analytics, smart parking guidance systems, and mobile loyalty shopping apps.", "legal": "Commercial leasing contracts, statutory fire safety certifications, and corporate public listing compliances.", "environmental": "LEED Gold certified retail developments, extensive rainwater harvesting, and solar rooftop installations cutting common-area power usage."},
        [0.15, 0.40, 0.30, 0.18, 0.48],
        {"threat_of_new_entrants": "Very low; developing a 1.5-million-sq-ft destination mall and attracting 300+ global brands (Zara, Apple, Gucci) requires unmatched retail leasing trust.", "bargaining_power_of_buyers": "Low; international brands must be present in Phoenix malls to reach affluent Indian consumers.", "bargaining_power_of_suppliers": "Low; civil construction and interior finishing contractors.", "threat_of_substitutes": "Moderate from e-commerce for basic goods, but experiential dining and entertainment malls cannot be substituted online.", "competitive_rivalry": "Low to moderate; undisputed national market leader in destination shopping malls ahead of DLF Retail."}
    ),
    (
        "Mahindra Lifespace Developers", "Real Estate & Commercial Development",
        "homebuyers seeking green, sustainable living, and multinational manufacturers needing plug-and-play industrial cities",
        "need 100% green-certified residential apartments and fully integrated industrial smart cities (Mahindra World City) with plug-and-play infrastructure",
        "Mahindra Happinest, Alcove & Mahindra World City (MWC)", "Sustainable Green Homes & Integrated Industrial Cities",
        "pioneered sustainable green-certified homes in India, alongside integrated industrial mega-cities (MWC Chennai and Jaipur) hosting global export manufacturers",
        [0.78, 0.92, 0.95, 0.92, 0.86, 0.88],
        {"political": "Supports Make in India and export manufacturing; MWC operates Special Economic Zones (SEZs) and Domestic Tariff Areas.", "economic": "Dual engine: asset-light residential development backed by Mahindra brand trust, and high-value industrial land leasing to global MNCs (BMW, JCB).", "social": "Promotes healthy, eco-friendly urban living and creates hundreds of thousands of industrial manufacturing jobs in Mahindra World Cities.", "technological": "Precast concrete construction, smart water meters, net-zero waste management, and solar-powered common amenities.", "legal": "100% RERA compliant, SEZ regulatory approvals, and strict environmental impact assessments.", "environmental": "India's first real estate developer committed to 100% green-certified residential portfolio; net-zero carbon development roadmap."},
        [0.22, 0.48, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; developing 3,000-acre integrated industrial cities with sovereign highway/rail connectivity requires institutional credibility.", "bargaining_power_of_buyers": "Moderate; homebuyers appreciate Mahindra's green credentials and delivery trust.", "bargaining_power_of_suppliers": "Low; competitive civil contractor bidding.", "threat_of_substitutes": "Moderate in residential; low in integrated industrial cities.", "competitive_rivalry": "Moderate; competes with Godrej in housing and private industrial parks."}
    ),
    (
        "Sunteck Realty", "Real Estate & Commercial Development",
        "ultra-high-net-worth individuals, corporate CXOs, and aspirational luxury buyers in Mumbai",
        "need ultra-luxury, bespoke residential living in Mumbai's central business districts (BKC) and upscale mixed-use suburban townships",
        "Signature Island Bandra-Kurla Complex & Sunteck City Goregaon", "Bespoke Ultra-Luxury & Premium Mixed-Use Urban Living",
        "is a dominant luxury real estate developer in Mumbai, having created Signature Island in BKC—the ultra-exclusive residential home of India's top bankers and business leaders",
        [0.75, 0.92, 0.95, 0.92, 0.86, 0.78],
        {"political": "Complies with Maharashtra RERA and Mumbai Metropolitan Region Development Authority (MMRDA) land use norms.", "economic": "High-margin luxury focus; low debt-to-equity ratio and strong cash flows from flagship projects in BKC, Oshiwara, and Naigaon.", "social": "The definitive status symbol residence for Mumbai's top corporate CEOs, investment bankers, and high-net-worth investors.", "technological": "High-specification structural glazing, acoustic insulation, private elevator foyers, and smart home integrated automation.", "legal": "100% RERA registered, clear land titles, and strict adherence to MMRDA urban planning guidelines.", "environmental": "Energy-efficient architectural orientation reducing solar heat gain; LEED gold certified developments with rainwater harvesting."},
        [0.22, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; acquiring residential land parcels in Mumbai's prime commercial hub (BKC) is virtually impossible today.", "bargaining_power_of_buyers": "Low to moderate; ultra-wealthy buyers prioritize address prestige and privacy over minor price differences.", "bargaining_power_of_suppliers": "Low; premier construction contractors execute to tight tolerances.", "threat_of_substitutes": "Moderate from luxury South Mumbai heritage residences.", "competitive_rivalry": "High in Mumbai luxury with Oberoi Realty and Lodha."}
    ),
    (
        "Puravankara Limited", "Real Estate & Commercial Development",
        "middle-class families, first-time homebuyers, and luxury residential seekers across South and West India",
        "need well-constructed, amenity-rich gated communities with transparent pricing and dependable on-time delivery",
        "Purva Luxury Living & Provident Housing Affordable Homes", "Diversified Multi-Segment Residential Real Estate",
        "serves over 45,000 happy families across 9 cities with a dual-brand approach: luxury Purva residences and affordable Provident Housing",
        [0.74, 0.90, 0.95, 0.90, 0.86, 0.78],
        {"political": "Active developer under Pradhan Mantri Awas Yojana (PMAY) via Provident Housing; fully compliant with RERA regulations.", "economic": "Strong sales booking momentum across Bengaluru, Chennai, Hyderabad, and Pune; successful monetization of large land bank parcels.", "social": "Empowers middle-class and first-time homebuyer families to own quality gated community apartments with swimming pools and sports amenities.", "technological": "Pioneered precast concrete construction in India for large-scale housing, cutting construction timelines by over 30%.", "legal": "RERA registered projects, clear title deeds, and compliance with municipal town planning regulations.", "environmental": "Extensive rainwater harvesting, organic waste converters, and green landscape belts in residential layouts."},
        [0.25, 0.50, 0.35, 0.24, 0.70],
        {"threat_of_new_entrants": "Moderate; local builders compete, but lack Puravankara's 48-year brand trust and precast construction scale.", "bargaining_power_of_buyers": "Moderate; mid-income buyers compare prices and loan EMI options across developers.", "bargaining_power_of_suppliers": "Low; competitive civil contractor ecosystem.", "threat_of_substitutes": "Moderate from other regional residential builders.", "competitive_rivalry": "High with Prestige, Brigade, and Sobha in South India."}
    ),
    (
        "Kolte-Patil Developers", "Real Estate & Commercial Development",
        "homebuyers and families across Pune, Mumbai, and Bengaluru",
        "need master-planned residential townships with expansive green spaces, sports clubs, and dependable on-time possession in Western India",
        "Life Republic Integrated Township & 24K Luxury Residences", "Dominant Pune Real Estate Developer & Integrated Townships",
        "is the dominant market leader in Pune real estate with nearly 3 decades of heritage, building the landmark 400-acre Life Republic integrated township",
        [0.74, 0.92, 0.95, 0.90, 0.86, 0.78],
        {"political": "Complies strictly with Maharashtra RERA; key driver of Pune's emergence as an IT and automotive manufacturing residential hub.", "economic": "Consistent sales momentum backed by dominant Pune market share; expanding presence in Mumbai redevelopment projects with high capital efficiency.", "social": "Life Republic houses over 15,000 happy residents, providing a holistic, self-contained community close to Hinjewadi IT park.", "technological": "Mivan shuttering technology, smart township water management, automated security surveillance, and digital CRM platforms.", "legal": "100% RERA compliant, clear title deeds, and environmental clearances for mega-townships.", "environmental": "Extensive tree planting, solar street lighting, and biological sewage treatment recycling 100% of wastewater for township gardens."},
        [0.25, 0.50, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low to moderate; local Pune builders exist, but Kolte-Patil's multi-decade brand reputation and 400-acre township scale form a moat.", "bargaining_power_of_buyers": "Moderate; IT employees in Hinjewadi evaluate commute times and community amenities.", "bargaining_power_of_suppliers": "Low; local construction contractors and material suppliers.", "threat_of_substitutes": "Moderate from other Pune developers.", "competitive_rivalry": "Moderate; dominates Pune ahead of regional peers."}
    ),
    (
        "Embassy Office Parks REIT", "Real Estate & Commercial Development",
        "multinational technology giants (Fortune 500 tech, BFSI GCCs) and institutional yield investors",
        "need world-class, integrated Grade-A office tech campuses with campus amenities, 100% power redundancy, and quarterly cash dividend yields",
        "Embassy Manyata & Embassy TechVillage Grade-A Tech Campuses", "Asia's First & Largest Publicly Listed Real Estate Investment Trust (REIT)",
        "owns over 45 million sq ft of premier office campuses housing 240+ global blue-chip clients, paying out 100% of net distributable cash flows as dividends",
        [0.78, 0.94, 0.96, 0.95, 0.88, 0.85],
        {"political": "Pioneered REIT regulations under SEBI; key stakeholder in India's Global Capability Centers (GCC) policy and Special Economic Zone reforms.", "economic": "Resilient, high-occupancy business model (>85% occupancy); contracted 15% rent escalations every 3 years provide inflation-beating dividend growth.", "social": "Hosts over 250,000 knowledge workers across Bengaluru, Mumbai, Pune, and NCR; funds large-scale government school health and education programs.", "technological": "Proprietary digital tenant workplace app (Embassy One), automated air quality index monitoring, and high-tech corporate security operations centers.", "legal": "Regulated by SEBI REIT Regulations 2014, mandatory distribution of >=90% net cash flows, and transparent corporate governance.", "environmental": "USGBC LEED Platinum and Gold certified office parks, 100 MW captive solar park in Bellary, and ambitious Net Zero 2040 commitment."},
        [0.12, 0.40, 0.30, 0.18, 0.48],
        {"threat_of_new_entrants": "Zero; assembling 45 million sq ft of Grade-A campus assets with Fortune 500 tenants and sovereign credit ratings cannot be duplicated.", "bargaining_power_of_buyers": "Low to moderate; global tech giants (Google, IBM, Wells Fargo) invest hundreds of crores in interior fit-outs and renew multi-year leases.", "bargaining_power_of_suppliers": "Low; standardized campus facility management and maintenance contractors.", "threat_of_substitutes": "Low; physical office collaboration is critical for enterprise IP security and Global Capability Centers.", "competitive_rivalry": "Low to moderate; competes with Mindspace REIT and Brookfield India REIT for institutional tenant expansions."}
    ),
    (
        "Mindspace Business Parks REIT", "Real Estate & Commercial Development",
        "leading multinational tech, financial, and healthcare Global Capability Centers (GCCs)",
        "require master-planned, sustainable Grade-A commercial office parks in prime business micro-markets with institutional property management",
        "Mindspace Madhapur Hyderabad & Mindspace Airoli Navi Mumbai", "Grade-A Commercial Office Campus Real Estate Investment Trust",
        "operates 33+ million sq ft of prime commercial office campuses sponsored by K Raheja Corp, hosting the world's leading tech and financial institutions",
        [0.78, 0.94, 0.96, 0.95, 0.88, 0.85],
        {"political": "Regulated under SEBI REIT frameworks; vital infrastructure anchor for Telangana and Maharashtra IT/GCC growth policies.", "economic": "Superior cash distribution yield, low loan-to-value (LTV <22%), and high recurring rental collections from multinational corporate tenants.", "social": "Powers the IT engine of Hyderabad and Navi Mumbai, providing high-quality workplace environments and urban green spaces.", "technological": "Smart building IoT sensors optimizing HVAC energy, automated visitor management, and electric vehicle fleet charging stations.", "legal": "Full SEBI REIT regulatory compliance, clean title due diligence, and mandatory quarterly dividend distributions.", "environmental": "Over 95% of the portfolio is green-certified; extensive rooftop solar arrays, zero-liquid discharge STP recycling, and organic waste composting."},
        [0.15, 0.42, 0.30, 0.18, 0.50],
        {"threat_of_new_entrants": "Zero; creating a 33-million-sq-ft institutional office portfolio in Madhapur and Airoli is an insurmountable barrier.", "bargaining_power_of_buyers": "Moderate; multinational tenants negotiate lease terms, but value Mindspace's campus ecosystem and power reliability.", "bargaining_power_of_suppliers": "Low; specialized facilities management services.", "threat_of_substitutes": "Low; Grade-A certified office space is non-negotiable for Fortune 500 GCC compliance.", "competitive_rivalry": "Moderate; competes with Embassy Office Parks REIT."}
    ),
    (
        "Brookfield India Real Estate Trust", "Real Estate & Commercial Development",
        "premier global corporate occupiers and institutional income-seeking investors",
        "demand institutional, ESG-compliant Grade-A corporate office campuses backed by global asset management standards and attractive dividend payouts",
        "Candor TechSpace Campuses & Downtown Powai Commercial Assets", "Global-Grade Commercial Office Campus REIT",
        "is India's only institutionally managed commercial office REIT backed by Brookfield Asset Management, managing 25+ million sq ft across prime metro corridors",
        [0.78, 0.94, 0.96, 0.95, 0.88, 0.85],
        {"political": "SEBI-regulated REIT; direct conduit for global institutional capital investment into Indian urban infrastructure.", "economic": "Stable, inflation-hedged dividend distribution supported by 100% institutional Grade-A assets and strong rent collection efficiency (>99%).", "social": "Enhances employee productivity and well-being through modern campus dining, sports courts, and curated cultural events.", "technological": "Centralized ESG monitoring dashboards, digital touchless access controls, and energy-efficient building automation.", "legal": "SEBI REIT compliance, statutory public disclosures, and global anti-corruption compliance under Brookfield Group.", "environmental": "IGBC Platinum certified tech campuses, 100% renewable power procurement for select parks, and water-positive operations."},
        [0.15, 0.42, 0.30, 0.18, 0.50],
        {"threat_of_new_entrants": "Zero; Brookfield's global institutional relationships and multi-billion-dollar campus portfolio cannot be replicated by new entrants.", "bargaining_power_of_buyers": "Moderate; Fortune 500 tenants evaluate campus quality and commute convenience.", "bargaining_power_of_suppliers": "Low; professional facility management vendors.", "threat_of_substitutes": "Low for institutional GCCs.", "competitive_rivalry": "Moderate; competes with Embassy REIT and Mindspace REIT."}
    ),
    (
        "Nexus Select Trust", "Real Estate & Commercial Development",
        "leading international and domestic retail brands, movie multiplexes, and destination shopping consumers across 14 cities",
        "need high-consumption destination retail shopping mall space with guaranteed footfalls, and investors seeking pure retail consumption cash yields",
        "Select CITYWALK Delhi & Nexus Destination Malls Portfolio", "India's First Publicly Listed Retail Consumption REIT",
        "is India's premier retail REIT, owning 17 Grade-A urban shopping malls across 14 cities—including the legendary Select CITYWALK in South Delhi",
        [0.78, 0.94, 0.96, 0.94, 0.88, 0.82],
        {"political": "Pioneered retail REIT listings under SEBI; key beneficiary of urban middle-class consumption growth and formal retail expansion.", "economic": "Captures direct upside from booming Indian retail spending via minimum guaranteed rent plus turnover revenue share; 100% cash flow payout.", "social": "Select CITYWALK and Nexus malls are the premier community gathering places, hosting cultural festivals, dining, and luxury entertainment.", "technological": "Digital shopper tracking, heat-map retail footfall analytics, automated parking management, and unified digital gift card ecosystems.", "legal": "SEBI REIT statutory regulations, retail lease covenants, and municipal commercial safety guidelines.", "environmental": "Extensive rooftop solar generation, energy-efficient chilled water HVAC systems, and zero-waste food court composting."},
        [0.12, 0.40, 0.28, 0.15, 0.45],
        {"threat_of_new_entrants": "Zero; owning iconic retail landmarks like Select CITYWALK Delhi and Nexus Elante Chandigarh is an unassailable geographical moat.", "bargaining_power_of_buyers": "Low; retail brands must have anchor presence in Nexus malls to access high-spending urban shoppers.", "bargaining_power_of_suppliers": "Low; specialized mall facility management and security services.", "threat_of_substitutes": "Low; experiential dining, cinema, and luxury fashion try-on cannot be replicated online.", "competitive_rivalry": "Low to moderate; operates as the only pure-play retail REIT in India alongside The Phoenix Mills."}
    ),
    (
        "Signature Global (India)", "Real Estate & Commercial Development",
        "middle-income and lower-middle-class families, first-time home buyers, and young working professionals in Delhi-NCR",
        "need affordable, high-quality, and modern gated residential apartments with guaranteed RERA possession timelines in Gurugram",
        "Affordable & Mid-Segment Residential Housing Enclaves", "Dominant Affordable & Mid-Housing Developer in Delhi-NCR",
        "dominates affordable and mid-housing in Gurugram with over 35% market share, having delivered over 10 million sq ft of homes under Haryana housing policies",
        [0.76, 0.92, 0.96, 0.90, 0.86, 0.78],
        {"political": "Major beneficiary of Haryana Affordable Housing Policy and Pradhan Mantri Awas Yojana (PMAY) interest subsidies.", "economic": "Rapid capital turnaround: launches projects that sell out completely within days, generating rapid cash flows and high return on capital.", "social": "Enables thousands of middle-class families (teachers, engineers, small business owners) to realize the dream of owning a home in Gurugram.", "technological": "Aluform aluminum formwork construction casting an entire floor in 7 days, standardized modular architecture, and digital allotment processes.", "legal": "100% RERA registered, transparent state government lottery allotments, and strict statutory escrow account compliance.", "environmental": "IGBC Gold certified green homes, energy-efficient LED common lighting, and rainwater harvesting recharging groundwater aquifers."},
        [0.22, 0.48, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low to moderate; securing affordable housing licenses and delivering at capped price points requires immense execution speed.", "bargaining_power_of_buyers": "Low to moderate; immense demand outstrips supply, leading to oversubscribed applications.", "bargaining_power_of_suppliers": "Low; standardized bulk procurement of construction materials.", "threat_of_substitutes": "Moderate from unorganized builder floors in Delhi-NCR.", "competitive_rivalry": "Moderate; undisputed market leader in Gurugram affordable housing."}
    ),
    (
        "Anant Raj Limited", "Real Estate & Commercial Development",
        "cloud hyperscalers, artificial intelligence developers, and residential township dwellers in Delhi-NCR",
        "demand mega-scale green data center campuses with high power redundancy, alongside residential townships and commercial IT parks",
        "Anant Raj Green Data Centers & Residential Townships", "Hyperscale Green Data Centers & Delhi-NCR Real Estate",
        "is developing 300 MW of AI-ready green data center campuses in Manesar, Panchkula, and Rai by retrofitting massive owned IT park infrastructure",
        [0.78, 0.90, 0.95, 0.96, 0.86, 0.82],
        {"political": "Direct beneficiary of National Data Centre Policy and data localization mandates under the Digital Personal Data Protection (DPDP) Act.", "economic": "Transformational shift: retrofitting owned IT park buildings into high-margin data centers saves 70% capex and 3 years of construction time.", "social": "Creates high-tech digital infrastructure in Haryana, powering India's cloud and AI sovereignty.", "technological": "High-density server rack support (up to 40 kW/rack), direct-to-chip liquid cooling readiness, Tier-III uptime standards, and dual power substations.", "legal": "Data center security compliances, RERA for residential assets, and power transmission clearances.", "environmental": "PUE (Power Usage Effectiveness) <1.4, utilizing captive solar energy and adiabatic cooling to minimize water consumption."},
        [0.20, 0.45, 0.38, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; converting massive existing building structures with secured 100+ MW power substations creates a huge time-to-market advantage.", "bargaining_power_of_buyers": "Moderate; cloud hyperscalers negotiate capacity contracts, but face severe shortage of ready data center space in Delhi-NCR.", "bargaining_power_of_suppliers": "Moderate; precision electrical equipment (Schneider, ABB) and chilled water chillers.", "threat_of_substitutes": "Moderate from international data center operators (NTT, Equinix).", "competitive_rivalry": "Moderate; unique pioneer in retrofitted green data centers in North India."}
    ),
    (
        "Ashiana Housing", "Real Estate & Commercial Development",
        "senior citizens, retirees, and families seeking nurturing, child-centric residential communities",
        "need active senior living communities with 24/7 medical care, wheelchair accessibility, or child-centric homes with integrated sports coaching",
        "Senior Living Retirement Resorts & Child-Centric Homes", "Senior Living Communities & Child-Centric Housing Pioneer",
        "pioneered senior citizen retirement living in India, operating award-winning retirement resorts in Bhiwadi, Jaipur, Chennai, and Lavasa",
        [0.74, 0.90, 0.95, 0.88, 0.86, 0.80],
        {"political": "Supports national policies on senior citizen welfare and healthcare; complies with RERA regulations across all states.", "economic": "High customer loyalty and referral rates; annuity maintenance fees and specialized healthcare services provide recurring income.", "social": "Solves the acute social crisis of elderly loneliness and healthcare anxiety in India, providing vibrant, dignified retirement communities.", "technological": "Emergency response call systems in every room, wheelchair-accessible campus design with zero-step entries, and digital community apps.", "legal": "RERA registered, Maintenance and Welfare of Parents and Senior Citizens Act compliance, and consumer protection adherence.", "environmental": "Extensive lush green gardens, quiet walking tracks, rainwater harvesting, and organic waste composting."},
        [0.20, 0.45, 0.32, 0.20, 0.55],
        {"threat_of_new_entrants": "Low; managing active senior living requires specialized nursing care, geriatric dining, and compassionate community management.", "bargaining_power_of_buyers": "Moderate; seniors and their NRI children evaluate medical infrastructure and community warmth carefully.", "bargaining_power_of_suppliers": "Low; standard construction contractors.", "threat_of_substitutes": "Low; traditional unassisted residential apartments cannot cater to elderly mobility and medical emergencies.", "competitive_rivalry": "Low to moderate; undisputed pioneer and benchmark leader in Indian senior living communities."}
    ),
    (
        "Omaxe Limited", "Real Estate & Commercial Development",
        "middle-class families, local business owners, and commercial retail shoppers in Tier-2 and Tier-3 cities",
        "need modern master-planned residential townships, shopping malls, and commercial high streets in developing regional urban centers",
        "Integrated Tier-2/3 Regional Townships & High Street Commercials", "Tier-2 & Tier-3 City Real Estate & Township Developer",
        "has delivered over 130 million sq ft of real estate across 28 cities, pioneering modern township living in New Chandigarh, Lucknow, Indore, and Ludhiana",
        [0.72, 0.90, 0.94, 0.88, 0.84, 0.75],
        {"political": "Supports regional urbanization and Tier-2 smart city development policies across Northern and Central India.", "economic": "Large low-cost land banks in fast-growing non-metro cities provide high operational leverage as regional wealth expands.", "social": "Brings modern lifestyle amenities (clubhouses, shopping complexes, wide roads) to small-town families, elevating regional quality of life.", "technological": "Mechanized earthmoving and road paving, computerized layout planning, and digital customer relationship management.", "legal": "State RERA compliances, municipal town planning permissions, and statutory environmental clearances.", "environmental": "Extensive tree planting along township avenues and rainwater harvesting ponds recharging regional groundwater."},
        [0.26, 0.52, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; local regional contractors operate in Tier-2 cities, but lack Omaxe's organized master-township scale.", "bargaining_power_of_buyers": "Moderate; small-town buyers look for affordable price-points and reputable developer delivery.", "bargaining_power_of_suppliers": "Low; localized material and contractor sourcing.", "threat_of_substitutes": "Moderate from unorganized regional plot developers.", "competitive_rivalry": "Moderate; competes with regional builders in Lucknow and Punjab."}
    )
]

for item in sector18_data:
    add_c(*item)

print(f"Sector 18 added: {len(sector18_data)} companies. Total in Part 3B: {len(part3_b)}")

# Load part3_a.json and combine
part3_a_path = Path(__file__).parent / "part3_a.json"
with open(part3_a_path, "r", encoding="utf-8") as f:
    part3_a = json.load(f)

full_part3 = part3_a + part3_b
print(f"Combined Part 3 count: {len(full_part3)} companies (Expected: 122).")

# Save to scratch/part3.json
out_path = Path(__file__).parent / "part3.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(full_part3, f, indent=2)

print(f"SUCCESS: Saved {len(full_part3)} companies to {out_path}")
