"""
Omniscope AI - Part 3A Generator
Builds Sectors 13, 14, 15 (60 companies):
- Sector 13: Telecom, Fiber & Communications Infrastructure (18 companies)
- Sector 14: Power, Renewables & Clean Energy (22 companies)
- Sector 15: Oil, Gas, Refining & Petrochemicals (20 companies)
Outputs to scratch/part3_a.json
"""
import json
from pathlib import Path

part3_a = []

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    part3_a.append({
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
# SECTOR 13: Telecom, Fiber & Communications Infrastructure (18 companies)
# ==============================================================================
sector13_data = [
    (
        "Reliance Jio Infocomm", "Telecom, Fiber & Communications Infrastructure",
        "over 460 million Indian citizens, enterprises, and mobile internet users nationwide",
        "need ultra-fast, affordable, and seamless 4G/5G mobile connectivity, home broadband, and digital cloud applications",
        "Jio True 5G & JioFiber Home Broadband", "Nationwide 5G Standalone Wireless & Fiber Network",
        "built the world's largest Standalone 5G network powered by indigenous 5G radio technology, delivering high-speed internet at the world's lowest gigabyte tariffs",
        [0.85, 0.95, 0.99, 0.98, 0.88, 0.72],
        {"political": "National champion of Digital India; accelerated digital public infrastructure adoption and won substantial 5G spectrum allocations.", "economic": "Generates over Rs 1,00,000 Cr in revenue with industry-leading EBITDA margins; massive cash flows funded by 460M subscriber base.", "social": "Triggered India's digital revolution, lifting hundreds of millions of low-income citizens onto the digital economy, UPI, and streaming video.", "technological": "Pioneered indigenous 5G Standalone (SA) network core, Open-RAN architecture, and dense fiberization across 100% of Indian district headquarters.", "legal": "Telecom Regulatory Authority of India (TRAI) tariff norms, spectrum licensing agreements with Department of Telecommunications (DoT), and DPDP Act.", "environmental": "Energy-efficient 5G radio sleep modes and massive deployment of solar-powered off-grid telecom cell towers."},
        [0.10, 0.48, 0.30, 0.20, 0.75],
        {"threat_of_new_entrants": "Practically zero; acquiring spectrum auctions and deploying thousands of telecom towers requires tens of billions of dollars.", "bargaining_power_of_buyers": "Moderate; mobile subscribers can easily port numbers under MNP, but Jio offers the widest network coverage and free digital bundles.", "bargaining_power_of_suppliers": "Low; backward-integrated into proprietary in-house 5G stack and massive bulk purchasing power over optical fiber and electronics.", "threat_of_substitutes": "Low; mobile internet is a non-substitutable daily necessity of modern life.", "competitive_rivalry": "Duopoly competition with Bharti Airtel across 5G rollout and home fiber."}
    ),
    (
        "Bharti Airtel", "Telecom, Fiber & Communications Infrastructure",
        "quality-conscious smartphone users, high-spending families, and large enterprise corporations",
        "require premium high-speed network reliability, superior call voice quality, and integrated B2B enterprise cybersecurity and cloud solutions",
        "Airtel 5G Plus & Airtel Business Solutions", "Premium 5G Mobile Network & Enterprise ICT Solutions",
        "leads the Indian telecom industry in Average Revenue Per User (ARPU >Rs 200), delivering high-quality 5G Non-Standalone coverage and enterprise cloud security",
        [0.82, 0.94, 0.98, 0.96, 0.88, 0.74],
        {"political": "Critical stakeholder in national communications policy; operates across 17 countries in South Asia and Africa.", "economic": "Premium ARPU strategy cushions capital expenditure costs; high-margin B2B enterprise division powers resilient recurring free cash flow.", "social": "The preferred telecom operator for India's urban affluent and corporate professionals who prioritize continuous network uptime.", "technological": "Airtel 5G Plus utilizes Non-Standalone architecture for universal handset compatibility, paired with Nxtra green hyperscale data centers.", "legal": "TRAI regulations, adjusted gross revenue (AGR) statutory payment timelines, and DoT security compliance.", "environmental": "Nxtra by Airtel is committed to sourcing 50% of data center power from renewable energy; active energy-saving AI algorithms at cell sites."},
        [0.12, 0.45, 0.35, 0.20, 0.75],
        {"threat_of_new_entrants": "Practically zero; massive regulatory and capital barrier in Indian telecom.", "bargaining_power_of_buyers": "Moderate; high-ARPU post-paid and enterprise customers value network stability and are less sensitive to small tariff hikes.", "bargaining_power_of_suppliers": "Moderate; partners with global telecom equipment vendors (Ericsson, Nokia) for radio access networks.", "threat_of_substitutes": "Low; mobile connectivity is essential.", "competitive_rivalry": "Intense rivalry with Reliance Jio across premium subscriber acquisition and enterprise B2B contracts."}
    ),
    (
        "Indus Towers", "Telecom, Fiber & Communications Infrastructure",
        "mobile network operators (Airtel, Jio, Vodafone Idea) across all 22 Indian telecom circles",
        "need shared, highly reliable passive telecom tower infrastructure and uninterrupted power to host wireless antennae without redundant capital expenditure",
        "Shared Passive Telecom Towers & Green Energy Cell Sites", "Passive Telecommunications Infrastructure Sharing",
        "stands as the world's largest telecom tower infrastructure provider with over 220,000 towers, maintaining 99.98% network uptime for all major Indian telcos",
        [0.78, 0.90, 0.95, 0.90, 0.86, 0.78],
        {"political": "Critical national infrastructure partner for Department of Telecommunications; key enabler of national 5G network rollout mandates.", "economic": "Long-term 10-15 year tenancy master service agreements (MSAs) provide highly predictable annuity-like rental cash flows.", "social": "Powers mobile coverage in remote tribal areas, border regions, and densely populated urban slums.", "technological": "Automated tower operations centers (TOC) using IoT telemetry for real-time battery status, diesel pilferage prevention, and power optimization.", "legal": "Right of Way (RoW) municipal permissions, DoT telecom infrastructure provider (IP-1) licensing, and local property tax compliances.", "environmental": "Aggressively replacing diesel generators with high-capacity lithium-ion battery banks and solar photovoltaic hybrid setups at cell sites."},
        [0.15, 0.65, 0.35, 0.15, 0.50],
        {"threat_of_new_entrants": "Low; acquiring prime rooftop and ground-based real estate leases across 220,000 locations is virtually impossible for a newcomer.", "bargaining_power_of_buyers": "High; industry has consolidated into two main telco buyers (Airtel and Jio) who command strong lease negotiation leverage.", "bargaining_power_of_suppliers": "Low; standardized procurement of steel tubular masts, lithium batteries, and power converters.", "threat_of_substitutes": "Low; physical macro towers are mandatory for mobile cellular signal propagation.", "competitive_rivalry": "Low to moderate; operates with massive scale advantages over Brookfield/Summit Digitel."}
    ),
    (
        "Tejas Networks", "Telecom, Fiber & Communications Infrastructure",
        "telecom operators, state infrastructure agencies, and defense networks in India and 75+ countries",
        "demand indigenously designed, secure optical transmission networking, carrier routing, and 4G/5G wireless radio equipment",
        "TJ1400 Optical Transport & Indigenized 4G/5G RAN Architecture", "Indigenous Telecom Equipment & Optical Networking Systems",
        "stands as India's premier telecom product innovator, deploying wholly indigenous, secure 4G/5G radio and optical gear backed by the Tata Group",
        [0.85, 0.88, 0.92, 0.96, 0.88, 0.70],
        {"political": "Flagship recipient of Telecom PLI scheme and national trusted source telecom security approvals under National Security Council Secretariat (NSCS).", "economic": "Secured historic mega-orders from BSNL/DoT exceeding Rs 7,000 Cr to deploy indigenous 4G/5G network infrastructure across 100,000 sites.", "social": "Ensures national sovereign data security by eliminating foreign backdoors in critical telecom transmission backbones.", "technological": "Software-defined hardware architecture enabling remote upgrades from 4G to 5G via software; high-capacity multi-terabit optical transport.", "legal": "Strict adherence to TEC (Telecommunication Engineering Centre) certifications and global ITU telecom networking protocols.", "environmental": "Energy-efficient silicon design reducing operational power consumption of optical line terminals and wireless transceivers."},
        [0.22, 0.50, 0.45, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; telecom hardware R&D requires deep ASIC/FPGA engineering know-how and multi-year carrier interoperability trials.", "bargaining_power_of_buyers": "Moderate; major telcos negotiate strictly, but government mandates preferential market access for trusted indigenous gear.", "bargaining_power_of_suppliers": "Moderate to high; dependent on global semiconductor foundries (TSMC) for optical and baseband chipsets.", "threat_of_substitutes": "Moderate from multinational networking giants (Cisco, Huawei, Nokia).", "competitive_rivalry": "Moderate; protected in domestic sovereign contracts while expanding into global emerging markets."}
    ),
    (
        "Tata Communications", "Telecom, Fiber & Communications Infrastructure",
        "global enterprises, multinational corporations, and cloud hyperscalers across 190+ countries",
        "require high-bandwidth, ultra-low latency international data connectivity, subsea fiber routing, and secure cloud SD-WAN infrastructure",
        "Global Subsea Fiber Backbone & IZO Cloud Platform", "Global Digital Ecosystem & International Subsea Fiber Network",
        "owns the world's largest wholly-owned subsea fiber-optic cable network carrying over 30% of the world's internet traffic across 500,000 km of subsea fiber",
        [0.78, 0.92, 0.94, 0.96, 0.86, 0.74],
        {"political": "Strategic digital bridge connecting India to global internet hubs; holds international long-distance (ILD) statutory licenses.", "economic": "High-margin digital portfolio services (cloud, cybersecurity, IoT) growing rapidly, shifting business away from voice into recurring data annuity.", "social": "Enables global cross-border digital collaboration, video streaming, and financial transaction settlements worldwide.", "technological": "Global Tier-1 IP backbone (AS6453), software-defined wide area networking (SD-WAN), and multi-cloud interconnection fabric.", "legal": "Compliance with international maritime cable laws, telecom security frameworks, and cross-border data transfer laws.", "environmental": "Subsea cable infrastructure has low surface impact; data landing stations utilize green energy and seawater cooling."},
        [0.15, 0.48, 0.35, 0.18, 0.58],
        {"threat_of_new_entrants": "Practically impossible; laying 500,000 kilometers of trans-oceanic subsea fiber cables requires billions of dollars and international treaties.", "bargaining_power_of_buyers": "Moderate; global enterprises negotiate enterprise SLAs, but rely on Tata Communications for global routing redundancy.", "bargaining_power_of_suppliers": "Low; standardized subsea cable laying ships and optical repeaters.", "threat_of_substitutes": "Low; satellite internet (Starlink) cannot match the multi-terabit bandwidth capacity of physical optical subsea fiber.", "competitive_rivalry": "Moderate with global carrier transit giants (Lumen Technologies, NTT Communications, Telstra)."}
    ),
    (
        "Sterlite Technologies (STL)", "Telecom, Fiber & Communications Infrastructure",
        "telecom operators, cloud giants, and sovereign digital broadband missions globally",
        "need high-density optical fiber, specialized ribbon cables, and turnkey optical network design to handle exponential 5G and AI data growth",
        "Optical Fiber Preforms, Ribbon Cables & Turnkey Network Services", "Optical Fiber Solutions & Digital Network Integration",
        "is one of the world's few fully integrated optical fiber manufacturers, transforming raw silicon into high-density optical fiber with 700+ patents",
        [0.76, 0.88, 0.92, 0.95, 0.85, 0.72],
        {"political": "Key beneficiary of BharatNet rural broadband rollout and US/European government broadband stimulus programs (BEAD).", "economic": "Global export footprint across Europe, North America, and India; backward-integrated into silicon core preforms.", "social": "Enables high-speed fiber-to-the-home (FTTH) connectivity, bridging the digital divide for remote communities.", "technological": "Industry-leading 162-micron ultra-slim optical fiber allowing double the fiber density in existing city underground conduits.", "legal": "Global patent protection on optical fiber drawing and compliance with international ITU-T standards.", "environmental": "Zero Waste to Landfill (ZWL) certified manufacturing plants in Aurangabad, with 100% recycling of chemical byproducts."},
        [0.22, 0.50, 0.42, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; synthetic chemical glass vapor deposition and fiber preform drawing require immense capital and proprietary thermodynamic chemistry.", "bargaining_power_of_buyers": "Moderate; telcos procure fiber in massive volumes and negotiate per-kilometer pricing.", "bargaining_power_of_suppliers": "Moderate; high-purity silicon tetrachloride and chemical helium gases.", "threat_of_substitutes": "Low; optical fiber is the only physical medium capable of transmitting data at the speed of light.", "competitive_rivalry": "High with international fiber giants (Corning, Prysmian, HFCL)."}
    ),
    (
        "RailTel Corporation of India", "Telecom, Fiber & Communications Infrastructure",
        "Indian Railways, defense establishments, public sector enterprises, and rural citizens",
        "require exclusive, secure high-speed optical fiber communications and modern digital railway signaling along India's vast railway corridors",
        "RailWire Broadband & Railway Optical Fiber Infrastructure", "Sovereign Optical Fiber & Digital Railway Telecommunications",
        "operates an exclusive pan-India optical fiber network along 61,000+ route km of railway tracks, providing free high-speed Wi-Fi at 6,000+ railway stations",
        [0.82, 0.88, 0.95, 0.90, 0.86, 0.72],
        {"political": "Miniratna public sector undertaking under Ministry of Railways; holds exclusive Right of Way along Indian railway tracks.", "economic": "Consistently profitable and debt-free; dual monetization via government telecom project execution and retail RailWire broadband.", "social": "Station Wi-Fi transformed railway stations into digital learning centers for millions of students and porters in small Indian towns.", "technological": "High-reliability synchronous digital hierarchy (SDH) and dense wavelength division multiplexing (DWDM) fiber network along railway lines.", "legal": "DoT telecom license, railway safety act compliance, and public sector governance guidelines.", "environmental": "Fiber laid entirely within existing railway easements, requiring zero new land acquisition or deforestation."},
        [0.15, 0.45, 0.30, 0.20, 0.50],
        {"threat_of_new_entrants": "Non-existent; statutory exclusive right to lay telecom cables along the national railway track network.", "bargaining_power_of_buyers": "Moderate; government and defense agencies require secure dedicated communication lines.", "bargaining_power_of_suppliers": "Low; standardized optical fiber and switching hardware procurement.", "threat_of_substitutes": "Low for railway signaling and dedicated railway communications.", "competitive_rivalry": "Low in core railway domain; competes with private telcos for enterprise broadband."}
    ),
    (
        "HFCL (Himachal Futuristic Communications)", "Telecom, Fiber & Communications Infrastructure",
        "telecom operators, defense agencies, and enterprise network installers across India and abroad",
        "need high-performance optical fiber cables, PM-WANI Wi-Fi 6 access points, and indigenously designed 5G telecom backhaul radios",
        "io by HFCL (Wi-Fi 6 / 5G Small Cells) & Optical Fiber Cables", "Indigenous Optical Cable & Wireless Telecom Hardware",
        "manufactures indigenously engineered optical fiber cables and high-performance Wi-Fi 6 / 5G small cells, exporting telecom technology to 30+ countries",
        [0.78, 0.88, 0.92, 0.94, 0.85, 0.70],
        {"political": "Major beneficiary of Telecom Production Linked Incentive (PLI) scheme and national trusted telecom source guidelines.", "economic": "Strong order book from private telco 5G expansions (Jio, Airtel) and Indian defense communication network contracts.", "social": "Promotes PM-WANI public Wi-Fi initiative, enabling local grocery shops to become high-speed internet hotspots.", "technological": "In-house R&D centers in Bengaluru and Gurugram engineering 5G millimeter-wave radios, cloud network controllers, and micro-duct cables.", "legal": "TEC telecom certifications, Wi-Fi Alliance compliance, and BIS quality standards.", "environmental": "Solar energy integration at manufacturing plants in Hyderabad and Goa; recyclable polymer cable jacketing."},
        [0.24, 0.52, 0.42, 0.22, 0.68],
        {"threat_of_new_entrants": "Low to moderate; setting up high-speed optical cable extrusion and wireless hardware testing labs requires substantial capital.", "bargaining_power_of_buyers": "Moderate; telcos command volume pricing discounts.", "bargaining_power_of_suppliers": "Moderate; specialized semiconductor radio chips (Qualcomm) and optical preforms.", "threat_of_substitutes": "Low; optical fiber and Wi-Fi hardware are essential networking infrastructure.", "competitive_rivalry": "Moderate to high with Sterlite Technologies and international telecom OEMs."}
    ),
    (
        "Vodafone Idea (Vi)", "Telecom, Fiber & Communications Infrastructure",
        "mass mobile subscribers and enterprise B2B accounts across key Indian commercial circles",
        "need dependable voice and 4G data coverage, enterprise IoT telemetry, and flexible mobile post-paid family plans",
        "Vi GIGAnet 4G & Vi Business IoT Solutions", "National Cellular Voice, Data & Enterprise IoT Network",
        "serves over 215 million subscribers across India with integrated GIGAnet technology, leading in automotive smart-meter IoT deployments",
        [0.84, 0.80, 0.94, 0.90, 0.86, 0.70],
        {"political": "Government of India holds a significant equity stake through AGR debt conversion; strategic priority to preserve a 3-private-player market.", "economic": "Completed historic Rs 18,000 Cr follow-on public offer (FPO) to fund 4G network densification and selective 5G rollout.", "social": "Provides essential digital communication for hundreds of millions of citizens in Maharashtra, Gujarat, UP, and Kerala.", "technological": "Dynamic spectrum refarming, massive MIMO deployments, and eSIM-enabled cloud IoT platforms for smart meters.", "legal": "DoT licensing, TRAI quality of service regulations, and Supreme Court AGR dues installment frameworks.", "environmental": "Decommissioning redundant legacy cell sites post-merger to cut overall electrical power consumption."},
        [0.18, 0.55, 0.38, 0.25, 0.85],
        {"threat_of_new_entrants": "Zero; Indian telecom industry has impenetrable entry barriers.", "bargaining_power_of_buyers": "High; subscribers easily migrate to Jio or Airtel if network coverage is patchy.", "bargaining_power_of_suppliers": "Moderate; telecom tower and network equipment vendors demand timely clearing of dues.", "threat_of_substitutes": "Low; cellular connectivity is a baseline necessity.", "competitive_rivalry": "Intense; battles well-capitalized rivals Jio and Airtel in a fierce market share contest."}
    ),
    (
        "Mahanagar Telephone Nigam (MTNL)", "Telecom, Fiber & Communications Infrastructure",
        "government departments, central ministries, and historic residential subscribers in Delhi and Mumbai",
        "need reliable, secure landline telecommunications, dedicated government broadband lines, and official communications infrastructure",
        "MTNL Fixed Landline, Fiber Broadband & Government Leased Lines", "Public Sector Urban Telecom & Fixed-Line Infrastructure",
        "holds exclusive legacy underground copper and fiber ducts across Mumbai and Delhi, providing secure dedicated lines for sovereign ministries",
        [0.82, 0.70, 0.86, 0.78, 0.84, 0.65],
        {"political": "Wholly owned sovereign entity under Department of Telecommunications; operations closely integrated with BSNL under revival packages.", "economic": "Monetizing valuable prime real estate land parcels and underground duct assets in prime South Delhi and South Mumbai.", "social": "Historic emotional connect as the original telephone provider for millions of families in India's top two commercial hubs.", "technological": "Transitioning legacy copper landlines to fiber-to-the-home (FTTH) and IP-based voice exchange infrastructure.", "legal": "DoT licensing, public sector disinvestment guidelines, and sovereign communications protocols.", "environmental": "Safe recycling of decommissioned copper cabling and reduction of legacy power-hungry electromechanical exchanges."},
        [0.20, 0.55, 0.35, 0.30, 0.65],
        {"threat_of_new_entrants": "Zero in fixed-line city underground ducts due to municipal digging bans in congested metros.", "bargaining_power_of_buyers": "High; private subscribers switch to JioFiber and Airtel, while government departments remain captive.", "bargaining_power_of_suppliers": "Low; standard telecom equipment suppliers.", "threat_of_substitutes": "Very high from mobile phones and private fiber broadband providers.", "competitive_rivalry": "High in broadband; low in specialized sovereign government landlines."}
    ),
    (
        "Bharat Sanchar Nigam Limited (BSNL)", "Telecom, Fiber & Communications Infrastructure",
        "rural populations, border defense outposts, and citizens in remote tier-3/4 districts across India",
        "need dependable mobile, fiber, and emergency telecommunications in geographically challenging terrain where private telcos do not operate",
        "BSNL 4G/5G Indigenous Network & Bharat AirFibre", "Sovereign Rural & Strategic Telecommunications Network",
        "serves as the strategic telecom backbone of India, connecting remote Himalayan borders, Andaman islands, and 600,000 villages with 100% indigenous 4G/5G tech",
        [0.88, 0.82, 0.95, 0.88, 0.86, 0.70],
        {"political": "Backed by multi-lakh-crore sovereign revival packages from the Union Cabinet; critical instrument of national security and emergency relief.", "economic": "Turnaround driven by indigenous 4G deployment and rapid expansion of Bharat Fiber broadband across semi-urban and rural homes.", "social": "The ultimate national lifeline during natural disasters (floods, cyclones), maintaining communications when commercial towers collapse.", "technological": "Deploying 100,000 completely indigenous 4G/5G telecom sites engineered by TCS and C-DoT, achieving sovereign technology independence.", "legal": "Universal Service Obligation Fund (USOF) mandates, DoT governance, and strategic defense spectrum reservations.", "environmental": "Deploying solar-powered telecom towers across ecologically fragile Himalayan regions and coastal zones."},
        [0.12, 0.50, 0.30, 0.22, 0.60],
        {"threat_of_new_entrants": "Zero; sovereign national carrier status.", "bargaining_power_of_buyers": "Moderate; rural consumers appreciate affordable plans, but demand reliable network uptime.", "bargaining_power_of_suppliers": "Low; government procurement rules and indigenous vendor consortia (TCS/Tejas).", "threat_of_substitutes": "Moderate from private mobile networks in urban areas.", "competitive_rivalry": "Moderate; operates in rural and strategic regions where private telcos often have minimal presence."}
    ),
    (
        "Netweb Technologies India", "Telecom, Fiber & Communications Infrastructure",
        "enterprises, telecom operators, research institutes, and AI cloud builders across India",
        "require sovereign, high-performance computing (HPC) supercomputing servers, 5G cloud orchestration, and AI inference workstations",
        "Tyrone High-Performance Servers & 5G Open-RAN Cloud Infrastructure", "High-Performance Computing & 5G Cloud Edge Infrastructure",
        "built India's top supercomputers (PARAM Yuva II, Airawat AI) and manufactures indigenously engineered 5G ORAN servers under the Make in India initiative",
        [0.80, 0.86, 0.90, 0.96, 0.85, 0.68],
        {"political": "Pinnacle recipient of IT Hardware PLI 2.0 and Telecom PLI; critical partner in the National Supercomputing Mission (NSM).", "economic": "Rapid margin expansion driven by massive enterprise and telecom demand for AI computing clusters and private 5G edge clouds.", "social": "Empowers Indian universities, weather forecasting centers, and defense scientists with sovereign computational power.", "technological": "Proprietary server architecture, liquid immersion cooling systems, and specialized 5G virtualized distributed units (vDU).", "legal": "Compliance with trusted electronic hardware mandates and BIS safety certifications.", "environmental": "Pioneered direct-to-chip liquid cooling systems cutting data center server energy consumption by over 30%."},
        [0.22, 0.48, 0.45, 0.22, 0.60],
        {"threat_of_new_entrants": "Low; HPC server design requires deep thermal engineering, multi-layer motherboard routing, and semiconductor partnership status (NVIDIA, Intel).", "bargaining_power_of_buyers": "Moderate; enterprise clients evaluate performance-per-watt benchmarks.", "bargaining_power_of_suppliers": "High; dependent on leading-edge global silicon vendors (NVIDIA GPUs, AMD/Intel CPUs).", "threat_of_substitutes": "Moderate from multinational server OEMs (Dell, HP).", "competitive_rivalry": "Moderate; dominates domestic specialized sovereign supercomputing deployments."}
    ),
    (
        "GTL Infrastructure", "Telecom, Fiber & Communications Infrastructure",
        "telecom service providers requiring passive tower space across secondary and rural telecom circles",
        "need shared telecom tower hosting in semi-urban and rural locations without bearing dedicated infrastructure maintenance overheads",
        "Shared Rural & Semi-Urban Telecom Towers", "Independent Shared Passive Tower Infrastructure",
        "operates over 26,000 independent telecom towers across India, facilitating mobile connectivity across remote and tier-2/3 telecom circles",
        [0.72, 0.75, 0.90, 0.82, 0.82, 0.68],
        {"political": "Complies with Department of Telecommunications infrastructure provider guidelines and local municipal zoning norms.", "economic": "Operates as a pure-play independent tower company, focusing on restructuring debt and improving tenancy ratios.", "social": "Provides essential physical wireless infrastructure that connects small towns and rural agricultural communities.", "technological": "Remote monitoring systems for tower battery backup, automated energy meters, and security telemetry.", "legal": "DoT licensing compliance, municipal property tax dispute resolutions, and insolvency debt resolution processes.", "environmental": "Adopting solar hybrid power units to curb diesel generator usage at remote rural tower sites."},
        [0.25, 0.68, 0.38, 0.20, 0.65],
        {"threat_of_new_entrants": "Low; building tens of thousands of rural telecom towers is capital prohibitive.", "bargaining_power_of_buyers": "High; reliant on a handful of mobile telco tenants who demand competitive rental rates.", "bargaining_power_of_suppliers": "Moderate; steel fabricators, battery manufacturers, and fuel distributors.", "threat_of_substitutes": "Low; towers are indispensable for cellular wireless propagation.", "competitive_rivalry": "High; faces immense competition from well-capitalized industry giant Indus Towers."}
    ),
    (
        "ITI Limited", "Telecom, Fiber & Communications Infrastructure",
        "Indian defense forces, sovereign intelligence agencies, and public sector telecommunications",
        "require ultra-secure, encrypted defense communication systems, optical transmission equipment, and sovereign smart electronic manufacturing",
        "ASCON Defense Network & Encrypted Tactical Communications", "Sovereign Defense Electronics & Telecom Manufacturing",
        "stands as India's first public sector undertaking, securing military communications with the Army Static Switched Communication Network (ASCON)",
        [0.85, 0.82, 0.90, 0.92, 0.88, 0.70],
        {"political": "Strategic defense manufacturer under Ministry of Communications; executes mission-critical defense and homeland security communications.", "economic": "Revitalized by multi-thousand-crore defense contracts (ASCON Phase IV) and national BharatNet fiber rollout orders.", "social": "Safeguards national borders and defense forces from cyber warfare, foreign eavesdropping, and electronic interception.", "technological": "Indigenous cryptographic hardware, secure IP encryption devices, 3D printing labs, and high-density PCB manufacturing in Bengaluru and Mankapur.", "legal": "Highest-level military secrecy clearances, defense quality assurance (DGQA) approvals, and public procurement rules.", "environmental": "Zero-discharge effluent treatment for electroplating and printed circuit board etching chemicals."},
        [0.15, 0.40, 0.35, 0.18, 0.50],
        {"threat_of_new_entrants": "Low to non-existent; military communication requires sovereign security clearances that private entrants cannot access.", "bargaining_power_of_buyers": "High; Ministry of Defence dictates strict technical milestones and contractual terms.", "bargaining_power_of_suppliers": "Moderate; specialized electronic components and ruggedized military connectors.", "threat_of_substitutes": "Low; commercial civilian telecom gear cannot be substituted for classified military tactical networks.", "competitive_rivalry": "Low to moderate; collaborates closely with Bharat Electronics (BEL) and DRDO."}
    ),
    (
        "Nelco Limited", "Telecom, Fiber & Communications Infrastructure",
        "maritime vessels, commercial airlines, offshore oil rigs, and remote enterprise ATMs",
        "need high-speed satellite broadband connectivity in deep oceans, high altitudes, and remote geographical terrains with zero cellular coverage",
        "Nelco Satcom & In-Flight / Maritime Aero Connectivity", "Satellite Telecommunication & VSAT Enterprise Solutions",
        "leads India's commercial VSAT and satellite communication market with Tata backing, pioneering in-flight Wi-Fi for domestic flights and maritime tracking",
        [0.82, 0.86, 0.90, 0.95, 0.88, 0.72],
        {"political": "Direct beneficiary of Indian Space Policy 2023, IN-SPACe clearances, and opening of satellite broadband communication to private enterprise.", "economic": "High-margin B2B recurring subscription revenues from maritime shipping fleets, aviation airlines, and offshore oil platforms.", "social": "Brings internet access to air travelers mid-flight and mariners isolated for months in international waters.", "technological": "Advanced GEO/MEO satellite transponder management, high-throughput satellite (HTS) spot beams, and Ku-band tracking antennae.", "legal": "Department of Telecommunications VSAT licenses, Directorate General of Civil Aviation (DGCA) aero connectivity clearances.", "environmental": "Low physical terrestrial impact; satellite communications require zero land disturbance or cross-country trenching."},
        [0.22, 0.48, 0.45, 0.22, 0.55],
        {"threat_of_new_entrants": "Low; operating commercial satellite earth stations and securing regulatory satellite spectrum clearances has high hurdles.", "bargaining_power_of_buyers": "Moderate; maritime and aviation clients demand tight latency and reliability SLAs.", "bargaining_power_of_suppliers": "High; satellite capacity leased from ISRO/NSIL and global satellite fleet operators (Eutelsat OneWeb, Intelsat).", "threat_of_substitutes": "Moderate from emerging low-earth-orbit (LEO) constellations (Starlink, OneWeb).", "competitive_rivalry": "Moderate; primary domestic competitors are Hughes Communications India and BSNL Satcom."}
    ),
    (
        "Optiemus Infracom", "Telecom, Fiber & Communications Infrastructure",
        "global smartphone brands, telecom hardware companies, and hearable/wearable lifestyle brands",
        "need high-precision electronics manufacturing services (EMS), local assembly, and rapid scaling of mobile devices and telecom hardware in India",
        "Electronics Manufacturing Services (EMS) & Drone Hardware Assembly", "Contract Electronics & Telecom Hardware Manufacturing",
        "operates massive automated SMT electronics plants in Noida, assembling millions of mobile devices, wireless hearables, and agricultural drones",
        [0.78, 0.85, 0.88, 0.92, 0.84, 0.68],
        {"political": "Major beneficiary of Electronics PLI, IT Hardware PLI, and drone manufacturing subsidies under Make in India.", "economic": "Rapid revenue ramp-up through high-volume contract manufacturing partnerships with domestic leaders (Noise) and global tech brands.", "social": "Creates thousands of skilled manufacturing and assembly jobs for Indian women and youth in northern industrial corridors.", "technological": "High-speed Surface Mount Technology (SMT) lines, automated optical inspection, and cleanroom electronic cleanrooms.", "legal": "BIS electronics certification, factory safety labor compliance, and customs duty bonding regulations.", "environmental": "Lead-free soldering processes, ISO 14001 environmental management, and certified e-waste recycling partnerships."},
        [0.28, 0.60, 0.42, 0.25, 0.70],
        {"threat_of_new_entrants": "Moderate; setting up basic assembly is possible, but scaling advanced high-speed SMT lines requires tens of crores in capex.", "bargaining_power_of_buyers": "High; electronics brands negotiate tight assembly margins per device.", "bargaining_power_of_suppliers": "Moderate; reliant on component vendors for passive electronics and semiconductor chips.", "threat_of_substitutes": "Moderate from other domestic EMS giants (Dixon, Foxconn India).", "competitive_rivalry": "Intense rivalry with Dixon Technologies and Bhagwati Products."}
    ),
    (
        "Polycab Telecom", "Telecom, Fiber & Communications Infrastructure",
        "state governments, telecom operators, and smart city infrastructure authorities",
        "require turnkey engineering, procurement, and construction (EPC) for optical fiber rollouts, city surveillance networks, and rural broadband",
        "BharatNet Rural Optical EPC & Smart City Telecom Infrastructure", "Turnkey Telecom EPC & Optical Network Rollout",
        "delivers end-to-end turnkey optical fiber network rollout, having laid tens of thousands of kilometers of duct and fiber under BharatNet and smart cities",
        [0.78, 0.88, 0.92, 0.90, 0.84, 0.72],
        {"political": "Major implementation partner for BharatNet, National Optical Fibre Network (NOFN), and state smart city missions.", "economic": "Synergized with Polycab India's massive optical fiber and power cable manufacturing scale, giving unbeatable supply chain cost control.", "social": "Brings high-speed fiber broadband to remote gram panchayats, enabling telemedicine, digital schooling, and rural e-governance.", "technological": "Horizontal directional drilling (HDD), automated cable blowing machines, and fusion splicing with OTDR optical loss testing.", "legal": "Municipal Right-of-Way clearances, environmental safety protocols, and government tender contracting norms.", "environmental": "Trenchless directional drilling minimizes surface soil excavation and prevents road damage during optical fiber laying."},
        [0.26, 0.55, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; executing complex civil fiber EPC across multiple states requires massive project bonding and machinery.", "bargaining_power_of_buyers": "Moderate; government tenders award contracts to lowest qualified L1 bidders.", "bargaining_power_of_suppliers": "Low; backward-integrated into Polycab's captive optical fiber manufacturing.", "threat_of_substitutes": "Low; physical underground fiber is the mandatory backbone for modern communications.", "competitive_rivalry": "High with Sterlite Technologies, HFCL, and L&T Construction."}
    ),
    (
        "Route Mobile", "Telecom, Fiber & Communications Infrastructure",
        "enterprises, fintechs, banks, and e-commerce platforms worldwide",
        "need cloud communications platform (CPaaS), automated one-time password (OTP) delivery, two-factor authentication, and WhatsApp conversational commerce",
        "Route Mobile Cloud Communications Platform & Omnichannel Messaging", "Cloud Communication Platform as a Service (CPaaS)",
        "powers billions of mission-critical bank OTPs and enterprise messages monthly, connecting enterprises to 900+ mobile network operators globally",
        [0.72, 0.88, 0.94, 0.95, 0.84, 0.68],
        {"political": "Compliant with TRAI distributed ledger technology (DLT) anti-spam regulations and international telecommunications standards.", "economic": "Acquired by European telecom major Proximus Group; generates strong global cash flows from high-margin messaging APIs and conversational AI.", "social": "Secures daily financial transactions for millions of Indians, delivering time-critical OTPs for banking, credit cards, and e-commerce.", "technological": "Proprietary high-throughput SMS firewalls, WhatsApp Business API integrations, RCS messaging, and voice bots.", "legal": "TRAI DLT anti-phishing mandates, DPDP Act data privacy, and global GDPR telecommunication rules.", "environmental": "Pure-play cloud software infrastructure running on energy-efficient data center cloud platforms."},
        [0.28, 0.54, 0.40, 0.25, 0.70],
        {"threat_of_new_entrants": "Moderate; software APIs are easy to write, but direct operator interconnect agreements with 900+ global telcos form a heavy moat.", "bargaining_power_of_buyers": "Moderate to high; enterprise banks negotiate volume pricing per SMS/OTP across CPaaS providers.", "bargaining_power_of_suppliers": "High; mobile network operators (Jio, Airtel) hold statutory pricing power over termination interconnect tariffs.", "threat_of_substitutes": "Moderate from app-based push notifications and email authentication.", "competitive_rivalry": "Fierce rivalry with Tanla Platforms and Sinch India."}
    )
]

for item in sector13_data:
    add_c(*item)

print(f"Sector 13 added: {len(sector13_data)} companies. Total: {len(part3_a)}")

# ==============================================================================
# SECTOR 14: Power, Renewables & Clean Energy (22 companies)
# ==============================================================================
sector14_data = [
    (
        "Tata Power", "Power, Renewables & Clean Energy",
        "industrial, commercial, and residential energy consumers across India",
        "need clean, reliable, round-the-clock electricity, rooftop solar installations, and nationwide electric vehicle charging infrastructure",
        "Tata Power Renewable Energy & EZ Charge EV Network", "Integrated Clean Energy, Rooftop Solar & EV Charging",
        "leads India's green energy transition, operating over 5,500 clean MW, India's #1 rooftop solar EPC brand, and the largest pan-India EV charging network",
        [0.82, 0.92, 0.96, 0.95, 0.88, 0.90],
        {"political": "Aligned with Prime Minister's PM Surya Ghar: Muft Bijli Yojana (1 crore solar homes) and national Net Zero 2070 roadmap.", "economic": "Robust integrated cash flows from generation, transmission, distribution (Odisha/Delhi/Mumbai), and fast-growing renewable EPC.", "social": "Empowering millions of Indian homeowners and farmers with decentralized rooftop solar and solar agriculture irrigation pumps.", "technological": "State-of-the-art 4.3 GW cell and module manufacturing plant in Tirunelveli, automated micro-grids, and digital EV smart-charging platforms.", "legal": "Central Electricity Regulatory Commission (CERC) tariff regulations, State Electricity Regulatory Commissions (SERCs), and power purchase agreements.", "environmental": "Committed to 100% coal-free phaseout and 100% clean power generation by 2045; water-neutral thermal operations."},
        [0.18, 0.45, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; building an integrated utility with distribution licenses, transmission grids, and gigawatt solar plants requires billions in capital.", "bargaining_power_of_buyers": "Moderate; industrial buyers negotiate open-access power, but retail power distribution tariffs are regulated by state commissions.", "bargaining_power_of_suppliers": "Moderate; solar wafer suppliers, wind turbine OEMs, and transmission hardware vendors.", "threat_of_substitutes": "Low; electricity is the non-negotiable lifeblood of modern economic society.", "competitive_rivalry": "Moderate; competes with Adani Power, JSW Energy, and NTPC in generation auctions."}
    ),
    (
        "NTPC Limited", "Power, Renewables & Clean Energy",
        "state electricity distribution companies (DISCOMs) and heavy industrial power grids",
        "require massive, reliable, baseload thermal and renewable electrical power to prevent grid blackouts across India",
        "NTPC Thermal Power Stations & NTPC Green Energy (NGEL)", "Baseload Power Generation & Utility-Scale Clean Energy",
        "stands as India's largest power producer (74+ GW capacity), generating 25% of India's electricity and developing 60 GW of renewable energy by 2032",
        [0.88, 0.95, 0.98, 0.92, 0.88, 0.80],
        {"political": "Maharatna sovereign power giant under Ministry of Power; the bedrock guarantor of national energy security and grid stability.", "economic": "Guaranteed regulated return on equity (15.5%) under CERC cost-plus frameworks, delivering massive dividend yields and steady operating profits.", "social": "Powers the economic development of every Indian state, providing uninterrupted electricity to factories, hospitals, and homes.", "technological": "Supercritical and ultra-supercritical coal boilers, green hydrogen microgrids in Ladakh, and floating solar photovoltaic power stations.", "legal": "Long-term 25-year Power Purchase Agreements (PPAs) backed by tripartite payment security mechanisms with state governments and RBI.", "environmental": "Aggressively blending green hydrogen, co-firing biomass pellets in coal boilers to reduce stubble burning, and massive afforestation drives."},
        [0.12, 0.35, 0.25, 0.18, 0.50],
        {"threat_of_new_entrants": "Practically impossible; building multi-gigawatt thermal and hydro stations requires sovereign land acquisition and coal linkages.", "bargaining_power_of_buyers": "Low; state DISCOMs rely completely on NTPC for non-intermittent baseload electricity to avoid grid failure.", "bargaining_power_of_suppliers": "Low; captive coal mines and long-term priority coal supply agreements with Coal India.", "threat_of_substitutes": "Low; renewable energy needs NTPC's thermal balancing power to maintain 50 Hz grid frequency stability.", "competitive_rivalry": "Low; operates in a category of its own as the apex national power utility."}
    ),
    (
        "Adani Green Energy", "Power, Renewables & Clean Energy",
        "national grid operators, sovereign power off-takers (SECI), and commercial energy off-takers",
        "need massive, utility-scale solar, wind, and hybrid renewable energy projects delivered at the lowest levelized cost of energy (LCOE)",
        "Khavda Renewable Energy Mega-Park & Hybrid Wind-Solar Plants", "Utility-Scale Renewable Independent Power Producer (IPP)",
        "is building the world's largest renewable energy plant at Khavda (30 GW across 538 sq km), targeting 45 GW of total renewable capacity by 2030",
        [0.85, 0.94, 0.96, 0.95, 0.86, 0.92],
        {"political": "Strong alignment with national target of 500 GW non-fossil capacity by 2030; backed by long-term central sovereign off-taker contracts (SECI).", "economic": "Secured billions of dollars in international green bond and construction financing from global consortiums (TotalEnergies, international banks).", "social": "Transforms barren desert wastelands in Kutch and Rajasthan into green energy powerhouses providing regional technical employment.", "technological": "Advanced bifacial solar modules, single-axis solar trackers, robotic waterless panel cleaning, and high-altitude 5.2 MW wind turbines.", "legal": "25-year sovereign-backed PPAs with SECI, NTPC, and state utilities with strict contractual payment guarantees.", "environmental": "Generates 100% clean, zero-emission electricity; waterless robotic cleaning conserves millions of liters of scarce desert groundwater."},
        [0.18, 0.40, 0.35, 0.20, 0.65],
        {"threat_of_new_entrants": "Low; securing contiguous 500-square-kilometer land parcels and multi-gigawatt grid transmission connectivity is a massive barrier.", "bargaining_power_of_buyers": "Low to moderate; sovereign off-taker (SECI) has long-term 25-year locked tariffs.", "bargaining_power_of_suppliers": "Low to moderate; sister company Adani Solar supplies in-house solar cells and modules.", "threat_of_substitutes": "Low; clean renewable energy is the globally mandated future of power generation.", "competitive_rivalry": "Moderate; competes with Tata Power, ReNew, and NTPC Green in SECI mega-auctions."}
    ),
    (
        "Suzlon Energy", "Power, Renewables & Clean Energy",
        "independent power producers (IPPs), captive industrial power consumers, and state power utilities",
        "need high-efficiency wind turbine generators engineered specifically for India's low-wind regimes, backed by lifetime operations and maintenance",
        "Suzlon S144 3.X MW Wind Turbine Series & End-to-End Wind EPC", "Wind Turbine Generator (WTG) Manufacturing & Wind Farm EPC",
        "pioneered the Indian wind energy industry with over 20 GW of global installed capacity, commanding 32% domestic market share with indigenous 3.X MW turbines",
        [0.80, 0.90, 0.95, 0.94, 0.86, 0.92],
        {"political": "Prime beneficiary of Ministry of New and Renewable Energy (MNRE) wind bidding guidelines and Revised List of Models and Manufacturers (RLMM).", "economic": "Successfully turned net debt-free with massive order book (>3.8 GW), generating high-margin recurring cash flows from long-term O&M contracts.", "social": "Brings sustainable rural economic development, royalty rental incomes to rural farmers hosting wind turbines on their land.", "technological": "Proprietary S144 3.X MW turbine featuring a 160m hub height and carbon-fiber rotor blades that capture low-speed winds with 43%+ PLF.", "legal": "Strict adherence to MNRE quality guidelines, grid code connectivity compliance, and environmental clearances.", "environmental": "Wind power produces zero operational carbon emissions and uses zero water during power generation."},
        [0.22, 0.48, 0.42, 0.22, 0.60],
        {"threat_of_new_entrants": "Low; aerodynamic blade mold tooling, multi-megawatt nacelle testing, and 25-year wind resource micro-siting data create an unyielding barrier.", "bargaining_power_of_buyers": "Moderate; IPP clients (ReNew, Torrent, Adani) evaluate levelized cost of energy (LCOE) per kilowatt-hour.", "bargaining_power_of_suppliers": "Moderate; steel towers, specialized gearboxes, and permanent magnet generators.", "threat_of_substitutes": "Moderate from solar energy, but wind energy is essential for evening peak power when solar ceases generation.", "competitive_rivalry": "Moderate; primary domestic competitors are Inox Wind and Envision Energy."}
    ),
    (
        "ReNew Energy Global", "Power, Renewables & Clean Energy",
        "commercial and industrial (C&I) corporations and state distribution utilities",
        "need customized, round-the-clock (RTC) green power combining solar, wind, and battery storage to achieve 100% corporate renewable energy targets",
        "Utility-Scale Wind, Solar & Round-The-Clock (RTC) Green Power", "Utility-Scale Renewable IPP & Decarbonization Solutions",
        "operates over 10 GW of diversified wind and solar assets, pioneering India's first utility-scale Round-the-Clock (RTC) renewable energy projects",
        [0.80, 0.90, 0.96, 0.94, 0.86, 0.92],
        {"political": "Supports National Green Hydrogen Mission and corporate decarbonization mandates under India's climate commitments.", "economic": "Listed on NASDAQ; strong access to global climate finance and institutional debt for utility-scale project execution.", "social": "ReNew India Foundation drives women empowerment, solar-powered community water kiosks, and rural digital education.", "technological": "Proprietary AI-driven ReNew Power Digital Labs for predictive turbine maintenance, drone-based solar thermography, and RTC algorithmic dispatch.", "legal": "Long-term PPAs with state utilities and corporate C&I clients, complying with open-access green power regulations.", "environmental": "Avoids tens of millions of tons of CO2 emissions annually; committed to Net Zero operational emissions by 2040."},
        [0.20, 0.45, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; requires multi-gigawatt project execution track record, power grid connectivity, and international capital relationships.", "bargaining_power_of_buyers": "Moderate; commercial & industrial clients sign 15-25 year open-access contracts at fixed tariffs to hedge power costs.", "bargaining_power_of_suppliers": "Moderate; global wind turbine and solar module manufacturers.", "threat_of_substitutes": "Low; green power is legally mandated for corporate ESG compliance.", "competitive_rivalry": "Moderate to high with Tata Power, Adani Green, and JSW Energy."}
    ),
    (
        "Power Grid Corporation of India (POWERGRID)", "Power, Renewables & Clean Energy",
        "all power generation plants, state distribution utilities, and regional electrical grids across India",
        "require ultra-reliable, high-capacity interstate transmission lines to evacuate electricity from remote renewable zones without transmission congestion",
        "Inter-State Transmission System (ISTS) & Green Energy Corridors", "Monopoly Inter-State Electricity Transmission Utility",
        "operates as India's central transmission utility, transmitting over 85% of India's interstate power across 178,000 circuit km of high-voltage transmission lines",
        [0.88, 0.96, 0.98, 0.94, 0.88, 0.85],
        {"political": "Maharatna sovereign utility; implements the Green Energy Corridors and 'One Sun, One World, One Grid' cross-border interconnections.", "economic": "Guaranteed 15.5% regulated return on equity under CERC tariff norms; unmatched financial strength with near-zero payment default risk.", "social": "The physical backbone of national integration, ensuring surplus solar power from Rajasthan lights homes in Kerala and Assam.", "technological": "Pioneered +/-800 kV Ultra High Voltage Direct Current (UHVDC) transmission lines and automated substations with digital optical monitoring.", "legal": "Regulated by Central Electricity Regulatory Commission; statutory right of way and designated central transmission agency.", "environmental": "Compact GIS (Gas Insulated Substation) technology reducing land footprint by 70%; wildlife deflector devices on transmission lines."},
        [0.08, 0.25, 0.25, 0.15, 0.35],
        {"threat_of_new_entrants": "Practically zero; massive network effect and national strategic transmission monopoly.", "bargaining_power_of_buyers": "Low; generation companies and state utilities are legally mandated to pay ISTS wheeling tariffs under national point-of-connection pools.", "bargaining_power_of_suppliers": "Low; standardized procurement of transmission towers, conductors, and power transformers (BHEL, Siemens).", "threat_of_substitutes": "Zero; physical high-voltage transmission lines have no physical substitute.", "competitive_rivalry": "Low; private transmission bidding (TBCB) accounts for a minor fraction of the market where Adani Energy Solutions competes."}
    ),
    (
        "JSW Energy", "Power, Renewables & Clean Energy",
        "national electricity grids, industrial manufacturers, and state utilities",
        "demand reliable dispatchable clean power, large-scale pumped hydro storage, and competitive thermal-renewable hybrid generation",
        "Pumped Hydro Energy Storage & Hybrid Renewable Capacity", "Diversified Power Utility & Pumped Hydro Storage Pioneer",
        "is transforming rapidly into a pure-play green energy leader, locking in 3.4 GWh of pumped storage capacity and expanding toward 20 GW of total capacity",
        [0.80, 0.92, 0.95, 0.94, 0.86, 0.88],
        {"political": "Key beneficiary of Ministry of Power's comprehensive Pumped Storage Projects (PSP) guidelines and energy storage obligations.", "economic": "Strong balance sheet backed by the JSW Group; high operating cash generation from efficient coastal imported coal plants and hydro assets.", "social": "Provides clean grid balancing power that prevents catastrophic blackouts during periods of zero solar/wind generation.", "technological": "Large-scale closed-loop pumped hydroelectric storage turbines, automated hydro reservoir management, and high-efficiency wind farms.", "legal": "Long-term PPAs with state utilities and compliance with Central Electricity Authority (CEA) storage safety standards.", "environmental": "Hydro storage uses zero fossil fuels, producing circular, closed-loop mechanical battery storage with 50+ year asset lifespans."},
        [0.20, 0.45, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; developing pumped hydro storage requires unique topographic reservoirs, geological surveys, and environmental clearances.", "bargaining_power_of_buyers": "Moderate; grid off-takers willingly pay a premium for dispatchable evening peaking power.", "bargaining_power_of_suppliers": "Moderate; specialized hydro turbine suppliers (Voith, Andritz) and civil contractors.", "threat_of_substitutes": "Moderate from chemical lithium-ion battery storage (BESS), but pumped hydro has far lower levelized cost of storage.", "competitive_rivalry": "Moderate; competes with Tata Power, Torrent Power, and NTPC."}
    ),
    (
        "Torrent Power", "Power, Renewables & Clean Energy",
        "industrial estates, commercial enterprises, and urban households in Gujarat, Maharashtra, and UP",
        "need uninterrupted 24/7 power supply with zero voltage fluctuations, fair billing, and rapid customer service resolutions",
        "Urban Power Distribution Franchises & Renewable Generation", "Integrated Private Power Generation & Benchmark Distribution Utility",
        "leads the Indian power sector in operational efficiency, boasting world-class Aggregate Technical & Commercial (AT&C) losses of under 4% in Ahmedabad and Surat",
        [0.80, 0.92, 0.95, 0.92, 0.86, 0.85],
        {"political": "Benchmark private utility frequently cited by Ministry of Power as the model for state DISCOM privatization reforms.", "economic": "Consistent, high-margin cash generation from licensed distribution monopolies in prosperous industrial cities (Ahmedabad, Surat, Dahej).", "social": "Ensures zero power cuts for millions of businesses, diamond cutting factories, and homes, transforming regional industrial productivity.", "technological": "Underground smart cabling, automated ring main units (RMU), smart digital meters, and automated outage restoration systems.", "legal": "Regulated by Gujarat Electricity Regulatory Commission (GERC) and CERC; licensed distribution franchisee agreements.", "environmental": "Aggressively expanding solar and wind generation, phasing out old thermal units, and piloting green hydrogen gas blending in city gas."},
        [0.18, 0.40, 0.35, 0.20, 0.55],
        {"threat_of_new_entrants": "Zero in licensed distribution cities; distribution licenses grant statutory local geographical monopolies.", "bargaining_power_of_buyers": "Low; consumers within licensed areas cannot switch electricity suppliers.", "bargaining_power_of_suppliers": "Moderate; regasified LNG suppliers for gas-fired power plants, and transmission service providers.", "threat_of_substitutes": "Low; commercial open access is restricted by cross-subsidy surcharges.", "competitive_rivalry": "Low in core distribution cities; moderate in competitive renewable project bidding."}
    ),
    (
        "SJVN Limited", "Power, Renewables & Clean Energy",
        "northern Indian regional electricity boards and Himalayan state utilities",
        "require clean, low-cost hydroelectric power and mountain river run-of-the-river energy generation",
        "Nathpa Jhakri Hydro Power Station & Himalayan Clean Energy", "Hydroelectric & Multi-State Clean Power Development",
        "operates Nathpa Jhakri (1,500 MW)—India's largest underground hydroelectric power station—generating low-cost clean power across the Himalayas",
        [0.84, 0.90, 0.95, 0.90, 0.88, 0.85],
        {"political": "Joint venture between Government of India and Government of Himachal Pradesh; critical developer for Himalayan hydro potential.", "economic": "Extremely low variable generation cost (<Rs 2 per unit) from amortized hydro assets provides stellar EBITDA margins (>70%).", "social": "Provides free power allocations to home states, financing local Himalayan road infrastructure, schools, and hospitals.", "technological": "Deep underground desilting chambers, deep mountain headrace tunnels, and high-head Francis turbines engineered for silt-laden glacial rivers.", "legal": "CERC hydro tariff regulations, trans-boundary river water agreements, and strict environmental impact assessments.", "environmental": "Run-of-the-river hydro generation creates minimal reservoir submergence while producing 100% clean, non-polluting energy."},
        [0.15, 0.35, 0.28, 0.18, 0.45],
        {"threat_of_new_entrants": "Very low; developing Himalayan hydro requires decades of geological tunneling expertise and inter-governmental accords.", "bargaining_power_of_buyers": "Low; northern states depend heavily on SJVN's low-cost peaking hydro power during summer demand spikes.", "bargaining_power_of_suppliers": "Moderate; heavy civil contractors and hydro mechanical equipment manufacturers (BHEL).", "threat_of_substitutes": "Low; hydroelectric power provides critical black-start and grid-frequency stability.", "competitive_rivalry": "Low; collaborates with NHPC under Ministry of Power coordination."}
    ),
    (
        "NHPC Limited", "Power, Renewables & Clean Energy",
        "national electricity grid and state utilities across Jammu & Kashmir, Himachal Pradesh, Sikkim, and the Northeast",
        "need large-scale hydroelectric power generation and pumped storage in complex mountain terrains to balance intermittent renewable energy",
        "Himalayan Hydroelectric Stations & Subansiri Lower Hydro Project", "Apex Sovereign Hydroelectric Power Corporation",
        "stands as India's premier hydroelectric utility with over 7,000 MW operational, mastering complex geological tunneling in the young Himalayas",
        [0.86, 0.92, 0.96, 0.92, 0.88, 0.85],
        {"political": "Mini-Ratna Schedule-A public enterprise; apex agency for developing strategic hydropower near border river systems.", "economic": "Steady regulated cash generation and handsome dividend payouts; massive capital expenditure deployment into mega hydro assets.", "social": "Drives socio-economic development, bridge building, and disaster management across remote border districts of J&K and Arunachal Pradesh.", "technological": "Advanced seismic-resistant dam engineering, micro-tunneling under glacial moraines, and high-altitude heavy construction logistics.", "legal": "Indus Waters Treaty compliance, CERC statutory regulations, and National Green Tribunal (NGT) environmental clearances.", "environmental": "Implements extensive catchment area treatment plans, fish ladders for aquatic wildlife, and compensatory afforestation."},
        [0.12, 0.32, 0.25, 0.15, 0.40],
        {"threat_of_new_entrants": "Practically impossible; extreme geological risks and sovereign river basin allocations exclude private new entrants.", "bargaining_power_of_buyers": "Low; state utilities eagerly purchase NHPC's dispatchable hydro power.", "bargaining_power_of_suppliers": "Moderate; civil tunneling consortiums (L&T, Patel Engineering) and turbine OEMs.", "threat_of_substitutes": "Low; hydro power is the primary mechanical grid stabilizer.", "competitive_rivalry": "Low; undisputed sovereign leader in Indian hydroelectricity."}
    ),
    (
        "Sterling and Wilson Renewable Energy", "Power, Renewables & Clean Energy",
        "global utility-scale solar developers, sovereign wealth funds, and clean energy conglomerates across 29 countries",
        "require turnkey engineering, procurement, and construction (EPC) for multi-gigawatt solar PV and hybrid storage installations",
        "Turnkey Utility-Scale Solar EPC & Energy Storage Solutions", "Global Turnkey Utility-Scale Solar EPC Contractor",
        "has delivered over 15 GW of utility-scale solar projects across 29 countries, executing some of the world's largest single-site solar power plants",
        [0.78, 0.90, 0.94, 0.92, 0.85, 0.90],
        {"political": "Backed by Reliance Industries as a strategic clean energy partner for global and domestic gigawatt EPC rollouts.", "economic": "Turnaround driven by massive order pipeline across India, Middle East, and Australia; asset-light engineering model with zero manufacturing asset burden.", "social": "Employs tens of thousands of local technicians and workers across construction sites in desert and rural terrains.", "technological": "Algorithmic layout design optimizing solar yield, high-speed automated tracker installation, and 33/400 kV high-voltage substation integration.", "legal": "International FIDIC engineering contracts, performance-ratio guarantees, and local labor regulations across global jurisdictions.", "environmental": "Enables the world's transition to gigawatt-scale zero-emission solar energy; minimizes soil erosion through pile-driven mounting structures."},
        [0.25, 0.52, 0.40, 0.22, 0.68],
        {"threat_of_new_entrants": "Low to moderate; executing 1,000+ MW solar projects requires international bank guarantees and deep balance sheet backing.", "bargaining_power_of_buyers": "Moderate; global solar developers negotiate competitive EPC margins per watt.", "bargaining_power_of_suppliers": "Moderate; tier-1 solar module makers and inverter OEMs.", "threat_of_substitutes": "Low; solar developers rely on specialized EPC contractors for balance of plant.", "competitive_rivalry": "High in domestic auctions with Tata Power Solar and L&T; moderate globally."}
    ),
    (
        "Borosil Renewables", "Power, Renewables & Clean Energy",
        "solar photovoltaic module manufacturers across India, Europe, and the Americas",
        "need high-transmittance, ultra-low iron textured tempered solar glass that maximizes solar panel electrical efficiency and withstands hailstorms",
        "Selene Low-Iron Textured Solar Tempered Glass", "Low-Iron Solar Photovoltaic Tempered Glass",
        "stands as India's pioneer and dominant manufacturer of low-iron solar glass, engineering anti-reflective coated glass that boosts panel energy output by over 3%",
        [0.82, 0.88, 0.92, 0.94, 0.86, 0.88],
        {"political": "Major beneficiary of anti-dumping duties and countervailing duties imposed on subsidized Chinese and Vietnamese solar glass imports.", "economic": "Rapid capacity expansion in Bharuch, Gujarat; strong export demand from European solar module makers seeking non-Chinese supply chains.", "social": "Creates high-tech manufacturing employment and secures domestic supply chains for India's solar module revolution.", "technological": "Patented anti-reflective coating technology, specialized low-iron glass melting furnaces, and ultra-thin (2mm) glass for bifacial modules.", "legal": "Directorate General of Trade Remedies (DGTR) trade filings, BIS glass safety standards, and international IEC durability certifications.", "environmental": "Operates oxy-fuel glass melting furnaces reducing carbon emissions by 20% and NOx emissions by over 70%."},
        [0.22, 0.50, 0.38, 0.24, 0.60],
        {"threat_of_new_entrants": "Low; setting up solar glass furnaces requires complex ceramic refractory engineering and uninterrupted natural gas supply.", "bargaining_power_of_buyers": "Moderate; Indian solar module makers prefer Borosil for local availability and ALMM compliance.", "bargaining_power_of_suppliers": "Moderate; high-purity silica sand, soda ash, and piped natural gas.", "threat_of_substitutes": "Low; low-iron tempered glass is the universal protective front sheet for crystalline silicon solar panels.", "competitive_rivalry": "Moderate; competes with Chinese glass imports while expanding global export footprint."}
    ),
    (
        "Waaree Energies", "Power, Renewables & Clean Energy",
        "solar EPC contractors, commercial & industrial rooftop owners, and international solar developers",
        "demand high-efficiency, tier-1 certified solar photovoltaic modules engineered with the latest TOPCon and bifacial technology",
        "Waaree TOPCon & Bi-Facial Solar PV Module Series", "Solar Photovoltaic Cell & Module Manufacturing",
        "is India's largest solar PV module manufacturer with 12+ GW capacity, exporting high-efficiency modules to the US and dominating Indian rooftop and utility projects",
        [0.84, 0.92, 0.95, 0.95, 0.86, 0.90],
        {"political": "Key beneficiary of Approved List of Models and Manufacturers (ALMM) mandate and Basic Customs Duty (BCD) on imported solar modules.", "economic": "Huge financial scale and massive US export order book; backward-integrating into solar cell and ingot manufacturing.", "social": "Powers hundreds of thousands of farmer solar pumps under PM-KUSUM and green factories across India.", "technological": "Advanced n-type TOPCon module lines delivering over 22.5% module conversion efficiency and multi-busbar cell interconnection.", "legal": "ALMM listing, BIS solar certifications, and compliance with US Uyghur Forced Labor Prevention Act (UFLPA) supply-chain audits.", "environmental": "Solar modules generate green electricity for 30+ years; certified lead-free soldering and recycling initiatives."},
        [0.24, 0.52, 0.42, 0.22, 0.70],
        {"threat_of_new_entrants": "Moderate; many module assemblers exist, but matching Waaree's 12 GW scale, ALMM empanelment, and US export bankability is difficult.", "bargaining_power_of_buyers": "Moderate; developers compare module prices per watt, but require Tier-1 bankability for project debt.", "bargaining_power_of_suppliers": "Moderate to high; dependent on international solar polysilicon wafer suppliers.", "threat_of_substitutes": "Low; crystalline silicon is the dominant global solar standard.", "competitive_rivalry": "High with Adani Solar, Premier Energies, and Vikram Solar."}
    ),
    (
        "Premier Energies", "Power, Renewables & Clean Energy",
        "domestic and international solar module integrators and utility solar project developers",
        "require high-efficiency solar cells and modules manufactured with integrated cell-to-module quality control in modern cleanrooms",
        "Premier n-Type TOPCon Cells & Bifacial Modules", "Integrated Solar Cell & Module Manufacturing",
        "operates one of India's most modern automated solar cell and module manufacturing facilities in Hyderabad, leading the transition to n-type TOPCon cell tech",
        [0.84, 0.92, 0.95, 0.95, 0.86, 0.90],
        {"political": "Direct beneficiary of the Production Linked Incentive (PLI) scheme for high-efficiency solar modules and ALMM domestic content rules.", "economic": "Strong order backlog from blue-chip utility developers and high-margin exports to the United States solar market.", "social": "Fosters advanced technological manufacturing capabilities in Telangana, training hundreds of clean-energy technicians.", "technological": "Fully automated robotic cell manufacturing utilizing chemical vapor deposition, plasma etching, and laser-assisted contact optimization.", "legal": "ALMM compliant, BIS certified, and strict international environmental and labor audits.", "environmental": "High-efficiency TOPCon cells produce significantly more kilowatt-hours per square meter, reducing required solar farm land area."},
        [0.24, 0.50, 0.42, 0.22, 0.68],
        {"threat_of_new_entrants": "Low to moderate; solar cell manufacturing requires cleanroom environments and hundreds of crores in precision semiconductor machinery.", "bargaining_power_of_buyers": "Moderate; buyers demand high cell efficiency and Tier-1 bankability.", "bargaining_power_of_suppliers": "Moderate to high; global silicon wafer suppliers.", "threat_of_substitutes": "Low; solar PV is the cheapest source of new bulk electricity.", "competitive_rivalry": "Moderate to high with Waaree, Adani Solar, and Vikram Solar."}
    ),
    (
        "Inox Wind", "Power, Renewables & Clean Energy",
        "independent power producers (IPPs), public sector utilities, and captive green industrial projects",
        "need powerful, high-yield wind turbine generators engineered for low-speed wind regimes, with comprehensive turnkey wind farm development",
        "Inox Wind 3.3 MW WTG Platform & Turnkey Wind Solutions", "Wind Energy Equipment & Turnkey Project Development",
        "manufactures state-of-the-art 3.3 MW wind turbines with 145-meter rotors, operating multi-gigawatt blade and nacelle factories in Gujarat and MP",
        [0.80, 0.90, 0.95, 0.94, 0.86, 0.92],
        {"political": "Supports India's target of adding 10 GW of wind energy annually under MNRE's dedicated state-specific bidding trajectory.", "economic": "Turned net debt-free following major promoter capital infusions and large order wins from NTPC, SJVN, and private IPPs.", "social": "Generates green energy while providing rural land lease incomes and local technical employment across wind-rich states.", "technological": "Licensed European design tailored for Indian wind sites; automated resin infusion for 71-meter fiberglass rotor blades.", "legal": "RLMM listed by MNRE, CE certified, and compliant with state electricity grid connection codes.", "environmental": "Zero-emission wind power generation displacing thousands of tons of coal burned in conventional power plants."},
        [0.22, 0.48, 0.42, 0.22, 0.62],
        {"threat_of_new_entrants": "Low; specialized wind turbine tooling, aerodynamic testing, and turnkey land bank acquisition create steep entry hurdles.", "bargaining_power_of_buyers": "Moderate; developers negotiate competitive tariff bids in reverse auctions.", "bargaining_power_of_suppliers": "Moderate; specialized gearboxes, slewing bearings, and resin chemicals.", "threat_of_substitutes": "Moderate from solar energy, but hybrid wind-solar projects require both.", "competitive_rivalry": "Direct duopoly rivalry with Suzlon Energy in domestic wind manufacturing."}
    ),
    (
        "Tata Power Solar Systems", "Power, Renewables & Clean Energy",
        "residential housing societies, MSMEs, commercial complexes, and agricultural solar pump farmers",
        "need hassle-free, dependable rooftop solar installations with guaranteed net-metering execution and multi-decade power warranties",
        "Tata Power Solaroof & Solar Agricultural Water Pumps", "Distributed Rooftop Solar & Agricultural Solar EPC",
        "stands as India's #1 rooftop solar company for over 9 consecutive years, having installed over 2 GW of distributed rooftop solar systems across India",
        [0.82, 0.92, 0.96, 0.94, 0.86, 0.90],
        {"political": "Primary private executor for PM Surya Ghar Muft Bijli Yojana, enabling subsidized residential rooftop solar across 1 crore households.", "economic": "Lucrative distributed EPC model with attractive customer financing partnerships with leading public and private banks.", "social": "Enables middle-class families to reduce their monthly electricity bills to near zero while contributing to national green energy targets.", "technological": "IoT-enabled micro-inverters, remote solar performance monitoring mobile apps, and drone-based roof shade analysis.", "legal": "State DISCOM net-metering approvals, electrical inspectorate clearances, and BIS consumer safety norms.", "environmental": "Decentralized rooftop solar utilizes existing urban roof space, generating clean electricity without any land acquisition."},
        [0.26, 0.50, 0.35, 0.25, 0.68],
        {"threat_of_new_entrants": "Moderate; local rooftop solar installers exist, but Tata's unmatched brand trust and 25-year performance warranty form a powerful moat.", "bargaining_power_of_buyers": "Moderate; homeowners compare quotes, but overwhelmingly select Tata for safety and reliability.", "bargaining_power_of_suppliers": "Low; massive centralized purchasing of solar panels, inverters, and mounting structures.", "threat_of_substitutes": "Low; grid electricity is becoming increasingly expensive compared to rooftop solar amortized costs.", "competitive_rivalry": "Moderate; competes with fragmented local installers and new D2C solar startups (Freyr, SolarSquare)."}
    ),
    (
        "CESC Limited (RP-Sanjiv Goenka Group)", "Power, Renewables & Clean Energy",
        "over 3.5 million consumers in Kolkata, Howrah, Noida, and industrial hubs in Rajasthan",
        "demand uninterrupted, high-reliability electrical power with rapid storm outage restoration and transparent consumer billing",
        "Integrated Kolkata & Noida Power Distribution", "Urban Power Distribution Utility & Thermal Generation",
        "supplies uninterrupted 24/7 power to the megacity of Kolkata with world-class system reliability (SAIDI/SAIFI) and an unbroken operational legacy since 1899",
        [0.80, 0.92, 0.95, 0.90, 0.86, 0.82],
        {"political": "Regulated by West Bengal Electricity Regulatory Commission (WBERC) and Uttar Pradesh Electricity Regulatory Commission (UPERC).", "economic": "Highly stable, recession-proof cash flows guaranteed by licensed distribution monopolies in dense urban metropolitan centers.", "social": "The lifeblood of Kolkata's commercial economy and Durga Puja festivities, ensuring uninterrupted electricity during severe monsoon thunderstorms.", "technological": "Fully automated SCADA network control center, underground distribution cables, and smart prepaid electric meters.", "legal": "Distribution license exclusivity under the Electricity Act 2003, conforming to state grid regulatory standards.", "environmental": "Adheres to stringent thermal emission caps; expanding solar power procurement to meet Renewable Purchase Obligations (RPO)."},
        [0.18, 0.40, 0.35, 0.18, 0.52],
        {"threat_of_new_entrants": "Zero in core licensed areas; physical distribution networks in Kolkata and Noida are statutory monopolies.", "bargaining_power_of_buyers": "Low; residential and commercial consumers are bound to the licensed utility.", "bargaining_power_of_suppliers": "Moderate; fuel linkage with Coal India and power purchase agreements.", "threat_of_substitutes": "Low; grid electricity cannot be substituted in dense urban high-rises.", "competitive_rivalry": "Zero in licensed distribution zones; competes in renewable project tenders."}
    ),
    (
        "Gujarat Industries Power Company (GIPCL)", "Power, Renewables & Clean Energy",
        "Gujarat state grid off-taker (GUVNL) and regional industrial power consumers",
        "require dependable, low-cost gas, lignite, and large-scale renewable electricity to support Gujarat's vibrant manufacturing economy",
        "Khavda Renewable Energy Park (2,375 MW) & Combined Cycle Power", "State Clean Energy & Mega-Renewable Park Developer",
        "is developing a massive 2,375 MW renewable energy park in Khavda, Gujarat, while operating highly reliable gas and lignite power stations",
        [0.80, 0.90, 0.94, 0.90, 0.86, 0.85],
        {"political": "Promoted by leading Gujarat public sector undertakings (GSFC, GACL, Petrochem), strongly supported by the Government of Gujarat.", "economic": "Steady revenue and dividend track record; major upside from commissioning massive renewable park capacity in Khavda.", "social": "Powers regional industrial belts and agricultural water pumping in central and western Gujarat.", "technological": "Advanced combined-cycle gas turbines and high-capacity solar PV string inverters optimized for saline desert environments.", "legal": "Regulated by GERC; long-term power purchase agreements with GUVNL.", "environmental": "Accelerating transition away from fossil fuels to mega-scale solar and wind generation in the Rann of Kutch."},
        [0.20, 0.45, 0.35, 0.20, 0.55],
        {"threat_of_new_entrants": "Low; access to land allocations in Khavda Renewable Park is restricted to vetted public and private utilities.", "bargaining_power_of_buyers": "Moderate; GUVNL negotiates regulated tariffs under GERC frameworks.", "bargaining_power_of_suppliers": "Moderate; solar module and turbine suppliers.", "threat_of_substitutes": "Low; bulk electrical power is universally required.", "competitive_rivalry": "Moderate; collaborates and operates alongside GSECL and Torrent Power in Gujarat."}
    ),
    (
        "NLC India (Neyveli Lignite)", "Power, Renewables & Clean Energy",
        "state power distribution companies across Tamil Nadu, Karnataka, Kerala, and Andhra Pradesh",
        "need affordable baseload pit-head electrical power and large-scale green energy capacity to support southern India's industrial grid",
        "Pit-Head Lignite Thermal Stations & Mega Solar Parks", "Navratna Mining & Thermal-Renewable Power Generation",
        "operates massive open-cast lignite mines in Neyveli, generating 6,000+ MW of power and aggressively expanding toward 6,000 MW of pure renewable energy",
        [0.84, 0.92, 0.96, 0.90, 0.88, 0.82],
        {"political": "Navratna public sector enterprise under Ministry of Coal; key pillar of southern regional power security.", "economic": "Low-cost captive pit-head lignite fuel eliminates freight transport expenses, delivering low per-unit power generation costs.", "social": "The largest industrial employer in central Tamil Nadu, providing free community healthcare, schools, and township infrastructure.", "technological": "Specialized bucket-wheel excavators, continuous conveyor belt mining, and high-efficiency utility-scale solar PV installations.", "legal": "CERC tariff determinations, mine closure regulations, and Ministry of Environment, Forest and Climate Change (MoEFCC) clearances.", "environmental": "Pioneered afforestation of mined-out pit areas, converting open-cast lignite pits into massive freshwater eco-parks and lakes."},
        [0.15, 0.40, 0.25, 0.18, 0.50],
        {"threat_of_new_entrants": "Zero in pit-head lignite power; mining concessions are statutory sovereign allocations.", "bargaining_power_of_buyers": "Low to moderate; southern state utilities rely on NLC for low-cost baseload power.", "bargaining_power_of_suppliers": "Low; captive mining operations provide 100% internal fuel self-sufficiency.", "threat_of_substitutes": "Low for essential grid baseload power.", "competitive_rivalry": "Low to moderate; competes primarily in central renewable power auctions."}
    ),
    (
        "KPI Green Energy", "Power, Renewables & Clean Energy",
        "commercial and industrial (C&I) enterprises in Gujarat seeking to reduce high electricity tariffs",
        "need customized captive solar and hybrid wind-solar power plants that cut industrial electricity bills by over 40% under open-access norms",
        "Captive Power Producer (CPP) & Independent Power Producer (IPP) Solar", "Commercial & Industrial Solar and Hybrid Energy Solutions",
        "dominates Gujarat's high-margin industrial C&I renewable market, delivering over 1 GW of solar and wind-solar hybrid power plants for textile and chemical factories",
        [0.78, 0.88, 0.94, 0.92, 0.84, 0.88],
        {"political": "Direct beneficiary of Gujarat Renewable Energy Policy and national open-access green energy regulations.", "economic": "Dual business model: high-margin EPC sales to corporate clients seeking captive assets, and recurring revenue from owned IPP solar plants.", "social": "Accelerates the greening of Gujarat's energy-intensive MSME manufacturing clusters (Surat, Bharuch, Dahej).", "technological": "In-house private transmission evacuation lines connecting captive industrial customers directly to central substations.", "legal": "GERC open-access regulations, net-metering norms, and statutory electrical safety certifications.", "environmental": "Helps hundreds of manufacturing companies eliminate their carbon emissions, meeting global export supply chain ESG audits."},
        [0.25, 0.50, 0.38, 0.24, 0.65],
        {"threat_of_new_entrants": "Moderate; building private transmission evacuation lines and pooling substations requires heavy capital and local right of way.", "bargaining_power_of_buyers": "Moderate; industrial clients compare power savings against grid power tariffs.", "bargaining_power_of_suppliers": "Moderate; solar module and wind turbine component suppliers.", "threat_of_substitutes": "Moderate from state DISCOM grid power, but grid power is much more expensive.", "competitive_rivalry": "Moderate; leading specialist player in Gujarat's corporate C&I renewable space."}
    ),
    (
        "Gensol Engineering", "Power, Renewables & Clean Energy",
        "solar developers, corporate fleets, and urban electric mobility operators",
        "need specialized solar advisory and EPC, combined with modern electric vehicle fleet leasing and urban green logistics",
        "Solar EPC Turnkey Projects & EV Fleet Mobility Solutions", "Solar Engineering EPC & Electric Mobility Fleet Solutions",
        "uniquely combines multi-gigawatt solar consulting and EPC with over 6,000 leased electric vehicles for ride-hailing and green urban logistics",
        [0.78, 0.88, 0.94, 0.94, 0.84, 0.90],
        {"political": "Supports FAME II and PM e-Drive EV incentives alongside national solar capacity addition targets.", "economic": "Rapid financial expansion fueled by large-scale solar EPC contracts, battery energy storage system (BESS) bids, and EV fleet leasing.", "social": "Promotes zero-emission urban transportation, curbing toxic vehicular air pollution in major Indian metro cities.", "technological": "Engineering precision in utility solar design, integrated battery energy storage software, and automated EV fleet telematics.", "legal": "Compliance with CEA electrical safety guidelines, motor vehicle regulations, and corporate listing governance.", "environmental": "Synergizes solar generation with electric vehicle charging, creating a closed-loop zero-emission mobility ecosystem."},
        [0.28, 0.52, 0.40, 0.25, 0.68],
        {"threat_of_new_entrants": "Moderate; solar EPC is competitive, but combining utility solar EPC with large-scale EV fleet leasing requires balance sheet versatility.", "bargaining_power_of_buyers": "Moderate; solar clients and mobility platforms negotiate competitive lease rates.", "bargaining_power_of_suppliers": "Moderate; EV manufacturers (Tata Motors) and tier-1 solar module makers.", "threat_of_substitutes": "Moderate from separate standalone solar EPCs and traditional diesel fleet leasers.", "competitive_rivalry": "Moderate to high with standalone solar EPC contractors."}
    ),
    (
        "IREDA (Indian Renewable Energy Development Agency)", "Power, Renewables & Clean Energy",
        "renewable energy project developers, green hydrogen startups, and clean technology entrepreneurs",
        "require specialized, long-term, and cost-effective debt financing and loan syndication for high-capex green energy projects",
        "Renewable Project Debt Financing & Green Bond Issuance", "Navratna Green Energy Non-Banking Financial Institution (NBFC)",
        "stands as India's premier dedicated green financier, funding over 20 GW of solar, wind, hydro, and green hydrogen projects with near-zero non-performing assets",
        [0.86, 0.94, 0.96, 0.92, 0.88, 0.94],
        {"political": "Navratna NBFC under Ministry of New and Renewable Energy; the primary financial arm for executing India's 500 GW non-fossil energy targets.", "economic": "High return on equity (>16%) with lowest cost of borrowing in the renewable sector; pristine asset quality and robust loan book growth.", "social": "Finances clean drinking water solar filtration, rural distributed bio-energy, and electric mobility infrastructure across India.", "technological": "Proprietary green credit appraisal algorithms, digital loan disbursement, and environmental risk assessment telemetry.", "legal": "RBI NBFC regulations, international green taxonomy compliance, and statutory sovereign corporate governance.", "environmental": "Finances exclusively green and climate-friendly assets, accelerating the displacement of fossil fuels across India."},
        [0.18, 0.42, 0.30, 0.20, 0.50],
        {"threat_of_new_entrants": "Low; dedicated sovereign green charter and lowest-cost access to international multilateral climate funds (World Bank, ADB, JICA).", "bargaining_power_of_buyers": "Moderate; renewable developers compare loan rates against PFC and REC.", "bargaining_power_of_suppliers": "Low; sovereign credit ratings ensure ultra-low borrowing yields on domestic and global bond markets.", "threat_of_substitutes": "Moderate from commercial banks, but commercial banks lack IREDA's 20-year project loan tenors.", "competitive_rivalry": "Moderate; collaborates and competes alongside PFC and REC in clean energy lending."}
    )
]

for item in sector14_data:
    add_c(*item)

print(f"Sector 14 added: {len(sector14_data)} companies. Total: {len(part3_a)}")

# ==============================================================================
# SECTOR 15: Oil, Gas, Refining & Petrochemicals (20 companies)
# ==============================================================================
sector15_data = [
    (
        "Reliance Industries - Oil to Chemicals (O2C)", "Oil, Gas, Refining & Petrochemicals",
        "global energy markets, domestic transport sector, and plastic/chemical downstream processors",
        "need high-volume, premium transportation fuels (diesel, petrol, jet fuel) and essential petrochemical building blocks (polymers, aromatics, polyester)",
        "Jamnagar Refining Complex & Downstream Petrochemicals", "Integrated Mega-Refining & High-Value Petrochemicals",
        "operates the world's largest single-location refining complex in Jamnagar (1.4 million barrels/day), converting the heaviest crude into premium fuels and chemicals",
        [0.84, 0.96, 0.98, 0.96, 0.88, 0.74],
        {"political": "Critical contributor to national foreign exchange earnings; operates deep-water crude import berths and SEZ export refining assets.", "economic": "Generates hundreds of billions of dollars in revenue; unmatched Nelson Complexity Index (>21) enables processing of cheap heavy sour crude into premium fuels.", "social": "Powers India's transport connectivity and supplies polymers for food packaging, medical equipment, and textile fabrics nationwide.", "technological": "World-class fluid catalytic cracking, coking units, and petroleum coke gasification converting bottom-of-the-barrel residue into synthetic gas.", "legal": "Directorate General of Hydrocarbons compliance, environmental clearances, and international maritime fuel standards (IMO 2020).", "environmental": "Massive investments into carbon capture, algae bio-crude, and transitioning Jamnagar into an integrated green energy and chemicals hub."},
        [0.10, 0.45, 0.35, 0.18, 0.60],
        {"threat_of_new_entrants": "Practically impossible; building a 1.4-million-barrel/day deep-water coastal refining complex costs tens of billions of dollars.", "bargaining_power_of_buyers": "Moderate; refined fuels and polymers trade at global benchmark parity prices (Singapore GRM, ICIS polymer indices).", "bargaining_power_of_suppliers": "Moderate; crude oil sourced from global state oil producers (Saudi Aramco, ADNOC, Rosneft).", "threat_of_substitutes": "Moderate from electric mobility in the long run; low in petrochemicals and polymers.", "competitive_rivalry": "Low to moderate; unmatched global scale superiority over all Asian refiners."}
    ),
    (
        "Oil and Natural Gas Corporation (ONGC)", "Oil, Gas, Refining & Petrochemicals",
        "Indian oil refiners, natural gas distribution networks, and the national economy",
        "require domestic crude oil and natural gas production to reduce India's dangerous 85%+ dependence on foreign imported hydrocarbons",
        "Mumbai High Offshore & KG-DWN Deepwater Field Exploration", "Sovereign Upstream Oil & Natural Gas Exploration and Production",
        "is India's largest crude oil and natural gas company, producing ~70% of domestic crude oil and ~84% of natural gas across offshore and onshore basins",
        [0.88, 0.95, 0.98, 0.94, 0.88, 0.72],
        {"political": "Maharatna flagship; strategic arm of the Ministry of Petroleum & Natural Gas ensuring sovereign energy security and resource control.", "economic": "Vast operating cash flows driven by domestic crude realizations and government-determined natural gas pricing formulas (Kirit Parikh guidelines).", "social": "The foundational bedrock of India's industrialization, providing fuel and natural gas for fertilizer plants and cooking gas.", "technological": "Deepwater drilling rigs, subsea production trees in the Krishna-Godavari deep basin, and 3D seismic geological visualization.", "legal": "Petroleum and Natural Gas Regulatory Board (PNGRB) compliance, Directorate General of Hydrocarbons (DGH) oversight, and HELP licensing.", "environmental": "Adheres to zero flaring targets, offshore marine habitat protection, and investments in offshore wind and geothermal energy."},
        [0.10, 0.35, 0.30, 0.15, 0.40],
        {"threat_of_new_entrants": "Zero; sovereign exploration rights and multi-billion-dollar offshore drilling capex exclude new entrants.", "bargaining_power_of_buyers": "Low; domestic refiners (IOCL, BPCL, HPCL) take 100% of ONGC's crude oil at international import parity benchmarks.", "bargaining_power_of_suppliers": "Moderate; offshore oilfield service contractors (Schlumberger, Halliburton) and specialized drilling vessels.", "threat_of_substitutes": "Low; crude oil and natural gas are indispensable for national transport and petrochemicals.", "competitive_rivalry": "Low; operates as the national upstream champion with Oil India as a regional peer."}
    ),
    (
        "Indian Oil Corporation (IOCL)", "Oil, Gas, Refining & Petrochemicals",
        "over 30 million motorists daily, commercial airlines, industries, and rural households",
        "demand reliable, ubiquitous supply of petrol, diesel, Indane cooking gas (LPG), and aviation jet fuel at fair, stable national prices",
        "Indane LPG, SERVO Lubricants & Pan-India Fuel Retail Network", "National Oil Refining, Pipeline & Downstream Fuel Retail Network",
        "stands as 'The Energy of India', operating 9 refineries, a 17,000 km cross-country pipeline network, and over 36,000 retail fuel fuel stations",
        [0.88, 0.96, 0.99, 0.92, 0.88, 0.72],
        {"political": "Maharatna sovereign fuel champion; acts as the primary price stabilizer for transport fuels and domestic cooking gas across all Indian states.", "economic": "Fortune 500 powerhouse generating over Rs 8,50,000 Cr in revenue; massive pipeline network provides unmatched low-cost inland fuel transport.", "social": "Indane LPG touches over 150 million homes, liberating rural women from wood smoke under PM Ujjwala Yojana; SERVO is India's #1 lubricant.", "technological": "Indigenous INDMAX refining technology converting heavy residues into LPG, green hydrogen fuel cell buses, and smart automated fuel dispensing.", "legal": "Regulated under Ministry of Petroleum & Natural Gas, PNGRB pipeline access rules, and Weights and Measures fuel dispensing accuracy.", "environmental": "Building mega green hydrogen plants at Mathura and Panipat refineries; installing EV fast chargers across 10,000+ retail fuel pumps."},
        [0.15, 0.48, 0.30, 0.20, 0.65],
        {"threat_of_new_entrants": "Low to non-existent; building 36,000 fuel stations and 17,000 km of underground pipelines requires decades and tens of billions of dollars.", "bargaining_power_of_buyers": "Moderate; motorists have equal access to BPCL and HPCL pumps, but trust IOCL's ubiquitous highway network.", "bargaining_power_of_suppliers": "Low to moderate; crude oil procured via term contracts with national oil companies.", "threat_of_substitutes": "Moderate from electric vehicles in the long run; low in heavy commercial transport and aviation.", "competitive_rivalry": "Moderate oligopoly competition with sister public sector OMCs (BPCL, HPCL)."}
    ),
    (
        "Bharat Petroleum Corporation (BPCL)", "Oil, Gas, Refining & Petrochemicals",
        "urban motorists, premium car owners, commercial transport fleets, and domestic LPG kitchens",
        "need premium, high-octane fuels (Speed), pure lubricants, and digitally automated fuel dispensing with guaranteed quantity and quality",
        "Speed High-Octane Petrol, Bharatgas & MAK Lubricants", "High-Efficiency Oil Refining & Smart Fuel Retail Network",
        "pioneered smart automated fuel retail in India with 'Pure for Sure', operating ultra-modern coastal refineries in Mumbai and Kochi (Kochi Refinery)",
        [0.85, 0.94, 0.98, 0.92, 0.86, 0.72],
        {"political": "Maharatna public sector energy major; major contributor to central dividends, excise collections, and national energy transition.", "economic": "High refining complexity at Kochi and Mumbai refineries produces top-tier gross refining margins (GRMs) and robust dividend distributions.", "social": "Bharatgas provides clean cooking energy to over 85 million Indian households; MAK lubricants trusted across automotive workshops.", "technological": "Integrated Petrochemical Complex (PDPP) in Kochi producing niche petrochemicals (acrylic acid, acrylates); digital 'Urja' AI customer chatbot.", "legal": "PNGRB regulations, environmental stack emission standards, and corporate public sector governance.", "environmental": "Developing 1 GW of renewable wind and solar capacity to power captive refining operations and green hydrogen mobility pilots."},
        [0.18, 0.50, 0.32, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; building coastal refining and a 21,000-pump retail network is prohibitive for private startups.", "bargaining_power_of_buyers": "Moderate; retail motorists compare pump service quality and rewards (BPCL PetroCard).", "bargaining_power_of_suppliers": "Low to moderate; crude oil sourced under diversified global term tenders.", "threat_of_substitutes": "Moderate from alternative electric transport; low in aviation and petrochemicals.", "competitive_rivalry": "Direct oligopoly rivalry with IOCL and HPCL."}
    ),
    (
        "Hindustan Petroleum Corporation (HPCL)", "Oil, Gas, Refining & Petrochemicals",
        "motorists, commercial transport operators, and LPG consumers across western and southern India",
        "need reliable, digitally automated fuel dispensing, doorstep diesel delivery, and dependable cooking gas cylinders",
        "Power95 Petrol, HP Gas & HP Lubricants", "Downstream Petroleum Refining & Marketing Ecosystem",
        "operates over 21,000 modern retail fuel stations, delivering clean cooking gas to 90 million homes and modernizing mega-refineries in Mumbai and Vizag",
        [0.85, 0.94, 0.98, 0.92, 0.86, 0.72],
        {"political": "Maharatna subsidiary of ONGC, forming a fully integrated upstream-to-downstream national hydrocarbon powerhouse.", "economic": "Major beneficiary of the Visakh Refinery Modernization Project (VRMP) expanding refining capacity to 15 MMTPA with higher distillate yields.", "social": "HP Gas is an indispensable household utility for millions of families; HP Pay mobile app drives digitized fueling rewards.", "technological": "Doorstep diesel delivery platforms (Humsafar), high-octane Power95 and PoWer100 fuel blending, and green hydrogen pilot plants.", "legal": "PNGRB pipeline regulations, central environmental safety clearances, and weights & measures legal audits.", "environmental": "Rooftop solarization across 50% of retail outlets, rainwater harvesting, and developing second-generation (2G) ethanol plants."},
        [0.18, 0.50, 0.32, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; retail fuel infrastructure requires massive land parcels and statutory oil safety clearances.", "bargaining_power_of_buyers": "Moderate; fuel consumers switch between OMC brands based on pump convenience.", "bargaining_power_of_suppliers": "Low; crude oil supplied internally by parent ONGC and international crude tankers.", "threat_of_substitutes": "Moderate from CNG and EVs in urban personal mobility.", "competitive_rivalry": "High with IOCL and BPCL across every highway and city junction."}
    ),
    (
        "GAIL (India) Limited", "Oil, Gas, Refining & Petrochemicals",
        "city gas distribution networks, power plants, fertilizer factories, and industrial consumers",
        "need safe, uninterrupted, high-pressure natural gas transmission across cross-country pipelines to replace polluting coal and furnace oil",
        "Hazira-Vijaipur-Jagdishpur (HVJ) Gas Pipeline & National Gas Grid", "Sovereign Natural Gas Transmission, Processing & Petrochemicals",
        "operates over 15,600 km of natural gas pipelines—holding 70% national pipeline market share—acting as the gas lifeline for India's clean energy transition",
        [0.88, 0.95, 0.98, 0.94, 0.88, 0.82],
        {"political": "Maharatna sovereign gas champion under Ministry of Petroleum; spearheading Government of India's target to raise gas in energy mix to 15%.", "economic": "Regulated pipeline transmission tariffs provide highly predictable, recession-proof cash flows; strong profit contributions from polymer petrochemicals.", "social": "Powers clean cooking piped natural gas (PNG) and green vehicle CNG, eliminating dangerous particulate air pollution from Indian cities.", "technological": "Urja Ganga gas pipeline spanning Eastern India, SCADA automated pipeline valve controls, and green hydrogen blending into city gas networks.", "legal": "PNGRB open-access pipeline regulations, statutory gas transportation tariffs, and petroleum safety certifications.", "environmental": "Natural gas produces 50% less carbon emissions than coal and zero particulate soot; building green hydrogen electrolyzers in Vijaipur."},
        [0.10, 0.35, 0.28, 0.15, 0.45],
        {"threat_of_new_entrants": "Practically zero; laying cross-country natural gas pipelines requires statutory right-of-use (RoU) and billions in capex.", "bargaining_power_of_buyers": "Low; industrial and fertilizer plants are connected to GAIL's physical pipeline and have no alternative delivery channel.", "bargaining_power_of_suppliers": "Moderate; long-term LNG supply contracts from Qatar, USA, and domestic fields (ONGC/RIL).", "threat_of_substitutes": "Low; natural gas is legally mandated in clean fuel zones (NCR) and is the essential feedstock for urea fertilizers.", "competitive_rivalry": "Low; natural monopoly in interstate gas transmission."}
    ),
    (
        "Oil India Limited", "Oil, Gas, Refining & Petrochemicals",
        "northeastern refiners, national gas grids, and the sovereign petroleum reserve",
        "require specialized upstream crude oil and natural gas exploration and production in complex geological formations across Assam and the Northeast",
        "Brahmaputra Basin Exploration & Numaligarh Refinery Integration", "Upstream Exploration & Northeastern Hydrocarbon Development",
        "stands as India's second-largest public upstream exploration company, anchoring energy security across the Northeast with rich crude reserves",
        [0.86, 0.92, 0.96, 0.92, 0.88, 0.72],
        {"political": "Navratna upstream company; strategic executor of the Hydrocarbon Vision 2030 for North-East India.", "economic": "Majority shareholder in Numaligarh Refinery Limited (NRL), forming an integrated high-margin upstream-refining powerhouse in Assam.", "social": "Major driver of economic prosperity, local tribal employment, and social development across rural Upper Assam and Arunachal Pradesh.", "technological": "Horizontal directional drilling under mighty riverbeds (Brahmaputra), 3D seismic imaging in folded mountain belts, and enhanced oil recovery (EOR).", "legal": "HELP upstream licenses, Petroleum Mining Leases (PML), and strict forest conservation clearances.", "environmental": "Operates eco-friendly drilling pads, produced-water treatment plants, and elephant corridor conservation protocols."},
        [0.12, 0.35, 0.28, 0.15, 0.40],
        {"threat_of_new_entrants": "Zero; sovereign mining leases across the complex geological terrains of Assam.", "bargaining_power_of_buyers": "Low; regional refineries (Numaligarh, Bongaigaon, Guwahati) take 100% of crude production at import parity.", "bargaining_power_of_suppliers": "Moderate; specialized drilling rig contractors and seismic exploration services.", "threat_of_substitutes": "Low; domestic crude is vital for regional energy autonomy.", "competitive_rivalry": "Low; collaborates with ONGC in national exploration bidding."}
    ),
    (
        "Indraprastha Gas Limited (IGL)", "Oil, Gas, Refining & Petrochemicals",
        "millions of vehicle owners, auto-rickshaw drivers, and residential households across Delhi-NCR",
        "need clean, economical Compressed Natural Gas (CNG) for vehicles and 24/7 piped natural gas (PNG) for kitchen cooking and water heating",
        "Delhi-NCR City Gas Distribution & Piped Natural Gas (PNG)", "City Gas Distribution Utility & Clean Transport Fuel",
        "operates the world's largest CNG refueling network in Delhi-NCR across 800+ stations, powering 1.5+ million green vehicles and 2.5 million homes",
        [0.84, 0.94, 0.98, 0.90, 0.88, 0.88],
        {"political": "Promoted by GAIL and BPCL; direct instrument of the Supreme Court of India's clean air directives eliminating diesel buses in Delhi.", "economic": "Exceptional return on capital (ROCE >25%) and negative working capital; massive volume demand from mandatory commercial CNG fleets.", "social": "Dramatically reduced respiratory sulfur emissions in Delhi-NCR, providing auto-rickshaws and cabs with 50% cheaper fuel than petrol.", "technological": "Underground MDPE pipeline distribution, automated SCADA monitoring, smart prepaid gas meters, and fast-fill CNG dispensers.", "legal": "PNGRB geographical exclusivity licenses, Petroleum and Explosives Safety Organization (PESO) clearances.", "environmental": "CNG eliminates black carbon soot and particulate matter (PM 2.5), significantly improving the National Capital Region's air quality index."},
        [0.10, 0.40, 0.40, 0.22, 0.45],
        {"threat_of_new_entrants": "Zero in core authorized territories; PNGRB grants 25-year network infrastructure exclusivity.", "bargaining_power_of_buyers": "Low to moderate; commercial fleet operators are legally mandated to run on CNG; piped gas is cheaper than LPG cylinders.", "bargaining_power_of_suppliers": "Moderate; receives domestic natural gas allocations under government Administered Price Mechanism (APM).", "threat_of_substitutes": "Moderate from electric buses and EV two/three-wheelers in the long run.", "competitive_rivalry": "Zero inside authorized geographical zones; competes in tenders for new geographical areas."}
    ),
    (
        "Mahanagar Gas Limited (MGL)", "Oil, Gas, Refining & Petrochemicals",
        "commuters, taxi fleets, and families across Greater Mumbai, Thane, and Raigad",
        "demand safe, continuous, and economical piped natural gas directly to kitchen stoves, and high-pressure CNG for commercial auto/taxi fleets",
        "Mumbai City Gas Distribution & Piped Cooking Gas", "Urban City Gas Distribution Utility",
        "powers Mumbai's transit lifeline, providing uninterrupted piped cooking gas to 2+ million households and fueling Mumbai's iconic black-and-yellow taxis",
        [0.84, 0.94, 0.98, 0.90, 0.88, 0.88],
        {"political": "Promoted by GAIL with Government of Maharashtra equity; authorized by PNGRB to supply Mumbai's clean fuel infrastructure.", "economic": "Debt-free balance sheet with high cash balances and high dividend payouts; resilient operating margins supported by stable retail demand.", "social": "Eliminates the hassle of booking and waiting for heavy LPG cylinders in Mumbai high-rise apartments.", "technological": "High-density polyethene (MDPE) pipeline distribution, GIS mapping of subterranean gas networks, and automated leak detection sniffing vehicles.", "legal": "PNGRB statutory exclusivity, PESO gas cylinder filling certifications, and municipal trenching permissions.", "environmental": "Replaces polluting transport fuels and kerosene with clean-burning methane, curbing carbon and sulfur emissions in coastal Mumbai."},
        [0.10, 0.40, 0.40, 0.22, 0.45],
        {"threat_of_new_entrants": "Zero; physical underground city gas pipeline networks cannot be duplicated.", "bargaining_power_of_buyers": "Low; consumers enjoy continuous convenience and cheaper costs compared to bottled LPG.", "bargaining_power_of_suppliers": "Moderate; reliant on central government APM natural gas allocations and RLNG imports.", "threat_of_substitutes": "Moderate from EV auto-rickshaws and induction cooking stoves.", "competitive_rivalry": "Zero inside Mumbai municipal limits; acquired Unison Enviro to expand into surrounding Maharashtra districts."}
    ),
    (
        "Gujarat Gas Limited", "Oil, Gas, Refining & Petrochemicals",
        "industrial ceramics manufacturing clusters (Morbi), textile dye houses, and residential consumers across Gujarat",
        "need high-volume, reliable industrial natural gas to fire high-temperature ceramic tile kilns and clean fuel for vehicles",
        "Industrial Natural Gas Supply & Morbi Ceramics Clean Energy", "India's Largest City Gas Distribution (CGD) Company",
        "is India's largest city gas company by volume (processing 10+ MMSCMD), powering the world's second-largest ceramic tile manufacturing hub in Morbi",
        [0.84, 0.94, 0.98, 0.92, 0.88, 0.85],
        {"political": "Promoted by Gujarat State Petroleum Corporation (GSPC); key instrument of National Green Tribunal (NGT) orders banning coal gasifiers in Morbi.", "economic": "Immense volume scale; industrial gas consumption drives ~80% of volume, creating massive operating leverage and cash generation.", "social": "Transformed Morbi from a smog-choked industrial basin into a clean global export leader in ceramic tiles and vitrified sanitaryware.", "technological": "High-volume industrial gas metering skids, multi-city gas grid integration, and computerized pressure-reducing stations.", "legal": "PNGRB authorized CGD network operator with extensive geographical rights across 44 districts in 6 states.", "environmental": "Completely eliminated toxic coal gasifier tar pollution in Morbi, reducing hundreds of thousands of tons of carbon dioxide and sulfur dioxide emissions."},
        [0.12, 0.50, 0.42, 0.25, 0.50],
        {"threat_of_new_entrants": "Zero in authorized operating zones under PNGRB infrastructure exclusivity.", "bargaining_power_of_buyers": "Moderate to high; ceramic tile factory owners compare natural gas prices against propane and imported fuel oil.", "bargaining_power_of_suppliers": "Moderate to high; requires substantial imported spot and term LNG from Dahej to meet massive industrial volume demand.", "threat_of_substitutes": "Moderate from industrial liquefied petroleum gas (LPG/Propane).", "competitive_rivalry": "Low to moderate; undisputed volume king of Indian city gas distribution."}
    ),
    (
        "Petronet LNG", "Oil, Gas, Refining & Petrochemicals",
        "power stations, fertilizer manufacturers, city gas distribution companies, and industrial gas consumers",
        "require world-scale liquefied natural gas (LNG) regasification terminal infrastructure to import and convert cryogenic LNG into high-pressure natural gas",
        "Dahej & Kochi LNG Regasification Mega-Terminals", "Cryogenic LNG Import & Regasification Infrastructure",
        "operates South Asia's largest LNG terminal at Dahej (17.5 MMTPA), handling over 55% of India's total LNG imports with exceptional operational reliability",
        [0.85, 0.94, 0.98, 0.94, 0.88, 0.85],
        {"political": "Formed by Government of India with 50% equity held by public sector oil majors (IOCL, ONGC, BPCL, GAIL); strategic gateway for India's LNG imports.", "economic": "Toll-based regasification tariff model generates bulletproof annuity cash flows with multi-decade take-or-pay volume guarantees.", "social": "Secures essential natural gas feedstocks that keep national urea fertilizer plants producing subsidized food crops for Indian farmers.", "technological": "Cryogenic storage tanks operating at minus 160 deg C, submerged combustion vaporizers (SCV), and specialized LNG carrier jetty unloading arms.", "legal": "PNGRB tariff oversight, maritime port regulatory approvals, and long-term sale-and-purchase agreements (SPA) with QatarEnergy and ExxonMobil.", "environmental": "Utilizes seawater heat exchange vaporizers to gasify LNG, saving immense fuel energy and eliminating thousands of tons of boiler emissions."},
        [0.12, 0.40, 0.35, 0.15, 0.45],
        {"threat_of_new_entrants": "Very low; constructing deep-water cryogenic LNG terminals with marine breakwaters requires billions in capex and maritime clearances.", "bargaining_power_of_buyers": "Low; off-takers (GAIL, IOCL, BPCL) are locked into long-term take-or-pay regasification contracts.", "bargaining_power_of_suppliers": "Moderate; international LNG liquefaction sovereigns (Qatar, Australia).", "threat_of_substitutes": "Low; domestic natural gas production is insufficient to meet Indian demand, making LNG imports indispensable.", "competitive_rivalry": "Low; unmatched capacity advantages over private terminals in Hazira and Mundra."}
    ),
    (
        "Castrol India", "Oil, Gas, Refining & Petrochemicals",
        "motorists, commercial truck fleet operators, industrial machinery workshops, and farmers",
        "need advanced synthetic automotive and industrial engine oils that maximize thermal protection, extend oil-drain intervals, and prevent engine wear",
        "Castrol GTX, MAGNATEC, CRB Turbomax & Castrol ON EV Fluids", "High-Performance Automotive Lubricants & Thermal Fluids",
        "leads India's organized private lubricant market with over 115 years of heritage, trusted by over 150,000 retail mechanics across India",
        [0.68, 0.88, 0.95, 0.90, 0.84, 0.72],
        {"political": "Complies with Bureau of Indian Standards (BIS) lubricating oil norms and national Extended Producer Responsibility (EPR) for waste oil.", "economic": "Industry-leading return on capital (ROCE >60%) and debt-free balance sheet driven by brand premium pricing and asset-light blending plants.", "social": "Deep grassroots relationship with independent mechanics through the Castrol Fast Scan app and mechanic family insurance programs.", "technological": "Dualock molecule technology clinging to critical engine parts, fluid titanium shear resistance, and advanced immersion cooling fluids for EV batteries.", "legal": "Consumer protection trade standards, anti-counterfeit holographic packaging enforcement, and corporate statutory disclosures.", "environmental": "Pioneered 100% post-consumer recycled plastic bottles for lubricant packaging and eco-friendly bio-degradable industrial cutting oils."},
        [0.28, 0.52, 0.40, 0.28, 0.72],
        {"threat_of_new_entrants": "Low; building Castrol's 150,000-mechanic brand trust and automotive workshop recommendation channel takes decades.", "bargaining_power_of_buyers": "Moderate; motorists follow trusted local mechanic recommendations for oil brands.", "bargaining_power_of_suppliers": "Moderate; base oil (Group II/III) prices fluctuate with crude oil refining cycles.", "threat_of_substitutes": "Moderate from public sector OMC lubricant brands (SERVO, MAK, HP).", "competitive_rivalry": "High with IOCL SERVO, Gulf Oil, and Motul."}
    ),
    (
        "Chennai Petroleum Corporation (CPCL)", "Oil, Gas, Refining & Petrochemicals",
        "transport fleets, petrochemical industries, and power generators across Tamil Nadu and South India",
        "need reliable petroleum transport fuels, industrial solvents, naphtha, and bitumen for highway road building in southern India",
        "Manali Petroleum Refinery Products & Highway Bitumen", "Crude Oil Refining & Industrial Bitumen Infrastructure",
        "operates the 10.5 MMTPA Manali Refinery in Chennai, supplying 100% of fuel and road-construction bitumen requirements for Tamil Nadu and neighboring states",
        [0.82, 0.90, 0.95, 0.90, 0.86, 0.70],
        {"political": "Group company of Indian Oil Corporation (IOCL); executing the massive 9 MMTPA Cauvery Basin Refinery project in Nagapattinam.", "economic": "Turnaround driven by high regional fuel demand, pipeline connectivity to IOCL marketing terminals, and strong operational refining throughput.", "social": "Critical regional employment anchor in North Chennai and provider of high-grade bitumen for highway infrastructure projects across South India.", "technological": "Residue Upgradation Facility (RUF) converting heavy asphalt into high-value BS-VI petrol and diesel with low sulfur emissions.", "legal": "Compliant with BS-VI automotive fuel specifications, TNPCB pollution board consent, and coastal regulation zone (CRZ) clearances.", "environmental": "Operates Asia's largest sea-water desalination plant for captive refinery industrial water, saving scarce municipal drinking water for Chennai city."},
        [0.18, 0.45, 0.35, 0.20, 0.60],
        {"threat_of_new_entrants": "Zero; building mega-refineries with coastal crude mooring requires thousands of crores in capex.", "bargaining_power_of_buyers": "Low; parent company IOCL markets 100% of CPCL's refined petroleum output.", "bargaining_power_of_suppliers": "Low; crude oil procured through IOCL's centralized global purchasing arm.", "threat_of_substitutes": "Low; petroleum products are essential for regional transport and road construction.", "competitive_rivalry": "Low; captive regional refining supplier for IOCL's southern distribution network."}
    ),
    (
        "Mangalore Refinery and Petrochemicals (MRPL)", "Oil, Gas, Refining & Petrochemicals",
        "domestic fuel consumers in Karnataka/Kerala and international export markets",
        "need high-specification transport fuels, polypropylene polymers, and aromatics refined from diverse and heavy sour crude oils",
        "MRPL Coastal Mega-Refinery & Polypropylene Polymers", "High-Complexity Coastal Refining & Petrochemicals",
        "operates a 15 MMTPA high-complexity coastal refinery in Mangaluru with an unmatched ability to process over 250 diverse global crude oil grades",
        [0.84, 0.92, 0.96, 0.92, 0.86, 0.70],
        {"political": "Subsidiary of ONGC; critical refining export gateway strategically located on the Arabian Sea maritime shipping lanes.", "economic": "Direct single-point mooring (SPM) berths handle very large crude carriers (VLCCs), delivering superior freight and crude sourcing margins.", "social": "Major driver of industrialization and port commerce at New Mangalore Port, providing direct livelihoods for thousands in coastal Karnataka.", "technological": "High-complexity delayed cokers, petrochemical fluidized catalytic cracking (PFCC), and modern polypropylene polymer units.", "legal": "BS-VI fuel standards, Karnataka State Pollution Control Board clearances, and international maritime fuel regulations.", "environmental": "Advanced zero-liquid discharge effluent treatment and energy-saving waste heat recovery steam generators."},
        [0.18, 0.45, 0.35, 0.20, 0.60],
        {"threat_of_new_entrants": "Zero; port-linked mega-refineries have insurmountable capital and environmental licensing barriers.", "bargaining_power_of_buyers": "Moderate; fuel marketed through OMCs domestically and auctioned in international commodity export tenders.", "bargaining_power_of_suppliers": "Low; parent ONGC and international crude producers under term contracts.", "threat_of_substitutes": "Low for essential transportation fuels and industrial polymers.", "competitive_rivalry": "Low to moderate; serves captive regional fuel markets and export lanes."}
    ),
    (
        "Aegis Logistics", "Oil, Gas, Refining & Petrochemicals",
        "oil marketing companies, chemical manufacturers, and liquefied petroleum gas (LPG) importers",
        "require specialized deep-water port terminal storage tanks, pressurized cryogenic LPG import terminals, and chemical logistics",
        "Port Liquid Chemical & Cryogenic LPG Terminals", "Port Liquid Storage & Cryogenic LPG Import Terminal Logistics",
        "handles over 25% of India's total LPG imports through an unrivaled network of deep-water port terminals at Mumbai, Pipavav, Haldia, Kandla, and Kochi",
        [0.80, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Strategic partner for the Ministry of Petroleum under the Pradhan Mantri Ujjwala Yojana, providing the port import capacity for cooking gas.", "economic": "Formed historic global joint venture with Royal Vopak (Netherlands); annuity-like throughput storage fees provide highly predictable cash flows.", "social": "Ensures that over 100 million Indian kitchens receive an uninterrupted supply of clean, imported cooking gas cylinders.", "technological": "Cryogenic static storage tanks operating at minus 42 deg C, high-speed automated pipeline loading racks, and computerized chemical manifold systems.", "legal": "Major Port Trust concessions, PESO explosive safety licenses, and coastal environmental approvals.", "environmental": "High-integrity double-containment cryogenic storage tanks preventing fugitive hydrocarbon emissions into marine ports."},
        [0.15, 0.42, 0.30, 0.18, 0.50],
        {"threat_of_new_entrants": "Very low; port land parcels with deep-water pipeline jetty connectivity are scarce and require decades of concessions.", "bargaining_power_of_buyers": "Low to moderate; oil companies (IOCL, BPCL, HPCL) require Aegis's specialized port berths to discharge imported gas tankers.", "bargaining_power_of_suppliers": "Low; cryogenic steel fabrication and pump equipment suppliers.", "threat_of_substitutes": "Low; physical maritime port terminals are non-substitutable for seaborne LPG and bulk chemical imports.", "competitive_rivalry": "Low to moderate; dominant leader in private third-party port liquid logistics ahead of Adani Ports."}
    ),
    (
        "Deep Industries", "Oil, Gas, Refining & Petrochemicals",
        "upstream oil and gas exploration and production operators (ONGC, Vedanta Cairn, Oil India)",
        "need specialized natural gas compression, gas dehydration, workover drilling rigs, and integrated surface production facilities",
        "Natural Gas Compression Services & Workover Rigs", "Oil & Gas Field Services & Gas Compression",
        "pioneered high-pressure natural gas compression on a charter-hire basis in India, holding over 50% market share in outsourced gas compression services",
        [0.76, 0.86, 0.92, 0.92, 0.84, 0.70],
        {"political": "Direct beneficiary of domestic oil and gas production maximization mandates and marginal field development policies.", "economic": "Long-term 3 to 5-year charter-hire service contracts provide steady EBITDA margins (>40%) with high asset utilization rates.", "social": "Increases natural gas flow from depleted mature wells, bringing domestic gas into city grids without flaring.", "technological": "High-pressure multi-stage reciprocating gas compressors, mobile gas dehydration units, and automated drilling workover rigs.", "legal": "Directorate General of Mines Safety (DGMS) certifications, PESO compliances, and upstream safety standards.", "environmental": "Gas compression captures low-pressure associated gas that would otherwise be flared into the atmosphere, saving millions of tons of emissions."},
        [0.22, 0.48, 0.40, 0.22, 0.58],
        {"threat_of_new_entrants": "Low to moderate; acquiring high-pressure gas compressor packages and building specialized field operating crews requires substantial capital.", "bargaining_power_of_buyers": "Moderate; upstream E&P operators negotiate charter hire rates through competitive tenders.", "bargaining_power_of_suppliers": "Moderate; specialized gas compressor engine manufacturers (Caterpillar, Ariel).", "threat_of_substitutes": "Low; natural gas must be compressed to high pressures (70-90 bar) to enter cross-country pipelines.", "competitive_rivalry": "Moderate; dominates domestic gas compression ahead of smaller regional contractors."}
    ),
    (
        "Gulf Oil Lubricants India", "Oil, Gas, Refining & Petrochemicals",
        "motorcyclists, commercial truck fleet operators, and industrial tractor owners",
        "demand long-drain, high-protection engine oils and specialized electric vehicle cooling fluids backed by iconic global sports brand trust",
        "Gulf Pride 4T Motorcycle Oil & Gulf Superfleet Truck Oil", "Automotive Engine Lubricants & Industrial Fluids",
        "stands as the fastest-growing lubricant brand in India, pioneering 10,000 km oil-drain intervals for two-wheelers with MS Dhoni brand endorsement",
        [0.68, 0.88, 0.94, 0.88, 0.82, 0.72],
        {"political": "Part of the Hinduja Group; compliant with BIS automotive oil standards and national circular plastic recycling mandates.", "economic": "Consistent outperformance with double-digit volume growth; expanding into fast-growing EV charging stations (invested in Indra Renewables and ElectreeFi).", "social": "Deep connect with truckers and bike riders through iconic 15-year brand ambassadorship with cricket legend Mahendra Singh Dhoni.", "technological": "Oxy-biturators preventing oil thickening under Indian summer heat, and specialized dielectric fluids for EV battery fast-charging.", "legal": "BIS quality compliance, weights and measures adherence, and trademark IP protection.", "environmental": "Eco-friendly recyclable lubricant containers and specialized low-viscosity fuels that boost vehicle fuel economy by 2%."},
        [0.28, 0.52, 0.40, 0.28, 0.72],
        {"threat_of_new_entrants": "Low to moderate; building a 80,000-retailer and workshop distribution network requires multi-year credit and distributor loyalty.", "bargaining_power_of_buyers": "Moderate; mechanics and consumers choose Gulf for extended drain intervals and engine smoothness.", "bargaining_power_of_suppliers": "Moderate; base oil raw materials sourced from global petrochemical refineries.", "threat_of_substitutes": "Moderate from Castrol India and public sector OMC lubricants.", "competitive_rivalry": "Intense rivalry with Castrol India, Motul, and IOCL SERVO."}
    ),
    (
        "Savita Oil Technologies", "Oil, Gas, Refining & Petrochemicals",
        "power transformer manufacturers (BHEL, Siemens), power utilities, and pharmaceutical cosmetic formulators",
        "require ultra-pure, high-dielectric transformer insulating oils and pharmacopeia-grade white mineral oils and petroleum jellies",
        "SAVOL High-Voltage Transformer Oil & White Mineral Oils", "Specialty Petroleum Oils, Transformer Fluids & Petroleum Specialties",
        "is India's premier manufacturer of transformer insulating oils and petroleum specialties, exporting high-voltage dielectric fluids to over 75 countries",
        [0.72, 0.88, 0.94, 0.90, 0.84, 0.74],
        {"political": "Critical component supplier to national power transmission grid projects and transformer manufacturing under Make in India.", "economic": "Debt-free balance sheet with consistent profitability, benefiting from multi-year capex expansions in the Indian power transmission sector.", "social": "Protects high-voltage electrical grid transformers from overheating and catastrophic short-circuit explosions.", "technological": "Proprietary hydro-treating and refining processes yielding transformer oils with extreme dielectric breakdown voltages and oxidation resistance.", "legal": "IEC and Bureau of Indian Standards (IS 335) transformer oil specifications; Indian Pharmacopoeia compliance for white oils.", "environmental": "Pioneered bio-degradable synthetic ester-based transformer fluids with low fire risk and zero soil toxicity."},
        [0.24, 0.48, 0.38, 0.24, 0.62],
        {"threat_of_new_entrants": "Low; manufacturing specialty transformer oils requires rigorous type-testing approval from national testing laboratories (CPRI).", "bargaining_power_of_buyers": "Moderate; transformer OEMs (ABB, Siemens, BHEL) mandate stringent chemical purity and viscosity tests.", "bargaining_power_of_suppliers": "Moderate; specialized naphthenic and paraffinic base oil stocks.", "threat_of_substitutes": "Low; high-voltage liquid transformers require specialized dielectric cooling fluids.", "competitive_rivalry": "Moderate; competes with Apar Industries in transformer oils."}
    ),
    (
        "Confidence Petroleum India", "Oil, Gas, Refining & Petrochemicals",
        "commercial restaurants, industrial kitchens, auto-rickshaw drivers, and LPG cylinder marketing companies",
        "need convenient, lightweight commercial LPG cylinder deliveries and economical Auto-LPG refueling stations across major highways",
        "GoGas Auto-LPG & Composite Lightweight LPG Cylinders", "Auto-LPG Dispensing Stations & Composite Gas Cylinders",
        "operates India's largest private network of Auto-LPG dispensing stations (200+ stations) and pioneered rust-free, translucent composite LPG cylinders",
        [0.76, 0.86, 0.92, 0.88, 0.82, 0.75],
        {"political": "Direct beneficiary of national alternative clean transport fuel policies and PESO approval for composite gas cylinders.", "economic": "Integrated business model: in-house LPG cylinder manufacturing facilities supply both internal GoGas retail operations and public sector OMCs.", "social": "GoGas Auto-LPG offers auto-rickshaw and commercial fleet drivers a 40% fuel cost saving compared to petrol.", "technological": "High-strength fiberglass composite cylinder winding technology that is 100% explosion-proof and 50% lighter than heavy steel cylinders.", "legal": "PESO statutory approvals for LPG bottling plants, cylinder manufacturing licenses, and retail auto-LPG dispensing safety.", "environmental": "Auto-LPG produces 20% less CO2 than petrol and virtually zero particulate matter; composite cylinders eliminate steel rust scrap."},
        [0.26, 0.50, 0.38, 0.28, 0.68],
        {"threat_of_new_entrants": "Low to moderate; establishing LPG bottling plants and obtaining PESO explosive licenses requires complex regulatory approvals.", "bargaining_power_of_buyers": "Moderate; commercial kitchens and vehicle drivers look for competitive cylinder gas pricing.", "bargaining_power_of_suppliers": "Moderate; bulk commercial LPG procured from refineries and import terminals.", "threat_of_substitutes": "Moderate from CNG vehicles and piped natural gas.", "competitive_rivalry": "Moderate; dominates the private auto-LPG and cylinder manufacturing space."}
    ),
    (
        "Adani Total Gas", "Oil, Gas, Refining & Petrochemicals",
        "industrial estates, transport fleets, and domestic households across 33 authorized geographical areas in 14 states",
        "require clean piped natural gas for manufacturing and cooking, integrated with an expanding network of CNG stations and EV charging hubs",
        "City Gas Distribution (CNG/PNG) & EV Charging Infrastructure", "Multi-State City Gas Distribution & Clean Fuel Utility",
        "is developing city gas infrastructure across 33 geographical areas covering 10% of India's population, backed by global energy giant TotalEnergies",
        [0.82, 0.92, 0.96, 0.92, 0.86, 0.85],
        {"political": "Joint venture between Adani Group and France's TotalEnergies; major driver of the Prime Minister's vision for a gas-based economy.", "economic": "Rapid infrastructure ramp-up; long-term minimum work program commitments unlocking high operating cash flows as pipeline networks mature.", "social": "Brings clean cooking gas directly into kitchens and clean CNG into commercial fleets across hundreds of towns in northern and western India.", "technological": "Smart city gas metering, LNG-for-transport refueling stations for long-haul trucks, and integrated EV smart charging network.", "legal": "PNGRB regulatory authorization, municipal right-of-way permissions, and PESO safety compliances.", "environmental": "Displaces thousands of tons of heavy furnace oil, coal, and diesel with clean natural gas; piloting biogas (CBG) blending."},
        [0.18, 0.45, 0.38, 0.22, 0.58],
        {"threat_of_new_entrants": "Zero in authorized geographical areas due to PNGRB's multi-decade network infrastructure exclusivity.", "bargaining_power_of_buyers": "Moderate; industrial buyers evaluate alternative fuel costs, but households enjoy locked convenience.", "bargaining_power_of_suppliers": "Moderate; reliant on central APM gas allocations and international LNG contracts under TotalEnergies platform.", "threat_of_substitutes": "Moderate from industrial LPG and electric mobility in the long run.", "competitive_rivalry": "Low inside authorized districts; competes with IGL and Gujarat Gas for new city licenses."}
    )
]

for item in sector15_data:
    add_c(*item)

print(f"Sector 15 added: {len(sector15_data)} companies. Total in Part 3A: {len(part3_a)}")

# Save to scratch/part3_a.json
out_path = Path(__file__).parent / "part3_a.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(part3_a, f, indent=2)

print(f"SUCCESS: Saved {len(part3_a)} companies to {out_path}")
