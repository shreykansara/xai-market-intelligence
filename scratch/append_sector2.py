"""
Appends Sectors 2 to 6 (Banking, FinTech, IT Services, SaaS, Pharmaceuticals) to scratch/part1.json
"""
import json
from pathlib import Path

part1_path = Path(__file__).parent / "part1.json"
with open(part1_path, "r", encoding="utf-8") as f:
    comps = json.load(f)

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    comps.append({
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
# SECTOR 2: Banking & Financial Institutions (22 companies)
# ==============================================================================
sector2_data = [
    (
        "HDFC Bank", "Banking & Financial Institutions",
        "salaried urban professionals, affluent wealth clients, and premier corporate treasuries",
        "demand frictionless digital banking, ultra-low turnaround retail loans, and rock-solid institutional balance sheet safety",
        "HDFC Digital 2.0 & Infinia Credit Card", "Premier Private Commercial Banking",
        "provides seamless mobile banking with instant 10-second personal loans, best-in-class reward points, and access to 8,500+ branches nationwide",
        [0.65, 0.88, 0.86, 0.84, 0.78, 0.45],
        {"political": "Maintains high systemic importance as RBI Designated Domestic Systemically Important Bank (D-SIB); aligns with priority sector lending mandates.", "economic": "Directly impacted by RBI Monetary Policy Committee repo rate changes, credit cycle growth, and net interest margin (NIM) spreads.", "social": "Regarded as the gold standard of private banking trust in India, serving 80M+ customers across metro and rural corridors.", "technological": "Invests ₹3,000+ Cr annually in cloud migration, PayZapp 2.0 digital wallet, and AI automated credit underwriting models.", "legal": "Strictly adheres to RBI Basel III capital adequacy norms, stringent KYC/PMLA compliance, and digital security mandates.", "environmental": "Pioneering green infrastructure project financing and paperless digital account opening across all branches."},
        [0.15, 0.65, 0.50, 0.45, 0.82],
        {"threat_of_new_entrants": "Very low; stringent RBI universal banking licensing criteria and massive branch network form an insurmountable moat.", "bargaining_power_of_buyers": "Moderate; affluent clients enjoy competitive loan rates, but high switching friction on salary accounts preserves low-cost CASA deposits.", "bargaining_power_of_suppliers": "Low-to-moderate; diversified retail depositor base ensures minimal reliance on expensive wholesale institutional funds.", "threat_of_substitutes": "Moderate; specialized fintech lenders and wealth apps compete for retail loan and mutual fund distribution share.", "competitive_rivalry": "Intense; fierce competition against ICICI Bank, Axis Bank, and State Bank of India across mortgages and credit cards."}
    ),
    (
        "State Bank of India (SBI)", "Banking & Financial Institutions",
        "pan-Indian mass consumers, agricultural households, and government mega-infrastructure projects",
        "require universal financial access, government DBT welfare subsidy delivery, and massive long-tenure corporate credit",
        "SBI YONO Super-App & Agri Gold Loans", "Public Sector Commercial Banking & Sovereign Credit",
        "delivers unmatched financial presence across 22,000+ physical branches, YONO digital scale serving 60M+ registered users, and sovereign safety backing",
        [0.85, 0.90, 0.92, 0.78, 0.82, 0.50],
        {"political": "Flagship sovereign financial institution executing Union Budget initiatives, PM Jan Dhan Yojana, and national infrastructure financing.", "economic": "Central pillar of Indian economic credit expansion, absorbing government borrowing and channeling liquidity into priority sectors.", "social": "The cornerstone of trust for over 480M account holders, providing banking dignity across the most remote Himalayan and tribal villages.", "technological": "Scales YONO super-app processing over 100M daily UPI transactions, integrating automated KCC farm loan renewals.", "legal": "Complies with stringent statutory liquidity ratios (SLR), cash reserve ratios (CRR), and sovereign public accountability frameworks.", "environmental": "Financing large-scale national solar power parks, metro rail infrastructure, and green hydrogen projects with concessional interest rates."},
        [0.10, 0.60, 0.45, 0.40, 0.80],
        {"threat_of_new_entrants": "Virtually zero; 200+ years of institutional heritage, sovereign ownership, and unmatched 22,000-branch footprint cannot be rivaled.", "bargaining_power_of_buyers": "Moderate-low; mass retail depositors prioritize sovereign safety over slight deposit interest rate differentials.", "bargaining_power_of_suppliers": "Extremely low; immense low-cost CASA deposit base of over ₹45 lakh crore provides unmatched funding self-sufficiency.", "threat_of_substitutes": "Low-to-moderate; post office savings and cooperative banks offer local alternatives, but lack SBI's digital depth.", "competitive_rivalry": "High; competes with large private banks (HDFC, ICICI) in metro corporate credit and high-ARPU credit card markets."}
    ),
    (
        "ICICI Bank", "Banking & Financial Institutions",
        "tech-first retail consumers, emerging entrepreneurs, and multinational enterprises",
        "seek agile API-driven business banking, instant pre-approved consumer credit, and sophisticated foreign exchange services",
        "iMobile Pay & Trade Online Business Platform", "Technologically Agile Universal Banking",
        "pioneers 360-degree instant digital loan approvals, paperless trade remittances, and seamless integration with corporate ERPs via open banking APIs",
        [0.65, 0.86, 0.85, 0.92, 0.76, 0.48],
        {"political": "Designated Domestic Systemically Important Bank (D-SIB); actively supports government digital infrastructure and GIFT City IFSC banking.", "economic": "Delivers superior return on assets (RoA) by balancing high-yielding retail consumer loans with high-grade corporate balance sheet advisory.", "social": "Favored by digitally native Indian millennials and young families seeking intuitive mobile apps and frictionless financial services.", "technological": "Industry leader in open banking APIs with 500+ micro-services connecting fintechs, ERPs, and automated e-mandate systems.", "legal": "Strict compliance with RBI guidelines on cyber resilience, digital lending transparency, and data localization.", "environmental": "Active issuer of green bonds and ESG financing frameworks supporting commercial electric vehicle fleet adoptions."},
        [0.18, 0.70, 0.52, 0.48, 0.85],
        {"threat_of_new_entrants": "Low; strict regulatory capital requirements and established digital moat prevent new challengers from scaling quickly.", "bargaining_power_of_buyers": "Moderate-high; tech-savvy urban customers readily compare personal loan interest rates and credit card cashback benefits.", "bargaining_power_of_suppliers": "Low-to-moderate; robust retail deposit franchise cushions against volatile wholesale money market borrowing rates.", "threat_of_substitutes": "Moderate; neo-banks, NBFCs, and payment apps compete for entry-level consumer financial touchpoints.", "competitive_rivalry": "Fierce head-to-head battle against HDFC Bank and Axis Bank for dominance in retail consumer loans and credit cards."}
    ),
    (
        "Kotak Mahindra Bank", "Banking & Financial Institutions",
        "wealthy business families, mid-sized corporates, and high-yield digital savers",
        "demand disciplined credit underwriting, high interest yields on savings accounts, and personalized private family office wealth management",
        "Kotak 811 & Kotak Private Wealth", "Discipline-First Private Wealth & Digital Banking",
        "combines zero-balance mobile account onboarding via Kotak 811 with bespoke multi-asset wealth management and ultra-conservative asset quality underwriting",
        [0.64, 0.84, 0.82, 0.85, 0.76, 0.45],
        {"political": "Aligns with RBI financial inclusion mandates through zero-balance Kotak 811 video KYC accounts.", "economic": "Maintains industry-leading Net Interest Margins (NIM) and exceptional capital adequacy ratios exceeding 20%, ensuring resilient balance sheets.", "social": "Appeals to affluent business promoters seeking multi-generational estate planning and middle-class savers seeking reliable interest returns.", "technological": "Rebuilding full-stack core banking systems and microservices architecture to comply with heightened RBI digital transaction resilience guidelines.", "legal": "Navigates RBI supervisory regulatory audits on IT resilience, data governance, and promoter shareholding dilution norms.", "environmental": "Implementing sustainable banking practices, digital loan origination reducing physical paperwork, and renewable energy financing."},
        [0.22, 0.68, 0.55, 0.45, 0.82],
        {"threat_of_new_entrants": "Low; obtaining universal banking licenses and building multi-asset private wealth credibility requires decades of pristine reputation.", "bargaining_power_of_buyers": "Moderate; HNIs demand customized investment deals, but appreciate Kotak's conservative risk management.", "bargaining_power_of_suppliers": "Moderate; competitive deposit rates (6%+) needed to attract retail savings deposits from nationalized banks.", "threat_of_substitutes": "Moderate; specialized wealth managers and small finance banks compete for high-yield deposit dollars.", "competitive_rivalry": "Intense; competing against ICICI, HDFC, and boutique wealth management firms for wallet share of India's top 1% wealth."}
    ),
    (
        "Axis Bank", "Banking & Financial Institutions",
        "upwardly mobile corporate executives, SME supply chains, and transaction banking clients",
        "seek premium lifestyle credit cards with luxury travel perks, integrated SME trade finance, and customized merchant cash-management",
        "Magnus & Atlas Travel Credit Cards & Burgundy Banking", "Affluent Lifestyle & Corporate Transaction Banking",
        "delivers unmatched air-mile transfer ratios on luxury travel credit cards, Burgundy priority wealth relationship managers, and deep SME supply chain financing",
        [0.65, 0.85, 0.84, 0.86, 0.75, 0.45],
        {"political": "Works with Ministry of Finance and state governments to manage municipal tax collections and infrastructure debt syndication.", "economic": "Acquisition of Citibank India's consumer business significantly bolstered high-margin credit card and affluent wealth balances.", "social": "Caters to lifestyle-oriented urban consumers who actively maximize airline loyalty points, luxury dining discounts, and premium airport lounge access.", "technological": "Developed Open by Axis Bank app, automated rule-based underwriting algorithms, and WhatsApp commercial banking services.", "legal": "Adheres to RBI regulations on credit card billing practices, fair recovery codes, and co-branded credit card data privacy.", "environmental": "Committed to ₹30,000 Cr in sustainable wholesale financing for clean energy, wastewater treatment, and green building projects."},
        [0.20, 0.72, 0.54, 0.48, 0.84],
        {"threat_of_new_entrants": "Low; massive branch network (5,000+ branches) and deep corporate banking relationships create formidable entry barriers.", "bargaining_power_of_buyers": "High; affluent credit card users actively churn cards if reward redemption milestones or lounge access rules are devalued.", "bargaining_power_of_suppliers": "Low-to-moderate; retail CASA ratio around 42-44% provides stable, cost-effective domestic funding.", "threat_of_substitutes": "Moderate; fintech credit card challengers (CRED, OneCard) compete for urban tech workers' transaction volume.", "competitive_rivalry": "Fierce rivalry against HDFC Bank and ICICI Bank in credit card spend market share and corporate payroll accounts."}
    ),
    (
        "IndusInd Bank", "Banking & Financial Institutions",
        "commercial vehicle operators, diamond traders, and mid-market consumer borrowers",
        "need specialized commercial fleet financing, bullion trade banking, and flexible high-yield consumer checking accounts",
        "IndusInd Pioneer & Commercial Vehicle Finance", "Vehicle Asset Finance & Trade Banking",
        "delivers deep specialized domain expertise in commercial vehicle credit underwriting, high-yield Pioneer wealth accounts, and instant digital personal loans",
        [0.62, 0.84, 0.80, 0.82, 0.74, 0.46],
        {"political": "Aligns with government highway logistics growth and national priority sector microfinance lending programs.", "economic": "Beneficiary of commercial vehicle replacement cycles and booming freight transport activity across national industrial corridors.", "social": "Strong roots in financing independent truck drivers and micro-enterprises, catalyzing self-employment and commercial mobility.", "technological": "IndusMobile 2.0 app with video KYC, automated FASTag toll recharges, and algorithmic fleet financing assessments.", "legal": "Complies with RBI asset classification guidelines, PCR (provision coverage ratio) norms, and trade-based money laundering checks.", "environmental": "Financing electric commercial cargo fleets and supporting clean supply chain transportation logistics."},
        [0.24, 0.70, 0.58, 0.46, 0.80],
        {"threat_of_new_entrants": "Low; domain expertise in truck repossession networks, regional mandi credit, and vehicle salvage value cannot be easily cloned.", "bargaining_power_of_buyers": "Moderate-high; transport fleet owners compare interest rates and loan-to-value (LTV) ratios across NBFCs and private banks.", "bargaining_power_of_suppliers": "Moderate; reliance on higher-cost term deposits compared to the largest private banking giants.", "threat_of_substitutes": "Moderate; commercial vehicle NBFCs (Shriram, Chola) compete directly for transporter business.", "competitive_rivalry": "High; competing against Axis Bank, Kotak, and specialized NBFCs in vehicle loans and SME working capital."}
    ),
    (
        "Federal Bank", "Banking & Financial Institutions",
        "Non-Resident Indian (NRI) diaspora, Kerala remittance corridors, and digital fintech partners",
        "seek seamless low-cost cross-border foreign inward remittances, relationship-driven SME banking, and open API co-branded banking",
        "FedMobile & NRI Diaspora Remittance Suite", "NRI Corridors & Fintech Infrastructure Banking",
        "captures over 20% of India's total inward personal remittances, offering personalized relationship managers and agile banking-as-a-service (BaaS) APIs",
        [0.64, 0.82, 0.86, 0.88, 0.75, 0.44],
        {"political": "Facilitates vital foreign exchange inflows from Gulf Cooperation Council (GCC) countries, supporting India's foreign exchange balance of payments.", "economic": "Direct beneficiary of robust Middle East oil economies driving remittances to Kerala, Tamil Nadu, and Karnataka.", "social": "Deep cultural affinity with Gulf-based Malayali diaspora, serving as trusted family banker for multiple generations.", "technological": "Pioneered Bank-as-a-Service (BaaS) partnerships powering neo-banks like Jupiter and Fi Money with underlying banking rails.", "legal": "Adheres to strict Foreign Exchange Management Act (FEMA) guidelines, cross-border anti-money laundering (AML), and RBI digital regulations.", "environmental": "Financing rooftop solar initiatives and organic spice cultivation across Kerala and coastal Karnataka."},
        [0.25, 0.65, 0.52, 0.42, 0.78],
        {"threat_of_new_entrants": "Moderate-low; long-established Gulf branch representative offices and diaspora customer trust provide deep competitive moats.", "bargaining_power_of_buyers": "Moderate; NRI clients value personalized relationship managers and competitive foreign exchange conversion spreads.", "bargaining_power_of_suppliers": "Low-to-moderate; steady stream of low-cost NRE/NRO diaspora deposits ensures stable funding.", "threat_of_substitutes": "Moderate; fintech cross-border transfer apps (Wise, Western Union) compete for remittance volume.", "competitive_rivalry": "Moderate-high; competes with South Indian Bank, CSB Bank, and SBI for Kerala remittance market share."}
    ),
    (
        "Bandhan Bank", "Banking & Financial Institutions",
        "rural women self-help groups, micro-entrepreneurs, and unbanked East Indian households",
        "need doorstep collateral-free micro-credit, affordable savings accounts, and financial literacy to build small household businesses",
        "Bandhan Doorstep Micro-Banking & Sanchay Savings", "Financial Inclusion & Grassroots Microfinance",
        "provides weekly doorstep center meetings with female credit officers, 99%+ historical collection discipline, and transformation of micro-borrowers into formal bank savers",
        [0.72, 0.80, 0.94, 0.72, 0.76, 0.45],
        {"political": "Flagship success story of RBI universal bank licensing for financial inclusion, aligned with Priority Sector Lending (PSL) objectives.", "economic": "Directly exposed to rural consumption shocks, flood/cyclone climatic events in Eastern India, and grassroots agricultural cash liquidity.", "social": "Empowers over 20M underserved rural women through collateral-free group loans for livestock, weaving, and petty grocery shops.", "technological": "Equipping rural credit officers with biometric handheld micro-ATMs and real-time Aadhaar-enabled payment system (AePS) devices.", "legal": "Subject to strict RBI microfinance regulations on borrower indebtedness caps, household income verification, and ethical recovery codes.", "environmental": "Supports climate-resilient organic agriculture, rural bio-gas financing, and disaster relief micro-insurance packages."},
        [0.26, 0.62, 0.60, 0.38, 0.75],
        {"threat_of_new_entrants": "Moderate-low; building ground-level rural center meetings and human trust across 6,000+ banking units in West Bengal/Assam is difficult.", "bargaining_power_of_buyers": "Low-to-moderate; micro-borrowers have limited access to formal banking credit, though NBFC-MFIs provide options.", "bargaining_power_of_suppliers": "Moderate; ongoing effort to diversify retail deposit base outside Eastern India to reduce geographic concentration.", "threat_of_substitutes": "Moderate; informal local moneylenders and regional rural banks (RRBs) represent alternative credit channels.", "competitive_rivalry": "Moderate; competes with Small Finance Banks (Equitas, Ujjivan) and NBFC-MFIs in semi-urban microfinance markets."}
    ),
    (
        "AU Small Finance Bank", "Banking & Financial Institutions",
        "semi-urban micro-entrepreneurs, self-employed businessmen, and Tier-2/3 vehicle buyers",
        "require fast-turnaround collateral-free business loans, attractive savings deposit rates, and accessible branch banking in emerging towns",
        "AU 0101 Digital Banking & Commercial Wheels Loans", "High-Growth Small Finance & Semi-Urban Banking",
        "delivers up to 7.25% interest on savings accounts, specialized vehicle and small business loans evaluated via cash-flow assessments, and Sunday-open branches",
        [0.68, 0.82, 0.85, 0.86, 0.76, 0.44],
        {"political": "Beneficiary of RBI Small Finance Bank frameworks promoting financial deepening in unbanked and underbanked districts.", "economic": "Thrives on the vibrant entrepreneurial spirit of western and northern Indian trading communities, financing local shops and logistics.", "social": "Brings respectful, customer-first modern banking experiences to semi-urban merchants who were traditionally neglected by large private banks.", "technological": "Built the AU 0101 digital app offering 24/7 video banking, instant digital credit card issuance, and UPI merchant QR codes.", "legal": "Maintains minimum 75% Priority Sector Lending (PSL) compliance and 50% loans under ₹25 lakh as mandated by RBI SFB licensing guidelines.", "environmental": "Promotes electric three-wheeler and commercial transport financing, reducing emissions in Tier-2 Indian cities."},
        [0.28, 0.68, 0.58, 0.44, 0.80],
        {"threat_of_new_entrants": "Moderate; RBI has opened on-tap universal and SFB licensing, but building 1,000+ branches and credit underwriting is capital-intensive.", "bargaining_power_of_buyers": "Moderate-high; customers are attracted by higher deposit interest rates and quick 48-hour loan sanction turnaround.", "bargaining_power_of_suppliers": "Moderate; relies on offering 100-150 bps higher deposit rates than HDFC/SBI to attract retail deposits.", "threat_of_substitutes": "Moderate; traditional private banks, regional NBFCs, and state cooperative banks compete in district headquarters.", "competitive_rivalry": "Intense; competing against other leading SFBs (Equitas, Ujjivan) and regional NBFCs for MSME lending share."}
    ),
    (
        "Bajaj Finance Limited", "Banking & Financial Institutions",
        "consumer electronics buyers, smartphone shoppers, and lifestyle aspirational consumers",
        "seek instant zero-interest No-Cost EMI financing at physical retail checkouts without cumbersome paperwork",
        "Bajaj Finserv EMI Network Card & Insta EMI Card", "Omnichannel Consumer Durable & Lifestyle Financing",
        "provides pre-approved 0% interest EMI credit lines accepted across 150,000+ partner retail stores in 4,000+ towns, with instant 30-second POS checkout",
        [0.65, 0.88, 0.90, 0.94, 0.78, 0.42],
        {"political": "Interacts closely with Ministry of Consumer Affairs and RBI on transparent point-of-sale consumer finance disclosures.", "economic": "Dominant engine of Indian consumer discretionary consumption, driving 70%+ of retail smartphone, TV, and appliance financing.", "social": "Democratized lifestyle upgrades for Indian families, enabling purchase of refrigerators, laptops, and air conditioners via affordable monthly payments.", "technological": "Proprietary algorithmic underwriting evaluating 100M+ customer bureau and behavioral parameters in under 10 seconds at store counters.", "legal": "Adheres to RBI digital lending guidelines, fair practices code on recovery, and statutory loan-to-value limits.", "environmental": "Drives paperless digital e-sign loans, eliminating millions of physical paper agreement forms across India's retail landscape."},
        [0.22, 0.65, 0.52, 0.45, 0.85],
        {"threat_of_new_entrants": "Low; exclusive point-of-sale merchant store integration across 150,000 retail shops and deep manufacturer brand subsidies create massive moats.", "bargaining_power_of_buyers": "Moderate; consumers choose Bajaj Finserv due to widespread OEM tie-ups (Samsung, Apple, LG) offering zero-cost EMIs.", "bargaining_power_of_suppliers": "Low; consumer electronic brands subsidize subvention interest to Bajaj to boost their own retail sales velocity.", "threat_of_substitutes": "Moderate-high; credit cards and bank debit card EMIs compete, but have far lower physical store merchant penetration.", "competitive_rivalry": "High; competing against bank credit cards, Home Credit, and emerging digital BNPL platforms in urban centers."}
    ),
    (
        "Shriram Finance", "Banking & Financial Institutions",
        "pre-owned truck drivers, rural transport operators, and unorganized small business owners",
        "need collateral-free credit for 5-10 year old used commercial vehicles and tractor machinery ignored by traditional banks",
        "Pre-Owned Commercial Vehicle Loans & MSME Credit", "Used Asset Financing & Transport Ecosystem NBFC",
        "features deep relationship-based credit assessment of pre-owned commercial trucks, pan-India presence across 3,000+ branches, and flexible cash recovery",
        [0.66, 0.86, 0.88, 0.72, 0.74, 0.50],
        {"political": "Supports National Logistics Policy and rural transport connectivity by financing the lifeblood of India's unorganized trucking fleet.", "economic": "Direct beneficiary of infrastructure development and agricultural produce transport, financing pre-owned vehicles that move food and industrial goods.", "social": "Transforms truck drivers into asset-owning transport entrepreneurs, creating generational wealth for semi-literate rural families.", "technological": "Digital vehicle valuation algorithms, automated mobile collections, and FASTag toll integrations for transport fleets.", "legal": "Complies with RBI scale-based regulation for upper-layer NBFCs, asset classification norms, and CMVR commercial vehicle laws.", "environmental": "Participating in national commercial vehicle scrappage programs and encouraging fleet replacement with newer BS-VI used vehicles."},
        [0.20, 0.65, 0.56, 0.38, 0.80],
        {"threat_of_new_entrants": "Low; physically inspecting and valuing 10-year-old used trucks and managing localized recovery requires unique grassroots expertise.", "bargaining_power_of_buyers": "Low-to-moderate; used truck buyers have virtually zero access to prime private bank loans and rely on Shriram's flexible terms.", "bargaining_power_of_suppliers": "Moderate; diversified borrowing mix across domestic retail fixed deposits, bank credit lines, and offshore dollar bonds.", "threat_of_substitutes": "Low; traditional commercial banks avoid pre-owned commercial vehicle financing due to high perceived asset risk.", "competitive_rivalry": "Moderate-high; competes primarily against Cholamandalam and Sundaram Finance in transport corridors."}
    ),
    (
        "Muthoot Finance", "Banking & Financial Institutions",
        "cash-constrained micro-business owners, small farmers, and individuals facing medical/family emergencies",
        "seek immediate same-day liquidity against idle household gold jewelry without income tax returns or lengthy credit checks",
        "Muthoot Gold Loans & Doorstep Gold Banking", "Gold-Backed Retail & MSME Credit",
        "provides instant 15-minute cash loan disbursal against gold ornaments with maximum loan-to-value (LTV), secure branch vaults, and flexible interest servicing",
        [0.62, 0.85, 0.92, 0.75, 0.76, 0.40],
        {"political": "Regulated under RBI gold loan directives; benefits from India's cultural accumulation of over 25,000 tonnes of privately held gold.", "economic": "Provides crucial counter-cyclical emergency liquidity during economic distress, medical emergencies, or agricultural sowing seasons.", "social": "Destigmatized gold loans across India, transforming emotional heirloom jewelry into an active tool for productive business capital.", "technological": "Web and mobile app loan top-ups, online interest payment via UPI, and automated gold karat testing technology in branches.", "legal": "Strictly adheres to RBI 75% loan-to-value (LTV) cap, secure biometric vault protocols, and transparent auction guidelines for defaulted collateral.", "environmental": "Low-carbon physical branch operations with minimal paper consumption and energy-efficient vault security systems."},
        [0.24, 0.60, 0.48, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; 4,800+ secure physical branch networks with high-security armed vaults and established brand trust create high barriers.", "bargaining_power_of_buyers": "Moderate; borrowers value speed, privacy, and absolute security of their gold ornaments over minor interest rate differences.", "bargaining_power_of_suppliers": "Low; funded via retail non-convertible debentures (NCDs), bank term loans, and commercial paper.", "threat_of_substitutes": "Moderate; bank gold loans (SBI) and informal pawn brokers compete, but lack Muthoot's 15-minute turnaround.", "competitive_rivalry": "High; competing fiercely with Manappuram Finance, Shriram City, and public sector bank gold loan desks."}
    ),
    (
        "Manappuram Finance", "Banking & Financial Institutions",
        "unbanked daily wage earners, small traders, and rural women seeking micro-credit",
        "require rapid short-tenure gold loans with flexible monthly interest options and micro-housing finance",
        "Online Gold Loan (OGL) & Asirvad Microfinance", "Gold Loans & Diversified Rural Microfinance",
        "pioneers 24/7 Online Gold Loans with digital fund transfer to bank accounts, doorstep gold evaluation, and financial inclusion micro-credit",
        [0.62, 0.84, 0.90, 0.78, 0.75, 0.40],
        {"political": "Operates under RBI guidelines for non-banking financial companies; supports rural livelihood financing under financial inclusion goals.", "economic": "Benefits from high domestic gold prices which automatically expand borrowing headroom for existing gold loan customers.", "social": "Helps marginal borrowers avoid predatory local moneylenders charging 36-60% annual interest by offering formal financial credit.", "technological": "Industry-first 24/7 Online Gold Loan platform allowing customers to draw and repay loan tranches digitally against pledged collateral.", "legal": "Meets regulatory statutory capital ratios, RBI fair practice codes on gold auctions, and state-level microfinance regulations.", "environmental": "Focuses on paperless loan processing and digital repayments via UPI, reducing branch environmental footprint."},
        [0.25, 0.62, 0.50, 0.44, 0.82],
        {"threat_of_new_entrants": "Moderate-low; requires establishing thousands of high-security physical branches with dedicated gold appraisers and armed security.", "bargaining_power_of_buyers": "Moderate; customers compare loan-to-value ratios and interest rate tiers across competing gold loan branches.", "bargaining_power_of_suppliers": "Moderate; maintains diversified institutional bank credit lines and retail public deposit issuances.", "threat_of_substitutes": "Moderate; gold loan desks at PSU banks offer lower rates but require more documentation and longer branch wait times.", "competitive_rivalry": "Intense; competes head-to-head with Muthoot Finance across southern and northern Indian branch clusters."}
    ),
    (
        "Cholamandalam Investment and Finance (Murugappa Group)", "Banking & Financial Institutions",
        "light commercial vehicle buyers, tractors operators, and small industrial manufacturers",
        "demand reliable vehicle finance, home equity loans, and industrial machinery equipment financing from an established conglomerate",
        "Chola Vehicle Finance & Loan Against Property", "Asset-Backed Commercial Finance & MSME Mortgages",
        "delivers disciplined vehicle asset financing with deep field relationship management, flexible repayment schedules, and Murugappa Group trust",
        [0.64, 0.84, 0.82, 0.75, 0.74, 0.48],
        {"political": "Direct contributor to government national transport infrastructure goals, financing first-time commercial vehicle owners.", "economic": "Benefits from commercial vehicle sales momentum, rural tractor demand, and booming real estate asset-backed MSME loan appetite.", "social": "Deep roots in semi-urban India, guiding small transport operators and first-generation entrepreneurs toward commercial independence.", "technological": "Digital tablet-based loan origination for field sales teams, automated credit scoring models, and integration with credit bureaus.", "legal": "Adheres to RBI upper-layer scale-based NBFC prudential regulations, SARFAESI recovery procedures, and vehicle registration mandates.", "environmental": "Financing clean fuel commercial vehicles (CNG/EV) and supporting green construction machinery modernization."},
        [0.22, 0.68, 0.54, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; 1,200+ branches and 25+ years of vehicle underwriting data across multiple Indian economic cycles create strong moats.", "bargaining_power_of_buyers": "Moderate; commercial borrowers choose Chola for prompt vehicle delivery approvals and sensible restructuring during monsoon lulls.", "bargaining_power_of_suppliers": "Low-to-moderate; backing of the Murugappa Group ensures top-tier credit ratings (AA+) and low borrowing costs.", "threat_of_substitutes": "Moderate; private banks and specialized NBFCs (Shriram, Mahindra Finance) compete across similar asset classes.", "competitive_rivalry": "High; competing with Shriram Finance, Mahindra Finance, and HDFC Bank across vehicle financing corridors."}
    ),
    (
        "Sundaram Finance", "Banking & Financial Institutions",
        "conservative transport operators, fleet logistics firms, and premium fixed deposit savers",
        "seek dependable commercial vehicle loans with zero hidden charges, high integrity customer service, and absolute safety of term deposits",
        "Sundaram Commercial Vehicle Loans & Trust Deposits", "Conservative Commercial Vehicle & Equipment Finance",
        "renowned for its pristine 70-year reputation of 'Sundaram Trust', zero hidden fees, relationship-first loan collection, and AAA-rated fixed deposits",
        [0.62, 0.82, 0.84, 0.70, 0.75, 0.46],
        {"political": "Maintains harmonious regulatory relations with RBI, recognized for conservative corporate governance and ethical lending practices.", "economic": "Operates with conservative loan-to-value (LTV) ratios, deliberately sacrificing hyper-growth during booms to preserve balance sheet strength.", "social": "Generations of South Indian transport families and senior citizen depositors hold unshakeable faith in the Sundaram Finance name.", "technological": "Modernized customer portal, automated digital loan servicing, and real-time integration with national commercial transport databases.", "legal": "Flawless compliance track record with RBI prudential guidelines, capital adequacy exceeding regulatory thresholds, and zero regulatory penalties.", "environmental": "Financing modern commercial vehicle fleets meeting BS-VI standards, reducing particulate matter pollution along freight corridors."},
        [0.24, 0.65, 0.50, 0.40, 0.78],
        {"threat_of_new_entrants": "Low; the trust equity and generational customer loyalty built over seven decades cannot be replicated by venture-funded startups.", "bargaining_power_of_buyers": "Moderate; fleet operators appreciate that Sundaram stands by them during cyclical downturns without predatory asset seizures.", "bargaining_power_of_suppliers": "Low; retail fixed depositors enthusiastically queue up for Sundaram deposits even at slightly lower interest rates due to pristine safety.", "threat_of_substitutes": "Moderate; aggressive private banks and NBFCs offer higher LTV financing, but attract higher-risk credit profiles.", "competitive_rivalry": "Moderate; operates in its own high-quality credit niche, avoiding aggressive price wars with aggressive rivals."}
    ),
    (
        "IDFC FIRST Bank", "Banking & Financial Institutions",
        "customer-centric retail banking consumers, digital credit shoppers, and modern MSMEs",
        "demand transparent fee-free savings banking, monthly interest credits, and consumer-first credit cards with zero dynamic forex markups",
        "FIRST WOW Credit Card & Monthly Interest Savings", "Customer-Centric Transparent Retail Banking",
        "provides monthly interest compounding on savings accounts, zero fees on 28+ essential banking services, and customer-first transparent credit terms",
        [0.65, 0.82, 0.88, 0.90, 0.76, 0.45],
        {"political": "Supports financial deepening through rural microfinance transformation and digital-first priority sector credit expansion.", "economic": "Successfully transitioned from wholesale infrastructure lender to a diversified, high-growth retail franchise with surging CASA deposits.", "social": "Advocates ethical banking with 'near-zero fees' on everyday transactions, winning massive customer goodwill among young urban professionals.", "technological": "Best-in-class mobile banking app with clean intuitive UX, instant digital credit card issuance, and real-time expense tracking.", "legal": "Adheres to RBI Basel III capital requirements, digital lending guidelines, and customer protection codes on fair fees.", "environmental": "Financing clean energy projects and operating automated paperless branches with smart energy conservation."},
        [0.25, 0.72, 0.58, 0.46, 0.82],
        {"threat_of_new_entrants": "Low; significant regulatory barriers to securing universal bank licenses and building retail branch distribution.", "bargaining_power_of_buyers": "High; urban retail customers readily switch deposits to whoever offers best digital UX and attractive monthly interest payouts.", "bargaining_power_of_suppliers": "Moderate; building retail deposit base rapidly requires offering higher interest tiers (up to 7%) on savings accounts.", "threat_of_substitutes": "Moderate; top private banks (HDFC, ICICI) and fintech apps compete for the same tech-savvy demographic.", "competitive_rivalry": "High; competing aggressively against Kotak Mahindra, IndusInd, and Axis Bank for retail consumer wallet share."}
    ),
    (
        "Punjab National Bank (PNB)", "Banking & Financial Institutions",
        "northern Indian agricultural producers, MSME industrial clusters, and public sector institutions",
        "need large-scale credit facilities, Kisan Credit Cards for harvest cycles, and extensive branch reach across semi-urban North India",
        "PNB One Mobile App & Krishi Sarathi Agri Credit", "Public Sector Agricultural & Industrial Commercial Banking",
        "provides deep regional presence across 10,000+ branches, specialized agricultural and MSME credit schemes, and sovereign security backing",
        [0.80, 0.86, 0.88, 0.74, 0.78, 0.48],
        {"political": "Key public sector bank executing central government welfare schemes, agricultural loan waivers, and MSME credit guarantee funds.", "economic": "Directly exposed to Northern India's agricultural wheat/rice harvest cycles, industrial manufacturing in Punjab/Haryana, and real estate credit.", "social": "Deep historical connection as one of India's oldest national banks, founded during the Swadeshi movement by Lala Lajpat Rai.", "technological": "Modernized digital infrastructure with PNB One mobile app, digital KCC crop loan renewals, and automated loan processing centers.", "legal": "Operates under strict vigilance of Central Vigilance Commission (CVC), Comptroller and Auditor General (CAG), and RBI banking supervision.", "environmental": "Financing agricultural solar pump installations under PM-KUSUM scheme and promoting green industrial boiler retrofits."},
        [0.12, 0.62, 0.48, 0.42, 0.80],
        {"threat_of_new_entrants": "Extremely low; massive 10,000+ branch footprint across northern and central India is impossible to replicate.", "bargaining_power_of_buyers": "Moderate-low; agrarian communities and government departments maintain long-standing institutional deposit relationships.", "bargaining_power_of_suppliers": "Low; vast retail deposit base of over ₹13 lakh crore provides inexpensive, sticky domestic funding.", "threat_of_substitutes": "Moderate; regional rural banks (RRBs) and cooperative banks compete locally for farmer credit.", "competitive_rivalry": "Moderate-high; competes with State Bank of India, Bank of Baroda, and private banks in industrial cities."}
    ),
    (
        "Bank of Baroda", "Banking & Financial Institutions",
        "international trade businesses, overseas Indian diaspora, and modern retail borrowers",
        "require global cross-border trade finance, integrated digital banking, and competitive home loan interest rates",
        "bob World & Baroda Global Trade Finance", "Global Trade Finance & Universal Public Sector Banking",
        "features a strong international network across 17 countries, competitive home loan interest rates linked to repo rates, and bob World digital scale",
        [0.78, 0.85, 0.86, 0.80, 0.78, 0.48],
        {"political": "Premier public sector bank with strategic overseas branches in Dubai, London, and Singapore facilitating Indian international trade.", "economic": "Successfully integrated Dena Bank and Vijaya Bank mergers, creating an efficient high-yielding public sector banking powerhouse.", "social": "Trusted by millions of retail families and trading communities across Gujarat, Maharashtra, and international diaspora corridors.", "technological": "Upgraded digital architecture, implementing enterprise risk management, advanced fraud detection systems, and automated retail loan sanctioning.", "legal": "Subject to RBI regulatory guidelines, global financial authority compliances in overseas territories, and domestic consumer codes.", "environmental": "Active participant in financing renewable energy projects, electric commercial buses, and climate-resilient water infrastructure."},
        [0.15, 0.65, 0.50, 0.42, 0.82],
        {"threat_of_new_entrants": "Very low; 8,200+ branches and international trade banking presence create insurmountable barriers to entry.", "bargaining_power_of_buyers": "Moderate; retail home loan borrowers benefit from competitive repo-linked benchmark lending rates.", "bargaining_power_of_suppliers": "Low; massive CASA deposit base ensures continuous access to low-cost retail funding.", "threat_of_substitutes": "Moderate; private sector banks (ICICI, Axis) compete aggressively for export-import trade finance.", "competitive_rivalry": "High; competing directly against SBI, Punjab National Bank, and major private banks in retail mortgages."}
    ),
    (
        "Canara Bank", "Banking & Financial Institutions",
        "South Indian educational loan seekers, SME industrialists, and agricultural communities",
        "need accessible educational credit for professional degrees, affordable working capital for manufacturing SMEs, and secure branch banking",
        "Canara ai1 Super-App & Vidya Sagarkrupa Loans", "Education & Industrial SME Commercial Banking",
        "leads India in educational loan disbursements, provides tailored working capital credit for precision engineering clusters, and operates 9,600+ branches",
        [0.78, 0.84, 0.88, 0.75, 0.76, 0.48],
        {"political": "Executes national educational credit subsidy schemes (CSIS) and government credit guarantee schemes for small businesses (CGTMSE).", "economic": "Deeply linked to South Indian SME industrial hubs in Peenya, Coimbatore, and Hyderabad, financing precision components and textile units.", "social": "Known as the champion of higher education financing in India, enabling millions of students from modest backgrounds to attend engineering/medical colleges.", "technological": "Deployed Canara ai1 mobile app consolidating 250+ features, automated loan underwriting portals, and digital trade processing.", "legal": "Adheres to statutory RBI asset quality guidelines, prompt corrective action (PCA) prevention frameworks, and public banking regulations.", "environmental": "Financing green industrial effluent treatment plants and solar rooftop installations for SME textile factories."},
        [0.15, 0.62, 0.48, 0.40, 0.80],
        {"threat_of_new_entrants": "Very low; historic 118-year institutional presence and 9,600+ branch network across India provide unshakeable moats.", "bargaining_power_of_buyers": "Moderate-low; students and local SME industrialists rely on Canara Bank's supportive lending terms.", "bargaining_power_of_suppliers": "Low; vast retail deposit base of over ₹12 lakh crore ensures low cost of funds.", "threat_of_substitutes": "Moderate; private banks and small finance banks compete for urban retail depositors.", "competitive_rivalry": "Moderate-high; competes against Union Bank of India, Indian Bank, and SBI in southern banking circles."}
    ),
    (
        "Union Bank of India", "Banking & Financial Institutions",
        "large infrastructure EPC developers, agricultural exporters, and mid-market enterprises",
        "require syndicated infrastructure project loans, export credit facilities, and wide branch transaction accessibility",
        "Vyom Digital App & Union Infra Credit", "Infrastructure Syndication & Commercial Public Banking",
        "delivers extensive corporate debt syndication capabilities, seamless export bill discounting, and 8,500+ physical branches across India",
        [0.78, 0.85, 0.85, 0.75, 0.78, 0.48],
        {"political": "Active financier of National Highway Authority of India (NHAI) road contracts and state irrigation infrastructure under PMKSY.", "economic": "Successfully capitalized on the corporate credit recovery cycle, reducing non-performing assets through aggressive bad-debt recoveries.", "social": "Historic public bank serving commercial centers across Maharashtra, Gujarat, and South India following merger with Andhra Bank and Corporation Bank.", "technological": "Vyom super-app delivering digitized personal loans, automated MSME loan approvals up to ₹50 lakh, and online trade documentation.", "legal": "Strict adherence to Insolvency and Bankruptcy Code (IBC) proceedings in NCLT, RBI prudential norms, and public vigilance.", "environmental": "Dedicated lending window for green energy EPC projects, wind power farms, and municipal solid waste processing complexes."},
        [0.16, 0.65, 0.50, 0.42, 0.80],
        {"threat_of_new_entrants": "Very low; multi-thousand branch network, extensive corporate syndication desks, and sovereign backing prevent new entrants.", "bargaining_power_of_buyers": "Moderate; corporate borrowers negotiate keen interest spreads on consortium project finance.", "bargaining_power_of_suppliers": "Low; domestic low-cost CASA deposit foundation supports long-term infrastructure lending.", "threat_of_substitutes": "Moderate; private debt funds and infrastructure NBFCs (PFC, REC) compete in wholesale project finance.", "competitive_rivalry": "Moderate-high; competing against Bank of Baroda, PNB, and Canara Bank for consortium infrastructure mandates."}
    ),
    (
        "Equitas Small Finance Bank", "Banking & Financial Institutions",
        "unorganized self-employed micro-entrepreneurs, small school operators, and informal sector borrowers",
        "need formal bank credit evaluated without formal audited tax returns, affordable small business mortgages, and inclusive banking",
        "Self-Employed Small Business Loans & Eva Savings", "Inclusive Micro-Mortgages & Small Business Finance",
        "features specialized cash-flow based underwriting for informal micro-businesses, customized Eva accounts for women entrepreneurs, and high-interest savings",
        [0.68, 0.82, 0.90, 0.80, 0.75, 0.42],
        {"political": "Supports national financial inclusion goals and Priority Sector Lending (PSL) requirements set by the Reserve Bank of India.", "economic": "Catalyzes economic growth in informal urban and semi-urban clusters, financing neighborhood grocery stores, pharmacies, and small schools.", "social": "Brings unbanked street vendors and informal transport operators into the formal banking system with dignity and transparency.", "technological": "Digital tablet-based assisted onboarding, automated credit assessment algorithms, and WhatsApp micro-banking services.", "legal": "Meets RBI regulations requiring 75% of total loans to qualify under Priority Sector Lending and maintaining strict capital adequacy.", "environmental": "Financing electric three-wheelers, small commercial EV pickups, and rooftop solar for small retail storefronts."},
        [0.28, 0.65, 0.58, 0.44, 0.78],
        {"threat_of_new_entrants": "Moderate-low; field-based informal credit assessment and local verification across 900+ banking outlets require deep institutional capability.", "bargaining_power_of_buyers": "Moderate; self-employed borrowers value loan approval certainty and cash-flow understanding over minor interest differences.", "bargaining_power_of_suppliers": "Moderate; offers higher deposit interest rates (up to 7.5%) to attract retail deposits from traditional banks.", "threat_of_substitutes": "Moderate; local moneylenders, chit funds, and competing SFBs offer informal credit alternatives.", "competitive_rivalry": "Moderate-high; competes directly with AU Small Finance Bank and Ujjivan Small Finance Bank in semi-urban centers."}
    ),
    (
        "Ujjivan Small Finance Bank", "Banking & Financial Institutions",
        "aspiring microfinance borrowers transitioning to formal enterprise, affordable housing buyers, and senior citizens",
        "seek formal home construction loans under ₹20 lakh, respectful senior citizen banking with high deposit yields, and seamless branch digital services",
        "Ujjivan Micro-Mortgages & Maxima Savings", "Affordable Housing & Mass Market Small Finance",
        "provides affordable housing loans without complex ITR documentation, high-yield senior citizen fixed deposits (up to 8.25%), and doorstep micro-banking",
        [0.68, 0.80, 0.92, 0.82, 0.75, 0.42],
        {"political": "Active participant in Pradhan Mantri Awas Yojana (PMAY) credit-linked subsidy scheme for affordable housing in Tier-2/3 cities.", "economic": "Empowers low-income informal households to build pucca brick homes and expand micro-enterprises with affordable long-term credit.", "social": "Pioneered human-centric mass banking, treating blue-collar workers and elderly depositors with exemplary respect and patience.", "technological": "Voice, visual, and vernacular mobile app designed for neo-literate users, biometric AePS authentication, and automated phone banking.", "legal": "Adheres to strict RBI micro-lending caps, consumer grievance redressal frameworks, and micro-mortgage security perfection.", "environmental": "Promotes eco-friendly affordable housing construction techniques and financing for sanitary toilet installations."},
        [0.28, 0.65, 0.58, 0.44, 0.78],
        {"threat_of_new_entrants": "Moderate-low; specialized micro-mortgage title checking and informal income evaluation create significant operational barriers.", "bargaining_power_of_buyers": "Moderate; affordable housing borrowers value flexible 15-20 year repayment terms and prompt loan disbursals.", "bargaining_power_of_suppliers": "Moderate; attracts sticky retail deposits by offering top-tier senior citizen deposit rates.", "threat_of_substitutes": "Moderate; housing finance companies (Aavas, Home First) and SFBs compete in the affordable housing niche.", "competitive_rivalry": "Moderate-high; competes with Equitas SFB, Aavas Financiers, and regional affordable housing lenders."}
    )
]

for item in sector2_data:
    add_c(*item)

print(f"Sector 2 added: {len(sector2_data)} companies. Total: {len(comps)}")

with open(part1_path, "w", encoding="utf-8") as f:
    json.dump(comps, f, indent=2)
print("Updated part1.json successfully.")
