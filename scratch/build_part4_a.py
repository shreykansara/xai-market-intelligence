"""
Omniscope AI - Part 4A Generator
Builds Sectors 19, 20, 21 (62 companies):
- Sector 19: Paints, Adhesives & Home Building Materials (20 companies)
- Sector 20: Logistics, Freight & Supply Chain Tech (20 companies)
- Sector 21: Aviation, Travel, Hospitality & Dining (22 companies)
Outputs to scratch/part4_a.json
"""
import json
from pathlib import Path

part4_a = []

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    part4_a.append({
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
# SECTOR 19: Paints, Adhesives & Home Building Materials (20 companies)
# ==============================================================================
sector19_data = [
    (
        "Asian Paints", "Paints, Adhesives & Home Building Materials",
        "homeowners, painting contractors, architects, and interior designers across India",
        "need vibrant, washable, and long-lasting interior/exterior paints, waterproof coatings, and comprehensive home painting services",
        "Royale Luxury Emulsion, Apex Ultima & Beautiful Homes Service", "Architectural Decorative Coatings & Home Decor Ecosystem",
        "rules Indian decorative paints with over 50% market share, delivering automated color-tinting machines to 75,000+ dealers and guaranteed 4-hour replenishment",
        [0.72, 0.94, 0.96, 0.95, 0.86, 0.78],
        {"political": "Complies with Bureau of Indian Standards (BIS) lead-free paint regulations and VOC limits enforced by the Central Pollution Control Board.", "economic": "Generates over Rs 35,000 Cr in revenue with industry-leading ROCE (>35%); legendary supply chain bypasses wholesale middlemen completely.", "social": "The sacred ritual of painting one's home during Diwali is synonymous with Asian Paints; 'Har Ghar Kuch Kehta Hai' is an immortal cultural slogan.", "technological": "Pioneered early mainframe computing in India; installed computerized tinting machines at 75,000 retail dealers; AI home visualization tools.", "legal": "Competition Commission of India (CCI) scrutiny over dealer exclusivity, FSSAI/BIS compliance, and Legal Metrology Act.", "environmental": "Eliminated heavy metals and added lead from all decorative paints; 100% water-neutral manufacturing plants and extensive solar power."},
        [0.22, 0.45, 0.38, 0.22, 0.70],
        {"threat_of_new_entrants": "Low; matching Asian Paints' 75,000-dealer computerized tinting machine network and twice-a-day stock replenishment is a massive barrier.", "bargaining_power_of_buyers": "Moderate; homeowners follow professional painter recommendations, who are fiercely loyal to Asian Paints Master Painter programs.", "bargaining_power_of_suppliers": "Moderate; titanium dioxide, phthalic anhydride, and crude oil monomer inputs fluctuate with global chemical cycles.", "threat_of_substitutes": "Low; decorative paint has no substitute for home beautification and wall protection.", "competitive_rivalry": "Intense rivalry with Berger Paints, Kansai Nerolac, and new entrant Birla Opus (Grasim)."}
    ),
    (
        "Berger Paints India", "Paints, Adhesives & Home Building Materials",
        "homeowners, civil contractors, and industrial manufacturing clients",
        "demand weather-resistant exterior wall coatings, dust-resistant luxury interior finishes, and fast, dust-free mechanized painting services",
        "Silk Glamor Interior Emulsion & WeatherCoat Long Life Exterior Paint", "Decorative Wall Coatings & Mechanized Express Painting",
        "stands as India's #2 paint company, pioneering 'Express Painting' with automated vacuum sanding and high-durability silicon exterior paints",
        [0.70, 0.92, 0.96, 0.92, 0.86, 0.78],
        {"political": "Supports green building initiatives; compliant with BIS lead-free paints and environmental VOC emission limits.", "economic": "Consistent, high-margin compounder with strong presence in Eastern and Northern India; strong growth in protective industrial coatings.", "social": "Pioneered dust-free, hassle-free painting for families with Express Painting, eliminating the mess and toxic dust of manual wall sanding.", "technological": "PU-enamel cross-linking technology, automated mechanized sanding tools with dust extractors, and automated paint batching in mega-plants.", "legal": "BIS certification (IS 15489), consumer safety regulations, and trademark IP protection.", "environmental": "Green Pro certified paints with ultra-low VOCs, water-based enamel formulations, and industrial water recycling."},
        [0.25, 0.48, 0.38, 0.22, 0.72],
        {"threat_of_new_entrants": "Low to moderate; dealer color machine entrenchment and painter loyalty create formidable moats.", "bargaining_power_of_buyers": "Moderate; consumers cross-shop Asian Paints and Berger, but value Berger's exterior waterproofing warranties.", "bargaining_power_of_suppliers": "Moderate; imported titanium dioxide and emulsion polymer resins.", "threat_of_substitutes": "Low for wall coatings.", "competitive_rivalry": "High with Asian Paints, Kansai Nerolac, and Birla Opus."}
    ),
    (
        "Kansai Nerolac Paints", "Paints, Adhesives & Home Building Materials",
        "automotive OEMs (Maruti Suzuki, Tata Motors), two-wheeler makers, and health-conscious home dwellers",
        "require precision automotive electrostatic coatings, corrosion-resistant chassis primers, and non-toxic, healthy interior wall paints",
        "Automotive OEM High-Solid Coatings & Beauty Gold Decorative Paints", "Automotive Industrial Coatings & Eco-Friendly Decorative Paints",
        "dominates Indian automotive coatings with over 55% market share, painting every second car rolling off Indian automotive assembly lines",
        [0.72, 0.90, 0.95, 0.94, 0.86, 0.80],
        {"political": "Strategic partner for automotive manufacturing under Make in India; complies with strict industrial environmental emission caps.", "economic": "Sticky automotive OEM contracts provide high volume baseload; expanding decorative paint retail presence across western and southern India.", "social": "Pioneered lead-free and zero-VOC 'Healthy Home' paints in India, endorsed by Bollywood superstars for family health safety.", "technological": "Cathodic electro-deposition (CED) tank coatings for automotive bodies, water-borne metallic basecoats, and nano-silica scratch-resistant clearcoats.", "legal": "Stringent automotive supplier quality certifications (IATF 16949), BIS standards, and environmental consent to operate.", "environmental": "Pioneered water-based automotive paints cutting volatile solvent emissions by over 60%; zero-liquid discharge manufacturing."},
        [0.22, 0.52, 0.40, 0.20, 0.68],
        {"threat_of_new_entrants": "Low in automotive OEM coatings due to rigorous 3-year automotive paint-line validation; moderate in decorative paints.", "bargaining_power_of_buyers": "High in automotive (Maruti, Hyundai negotiate volume rates); moderate in retail decorative.", "bargaining_power_of_suppliers": "Moderate; specialty acrylic polyols, isocyanate hardeners, and titanium dioxide.", "threat_of_substitutes": "Low; electro-deposition coating is mandatory for automotive corrosion resistance.", "competitive_rivalry": "High with Asian Paints and Berger Paints in retail; Akzo Nobel in industrial."}
    ),
    (
        "Pidilite Industries", "Paints, Adhesives & Home Building Materials",
        "carpenters, plumbers, civil construction contractors, students, and home DIY users",
        "need instant, unbreakable bonding adhesives, waterproof repair sealants, and comprehensive building structural waterproofing",
        "Fevicol Adhesive, Fevikwik, M-Seal & Dr. Fixit Waterproofing", "Consumer Adhesives, Sealants & Construction Chemicals",
        "embodies 'The Ultimate Bond' (Fevicol) with near-monopoly market share (70%+), forming an indelible cultural synonym for bonding in India",
        [0.70, 0.94, 0.98, 0.92, 0.86, 0.80],
        {"political": "Supports construction skill development; key partner in national building waterproofing guidelines under Bureau of Indian Standards.", "economic": "Phenomenal economic moat; pricing power enables Pidilite to pass raw material vinyl acetate monomer (VAM) price hikes directly to consumers.", "social": "Fevicol is deeply embedded in Indian pop culture and Bollywood dialogue; built an unbreakable direct bond with millions of Indian carpenters via Fevicol Champions Club.", "technological": "Synthetic resin emulsion polymer chemistry, instant cyanoacrylate bonding (Fevikwik), and liquid polyurethane waterproofing elastomeric membranes (Dr. Fixit).", "legal": "Strict trademark enforcement protecting Fevicol, M-Seal, and Fevikwik against counterfeit local glue makers.", "environmental": "Water-based adhesives with zero hazardous phthalates or toxic volatile solvent emissions; certified green building construction chemicals."},
        [0.15, 0.40, 0.35, 0.18, 0.50],
        {"threat_of_new_entrants": "Practically impossible; Fevicol's generational carpenter emotional loyalty and retail distribution across 200,000+ hardware shops is unassailable.", "bargaining_power_of_buyers": "Low; adhesive represents <2% of furniture making cost, so carpenters refuse to risk expensive wood with any other glue.", "bargaining_power_of_suppliers": "Moderate; vinyl acetate monomer (VAM) is an imported chemical commodity.", "threat_of_substitutes": "Low; adhesive and structural sealants are indispensable.", "competitive_rivalry": "Low to moderate; undisputed domestic monopoly in consumer adhesives."}
    ),
    (
        "Astral Pipes", "Paints, Adhesives & Home Building Materials",
        "plumbers, real estate developers, industrial chemical plants, and municipal water authorities",
        "require corrosion-free, heat-resistant hot and cold water piping, silent drainage, and underground stormwater transport",
        "Astral CPVC Pro Plumbing Pipes & Silencio Soundproof Drainage", "High-Performance Chlorinated Polyvinyl Chloride (CPVC) Piping Systems",
        "introduced CPVC plumbing pipes to India, completely replacing rust-prone galvanized iron pipes with unbreakable, chemical-resistant polymer plumbing",
        [0.72, 0.92, 0.96, 0.94, 0.85, 0.78],
        {"political": "Direct beneficiary of National Real Estate boom, Smart Cities mission, and Jal Jeevan Mission rural piped water rollout.", "economic": "Consistent, high-margin compounder (ROCE >25%); expanded successfully into adhesives (Bondtite) and sanitaryware/faucets.", "social": "Transformed Indian residential plumbing safety: eliminated rusty brown drinking water caused by corroding iron pipes in millions of homes.", "technological": "Proprietary Lubrizol CPVC compound licensing, automated twin-screw extrusion lines, and acoustic soundproof multi-layer mineral-reinforced drainage pipes.", "legal": "BIS certification (IS 15778), ASTM D2846 international standards, and NSF-61 drinking water toxicity certifications.", "environmental": "Lead-free CPVC formulation safe for potable water, 100% recyclable polymer scrap, and energy-efficient pipe extrusion."},
        [0.22, 0.48, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; building deep plumber trust, stocking 35,000 SKUs, and maintaining nationwide distributor credit creates a heavy barrier.", "bargaining_power_of_buyers": "Moderate; plumbers and builders demand Astral for reliable leak-free solvent cement joints.", "bargaining_power_of_suppliers": "Moderate; imported CPVC raw resin compound from Lubrizol (USA) and Sekisui (Japan).", "threat_of_substitutes": "Low; CPVC and PVC are the universal global plumbing standards.", "competitive_rivalry": "High with Supreme Industries, Finolex Industries, and Prince Pipes."}
    ),
    (
        "Supreme Industries", "Paints, Adhesives & Home Building Materials",
        "farmers, building contractors, municipal sewage boards, and industrial packaging users",
        "need high-volume, durable agricultural PVC pipes, rotomolded water storage tanks, composite LPG cylinders, and molded plastic furniture",
        "Supreme Agricultural & SWR Drainage Pipes, SILTANK Water Tanks", "Plastic Piping Systems, Molded Furniture & Industrial Plastics",
        "is India's largest plastics processor (handling over 500,000 MT annually), offering the country's most comprehensive 32-category plastic product portfolio",
        [0.72, 0.92, 0.96, 0.92, 0.85, 0.76],
        {"political": "Major supplier for national agricultural irrigation schemes (PM Krishi Sinchayee Yojana) and rural piped drinking water missions.", "economic": "Unmatched operational scale gives rock-bottom polymer resin procurement costs, sustaining high return on equity (>22%) and zero net debt.", "social": "Empowers millions of Indian smallholder farmers with durable subsurface drip and sprinkler piping, preventing canal water seepage losses.", "technological": "Automated high-capacity plastic extrusion lines, rotomolding for multi-layer insulated water tanks, and advanced composite gas cylinder winding.", "legal": "BIS pipe certifications (IS 4985), municipal drainage approvals, and statutory factory labor compliances.", "environmental": "100% recyclable thermoplastic processing, lead-free PVC piping lines, and energy-efficient electric injection molding machines."},
        [0.22, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; matching Supreme's 28 mega-processing plants, 500,000-ton polymer purchasing scale, and national dealer reach is prohibitive.", "bargaining_power_of_buyers": "Moderate; farmers and contractors compare pipe per-meter pricing, but trust Supreme for burst resistance.", "bargaining_power_of_suppliers": "Moderate; PVC resin prices fluctuate with international crude oil and ethylene feedstocks (Reliance, Chemplast).", "threat_of_substitutes": "Low for essential plumbing and agricultural irrigation.", "competitive_rivalry": "Intense competition with Astral, Finolex, and Ashirvad Pipes."}
    ),
    (
        "Finolex Cables", "Paints, Adhesives & Home Building Materials",
        "electricians, homebuilders, industrial machinery fabricators, and agricultural farmers",
        "need 100% pure copper electrical house wires, flame-retardant electrical cables, and agricultural submersible cables that prevent electrical fires",
        "Flame Retardant (FR) Electrical House Wires & Submersible Cables", "Flame-Retardant Electrical Wires, Power Cables & Switchgear",
        "is India's premier household electrical wire brand with 5 decades of trust, pioneering 100% electrolytic pure copper wires that do not catch fire",
        [0.70, 0.92, 0.96, 0.90, 0.86, 0.78],
        {"political": "Complies with Central Electricity Authority (CEA) home electrical safety guidelines and BIS wire standards.", "economic": "Debt-free balance sheet with large cash reserves and high brand equity, expanding into fast-growing switches, fans, and smart home lighting.", "social": "The trusted default wire choice for Indian electricians; protects millions of families from lethal short-circuit electrical home fires.", "technological": "In-house copper rod drawing, continuous tandem wire insulation extruders, and computerized spark testing of 100% of wire length.", "legal": "BIS certification (IS 694), fire-retardant low-smoke (FRLS) toxicity testing, and consumer protection trade compliances.", "environmental": "Halogen-free flame retardant (HFFR) wire compounds that emit zero toxic acidic gases during accidental building fires."},
        [0.24, 0.48, 0.40, 0.24, 0.70],
        {"threat_of_new_entrants": "Low; building Finolex's 50-year electrical contractor trust and 150,000-retailer hardware channel takes decades.", "bargaining_power_of_buyers": "Moderate; homeowners follow licensed electrician recommendations for wiring safety.", "bargaining_power_of_suppliers": "Moderate to high; copper cathode raw materials traded at LME benchmarks.", "threat_of_substitutes": "Low; copper wiring is mandatory for indoor electrical conduction.", "competitive_rivalry": "High with Polycab India, Havells, and KEI Industries."}
    ),
    (
        "Polycab India", "Paints, Adhesives & Home Building Materials",
        "electrical contractors, industrial mega-plants, infrastructure developers, and home dwellers",
        "require heavy-duty industrial power cables, smart home automation wires, energy-efficient ceiling fans, and LED lighting solutions",
        "Polycab Green Wires, Extra High Voltage Power Cables & FMEG Appliances", "Wires, Power Cables & Fast-Moving Electrical Goods (FMEG)",
        "stands as India's #1 wire and cable manufacturer with over 25% organized market share, distributing through 4,300+ authorized dealers and 200,000+ retailers",
        [0.72, 0.94, 0.96, 0.94, 0.86, 0.78],
        {"political": "Major supplier for national infrastructure electrification, metro railways, and rural grid revamp schemes (RDSS).", "economic": "Revenue exceeding Rs 18,000 Cr with industry-leading cash generation; unmatched backward integration from copper cathode to finished cable.", "social": "Powers India's urban homes and modern infrastructure with reliable, energy-saving electrical conduction and appliances.", "technological": "Electron-beam (E-beam) cross-linked polymer insulation technology, robotic cable spooling, and smart IoT-connected ceiling fans.", "legal": "BIS certifications, IEC international standards, and corporate governance compliance.", "environmental": "Solar-powered manufacturing plants in Halol, Gujarat; lead-free PVC insulation and recyclable copper scrap recovery."},
        [0.22, 0.48, 0.38, 0.22, 0.70],
        {"threat_of_new_entrants": "Low; matching Polycab's 25 mega-manufacturing plants and 200,000-retailer distribution reach requires immense capital.", "bargaining_power_of_buyers": "Moderate; institutional infrastructure clients negotiate bulk volume discounts.", "bargaining_power_of_suppliers": "Moderate; copper and aluminum base metals sourced at international spot prices.", "threat_of_substitutes": "Low for essential electrical transmission wires.", "competitive_rivalry": "High with Havells India, KEI Industries, and Finolex Cables."}
    ),
    (
        "KEI Industries", "Paints, Adhesives & Home Building Materials",
        "power transmission utilities, metro rail networks, refineries, and renewable energy developers",
        "need Extra High Voltage (EHV) underground power cables up to 400 kV, specialized instrumentation cables, and turnkey EPC substation cabling",
        "Extra High Voltage (EHV) Power Cables & Solar DC Cables", "Specialized Heavy Power Cables & Turnkey Cable EPC",
        "is India's premier manufacturer of Extra High Voltage (EHV) power cables up to 400 kV, holding technological leadership in critical underground power transmission",
        [0.75, 0.92, 0.95, 0.94, 0.86, 0.75],
        {"political": "Key beneficiary of urban underground cabling tenders and renewable energy evacuation corridors under Make in India.", "economic": "High-margin specialized EHV and export cable sales drive superior return on capital (ROCE >28%) and a debt-free balance sheet.", "social": "Replaces dangerous overhead tangled city power lines with safe, invisible underground high-voltage power cable networks.", "technological": "Triple-extrusion dry-curing vulcanization lines for 400 kV XLPE cables, specialized electron-beam radiation cross-linking.", "legal": "Type-tested and certified by international testing laboratories (KEMA Netherlands, CPRI India), complying with IEC standards.", "environmental": "XLPE insulated cables eliminate messy oil-filled paper cable leaks, protecting urban soil and groundwater aquifers."},
        [0.22, 0.48, 0.40, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; manufacturing 400 kV EHV cables requires specialized imported catenary lines and multi-year KEMA type-test approvals.", "bargaining_power_of_buyers": "Moderate; state utilities and solar developers negotiate through competitive bids.", "bargaining_power_of_suppliers": "Moderate; electrolytic copper and aluminum grade wire rods.", "threat_of_substitutes": "Low; underground EHV cables are mandatory in congested urban corridors.", "competitive_rivalry": "Moderate; competes with Polycab India and Universal Cables in high-voltage segments."}
    ),
    (
        "Havells India", "Paints, Adhesives & Home Building Materials",
        "modern urban homeowners, architects, corporate offices, and premium consumers",
        "demand stylish, smart connected electrical appliances: Crabtree luxury switches, Lloyd heavy-duty air conditioners, and premium BLDC fans",
        "Crabtree Switches, Lloyd Inverter ACs & Stealth BLDC Fans", "Fast-Moving Electrical Goods (FMEG) & Consumer Appliances",
        "is India's premier consumer electrical brand with 90%+ in-house manufacturing, dominating switches, switchgear, Lloyd air conditioners, and premium lighting",
        [0.72, 0.92, 0.96, 0.95, 0.86, 0.80],
        {"political": "Supports domestic manufacturing under Make in India; complies with Bureau of Energy Efficiency (BEE) mandatory star-rating norms.", "economic": "Powerhouse consumer brand generating over Rs 18,000 Cr in revenue with pristine debt-free balance sheet and high return on capital.", "social": "Elevates everyday home living with elegant, aesthetically pleasing modular switches, whisper-quiet fans, and smart home lighting.", "technological": "Smart IoT-enabled appliances powered by Havells Sync app, rapid 53 deg C high-ambient cooling in Lloyd ACs, and silent BLDC motor engineering.", "legal": "BIS electrical safety certifications, BEE energy conservation compliance, and consumer protection warranties.", "environmental": "Pioneered energy-saving 5-star BLDC fans cutting domestic electricity consumption by over 50%; rooftop solar power across factories."},
        [0.24, 0.50, 0.38, 0.25, 0.72],
        {"threat_of_new_entrants": "Low to moderate; replicating Havells' 15,000-retailer network, iconic brand equity, and massive captive manufacturing is prohibitive.", "bargaining_power_of_buyers": "Moderate; consumers cross-shop appliances, but trust Havells and Crabtree for luxury aesthetics and durability.", "bargaining_power_of_suppliers": "Low; 90%+ in-house manufacturing provides extreme control over component supply.", "threat_of_substitutes": "Moderate from multinational consumer electronics brands (Samsung, LG).", "competitive_rivalry": "High with Crompton Greaves, Voltas, and Polycab."}
    ),
    (
        "Crompton Greaves Consumer Electricals", "Paints, Adhesives & Home Building Materials",
        "families, homeowners, and agricultural farmers across India",
        "need energy-saving, silent ceiling fans, reliable domestic and agricultural water pumps, and long-lasting LED home lighting",
        "Energion BLDC Ceiling Fans, Mini Master Water Pumps & LED Lighting", "Consumer Electrical Appliances, Fans & Pumping Systems",
        "leads India's fan industry with over 85 years of brand trust, pioneering silent, 5-star energy-saving BLDC ceiling fans and reliable water pumps",
        [0.70, 0.92, 0.96, 0.92, 0.86, 0.78],
        {"political": "Direct beneficiary of BEE mandatory energy labeling standards for ceiling fans and national rural water pumping missions.", "economic": "Consistent dividend payer with high return on invested capital; acquired Butterfly Gandhimathi to expand into South Indian kitchen appliances.", "social": "An integral fixture in hundreds of millions of Indian living rooms and bedrooms, providing relief from scorching summer heat.", "technological": "Proprietary ActivBLDC motor technology cutting fan energy consumption from 75W to 28W; anti-dust surface coating preventing wall grime.", "legal": "BIS certifications, BEE star labeling compliance, and Legal Metrology standards.", "environmental": "Energion BLDC fans save millions of units of electricity annually across Indian households, directly reducing coal power carbon emissions."},
        [0.24, 0.52, 0.38, 0.25, 0.72],
        {"threat_of_new_entrants": "Moderate; assembling basic ceiling fans is simple, but building Crompton's 100,000-retailer brand trust is very hard.", "bargaining_power_of_buyers": "Moderate; consumers evaluate electricity bill savings and noise levels when purchasing fans.", "bargaining_power_of_suppliers": "Low to moderate; in-house motor winding, stamping, and plastic molding.", "threat_of_substitutes": "Moderate from air conditioners and air coolers.", "competitive_rivalry": "Intense rivalry with Havells, Orient Electric, and Atomberg Technologies."}
    ),
    (
        "Voltas (Tata Group)", "Paints, Adhesives & Home Building Materials",
        "urban households, retail commercial shops, and large-scale infrastructure projects across India and the Middle East",
        "need powerful, energy-efficient room air conditioners engineered for extreme 50 deg C Indian summer heat, and heavy commercial MEP chillers",
        "Voltas Maha-Adjustable Inverter ACs & Commercial MEP Cooling", "Room Air Conditioners & Commercial Electro-Mechanical Projects (MEP)",
        "stands as India's undisputed #1 room air conditioner brand with over 20% market share, having cooled Indian homes and prestigious global landmarks (Burj Khalifa)",
        [0.72, 0.92, 0.96, 0.94, 0.86, 0.78],
        {"political": "Key beneficiary of the Production Linked Incentive (PLI) for White Goods (AC components); backed by the trusted Tata Group.", "economic": "Dominant market leader in room ACs with massive summer cash generation; joint venture with Arcelik (Voltas Beko) expanding into home appliances.", "social": "The quintessential Indian air conditioner brand, celebrated for cooling homes even during severe 50-degree North Indian heatwaves.", "technological": "High-ambient inverter rotary compressors operating at 52 deg C, eco-friendly R32 refrigerant, and customizable multi-tonnage cooling modes.", "legal": "BEE mandatory star ratings, Ozone Depleting Substances (ODS) phase-out regulations, and BIS safety standards.", "environmental": "Using zero-ozone-depletion R32 refrigerant and high-efficiency inverter heat pumps cutting domestic energy consumption."},
        [0.24, 0.52, 0.40, 0.22, 0.72],
        {"threat_of_new_entrants": "Low to moderate; establishing national air conditioner service networks and compressor warranties requires substantial infrastructure.", "bargaining_power_of_buyers": "Moderate; summer heat makes ACs non-discretionary necessities, but buyers compare star ratings and prices across brands.", "bargaining_power_of_suppliers": "Moderate; air conditioner compressors (Highly, GMCC) and copper tubing.", "threat_of_substitutes": "Moderate from desert air coolers in dry northern states.", "competitive_rivalry": "High with Blue Star, Daikin India, and Lloyd (Havells)."}
    ),
    (
        "Blue Star", "Paints, Adhesives & Home Building Materials",
        "commercial IT parks, pharmaceutical vaccine cold rooms, hospital ICUs, and premium homeowners",
        "require precision, heavy-duty central HVAC chillers, commercial deep freezers, pharmaceutical cold storage, and premium room ACs",
        "Commercial VRF Systems, Vaccine Cold Rooms & Premium Inverter ACs", "Commercial Air Conditioning & Cold Chain Refrigeration",
        "leads India's commercial air conditioning and cold chain refrigeration sector, cooling 1 out of every 3 commercial buildings and storing national vaccines",
        [0.72, 0.92, 0.96, 0.94, 0.86, 0.80],
        {"political": "Strategic partner for national pharmaceutical cold-chains, vaccine storage missions, and mega food park cold logistics.", "economic": "Dual engine: high-margin commercial refrigeration and VRF systems balanced by fast-growing residential inverter room AC sales.", "social": "Crucial national infrastructure: safeguards life-saving pediatric vaccines and food perishables with precision temperature cold rooms.", "technological": "Variable Refrigerant Flow (VRF) Gen-5 systems, oil-free magnetic levitation centrifugal chillers, and remote IoT chiller plant telemetry.", "legal": "BEE energy standards, Montreal Protocol hydrofluorocarbon phase-down compliances, and factory safety certifications.", "environmental": "Pioneered eco-friendly hydrocarbon and hydrofluoroolefin (HFO) chillers with near-zero Global Warming Potential (GWP)."},
        [0.22, 0.50, 0.40, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; building commercial VRF engineering expertise, chiller manufacturing, and 24/7 service technicians is a steep barrier.", "bargaining_power_of_buyers": "Moderate; commercial MEP clients demand verified uptime SLAs for corporate data centers and hospitals.", "bargaining_power_of_suppliers": "Moderate; heavy scroll and screw compressor OEMs (Danfoss, Copeland).", "threat_of_substitutes": "Low; precision temperature and humidity control is mandatory for hospitals and data centers.", "competitive_rivalry": "High with Voltas and Daikin in room ACs; Carrier and Trane in commercial chillers."}
    ),
    (
        "Symphony Limited", "Paints, Adhesives & Home Building Materials",
        "budget-conscious households, dry-climate families, and industrial factory floor managers",
        "need powerful, ultra-low-electricity cooling that works effectively in hot, dry Indian summers at 1/10th the running cost of air conditioning",
        "Symphony Diet, Touch & Large-Scale Industrial Evaporative Air Coolers", "Evaporative Air Coolers & Industrial Climate Control",
        "is the world's largest manufacturer of evaporative air coolers, operating in 60+ countries with patented engineering that cools rooms using mere 100W of power",
        [0.68, 0.88, 0.94, 0.88, 0.82, 0.85],
        {"political": "Promotes natural, low-power evaporative cooling aligned with national energy efficiency and sustainable cooling action plans.", "economic": "Asset-light outsourced manufacturing model produces phenomenal return on equity (>30%) and a debt-free balance sheet.", "social": "Provides affordable, clean cooling to tens of millions of working-class families who cannot afford expensive air conditioner power bills.", "technological": "High-efficiency honeycomb cooling pads, i-Pure multi-stage air purification filters, and energy-saving BLDC cooler fan motors.", "legal": "BIS quality standards, international CE marks, and consumer protection warranties.", "environmental": "Evaporative cooling consumes 90% less electricity than air conditioning, utilizes 100% natural water evaporation, and uses zero chemical refrigerants."},
        [0.25, 0.55, 0.38, 0.25, 0.65],
        {"threat_of_new_entrants": "Moderate; unorganized sheet-metal cooler makers exist locally, but lack Symphony's patented aesthetic design and national service network.", "bargaining_power_of_buyers": "Moderate; consumers buy coolers as an economical summer relief option and compare prices.", "bargaining_power_of_suppliers": "Low; asset-light contract manufacturing partners produce exclusively to Symphony's molds.", "threat_of_substitutes": "Moderate from entry-level split ACs and ceiling fans.", "competitive_rivalry": "Moderate; undisputed organized market leader ahead of Bajaj Electricals and Kenstar."}
    ),
    (
        "Kajaria Ceramics", "Paints, Adhesives & Home Building Materials",
        "homeowners, architects, interior designers, and commercial builders across India",
        "need high-durability, stain-resistant glazed vitrified floor tiles, designer ceramic wall tiles, and large-format porcelain slabs",
        "Kajaria Eternity Glazed Vitrified Tiles & Large-Format Porcelain Slabs", "Ceramic, Polished Vitrified & Large-Format Glazed Porcelain Tiles",
        "stands as India's #1 tile manufacturer and the 7th largest globally, operating 8 mega-plants with 3,000+ exquisite designs and zero-scratch durability",
        [0.70, 0.92, 0.96, 0.92, 0.86, 0.78],
        {"political": "Key beneficiary of anti-dumping actions on cheap Chinese ceramic imports and national real estate urban renewal.", "economic": "Consistent financial outperformance; generates highest operating margins in the tile sector with an expansive network of 1,800+ exclusive dealer showrooms.", "social": "The definitive synonym for stylish, durable flooring in India; 'Desh Ki Mitti Se Bani Tile Se Desh Ko Banate Hain' advertising resonance.", "technological": "Imported Sacmi continuous hydraulic presses, high-resolution digital ceramic inkjet printers, and 1200x2400mm giant porcelain slab lines.", "legal": "BIS tile quality certifications (IS 15622), environmental state pollution control clearances, and Legal Metrology compliance.", "environmental": "Clean natural gas fired kilns, 100% recycling of ceramic tile scrap into raw body formulations, and solar rooftop plants."},
        [0.24, 0.50, 0.38, 0.25, 0.70],
        {"threat_of_new_entrants": "Low to moderate; local Morbi factories make tiles, but replicating Kajaria's pan-India brand equity and showroom network is formidable.", "bargaining_power_of_buyers": "Moderate; homeowners and architects select Kajaria for zero edge-chipping and design consistency.", "bargaining_power_of_suppliers": "Moderate; natural gas fuel costs and imported ceramic glazes/frits.", "threat_of_substitutes": "Moderate from natural Italian marble and granite.", "competitive_rivalry": "High with Somany Ceramics, Prism Johnson, and regional Morbi tile exporters."}
    ),
    (
        "Cera Sanitaryware", "Paints, Adhesives & Home Building Materials",
        "homebuilders, interior renovators, architects, and luxury bathroom connoisseurs",
        "demand water-saving dual-flush sanitaryware, elegant designer chrome faucets, sensor urinals, and wellness bathtubs",
        "Cera Rimless Water-Saving Toilets & Designer Bathroom Faucets", "Sanitaryware, Bathroom Faucets & Wellness Solutions",
        "is a dominant leader in Indian sanitaryware and faucets, pioneering rimless germ-free toilets and robotic 3D-glazed ceramic bathroom suites",
        [0.70, 0.92, 0.96, 0.92, 0.86, 0.78],
        {"political": "Major contributor to national sanitation programs (Swachh Bharat Mission) and water-conservation building standards.", "economic": "Debt-free balance sheet with robust cash balances; rapid growth in high-margin faucets and wellness products alongside ceramic sanitaryware.", "social": "Upgraded millions of Indian bathrooms from utilitarian washrooms into beautiful, hygienic personal wellness retreats.", "technological": "High-pressure battery casting of vitreous china, robotic glazing carousels in Kadi, Gujarat, and automated brass faucet casting.", "legal": "BIS certifications (IS 2556), water-saving green rating certifications, and statutory listing governance.", "environmental": "Pioneered eco-friendly 3/6-liter and 2/4-liter dual-flush toilets, saving billions of liters of fresh water in urban apartments."},
        [0.24, 0.48, 0.38, 0.24, 0.70],
        {"threat_of_new_entrants": "Low to moderate; sanitaryware casting requires specialized refractory kiln firing and deep plumber/architect relationships.", "bargaining_power_of_buyers": "Moderate; homeowners select sanitaryware based on showroom aesthetics, brand trust, and flush performance.", "bargaining_power_of_suppliers": "Moderate; high-grade china clay, natural gas fuel, and brass ingot raw materials.", "threat_of_substitutes": "Low; vitreous china sanitaryware is the universal global standard for hygienic sanitation.", "competitive_rivalry": "High with Hindware (HSIL), Kohler India, and Jaquar."}
    ),
    (
        "Somany Ceramics", "Paints, Adhesives & Home Building Materials",
        "architects, high-traffic commercial builders, and discerning residential renovators",
        "need ultra-high abrasion-resistant floor tiles, anti-slip bathroom flooring, and polished glazed vitrified slabs that retain gloss indefinitely",
        "VC Shield High-Abrasion Tiles & Slip-Shield Bathroom Ceramics", "Ceramic Wall, Floor & Patented Abrasion-Resistant Vitrified Tiles",
        "holds patented technology in abrasion resistance with 'VC Shield', delivering tiles that withstand heavy commercial airport and mall footfalls without scratching",
        [0.70, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Supports domestic manufacturing under Make in India; complies with Bureau of Indian Standards ceramic quality orders.", "economic": "Robust nationwide distribution across 10,000+ touchpoints; consistent profitability driven by high-value glazed vitrified tile mix.", "social": "Pioneered Slip-Shield tiles with specialized micro-textured glazes, preventing dangerous bathroom slip-and-fall injuries for elderly citizens.", "technological": "Patented VeLeCo (VC) Shield technology embedding specialized crystalline minerals that achieve Mohs scale hardness >8; high-speed digital printing.", "legal": "Indian and global patent protection on VC Shield coating; BIS quality compliance.", "environmental": "Heat recovery from tile cooling kilns to dry raw spray clay; extensive rainwater harvesting at manufacturing sites."},
        [0.24, 0.50, 0.38, 0.25, 0.70],
        {"threat_of_new_entrants": "Low to moderate; building a trusted national dealer network and patented ceramic technology takes decades.", "bargaining_power_of_buyers": "Moderate; commercial infrastructure developers specify Somany for high-footfall terminal areas.", "bargaining_power_of_suppliers": "Moderate; natural gas fuel and feldspar/clay raw materials.", "threat_of_substitutes": "Moderate from natural stone and Kajaria tiles.", "competitive_rivalry": "Direct rivalry with Kajaria Ceramics and Prism Johnson."}
    ),
    (
        "HSIL (Hindware Home Innovation)", "Paints, Adhesives & Home Building Materials",
        "home renovators, modern kitchen chefs, and architectural bathroom designers",
        "need touchless sensor faucets, auto-clean kitchen chimney hoods, and sleek contemporary sanitaryware from an iconic trusted heritage brand",
        "Hindware Italian Collection Sanitaryware & Auto-Clean Kitchen Chimneys", "Sanitaryware, Designer Faucets & Smart Kitchen Appliances",
        "has shaped Indian bathrooms for 60+ years with 'Hindware', pioneering auto-clean kitchen chimneys and IoT touchless sensor sanitaryware",
        [0.70, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Complies with BIS standards, national sanitation mandates, and electrical safety standards for kitchen appliances.", "economic": "Demerged consumer and manufacturing businesses to unlock value; market leader in kitchen chimneys with strong presence in sanitaryware.", "social": "Hindware is a household name across multi-generational Indian homes, trusted for durability, smooth ceramic glaze, and water efficiency.", "technological": "Thermal auto-clean kitchen chimney technology with filterless oil collection, touchless gesture controls, and water-saving rimless flushing.", "legal": "BIS sanitaryware certification, trademark protections, and consumer warranty regulations.", "environmental": "Water-saving dual-flush toilets, 100% recycling of ceramic casting slurry, and energy-efficient manufacturing kilns."},
        [0.24, 0.50, 0.38, 0.25, 0.70],
        {"threat_of_new_entrants": "Low to moderate; deep distributor reach and plumber recommendation network form a solid defense.", "bargaining_power_of_buyers": "Moderate; buyers compare features in sanitaryware and kitchen chimneys.", "bargaining_power_of_suppliers": "Moderate; brass ingots, ceramic clay, and specialized kitchen electronic components.", "threat_of_substitutes": "Low for essential bathroom sanitaryware.", "competitive_rivalry": "High with Cera Sanitaryware, Jaquar, and Faber in kitchen appliances."}
    ),
    (
        "Greenpanel Industries", "Paints, Adhesives & Home Building Materials",
        "interior carpenters, modular furniture manufacturers, and architectural builders",
        "need high-density, moisture-resistant medium-density fiberboard (MDF) and commercial wood panels that replace traditional expensive plywood",
        "Greenpanel Club Grade High-Density Moisture Resistant (HDMR) MDF", "Medium Density Fiberboard (MDF) & Wood Panel Manufacturing",
        "is India's largest manufacturer of Medium Density Fiberboard (MDF) with over 50% market share, operating Asia's largest automated MDF plant in Andhra Pradesh",
        [0.72, 0.90, 0.95, 0.94, 0.86, 0.82],
        {"political": "Supports agro-forestry and farmer tree-planting schemes; complies with Bureau of Indian Standards wood panel norms.", "economic": "Industry-leading operating margins (>25% in MDF) and low debt; strong beneficiary of the rapid consumer shift from manual carpentry to modular furniture.", "social": "Provides tens of thousands of rural farmers with guaranteed cash crops through commercial agro-forestry eucalyptus plantation buyback programs.", "technological": "Continuous press lines from Dieffenbacher (Germany), computerized wood fiber refining, and automated resin blending.", "legal": "BIS MDF certifications (IS 12406), formal wood timber procurement licensing, and environmental clearances.", "environmental": "Sourced 100% from renewable agricultural plantation wood (eucalyptus, subabul), saving natural virgin forest timber from deforestation."},
        [0.22, 0.48, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; setting up modern continuous-press MDF plants requires hundreds of crores in capital and extensive agro-forestry farmer supply chains.", "bargaining_power_of_buyers": "Moderate; modular furniture makers (Wakefit, Godrej Interio) specify Greenpanel for routing smoothness.", "bargaining_power_of_suppliers": "Low to moderate; contracts with thousands of local agro-forestry tree farmers.", "threat_of_substitutes": "Moderate from conventional plywood and particle boards.", "competitive_rivalry": "Moderate; undisputed market leader ahead of Action TESA and Century Plyboards."}
    ),
    (
        "Century Plyboards (India)", "Paints, Adhesives & Home Building Materials",
        "carpenters, homeowners, and interior architects across India",
        "demand 100% borer and termite-proof plywood, fire-retardant structural panels, and decorative veneers that withstand tropical humidity",
        "CenturyPly Club Prime, Firewall Technology & Sainik 710 Plywood", "Borer-Proof Plywood, Fire-Retardant Panels & Decorative Laminates",
        "is India's premier plywood and laminate brand, pioneering 'Firewall' technology that prevents plywood from catching fire, and boiling-water-proof Sainik 710",
        [0.70, 0.92, 0.96, 0.92, 0.86, 0.80],
        {"political": "Promotes sustainable agro-forestry timber harvesting; compliant with BIS mandatory plywood quality control orders.", "economic": "Robust brand equity with zero promotional discounts; Sainik 710 successfully captured the massive mass-market semi-urban plywood segment.", "social": "The gold standard of trust for Indian homeowners building bespoke kitchen cabinets and wardrobes that last for decades without termite damage.", "technological": "Patented Firewall nano-engineered fire-retardant chemical treatment, vacuum pressure chemical impregnation, and automated hydraulic pressing.", "legal": "BIS quality certifications (IS 710 for Marine Grade), Forest Stewardship Council (FSC) certifications, and trademark enforcement.", "environmental": "Promotes commercial agro-forestry plantation wood, low-emission non-toxic resin glues, and zero-discharge manufacturing."},
        [0.22, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; local unorganized sawmills exist, but consumers demand certified boiling-water-proof (BWP) plywood backed by multi-decade warranties.", "bargaining_power_of_buyers": "Moderate; carpenters and homeowners choose CenturyPly for termite-proof guarantees.", "bargaining_power_of_suppliers": "Moderate; agro-forestry face veneer and core timber logs.", "threat_of_substitutes": "Moderate from MDF boards and aluminum modular cabinets.", "competitive_rivalry": "Direct rivalry with Greenply Industries and Greenpanel."}
    )
]

for item in sector19_data:
    add_c(*item)

print(f"Sector 19 added: {len(sector19_data)} companies. Total: {len(part4_a)}")

# ==============================================================================
# SECTOR 20: Logistics, Freight & Supply Chain Tech (20 companies)
# ==============================================================================
sector20_data = [
    (
        "Delhivery", "Logistics, Freight & Supply Chain Tech",
        "e-commerce platforms, D2C brands, retail enterprises, and B2B freight shippers across 18,600+ pin codes",
        "need high-speed express parcel delivery, automated warehousing, heavy partial-truckload (PTL) freight, and cross-border logistics",
        "Express Parcel Delivery, Automated Mega-Hubs & PTL Freight Services", "Integrated Full-Stack Technology-Driven Logistics Network",
        "is India's largest fully integrated logistics player, delivering over 2.5 billion parcels across 18,600+ pin codes using proprietary mesh network routing",
        [0.75, 0.92, 0.96, 0.96, 0.85, 0.75],
        {"political": "Direct beneficiary of National Logistics Policy (NLP) targeting reduction of India's logistics cost from 14% to sub-9% of GDP.", "economic": "Achieved positive adjusted EBITDA and operating cash flows; massive operational leverage through shared infrastructure between express parcel and B2B freight.", "social": "Bridges urban e-commerce to remote frontier villages in Kashmir, Northeast India, and the Thar desert with reliable doorstep delivery.", "technological": "Proprietary machine learning address-correction algorithms, automated robotic sortation hubs (Tauru and Bhiwandi), and dynamic linehaul optimization.", "legal": "Compliance with motor vehicle transit rules, GST e-way bill verification, and gig-worker social security frameworks.", "environmental": "Rapid transition to electric commercial delivery vehicles (EV 2/3/4-wheelers) and paperless digital consignments."},
        [0.25, 0.55, 0.38, 0.25, 0.75],
        {"threat_of_new_entrants": "Low; building a logistics mesh network covering 18,600 pin codes with multi-million-parcel daily capacity costs billions of dollars.", "bargaining_power_of_buyers": "Moderate to high; major e-commerce platforms (Amazon, Meesho) negotiate competitive per-parcel shipping rates.", "bargaining_power_of_suppliers": "Low; fragmented long-haul truck suppliers and commercial fleet vendors.", "threat_of_substitutes": "Moderate from in-house captive logistics fleets (Ekart, Amazon ATS).", "competitive_rivalry": "High with Blue Dart, Ecom Express, and Xpressbees."}
    ),
    (
        "Blue Dart Express (DHL Group)", "Logistics, Freight & Supply Chain Tech",
        "banks, pharmaceutical clinical trial shippers, corporate enterprises, and high-value e-commerce clients",
        "require guaranteed overnight express air courier delivery, secure cash/document transit, and temperature-controlled medical logistics",
        "Blue Dart Aviation Dedicated Freighters & Time-Definite Air Express", "Premier Aviation-Led Air Express Courier & Specialized Logistics",
        "is South Asia's premier air express company, operating India's only dedicated commercial fleet of Boeing 737 and 757 freighter aircraft",
        [0.75, 0.92, 0.96, 0.95, 0.86, 0.75],
        {"political": "Strategic air cargo partner for Ministry of Civil Aviation; compliant with Directorate General of Civil Aviation (DGCA) air security norms.", "economic": "Commands the highest pricing power and premium yields in Indian logistics; unmatched brand reputation ensures recession-proof corporate accounts.", "social": "Delivers time-critical biometric passports, bank debit/credit cards, and emergency medical organs overnight across the nation.", "technological": "Dedicated Boeing freighter network, computerized track-and-trace with real-time barcode scanning, and temperature-controlled Smartbox containers.", "legal": "DGCA air carrier operations compliance, airport security clearances, and postal courier licensing regulations.", "environmental": "Aviation fleet modernization reducing aircraft fuel burn; pilot testing electric delivery vans and paperless digital airway bills."},
        [0.18, 0.45, 0.35, 0.20, 0.65],
        {"threat_of_new_entrants": "Low; operating an owned fleet of commercial jet freighters with dedicated airport cargo slots is an impenetrable barrier.", "bargaining_power_of_buyers": "Low to moderate; banks and clinical labs willingly pay a premium for Blue Dart's guaranteed next-morning delivery reliability.", "bargaining_power_of_suppliers": "Moderate; aviation turbine fuel (ATF) prices and airport landing fees.", "threat_of_substitutes": "Moderate from surface express road logistics for non-urgent shipments.", "competitive_rivalry": "Low in air express; moderate in surface express."}
    ),
    (
        "Container Corporation of India (CONCOR)", "Logistics, Freight & Supply Chain Tech",
        "international container shipping lines, import-export traders, and domestic bulk cargo movers",
        "need seamless, multimodal container rail transportation between coastal seaports and inland industrial manufacturing hinterlands",
        "Inland Container Depots (ICDs) & Scheduled Multi-Modal Container Trains", "Navratna Multimodal Rail Container Logistics Monolith",
        "dominates Indian containerized rail logistics with ~60% market share, operating a strategic nationwide network of 60+ Inland Container Depots (ICDs)",
        [0.85, 0.94, 0.96, 0.92, 0.88, 0.80],
        {"political": "Navratna public sector enterprise under Ministry of Railways; prime beneficiary of the Dedicated Freight Corridor (DFC).", "economic": "Exceptional return on capital and massive debt-free cash balances; double-stacking container trains on Western DFC slashes unit haulage costs.", "social": "Enables landlocked states (Punjab, Haryana, UP, MP) to export goods globally with port-customs clearances right in their home cities.", "technological": "Double-stack container rakes, automated container terminal operating systems, and satellite GPS tracking of container freight trains.", "legal": "Indian Railways haulage agreements, Customs bonded warehouse licensing, and public sector governance.", "environmental": "Shifting freight from highway diesel trucks to electric rail container trains slashes greenhouse gas emissions by over 75%."},
        [0.12, 0.42, 0.30, 0.18, 0.48],
        {"threat_of_new_entrants": "Low; building inland container depots (ICDs) with dedicated railway sidings and sovereign customs ports requires vast land and railway accords.", "bargaining_power_of_buyers": "Moderate; shipping lines and freight forwarders negotiate volume box rates.", "bargaining_power_of_suppliers": "Moderate; Indian Railways sets statutory track haulage charges.", "threat_of_substitutes": "Moderate from highway road container trailers for short hauls (<500 km).", "competitive_rivalry": "Low to moderate; dominates rail container transport ahead of Gateway Distriparks and Adani Logistics."}
    ),
    (
        "Mahindra Logistics", "Logistics, Freight & Supply Chain Tech",
        "automotive OEMs, industrial engineering companies, e-commerce giants, and corporate mobility clients",
        "require complex third-party logistics (3PL), automotive inbound-to-manufacturing logistics, automated warehousing, and electric enterprise transport",
        "3PL Supply Chain Management, Integrated Warehousing & Alyte EV Mobility", "Integrated Third-Party Logistics (3PL) & Enterprise Mobility",
        "operates an asset-light 3PL model managing 19+ million sq ft of modern logistics parks, specializing in complex automotive and engineering supply chains",
        [0.72, 0.90, 0.95, 0.92, 0.85, 0.80],
        {"political": "Direct beneficiary of national GST harmonization, National Logistics Policy, and corporate outsourcing of fragmented supply chains.", "economic": "Asset-light business model delivers superior return on capital; strong revenue synergy from parent Mahindra Group anchor business.", "social": "Operates 'Alyte' enterprise mobility transporting hundreds of thousands of corporate employees safely to work daily.", "technological": "Automated warehouse management systems (WMS), AI transportation route planning, and telematics-enabled freight fleet dispatch.", "legal": "Motor vehicle regulations, labor contract compliance, and public corporate governance.", "environmental": "Pioneered 'Edel' electric vehicle last-mile delivery and net-zero carbon warehouse facilities with solar rooftops."},
        [0.24, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; basic trucking is easy, but managing multi-client mega-warehouses and automotive just-in-time logistics requires enterprise trust.", "bargaining_power_of_buyers": "Moderate; corporate clients negotiate competitive long-term service level agreements.", "bargaining_power_of_suppliers": "Low; fragmented network of regional trucking partners and warehouse developers.", "threat_of_substitutes": "Moderate from in-house corporate logistics.", "competitive_rivalry": "High with TVS Supply Chain Solutions, DHL Supply Chain, and Delhivery."}
    ),
    (
        "Transport Corporation of India (TCI)", "Logistics, Freight & Supply Chain Tech",
        "chemical manufacturers, automotive giants, retail FMCG, and industrial infrastructure builders",
        "need multi-modal freight transport combining road, coastal shipping, rail, and specialized cold-chain logistics across South Asia",
        "TCI Freight, TCI Seaways Coastal Shipping & TCI Supply Chain Solutions", "Multimodal Freight Logistics, Coastal Shipping & Chemical Supply Chain",
        "has moved India's cargo for over 65 years, operating 6 coastal cargo ships, 14 million sq ft of warehousing, and 10,000+ trucks on the road daily",
        [0.74, 0.92, 0.95, 0.90, 0.86, 0.78],
        {"political": "Pioneer of Sagarmala coastal shipping initiative; multimodal transit permits connecting India with Nepal, Bhutan, and Bangladesh.", "economic": "Exceptional capital discipline with low debt-to-equity and steady compounding cash generation across diverse transport modes.", "social": "The foundational carrier of Indian commerce, running specialized healthcare clinics (Kavach) for highway truck drivers across major national routes.", "technological": "GPS fleet tracking, automated freight billing ERP, specialized chemical ISO tank containers, and mechanized multimodal transshipment.", "legal": "Merchant Shipping Act compliance, carriage of dangerous goods regulations, and Motor Vehicles Act rules.", "environmental": "Coastal shipping on cargo vessels emits 80% less CO2 per ton-km than highway trucking; utilizes green warehousing practices."},
        [0.22, 0.48, 0.35, 0.20, 0.65],
        {"threat_of_new_entrants": "Low; building a 65-year corporate logistics brand, coastal cargo vessel fleet, and 1,000 branch network requires multi-decade trust.", "bargaining_power_of_buyers": "Moderate; industrial shippers negotiate annual freight contracts, but rely on TCI for specialized multimodal logistics.", "bargaining_power_of_suppliers": "Low; truck fleet owners and fuel providers.", "threat_of_substitutes": "Moderate from pure-road trucking, but multimodal coastal routes offer lower cost.", "competitive_rivalry": "Moderate; leads organized multi-modal transport ahead of VRL and Allcargo."}
    ),
    (
        "Allcargo Logistics", "Logistics, Freight & Supply Chain Tech",
        "international freight forwarders, global import-export traders, and industrial multinational shippers",
        "require global less-than-container-load (LCL) ocean freight consolidation, container freight stations (CFS), and project cargo handling",
        "ECU Worldwide Global LCL Consolidation & Port CFS Infrastructure", "Global Less-than-Container-Load (LCL) Ocean Freight & Multimodal Logistics",
        "is the world's #1 LCL ocean freight consolidator through ECU Worldwide, operating across 180 countries with unmatched global trade connectivity",
        [0.75, 0.92, 0.95, 0.92, 0.86, 0.75],
        {"political": "Supports India's export growth mission and trade formalization; operates major Customs Bonded Container Freight Stations (CFS) at major ports.", "economic": "Global scale generates substantial foreign currency operating cash flows; successfully completed strategic restructuring into focused logistics verticals.", "social": "Connects small Indian MSME exporters directly to global maritime shipping lanes, enabling international trade for small enterprises.", "technological": "ECU360 digital freight platform offering instant global ocean freight quotes, online booking, and multi-country customs tracking.", "legal": "Customs Act compliance for port CFS operations, international maritime shipping laws, and FMC US shipping regulations.", "environmental": "Promotes container load consolidation, maximizing vessel space utilization and cutting greenhouse gas emissions per cargo ton."},
        [0.18, 0.45, 0.35, 0.18, 0.55],
        {"threat_of_new_entrants": "Low; matching ECU Worldwide's global 180-country trade network and port CFS infrastructure is an insurmountable barrier.", "bargaining_power_of_buyers": "Moderate; international shippers compare ocean freight spot rates across freight forwarders.", "bargaining_power_of_suppliers": "Moderate; ocean container shipping lines (Maersk, CMA CGM).", "threat_of_substitutes": "Low; ocean shipping carries 95% of international bulk trade.", "competitive_rivalry": "Low to moderate globally in LCL consolidation; moderate in domestic CFS."}
    ),
    (
        "Shadowfax Technologies", "Logistics, Freight & Supply Chain Tech",
        "quick-commerce dark stores, food delivery platforms, e-commerce marketplaces, and retail brands",
        "need instant on-demand hyperlocal delivery, express reverse logistics (returns pickup), and flexible gig delivery fleets",
        "Hyperlocal 15-Minute Fleet, Express E-Commerce & Reverse Logistics", "Crowdsourced On-Demand Hyperlocal & E-Commerce Logistics Platform",
        "operates India's largest crowdsourced third-party delivery network with over 3 million registered delivery partners across 2,500+ cities",
        [0.70, 0.90, 0.96, 0.96, 0.82, 0.70],
        {"political": "Complies with state gig-worker welfare guidelines, traffic safety regulations, and local municipal delivery norms.", "economic": "Multi-category fleet sharing: delivery partners alternate between afternoon e-commerce deliveries and evening food/quick-commerce runs, maximizing rider productivity.", "social": "Provides flexible, dignified earning opportunities for millions of young gig workers and students across non-metro Indian towns.", "technological": "AI algorithmic dispatch matching riders to nearest delivery tasks, dynamic route optimization, and instant doorstep quality checks for returns.", "legal": "Motor vehicle regulations, intermediary guidelines, and gig labor welfare policies.", "environmental": "Accelerating deployment of electric two-wheelers across urban delivery fleets to achieve zero-tailpipe last-mile emissions."},
        [0.28, 0.58, 0.35, 0.28, 0.78],
        {"threat_of_new_entrants": "Moderate; building rider network density across 2,500 cities requires substantial venture capital and operational discipline.", "bargaining_power_of_buyers": "High; enterprise platforms (Swiggy, Meesho, Flipkart) negotiate competitive per-delivery payouts.", "bargaining_power_of_suppliers": "Moderate; gig delivery partners choose between competing delivery platforms based on daily earning incentives.", "threat_of_substitutes": "Moderate from captive in-house delivery fleets.", "competitive_rivalry": "Intense rivalry with Delhivery, Porter, and Loadshare."}
    ),
    (
        "Shiprocket (BigFoot Retail Solutions)", "Logistics, Freight & Supply Chain Tech",
        "D2C brands, social commerce sellers, Shopify merchants, and SME online retailers",
        "need automated multi-carrier shipping aggregation, lowest shipping rates, automated tracking notifications, and cash-on-delivery (COD) fraud prevention",
        "Shiprocket Automated Shipping Aggregator & Shiprocket Fulfillment", "E-Commerce Shipping Aggregation & D2C Enablement Platform",
        "powers over 100,000 active digital sellers and D2C brands, automating over $3 billion in annual gross merchandise value through integrated courier APIs",
        [0.72, 0.90, 0.96, 0.96, 0.84, 0.72],
        {"political": "Champion of Digital India and MSME e-commerce export enablement; partnered with India Post to expand rural and international shipping.", "economic": "High-margin software take-rate plus logistics arbitrage; sticky SaaS subscription and logistics workflow integration for online brands.", "social": "Democratized national logistics for small home-based women entrepreneurs and Instagram fashion sellers, giving them corporate-grade shipping rates.", "technological": "Proprietary CORE machine learning engine recommending the fastest/cheapest courier per pin code; automated RTO (Return to Origin) fraud prediction.", "legal": "Consumer protection e-commerce rules, IT Act intermediary compliance, and secure payment processing.", "environmental": "Optimized multi-carrier routing reduces failed delivery attempts (RTO), preventing wasted fuel and vehicle emissions."},
        [0.26, 0.52, 0.35, 0.25, 0.68],
        {"threat_of_new_entrants": "Low to moderate; network effects and API integrations with 25+ courier partners create a strong moat.", "bargaining_power_of_buyers": "Moderate; D2C brands love the convenience and unified dashboard, but compare rate-cards.", "bargaining_power_of_suppliers": "Moderate; courier companies (Delhivery, Blue Dart, Shadowfax) value Shiprocket's massive aggregated volume.", "threat_of_substitutes": "Moderate from dealing directly with single courier companies.", "competitive_rivalry": "Moderate; undisputed market leader in Indian e-commerce shipping enablement."}
    ),
    (
        "BlackBuck (Zinka Logistics)", "Logistics, Freight & Supply Chain Tech",
        "highway truck fleet owners, independent truck drivers, and commercial shippers across India",
        "need digital freight matchmaking, seamless FASTag toll payments, GPS fleet telematics, and discounted diesel fuel procurement",
        "BlackBuck Trucker Super-App & Digital FASTag Solutions", "India's Largest Digital Freight & Trucking Services Platform",
        "empowers over 1 million truck operators—representing over 30% of India's commercial trucks—processing over 35% of all national FASTag toll payments",
        [0.75, 0.92, 0.96, 0.96, 0.84, 0.72],
        {"political": "Pinnacle digital platform executing the Government of India's mandatory electronic FASTag highway toll collection mandate.", "economic": "Network monetization through high-frequency financial payments: collects transaction fees on billions of rupees in FASTag tolls and diesel refueling.", "social": "Transforms the harsh lives of Indian truck drivers, eliminating highway cash extortion and providing transparent digital banking services.", "technological": "IoT GPS vehicle tracking, automated fuel-theft alerts, digital freight bidding marketplace, and automated tire management.", "legal": "NPCI FASTag regulations, RBI payment system guidelines, and Motor Vehicles Act compliance.", "environmental": "Reduces empty truck deadhead return trips by 20%, saving millions of liters of diesel fuel and cutting nationwide transport emissions."},
        [0.22, 0.48, 0.30, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; building a platform used by 1 million truck operators and processing 35% of national FASTags is an insurmountable network effect.", "bargaining_power_of_buyers": "Low to moderate; truckers rely on BlackBuck as their primary daily operating app for tolls, fuel, and loads.", "bargaining_power_of_suppliers": "Low; oil marketing companies (IOCL, HPCL) partner with BlackBuck to drive fuel retail volumes.", "threat_of_substitutes": "Low; digital toll collection is legally mandated.", "competitive_rivalry": "Low to moderate; undisputed dominant digital platform for Indian highway trucking."}
    ),
    (
        "VRL Logistics", "Logistics, Freight & Supply Chain Tech",
        "SME manufacturers, wholesale traders, and intercity passenger commuters across South and West India",
        "need dependable less-than-truckload (LTL) parcel cargo delivery with guaranteed transit times, and luxurious intercity sleeper passenger bus travel",
        "LTL Surface Parcel Cargo & Luxury Intercity Passenger Coach Network", "Surface Express Less-Than-Truckload (LTL) Cargo & Luxury Passenger Transport",
        "operates an owned fleet of over 5,500 goods trucks and 300+ luxury passenger buses, providing seamless parcel cargo delivery across 24 Indian states",
        [0.72, 0.92, 0.95, 0.90, 0.85, 0.74],
        {"political": "Complies strictly with the Motor Vehicles Act, National Permit regulations, and state commercial passenger transport guidelines.", "economic": "Consistently generates high operating cash flows and ROCE (>25%) through 100% company-owned vehicle fleets and captive in-house maintenance hubs.", "social": "The lifeblood of small traders and textile merchants in Karnataka, Maharashtra, and Gujarat, transporting small commercial parcels safely.", "technological": "In-house software tracking every parcel bar-code, automated tire retreading plants, and computerized logistics transshipment hubs.", "legal": "Motor Vehicles Act, GST e-way bill compliance, and public corporate listing standards.", "environmental": "In-house bio-diesel blending and aerodynamic truck body designs cutting highway diesel consumption."},
        [0.24, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; building VRL's owned 5,500-truck fleet, 1,000+ branch transshipment network, and decades of trader trust requires immense capital.", "bargaining_power_of_buyers": "Moderate; small SME traders value VRL's guaranteed cargo safety and zero-loss record.", "bargaining_power_of_suppliers": "Low; bulk direct purchaser of commercial chassis from Ashok Leyland and fuel from refineries.", "threat_of_substitutes": "Moderate from railway parcel services and competing LTL operators.", "competitive_rivalry": "Moderate; dominates Southern and Western Indian surface parcel routes ahead of TCI Express."}
    ),
    (
        "Gati (Allcargo company)", "Logistics, Freight & Supply Chain Tech",
        "enterprises, retail distribution networks, and B2B industrial manufacturers",
        "need time-definite express surface cargo, cold-chain solutions, and pan-India supply chain management",
        "Gati-KWE Express Surface Distribution & Air Cargo Services", "Pioneer of Express Cargo Distribution & Supply Chain Solutions",
        "pioneered express cargo distribution in India, delivering time-definite surface parcel logistics covering 99% of India's economic districts",
        [0.72, 0.90, 0.95, 0.90, 0.85, 0.74],
        {"political": "Direct beneficiary of national GST unified tax borders and National Logistics Policy reforms.", "economic": "Revitalized under Allcargo Logistics ownership; modernizing surface transshipment hubs (STHs) to achieve fast turnaround and margin expansion.", "social": "Historic pioneer that built modern express cargo logistics in India, connecting industrial manufacturers with retail stockists.", "technological": "Automated mega-transshipment hubs with automated conveyor sorters, mobile pick-and-pack scanning, and API enterprise ERP integrations.", "legal": "Motor Vehicles Act, carrier liability laws, and statutory public corporate governance.", "environmental": "Deployment of electric commercial vehicles for urban pickup/delivery and energy-efficient warehouse lighting."},
        [0.25, 0.52, 0.38, 0.22, 0.70],
        {"threat_of_new_entrants": "Low to moderate; operating pan-India express routes with automated hubs requires heavy network investments.", "bargaining_power_of_buyers": "Moderate; corporate shippers compare transit speeds and freight rates.", "bargaining_power_of_suppliers": "Low; commercial vehicle suppliers and fleet operators.", "threat_of_substitutes": "Moderate from full truckload (FTL) and rail transport.", "competitive_rivalry": "High with TCI Express, Safexpress, and Delhivery."}
    ),
    (
        "Gateway Distriparks", "Logistics, Freight & Supply Chain Tech",
        "international container shipping lines, EXIM cargo traders, and cold-chain shippers",
        "require integrated intermodal rail transportation, port container freight stations (CFS), and refrigerated cold-chain storage",
        "Intermodal Rail Container Trains & Port Container Freight Stations", "Intermodal Rail Logistics & Port CFS Infrastructure",
        "operates premier intermodal rail container networks connected to major Indian ports, running 31 container trainsets and 6 inland container terminals",
        [0.76, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Key private operator licensed under Indian Railways container policy; major beneficiary of Western Dedicated Freight Corridor.", "economic": "Strong operating cash flows driven by integrated rail-CFS-cold chain operations; high asset turns on double-stacked container rail routes.", "social": "Facilitates seamless export of Indian agricultural produce, textiles, and auto parts from inland factories to global seaports.", "technological": "High-capacity reach stackers, computerized container yard tracking, and real-time GPS tracking of scheduled container trains.", "legal": "Concession agreements with Indian Railways, Customs bonded warehouse regulations, and maritime port compliances.", "environmental": "Double-stack rail container transport slashes highway diesel emissions by over 70% compared to road container trailers."},
        [0.22, 0.48, 0.35, 0.20, 0.62],
        {"threat_of_new_entrants": "Low; acquiring inland container rail terminals with private rail sidings and train operating licenses requires substantial capital.", "bargaining_power_of_buyers": "Moderate; global shipping lines negotiate container terminal handling tariffs.", "bargaining_power_of_suppliers": "Moderate; Indian Railways sets track haulage fees.", "threat_of_substitutes": "Moderate from road container trucking for short hauls.", "competitive_rivalry": "Moderate; competes with CONCOR and Adani Logistics."}
    ),
    (
        "TCI Express", "Logistics, Freight & Supply Chain Tech",
        "automotive, pharmaceutical, electronic, and engineering manufacturers",
        "need guaranteed, time-definite express parcel delivery with automated tracking and zero transshipment damage",
        "Time-Definite Express Surface & Air Domestic Courier", "Pure-Play Express Cargo Logistics Specialist",
        "is India's leading pure-play express cargo company, operating 28 automated sorting centers and 900+ company branches with 95%+ on-time delivery",
        [0.72, 0.92, 0.95, 0.92, 0.85, 0.75],
        {"political": "Complies with national carriage of goods acts, GST e-way bill mandates, and interstate transit regulations.", "economic": "Industry-leading return on capital employed (>30%) and zero net debt; pure-play B2B focus delivers superior pricing discipline.", "social": "Ensures time-critical industrial spare parts and life-saving medicines reach factories and hospitals without delay.", "technological": "High-speed automated sorters in mega-hubs (Gurugram and Pune), barcoded parcel tracking, and real-time customer mobile dashboards.", "legal": "Carrier liability laws, motor transport worker regulations, and public corporate listing standards.", "environmental": "Constructs green automated sorting hubs with rooftop solar arrays and rainwater harvesting systems."},
        [0.24, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low to moderate; building a 900-branch time-definite express network requires decades of operational perfection.", "bargaining_power_of_buyers": "Moderate; corporate clients prioritize on-time delivery guarantees and cargo safety over cheap commodity trucking.", "bargaining_power_of_suppliers": "Low; outsourced dedicated vehicle fleet operators.", "threat_of_substitutes": "Moderate from air express and general trucking.", "competitive_rivalry": "Direct rivalry with Gati, Safexpress, and Blue Dart."}
    ),
    (
        "Ecom Express", "Logistics, Freight & Supply Chain Tech",
        "large-scale e-commerce marketplaces and direct-to-consumer digital brands",
        "demand dedicated e-commerce delivery covering deep tier-3, tier-4, and rural India, with seamless Cash on Delivery (COD) management",
        "Ecom Express Parcel Delivery & Automated E-Commerce Fulfillment", "Dedicated Tech-Driven E-Commerce Logistics Network",
        "covers over 27,000 pin codes reaching 95%+ of India's population, pioneering secure Cash on Delivery and digital address verification for e-commerce",
        [0.72, 0.90, 0.96, 0.95, 0.84, 0.72],
        {"political": "Supports Digital India and financial inclusion by enabling cash-reliant rural citizens to participate in online e-commerce.", "economic": "High-volume automated parcel processing; massive presence in semi-urban and rural non-metro towns with high COD transaction volumes.", "social": "Brings the convenience of modern online shopping into remote rural hamlets across Bihar, UP, and the Northeast.", "technological": "Automated parcel sortation conveyors, geocoding algorithms for unstandardized rural addresses, and biometric delivery verification.", "legal": "Intermediary compliance, motor vehicle regulations, and digital consumer protection standards.", "environmental": "Deploying electric delivery 2-wheelers and implementing 100% recyclable paper delivery packaging."},
        [0.26, 0.55, 0.38, 0.25, 0.75],
        {"threat_of_new_entrants": "Low to moderate; establishing last-mile delivery reach across 27,000 pin codes requires immense operating capital.", "bargaining_power_of_buyers": "High; e-commerce platforms (Amazon, Flipkart, Meesho) negotiate competitive delivery fees.", "bargaining_power_of_suppliers": "Low; linehaul fleet vendors and delivery riders.", "threat_of_substitutes": "High from Delhivery, Shadowfax, and captive e-commerce delivery fleets.", "competitive_rivalry": "Intense rivalry with Delhivery and Xpressbees."}
    ),
    (
        "Snowman Logistics", "Logistics, Freight & Supply Chain Tech",
        "quick-service restaurant chains, ice cream makers, pharmaceutical vaccine manufacturers, and seafood exporters",
        "require temperature-controlled cold storage (-25 deg C to +20 deg C) and multi-temperature refrigerated transport without breaking the cold chain",
        "Cold Storage Warehousing & Refrigerated Reefer Fleet Logistics", "Integrated Temperature-Controlled Cold-Chain Logistics",
        "is India's premier organized cold-chain logistics provider, operating 45+ temperature-controlled warehouses and a massive fleet of GPS-tracked reefer trucks",
        [0.74, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Direct beneficiary of National Cold Chain Policy and food processing infrastructure subsidies by the Ministry of Food Processing Industries.", "economic": "High asset utilization and multi-year corporate contracts with global brands (Domino's, Baskin Robbins, multinational pharma).", "social": "Eliminates post-harvest food waste and safeguards critical biological medicines and vaccines from temperature degradation.", "technological": "Automated multi-temperature chamber control, IoT real-time temperature data logging, and GPS-monitored refrigerated transport vans.", "legal": "FSSAI cold-chain licensing, CDSCO pharmaceutical storage compliance, and municipal warehouse fire safety.", "environmental": "Ammonia and eco-friendly refrigerant systems, solar rooftop generation, and thermal insulation minimizing energy consumption."},
        [0.22, 0.48, 0.38, 0.22, 0.62],
        {"threat_of_new_entrants": "Low; building temperature-controlled warehouses with multi-chamber freezing (-25 deg C) requires specialized engineering and capital.", "bargaining_power_of_buyers": "Moderate; QSR and pharma clients cannot compromise on cold-chain integrity, making Snowman a sticky partner.", "bargaining_power_of_suppliers": "Moderate; commercial refrigeration equipment (Daikin, Carrier Transicold) and insulated reefer chassis.", "threat_of_substitutes": "Low; perishable frozen foods and vaccines require unbroken cold chains.", "competitive_rivalry": "Moderate; dominates organized corporate cold-chain logistics in India."}
    ),
    (
        "Porter (Resfeber Labs)", "Logistics, Freight & Supply Chain Tech",
        "SME merchants, retail shopkeepers, moving households, and local business owners",
        "need instant on-demand booking of mini-trucks (Tata Ace, Pickup) and two-wheelers for fast, transparently priced intra-city goods movement",
        "On-Demand Intra-City Mini-Truck & Bike Delivery Platform", "Intra-City On-Demand Logistics & Mini-Truck Aggregation",
        "revolutionized urban intra-city goods transport in India, aggregating over 500,000 driver-partners across 20+ cities with algorithmic transparent pricing",
        [0.72, 0.92, 0.96, 0.96, 0.84, 0.72],
        {"political": "Formalizes the fragmented unorganized tempo and mini-truck market; compliant with municipal urban traffic and transport policies.", "economic": "Asset-light aggregator platform earning take-rates on millions of monthly trips; achieved unicorn status and positive unit economics.", "social": "Eliminates the frustration of haggling with roadside tempo drivers; dramatically increases monthly earnings for driver-partners.", "technological": "Algorithmic driver dispatch matching nearest mini-truck to customer, real-time trip GPS telemetry, and dynamic pricing algorithms.", "legal": "Motor vehicle commercial aggregator guidelines, municipal city transport rules, and consumer protection frameworks.", "environmental": "Optimized route dispatch eliminates idle deadhead miles; actively onboarding electric mini-trucks (Tata Ace EV)."},
        [0.26, 0.52, 0.35, 0.24, 0.68],
        {"threat_of_new_entrants": "Low to moderate; achieving driver supply liquidity and customer demand density across 20 major cities requires substantial scale.", "bargaining_power_of_buyers": "Moderate; SME traders compare Porter prices against local tempo stands, but love the instant app booking convenience.", "bargaining_power_of_suppliers": "Moderate; mini-truck driver-partners choose between Porter, Uncle Delivery, and independent street stands.", "threat_of_substitutes": "Moderate from traditional offline tempo stands.", "competitive_rivalry": "Moderate; undisputed market leader in on-demand intra-city commercial transport."}
    ),
    (
        "Blowhorn (Catbus Infolabs)", "Logistics, Freight & Supply Chain Tech",
        "fast-growing D2C brands, e-commerce platforms, and retail enterprise clients",
        "require same-day intra-city delivery, micro-fulfillment dark warehousing, and integrated middle-mile-to-last-mile logistics",
        "Same-Day Intra-City Delivery & Micro-Warehousing Network", "Intra-City Same-Day Logistics & Micro-Fulfillment Platform",
        "pioneered micro-fulfillment same-day delivery in India, operating urban micro-hubs that allow brands to deliver customer orders in under 4 hours",
        [0.70, 0.88, 0.95, 0.95, 0.82, 0.72],
        {"political": "Supports urban logistics formalization and clean city distribution initiatives under National Logistics Policy.", "economic": "High-margin value proposition: enables D2C brands to compete with Amazon Prime speeds by placing stock in urban micro-warehouses.", "social": "Empowers local driver-partners with predictable daily intra-city delivery routes and steady monthly incomes.", "technological": "Predictive stock placement algorithms, real-time routing engine, and dark-store inventory picking software.", "legal": "Municipal commercial warehousing licenses, motor vehicle regulations, and consumer privacy standards.", "environmental": "Pioneered early transition to commercial electric delivery vehicles, significantly reducing urban delivery emissions."},
        [0.28, 0.55, 0.38, 0.25, 0.72],
        {"threat_of_new_entrants": "Moderate; micro-fulfillment software can be developed, but managing leased urban dark hubs requires operating capital.", "bargaining_power_of_buyers": "Moderate; brands compare fulfillment costs and delivery speed SLAs across providers.", "bargaining_power_of_suppliers": "Moderate; commercial van and EV fleet owners.", "threat_of_substitutes": "High from standard next-day courier delivery (Delhivery) and quick commerce.", "competitive_rivalry": "High with Porter and Shadowfax in intra-city delivery."}
    ),
    (
        "Xpressbees (BusyBees Logistics)", "Logistics, Freight & Supply Chain Tech",
        "large e-commerce marketplaces, social commerce platforms, and retail enterprises",
        "need high-throughput e-commerce parcel logistics, integrated 3PL warehousing, B2B express cargo, and cross-border freight",
        "E-Commerce Express Parcel Logistics & 3PL Warehousing", "Full-Stack Tech-Enabled Express Logistics & 3PL Solutions",
        "delivers over 3 million parcels daily across 20,000+ pin codes, operating as a core logistics backbone for India's leading digital platforms",
        [0.72, 0.90, 0.96, 0.95, 0.84, 0.72],
        {"political": "Supports national digital commerce growth and logistics cost reduction under National Logistics Policy.", "economic": "Achieved unicorn valuation; strong financial backing from Ontario Teachers' and Blackstone, expanding rapidly into B2B freight.", "social": "Creates tens of thousands of delivery and sortation jobs for youth in Tier-2, 3, and 4 towns across India.", "technological": "Automated sorters handling 45,000 parcels/hour in mega-hubs, mobile delivery apps with offline sync, and real-time transit telemetry.", "legal": "Motor vehicle compliances, carrier liability laws, and consumer protection e-commerce regulations.", "environmental": "Deploying electric delivery two-wheelers and optimizing truck loads to minimize linehaul carbon emissions."},
        [0.26, 0.55, 0.38, 0.25, 0.75],
        {"threat_of_new_entrants": "Low to moderate; matching Xpressbees' 20,000 pin code delivery footprint requires multi-year investments.", "bargaining_power_of_buyers": "High; e-commerce platforms negotiate volume shipping contracts.", "bargaining_power_of_suppliers": "Low; linehaul trucking partners and delivery associates.", "threat_of_substitutes": "High from Delhivery and Ecom Express.", "competitive_rivalry": "Intense rivalry with Delhivery, Ecom Express, and Shadowfax."}
    ),
    (
        "WheelsEye Technology", "Logistics, Freight & Supply Chain Tech",
        "independent commercial truck owners and small fleet operators across India",
        "need affordable, high-precision GPS truck tracking, fuel theft monitoring, digital FASTag payments, and truck insurance",
        "WheelsEye IoT Truck GPS Tracker & Fleet Management Software", "IoT Fleet Management SaaS & Trucker Telematics Platform",
        "empowers over 2 million commercial truck owners with affordable GPS telematics and mobile fleet management software, cutting fleet operating costs",
        [0.70, 0.88, 0.94, 0.96, 0.84, 0.70],
        {"political": "Direct beneficiary of AIS-140 mandatory government vehicle tracking device mandates for commercial vehicles in India.", "economic": "Recurring SaaS subscription revenue model combined with high-volume FASTag transaction fees; rapid organic word-of-mouth adoption.", "social": "Protects small truck owners from vehicle theft, unauthorized trips by drivers, and roadside diesel pilferage.", "technological": "AIS-140 certified GPS hardware with panic buttons, fuel sensor telemetry, engine immobilization, and truck health analytics.", "legal": "Automotive Industry Standard (AIS-140) government approvals, WPC wireless certifications, and data privacy compliance.", "environmental": "Optimized driving behavior and idling reduction features cut truck fuel waste and carbon emissions."},
        [0.24, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; basic GPS hardware is imported, but WheelsEye's proprietary software and direct truck-stand sales team form a solid moat.", "bargaining_power_of_buyers": "Moderate; truck owners pay an affordable annual subscription fee for valuable theft security.", "bargaining_power_of_suppliers": "Moderate; cellular IoT SIM card providers (Airtel, Vi) and GPS chipsets.", "threat_of_substitutes": "Moderate from BlackBuck and factory-fitted OEM telematics (Tata Fleetman, Ashok Leyland i-Alert).", "competitive_rivalry": "Direct rivalry with BlackBuck and LocoNav."}
    ),
    (
        "TVS Supply Chain Solutions", "Logistics, Freight & Supply Chain Tech",
        "global automotive manufacturers, aerospace defense companies, and industrial conglomerates across 25+ countries",
        "require end-to-end supply chain transformation, global procurement engineering, automated in-plant logistics, and parts warehousing",
        "Integrated Supply Chain Solutions (ISCS) & Global Forwarding", "Global Supply Chain Management & Integrated Logistics Solutions",
        "is a global supply chain powerhouse backed by the TVS heritage, managing over 30 million sq ft of specialized warehousing across 25+ countries",
        [0.75, 0.92, 0.95, 0.95, 0.86, 0.78],
        {"political": "Key partner for defense procurement supply chains and automotive manufacturing under Make in India.", "economic": "Resilient multi-currency revenue streams; long-term sticky enterprise contracts with multi-year contract renewals.", "social": "Deep roots in the 110-year TVS corporate ethics culture, trusted for supply chain integrity and worker safety.", "technological": "Proprietary supply chain tech suite (Msys, Lsys, e-Connect), automated guided vehicles (AGVs) in assembly plants, and automated inventory replenishment.", "legal": "International trade compliance, customs regulations across 25 countries, and defense quality accreditations.", "environmental": "Constructs energy-efficient green warehouses, optimizes parts packaging to eliminate plastic, and deploys electric logistics vehicles."},
        [0.22, 0.48, 0.38, 0.20, 0.65],
        {"threat_of_new_entrants": "Low; building global multi-country automotive parts sequencing and procurement engineering requires decades of credibility.", "bargaining_power_of_buyers": "Moderate; multinational industrial clients negotiate SLAs, but cannot risk production line stoppages.", "bargaining_power_of_suppliers": "Low; diversified logistics and transport vendors globally.", "threat_of_substitutes": "Low for complex integrated manufacturing logistics.", "competitive_rivalry": "Moderate; competes with Mahindra Logistics and international 3PL giants (DHL, Kuehne+Nagel)."}
    )
]

for item in sector20_data:
    add_c(*item)

print(f"Sector 20 added: {len(sector20_data)} companies. Total: {len(part4_a)}")

# ==============================================================================
# SECTOR 21: Aviation, Travel, Hospitality & Dining (22 companies)
# ==============================================================================
sector21_data = [
    (
        "InterGlobe Aviation (IndiGo)", "Aviation, Travel, Hospitality & Dining",
        "air travelers, corporate executives, vacationing families, and budget flyers across India and 30+ international destinations",
        "demand reliable, hassle-free, and affordable point-to-point air travel with guaranteed on-time departures and clean aircraft",
        "IndiGo Scheduled Air Services, 6E Prime & International Network", "Low-Cost Airline & National Commercial Aviation Market Leader",
        "rules Indian aviation with over 60% domestic market share, operating a massive single-family fleet of 350+ Airbus A320neos with world-class on-time punctuality",
        [0.82, 0.94, 0.98, 0.96, 0.88, 0.75],
        {"political": "Critical national transport lifeline; major partner in Government of India's UDAN regional connectivity scheme.", "economic": "Phenomenal operational efficiency with lowest cost per available seat kilometer (CASK); placed historic 500-aircraft order with Airbus.", "social": "Democratized air travel in India, making flying affordable for tens of millions of first-time middle-class passengers.", "technological": "Fuel-efficient Airbus A320neo and A321XLR aircraft, high-speed automated passenger bag drops, and digital AI customer service bot (6Eskai).", "legal": "Strict adherence to DGCA aviation safety directives, airport slot allocation rules, and international ICAO standards.", "environmental": "Operates one of the world's youngest and most fuel-efficient aircraft fleets, cutting fuel burn and carbon emissions by over 15% per seat."},
        [0.15, 0.50, 0.45, 0.25, 0.68],
        {"threat_of_new_entrants": "Low; aircraft leasing capital, pilot recruitment, airport terminal slots, and safety certifications form an impenetrable barrier.", "bargaining_power_of_buyers": "Moderate; air travelers compare ticket prices across booking portals, but prefer IndiGo for punctuality and route frequency.", "bargaining_power_of_suppliers": "High; aircraft engine makers (Pratt & Whitney, CFM International) and aviation turbine fuel suppliers hold pricing power.", "threat_of_substitutes": "Moderate from high-speed trains (Vande Bharat) for short routes (<500 km); zero for long-distance and international travel.", "competitive_rivalry": "Moderate; dominates the domestic sky with Air India Group as its sole consolidated full-service competitor."}
    ),
    (
        "Air India", "Aviation, Travel, Hospitality & Dining",
        "international long-haul travelers, Indian diaspora worldwide, and full-service premium business executives",
        "need non-stop direct international flights to the US, Europe, and Asia, luxurious lie-flat business class, and gracious Indian hospitality",
        "Air India International Non-Stop Routes & Vihaan.AI Transformation", "Full-Service Global Sovereign Carrier & Premium Long-Haul Aviation",
        "is undergoing a historic multi-billion dollar transformation under the Tata Group, ordering 470 modern Boeing and Airbus jets to reclaim global aviation leadership",
        [0.85, 0.94, 0.98, 0.96, 0.88, 0.75],
        {"political": "India's historic flag carrier, restored to its founding Tata roots; key vehicle for national diplomatic soft power and international bilateral flying rights.", "economic": "Privatization unlocked massive private capital; consolidating Air India, Vistara, and Air India Express into a unified multi-segment global powerhouse.", "social": "The legendary Maharaja symbolizes gracious Indian hospitality; connects the global Indian diaspora directly to their homeland.", "technological": "New generation Airbus A350 and Boeing 777X wide-body aircraft, modern in-flight entertainment, Wi-Fi connectivity, and state-of-the-art training academies.", "legal": "International bilateral air service agreements, FAA/EASA international safety certifications, and DGCA flight regulations.", "environmental": "Retiring obsolete fuel-guzzling aircraft in favor of ultra-modern carbon-composite Airbus A350s that cut emissions by 25%."},
        [0.15, 0.48, 0.45, 0.22, 0.65],
        {"threat_of_new_entrants": "Zero; acquiring international bilateral flying rights and wide-body long-haul jets requires billions and sovereign treaties.", "bargaining_power_of_buyers": "Moderate; diaspora travelers value direct non-stop flights from Delhi/Mumbai to New York/London over Gulf transit stops.", "bargaining_power_of_suppliers": "High; Boeing, Airbus, and jet engine manufacturers (GE, Rolls-Royce).", "threat_of_substitutes": "Low for inter-continental long-haul travel.", "competitive_rivalry": "Direct international rivalry with Gulf carriers (Emirates, Qatar Airways); domestic competition with IndiGo."}
    ),
    (
        "Indian Hotels Company (IHCL / Taj)", "Aviation, Travel, Hospitality & Dining",
        "discerning global travelers, luxury seekers, wedding families, and corporate executives",
        "demand peerless, authentic Indian luxury hospitality, iconic royal heritage palaces, and gracious, anticipatory five-star service",
        "Taj Palaces, Vivanta, SeleQtions & Ginger Hotels", "Iconic Luxury Hospitality & Palace Living",
        "is South Asia's largest hospitality enterprise, celebrated globally as the 'World's Strongest Hotel Brand' with iconic living heritage palaces like Taj Lake Palace",
        [0.78, 0.94, 0.98, 0.94, 0.88, 0.82],
        {"political": "Key ambassador for Indian tourism and the national 'Heal in India / Visit India' campaigns; hosted historic global G20 summit delegations.", "economic": "Record financial performance under 'Ahvaan 2025', generating over Rs 6,500 Cr in revenue with high operating margins and zero net debt.", "social": "Tajness represents the pinnacle of Indian warmth and mutual respect; iconic response during 26/11 demonstrated legendary institutional selflessness.", "technological": "Tata Neu super-app integration, computerized central reservation systems, and mobile guest digital check-in.", "legal": "Municipal hotel licensing, heritage building conservation covenants, and food safety standards.", "environmental": "Pioneered 'Paathya' sustainability framework: 100% elimination of single-use plastics across hotels, on-site water bottling plants, and green energy."},
        [0.18, 0.45, 0.35, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; acquiring authentic royal heritage palaces (Udaipur, Jaipur, Hyderabad) and building Taj's century of service trust cannot be duplicated.", "bargaining_power_of_buyers": "Low to moderate; affluent wedding parties and luxury travelers accept premium rack rates for the prestige of the Taj hallmark.", "bargaining_power_of_suppliers": "Low; premier hospitality vendors compete to supply the Taj portfolio.", "threat_of_substitutes": "Low for iconic heritage luxury and palace weddings.", "competitive_rivalry": "Moderate; competes with Oberoi Hotels and ITC Hotels in the luxury tier."}
    ),
    (
        "ITC Hotels", "Aviation, Travel, Hospitality & Dining",
        "luxury business travelers, diplomatic delegations, and gourmet culinary connoisseurs",
        "need opulent, palatial luxury hotels embodying regional Indian dynasty architecture, paired with world-renowned Indian fine dining (Bukhara, Dum Pukht)",
        "ITC Grand Chola, ITC Maurya & Legendary Bukhara Dining", "Responsible Luxury Palaces & World-Class Fine Dining",
        "pioneered 'Responsible Luxury', operating the world's greenest luxury hotel chain with 100% LEED Platinum certified hotels and the iconic Bukhara restaurant",
        [0.78, 0.94, 0.98, 0.92, 0.88, 0.90],
        {"political": "The default choice for visiting world leaders, US Presidents, and heads of state in New Delhi at ITC Maurya; demerging to unlock pure-play hotel value.", "economic": "High average room rates (ARR) and industry-leading food and beverage margins driven by globally celebrated destination restaurants.", "social": "Celebrates India's great architectural empires (Cholas in Chennai, Mauryas in Delhi, Mughals in Agra), showcasing civilizational grandeur.", "technological": "Atmospheric air purification systems (breathe clean air), smart room climate sensors, and culinary precision tandoor kitchens.", "legal": "Municipal hotel and bar licensing, FSSAI high-end culinary compliance, and heritage architectural clearances.", "environmental": "First hotel chain in the world to have 100% of its luxury hotels certified LEED Platinum; over 50% of electrical energy sourced from captive wind and solar."},
        [0.18, 0.45, 0.35, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; building massive 600-room luxury architectural monuments like ITC Grand Chola requires thousands of crores and prime metro land.", "bargaining_power_of_buyers": "Low to moderate; global business travelers and diplomatic delegations prioritize security, prestige, and culinary excellence.", "bargaining_power_of_suppliers": "Low; premier culinary and hotel furnishing suppliers.", "threat_of_substitutes": "Low for state visits and signature culinary dining.", "competitive_rivalry": "Direct rivalry with Taj Hotels and The Oberoi Group in metro hubs."}
    ),
    (
        "EIH Limited (The Oberoi Group)", "Aviation, Travel, Hospitality & Dining",
        "ultra-wealthy global leisure travelers, royalty, and connoisseurs of bespoke personal service",
        "demand the ultimate in personalized luxury, intimate attention to detail, and tranquil resort sanctuaries with private plunge pools",
        "Oberoi Amarvilas, Udaivilas, Rajvilas & Trident Hotels", "Ultra-Luxury Bespoke Hospitality & Destination Resorts",
        "is consistently voted among the top hotel brands in the world by Travel + Leisure, delivering unmatched personal service overlooking the Taj Mahal (Amarvilas)",
        [0.76, 0.94, 0.98, 0.94, 0.88, 0.80],
        {"political": "Showcases India's apex luxury hospitality to the world's most influential travelers, heads of state, and celebrities.", "economic": "Highest Average Room Rates (ARR) in the Indian resort sector; high operating margins and low debt with significant promoter and institutional backing.", "social": "Founded by Rai Bahadur M.S. Oberoi; established the Oberoi Centre of Learning and Development (OCLD), grooming India's finest hoteliers.", "technological": "High-tech touchless guest room automation, motorized blackout blinds, and precision water purification.", "legal": "Luxury hotel licensing, environmental clearances, and heritage tourism compliances.", "environmental": "Eco-friendly resort designs with indigenous stone masonry, natural water ponds, and zero-plastic guest room amenities."},
        [0.18, 0.42, 0.30, 0.18, 0.55],
        {"threat_of_new_entrants": "Low; owning unobstructed views of the Taj Mahal (Amarvilas) and multi-acre Lake Pichola shoreline (Udaivilas) is an unassailable geographic moat.", "bargaining_power_of_buyers": "Low; ultra-luxury travelers willingly pay $800 to $2,000+ per night for Oberoi's legendary perfection.", "bargaining_power_of_suppliers": "Low; elite suppliers.", "threat_of_substitutes": "Low in the ultra-luxury leisure tier.", "competitive_rivalry": "Exclusive competition with Taj Hotels for the title of India's finest luxury brand."}
    ),
    (
        "Lemon Tree Hotels", "Aviation, Travel, Hospitality & Dining",
        "business travelers, cost-conscious corporate executives, and road-trip tourists across 50+ Indian cities",
        "need fresh, contemporary, and reliable midscale business hotel rooms with comfortable beds, clean bathrooms, and complimentary Wi-Fi at sensible prices",
        "Lemon Tree Premier, Lemon Tree Hotels & Red Fox", "Mid-Priced Business Hotel Chain & Inclusive Hospitality",
        "is India's largest mid-priced hotel chain, operating 100+ hotels with a unique socially inclusive philosophy where ~15% of employees are Opportunity Deprived Indians",
        [0.72, 0.90, 0.95, 0.92, 0.86, 0.78],
        {"political": "Celebrated national case study for inclusive hiring: employs speech and hearing-impaired individuals across front and back-of-house operations.", "economic": "Rapid expansion via asset-light hotel management contracts; opened India's largest hotel (669-room Aurika Mumbai Skycity) near Mumbai International Airport.", "social": "Pioneered barrier-free, compassionate employment for differently-abled citizens while offering cheerful, accessible lodging to middle-class travelers.", "technological": "Centralized hotel revenue management algorithms, dynamic room pricing, and digital guest self-service kiosks.", "legal": "Municipal hotel commercial licenses, food safety compliance, and disability rights access legislation.", "environmental": "All new hotels designed to IGBC Gold green building standards; solar water heating and wastewater recycling across properties."},
        [0.24, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; midscale hotel management requires strong corporate sales relationships and central reservation systems.", "bargaining_power_of_buyers": "Moderate; corporate travel managers negotiate negotiated corporate room rates across hotel chains.", "bargaining_power_of_suppliers": "Low; diversified hotel linen, food, and maintenance vendors.", "threat_of_substitutes": "Moderate from budget hotel aggregators and alternative midscale brands.", "competitive_rivalry": "Moderate to high with Ginger (IHCL), Fortune (ITC), and Ibis (Accor)."}
    ),
    (
        "Chalet Hotels", "Aviation, Travel, Hospitality & Dining",
        "international business executives, transit travelers, and high-end convention delegates",
        "need upscale, high-room-inventory luxury business hotels strategically situated in gateway airport and commercial business districts",
        "JW Marriott Sahar, Westin Powai & Bengaluru Marriott Whitefield", "Owner & Developer of High-End Luxury Business Hotels",
        "is a premier owner and asset manager of high-end business hotels partnered with global hospitality giants (Marriott, Accor), located in prime metro hubs",
        [0.74, 0.92, 0.96, 0.94, 0.86, 0.78],
        {"political": "Complies with municipal commercial development zoning and environmental regulations in Mumbai, Hyderabad, Bengaluru, and NCR.", "economic": "High operating profitability: large-format hotels (>400 rooms) achieve massive economies of scale with high convention and corporate occupancy.", "social": "Provides state-of-the-art international convention venues and executive hospitality supporting foreign direct investment and business conferences.", "technological": "High-efficiency building management systems, advanced air handling units with MERV-14 filtration, and automated energy optimization.", "legal": "International hotel management agreements (HMAs) with Marriott International, local liquor licenses, and building safety codes.", "environmental": "All operational hotels are certified USGBC LEED or IGBC green buildings, powered by captive renewable wind and solar energy."},
        [0.22, 0.48, 0.35, 0.20, 0.62],
        {"threat_of_new_entrants": "Low; developing 400-to-600-room five-star hotels adjacent to Mumbai International Airport requires immense capital and prime land parcels.", "bargaining_power_of_buyers": "Moderate; corporate accounts and airline crew contracts negotiate volume room blocks.", "bargaining_power_of_suppliers": "Moderate; global hotel brand franchisors (Marriott) set strict brand standard audits.", "threat_of_substitutes": "Moderate from competing luxury business hotels.", "competitive_rivalry": "Moderate; dominates airport and IT hub sub-markets in Mumbai and Bengaluru."}
    ),
    (
        "MakeMyTrip", "Aviation, Travel, Hospitality & Dining",
        "leisure travelers, family vacationers, corporate professionals, and holiday bookers nationwide",
        "need a comprehensive, reliable one-stop platform for flights, verified hotel reviews, holiday packages, bus tickets, and train reservations",
        "MakeMyTrip Super-App, Goibibo & RedBus Multi-Modal Travel", "India's Apex Online Travel Agency (OTA) & Multi-Modal Booking Platform",
        "commands over 50% of the Indian online travel market across MakeMyTrip, Goibibo, and RedBus, powering hundreds of millions of travel bookings annually",
        [0.75, 0.94, 0.98, 0.96, 0.85, 0.72],
        {"political": "Direct beneficiary of national tourism promotion, airport expansion, and digital payment infrastructure (UPI).", "economic": "Listed on NASDAQ; achieved sustained GAAP profitability driven by high hotel take-rates, advertising monetization, and corporate travel bookings.", "social": "Pioneered online flight booking and vacation planning in India, liberating citizens from traditional brick-and-mortar travel agency queues.", "technological": "AI-powered travel search algorithms, dynamic hotel pricing integration, vernacular voice search in multiple Indian languages, and instant refund processing.", "legal": "Consumer protection e-commerce rules, airline ticketing agency compliance (IATA), and DPDP Act personal travel data privacy.", "environmental": "Promotes eco-certified hotels, provides carbon-offset options for flight bookings, and reduces paper tickets with 100% digital boarding passes."},
        [0.22, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; network effects of connecting thousands of hotels, airlines, and bus operators with 70+ million users is an insurmountable moat.", "bargaining_power_of_buyers": "Moderate; consumers browse prices on meta-search engines, but book on MMT for reliability and loyalty rewards.", "bargaining_power_of_suppliers": "Moderate; airlines have thin margins, but independent hotels rely heavily on MakeMyTrip for occupancy.", "threat_of_substitutes": "Moderate from direct airline/hotel websites.", "competitive_rivalry": "Moderate; dominates the Indian OTA space ahead of EaseMyTrip, Yatra, and Cleartrip."}
    ),
    (
        "EaseMyTrip (Easy Trip Planners)", "Aviation, Travel, Hospitality & Dining",
        "budget-conscious air travelers, families, and travel agents seeking transparent, zero-fee flight bookings",
        "demand transparent, unbundled flight ticketing without hidden convenience fees added at the final checkout screen",
        "Zero-Convenience-Fee Flight Bookings & Travel Services", "Bootstrapped Profitable Online Travel Agency (OTA)",
        "built India's only consistently profitable, bootstrapped online travel unicorn by pioneering 'No Convenience Fee' air ticketing on transparent pricing",
        [0.72, 0.90, 0.96, 0.94, 0.85, 0.70],
        {"political": "Aligned with consumer welfare and transparency directives regarding hidden e-commerce travel ticketing surcharges.", "economic": "Bootstrapped to public market listing without external venture capital burn; leanest operational employee cost-to-booking ratio in the industry.", "social": "Eliminated the consumer anger of discovering surprise 300-rupee convenience fees right before paying for flight tickets.", "technological": "Proprietary lean algorithmic booking engine, automated airline GDS integration, and automated cancellation processing.", "legal": "IATA travel agency accreditations, consumer protection rules, and statutory listing disclosures.", "environmental": "Paperless digital flight ticketing and partnership with eco-conscious hotel properties."},
        [0.26, 0.55, 0.35, 0.25, 0.72],
        {"threat_of_new_entrants": "Moderate; travel software is accessible, but building consumer trust and securing IATA airline credit lines requires capital.", "bargaining_power_of_buyers": "High; price-sensitive flyers choose EaseMyTrip specifically to save the Rs 300-400 convenience fee.", "bargaining_power_of_suppliers": "High; domestic airlines set base ticket commissions.", "threat_of_substitutes": "High from MakeMyTrip and direct airline websites.", "competitive_rivalry": "Fierce rivalry with MakeMyTrip, Cleartrip, and Yatra."}
    ),
    (
        "Yatra Online", "Aviation, Travel, Hospitality & Dining",
        "corporate enterprises, business travelers, and leisure holiday seekers",
        "need comprehensive corporate travel expense management, corporate hotel negotiated rates, and managed employee flight booking workflows",
        "Corporate Travel Management Platform & Yatra Consumer Holidays", "Enterprise Corporate Travel & Consumer OTA Solutions",
        "is India's largest corporate travel services provider, servicing over 800 large corporate clients with automated travel booking and expense reporting software",
        [0.72, 0.90, 0.95, 0.94, 0.85, 0.72],
        {"political": "Compliant with corporate travel tax compliance, GST input tax credit reconciliation, and national travel policies.", "economic": "Sticky corporate B2B contracts provide stable, high-volume recurring transaction revenue with lower customer acquisition costs than B2C.", "social": "Streamlines business travel for hundreds of thousands of corporate executives, integrating company travel policies and approval workflows.", "technological": "Proprietary corporate travel expense management platform, automated policy compliance engines, and dynamic airline/hotel rate caching.", "legal": "IATA certifications, corporate travel procurement agreements, and consumer privacy compliances.", "environmental": "Corporate carbon footprint reporting tools enabling enterprise clients to track and offset business travel emissions."},
        [0.26, 0.52, 0.35, 0.24, 0.70],
        {"threat_of_new_entrants": "Moderate; building enterprise ERP-integrated corporate travel software and managing corporate credit lines is a barrier.", "bargaining_power_of_buyers": "Moderate; corporate clients negotiate corporate rates, but value Yatra's policy compliance automation.", "bargaining_power_of_suppliers": "Moderate; commercial airlines and business hotel chains.", "threat_of_substitutes": "Moderate from MakeMyTrip MyBiz and American Express Global Business Travel.", "competitive_rivalry": "High with MakeMyTrip in corporate and leisure travel."}
    ),
    (
        "OYO Rooms (Oravel Stays)", "Aviation, Travel, Hospitality & Dining",
        "budget travelers, young professionals, tourists, and small business travelers across India and 35+ countries",
        "need clean, standardized, and affordable hotel rooms with guaranteed AC, clean linen, free Wi-Fi, and instant mobile booking",
        "OYO Standardized Budget Hotels & OYO Townhouse", "Technology-Driven Budget Hospitality Ecosystem",
        "standardized the chaotic unorganized budget hotel industry across thousands of small independent hotels with automated hotel management software",
        [0.70, 0.90, 0.96, 0.95, 0.82, 0.68],
        {"political": "Complies with municipal hotel licensing norms, local police guest reporting rules, and national tourism guidelines across 35 countries.", "economic": "Turnaround to sustained EBITDA profitability; asset-light franchise revenue-share model with minimal physical capital expenditure.", "social": "Democratized reliable, standardized budget travel for millions of young Indians, students, and tier-2/3 business travelers.", "technological": "Patented proprietary OS for hotel owners (Co-OYO), automated dynamic room pricing algorithms, and instant mobile room check-in.", "legal": "Consumer protection regulations, hotel partner arbitration agreements, and local lodging tax compliances.", "environmental": "Promotes energy-efficient LED lighting and digital paperless billing across thousands of budget properties."},
        [0.30, 0.58, 0.35, 0.30, 0.75],
        {"threat_of_new_entrants": "Moderate; basic hotel aggregation apps exist, but OYO's massive brand recall and partner hotel network form a barrier.", "bargaining_power_of_buyers": "High; budget travelers readily compare prices on Google and travel apps for the cheapest clean room.", "bargaining_power_of_suppliers": "Moderate; independent hotel owners negotiate revenue-share commissions.", "threat_of_substitutes": "High from local standalone budget lodges, homestays, and Airbnb.", "competitive_rivalry": "Intense with Treebo, FabHotels, and standalone budget lodgings."}
    ),
    (
        "Jubilant FoodWorks", "Aviation, Travel, Hospitality & Dining",
        "pizza lovers, families, youth, and corporate professionals seeking fast, delicious meals",
        "need piping-hot, customized pizzas and Italian sides delivered reliably to their doorstep in under 20-30 minutes",
        "Domino's Pizza Delivery Network & Hong's Kitchen", "Master QSR Franchisee & Food Delivery Technology Leader",
        "is India's largest Quick Service Restaurant (QSR) operator with 2,000+ Domino's outlets, pioneering the 30-minute delivery guarantee and localized pizza toppings",
        [0.70, 0.92, 0.96, 0.95, 0.84, 0.74],
        {"political": "Complies with FSSAI food hygiene standards, packaging commodity regulations, and GST restaurant service rules.", "economic": "Phenomenal return on capital employed (>20%) driven by high store-level throughput, backward-integrated commissary dough supply, and app-driven direct orders.", "social": "Domino's Pizza is the definitive celebratory treat for Indian birthdays, game nights, and family weekend gatherings.", "technological": "Proprietary high-frequency pizza delivery routing algorithms, central automated dough manufacturing commissaries, and fast electric delivery tracking.", "legal": "Exclusive master franchise agreements with Domino's Pizza International, FSSAI licensing, and weights & measures compliance.", "environmental": "Transitioning to 100% electric delivery 2-wheelers and using certified recyclable cardboard pizza boxes."},
        [0.24, 0.50, 0.35, 0.25, 0.72],
        {"threat_of_new_entrants": "Low to moderate; replicating Jubilant's 2,000-store delivery network and central dough commissary supply chain takes decades.", "bargaining_power_of_buyers": "Moderate; consumers have many food choices, but Domino's delivers unmatched value combinations (Everyday Value Offers).", "bargaining_power_of_suppliers": "Low; backward-integrated mega commissaries produce their own dough, sauces, and cheese blends.", "threat_of_substitutes": "High from cloud kitchens (Oven Story), burgers, and local street pizzerias.", "competitive_rivalry": "Moderate to high with Pizza Hut and modern gourmet pizza brands."}
    ),
    (
        "Devyani International", "Aviation, Travel, Hospitality & Dining",
        "fried chicken enthusiasts, pizza lovers, and coffee seekers across India, Nigeria, and Nepal",
        "need crispy, authentic fried chicken (KFC), pan pizzas (Pizza Hut), and artisanal coffee (Costa Coffee) delivered with international quality standards",
        "KFC Fried Chicken, Pizza Hut & Costa Coffee QSR Outlets", "Multi-Brand Quick Service Restaurant (QSR) Powerhouse",
        "operates over 1,700 QSR restaurants across India as the largest franchisee of Yum! Brands, delivering iconic KFC crispy chicken and Costa Coffee",
        [0.70, 0.92, 0.96, 0.94, 0.84, 0.74],
        {"political": "Complies with national food safety and hygiene regulations, agricultural poultry sourcing norms, and local shop licensing.", "economic": "Rapid store expansion trajectory across Tier-1, 2, and 3 Indian cities; KFC brand delivers industry-leading average daily sales (ADS) per store.", "social": "KFC's signature secret recipe fried chicken is a cult favorite among Indian youth and non-vegetarian food lovers.", "technological": "Automated computerized pressure fryers, digital self-order kiosks in restaurants, and integration with Swiggy and Zomato.", "legal": "Exclusive Yum! Brands franchise territory rights, FSSAI central food processing licenses, and labor welfare compliances.", "environmental": "100% sustainable paper packaging wraps, used cooking oil recycling into biodiesel, and energy-efficient kitchen equipment."},
        [0.25, 0.52, 0.38, 0.25, 0.72],
        {"threat_of_new_entrants": "Low; securing exclusive global QSR brand rights and building a 1,700-restaurant retail chain requires immense institutional capital.", "bargaining_power_of_buyers": "Moderate; consumers love KFC's secret recipe, but switch between fast food options based on cravings.", "bargaining_power_of_suppliers": "Moderate; biosecure poultry suppliers (Venky's) and global food ingredient blenders.", "threat_of_substitutes": "High from local fried chicken outlets, burgers, and biryani.", "competitive_rivalry": "Direct rivalry with Sapphire Foods, McDonald's, and Domino's."}
    ),
    (
        "Westlife Foodworld", "Aviation, Travel, Hospitality & Dining",
        "families, children, college youth, and breakfast seekers across Western and Southern India",
        "demand iconic, consistent burgers, crispy golden fries, McCafé artisanal beverages, and convenient highway drive-thrus",
        "McDonald's India (West & South), McAloo Tikki, Big Spicy & McCafé", "Exclusive McDonald's Master Franchisee & Drive-Thru Pioneer",
        "operates 380+ McDonald's restaurants in West and South India, having localized the global menu with the iconic McAloo Tikki and McCafé coffee",
        [0.70, 0.92, 0.96, 0.94, 0.84, 0.74],
        {"political": "Complies with FSSAI regulations, local health safety norms, and municipal commercial establishment licensing.", "economic": "High return on capital; McCafé and Drive-Thrus drive high average bill values and lucrative breakfast and late-night snacking occasions.", "social": "McAloo Tikki revolutionized affordable dining in India, creating a welcoming family dining destination for children and birthday celebrations.", "technological": "Experience of the Future (EOTF) restaurants with digital self-ordering touchscreens, mobile app ordering, and automated kitchen conveyor assembly.", "legal": "Exclusive master development license from McDonald's Corporation, FSSAI hygiene ratings, and trademark protection.", "environmental": "Used cooking oil converted into 100% biodiesel for delivery trucks; zero plastic cutlery and paper cup recycling."},
        [0.24, 0.50, 0.38, 0.24, 0.72],
        {"threat_of_new_entrants": "Low; building a 380-store prime retail network and an unbroken cold-chain supply for fresh lettuce and potatoes takes decades.", "bargaining_power_of_buyers": "Moderate; consumers love McDonald's taste consistency and value meal pricing.", "bargaining_power_of_suppliers": "Low; dedicated agricultural contract suppliers (Vista Processed Foods, McCain) supply exclusively to McDonald's specifications.", "threat_of_substitutes": "High from local burger joints, KFC, and street food.", "competitive_rivalry": "High with Burger King India, KFC, and Subway."}
    ),
    (
        "Sapphire Foods India", "Aviation, Travel, Hospitality & Dining",
        "fast food lovers, mall shoppers, and delivery consumers in South and West India and Sri Lanka",
        "require fast, hygienic, and delicious fried chicken, pizzas, and snacks served in modern high-street and mall food court locations",
        "KFC & Pizza Hut Restaurant Networks (South & West India)", "Leading Multi-Brand QSR Restaurant Operator",
        "operates over 850 KFC and Pizza Hut restaurants across India and Sri Lanka, driving disciplined restaurant-level profitability and omnichannel delivery",
        [0.70, 0.92, 0.96, 0.94, 0.84, 0.74],
        {"political": "Complies with FSSAI guidelines, foreign investment regulations in food retail, and local commercial zoning.", "economic": "Disciplined capital allocation; rapid restaurant rollout in Tier-2 and Tier-3 towns delivering high restaurant-level EBITDA margins.", "social": "Brings international dining experiences to non-metro families, creating high-trust celebratory dining venues.", "technological": "Automated kitchen display systems (KDS), omnichannel order aggregation, and automated fryer temperature controls.", "legal": "Yum! Brands franchise agreements, FSSAI food licensing, and labor law compliances.", "environmental": "Sustainable poultry sourcing ethics, reduction in single-use plastic, and conversion of cooking oil waste into biofuel."},
        [0.25, 0.52, 0.38, 0.25, 0.72],
        {"threat_of_new_entrants": "Low; global brand franchise exclusivity and capital hurdles create strong entry barriers.", "bargaining_power_of_buyers": "Moderate; diners compare fast food options.", "bargaining_power_of_suppliers": "Moderate; certified poultry and dairy cheese vendors.", "threat_of_substitutes": "High from burgers and local street food.", "competitive_rivalry": "Direct operational benchmark against Devyani International."}
    ),
    (
        "Barbeque Nation Hospitality", "Aviation, Travel, Hospitality & Dining",
        "large family gatherings, corporate team celebrations, and food lovers seeking unlimited buffet indulgence",
        "demand unlimited, multi-cuisine barbecued kebabs grilled live on their personal table skewers, followed by an expansive buffet feast",
        "Live Table Grill Dining, Unlimited Buffet & Toscano Italian", "Casual Dining Live-Grill Buffet Restaurant Chain",
        "pioneered the live-on-the-table grilling concept in India with 200+ restaurants, delivering unlimited succulent kebabs, main courses, and kulfis at fixed prices",
        [0.68, 0.90, 0.96, 0.90, 0.84, 0.72],
        {"political": "Complies with municipal restaurant licenses, fire safety clearances, and FSSAI culinary standards.", "economic": "Fixed per-head buffet pricing ensures high average spend and predictable group dining revenues; expanded into premium Italian dining with Toscano.", "social": "The definitive celebration hub for Indian corporate promotions, family birthdays, and anniversaries with personalized celebration cakes.", "technological": "Patented recessed table charcoal/electric grill mechanisms, centralized commissary marination, and digital guest feedback tablets.", "legal": "FSSAI food hygiene licensing, labor welfare compliances, and corporate listing governance.", "environmental": "Smokeless electric table grill technology reducing indoor particulate smoke and energy-efficient kitchen ventilation."},
        [0.26, 0.50, 0.35, 0.25, 0.68],
        {"threat_of_new_entrants": "Moderate; replicating Barbeque Nation's 200-restaurant footprint and operational buffet supply chain requires scale.", "bargaining_power_of_buyers": "Moderate; diners appreciate unlimited value, but have many casual dining options.", "bargaining_power_of_suppliers": "Low; bulk direct procurement of meats, vegetables, and paneer.", "threat_of_substitutes": "High from a-la-carte restaurants and local barbecue grills.", "competitive_rivalry": "Moderate; dominates live-grill buffet dining ahead of Absolute Barbecues (AB's)."}
    ),
    (
        "Rebel Foods", "Aviation, Travel, Hospitality & Dining",
        "digital food delivery orderers, office desk diners, and late-night culinary cravers",
        "need piping-hot, high-quality biryanis, wraps, pizzas, and desserts delivered to their doorstep in minutes from trusted digital food brands",
        "Faasos Wraps, Behrouz Biryani, Oven Story Pizza & Wendy's India", "World's Largest Cloud Kitchen Internet Restaurant Company",
        "is the world's largest cloud kitchen company with 450+ dark kitchens across 10 countries, operating 10+ digital brands from a single kitchen footprint",
        [0.70, 0.92, 0.96, 0.96, 0.84, 0.70],
        {"political": "Complies with FSSAI cloud kitchen food safety standards, gig delivery coordination, and municipal health trade licenses.", "economic": "Unmatched capital efficiency: operates 10 distinct restaurant brands (Behrouz, Faasos, Oven Story) out of a single shared kitchen space, maximizing rent productivity.", "social": "Pioneered internet restaurant dining in India; Behrouz Biryani redefined royal packaged biryani gifting for Indian celebrations.", "technological": "Rebel Operating System (ROS) automating inventory, robotic automated wok fryers and induction cookers, and AI order dispatch.", "legal": "FSSAI central food licenses, digital food aggregator agreements, and trademark protection across global brands.", "environmental": "Dark kitchen models eliminate sprawling dining real estate and reduce food waste through centralized ingredient preparation."},
        [0.28, 0.55, 0.35, 0.28, 0.75],
        {"threat_of_new_entrants": "Moderate; launching a single cloud kitchen is easy, but scaling 450 multi-brand hubs to unicorn valuation requires deep software mastery.", "bargaining_power_of_buyers": "High; consumers browse hundreds of competing restaurants on Swiggy and Zomato.", "bargaining_power_of_suppliers": "Low; bulk centralized procurement of meats, rice, and packaging.", "threat_of_substitutes": "High from physical restaurants and competing cloud kitchens.", "competitive_rivalry": "High with Curefoods, EatClub (Box8), and local dark kitchens."}
    ),
    (
        "Chaayos (Sunshine Teahouse)", "Aviation, Travel, Hospitality & Dining",
        "tea lovers, modern office workers, and youth seeking fresh, customized chai in aesthetic cafe environments",
        "crave authentic, freshly brewed Indian chai customized to their exact preferences (adrak, tulsi, elaichi, milk thickness) alongside nostalgic snacks",
        "Customized Fresh Chai (80,000 combinations) & Chai Monk Brewing", "Modern Chai Cafe Chain & Automated IoT Tea Technology",
        "modernized India's favorite beverage with 200+ stylish cafes, brewing fresh custom chai to 80,000 personalized combinations using proprietary 'Chai Monk' robotics",
        [0.68, 0.90, 0.96, 0.94, 0.82, 0.74],
        {"political": "Complies with municipal shop licenses, food safety regulations, and tea board sourcing guidelines.", "economic": "High-margin repeat consumption: chai is consumed multiple times daily; high average order value driven by bundled bun maska and samosas.", "social": "Created clean, air-conditioned neighborhood social hubs where young professionals and friends can relax over a hot cutting chai.", "technological": "Patented 'Chai Monk' automated robotic tea brewing machines that deliver consistent custom brew recipes in under 2 minutes without human error.", "legal": "FSSAI licensing, patent protection on Chai Monk automated brewing hardware, and trademark protection.", "environmental": "Eliminates plastic cups in favor of traditional terracotta kulhads and recyclable paper takeaway flasks."},
        [0.28, 0.52, 0.35, 0.28, 0.70],
        {"threat_of_new_entrants": "Moderate; anyone can brew tea, but Chaayos's Chai Monk technology and 200 high-street locations form a solid moat.", "bargaining_power_of_buyers": "Moderate; consumers love their specific custom chai recipe and return daily.", "bargaining_power_of_suppliers": "Low; direct estate sourcing of tea leaves, spices, and fresh dairy milk.", "threat_of_substitutes": "High from traditional roadside chai tapris and coffee cafes.", "competitive_rivalry": "Direct rivalry with Chai Point and modern coffee chains."}
    ),
    (
        "Chai Point (Mountain Trail Foods)", "Aviation, Travel, Hospitality & Dining",
        "corporate office campuses, tech park workers, and transit commuters",
        "need instant access to freshly brewed hot chai, filter coffee, and healthy snacks delivered directly into office pantries or transit hubs",
        "Chai Point Cafes, myChai Box & IoT Automated Box Dispensers", "Omnichannel Chai Ecosystem & Automated Corporate Tea Dispensers",
        "serves over 700,000 cups of tea daily through an omnichannel model combining high-street cafes, disposable heat-retaining chai flasks, and IoT office dispensers",
        [0.68, 0.90, 0.96, 0.94, 0.82, 0.74],
        {"political": "Complies with municipal food business norms and FSSAI health and safety guidelines.", "economic": "Lucrative corporate B2B contracts: IoT tea dispenser machines installed in Fortune 500 tech offices provide steady high-margin recurring cash flows.", "social": "Transformed office tea breaks with hygienic, fresh leaf tea, replacing stale vending machine tea powders across corporate India.", "technological": "Proprietary SHARK IoT cloud platform powering corporate tea dispensers, heat-retaining multi-layer cardboard flasks keeping tea hot for 60 minutes.", "legal": "FSSAI food licenses, patent protection on disposable chai flask packaging, and corporate lease contracts.", "environmental": "Pioneered 100% biodegradable heat-retaining paper flasks and bagasse sugarcane pulp snack containers."},
        [0.28, 0.52, 0.35, 0.28, 0.70],
        {"threat_of_new_entrants": "Moderate; building a corporate pantry IoT dispenser network across thousands of offices requires capital and maintenance teams.", "bargaining_power_of_buyers": "Moderate; corporate facility managers evaluate machine uptime and beverage taste.", "bargaining_power_of_suppliers": "Low; direct tea garden partnerships in Assam and Nilgiris.", "threat_of_substitutes": "High from Chaayos, roadside tea stalls, and office coffee machines.", "competitive_rivalry": "Direct rivalry with Chaayos in retail cafes."}
    ),
    (
        "Wow! Momo Foods", "Aviation, Travel, Hospitality & Dining",
        "youth, college students, mall shoppers, and street food lovers across India",
        "demand clean, delicious, and innovative momos (dumplings), momo burgers (MoBurg), and sizzling Indo-Chinese meals at accessible prices",
        "Wow! Momo, MoBurg, Wow! China & Wow! Chicken", "India's Largest Home-Grown QSR & Ethnic Dumpling Chain",
        "is India's largest home-grown QSR chain with 650+ outlets across 38 cities, transforming unorganized Himalayan momos into an organized QSR sensation",
        [0.68, 0.92, 0.96, 0.92, 0.82, 0.72],
        {"political": "Supports domestic entrepreneurship and youth QSR employment under Make in India.", "economic": "Rapid growth with compact kiosk formats (150-300 sq ft) in metro stations and mall food courts delivering fast store breakeven and high capital turns.", "social": "Cultural icon of youth snacking, popularizing innovative fusion concepts like 'MoBurg' (momo burger) and pan-fried momos in spicy schezwan sauce.", "technological": "Centralized automated frozen momo manufacturing plants with cryogenic IQF freezing, and standardized steam and fry cooking protocols.", "legal": "FSSAI food hygiene licensing, metro station retail lease concessions, and trademark protections.", "environmental": "Eliminated plastic plates in favor of biodegradable corn-starch containers and eco-friendly paper takeaway boxes."},
        [0.28, 0.52, 0.35, 0.28, 0.70],
        {"threat_of_new_entrants": "Moderate; momos are made by street vendors everywhere, but matching Wow! Momo's 650-store brand trust and hygiene is hard.", "bargaining_power_of_buyers": "Moderate; students and office workers love the taste and accessible price points (Rs 99-199).", "bargaining_power_of_suppliers": "Low; centralized procurement of flour, chicken, and vegetables.", "threat_of_substitutes": "High from local street momo vendors and fast food chains.", "competitive_rivalry": "Low to moderate; undisputed organized market leader in dumplings and ethnic momos."}
    ),
    (
        "Biryani By Kilo (SkyGate Hospitality)", "Aviation, Travel, Hospitality & Dining",
        "biryani connoisseurs, family dinner celebrators, and premium culinary delivery lovers",
        "demand authentic, freshly cooked dum biryani prepared individually in natural earthen clay pots (handis) rather than mass-reheated commercial batches",
        "Individual Handi Dum Biryani & Galouti Kebabs", "Authentic Earthen Pot Dum Biryani & Royal Nizami Cuisine",
        "delivers authentic Nizami and Awadhi biryanis slow-cooked individually in fresh earthen handis and delivered with self-heating candle kits (Aangi)",
        [0.68, 0.90, 0.96, 0.92, 0.84, 0.74],
        {"political": "Complies with FSSAI regulations, central kitchen hygiene protocols, and packaging safety rules.", "economic": "High average order values (>Rs 800) and strong repeat order frequency; operating 100+ delivery and dine-in outlets across 45 Indian cities.", "social": "Celebrates India's rich royal culinary heritage, turning biryani delivery into an authentic slow-food celebration with traditional earthen pottery.", "technological": "Individual portion clay handi sealing with dough, proprietary 'Aangi' portable candle warming stoves, and centralized spice blend kitchens.", "legal": "FSSAI food licensing, trademark protection, and delivery aggregator agreements.", "environmental": "Uses 100% natural clay earthen handis sourced from rural potters, providing rural artisan livelihoods and biodegradable dining packaging."},
        [0.28, 0.50, 0.35, 0.26, 0.70],
        {"threat_of_new_entrants": "Moderate; biryani is the most ordered dish in India, but delivering individual fresh dum handis with consistent flavor is operationally complex.", "bargaining_power_of_buyers": "Moderate; biryani lovers are fiercely passionate about authentic aroma and long-grain basmati texture.", "bargaining_power_of_suppliers": "Low to moderate; aged basmati rice, direct poultry sourcing, and artisanal earthenware.", "threat_of_substitutes": "High from Behrouz Biryani (Rebel Foods) and local iconic biryani houses (Paradise, Bawarchi).", "competitive_rivalry": "Direct rivalry with Behrouz Biryani and regional biryani legends."}
    ),
    (
        "Speciality Restaurants", "Aviation, Travel, Hospitality & Dining",
        "fine-dining lovers, family celebration parties, and connoisseurs of authentic regional and oriental cuisines",
        "need authentic, sit-down oriental dining (Mainland China), authentic Bengali cuisine (Oh! Calcutta), and traditional barbecue experiences",
        "Mainland China, Oh! Calcutta, Sigree & Asia Kitchen", "Fine-Dining Asian & Regional Heritage Restaurant Chains",
        "has defined fine-dining Chinese and regional cuisine in India for over 30 years with iconic brands like Mainland China and Oh! Calcutta",
        [0.68, 0.90, 0.95, 0.90, 0.84, 0.70],
        {"political": "Complies with state restaurant and bar excise licenses, municipal food hygiene regulations, and fire safety norms.", "economic": "Consistent cash generation from established flagship locations; low debt balance sheet with high average spend per dining guest.", "social": "Mainland China is an iconic dining landmark for family celebratory dinners across Kolkata, Mumbai, Delhi, and Bengaluru.", "technological": "High-heat wok cooking suites, centralized master culinary recipe standardization, and digital guest reservation systems.", "legal": "FSSAI food hygiene licensing, liquor service regulatory compliance, and statutory public corporate reporting.", "environmental": "Energy-efficient kitchen induction ranges, organic composting of kitchen food scraps, and water-efficient pre-rinse dishwashers."},
        [0.25, 0.48, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; independent fine-dining restaurants open frequently, but few sustain multi-city brand trust for 3 decades.", "bargaining_power_of_buyers": "Moderate; diners evaluate food taste, ambiance, and hospitality service.", "bargaining_power_of_suppliers": "Low; authentic oriental sauces, fresh seafood, and premium culinary ingredients.", "threat_of_substitutes": "High from modern contemporary pan-Asian bistros and home delivery.", "competitive_rivalry": "Moderate to high with standalone fine-dining restaurants and luxury hotel dining."}
    )
]

for item in sector21_data:
    add_c(*item)

print(f"Sector 21 added: {len(sector21_data)} companies. Total in Part 4A: {len(part4_a)}")

# Save to scratch/part4_a.json
out_path = Path(__file__).parent / "part4_a.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(part4_a, f, indent=2)

print(f"SUCCESS: Saved {len(part4_a)} companies to {out_path}")
