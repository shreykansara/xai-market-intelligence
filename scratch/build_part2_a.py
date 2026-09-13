"""
Omniscope AI - Part 2A Generator
Builds Sectors 7, 8, 9 (65 companies):
- Sector 7: Biotech, Vaccines & Healthcare Diagnostics (20 companies)
- Sector 8: Hospital Networks & Healthcare Delivery (20 companies)
- Sector 9: FMCG, Personal Care & Packaged Foods (25 companies)
"""
import json
from pathlib import Path

part2_a = []

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    part2_a.append({
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
# SECTOR 7: Biotech, Vaccines & Healthcare Diagnostics (20 companies)
# ==============================================================================
sector7_data = [
    (
        "Serum Institute of India", "Biotech, Vaccines & Healthcare Diagnostics",
        "global sovereign health agencies, GAVI, UNICEF, and developing nation immunization programs",
        "require ultra-affordable, massive-scale pediatric and infectious disease vaccines to protect populations without crippling national health budgets",
        "Covishield, Cervavac & Pentavalent Vaccine Portfolio", "High-Volume Preventive Immunobiological Vaccines",
        "manufactures over 1.5 billion doses annually at world-lowest unit economics, protecting over 65% of the world's children against lethal childhood diseases",
        [0.85, 0.92, 0.98, 0.95, 0.92, 0.70],
        {"political": "Critical national biosecurity partner for Government of India's Universal Immunization Programme and GAVI global vaccine diplomacy.", "economic": "Generates multi-billion dollar export revenues through unmatched manufacturing scale that competitors cannot replicate at similar price points.", "social": "Immense global humanitarian impact, eliminating measles, polio, and rubella in vulnerable demographic segments.", "technological": "Pioneered automated massive-scale bioreactors, high-yield cell-culture platforms, and high-speed multi-dose vial filling lines in Pune.", "legal": "Strict adherence to WHO Prequalification, US FDA, and Indian CDSCO bio-safety and clinical trial protocols.", "environmental": "Operates high-efficiency zero-liquid discharge effluent treatment plants for complex biological and viral waste streams."},
        [0.10, 0.45, 0.35, 0.20, 0.50],
        {"threat_of_new_entrants": "Practically impossible for new entrants given multi-billion dollar capex, specialized BSL-3 facilities, and decades of clinical regulatory trust.", "bargaining_power_of_buyers": "Moderate to low; global health agencies buy in bulk, but few suppliers can match Serum's volume and price guarantee.", "bargaining_power_of_suppliers": "Moderate; depends on specialized single-use bioreactor bags, adjuvants, and vials.", "threat_of_substitutes": "Very low; preventive vaccination remains the most cost-effective medical intervention known to science.", "competitive_rivalry": "Low to moderate globally, dominated by Serum Institute alongside Pfizer, GSK, and Sanofi."}
    ),
    (
        "Bharat Biotech", "Biotech, Vaccines & Healthcare Diagnostics",
        "national governments and public health systems facing endemic infectious disease threats",
        "require indigenous, IP-owned novel vaccines engineered against tropical and emerging viral pathogens",
        "Covaxin, Rotavac & BBV154 Intranasal Vaccine", "Novel Inactivated & Mucosal Vaccines",
        "delivers wholly indigenous, clinically proven vaccines developed via novel Indian antigen platforms and mucosal delivery mechanisms",
        [0.88, 0.84, 0.95, 0.94, 0.90, 0.68],
        {"political": "Pinnacle of Prime Minister's 'Make in India' and 'Atmanirbhar Bharat' biotechnology vision, partnering with ICMR and NIV.", "economic": "Captures high-margin IP ownership on novel vaccines rather than purely contract manufacturing foreign formulations.", "social": "Drastically reduced child mortality from rotavirus diarrhea across rural India through indigenous 1-dollar-a-dose Rotavac.", "technological": "Engineered the world's first approved needle-free intranasal COVID-19 vaccine and specialized Vero cell culture platforms in Genome Valley, Hyderabad.", "legal": "Complex global approval processes with WHO EUL, DCGI authorizations, and international patent prosecution.", "environmental": "Adheres to strict biosafety level 3 (BSL-3) containment and thermal viral inactivation bio-waste management."},
        [0.15, 0.40, 0.30, 0.22, 0.55],
        {"threat_of_new_entrants": "Extremely low; requires advanced BSL-3 infrastructure, deep virology IP, and multi-year clinical trial capabilities.", "bargaining_power_of_buyers": "Moderate; public health procurement tenders negotiate strictly on volume and price.", "bargaining_power_of_suppliers": "Low; backward-integrated into indigenous adjuvants and proprietary cell banks.", "threat_of_substitutes": "Low; vaccines are non-substitutable preventive medicines.", "competitive_rivalry": "Moderate; competes with Serum Institute and multinational biopharma majors for government tenders."}
    ),
    (
        "Biological E Limited", "Biotech, Vaccines & Healthcare Diagnostics",
        "pediatric immunization campaigns and emerging nation health ministries",
        "need reliable, affordable supply of complex multi-component childhood vaccines and protein subunit formulations",
        "Corbevax & Liquid Pentavalent Vaccine", "Recombinant Subunit & Pediatric Combination Vaccines",
        "provides proven, heat-stable combination vaccines with WHO prequalification and high-yield yeast fermentation technology",
        [0.80, 0.82, 0.94, 0.90, 0.88, 0.65],
        {"political": "Integral supplier to India's National Health Mission and UNICEF global vaccine supply pools.", "economic": "Steady multi-year sovereign purchase orders provide resilient revenue stability amidst commercial drug price volatility.", "social": "Protects tens of millions of neonates and toddlers against diphtheria, pertussis, tetanus, hepatitis B, and Hib.", "technological": "Mastered Pichia pastoris yeast expression systems and high-throughput antigen purification.", "legal": "Fully certified across WHO CGMP, Indian DCGI, and international regulatory frameworks.", "environmental": "Implements clean biotechnology processes with low environmental footprint compared to chemical synthetic drug manufacturing."},
        [0.18, 0.42, 0.32, 0.20, 0.52],
        {"threat_of_new_entrants": "Very low; high barrier due to complex combination formulation know-how and WHO audit standards.", "bargaining_power_of_buyers": "Moderate; institutional buyers command volume rebates.", "bargaining_power_of_suppliers": "Low; diverse chemical and consumable sourcing.", "threat_of_substitutes": "Negligible for pediatric combination vaccines.", "competitive_rivalry": "Moderate with Indian peers like Serum Institute and Bharat Biotech."}
    ),
    (
        "Panacea Biotec", "Biotech, Vaccines & Healthcare Diagnostics",
        "public immunization agencies and infant healthcare specialists",
        "seek fully liquid combination vaccines that eliminate reconstituting steps to prevent administration errors in rural clinics",
        "EasySix & Polprotect", "Fully Liquid Hexavalent Pediatric Vaccines",
        "delivers the world's first fully liquid hexavalent vaccine protecting against 6 deadly infant diseases with zero clinic preparation errors",
        [0.76, 0.75, 0.92, 0.88, 0.86, 0.62],
        {"political": "Strategic collaborator with Indian Ministry of Health and international polio eradication alliances.", "economic": "High value-add hexavalent formulations command premium pricing over basic single-antigen vaccines.", "social": "Simplifies immunization workflows for rural ASHA and ANM workers across primary health centres.", "technological": "Proprietary stabilization technology keeping six distinct antigens chemically stable in a single pre-filled syringe.", "legal": "CDSCO approval and patent coverage over liquid formulation matrix.", "environmental": "Compact pre-filled packaging drastically reduces cold chain footprint and clinic plastic packaging waste."},
        [0.20, 0.48, 0.35, 0.25, 0.58],
        {"threat_of_new_entrants": "Low; multi-antigen liquid formulation is notoriously difficult to formulate without degradation.", "bargaining_power_of_buyers": "Moderate; private pediatricians pay premium, public tenders demand discounts.", "bargaining_power_of_suppliers": "Moderate; proprietary antigens and syringe assemblies.", "threat_of_substitutes": "Moderate from multi-injection traditional vaccination protocols.", "competitive_rivalry": "High in domestic private immunization segment."}
    ),
    (
        "Dr Lal PathLabs", "Biotech, Vaccines & Healthcare Diagnostics",
        "urban and semi-urban patients and consulting physicians across North and East India",
        "require accurate, rapid, and certified clinical pathology test reports backed by uncompromising quality control",
        "National Reference Lab & Suburban Hub-and-Spoke Network", "Standardized Clinical Pathology Diagnostic Services",
        "guarantees NABL and CAP-accredited diagnostic accuracy with 24-hour turnaround across 10,000+ tests and a vast home collection network",
        [0.65, 0.82, 0.90, 0.88, 0.82, 0.55],
        {"political": "Benefits from government focus on Ayushman Bharat preventative health screenings and diagnostics expansion.", "economic": "Robust operating cash flows and zero-debt balance sheet driven by high-margin B2C patient walk-ins.", "social": "Growing preventive health awareness among urban middle-class driving annual wellness checkup packages (Swasthfit).", "technological": "State-of-the-art National Reference Laboratory in Rohini, Delhi equipped with AI-assisted digital pathology and robotic analyzers.", "legal": "NABL accreditation and compliance with Clinical Establishments Act and bio-medical waste rules.", "environmental": "Standardized neutralization and biohazard sterilization before municipal waste handover."},
        [0.45, 0.55, 0.38, 0.30, 0.75],
        {"threat_of_new_entrants": "Moderate to high at local unorganized level, but extremely hard to build trusted national brand equity.", "bargaining_power_of_buyers": "Moderate; patients compare package prices between Lal, Metropolis, and Thyrocare.", "bargaining_power_of_suppliers": "Moderate; diagnostic reagent giants (Roche, Abbott, Siemens) set equipment pricing.", "threat_of_substitutes": "Low; diagnostic testing is mandatory for evidence-based clinical therapy.", "competitive_rivalry": "High; intense competition from organized chains and hospital-attached diagnostic labs."}
    ),
    (
        "Metropolis Healthcare", "Biotech, Vaccines & Healthcare Diagnostics",
        "oncologists, geneticists, and complex chronic disease patients across West and South India",
        "need deep specialized pathology, molecular oncology, and esoteric diagnostic testing for accurate clinical staging",
        "Metropolis Comprehensive Molecular & Oncology Pathology Hub", "Specialized Esoteric Clinical Diagnostics",
        "offers an extensive menu of 4,000+ specialized tests, advanced immunohistochemistry, and next-gen sequencing for precision oncology",
        [0.64, 0.80, 0.89, 0.89, 0.80, 0.55],
        {"political": "Supports government initiatives on non-communicable disease (cancer, cardiac) early detection.", "economic": "High-margin esoteric test mix cushions against price wars in routine blood glucose and lipid profile testing.", "social": "Rise of personalized medicine and targeted oncology therapies requires companion diagnostic testing.", "technological": "Cutting-edge molecular diagnostics, liquid biopsies, and automated cytogenetics pipelines in Mumbai central lab.", "legal": "CAP (College of American Pathologists) accredited with stringent quality assurance benchmarks.", "environmental": "Rigid compliance with biohazard sterilization protocols for chemical reagents and infectious specimens."},
        [0.35, 0.50, 0.40, 0.25, 0.70],
        {"threat_of_new_entrants": "Low for specialized esoteric tests; high capital barrier for advanced mass spectrometers and sequencers.", "bargaining_power_of_buyers": "Low to moderate; doctors mandate specific trusted reference labs for biopsy and genetic analysis.", "bargaining_power_of_suppliers": "Moderate; specialized diagnostic kits and sequencing reagents.", "threat_of_substitutes": "Low; accurate biopsy and molecular testing cannot be substituted.", "competitive_rivalry": "Moderate with specialized diagnostic providers like Dr Lal, MedGenome, and hospital reference labs."}
    ),
    (
        "Thyrocare Technologies", "Biotech, Vaccines & Healthcare Diagnostics",
        "price-sensitive retail consumers, B2B local labs, and wellness platforms across India",
        "demand the most affordable, centralized routine biochemistry and thyroid screening without paying retail diagnostic premiums",
        "Centralized Automated Laboratory Network & Aarogyam Packages", "High-Volume Low-Cost Preventive Screening",
        "operates a world-class 24/7 centralized mega-lab in Navi Mumbai utilizing robotic automation to deliver India's lowest-cost preventive blood panels",
        [0.60, 0.84, 0.88, 0.92, 0.78, 0.58],
        {"political": "Democratizes diagnostic access aligned with government preventive health priorities.", "economic": "Disruptive low-cost business model powered by massive batch-processing economies of scale and B2B sample aggregation.", "social": "Aarogyam packages made comprehensive 60-parameter wellness checkups accessible to lower-middle-class households.", "technological": "Pioneered India's first Total Laboratory Automation (TLA) track system processing over 100,000 samples nightly.", "legal": "NABL and CAP certified testing protocols adhering to national diagnostic standards.", "environmental": "High-efficiency centralized testing drastically reduces localized reagent plastic waste compared to distributed standalone labs."},
        [0.40, 0.65, 0.35, 0.35, 0.78],
        {"threat_of_new_entrants": "Moderate; low barrier to open a collection booth, but impossible to match Thyrocare's centralized unit costs.", "bargaining_power_of_buyers": "High; retail consumers and digital health aggregators (PharmEasy) demand rock-bottom package pricing.", "bargaining_power_of_suppliers": "Low; Thyrocare is one of the largest bulk reagent buyers in Asia, demanding steep OEM discounts.", "threat_of_substitutes": "Low; standard blood biochemistry has no direct substitute.", "competitive_rivalry": "Fierce; price competition from local unorganized labs and e-pharmacy wellness bundles."}
    ),
    (
        "Vijaya Diagnostic Centre", "Biotech, Vaccines & Healthcare Diagnostics",
        "patients and families in Andhra Pradesh, Telangana, and Tier-2 South Indian cities",
        "need integrated pathology and advanced radiology (MRI, CT, PET-CT) under a single roof to avoid multiple clinic visits",
        "Integrated One-Stop Diagnostic Hubs", "Integrated Pathology & Radiology Diagnostic Services",
        "provides seamless integrated pathology and 3T MRI/128-slice CT imaging at a single location with trusted regional doctor relationships",
        [0.62, 0.78, 0.88, 0.86, 0.79, 0.54],
        {"political": "Compliant with state medical council norms and PCPNDT act regulations for prenatal imaging.", "economic": "Dual-revenue engine from high-capex radiology and high-margin pathology delivers superior average revenue per patient.", "social": "Deep regional trust and multi-generational patient loyalty in Hyderabad and surrounding tier-2/3 districts.", "technological": "Equipped with advanced 3T MRI, 128-slice CT scanners, digital mammography, and fully automated hematology lines.", "legal": "AERB (Atomic Energy Regulatory Board) clearances for radiation safety and NABL accreditation for pathology.", "environmental": "Radiation shielding containment protocols and eco-friendly digital PACS film-less reporting."},
        [0.30, 0.52, 0.42, 0.28, 0.65],
        {"threat_of_new_entrants": "Low; integrated centers require substantial upfront capex for heavy imaging equipment (MRI/CT).", "bargaining_power_of_buyers": "Moderate; patients follow physician referrals for major radiological investigations.", "bargaining_power_of_suppliers": "High; GE Healthcare, Siemens Healthineers, and Philips hold pricing power on high-end imaging machines.", "threat_of_substitutes": "Low; combined imaging and tissue diagnostics cannot be substituted.", "competitive_rivalry": "Moderate; strong regional dominance with limited overlap from North-centric chains."}
    ),
    (
        "Medall Healthcare", "Biotech, Vaccines & Healthcare Diagnostics",
        "underserved semi-urban and rural populations across South India and state public health systems",
        "need accessible, dependable diagnostic and imaging services through affordable district-level and PPP government hospital models",
        "Public-Private-Partnership (PPP) & Community Diagnostic Centers", "Accessible District-Level Medical Diagnostics",
        "operates India's largest healthcare diagnostic PPP network, bringing modern CT/MRI scans and blood diagnostics to government district hospitals",
        [0.72, 0.76, 0.90, 0.82, 0.80, 0.52],
        {"political": "Direct beneficiary of state government PPP healthcare tenders in Tamil Nadu, Andhra Pradesh, and Karnataka.", "economic": "Volume-driven government concession agreements provide predictable baseline footfalls.", "social": "Bridges the acute rural-urban diagnostic divide, serving economically disadvantaged patients at subsidized rates.", "technological": "Cloud-connected tele-radiology network enabling rural scans to be interpreted in real-time by specialist radiologists in Chennai.", "legal": "Adherence to state healthcare tender contracts, NABL norms, and AERB safety codes.", "environmental": "Standardized e-waste management of imaging hardware and bio-medical waste segregation."},
        [0.32, 0.60, 0.38, 0.25, 0.62],
        {"threat_of_new_entrants": "Moderate; securing state-level PPP concession contracts requires past operational track record and capital.", "bargaining_power_of_buyers": "High; state health departments dictate tariff schedules in public-private contracts.", "bargaining_power_of_suppliers": "Moderate; dependent on imaging equipment leasing and maintenance contracts.", "threat_of_substitutes": "Low in rural districts where alternatives do not exist.", "competitive_rivalry": "Moderate during tender bidding, followed by 5 to 10-year exclusive operational periods."}
    ),
    (
        "Neuberg Diagnostics", "Biotech, Vaccines & Healthcare Diagnostics",
        "tertiary clinicians, transplant surgeons, and specialty research institutions globally",
        "require cutting-edge genomics, proteomics, next-gen sequencing, and specialized molecular diagnostics for personalized therapy",
        "Neuberg Center for Genomic Medicine", "Advanced Molecular & Genomic Specialty Diagnostics",
        "delivers ultra-specialized genetic sequencing, cancer liquid biopsies, and newborn screening with presence across India, UAE, and South Africa",
        [0.65, 0.80, 0.89, 0.93, 0.82, 0.56],
        {"political": "Supports National Biotechnology Development Strategy and genomic medicine initiatives.", "economic": "International diagnostic operations in Dubai and South Africa provide foreign currency revenue diversification.", "social": "Helps couples detect hereditary genetic disorders through carrier screening and non-invasive prenatal testing (NIPT).", "technological": "State-of-the-art Illumina NGS platforms, real-time droplet digital PCR, and AI-driven variant calling algorithms.", "legal": "Complies with Indian ICMR guidelines on genomic research and international CAP/ISO standards.", "environmental": "Controlled handling of molecular biological chemicals and specialized clinical cold-chain logistics."},
        [0.28, 0.48, 0.45, 0.22, 0.64],
        {"threat_of_new_entrants": "Low; requires rare bioinformatician talent, heavy gene-sequencer capex, and physician credibility.", "bargaining_power_of_buyers": "Moderate; specialty genomic panels are price-inelastic when treating life-threatening diseases.", "bargaining_power_of_suppliers": "High; Illumina and Thermo Fisher dominate sequencing consumables and reagent chemistry.", "threat_of_substitutes": "Low; genomics is the frontier of personalized medicine.", "competitive_rivalry": "Moderate; competes with MedGenome, Strand Life Sciences, and global specialty labs."}
    ),
    (
        "Agappe Diagnostics", "Biotech, Vaccines & Healthcare Diagnostics",
        "small to medium diagnostic labs, nursing homes, and rural clinics across India and Asia",
        "need affordable, high-reliability in-vitro diagnostic (IVD) reagents and automated hematology analyzers without costly imported equipment",
        "Mispa Series & Indigenized IVD Reagents", "Affordable Indigenous In-Vitro Diagnostic Systems",
        "manufactures indigenously developed clinical chemistry and hematology reagents and analyzers, cutting diagnostic setup costs by over 40%",
        [0.78, 0.82, 0.86, 0.88, 0.80, 0.60],
        {"political": "Pioneered indigenization under Make in India medical devices mission, reducing reliance on European and Chinese IVD imports.", "economic": "Razor-and-blade model: analyzer placement creates decades of recurring high-margin domestic reagent sales.", "social": "Enables small town clinics in Tier 3/4 India to run local blood tests without sending samples 100km away.", "technological": "Proprietary cartridge-based nephelometry and 3-part/5-part hematology analyzer engineering in Kochi, Kerala.", "legal": "CDSCO manufacturing licenses and ISO 13485 medical device quality management certification.", "environmental": "Formulated eco-friendly cyanide-free reagents for safer lab technician handling and sewage disposal."},
        [0.25, 0.50, 0.35, 0.30, 0.60],
        {"threat_of_new_entrants": "Low to moderate; precision manufacturing of optical sensors and enzymatic reagents has high entry barriers.", "bargaining_power_of_buyers": "Moderate; small labs have budget constraints but need dependable machine uptime.", "bargaining_power_of_suppliers": "Moderate; raw enzymes, optical components, and precision fluidics.", "threat_of_substitutes": "Low; diagnostic equipment is indispensable.", "competitive_rivalry": "Intense from global giants (Mindray, Sysmex, Roche) offering aggressive machine financing."}
    ),
    (
        "MedGenome Labs", "Biotech, Vaccines & Healthcare Diagnostics",
        "oncologists, rare disease specialists, and pharmaceutical drug discovery researchers",
        "require deep South Asian genomic data, complex variant interpretation, and high-throughput next-generation sequencing",
        "MedGenome South Asian Genetic Database & Claria NIPT", "Clinical Genomics & Bioinformatics Discovery Platform",
        "houses the world's largest repository of South Asian genetic data, delivering unmatched accuracy in hereditary disease risk and cancer mutation profiling",
        [0.68, 0.82, 0.90, 0.96, 0.84, 0.58],
        {"political": "Aligns with GenomeIndia project and ICMR ethical frameworks for human genomic research.", "economic": "Attracts global pharmaceutical R&D partnerships seeking diverse genomic cohorts for target validation.", "social": "Diagnosing previously uncharacterized rare pediatric genetic syndromes in high-consanguinity communities.", "technological": "High-throughput NovaSeq 6000 sequencing engines paired with proprietary OncoPept and VariantPath algorithms in Bengaluru.", "legal": "Strict compliance with Indian DPDP Act genomic data localization and HIPAA clinical standards.", "environmental": "High-density compute infrastructure optimized for power efficiency and renewable energy procurement."},
        [0.20, 0.42, 0.48, 0.20, 0.58],
        {"threat_of_new_entrants": "Very low; proprietary genomic database of over 300,000 South Asian genomes forms an insurmountable moat.", "bargaining_power_of_buyers": "Low; clinicians rely exclusively on MedGenome's validated genetic variant classifications.", "bargaining_power_of_suppliers": "High; Illumina supplies dominant sequencing platforms and flow cells.", "threat_of_substitutes": "Low; standard biochemical testing cannot decipher genetic mutations.", "competitive_rivalry": "Low to moderate; clear undisputed leader in clinical genomics across South Asia."}
    ),
    (
        "Strand Life Sciences", "Biotech, Vaccines & Healthcare Diagnostics",
        "clinical oncologists, hospital networks, and bioinformatics developers",
        "seek automated, AI-assisted genomic variant annotation and curated clinical interpretation to translate raw NGS data into actionable cancer therapy",
        "Strand NGS & Precision Oncology Gene Panels", "AI-Powered Genomic Analysis & Clinical Annotation Platform",
        "combines two decades of world-class computational biology with CAP-certified clinical diagnostic testing for actionable precision therapy guidance",
        [0.66, 0.80, 0.88, 0.95, 0.82, 0.55],
        {"political": "Beneficiary of Indian Ministry of Science & Technology BIRAC research grants and deep-tech innovation initiatives.", "economic": "Dual monetization through clinical testing services in India and software licensing to global pharma research labs.", "social": "Directs cancer patients to targeted therapies, sparing them unnecessary toxic chemotherapy regimes.", "technological": "Pioneered proprietary bioinformatics pipelines and NLP algorithms that parse biomedical literature to annotate clinical significance.", "legal": "Adheres to international clinical genetic reporting guidelines (ACMG/AMP).", "environmental": "Pure-play green software and cloud computing infrastructure with low physical resource intensity."},
        [0.22, 0.45, 0.42, 0.25, 0.55],
        {"threat_of_new_entrants": "Low; requires 20+ years of curated bioinformatics algorithms and clinical validation data.", "bargaining_power_of_buyers": "Moderate; oncologists select gene panels based on depth of clinical evidence.", "bargaining_power_of_suppliers": "Low; algorithmic IP and computational software are owned internally.", "threat_of_substitutes": "Moderate from open-source academic tools, but lacking clinical liability and regulatory certification.", "competitive_rivalry": "Moderate with global bioinformatics platforms (Sophia Genetics, Foundation Medicine)."}
    ),
    (
        "Molbio Diagnostics", "Biotech, Vaccines & Healthcare Diagnostics",
        "public health agencies, rural primary healthcare centres, and global anti-tuberculosis programs",
        "need rugged, battery-operated, point-of-care molecular RT-PCR testing that works without air conditioning or specialized lab infrastructure",
        "Truenat Real-Time PCR Platform", "Portable Point-of-Care Molecular Diagnostic Device",
        "enables sample-to-result molecular diagnosis of Tuberculosis, COVID-19, and infectious diseases in under 1 hour in remote rural villages",
        [0.84, 0.85, 0.94, 0.92, 0.85, 0.65],
        {"political": "Endorsed by WHO and Ministry of Health as the primary weapon in Prime Minister's Mission TB Mukt Bharat 2025.", "economic": "Achieved unicorn valuation driven by global health procurements and decentralized rural public health tenders across 40+ countries.", "social": "Revolutionized grassroots tuberculosis detection, diagnosing infectious patients before transmission spreads in crowded rural households.", "technological": "Patented microfluidic cartridge technology, room-temperature stable freeze-dried reagents, and solar/battery-powered hardware built in Goa.", "legal": "WHO policy recommendation and CDSCO/CE approvals for point-of-care rapid molecular testing.", "environmental": "Low-power energy-efficient hardware and self-contained cartridge waste reduces toxic liquid disposal."},
        [0.16, 0.45, 0.35, 0.22, 0.50],
        {"threat_of_new_entrants": "Low; patented micro-PCR chip technology and WHO endorsement take over a decade to achieve.", "bargaining_power_of_buyers": "Moderate; global tender procurements negotiated at volume, but few competitors offer true battery-operated portability.", "bargaining_power_of_suppliers": "Moderate; precision plastic microfluidics and thermal sensors.", "threat_of_substitutes": "Low; traditional sputum microscopy has high false-negative rates compared to molecular PCR.", "competitive_rivalry": "Low to moderate; main international competitor is Cepheid GeneXpert (which requires continuous AC and mains electricity)."}
    ),
    (
        "Mylab Discovery Solutions", "Biotech, Vaccines & Healthcare Diagnostics",
        "diagnostic laboratories, hospitals, and direct consumers seeking rapid infectious disease detection",
        "need affordable, indigenously engineered molecular testing kits and automated high-throughput nucleic acid extraction systems",
        "PathoDetect & CoviSelf At-Home Rapid Antigen Kit", "Indigenous Molecular & Rapid Diagnostic Platforms",
        "developed India's first indigenous commercial RT-PCR kit and first approved at-home self-test, slashing test costs from Rs 4,500 to Rs 250",
        [0.75, 0.80, 0.90, 0.90, 0.82, 0.60],
        {"political": "Celebrated pioneer of Atmanirbhar Bharat during the pandemic crisis, partnering with Serum Institute for scale-up.", "economic": "Strong cash accumulation during pandemic deployed into automated robotic sample processing systems (Compact XL).", "social": "Empowered millions of Indian households to conduct safe at-home infectious screening during public lockdowns.", "technological": "In-house molecular biology enzymes, primer-probe synthesis, and automated magnetic bead RNA extraction machinery in Pune.", "legal": "ICMR validation and CDSCO licenses for commercial diagnostic kit manufacturing.", "environmental": "Biodegradable swab components and enclosed cartridge disposal safe bags."},
        [0.28, 0.55, 0.38, 0.32, 0.68],
        {"threat_of_new_entrants": "Moderate; rapid antigen kits face commodity price competition from Chinese and domestic manufacturers.", "bargaining_power_of_buyers": "High in OTC retail; consumers compare rapid kit prices across pharmacies.", "bargaining_power_of_suppliers": "Moderate; nitrocellulose membranes, antibody conjugates, and plastic cassettes.", "threat_of_substitutes": "Moderate from centralized laboratory tests.", "competitive_rivalry": "High; post-pandemic normalization created surplus diagnostic manufacturing capacity."}
    ),
    (
        "Tata Medical and Diagnostics (Tata MD)", "Biotech, Vaccines & Healthcare Diagnostics",
        "healthcare systems, corporate workforces, and government public health screening initiatives",
        "seek rapid, scalable, and innovative diagnostic technologies based on novel CRISPR and automated digital imaging systems",
        "Tata MD CHECK (CRISPR-Cas9 Diagnostic) & Tata MD TransCheck", "CRISPR-Based & Digital Point-of-Care Diagnostics",
        "commercialized world's first CRISPR-Cas9 FELUDA diagnostic test delivering PCR-grade accuracy on a simple paper strip within 45 minutes",
        [0.76, 0.82, 0.90, 0.94, 0.85, 0.62],
        {"political": "Backed by Tata Group's multi-century institutional trust and close collaboration with CSIR-IGIB government labs.", "economic": "Strong balance sheet backing allows long-horizon investments into futuristic CRISPR and AI-microscopy technologies.", "social": "Brings cutting-edge molecular diagnostics to corporate wellness programs and rural public screenings.", "technological": "Pioneered commercial deployment of FnCas9 enzyme chemistry and automated digital tele-microscopy hardware in Chennai.", "legal": "Regulatory approvals from DCGI and ICMR for commercial CRISPR-based infectious disease testing.", "environmental": "Minimal chemical footprint utilizing ambient-temperature paper lateral flow test strips."},
        [0.22, 0.48, 0.35, 0.28, 0.60],
        {"threat_of_new_entrants": "Low; CRISPR IP licensing and biochemical enzymology require immense institutional and scientific credibility.", "bargaining_power_of_buyers": "Moderate; corporate and institutional buyers expect competitive pricing alongside Tata brand reliability.", "bargaining_power_of_suppliers": "Low to moderate; internal IP partnerships with CSIR.", "threat_of_substitutes": "Moderate from established RT-PCR platforms.", "competitive_rivalry": "Moderate; competing with specialized diagnostic kit developers."}
    ),
    (
        "Premas Biotech", "Biotech, Vaccines & Healthcare Diagnostics",
        "global biopharmaceutical innovators and vaccine development companies",
        "require high-yield, complex eukaryotic protein expression systems for challenging virus-like particles and difficult-to-express antigens",
        "D-Crypt Expression Platform", "Recombinant Protein Expression & Fermentation Platform",
        "delivers unmatched protein expression yields for complex multi-protein VLPs and membrane proteins using proprietary modified yeast hosts",
        [0.68, 0.78, 0.84, 0.95, 0.80, 0.65],
        {"political": "Supports India's biopharma manufacturing export capabilities and national biotechnology mission.", "economic": "High-margin technology out-licensing and milestone royalty revenues from international biopharma clients.", "social": "Accelerated oral COVID-19 and infectious vaccine candidate development through novel VLP production.", "technological": "Patented D-Crypt yeast platform overcoming traditional mammalian and bacterial expression bottlenecks.", "legal": "Global patent filings across US, Europe, and India covering proprietary expression vectors and fermentation methods.", "environmental": "Sustainable bio-fermentation processes minimizing hazardous chemical solvent usage."},
        [0.18, 0.40, 0.35, 0.22, 0.52],
        {"threat_of_new_entrants": "Low; proprietary biological expression systems require decades of genetic engineering and strain optimization.", "bargaining_power_of_buyers": "Moderate; clients have alternate expression systems (CHO cells, E. coli) but choose Premas for difficult proteins.", "bargaining_power_of_suppliers": "Low; standard microbiological nutrients and fermenter consumables.", "threat_of_substitutes": "Moderate from mammalian cell line platforms.", "competitive_rivalry": "Low to moderate; highly specialized niche bioprocessing domain."}
    ),
    (
        "Gennova Biopharmaceuticals", "Biotech, Vaccines & Healthcare Diagnostics",
        "national health agencies and developing countries lacking ultra-cold-chain refrigeration infrastructure",
        "need next-generation mRNA vaccines and therapeutics that remain stable at standard refrigerator temperatures (2-8 deg C)",
        "GEMCOVAC-19 & GEMCOVAC-OM", "Lyophilized Thermostable mRNA Vaccine Platform",
        "engineered the world's first freeze-dried, thermostable mRNA vaccine that dispenses with minus 70 deg C ultra-cold freezers, enabling tropical distribution",
        [0.82, 0.82, 0.94, 0.96, 0.88, 0.68],
        {"political": "Flagship recipient of Department of Biotechnology and BIRAC Mission COVID Suraksha seed funding.", "economic": "Unlocks massive commercialization potential for mRNA therapies in Africa, Southeast Asia, and rural India.", "social": "Democratizes mRNA technology for low-resource environments without specialized sub-zero infrastructure.", "technological": "Proprietary self-amplifying mRNA and lipid nanoparticle (LNP) lyophilization technology engineered in Pune.", "legal": "Emergency use authorization from DCGI and ongoing global patent protection on thermostable mRNA formulation.", "environmental": "Eliminating deep-freezer cold-chain logistics drastically reduces carbon emissions and diesel generator reliance in rural health centres."},
        [0.15, 0.40, 0.38, 0.20, 0.50],
        {"threat_of_new_entrants": "Extremely low; mRNA synthesis, LNP encapsulation, and lyophilization know-how is globally concentrated in less than 10 companies.", "bargaining_power_of_buyers": "Low to moderate; developing nations desperately need thermostable formulations.", "bargaining_power_of_suppliers": "High; specialized ionizable lipids and capped RNA raw materials.", "threat_of_substitutes": "Moderate from traditional protein subunit and viral vector vaccines.", "competitive_rivalry": "Moderate with global mRNA pioneers (Moderna, BioNTech) who lack thermostable shelf-stability."}
    ),
    (
        "Wockhardt Biotech", "Biotech, Vaccines & Healthcare Diagnostics",
        "infectious disease physicians, hospitals, and critical care units battling multi-drug resistant superbugs",
        "require novel, pathogen-targeted antibiotics and recombinant biologicals capable of overcoming deadly antimicrobial resistance (AMR)",
        "WCK 5222 (Zidebactam/Cefepime) & Recombinant Insulin", "Novel Anti-Infective NCEs & Biosimilar Peptides",
        "develops breakthrough QIDP-designated antibiotics engineered specifically to defeat carbapenem-resistant Gram-negative superbug hospital infections",
        [0.72, 0.78, 0.90, 0.94, 0.88, 0.62],
        {"political": "Aligns with National Action Plan on Antimicrobial Resistance (NAP-AMR) and US FDA Qualified Infectious Disease Product (QIDP) fast-track status.", "economic": "Massive potential peak sales in US and European hospital markets where multi-drug resistant infections cause tens of thousands of deaths.", "social": "Saving lives of ICU patients suffering from untreatable hospital-acquired pneumonia and bloodstream infections.", "technological": "Deep medicinal chemistry R&D synthesizing dual-action beta-lactamase inhibitors and recombinant DNA biological human insulin.", "legal": "Extensive international Phase 3 clinical trials and US FDA fast-track review pathways.", "environmental": "High-efficiency zero-discharge biological waste treatment facilities at Aurangabad manufacturing plants."},
        [0.16, 0.38, 0.35, 0.18, 0.52],
        {"threat_of_new_entrants": "Extremely low; discovering and running Phase 3 trials on new antibiotic chemical entities takes over $500M and 12 years.", "bargaining_power_of_buyers": "Low; critical ICU patients facing lethal pan-resistant infections have zero alternative therapies.", "bargaining_power_of_suppliers": "Moderate; specialized chemical precursors and peptide synthesis reagents.", "threat_of_substitutes": "Low; when existing antibiotics fail, novel NCE molecules are the only cure.", "competitive_rivalry": "Low; very few pharmaceutical companies globally are actively investing in novel Gram-negative antibiotics."}
    ),
    (
        "Shilpa Biologicals", "Biotech, Vaccines & Healthcare Diagnostics",
        "global biopharma companies and oncology centers",
        "need high-yield, cost-effective contract development and manufacturing (CDMO) for biosimilar monoclonal antibodies and recombinant proteins",
        "Biosimilar Monoclonal Antibody CDMO & Recombinant Albumin", "Biologics CDMO & Biosimilar Therapeutics",
        "provides end-to-end mammalian cell-line development, sterile injectable fill-finish, and commercial biosimilar manufacturing in Dharwad, Karnataka",
        [0.70, 0.80, 0.86, 0.91, 0.84, 0.64],
        {"political": "Benefits from Government of India's PLI scheme for biopharmaceuticals and active biologics manufacturing.", "economic": "Captures lucrative long-term supply contracts from global innovators shifting biomanufacturing from China to India.", "social": "Expanding affordable biosimilar oncology drugs to reduce cancer treatment bankruptcy for families.", "technological": "Modern single-use bioreactor systems, automated vial and prefilled syringe lines, and deep protein characterization labs.", "legal": "Adheres to cGMP requirements of US FDA, EMA, and Indian CDSCO.", "environmental": "Operates fully biological wastewater digestion and scrubbers to neutralize bioprocess byproducts."},
        [0.22, 0.45, 0.38, 0.24, 0.58],
        {"threat_of_new_entrants": "Low; biologics manufacturing requires cleanroom certifications, cell banking, and massive technical validations.", "bargaining_power_of_buyers": "Moderate; global pharma sponsors demand stringent quality metrics and competitive batch pricing.", "bargaining_power_of_suppliers": "Moderate; single-use consumables and specialized cell culture media (Cytiva, Sartorius).", "threat_of_substitutes": "Low; monoclonal antibodies are standard-of-care in oncology and autoimmune disorders.", "competitive_rivalry": "Moderate with Indian biologics CDMOs (Biocon Biologics, Syngene, Enzene)."}
    )
]

for item in sector7_data:
    add_c(*item)

print(f"Sector 7 added: {len(sector7_data)} companies. Total: {len(part2_a)}")

# ==============================================================================
# SECTOR 8: Hospital Networks & Healthcare Delivery (20 companies)
# ==============================================================================
sector8_data = [
    (
        "Apollo Hospitals Enterprise", "Hospital Networks & Healthcare Delivery",
        "middle-class and affluent Indian families, international medical tourists, and digital-first healthcare seekers",
        "require seamless, world-class tertiary and quaternary hospital care integrated with 24/7 digital pharmacy and doctor consultations",
        "Apollo Hospitals & Apollo 24/7 Omnichannel Ecosystem", "Integrated Tertiary Healthcare & Omnichannel Digital Health",
        "delivers India's largest JCI-accredited tertiary hospital network combined with an omnichannel digital app offering 2-hour medicine delivery and telemedicine",
        [0.72, 0.88, 0.95, 0.94, 0.85, 0.65],
        {"political": "Key partner for National Health Authority under Ayushman Bharat Digital Mission and medical tourism promotion (Heal in India).", "economic": "Unmatched scale generates over Rs 16,000 Cr in revenues across hospital beds, 5,500+ pharmacies, and digital health.", "social": "Pioneered private corporate healthcare in India, establishing consumer trust over 4 decades of clinical excellence.", "technological": "Apollo 24/7 digital platform, robotic surgery suites (Da Vinci), and South Asia's first Proton Beam Therapy cancer center in Chennai.", "legal": "Compliant with Clinical Establishments Act, NABH, JCI international accreditations, and medical negligence jurisprudence.", "environmental": "Extensive biomedical waste segregation, green hospital IGBC Platinum certifications, and rooftop solar arrays."},
        [0.25, 0.45, 0.42, 0.28, 0.65],
        {"threat_of_new_entrants": "Low; enormous capital expenditure (Rs 1-1.5 Cr per bed), land constraints, and decades required to recruit top clinicians.", "bargaining_power_of_buyers": "Moderate; high-end quaternary treatments are price-inelastic, but routine surgeries face insurance TPA package scrutiny.", "bargaining_power_of_suppliers": "Moderate; medical equipment OEMs (GE, Siemens) negotiate with Apollo's massive centralized procurement division.", "threat_of_substitutes": "Low; specialized cardiac, oncology, and transplant surgeries have no substitute.", "competitive_rivalry": "Moderate to high; competes with Max Healthcare, Fortis, and Manipal in top metro clusters."}
    ),
    (
        "Fortis Healthcare", "Hospital Networks & Healthcare Delivery",
        "metro residents seeking comprehensive multi-specialty tertiary and quaternary clinical care",
        "need trusted multi-super-specialty clinical treatment with proven survival outcomes in cardiac sciences, orthopedics, and neurosciences",
        "Fortis Memorial Research Institute (FMRI) & Network Hospitals", "Multi-Specialty Quaternary Hospital Chain",
        "offers globally recognized clinical excellence across 27 hospitals with advanced organ transplant, cardiology, and oncology programs",
        [0.70, 0.85, 0.92, 0.92, 0.84, 0.64],
        {"political": "Operates within strict state health regulatory frameworks and engages in public health insurance panel empanelements.", "economic": "Turnaround backed by Malaysia's IHH Healthcare, delivering strong occupancy, higher ARPOB (average revenue per occupied bed), and margin expansion.", "social": "Major provider of acute emergency care and complex cardiac surgeries across Delhi-NCR, Mumbai, and Bengaluru.", "technological": "Equipped with TrueBeam Linac cancer radiation, BrainSuite neurosurgical navigation, and robotic orthopedic joint replacement.", "legal": "NABH and JCI accreditations, compliant with organ transplantation legal protocols (THOTA act).", "environmental": "Comprehensive bio-medical waste treatment, water recycling STP plants, and energy-efficient building management."},
        [0.28, 0.48, 0.45, 0.26, 0.70],
        {"threat_of_new_entrants": "Low; prohibitive land acquisition costs and clinician brand loyalty in core metro locations.", "bargaining_power_of_buyers": "Moderate; private health insurance penetration empowers TPAs to negotiate structured procedure package rates.", "bargaining_power_of_suppliers": "Moderate; specialized surgical consumables and pharmaceutical drug suppliers.", "threat_of_substitutes": "Low for acute quaternary tertiary care.", "competitive_rivalry": "Intense with Max Healthcare, Apollo, and Medanta in the lucrative North Indian healthcare corridor."}
    ),
    (
        "Max Healthcare Institute", "Hospital Networks & Healthcare Delivery",
        "discerning urban patients, high-net-worth individuals, and international medical tourists in North and West India",
        "demand the highest tier of quaternary clinical quality, five-star patient hospitality, and leading surgical luminaries",
        "Max Super Speciality Hospitals & Max BLK-Nanavati Network", "Premium Quaternary Healthcare & Surgical Oncology Hub",
        "leads the Indian private hospital industry in Average Revenue Per Occupied Bed (ARPOB) with premium clinical facilities and top surgical outcomes",
        [0.70, 0.89, 0.94, 0.93, 0.85, 0.65],
        {"political": "Supports government initiatives on medical value travel (MVT) attracting patients from Central Asia, Middle East, and Africa.", "economic": "Highest financial metrics in the sector with industry-leading EBITDA margins (>27%) and disciplined brownfield bed capacity expansions.", "social": "Aspirational private hospital choice for Delhi-NCR and Mumbai residents seeking premium clinical comfort and doctor prestige.", "technological": "Advanced Da Vinci Xi robotic surgical systems, intraoperative MRI, stereotactic radiosurgery, and digital patient record portals.", "legal": "JCI and NABH accredited, compliant with Medical Termination of Pregnancy, Organ Transplant Act, and clinical safety laws.", "environmental": "Green building certified tertiary units with automated HVAC energy conservation and medical effluent neutralizing plants."},
        [0.22, 0.42, 0.42, 0.22, 0.68],
        {"threat_of_new_entrants": "Very low in prime metro locations (South Delhi, Gurugram, Mumbai) due to zero available land parcels.", "bargaining_power_of_buyers": "Low to moderate; affluent patients prioritize physician reputation and clinical success over procedure discounting.", "bargaining_power_of_suppliers": "Moderate; centralized purchasing team negotiates volume rebates on implants and stents.", "threat_of_substitutes": "Low; quaternary medical procedures cannot be substituted.", "competitive_rivalry": "High between Max, Fortis, Apollo, and Medanta in North India."}
    ),
    (
        "Narayana Health", "Hospital Networks & Healthcare Delivery",
        "value-conscious middle-class families, rural patients, and low-income heart patients across India and developing nations",
        "need life-saving cardiac, pediatric, and multi-specialty surgery delivered at ultra-low cost without compromising clinical safety",
        "Narayana Health City & Affordable Cardiac Assembly-Line Model", "High-Efficiency Low-Cost Tertiary Healthcare Network",
        "pioneered the 'Henry Ford' high-volume surgical assembly-line model, delivering open-heart surgery at less than $1,500 with world-class survival rates",
        [0.78, 0.92, 0.98, 0.95, 0.86, 0.68],
        {"political": "Founded by Padma Bhushan Dr. Devi Shetty; major driver and advisor for Ayushman Bharat PM-JAY and national universal healthcare policy.", "economic": "Maintains ultra-lean operating model with high bed turnover and shared asset utilization, producing strong ROCE even at subsidized pricing.", "social": "Performs more pediatric heart surgeries than any institution globally, saving thousands of impoverished children annually.", "technological": "Proprietary MEDHA electronic health record system, AI-driven digital ICU monitoring, and remote telemedicine clinics.", "legal": "Full NABH and JCI accreditation with transparent pricing schedules complying with National Pharmaceutical Pricing Authority (NPPA) stent caps.", "environmental": "Energy-efficient hospital campus designs utilizing natural ventilation and solar water heating."},
        [0.20, 0.50, 0.35, 0.22, 0.58],
        {"threat_of_new_entrants": "Low; almost impossible for new commercial hospital operators to match Narayana's hyper-lean cost structure and mission-driven surgeon culture.", "bargaining_power_of_buyers": "Moderate; patients are price-sensitive, but Narayana already offers the lowest prices in the private market.", "bargaining_power_of_suppliers": "Low; Dr. Shetty famously negotiates directly with global OEMs to re-engineer machines and cut consumables prices.", "threat_of_substitutes": "Low; complex open-heart and vascular surgery cannot be substituted.", "competitive_rivalry": "Moderate; operates in a differentiated market segment focusing on mass-market affordability rather than luxury hospitality."}
    ),
    (
        "Medanta - The Medicity (Global Health)", "Hospital Networks & Healthcare Delivery",
        "patients with complex, multi-organ clinical conditions requiring collaborative super-specialty doctor team care",
        "require physician-led quaternary care where multidisciplinary teams of cardiologists, oncologists, and transplant surgeons collaborate seamlessly",
        "Medanta The Medicity & Integrated Institutes of Health", "Doctor-Led Multi-Super-Specialty Quaternary Hospital",
        "founded by legendary cardiac surgeon Dr. Naresh Trehan, featuring 1,400+ beds in Gurugram and expanding into underserved regions (Lucknow, Patna, Ranchi)",
        [0.72, 0.88, 0.95, 0.94, 0.85, 0.65],
        {"political": "Expanding quaternary clinical excellence to underserved Hindi heartland states (Uttar Pradesh, Bihar, Jharkhand) with state government backing.", "economic": "Rapid ramp-up of new hospital assets in Lucknow and Patna producing high operational leverage and strong cash generation.", "social": "Brings Delhi-NCR grade medical treatments directly to tier-2 North Indian cities, sparing families exhausting travel.", "technological": "Pioneered robotic beating-heart coronary bypass surgeries, TomoTherapy HD, and CyberKnife stereotactic radiosurgery.", "legal": "JCI, NABH, and NABL accredited, strictly adhering to medical ethics and organ transplant protocols.", "environmental": "Expansive 43-acre green campus in Gurugram with automated biomedical waste treatment and rain-water harvesting."},
        [0.20, 0.44, 0.40, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; building massive 1,000-bed doctor-led flagship institutions requires over Rs 1,000 Cr capex and clinical prestige.", "bargaining_power_of_buyers": "Low to moderate; patients travel across India specifically for Medanta's marquee doctors.", "bargaining_power_of_suppliers": "Moderate; strong volume discounts negotiated directly with pharmaceutical and implant vendors.", "threat_of_substitutes": "Low for life-saving quaternary interventions.", "competitive_rivalry": "Moderate; commanding leadership in Gurugram, Lucknow, and Patna."}
    ),
    (
        "Aster DM Healthcare", "Hospital Networks & Healthcare Delivery",
        "middle-class families and NRI returnees in Kerala, Karnataka, and Maharashtra",
        "need compassionate, transparently priced tertiary hospital care delivered with international clinical quality standards",
        "Aster Medcity & Regional Multi-Specialty Hospital Network", "Integrated Tertiary & Secondary Healthcare Network",
        "operates premier quaternary institutions like Aster Medcity in Kochi alongside a dense network of Tier 2/3 hospitals and clinics across South India",
        [0.68, 0.84, 0.92, 0.90, 0.84, 0.65],
        {"political": "Completed strategic demerger separating high-growth India business from GCC assets, unlocking dedicated domestic expansion capex.", "economic": "Robust growth in South India fueled by high private health insurance penetration and medical tourism from the Indian diaspora.", "social": "Deep community engagement through Aster DM Foundation providing subsidized treatments and mobile health clinics.", "technological": "Aster Medcity features minimal invasive robotic surgery, ECMO critical care units, and integrated tele-ICU networks.", "legal": "JCI and NABH accredited, compliant with Bio-Medical Waste Management rules and clinical protocols.", "environmental": "Solar-powered hospital facilities, water treatment plants, and paperless digital electronic medical records."},
        [0.26, 0.48, 0.42, 0.28, 0.66],
        {"threat_of_new_entrants": "Low to moderate; strong regional footprint in Kerala and South India creates deep brand entrenchment.", "bargaining_power_of_buyers": "Moderate; patients have choice among established private institutions in South India.", "bargaining_power_of_suppliers": "Moderate; multi-vendor sourcing for medical hardware and medicines.", "threat_of_substitutes": "Low; surgical and emergency clinical care has no alternative.", "competitive_rivalry": "Moderate to high with Apollo, Manipal, and regional healthcare players."}
    ),
    (
        "Rainbow Children's Medicare", "Hospital Networks & Healthcare Delivery",
        "expectant mothers, newborns, and critically ill children requiring specialized pediatric intensive care",
        "need specialized, child-centric pediatric and perinatal healthcare with full-time pediatric sub-specialists and advanced neonatal ICUs",
        "Rainbow Children's Hospital & BirthRight by Rainbow", "Super-Specialty Pediatric & Perinatal Hospital Chain",
        "operates India's premier dedicated pediatric hospital chain with comprehensive Level-3 NICU/PICU units and full-time round-the-clock pediatric surgeons",
        [0.72, 0.86, 0.96, 0.92, 0.86, 0.64],
        {"political": "Supports National Health Mission infant mortality reduction goals and pediatric health standards.", "economic": "Resilient business model with low dependence on government scheme tariffs; high private pay and insurance revenue share.", "social": "High emotional trust among young urban parents; specialized pediatric environment minimizes trauma for hospitalized children.", "technological": "Advanced high-frequency oscillatory ventilators, nitric oxide therapy, pediatric ECMO, and dedicated pediatric air ambulance transport.", "legal": "NABH accredited, adhering to rigorous child safety, pediatric medication dosing, and perinatal care standards.", "environmental": "Dedicated pediatric biomedical waste management and eco-friendly nursery and ward environments."},
        [0.22, 0.40, 0.38, 0.20, 0.54],
        {"threat_of_new_entrants": "Low; general multi-specialty hospitals struggle to replicate Rainbow's child-specific infrastructure and specialized pediatric surgeon pool.", "bargaining_power_of_buyers": "Low; parents prioritize the survival and safety of premature neonates and ill children above all costs.", "bargaining_power_of_suppliers": "Moderate; specialized pediatric ventilators, incubators (GE, Draeger), and neonatal consumables.", "threat_of_substitutes": "Low; general adult hospitals lack specialized Level-3 pediatric intensive care capabilities.", "competitive_rivalry": "Low to moderate; very few organized pan-India pure-play pediatric hospital chains exist."}
    ),
    (
        "Krishna Institute of Medical Sciences (KIMS Hospitals)", "Hospital Networks & Healthcare Delivery",
        "patients and families in Andhra Pradesh, Telangana, Maharashtra, and Karnataka",
        "require advanced multi-specialty tertiary care at affordable, transparent price points in tier-1 and tier-2 southern cities",
        "KIMS Multi-Specialty Hospital Network", "Affordable Tier-1 & Tier-2 Tertiary Healthcare Network",
        "delivers high clinical quality in organ transplants, cardiology, and oncology at a 20-30% lower cost structure than metro hospital chains",
        [0.70, 0.86, 0.94, 0.89, 0.84, 0.62],
        {"political": "Empaneled with Aarogyasri (AP/Telangana) and state government health insurance schemes, expanding public healthcare access.", "economic": "Industry-leading capital efficiency with low capex per bed (Rs 60-80 Lakhs) generating high return on capital employed (ROCE >20%).", "social": "Brings high-end medical procedures (heart/lung transplants, robotic surgeries) to tier-2 cities like Rajahmundry, Kurnool, and Nagpur.", "technological": "Leader in heart and lung transplants in South India; advanced cath labs, neuro-navigation, and robotic surgery suites.", "legal": "NABH and NABL accreditations across all hospitals, adhering to Clinical Establishments Act and medical protocols.", "environmental": "Modern wastewater treatment plants, solid medical waste autoclaving, and solar energy installations."},
        [0.25, 0.48, 0.40, 0.25, 0.62],
        {"threat_of_new_entrants": "Low; establishing multi-specialty clinical credibility and securing clinical doctor talent in tier-2 cities requires deep local relationships.", "bargaining_power_of_buyers": "Moderate; strong value-for-money reputation protects against patient churn.", "bargaining_power_of_suppliers": "Moderate; centralized purchasing division manages medical equipment procurement.", "threat_of_substitutes": "Low; essential tertiary surgeries have no substitutes.", "competitive_rivalry": "Moderate; dominates AP/Telangana with strategic regional moat."}
    ),
    (
        "Shalby Hospitals", "Hospital Networks & Healthcare Delivery",
        "elderly patients and orthopedic candidates suffering from degenerative joint disease and mobility loss",
        "need rapid, minimally invasive joint replacement surgery with quick post-operative recovery and long implant longevity",
        "Zero Technique Joint Replacement & Shalby Orthopedics Centers", "High-Volume Orthopedic & Joint Replacement Hospital Chain",
        "performs over 14,000 joint replacements annually using founder Dr. Vikram Shah's patented 'Zero Technique' that cuts surgical time to under 15 minutes",
        [0.66, 0.84, 0.92, 0.88, 0.82, 0.60],
        {"political": "Compliant with National Pharmaceutical Pricing Authority (NPPA) ceiling prices on orthopedic knee implants.", "economic": "High surgical throughput and proprietary orthopedic implant manufacturing (acquired Consensus Orthopedics US) enables backward integration.", "social": "Restores pain-free walking mobility and independence to thousands of elderly Indian citizens annually.", "technological": "Proprietary 'Zero Technique' surgical protocol reduces soft-tissue damage, blood loss, and patient infection rates.", "legal": "NABH and ISO accredited, strict compliance with medical implant traceability and surgical safety checklists.", "environmental": "Safe biological disposal of bone tissue and titanium/ceramic implant packaging sterilization."},
        [0.24, 0.46, 0.32, 0.26, 0.60],
        {"threat_of_new_entrants": "Low; orthopedic joint surgery requires immense surgical reputation, surgeon training, and specialized laminar airflow OTs.", "bargaining_power_of_buyers": "Moderate; implant price caps by government have standardized procedure pricing across hospitals.", "bargaining_power_of_suppliers": "Low to moderate; Shalby's owned implant manufacturing subsidiary reduces reliance on foreign implant vendors (Zimmer, Stryker).", "threat_of_substitutes": "Low; severe osteoarthritis has no non-surgical curative alternative.", "competitive_rivalry": "Moderate; competes with general multi-specialty hospital orthopedic departments."}
    ),
    (
        "HealthCare Global Enterprises (HCG)", "Hospital Networks & Healthcare Delivery",
        "cancer patients and oncologists across India seeking specialized precision oncology care",
        "need comprehensive cancer care (surgical, medical, radiation oncology, genomics) under specialized disease-management protocols",
        "HCG Cancer Centre Network & Comprehensive Oncology Care", "Pure-Play Specialized Cancer Care Hospital Network",
        "operates India's largest dedicated cancer care network with 24 comprehensive oncology centers utilizing advanced genomics and linear accelerators",
        [0.72, 0.85, 0.94, 0.95, 0.85, 0.64],
        {"political": "Supports National Cancer Grid and government cancer screening and treatment initiatives.", "economic": "Specialized oncology model commands higher revenue per bed with continuous multi-modality patient treatment cycles.", "social": "Fosters dedicated cancer support groups, psychosocial counseling, and palliative care for patients and caregivers.", "technological": "Pioneered CyberKnife, TrueBeam, and Genomics-driven targeted chemotherapy protocols in India.", "legal": "AERB licensed for radiation oncology, NABH and CAP accredited for oncopathology.", "environmental": "Strict nuclear medicine radiation containment protocols, lead-shielded bunkers, and radioactive isotope waste decay storage."},
        [0.20, 0.42, 0.45, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; building comprehensive cancer hospitals requires heavy radiation bunker capex, AERB clearances, and top oncologists.", "bargaining_power_of_buyers": "Low; cancer treatment is life-critical and patients prioritize clinical expertise over price.", "bargaining_power_of_suppliers": "High; radiation oncology hardware (Varian, Elekta) and oncology biologics suppliers possess strong pricing leverage.", "threat_of_substitutes": "Low; oncology treatment modalities are medically indispensable.", "competitive_rivalry": "Moderate; competes with general tertiary hospital oncology wings and Tata Memorial Centre."}
    ),
    (
        "Manipal Hospitals", "Hospital Networks & Healthcare Delivery",
        "urban Indian patients seeking multi-specialty tertiary clinical excellence backed by academic medical heritage",
        "need reliable, comprehensive tertiary healthcare backed by university-grade medical research and top-tier physician specialists",
        "Manipal Hospital Network & Academic Medical Centers", "Pan-India Multi-Specialty Quaternary Hospital Network",
        "operates India's second-largest hospital chain (9,500+ beds across 33 hospitals) backed by Temasek, delivering top-ranked clinical care",
        [0.70, 0.88, 0.95, 0.93, 0.85, 0.65],
        {"political": "Key participant in Ayushman Bharat PM-JAY and national academic medical training (DNB residency programs).", "economic": "Aggressive expansion via acquisitions (Columbia Asia, Vikram Hospital, AMRI Hospitals) creates strong scale economies.", "social": "Deep multi-generational brand trust originating from Manipal University's pioneering medical education roots.", "technological": "Robotic surgical systems, advanced ECMO, heart-lung transplants, and AI-assisted clinical decision support systems.", "legal": "NABH, NABL, and JCI accredited, adhering strictly to clinical governance and patient rights charters.", "environmental": "Green OT certifications, extensive rainwater harvesting, and zero-liquid discharge effluent treatment across campuses."},
        [0.22, 0.45, 0.42, 0.25, 0.70],
        {"threat_of_new_entrants": "Low; building a 9,500-bed hospital network requires billions of dollars of institutional capital and decades of reputation.", "bargaining_power_of_buyers": "Moderate; private insured patients evaluate hospital network empanelment.", "bargaining_power_of_suppliers": "Moderate; massive centralized scale provides strong bargaining leverage over medical equipment vendors.", "threat_of_substitutes": "Low; tertiary inpatient clinical care cannot be substituted.", "competitive_rivalry": "High with Apollo, Max, and Fortis in Bengaluru, Delhi-NCR, and Kolkata."}
    ),
    (
        "Sir Ganga Ram Hospital", "Hospital Networks & Healthcare Delivery",
        "patients from North India and neighboring countries needing high-trust tertiary referral care without commercial corporate hospital pressures",
        "seek world-class clinical expertise and ethical medical care operated by a non-profit trust with transparent physician consultations",
        "Sir Ganga Ram Tertiary Referral Hospital & Research Institute", "Non-Profit Trust Quaternary Referral Hospital",
        "operates a legendary 675-bed non-profit trust hospital in New Delhi where private revenue cross-subsidizes free treatment for 20% of beds for impoverished citizens",
        [0.75, 0.85, 0.96, 0.92, 0.86, 0.65],
        {"political": "Non-profit trust charter mandates 20% reserved beds for economically weaker sections (EWS) free of cost.", "economic": "Unique self-sustaining society model reinvesting all operating surplus into medical research, equipment upgrades, and subsidized care.", "social": "Immense public trust built over 70+ years in Delhi as the ultimate ethical second-opinion medical institution.", "technological": "Pioneered minimal access surgery, multi-organ liver and kidney transplantation, and extensive clinical research laboratories.", "legal": "NABH and NABL accredited; compliant with Delhi High Court EWS treatment guidelines and human organ transplant laws.", "environmental": "Full bio-medical waste segregation, modern incinerator-free waste processing, and energy-efficient building systems."},
        [0.18, 0.40, 0.40, 0.22, 0.58],
        {"threat_of_new_entrants": "Low; impossible for commercial corporate entrants to replicate Ganga Ram's 70-year non-profit trust reputation.", "bargaining_power_of_buyers": "Low; demand consistently outstrips bed capacity with long waiting lists for elective surgeries.", "bargaining_power_of_suppliers": "Moderate; ethical procurement committees evaluate equipment on clinical efficacy rather than commercial deals.", "threat_of_substitutes": "Low for complex referral medical cases.", "competitive_rivalry": "Low; operates above commercial rivalry due to charitable trust status."}
    ),
    (
        "Tata Memorial Centre", "Hospital Networks & Healthcare Delivery",
        "cancer patients from all socioeconomic strata across India and SAARC nations",
        "need evidence-based, subsidized, and compassionate cancer treatment adhering to global oncological clinical trial protocols",
        "Tata Memorial Hospital & Advanced Centre for Treatment, Research and Education in Cancer (ACTREC)", "Autonomous Grant-in-Aid National Comprehensive Cancer Centre",
        "stands as India's apex public cancer institute, treating over 70,000 new cancer patients annually with 70% receiving free or heavily subsidized care",
        [0.90, 0.90, 0.99, 0.96, 0.90, 0.70],
        {"political": "Funded and managed under Department of Atomic Energy, Government of India; apex national policy maker for cancer care.", "economic": "Government budgetary grants and philanthropic endowments insulate institution from commercial market pressures.", "social": "The ultimate national haven of hope for impoverished cancer patients, providing state-of-the-art oncology care regardless of paying capacity.", "technological": "Pioneered landmark global clinical trials in breast cancer, bone marrow transplants, and indigenously engineered CAR-T cell therapy.", "legal": "Highest statutory oversight, ethical review boards, and global clinical trial compliance.", "environmental": "World-class nuclear medicine waste containment, radiopharmaceutical decay facilities, and biohazard incineration."},
        [0.08, 0.20, 0.35, 0.15, 0.30],
        {"threat_of_new_entrants": "Non-existent; state-funded apex national institute with global clinical research prestige.", "bargaining_power_of_buyers": "None; patients seek admission based on institutional excellence and subsidized care.", "bargaining_power_of_suppliers": "Low; government public procurement rules and massive patient volume command lowest prices from global pharma.", "threat_of_substitutes": "None; apex referral institute.", "competitive_rivalry": "None; collaborates with all hospitals through the National Cancer Grid."}
    ),
    (
        "Aravind Eye Care System", "Hospital Networks & Healthcare Delivery",
        "preventable blind and visually impaired individuals across rural and urban India and global developing nations",
        "require high-volume, high-quality cataract and ophthalmic surgeries to restore sight without economic devastation",
        "High-Efficiency Cataract Surgical Model & Aurolab Intraocular Lenses", "High-Volume Self-Sustaining Eye Care Network",
        "performed over 8 million eye surgeries using a cross-subsidy model where 50% paying patients fully fund free surgeries for the impoverished half",
        [0.80, 0.92, 0.99, 0.94, 0.88, 0.72],
        {"political": "Global case study partner for WHO 'Vision 2020: The Right to Sight' and Harvard Business School.", "economic": "Financially self-sustaining non-profit that has never taken government grants, funded entirely by paying patients and Aurolab lens sales.", "social": "Restores sight and economic livelihood to millions of rural Indians, breaking intergenerational poverty cycles caused by blindness.", "technological": "Standardized two-bed surgical suites where a single ophthalmic surgeon performs 6-8 cataract surgeries per hour with near-zero infection rates.", "legal": "NABH accredited; Aurolab lenses comply with European CE and US FDA regulatory standards.", "environmental": "Produces 1/20th the carbon footprint of equivalent UK NHS cataract surgeries through lean, reusable sterilization protocols."},
        [0.10, 0.30, 0.25, 0.15, 0.40],
        {"threat_of_new_entrants": "Low; impossible for commercial clinics to match Aravind's mission-driven physician retention and manufacturing scale.", "bargaining_power_of_buyers": "Low; patients receive highest quality care at either zero cost or transparently low fees.", "bargaining_power_of_suppliers": "Negligible; Aurolab manufactures indigenous intraocular lenses, sutures, and ophthalmic blades at 10% of global cost.", "threat_of_substitutes": "Low; cataract removal is the only cure for lens opacity.", "competitive_rivalry": "Low; operates on compassion and service rather than commercial competition."}
    ),
    (
        "Dr. Agarwal's Eye Hospital", "Hospital Networks & Healthcare Delivery",
        "patients seeking advanced refractive, cataract, and complex corneal eye surgeries across India and Africa",
        "need cutting-edge ophthalmic surgical innovation (glued IOL, PDEK) delivered in modern, patient-friendly specialized eye clinics",
        "Glued IOL & Pre-Descemet's Endothelial Keratoplasty (PDEK)", "Specialized Ophthalmic Surgical Hospital Chain",
        "pioneered global surgical innovations like Glued IOL for aphakic eyes and PDEK corneal transplants across 160+ specialized eye care centers",
        [0.66, 0.84, 0.92, 0.92, 0.82, 0.60],
        {"political": "Expanding ophthalmic infrastructure into Tier 2/3 Indian towns aligned with national blindness control programs.", "economic": "Strong private equity backing (TPG, Temasek) funding aggressive clinic rollout across South and West India and Africa.", "social": "Provides accessible eye surgeries, SMILE laser vision correction, and pediatric ophthalmology to middle-class families.", "technological": "Proprietary surgical techniques published in international journals; state-of-the-art femtosecond lasers and optical coherence tomography.", "legal": "NABH accredited centers complying with ophthalmic day-care surgical regulations.", "environmental": "Strict sterilization of micro-instruments and safe disposal of ophthalmic viscoelastics and sharps."},
        [0.28, 0.50, 0.40, 0.28, 0.68],
        {"threat_of_new_entrants": "Moderate; local ophthalmologists can open single clinics, but cannot match Dr. Agarwal's surgical innovation brand.", "bargaining_power_of_buyers": "Moderate; patients compare prices for premium refractive laser surgeries (LASIK/SMILE).", "bargaining_power_of_suppliers": "Moderate; global ophthalmic laser and microscope suppliers (Zeiss, Alcon, Bausch + Lomb).", "threat_of_substitutes": "Moderate from eyeglasses and contact lenses for refractive errors.", "competitive_rivalry": "High with ASG Eye Hospitals, Eye-Q, and Center for Sight."}
    ),
    (
        "Sankara Nethralaya", "Hospital Networks & Healthcare Delivery",
        "patients with complex vitreoretinal diseases, pediatric ocular cancers, and complex corneal disorders",
        "seek world-class, ethical charitable ophthalmic care driven by clinical research without commercial profit motives",
        "Charitable Ophthalmic Specialty & Vitreoretinal Surgery Institute", "Non-Profit Tertiary Eye Hospital & Research Centre",
        "operates as India's premier charitable non-profit eye hospital in Chennai, treating 1,500 outpatients daily with zero physician commission culture",
        [0.75, 0.88, 0.98, 0.94, 0.86, 0.68],
        {"political": "Established under the guidance of Kanchi Kamakoti Peetham; recognized as an Institute of National Importance in eye care.", "economic": "Philanthropic cross-subsidization where revenue from private rooms fully finances free surgeries for 35% of indigent patients.", "social": "Revered nationwide for complete medical ethics, where doctors receive fixed salaries with zero incentives for prescribing surgeries.", "technological": "Pioneered mobile eye surgical units (MESU) operating inside rural villages with laminar airflow OT sterilization.", "legal": "NABH and NABL accredited, complying with ethical clinical research and human corneal donation laws.", "environmental": "Solar energy generation, green building practices, and clinical waste neutralization."},
        [0.12, 0.32, 0.30, 0.16, 0.45],
        {"threat_of_new_entrants": "Low; unparalleled medical reputation built over 45+ years of ethical non-profit service.", "bargaining_power_of_buyers": "Low; patients travel from across India and Bangladesh seeking expert retinal and corneal care.", "bargaining_power_of_suppliers": "Low; suppliers offer preferential institutional pricing to charitable trusts.", "threat_of_substitutes": "Low for complex retinal detachments and ocular oncology.", "competitive_rivalry": "Low; non-commercial mission operates beyond market rivalry."}
    ),
    (
        "Cloudnine Hospitals", "Hospital Networks & Healthcare Delivery",
        "expectant modern urban parents and new mothers in Tier-1 metros",
        "need luxury, boutique maternity care, comprehensive fetal medicine, and celebratory childbirth experiences with intensive clinical backup",
        "Boutique Birthing & Comprehensive Perinatal Care Suites", "Boutique Maternal, Fetal & Neonatal Healthcare Chain",
        "pioneered boutique maternity hospitality in India, combining 5-star hotel comfort with Level-3 neonatal intensive care and 99.8% safe delivery records",
        [0.65, 0.85, 0.94, 0.90, 0.82, 0.60],
        {"political": "Complies with PCPNDT Act regulations, maternity benefit directives, and national newborn health guidelines.", "economic": "High out-of-pocket and corporate insurance spending by dual-income urban millennial couples willing to spend for childbirth comfort.", "social": "Transforms childbirth from a stressful hospital stay into a joyful, celebratory family milestone with luxury suites and prenatal fitness.", "technological": "Advanced 4D fetal ultrasound screening, genetic anomaly testing, high-tech Level-3 NICU pods, and mobile prenatal tracking apps.", "legal": "NABH accredited, strictly adhering to anti-sex selection laws and clinical obstetric safety guidelines.", "environmental": "Eco-friendly baby care amenities, safe placental biological waste incineration, and energy-conserving maternity suites."},
        [0.32, 0.48, 0.40, 0.25, 0.68],
        {"threat_of_new_entrants": "Moderate; boutique maternity requires real estate in affluent suburbs, but clinical obstetric reputation takes years to build.", "bargaining_power_of_buyers": "Moderate; affluent parents evaluate luxury maternity packages against traditional hospitals.", "bargaining_power_of_suppliers": "Moderate; fetal monitors, ultrasound scanners, and neonatal incubators.", "threat_of_substitutes": "Low; institutional hospital delivery is mandatory for safety.", "competitive_rivalry": "High in metro cities with Motherhood Hospitals and Apollo Cradle."}
    ),
    (
        "Motherhood Hospitals", "Hospital Networks & Healthcare Delivery",
        "urban mothers and families seeking comprehensive maternal, gynecological, and pediatric specialty care",
        "require clinically sound, compassionate mother-and-child healthcare close to residential neighborhoods without visiting chaotic general hospitals",
        "Neighborhood Mother & Child Specialty Clinics", "Specialized Perinatal & Pediatric Hospital Network",
        "delivers specialized maternity, advanced laparoscopic gynecology, and Level-3 NICU care across 20+ specialized centers in South and West India",
        [0.65, 0.84, 0.93, 0.89, 0.82, 0.60],
        {"political": "Complies with maternal health safety guidelines and Pre-Conception and Pre-Natal Diagnostic Techniques (PCPNDT) rules.", "economic": "Asset-light leasehold model enables rapid suburban expansion and fast breakeven per clinic.", "social": "Growing urban preference for specialized women-and-children hospitals over intimidating multi-specialty trauma centers.", "technological": "Advanced neonatal monitoring, fetal medicine imaging, and comprehensive electronic medical records for pediatric vaccination tracking.", "legal": "NABH accredited, strict compliance with newborn care and medical negligence standards.", "environmental": "Safe biological waste handling and energy-efficient suburban clinic architecture."},
        [0.34, 0.50, 0.40, 0.26, 0.70],
        {"threat_of_new_entrants": "Moderate; requires medical zoning clearances and gynecologist partnerships.", "bargaining_power_of_buyers": "Moderate; suburban families compare maternity package inclusions.", "bargaining_power_of_suppliers": "Moderate; medical consumables and infant care supplies.", "threat_of_substitutes": "Low; hospital delivery is essential.", "competitive_rivalry": "Intense with Cloudnine and local private nursing homes in Bengaluru, Mumbai, and Pune."}
    ),
    (
        "CARE Hospitals", "Hospital Networks & Healthcare Delivery",
        "middle-income patients across Tier-2 and Tier-3 cities in central and southern India",
        "need advanced cardiac, critical care, and multi-specialty hospital treatment without having to migrate to expensive tier-1 metros",
        "Tier-2 Multi-Specialty Healthcare Network", "Regional Tertiary Healthcare Network",
        "founded by cardiologists, operating 16+ hospitals across 7 cities with deep market leadership in Hyderabad, Bhubaneswar, Raipur, and Visakhapatnam",
        [0.68, 0.85, 0.92, 0.88, 0.82, 0.62],
        {"political": "Empaneled with state health insurance schemes (Biju Swasthya Kalyan Yojana, Aarogyasri), serving public scheme beneficiaries.", "economic": "Backed by Blackstone, driving consolidation and brownfield bed expansions across underserved Tier 2 industrial hubs.", "social": "Delivers life-saving cardiac catheterization and stroke interventions in cities that previously had no advanced cath labs.", "technological": "Equipped with biplane cath labs, advanced critical care telemetry, and modular laminar OTs.", "legal": "NABH and NABL accredited, adhering to Clinical Establishments Act and medical audit standards.", "environmental": "Hospital sewage treatment plants, medical waste autoclaving, and solar power integration."},
        [0.26, 0.50, 0.40, 0.25, 0.64],
        {"threat_of_new_entrants": "Low to moderate; strong regional physician loyalty and hospital brand trust in Tier-2 cities.", "bargaining_power_of_buyers": "Moderate; balance of government scheme patients and private cash/insurance patients.", "bargaining_power_of_suppliers": "Moderate; centralized procurement under Blackstone platform creates bargaining leverage.", "threat_of_substitutes": "Low for acute tertiary inpatient interventions.", "competitive_rivalry": "Moderate; primary competitor in central India is KIMS and local regional nursing homes."}
    ),
    (
        "Sahyadri Hospitals", "Hospital Networks & Healthcare Delivery",
        "patients across Maharashtra requiring advanced neurosurgery, multi-organ transplants, and trauma emergency care",
        "need specialized, accessible tertiary healthcare with proven surgical track records in neurosciences and solid organ transplantation",
        "Sahyadri Super Speciality Hospitals & Neurosciences Institute", "Regional Tertiary Care & Neurosciences Hospital Chain",
        "operates the largest hospital network in Maharashtra (over 1,000 beds across Pune, Nashik, Karad, and Navi Mumbai) specializing in neurosurgery",
        [0.68, 0.85, 0.92, 0.89, 0.82, 0.62],
        {"political": "Key healthcare provider empaneled under Maharashtra's Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY).", "economic": "Backed by Ontario Teachers' Pension Plan (OTPP), providing deep long-term institutional capital for multi-specialty expansion.", "social": "Pioneered advanced neurosurgical care and liver transplants in Western Maharashtra, serving both urban and agricultural communities.", "technological": "Equipped with neuro-navigation suites, stereotactic radiosurgery, 3T MRI, and high-tech solid organ transplant intensive care units.", "legal": "NABH accredited, licensed for brain-dead organ retrieval and solid organ transplants under national regulatory bodies.", "environmental": "Bio-medical effluent neutralization, zero-liquid discharge STP, and solar energy capture."},
        [0.25, 0.48, 0.40, 0.24, 0.65],
        {"threat_of_new_entrants": "Low; deep clinician networks and multi-decade surgical trust across Pune and Western Maharashtra.", "bargaining_power_of_buyers": "Moderate; mix of corporate insurance, self-pay, and government scheme patients.", "bargaining_power_of_suppliers": "Moderate; standard medical device and surgical consumable procurement.", "threat_of_substitutes": "Low; emergency neurosurgery and trauma care have zero substitutes.", "competitive_rivalry": "Moderate with Ruby Hall Clinic and Jehangir Hospital in Pune."}
    )
]

for item in sector8_data:
    add_c(*item)

print(f"Sector 8 added: {len(sector8_data)} companies. Total: {len(part2_a)}")

# ==============================================================================
# SECTOR 9: FMCG, Personal Care & Packaged Foods (25 companies)
# ==============================================================================
sector9_data = [
    (
        "ITC Limited - Foods & Personal Care", "FMCG, Personal Care & Packaged Foods",
        "Indian households across metro, tier-1, tier-2, and rural markets",
        "demand trustworthy, premium packaged staples, snacks, personal hygiene, and biscuits backed by uncompromised quality and hygiene",
        "Aashirvaad Atta, Sunfeast, Bingo & Savlon", "Branded Consumer Foods & Personal Care Portfolio",
        "leverages e-Choupal farm-gate sourcing and 7 million retail touchpoints to deliver India's #1 packaged wheat flour, snacks, and antiseptic hygiene",
        [0.72, 0.90, 0.96, 0.88, 0.84, 0.85],
        {"political": "Supports government millets mission (Shree Anna), PM Formalisation of Micro food enterprises, and agricultural farm-gate value addition.", "economic": "Non-cigarette FMCG business crossed Rs 20,000 Cr in consumer spend, self-funded by immense corporate cash flows.", "social": "Deep Indian consumer trust; Aashirvaad atta transformed traditional unbranded chakkis into hygienic packaged flour across 100M homes.", "technological": "Customized wheat-grain blending algorithms, high-speed automated extrusion lines, and AI-driven supply chain replenishment.", "legal": "FSSAI compliance, Legal Metrology packaged commodity standards, and strict advertising standards (ASCI).", "environmental": "Global exemplar in sustainability: water-positive for 22 years, carbon-positive for 18 years, and 100% recyclable plastic packaging roadmap."},
        [0.30, 0.60, 0.35, 0.35, 0.78],
        {"threat_of_new_entrants": "Low to moderate; entering FMCG is easy for local brands, but matching ITC's 7-million store distribution moat is near impossible.", "bargaining_power_of_buyers": "High; Indian consumers are value-conscious with zero switching cost between snack or biscuit brands.", "bargaining_power_of_suppliers": "Low; backward-integrated into direct farm sourcing via e-Choupal eliminates middleman price leverage.", "threat_of_substitutes": "Moderate from local unbranded loose commodities and regional namkeen makers.", "competitive_rivalry": "Fierce; battles Britannia, Parle, Marico, and HUL across every grocery aisle."}
    ),
    (
        "Marico Limited", "FMCG, Personal Care & Packaged Foods",
        "urban and semi-urban Indian consumers seeking pure hair nourishment and healthy edible cooking oils",
        "need 100% pure, unadulterated coconut oil for traditional hair nourishment and blended edible oils that manage cholesterol and cardiovascular health",
        "Parachute Coconut Oil & Saffola Edible Oils", "Branded Edible Oils & Hair Nourishment Solutions",
        "dominates Indian hair care and heart wellness with over 60% market share in coconut oil and trusted cardiologist-recommended blended cooking oils",
        [0.65, 0.86, 0.92, 0.84, 0.80, 0.72],
        {"political": "Engages with Coconut Development Board and monitors agricultural import tariffs on crude edible palm and sunflower oils.", "economic": "Resilient operating margins supported by pricing power and copra raw material hedging on commodity exchanges.", "social": "Parachute is an iconic Indian household staple present in 1 out of 3 Indian households; Saffola pioneered urban heart-health awareness.", "technological": "Proprietary triple-filtration copra processing technology and LOSORB oil-absorption reduction in fried foods.", "legal": "Strict adherence to FSSAI packaging guidelines and trans-fat limits.", "environmental": "Pioneered water stewardship across copra farmer belts in Tamil Nadu and Kerala; converting packaging to post-consumer recycled plastic."},
        [0.32, 0.62, 0.45, 0.35, 0.72],
        {"threat_of_new_entrants": "Low in branded pure coconut oil due to immense consumer trust in the blue Parachute bottle; moderate in foods.", "bargaining_power_of_buyers": "Moderate to high; edible oil consumers switch if price gaps with sunflower or mustard oil widen.", "bargaining_power_of_suppliers": "Moderate; copra and vegetable oil prices fluctuate with monsoons and global agricultural yields.", "threat_of_substitutes": "Moderate from modern hair serums and regional mustard/groundnut cooking oils.", "competitive_rivalry": "Moderate in hair oils; high in healthy foods (Saffola Oats vs. Quaker/Kellogg's)."}
    ),
    (
        "Dabur India", "FMCG, Personal Care & Packaged Foods",
        "multi-generational Indian households seeking natural, Ayurvedic wellness and immunity products",
        "need authentic, time-tested Ayurvedic formulations and natural herbal personal care free from harsh synthetic chemicals",
        "Dabur Chyawanprash, Honey, Vatika & Real Fruit Juices", "Natural Ayurvedic Consumer Health & Packaged Food",
        "stands as the world's largest Ayurvedic consumer goods brand with 140 years of herbal heritage, leading in immunity, pure honey, and fruit juices",
        [0.70, 0.88, 0.95, 0.85, 0.82, 0.75],
        {"political": "Direct beneficiary of Ministry of AYUSH institutional backing, herbal cultivation subsidies, and Ayurvedic medicine promotion.", "economic": "Strong rural sales footprint (>45% of domestic revenue) benefiting from rural infrastructure spending and monsoon prosperity.", "social": "Chyawanprash is the bedrock of family immunity in North and East India; growing consumer shift towards natural herbal products.", "technological": "Modern scientific validation of classical Ayurvedic herbs using clinical trials, automated botanical extraction, and sterile juice bottling.", "legal": "Compliant with Drugs and Cosmetics Act (Ayurvedic division), FSSAI food norms, and NMR purity testing for honey.", "environmental": "Extensive contract farming for endangered medicinal herbs, plastic-neutral certification, and solar-powered manufacturing plants."},
        [0.28, 0.58, 0.38, 0.30, 0.74],
        {"threat_of_new_entrants": "Moderate; many herbal startups emerge, but matching Dabur's 140-year Ayurvedic trust and clinical credibility is difficult.", "bargaining_power_of_buyers": "Moderate; brand-loyal consumers stick to Dabur Chyawanprash and Honey, but juices face retail competition.", "bargaining_power_of_suppliers": "Low to moderate; large contract farming network for Amla, herbs, and direct beekeeper honey procurement.", "threat_of_substitutes": "Moderate from allopathic vitamins, dietary supplements, and soft drinks.", "competitive_rivalry": "High with Patanjali, Baidyanath, Emami, and multinational consumer health brands."}
    ),
    (
        "Godrej Consumer Products", "FMCG, Personal Care & Packaged Foods",
        "mass-market consumers across India, Africa, and Latin America",
        "require affordable, highly effective home mosquito protection, gentle personal hygiene soaps, and convenient hair coloring",
        "Goodknight, HIT, Cinthol & Godrej Expert Rich Crème", "Household Insecticides & Mass Personal Care",
        "leads the household insecticide market in India and hair color across emerging nations, making daily hygiene and vector protection affordable for all",
        [0.66, 0.86, 0.92, 0.86, 0.82, 0.70],
        {"political": "Collaborates with public health authorities on malaria and dengue mosquito vector control campaigns.", "economic": "Democratized hair color with Rs 30 Godrej Expert Crème sachet, converting millions from powder to cream formulation.", "social": "Goodknight is ubiquitous across Indian homes to prevent vector-borne diseases; Cinthol is synonymous with outdoor adventure and freshness.", "technological": "Pioneered low-smoke mosquito coils, fast-card paper mosquito repellents, and advanced micro-encapsulation perfume chemistry.", "legal": "Central Insecticides Board (CIB) registrations and stringent chemical safety standards for household pesticides.", "environmental": "Pioneered sustainable palm oil sourcing, zero-waste-to-landfill manufacturing, and reduction of volatile organic compounds (VOCs)."},
        [0.26, 0.60, 0.40, 0.32, 0.72],
        {"threat_of_new_entrants": "Low in household insecticides due to strict CIB chemical registration hurdles; moderate in soaps.", "bargaining_power_of_buyers": "Moderate to high; consumers expect maximum mosquito knockout power at accessible price points.", "bargaining_power_of_suppliers": "Moderate; active pesticide molecules (transfluthrin) and palm oil derivative feedstocks.", "threat_of_substitutes": "Moderate from electric zappers, mosquito nets, and natural citronella sprays.", "competitive_rivalry": "High with Reckitt Benckiser (Mortein) and SC Johnson (All Out) in pest control; HUL in soaps."}
    ),
    (
        "Emami Limited", "FMCG, Personal Care & Packaged Foods",
        "working-class and rural Indian consumers seeking relief from physical fatigue, headaches, and skin dryness",
        "need intense cooling, pain-relieving therapeutic oils, multi-purpose antiseptic creams, and winter skincare at accessible price points",
        "Navratna Cool Oil, BoroPlus, Zandu Balm & Kesh King", "Therapeutic Ayurvedic Personal Care & OTC Healthcare",
        "dominates niche therapeutic personal care categories with over 65% market share in cooling hair oils and antiseptic skincare creams",
        [0.64, 0.85, 0.90, 0.82, 0.80, 0.65],
        {"political": "Compliant with AYUSH regulatory frameworks for over-the-counter herbal medicinal formulations.", "economic": "High gross margin profile (>65%) in niche therapeutic categories shielded from commodity price volatility.", "social": "Navratna 'Thanda Thanda Cool Cool' is an iconic stress-relief ritual for labor-intensive workers across Northern and Eastern India.", "technological": "Herbal infusion technology combining camphor, menthol, and nine Ayurvedic herbs without synthetic oil separation.", "legal": "Drugs and Cosmetics Act OTC herbal licensing and consumer trade promotion standards.", "environmental": "Transitioning to recyclable laminate tubes and bio-degradable personal care formulation ingredients."},
        [0.30, 0.58, 0.35, 0.32, 0.68],
        {"threat_of_new_entrants": "Low in specialized therapeutic niches (cooling oils, pain balms); high in general skincare.", "bargaining_power_of_buyers": "Moderate; consumers view BoroPlus and Zandu Balm as medicinal necessities rather than lifestyle luxuries.", "bargaining_power_of_suppliers": "Low; widely sourced menthol, liquid paraffin, and medicinal botanical extracts.", "threat_of_substitutes": "Moderate from allopathic pain-relief gels (Volini, Moov) and petroleum jelly.", "competitive_rivalry": "Moderate; dominates its core sub-segments while facing competition from Dabur and Patanjali."}
    ),
    (
        "Patanjali Ayurved", "FMCG, Personal Care & Packaged Foods",
        "patriotic and health-conscious Indian consumers seeking Swadeshi, natural daily essentials",
        "demand chemical-free, indigenous Ayurvedic food staples, cow ghee, toothpaste, and personal care at disruptive, affordable prices",
        "Patanjali Dant Kanti, Cow Ghee & Kesh Kanti", "Swadeshi Ayurvedic Essentials & Daily Consumables",
        "sparked the indigenous 'Swadeshi' FMCG revolution in India, building a multi-billion dollar enterprise on natural ingredients and accessible pricing",
        [0.78, 0.88, 0.96, 0.82, 0.82, 0.72],
        {"political": "Strong ideological alignment with national self-reliance (Atmanirbhar Bharat), yoga promotion, and indigenous agro-processing.", "economic": "Disrupted established MNC pricing power by offering natural products at 20-30% lower prices with massive retail footfalls.", "social": "Endorsed by yoga guru Baba Ramdev, creating massive religious and cultural resonance across semi-urban and rural families.", "technological": "Mega Food Parks in Haridwar, automated cow ghee clarification plants, and modern herbal testing laboratories.", "legal": "Monitored closely by FSSAI for food standards and ASCI for advertisement claim substantiations.", "environmental": "Promotes organic farming, indigenous cow breed conservation, and natural bio-fertilizers."},
        [0.32, 0.60, 0.32, 0.35, 0.75],
        {"threat_of_new_entrants": "Moderate; many herbal brands followed, but none possess Ramdev's mass spiritual following.", "bargaining_power_of_buyers": "High; value-conscious consumers demand low prices and switch if quality slips.", "bargaining_power_of_suppliers": "Low; massive direct farmer sourcing network for amla, wheat, and raw cow milk.", "threat_of_substitutes": "High from conventional FMCG giants (HUL, Colgate, Dabur).", "competitive_rivalry": "Fierce; sparked intense retaliatory herbal launches from Colgate (Vedshakti) and HUL (Ayush)."}
    ),
    (
        "Britannia Industries", "FMCG, Personal Care & Packaged Foods",
        "every Indian household across all age groups and income demographics",
        "need delicious, hygienic, and nutritious bakery biscuits, cakes, dairy, and rusks for daily tea-time snacking and on-the-go nourishment",
        "Good Day, Marie Gold, Milk Bikis, NutriChoice & Bourbon", "Packaged Biscuits, Bakery Snacks & Value-Added Dairy",
        "serves over 100 million Indian consumers daily with iconic bakery brands, unmatched distribution reach across 6 million outlets, and fortified nutrition",
        [0.68, 0.90, 0.96, 0.86, 0.82, 0.74],
        {"political": "Pioneered micronutrient fortification (iron, vitamins) in mass biscuits supporting national nutrition initiatives.", "economic": "Consistently generates superior ROCE (>40%) driven by high asset turns, direct distribution, and continuous premiumization (Good Day Harmony).", "social": "Marie Gold and Good Day are deeply woven into daily Indian morning and evening tea rituals across all social strata.", "technological": "Automated mega-baking tunnel ovens running at 1,500 biscuits per minute with laser inspection and zero manual touch packaging.", "legal": "FSSAI packaging compliance, nutritional disclosure labeling, and Legal Metrology rules.", "environmental": "Zero trans-fat across all biscuits, 100% plastic waste collection neutrality, and factory biomass boilers."},
        [0.28, 0.62, 0.42, 0.38, 0.80],
        {"threat_of_new_entrants": "Low to moderate; local bakeries exist, but cannot match Britannia's mega-scale baking economics and brand recall.", "bargaining_power_of_buyers": "High; consumers readily switch between Britannia, Parle, and ITC if pricing or pack grammage fluctuates.", "bargaining_power_of_suppliers": "Moderate; flour, sugar, and palm oil input costs are commodity-driven.", "threat_of_substitutes": "High from traditional Indian snacks (namkeens, samosas, fruits).", "competitive_rivalry": "Intense duopoly battle with Parle Products across mass biscuits, and ITC Sunfeast in premium cookies."}
    ),
    (
        "Parle Products", "FMCG, Personal Care & Packaged Foods",
        "every Indian citizen from remote village hamlets to bustling railway stations and metro cities",
        "require unbeatable energy-giving glucose biscuits, crisp crackers, and confections at the most disciplined, pocket-friendly price points",
        "Parle-G, Monaco, Krackjack & Hide & Seek", "Mass Biscuits, Crackers & Premium Cookies",
        "manufactures Parle-G—the world's bestselling biscuit by volume—maintaining a sacred Rs 5 entry price point for over 25 years through hyper-efficient manufacturing",
        [0.66, 0.92, 0.98, 0.85, 0.80, 0.72],
        {"political": "The quintessential national emergency food ration during floods, disasters, and monsoons, praised for reliable caloric sustenance.", "economic": "Master of hyper-volume, thin-margin economics; sells billions of packs annually across 8 million retail kirana stores.", "social": "Parle-G is an immortal cultural icon synonymous with childhood nostalgia, dunked in hot chai across 4 generations of Indians.", "technological": "High-speed continuous baking conveyor systems and automated high-density packaging minimizing film usage.", "legal": "FSSAI food hygiene standards and compliance with packaged commodity weight norms.", "environmental": "Pioneered carton recycling, energy-efficient gas-fired ovens, and localized manufacturing to minimize transport emissions."},
        [0.25, 0.65, 0.40, 0.35, 0.82],
        {"threat_of_new_entrants": "Practically impossible at the Rs 5 price point; nobody can replicate Parle-G's economies of scale.", "bargaining_power_of_buyers": "High; consumers expect uncompromising volume at fixed entry price coins.", "bargaining_power_of_suppliers": "Moderate; massive bulk purchaser of agricultural wheat, sugar, and packaging film.", "threat_of_substitutes": "Moderate; biscuits are the cheapest packaged caloric snack in India.", "competitive_rivalry": "Relentless rivalry with Britannia and ITC Sunfeast across every biscuit segment."}
    ),
    (
        "Haldiram's Snacks", "FMCG, Personal Care & Packaged Foods",
        "Indian families, festive celebrators, and global Indian diaspora seeking authentic traditional ethnic tastes",
        "need authentic, hygienic traditional Indian namkeens, sweets, and ready-to-eat meals that preserve heirloom recipes without quality degradation",
        "Haldiram's Aloo Bhujia, Soan Papdi & Ready-to-Eat Curries", "Traditional Ethnic Indian Snacks & Packaged Sweets",
        "rules Indian ethnic snacking with over 40% market share in traditional namkeens, exporting authentic Indian taste to over 80 countries worldwide",
        [0.68, 0.90, 0.96, 0.84, 0.82, 0.70],
        {"political": "Champion of India's indigenous food heritage exports, receiving export awards from APEDA and Ministry of Food Processing.", "economic": "Generates over Rs 10,000 Cr in consolidated revenues, boasting superior profitability compared to multinational potato chip competitors.", "social": "Irreplaceable component of Indian festivals (Diwali, Rakhi), tea-time hospitality, and gifting traditions.", "technological": "State-of-the-art nitrogen-flushed automated packaging, vacuum frying, and continuous besan extrusion lines in Nagpur and Noida.", "legal": "US FDA, EU food safety, and FSSAI export-grade certifications.", "environmental": "Transitioning to solar-powered food processing plants and closed-loop oil recovery systems."},
        [0.26, 0.58, 0.38, 0.32, 0.74],
        {"threat_of_new_entrants": "Low to moderate; local halwais make sweets, but cannot match Haldiram's 6-month shelf life and national distribution.", "bargaining_power_of_buyers": "Moderate; consumers are fiercely brand loyal to Haldiram's specific spice blends and taste profile.", "bargaining_power_of_suppliers": "Low to moderate; pulses (moth dal, gram), spices, and edible oils sourced in bulk from agricultural mandis.", "threat_of_substitutes": "Moderate from western snacks (potato chips, nachos).", "competitive_rivalry": "Moderate; leads the market ahead of Bikaji, Balaji, and Bikano."}
    ),
    (
        "Bikaji Foods International", "FMCG, Personal Care & Packaged Foods",
        "ethnic snack lovers across Northern and Eastern India seeking authentic Rajasthani taste",
        "demand authentic, crispy Bikaneri bhujia, rasgullas, and ethnic namkeens crafted with genuine Bikaneri moth bean flour",
        "Bikaji Aslee Bikaneri Bhujia & Gulab Jamun", "Authentic Rajasthani Ethnic Savory Snacks",
        "holds Geographical Indication (GI) heritage leadership in Bikaneri Bhujia, delivering over 100 tons of authentic Rajasthani namkeens daily",
        [0.66, 0.86, 0.92, 0.82, 0.80, 0.68],
        {"political": "Promotes traditional Geographical Indication (GI) heritage of Bikaner agro-processing on the national stage.", "economic": "High growth trajectory driven by rapid retail expansion from core Rajasthan/Bihar/Assam stronghold into pan-India markets.", "social": "Deep cultural affinity in Hindi-speaking belts where Bikaji Bhujia is consumed with tea, poha, and meals daily.", "technological": "Modern automated dough kneading, frying, and nitrogen packaging plants in Bikaner maintaining artisanal texture.", "legal": "GI tag compliance for Bikaneri Bhujia and strict FSSAI quality norms.", "environmental": "Solar rooftop installations in desert manufacturing facilities and water recycling systems."},
        [0.30, 0.60, 0.38, 0.32, 0.72],
        {"threat_of_new_entrants": "Moderate; regional namkeen makers compete locally, but lack Bikaji's automated modern scale and listed capital access.", "bargaining_power_of_buyers": "Moderate to high; consumers compare prices against Haldiram's and local sweet shops.", "bargaining_power_of_suppliers": "Moderate; specialty desert moth beans harvested in arid Rajasthan.", "threat_of_substitutes": "Moderate from western packaged snacks.", "competitive_rivalry": "High with Haldiram's and Balaji Wafers in Western and Northern markets."}
    ),
    (
        "Balaji Wafers", "FMCG, Personal Care & Packaged Foods",
        "value-conscious consumers, youth, and families in Western India (Gujarat, Maharashtra, Rajasthan, MP)",
        "seek maximum packet quantity and bold, spicy crunch in potato chips and namkeens without paying international advertising markups",
        "Balaji Potato Wafers, Farali & Masala Shing", "High-Grammage Low-Cost Snack Foods",
        "famously defeated multinational giants (PepsiCo Lay's) in Western India by offering 30-40% more snack grammage per packet at the exact same Rs 5 and Rs 10 price points",
        [0.65, 0.88, 0.94, 0.84, 0.80, 0.68],
        {"political": "A home-grown Gujarat entrepreneurial legend praised for grassroots rural employment and direct farmer contract procurement.", "economic": "Master of frugal manufacturing and minimal marketing spend; reinvests all operational savings directly into extra packet weight.", "social": "The undisputed snack champion of Gujarat and Maharashtra, consumed at every roadside tea stall, train journey, and family picnic.", "technological": "World-class automated potato peeling, continuous slicing, and Urschel fryers processing 100,000 kg of potatoes daily in Rajkot.", "legal": "FSSAI compliance, packaged commodity labeling, and environmental plastic waste collection agreements.", "environmental": "Captive wind and solar installations; wastewater treatment converting potato wash starch into useful bio-products."},
        [0.30, 0.65, 0.35, 0.35, 0.78],
        {"threat_of_new_entrants": "Low in Western India; Balaji's razor-thin margins and massive retailer goodwill deter new entrants.", "bargaining_power_of_buyers": "High; consumers love the extra grammage and would penalize any reduction in packet size.", "bargaining_power_of_suppliers": "Low to moderate; contracts with thousands of potato farmers in Gujarat with guaranteed purchase prices.", "threat_of_substitutes": "High from local namkeen makers and biscuit brands.", "competitive_rivalry": "Intense rivalry with PepsiCo (Lay's/Kurkure) and Prataap Snacks."}
    ),
    (
        "Gujarat Cooperative Milk Marketing Federation (Amul)", "FMCG, Personal Care & Packaged Foods",
        "every Indian household, culinary professional, and dairy consumer nationwide",
        "need 100% pure, unadulterated milk, butter, cheese, ghee, and dairy nutrition at fair prices while ensuring dairy farmers receive fair pay",
        "Amul Butter, Milk, Cheese, Ice Cream & Organic Staples", "Cooperative Dairy & FMCG Essential Products",
        "stands as the world's largest farmer-owned cooperative, processing over 30 million liters of milk daily and returning 80% of consumer spend directly to 3.6 million smallholder farmers",
        [0.85, 0.96, 0.99, 0.90, 0.86, 0.85],
        {"political": "The crown jewel of India's White Revolution; direct policy alignment with National Dairy Development Board and Ministry of Cooperation.", "economic": "Generates over Rs 72,000 Cr in annual group turnover; acts as the national price stabilizer ensuring milk remains affordable for all citizens.", "social": "The 'Taste of India' and the iconic Amul Girl topical cartoons have formed an indelible part of Indian cultural consciousness for 60+ years.", "technological": "Automated computerized milk testing and instant direct bank payments to millions of village women milk producers twice daily.", "legal": "FSSAI compliance, AGMARK ghee purity certification, and cooperative society legislative governance.", "environmental": "Promotes sustainable village dairy husbandry, biogas manure digesters, and energy-efficient bulk milk chilling centers."},
        [0.15, 0.50, 0.20, 0.25, 0.65],
        {"threat_of_new_entrants": "Practically impossible; no private corporate can match Amul's 3.6-million farmer cooperative procurement network and social trust.", "bargaining_power_of_buyers": "Low to moderate; Amul products are already priced at the lowest sustainable margin with massive brand loyalty.", "bargaining_power_of_suppliers": "None; the farmers ARE the owners and board members of the cooperative.", "threat_of_substitutes": "Low; milk and butter are daily dietary necessities with limited substitutes.", "competitive_rivalry": "Moderate; dominates the organized dairy sector ahead of Mother Dairy, Britannia, and Nestlé."}
    ),
    (
        "Mother Dairy Fruit & Vegetable", "FMCG, Personal Care & Packaged Foods",
        "urban households in Delhi-NCR and Northern India",
        "need fresh, pasteurized token milk, hygienic curd, and affordable fresh farm produce close to their residential housing societies",
        "Mother Dairy Token Milk, Mishti Doi & Safal Fresh Produce", "Urban Cooperative Dairy & Horticultural Distribution",
        "pioneered token automated milk vending machines and Safal fruit & vegetable outlets, supplying daily fresh essentials across Delhi-NCR",
        [0.78, 0.88, 0.94, 0.86, 0.84, 0.75],
        {"political": "Wholly owned subsidiary of the National Dairy Development Board (NDDB); critical instrument for urban food security.", "economic": "High daily cash collections and efficient cold-chain distribution ensure low spoilage and stable operating cash flows.", "social": "The lifeline of Delhi-NCR morning routines; Mother Dairy neighborhood booths serve as daily community touchpoints.", "technological": "Refrigerated insulated milk tankers, automated token dispensing machines, and controlled atmosphere cold stores for Safal produce.", "legal": "FSSAI food hygiene norms and municipal vendor licensing compliance.", "environmental": "Pioneered reusable container token milk dispensing, eliminating millions of single-use plastic milk pouches annually."},
        [0.25, 0.55, 0.30, 0.30, 0.70],
        {"threat_of_new_entrants": "Low in Delhi-NCR due to exclusive municipal land allotments for neighborhood milk and Safal booths.", "bargaining_power_of_buyers": "Moderate; consumers have access to Amul and local milkmen, but trust Mother Dairy's pasteurization.", "bargaining_power_of_suppliers": "Low; organized procurement from state dairy federations and farmer producer organizations.", "threat_of_substitutes": "Moderate from private dairy pouch brands.", "competitive_rivalry": "Intense competition with Amul across Delhi-NCR dairy counters."}
    ),
    (
        "Hatsun Agro Product", "FMCG, Personal Care & Packaged Foods",
        "rural and urban consumers across Tamil Nadu, Andhra Pradesh, Telangana, and Karnataka",
        "need fresh daily milk, rich curd, and innovative ice cream treats sourced directly from local dairy farmers",
        "Arokya Milk, Hatsun Curd & Arun Icecreams", "Private Dairy & Commercial Ice Cream Network",
        "operates South India's largest private dairy, collecting milk directly from over 400,000 farmers with zero middlemen and running 3,500+ exclusive Hatsun Daily outlets",
        [0.70, 0.88, 0.94, 0.88, 0.82, 0.72],
        {"political": "Compliant with state animal husbandry regulations and cattle welfare support schemes in South India.", "economic": "Direct procurement model delivers higher margins than peers; Arun Icecreams operates a unique franchised parlor model across Tier 2/3 towns.", "social": "Arokya is the gold standard for full-cream milk in Tamil Nadu; Arun Icecreams made novel bar ice creams accessible to small villages.", "technological": "Hatsun Milk Banks (HMB) equipped with automated analyzers and instant chilling within 15 minutes of milking.", "legal": "FSSAI dairy processing standards, cold chain compliance, and weights/measures legal audits.", "environmental": "Massive solar rooftop generation across processing plants and recyclable packaging initiatives."},
        [0.22, 0.54, 0.35, 0.28, 0.68],
        {"threat_of_new_entrants": "Low; building a 400,000-farmer daily chilled collection network requires decades of local rural trust and capital.", "bargaining_power_of_buyers": "Moderate; consumers are loyal to Arokya's thickness and creaminess.", "bargaining_power_of_suppliers": "Low to moderate; farmers receive prompt direct-bank payments every 10 days, securing supply loyalty.", "threat_of_substitutes": "Low for fresh daily milk; moderate in ice creams.", "competitive_rivalry": "Moderate; competes with state cooperative Aavin, Heritage Foods, and Amul in South India."}
    ),
    (
        "Heritage Foods", "FMCG, Personal Care & Packaged Foods",
        "urban households and families across Andhra Pradesh, Telangana, Karnataka, and Tamil Nadu",
        "need pure, quality-tested cow and buffalo milk, paneer, and rich curd for daily family nutrition",
        "Heritage Buffalo Milk, Curd, Ghee & Paneer", "Branded Value-Added Dairy Products",
        "serves over 1.5 million households daily with a strong cold chain and increasing focus on high-margin value-added curd and paneer",
        [0.68, 0.85, 0.92, 0.85, 0.82, 0.70],
        {"political": "Founded by the family of Andhra Pradesh Chief Minister N. Chandrababu Naidu; deep agricultural roots across rural AP.", "economic": "Expanding share of high-margin value-added products (>35% of revenue) driving margin expansion over plain pouch milk.", "social": "Deep brand equity in Hyderabad and Andhra towns, trusted for hygienic handling and consistent fat content.", "technological": "Automated pouch packaging lines, ultra-high-temperature (UHT) milk processing, and cold-chain GPS fleet tracking.", "legal": "FSSAI compliance, dairy farm sanitation guidelines, and statutory public company reporting.", "environmental": "Captive renewable energy projects (wind and solar) supplying over 80% of company manufacturing electricity."},
        [0.26, 0.58, 0.38, 0.30, 0.70],
        {"threat_of_new_entrants": "Low; establishing farm-level milk collection and chilled supply chains in South India has high entry hurdles.", "bargaining_power_of_buyers": "Moderate; urban buyers have options (Vijaya, Amul, Hatsun) if milk prices diverge.", "bargaining_power_of_suppliers": "Moderate; village collection agents compete for farmer milk supply with cooperatives.", "threat_of_substitutes": "Low for liquid milk; moderate for packaged curd vs. home-made curd.", "competitive_rivalry": "High with Hatsun Agro, Dodla Dairy, and Tirumala Milk."}
    ),
    (
        "Parag Milk Foods", "FMCG, Personal Care & Packaged Foods",
        "modern retail shoppers, gourmet food enthusiasts, and QSR restaurant chains across India",
        "require premium 100% cow milk dairy products, authentic cow ghee, specialized mozzarella cheese, and sports nutrition",
        "Gowardhan Ghee, Go Cheese & Avvatar Whey Protein", "Value-Added Cow Dairy & Active Nutrition Products",
        "rules the Indian cheese category with over 35% market share in pizza cheese and pioneered India's first 100% vegetarian indigenous whey protein (Avvatar)",
        [0.66, 0.85, 0.92, 0.88, 0.82, 0.70],
        {"political": "Beneficiary of central government dairy processing infrastructure development funds and PLI for food processing.", "economic": "Focus on high-value cow milk derivatives (cheese, whey, ghee) insulates business from low-margin liquid milk price wars.", "social": "Gowardhan is revered for yellow cow ghee; Go Cheese is the default choice for home pizzas and sandwiches for kids.", "technological": "Asia's largest single-location cheese manufacturing plant in Manchar, Maharashtra producing 40 tons of cheese daily; indigenous whey filtration.", "legal": "FSSAI certification and strict halal/vegetarian certifications for rennet-free cheese production.", "environmental": "Biogas co-generation from dairy effluent and advanced water recycling at dairy plants."},
        [0.28, 0.55, 0.40, 0.30, 0.68],
        {"threat_of_new_entrants": "Moderate; cheese making requires sophisticated ripening and enzymatic maturation technology.", "bargaining_power_of_buyers": "Moderate; QSR chains (Domino's, Pizza Hut) negotiate strictly, while retail consumers are brand loyal.", "bargaining_power_of_suppliers": "Moderate; relies on farmer collection networks in Western Maharashtra.", "threat_of_substitutes": "Moderate from imported cheese brands and alternative fitness whey proteins (Optimum Nutrition).", "competitive_rivalry": "Intense competition with Amul in cheese and butter, and local ghee makers."}
    ),
    (
        "Tata Consumer Products", "FMCG, Personal Care & Packaged Foods",
        "health-conscious and discerning Indian consumers seeking pure staples, tea, coffee, and pantry essentials",
        "need unadulterated iodized salt, high-quality packet tea blends, unpolished pulses, and organic pantry staples backed by absolute integrity",
        "Tata Salt, Tata Tea & Tata Sampann", "Branded Daily Food Staples & Beverage Ecosystem",
        "commands India's pantry with 'Desh Ka Namak' (Tata Salt) holding over 35% market share, alongside India's #1 tea company by volume",
        [0.75, 0.92, 0.98, 0.88, 0.86, 0.82],
        {"political": "Pioneered national iodized salt under National Iodine Deficiency Disorders Control Programme; strategic partner for Indian millet commercialization.", "economic": "Fast-growing FMCG powerhouse resulting from consolidation of Tata Chemicals consumer business and Tata Global Beverages.", "social": "'Desh Ka Namak' is synonymous with national integrity and honesty; 'Jaago Re' campaigns sparked mass civic awakening on social issues.", "technological": "Vacuum evaporation salt refining in Mithapur, automated leaf tea blending, and moisture-controlled packaging of unpolished pulses.", "legal": "FSSAI food safety regulations, AGMARK standards, and national packaged commodities acts.", "environmental": "Sustainable tea sourcing (Trustea certified), solar-powered packaging hubs, and recyclable packaging transitions."},
        [0.20, 0.52, 0.35, 0.28, 0.72],
        {"threat_of_new_entrants": "Low in salt due to massive coastal vacuum evaporation infrastructure; moderate in tea and packaged pulses.", "bargaining_power_of_buyers": "Moderate; Tata Salt costs mere rupees per month, making consumers completely insensitive to minor price fluctuations.", "bargaining_power_of_suppliers": "Low; backward-integrated into captive solar salt works in Gujarat and tea plantation associations.", "threat_of_substitutes": "Low; salt and tea are daily non-negotiable dietary rituals.", "competitive_rivalry": "Moderate in salt (duopoly with private labels); intense in tea against HUL (Brooke Bond/Red Label)."}
    ),
    (
        "Jyothy Labs", "FMCG, Personal Care & Packaged Foods",
        "middle and lower-middle-class Indian homemakers seeking superior fabric whiteness and household cleaning",
        "need affordable, effective solutions to prevent white clothes from yellowing and powerful grease-cutting dishwash at mass-market prices",
        "Ujala Fabric Whitener, Pril Dishwash & Exo Dishwash Bar", "Fabric Care, Dishwashing & Household Cleaning",
        "created the fabric whitener category with Ujala holding over 80% market share, revolutionizing laundry care across millions of Indian homes",
        [0.64, 0.84, 0.90, 0.82, 0.80, 0.65],
        {"political": "Complies with consumer safety regulations and Bureau of Indian Standards (BIS) for household cleaning formulations.", "economic": "Exceptional return on equity driven by debt-free balance sheet and deep penetration in South and West Indian grocers.", "social": "Ujala 'Chaar Boondon Wala' (four drops) is an iconic advertising memory; transformed laundry rituals without messy blue powders.", "technological": "Proprietary violet acid dye formulation that binds to cotton fibers to reflect optical whiteness under Indian sunlight.", "legal": "Compliant with Legal Metrology Act and environmental surfactant biodegradability standards.", "environmental": "Phosphate-free dishwash bars to protect freshwater lakes; zero hazardous chemical discharge in production."},
        [0.28, 0.58, 0.35, 0.32, 0.72],
        {"threat_of_new_entrants": "Low in liquid fabric whiteners due to Ujala's near-monopoly; high in dishwash and laundry detergents.", "bargaining_power_of_buyers": "Moderate to high; homemakers switch dishwash brands if competitor offers attractive free scrubber promotions.", "bargaining_power_of_suppliers": "Low; widely sourced basic surfactants, fragrances, and plastic bottles.", "threat_of_substitutes": "Moderate from laundry bleaches and modern washing machine liquid detergents.", "competitive_rivalry": "Fierce with HUL (Vim) in dishwashing, and Reckitt Benckiser (Robin Blue) in whiteners."}
    ),
    (
        "Agro Tech Foods", "FMCG, Personal Care & Packaged Foods",
        "urban Indian youth, movie lovers, and health-conscious families",
        "need instant, hot cinema-style snacking at home and heart-healthy premium cooking oils enriched with natural vitamins",
        "ACT II Popcorn & Sundrop Cooking Oil", "Convenience Snacking & Healthy Edible Oils",
        "commands over 85% market share in instant popcorn in India with ACT II, bringing American theater-style micro-snacking into Indian kitchens",
        [0.64, 0.82, 0.88, 0.84, 0.80, 0.65],
        {"political": "Complies with FSSAI regulations on food additives, trans-fats, and clear nutrition front-of-pack labeling.", "economic": "High-margin branded popcorn cushions commodity oil margin volatility; strong presence across modern retail and cinema chains.", "social": "ACT II made popcorn popping a fun, interactive family cooking ritual for kids and movie nights at home.", "technological": "Patented instant microwave popping bags and high-expansion hybrid corn grain sourcing.", "legal": "FSSAI food licensing, legal metrology packaging, and advertising standards compliance.", "environmental": "Biodegradable paper popping bags and sustainable sunflower/corn oil sourcing practices."},
        [0.32, 0.58, 0.40, 0.35, 0.68],
        {"threat_of_new_entrants": "Low in microwave popcorn due to proprietary bag technology; moderate in ready-to-eat bagged popcorn.", "bargaining_power_of_buyers": "Moderate; consumers view ACT II as the definitive synonym for instant popcorn.", "bargaining_power_of_suppliers": "Moderate; contract farming for high-expansion popping corn grains in Andhra Pradesh.", "threat_of_substitutes": "High from potato chips, nachos, and traditional namkeens.", "competitive_rivalry": "Low in instant un-popped corn; moderate in ready-to-eat gourmet popcorn (4700BC)."}
    ),
    (
        "DFM Foods", "FMCG, Personal Care & Packaged Foods",
        "schoolchildren and young teens in Tier-2, Tier-3, and semi-urban India",
        "seek playful, crunchy, and affordable extruded corn snacks packed with exciting flavors and collectible toy surprises",
        "CRAX Corn Rings, Fritts & Natkhat", "Extruded Corn Snacks & Children's Confectionery",
        "pioneered extruded finger snacks in India with CRAX rings, delighting children for 40 years with iconic wearable ring snacks and collectible toys",
        [0.62, 0.82, 0.88, 0.80, 0.78, 0.60],
        {"political": "Monitors regulations regarding food advertising targeting children and school-zone junk food limits.", "economic": "High volume driven by dedicated Rs 5 and Rs 10 price points; backed by private equity to expand distribution across Western and Eastern India.", "social": "Beloved childhood ritual of wearing CRAX rings on all five fingers before eating them; immense emotional nostalgia.", "technological": "Continuous twin-screw corn extrusion, automated seasoning tumbling, and integrated high-speed toy insertion lines.", "legal": "FSSAI food safety regulations and toy safety certifications (BIS) for embedded plastic toys.", "environmental": "Transitioning to thinner multi-layer packaging films to reduce plastic volume per unit snack."},
        [0.35, 0.65, 0.35, 0.38, 0.76],
        {"threat_of_new_entrants": "Moderate; small regional extruders emerge, but matching CRAX brand equity and toy supply chain is challenging.", "bargaining_power_of_buyers": "High; kids are fickle snackers and readily switch between Kurkure, Crax, and local extruded chips.", "bargaining_power_of_suppliers": "Low; abundant domestic corn grits, rice flour, and food-grade packaging laminate.", "threat_of_substitutes": "Very high from potato chips, sweet biscuits, and local namkeens.", "competitive_rivalry": "Intense rivalry with PepsiCo Kurkure and regional snack manufacturers."}
    ),
    (
        "Prataap Snacks", "FMCG, Personal Care & Packaged Foods",
        "price-sensitive snackers and families across central, northern, and eastern India",
        "need high-quality potato chips, extruded snacks, and namkeens delivered at affordable entry price points without quality compromises",
        "Yellow Diamond Potato Chips & Chulbule Extruded Snacks", "Value-Priced Packaged Savory Snacks",
        "commands leadership in central India's value snacking space, operating efficient regional plants that minimize logistics costs and maximize consumer grammage",
        [0.64, 0.84, 0.90, 0.82, 0.79, 0.65],
        {"political": "Supports domestic agricultural farmers through large-scale contract farming of processing-grade potatoes in Madhya Pradesh.", "economic": "Ultra-lean manufacturing and localized regional distribution hubs enable competitive pricing against national snacking conglomerates.", "social": "Deep penetration in Tier 2/3/4 towns where Yellow Diamond is a household staple for budget-conscious children and families.", "technological": "Continuous automated potato frying and nitrogen flushing lines in Indore, Guwahati, and Rajkot.", "legal": "FSSAI compliance, legal metrology packaging, and Extended Producer Responsibility (EPR) plastic recovery.", "environmental": "Captive solar installations and advanced effluent treatment recycling water from potato washing."},
        [0.34, 0.65, 0.38, 0.35, 0.78],
        {"threat_of_new_entrants": "Moderate; regional snack makers can launch local brands, but scaling distribution across states requires capital.", "bargaining_power_of_buyers": "High; consumers expect full bags for Rs 5 and switch brands if air-to-chip ratio feels unfair.", "bargaining_power_of_suppliers": "Moderate; potato prices fluctuate with cold storage release cycles and monsoon yields.", "threat_of_substitutes": "High from local street food, biscuits, and namkeen.", "competitive_rivalry": "Fierce with Balaji Wafers, PepsiCo Lay's, and Haldiram's."}
    ),
    (
        "Vadilal Industries", "FMCG, Personal Care & Packaged Foods",
        "vegetarian Indian families and ice cream lovers seeking 100% eggless, rich dairy ice creams and frozen desserts",
        "need guaranteed 100% vegetarian, eggless ice creams, novel kulfis, gourmet tubs, and frozen ready-to-eat vegetables and snacks",
        "Vadilal Ice Creams, Gourmet Tubs & Quick Treat Frozen Foods", "Pure Vegetarian Ice Creams & Frozen Consumer Foods",
        "stands as one of India's oldest and most loved 100% pure vegetarian ice cream brands with over 150 flavors and modern automated plants in Gujarat and UP",
        [0.65, 0.85, 0.92, 0.85, 0.80, 0.68],
        {"political": "Beneficiary of central government cold-chain infrastructure subsidies and export incentives for frozen foods.", "economic": "Strong seasonal summer cash generation complemented by year-round frozen vegetable (green peas, sweet corn) exports to the global diaspora.", "social": "Deep cultural trust among conservative vegetarian households (Jain, Gujarati, Marwari) who strictly demand eggless frozen treats.", "technological": "Continuous extrusion ice cream freezers, robotic cone filling lines, and liquid nitrogen IQF (Individually Quick Frozen) processing.", "legal": "FSSAI ice cream standards (milk fat vs. vegetable oil frozen desserts differentiation) and cold-chain compliance.", "environmental": "Solar-assisted cold storage facilities and eco-friendly hydrocarbon refrigerants with zero ozone-depletion potential."},
        [0.30, 0.58, 0.38, 0.32, 0.72],
        {"threat_of_new_entrants": "Low to moderate; ice cream requires unbroken minus 18 deg C deep-freezer distribution networks which are expensive to build.", "bargaining_power_of_buyers": "Moderate; consumers have multiple ice cream brands to choose from in retail parlors.", "bargaining_power_of_suppliers": "Moderate; whole milk fat, sugar, cocoa, and fruit pulp suppliers.", "threat_of_substitutes": "Moderate from kulfi vendors, soft drinks, and chilled fruit juices.", "competitive_rivalry": "Intense rivalry with Amul, Kwality Wall's (HUL), and Havmor."}
    ),
    (
        "Cremica Food Park (Mrs. Bector's Food Specialities)", "FMCG, Personal Care & Packaged Foods",
        "urban households, premium sandwich makers, and leading global QSR chains (McDonald's, Burger King)",
        "require premium gourmet bread, English oven loaves, specialized condiments, and high-export-quality biscuits",
        "English Oven Bread & Mrs. Bector's Cremica Sauces", "Premium Bakery Bread, Biscuits & Institutional Condiments",
        "rules Delhi-NCR and Mumbai premium bakery shelves with English Oven bread, while acting as the sole bun and sauce supplier to India's top QSR burger chains",
        [0.66, 0.86, 0.92, 0.86, 0.80, 0.68],
        {"political": "Supports National Food Processing Policy and mega food park infrastructure development in Punjab.", "economic": "Dual growth engine: high-margin B2C premium bread (English Oven) and sticky, recession-proof institutional supply contracts with global QSRs.", "social": "English Oven transformed the plain white loaf into artisanal sourdough, multigrain, and sub-rolls for urban sandwich lovers.", "technological": "High-throughput automated baking lines producing 50,000 buns per hour with laser optical crust color and height inspection.", "legal": "Stringent global food safety audits (AIB International, FSSC 22000) mandated by multinational fast-food clients.", "environmental": "Heat recovery systems from baking ovens, eco-friendly paper packaging wraps, and biomass fuel boilers."},
        [0.28, 0.54, 0.40, 0.30, 0.70],
        {"threat_of_new_entrants": "Low for institutional QSR supply due to rigorous multinational supplier audit hurdles; moderate in retail bakery.", "bargaining_power_of_buyers": "Moderate; global QSR chains audit costs, but cannot risk switching to unvetted bun bakers.", "bargaining_power_of_suppliers": "Moderate; high-protein wheat flour, yeast, and food-grade packaging.", "threat_of_substitutes": "Moderate from traditional breakfast options (parathas, idlis).", "competitive_rivalry": "Moderate in premium bread (Modern, Harvest Gold); high in mass biscuits."}
    ),
    (
        "Adani Wilmar", "FMCG, Personal Care & Packaged Foods",
        "millions of Indian kitchens requiring pure, affordable edible cooking oils and packaged kitchen staples",
        "need trustworthy, hygienically refined soybean, mustard, sunflower, and palm edible cooking oils, basmati rice, and besan",
        "Fortune Edible Oils, Fortune Chakki Atta & Fortune Basmati", "Essential Kitchen Staples & Branded Edible Oils",
        "operates India's #1 edible oil brand (Fortune) with over 19% market share, running the largest integrated edible oil refining capacity in the country",
        [0.72, 0.90, 0.96, 0.86, 0.82, 0.72],
        {"political": "Key policy stakeholder in National Mission on Edible Oils - Oil Palm (NMEO-OP) to reduce India's import dependency on crude oil.", "economic": "Generates over Rs 50,000 Cr in revenue; massive port-based refining assets (Mundra) process imported oils with superior freight economics.", "social": "Fortune oil is the foundational cooking medium across 30 million Indian households, trusted for pure color and aroma.", "technological": "World-class continuous de-gumming, bleaching, and deodorizing refining towers; automated high-speed pouch filling at port terminals.", "legal": "FSSAI compliance, AGMARK grade-1 certification, and monitoring of national essential commodities stock limits.", "environmental": "Zero-waste edible oil refining, conversion of soap-stock byproducts into oleochemicals, and solar energy deployment."},
        [0.22, 0.60, 0.45, 0.35, 0.76],
        {"threat_of_new_entrants": "Very low; building port-connected mega-refineries with deep draft pipeline berths requires thousands of crores in capex.", "bargaining_power_of_buyers": "High; edible oil is highly price-sensitive and consumers switch between brands based on 5-rupee discounts.", "bargaining_power_of_suppliers": "Moderate; international palm and soy crude oil prices are determined on global commodity exchanges (Bursa Malaysia, CBOT).", "threat_of_substitutes": "Low; edible cooking oil is a non-substitutable daily nutritional necessity.", "competitive_rivalry": "Intense rivalry with Marico, Emami Agrotech, Patanjali (Ruchi Soya), and Cargill."}
    ),
    (
        "LT Foods", "FMCG, Personal Care & Packaged Foods",
        "gourmet households, biryani lovers, and international consumers across 80+ countries",
        "require long-grain, aromatic, aged Basmati rice that cooks into fluffy, non-sticky, fragrant grains for celebratory biryanis and daily meals",
        "Daawat Basmati Rice & Royal Brand Basmati", "Packaged Aged Fragrant Basmati Rice & Convenience Foods",
        "rules global and domestic premium basmati rice with Daawat and Royal, aging aromatic paddy naturally for up to 2 years in climate-controlled silos",
        [0.68, 0.88, 0.94, 0.85, 0.82, 0.72],
        {"political": "Protects India's unique Himalayan Basmati GI heritage, collaborating with APEDA on basmati minimum export price (MEP) monitoring.", "economic": "Enjoys strong dollar/euro export cash flows; Royal brand is the #1 bestselling basmati rice brand across North America.", "social": "An essential element of Indian festivals, Eid biryanis, and royal dining; represents the pinnacle of Indian agricultural aroma.", "technological": "Buhler optical color sorters, laser grain scanners, and scientific silo aging that cures rice starch for maximum elongation upon boiling.", "legal": "Strict adherence to US FDA and European pesticide residue limits (MRLs) and FSSAI standards.", "environmental": "Promotes Sustainable Rice Platform (SRP) farming practices, cutting water usage by 25% and greenhouse methane emissions in paddy fields."},
        [0.25, 0.55, 0.38, 0.28, 0.70],
        {"threat_of_new_entrants": "Low; building farmer procurement across Punjab/Haryana, large-scale capital-intensive aging silos, and global retail distribution is prohibitive.", "bargaining_power_of_buyers": "Moderate; consumers pay a premium for guaranteed non-sticky aromatic grains from Daawat.", "bargaining_power_of_suppliers": "Moderate; procurement during 60-day autumn harvest in northern mandis requires massive working capital.", "threat_of_substitutes": "Moderate from non-basmati long grain and jasmine rice varieties.", "competitive_rivalry": "Duopoly competition with KRBL (India Gate Basmati Rice)."}
    )
]

for item in sector9_data:
    add_c(*item)

print(f"Sector 9 added: {len(sector9_data)} companies. Total in Part 2A: {len(part2_a)}")

# Save to scratch/part2_a.json
out_path = Path(__file__).parent / "part2_a.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(part2_a, f, indent=2)

print(f"SUCCESS: Saved {len(part2_a)} companies to {out_path}")
