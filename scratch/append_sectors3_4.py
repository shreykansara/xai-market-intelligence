"""
Appends Sector 3 (FinTech, Payments & InsurTech - 23 companies) and
Sector 4 (IT Services & Tech Consulting - 22 companies) to scratch/part1.json
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
# SECTOR 3: FinTech, Payments & InsurTech (23 companies)
# ==============================================================================
sector3_data = [
    (
        "Zerodha Broking", "FinTech, Payments & InsurTech",
        "active retail stock traders, long-term equity investors, and DIY personal finance managers",
        "demand zero-brokerage long-term investing, blazing-fast trade execution, and transparent flat ₹20 F&O pricing",
        "Kite Trading Platform & Console Analytics", "Discount Broking & Wealth Technology",
        "delivers zero brokerage on equity delivery investments, ultra-reliable sub-millisecond Kite execution, and comprehensive tax P&L reporting",
        [0.60, 0.85, 0.92, 0.94, 0.82, 0.35],
        {"political": "Adheres strictly to SEBI capital market regulations, upstream client fund segregation rules, and investor education guidelines.", "economic": "Directly exposed to equity market trading volumes, retail participation cycles, and interest income earned on client float balances.", "social": "Pioneered retail equity investing revolution in India, educating millions of young Indians through Varsity financial literacy modules.", "technological": "Engineered lightweight in-house Kite trading architecture capable of processing billions of financial requests daily with zero venture capital backing.", "legal": "Complies with stringent SEBI circulars on algorithmic trading, derivatives position limits, and National Stock Exchange (NSE) surveillance.", "environmental": "Operates 100% paperless digital onboarding, reducing physical document handling and carbon footprint across capital markets."},
        [0.32, 0.70, 0.55, 0.48, 0.84],
        {"threat_of_new_entrants": "Moderate-low; high customer trust, massive ₹4 lakh crore client assets under custody, and SEBI compliance moats deter new startups.", "bargaining_power_of_buyers": "Moderate; active traders demand rock-solid server uptime during volatile market opens and easily switch if glitches occur.", "bargaining_power_of_suppliers": "Moderate; dependent on stock exchanges (NSE, BSE) for transaction connectivity and clearing corporation depository fees (CDSL).", "threat_of_substitutes": "Moderate; competing discount brokers (Groww, Angel One) and bank brokers (ICICI Direct, HDFC Sky) offer similar pricing.", "competitive_rivalry": "Intense; fierce market share battle against Groww, Angel One, and Upstox for active NSE retail trading accounts."}
    ),
    (
        "Groww (Billionbrains Garage)", "FinTech, Payments & InsurTech",
        "first-time millennial and Gen-Z investors, mutual fund SIP savers, and mobile-first wealth accumulators",
        "seek intuitive, jargon-free investing in direct mutual funds, US equities, and Indian stocks via a sleek mobile app",
        "Groww Super-App & Direct Mutual Fund SIPs", "Mobile-First Consumer Investing & Wealth Management",
        "provides zero-commission direct mutual fund investing, paperless 5-minute digital onboarding, and clean educational charts for beginners",
        [0.62, 0.86, 0.94, 0.95, 0.80, 0.35],
        {"political": "Operates under SEBI investment adviser, stock broker, and depository participant regulatory oversight.", "economic": "Captures the massive financialization of Indian household savings, channeling monthly SIP inflows from Tier-2/3 cities into capital markets.", "social": "Demystified investing for India's youth, transforming conservative bank fixed deposit savers into disciplined systematic equity investors.", "technological": "Clean native mobile app architecture with microservices, instant UPI AutoPay mandate integrations, and real-time market data feeds.", "legal": "Complies with SEBI mutual fund distributor codes, digital KYC verification, and Association of Mutual Funds in India (AMFI) codes.", "environmental": "100% digital investment lifecycle eliminating paper application forms, cheques, and physical statement mailers."},
        [0.35, 0.72, 0.58, 0.50, 0.86],
        {"threat_of_new_entrants": "Moderate; building a slick mobile frontend is achievable, but scaling to 10M+ active transacting users requires massive trust.", "bargaining_power_of_buyers": "High; Gen Z users have zero emotional loyalty and readily migrate to platforms offering better UI, zero fees, or instant cashouts.", "bargaining_power_of_suppliers": "Moderate; reliant on asset management companies (AMCs) and depository participants for backend trade settlement.", "threat_of_substitutes": "High; Zerodha, Paytm Money, Angel One, and traditional banking apps offer identical stock and mutual fund access.", "competitive_rivalry": "Fierce; leading India in active retail client count, engaged in relentless product feature expansion into credit, payments, and FDs."}
    ),
    (
        "Razorpay Software", "FinTech, Payments & InsurTech",
        "e-commerce merchants, internet startups, and enterprise billing departments",
        "need frictionless checkout payment gateway integration with high transaction success rates and automated developer APIs",
        "Razorpay Payment Gateway & RazorpayX Payroll", "Full-Stack Financial Infrastructure & Neobanking APIs",
        "features 100+ payment methods (UPI, cards, net banking, BNPL), intelligent dynamic routing boosting checkout conversion by 20%, and automated vendor payouts",
        [0.68, 0.88, 0.90, 0.96, 0.82, 0.36],
        {"political": "Secured RBI Payment Aggregator (PA) license; actively collaborates with NPCI on novel UPI Autopay and international payment corridors.", "economic": "Powers online checkouts for over 10M Indian businesses, capturing transaction fees on India's booming $100B+ e-commerce market.", "social": "The backbone of India's startup ecosystem, enabling small entrepreneurs to accept instant digital payments within hours of launching.", "technological": "Industry-standard developer documentation, pre-built SDKs for mobile and web platforms, AI Magic Checkout with auto-filled addresses.", "legal": "Meets strict PCI-DSS Level 1 payment security compliance, RBI tokenization guidelines, and DPDP customer transaction data protections.", "environmental": "Drives digital transaction adoption, eliminating millions of tons of paper billing invoices and carbon emissions from cash logistics."},
        [0.30, 0.68, 0.60, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; strict RBI payment aggregator licensing barriers and massive enterprise merchant integration moats protect leadership.", "bargaining_power_of_buyers": "Moderate-high; large e-commerce enterprises (Zomato, Swiggy) negotiate aggressive basis-point transaction fee discounts.", "bargaining_power_of_suppliers": "Moderate-high; reliant on card networks (Visa, Mastercard, RuPay) and major acquiring banks (HDFC, Axis) for payment clearing.", "threat_of_substitutes": "Moderate; Cashfree, PayU India, and CC Avenue offer competing merchant payment gateway solutions.", "competitive_rivalry": "High; continuous innovation in checkout speeds, fraud prevention, and corporate banking suites against Cashfree and PayU."}
    ),
    (
        "PhonePe Private Limited (Walmart Group)", "FinTech, Payments & InsurTech",
        "pan-Indian smartphone users, offline kirana merchants, and digital bill payers",
        "seek instant zero-failure peer-to-peer UPI payments, QR-code merchant billing, and one-tap utility bill recharges",
        "PhonePe Consumer App & Merchant SmartSpeaker", "National Payments Super-App & Merchant Acquiring Rails",
        "commands over 48% market share in UPI transaction volume, offers instant audio payment confirmations via smart speakers across 35M+ merchants",
        [0.72, 0.88, 0.95, 0.96, 0.80, 0.36],
        {"political": "Engages closely with National Payments Corporation of India (NPCI) on market share caps, UPI credit line linking, and digital public infrastructure.", "economic": "Drives economic velocity across India, facilitating over 6 billion monthly transactions and expanding into high-margin lending and insurance.", "social": "Everyday utility app used by over 500M registered Indians across languages, becoming synonymous with the digital cash transition.", "technological": "High-throughput real-time distributed backend processing 200M+ peak daily transactions with near-zero latency; IoT soundbox design.", "legal": "Adheres to RBI regulations on prepaid payment instruments (PPI), payment aggregator mandates, and insurance broker compliances.", "environmental": "Virtually eliminated cash dependency in retail commerce, dramatically reducing physical currency printing and coin transport logistics."},
        [0.22, 0.62, 0.65, 0.48, 0.88],
        {"threat_of_new_entrants": "Very low; establishing 35M+ physical merchant QR network and processing half of India's UPI volume creates an unassailable moat.", "bargaining_power_of_buyers": "Low-to-moderate; consumers love PhonePe's zero-failure rate, though switching to Google Pay or Paytm is technically costless.", "bargaining_power_of_suppliers": "High; dependent on NPCI UPI switch stability and partner bank core systems (Yes Bank, ICICI) for transaction routing.", "threat_of_substitutes": "High; Google Pay and Paytm provide identical UPI functionality on identical interoperable QR codes.", "competitive_rivalry": "Fierce duopoly battle against Google Pay for UPI transaction leadership, and against Paytm for merchant soundbox dominance."}
    ),
    (
        "One97 Communications (Paytm)", "FinTech, Payments & InsurTech",
        "neighborhood retail merchants, daily commuter transit users, and micro-ticket borrowers",
        "need instant audio payment verification, merchant working capital loans, and integrated movie/travel bookings",
        "Paytm Soundbox & Merchant QR Ecosystem", "Merchant Commerce, Soundbox & Digital Financial Services",
        "invented the iconic Paytm Soundbox for instant audio payment alerts in 11 regional languages, processing merchant micro-credit and travel bookings",
        [0.78, 0.82, 0.90, 0.92, 0.88, 0.38],
        {"political": "Operates under rigorous regulatory scrutiny following RBI actions on Paytm Payments Bank; restructured operations via third-party bank partnerships.", "economic": "Monetizes India's largest merchant ecosystem through monthly soundbox subscription rentals and loan distribution commissions.", "social": "The pioneer of mobile digital payments in India post-demonetization, deeply woven into everyday commercial street vocabulary.", "technological": "Engineered multi-lingual IoT Soundbox hardware, Pocket Soundbox, card machines, and dynamic AI fraud prevention engines.", "legal": "Complies with strict RBI directives on payment aggregator operations, TPAP (Third-Party Application Provider) migration, and data security.", "environmental": "Reduces physical paper receipt printing across retail checkout counters, deploying solar-powered audio soundboxes."},
        [0.28, 0.70, 0.68, 0.50, 0.88],
        {"threat_of_new_entrants": "Low; establishing millions of physical merchant relationships and deploying hardware soundboxes requires massive field force operations.", "bargaining_power_of_buyers": "Moderate-high; merchants evaluate monthly soundbox rental fees and can switch to PhonePe or BharatPe if subscription costs rise.", "bargaining_power_of_suppliers": "High; dependent on banking partners (HDFC, Axis, SBI) to host UPI handles and route merchant settlements.", "threat_of_substitutes": "High; PhonePe and BharatPe offer identical audio soundboxes and interoperable QR payment acceptance.", "competitive_rivalry": "Intense; battling PhonePe and BharatPe for retail merchant soundbox dominance and merchant working capital distribution."}
    ),
    (
        "Pine Labs", "FinTech, Payments & InsurTech",
        "large retail chains, luxury department stores, and multi-brand electronics merchants",
        "require intelligent Android smart POS terminals capable of running brand EMI promotions, loyalty programs, and omnichannel payment processing",
        "Pine Labs Android Smart POS & Plural Online Gateway", "Enterprise Merchant Commerce & Point-of-Sale Infrastructure",
        "dominates organized retail POS terminals, enabling instant multi-bank credit card EMIs, gift card management, and omnichannel digital payments",
        [0.66, 0.85, 0.88, 0.92, 0.78, 0.38],
        {"political": "Authorized by RBI as an online payment aggregator, actively supporting digital point-of-sale modernization across organized retail.", "economic": "Monetizes organized retail transaction processing volume across India, Southeast Asia, and Middle East shopping centers.", "social": "Empowers retail consumers to purchase premium goods by instantly converting store purchases into easy installments at checkout.", "technological": "Built customized Android POS application ecosystem, Plural online payment gateway, and Qfix school fee management platforms.", "legal": "Complies with RBI card tokenization rules, PCI-PTS hardware security certification, and GST-compliant electronic invoice generation.", "environmental": "Reduces printed thermal receipt paper waste through SMS and WhatsApp digital invoice delivery at retail checkouts."},
        [0.25, 0.65, 0.58, 0.45, 0.82],
        {"threat_of_new_entrants": "Low; established deep integrations with 150+ brand manufacturers and major private banks create a high competitive moat.", "bargaining_power_of_buyers": "Moderate-high; large retail chains (Reliance Retail, Shoppers Stop) command volume pricing on terminal monthly rentals.", "bargaining_power_of_suppliers": "Moderate; reliant on global POS hardware manufacturers and card networks (Visa, Mastercard, RuPay).", "threat_of_substitutes": "Moderate; mobile QR soundboxes suit micro-kiranas, but large retail stores require full-fledged POS card terminals.", "competitive_rivalry": "High; competing against Mswipe, Paytm POS, and bank-owned card swipe terminals (Innoviti, HDFC POS)."}
    ),
    (
        "CRED (Dreamplug Technologies)", "FinTech, Payments & InsurTech",
        "affluent, creditworthy urban professionals with high Experian/CIBIL credit scores (750+)",
        "seek rewarding credit card bill payments, curated luxury D2C brand commerce, and instant pre-approved personal credit lines",
        "CRED App, CRED Pay & CRED Garage", "Premium High-Trust Consumer FinTech & Lifestyle Club",
        "delivers exclusive rewards for timely credit card bill payments, CRED Cash instant pre-approved low-interest loans, and vehicle maintenance tracking via Garage",
        [0.60, 0.82, 0.92, 0.95, 0.76, 0.35],
        {"political": "Aligns with RBI directives promoting credit discipline, digital debt repayment, and consumer credit bureau score transparency.", "economic": "Caters exclusively to India's top 1% consuming class who account for over 35% of all credit card spends in the nation.", "social": "Cultivated an aspirational, invite-only community aesthetic, making timely bill payment a badge of social and financial prestige.", "technological": "Award-winning, highly distinctive neo-brutalist mobile UI design, automated hidden credit card fee detectors, and micro-app architecture.", "legal": "Strictly adheres to RBI digital lending guidelines, customer data privacy mandates, and explicit borrower consent frameworks.", "environmental": "Paperless digital credit card statement parsing and automated reward redemptions with zero physical paper waste."},
        [0.32, 0.68, 0.55, 0.48, 0.80],
        {"threat_of_new_entrants": "Moderate-low; high brand equity, cultural resonance, and concentrated base of 12M+ affluent users create strong network effects.", "bargaining_power_of_buyers": "Moderate-high; discerning affluent members expect premium rewards and quickly voice criticism if reward points are devalued.", "bargaining_power_of_suppliers": "Moderate; partners with lending NBFCs and D2C brands eager to access India's highest-spending demographic.", "threat_of_substitutes": "Moderate; mobile banking apps and rival payment platforms (PhonePe, Paytm) offer card bill payment facilities.", "competitive_rivalry": "Moderate; unique focus on the high-credit-score niche limits direct competition from mass-market UPI apps."}
    ),
    (
        "BharatPe (Resilient Innovations)", "FinTech, Payments & InsurTech",
        "small offline shopkeepers, neighborhood merchants, and unorganized grocery retailers",
        "need zero-commission merchant UPI payment acceptance and unsecured daily-installment working capital credit",
        "BharatPe Interoperable QR & BharatSwipe", "Merchant Financial Services & Kirana Working Capital",
        "pioneered 0% MDR interoperable merchant QR codes, automated daily installment loan collections via incoming payments, and PostPe consumer credit",
        [0.68, 0.85, 0.88, 0.90, 0.80, 0.36],
        {"political": "Beneficiary of government digital payment promotion; operates Unity Small Finance Bank in partnership with Centrum Group.", "economic": "Provides vital working capital loans to underbanked small merchants, recovering principal through automated daily UPI deductions.", "social": "Empowered over 13M small merchants to embrace digital payments without paying transaction commission fees on debit cards.", "technological": "Proprietary loan underwriting algorithm based on daily UPI transaction velocity, custom merchant soundbox, and BharatSwipe Android POS.", "legal": "Complies with RBI NBFC partnership guidelines, fair debt recovery practices, and payment aggregator licensing criteria.", "environmental": "Replaces paper passbooks and manual cash collections with clean, automated digital UPI settlements."},
        [0.28, 0.70, 0.62, 0.50, 0.85],
        {"threat_of_new_entrants": "Moderate-low; merchant onboarding field force and lending historical repayment data create solid moats.", "bargaining_power_of_buyers": "High; kirana merchants are sensitive to loan interest rates and readily switch QR stands if fees or penalties are imposed.", "bargaining_power_of_suppliers": "Moderate; relies on partner NBFCs and Unity Small Finance Bank for underlying loan capital.", "threat_of_substitutes": "High; PhonePe, Paytm, and Google Pay offer identical merchant QR stands with audio soundboxes.", "competitive_rivalry": "Fierce; battling Paytm and PhonePe directly for merchant counter real estate and merchant lending volume."}
    ),
    (
        "PolicyBazaar (PB Fintech)", "FinTech, Payments & InsurTech",
        "Indian middle-class families, self-employed professionals, and vehicle owners",
        "seek transparent, unbiased price comparisons of life, health, and motor insurance policies with end-to-end claim assistance",
        "PolicyBazaar Insurance Marketplace & Claim Samadhan", "Digital Insurance Aggregator & Claim Support Platform",
        "commands 90%+ market share in online insurance aggregation, offering side-by-side policy comparisons, discounted premiums, and dedicated 24/7 on-ground claim assistance",
        [0.72, 0.86, 0.92, 0.94, 0.84, 0.35],
        {"political": "Regulated under Insurance Regulatory and Development Authority of India (IRDAI); supports national goal of 'Insurance for All by 2047'.", "economic": "Direct beneficiary of low insurance penetration in India (less than 4% of GDP), expanding rapidly into Tier-2/3 semi-urban markets.", "social": "Transformed insurance buying from an awkward face-to-face push by neighborhood agents into an empowered self-directed digital decision.", "technological": "AI conversational advisory chatbots, automated pre-medical tele-consultations, and integrated claim submission workflows.", "legal": "Strict compliance with IRDAI advertising guidelines, commission disclosure regulations, and policyholder protection rules.", "environmental": "100% paperless insurance issuance, eliminating millions of physical policy bond booklets and courier dispatches."},
        [0.25, 0.62, 0.58, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; massive 15+ year consumer brand recall, millions of policy reviews, and deep insurer API integrations create unassailable moats.", "bargaining_power_of_buyers": "Moderate-high; customers visit PolicyBazaar precisely to compare prices and switch to lower-premium insurance plans.", "bargaining_power_of_suppliers": "Moderate; insurance companies (HDFC Life, Star Health) rely heavily on PolicyBazaar for direct retail distribution volumes.", "threat_of_substitutes": "Moderate; direct insurer websites and traditional offline insurance agents offer competing purchase routes.", "competitive_rivalry": "Low-to-moderate online; maintains near-monopolistic dominance in digital insurance aggregation against smaller rivals."}
    ),
    (
        "Paisabazaar (PB Fintech)", "FinTech, Payments & InsurTech",
        "salaried individuals, credit seekers, and retail borrowers",
        "need free lifelong credit score tracking, transparent credit health advisory, and instant pre-approved personal loans across multiple banks",
        "Paisabazaar Credit Tracker & Pre-Approved Loan Marketplace", "Digital Lending Marketplace & Credit Health Platform",
        "delivers free monthly credit bureau score updates, personalized credit building advice, and instant digital personal loan approvals from 50+ partner lenders",
        [0.65, 0.85, 0.90, 0.92, 0.80, 0.35],
        {"political": "Operates within RBI digital lending guidelines; supports national financial inclusion through transparent credit health monitoring.", "economic": "Monetizes lead generation and loan fulfillment fees across unsecured personal loans, credit cards, and micro-business credit lines.", "social": "Educates millions of first-time borrowers on the importance of maintaining a healthy 750+ CIBIL score to secure low loan rates.", "technological": "Algorithmic matching engine (Chance of Approval) that evaluates credit history against lender risk models to maximize sanction probability.", "legal": "Adheres strictly to explicit customer consent norms for bureau pulls, RBI data privacy mandates, and ethical tele-calling guidelines.", "environmental": "Paperless end-to-end digital loan origination and instant bank account disbursals without physical branch visits."},
        [0.28, 0.68, 0.58, 0.46, 0.82],
        {"threat_of_new_entrants": "Moderate-low; consumer brand recall, partnerships with 50+ banking institutions, and bureau integrations form strong moats.", "bargaining_power_of_buyers": "Moderate; users compare loan interest rates, processing fees, and tenure options across competing banks on a single screen.", "bargaining_power_of_suppliers": "Moderate; banks and NBFCs pay origination fees, but set their own independent underwriting approval policies.", "threat_of_substitutes": "High; competing loan aggregators (BankBazaar), fintech apps, and direct bank net banking pre-approved offers.", "competitive_rivalry": "High; competing against BankBazaar, CRED, and direct digital lending apps for consumer credit origination."}
    ),
    (
        "Navi Technologies (Sachin Bansal)", "FinTech, Payments & InsurTech",
        "middle-class smartphone users, entry-level professionals, and first-time home buyers",
        "demand instant collateral-free digital personal loans in under 10 minutes and zero-commission comprehensive health insurance",
        "Navi App & 2-Minute Cash Loans", "Full-Stack Digital Lending & Health Insurance",
        "provides 100% paperless digital personal loans disbursed directly to bank accounts in under 10 minutes, with transparent interest rates and zero paperwork",
        [0.64, 0.84, 0.88, 0.94, 0.80, 0.36],
        {"political": "Operates under RBI NBFC regulations and IRDAI insurance framework; demonstrates high-tech domestic financial product innovation.", "economic": "Targets middle-income Indian households seeking fast emergency liquidity or affordable family health insurance without agent commissions.", "social": "Eliminated the indignity and bureaucratic intimidation of traditional bank loan applications for young aspirational workers.", "technological": "100% automated algorithmic credit underwriting using bank statement analyzers and alternate digital footprint parameters.", "legal": "Strictly adheres to RBI digital lending guidelines prohibiting third-party pool accounts and ensuring transparent annual percentage rates (APR).", "environmental": "Completely digital operations eliminating branch infrastructure, paper documentation, and in-person agent travel."},
        [0.32, 0.72, 0.58, 0.48, 0.85],
        {"threat_of_new_entrants": "Moderate; building proprietary automated underwriting models requires capital, but lending market remains open to tech challengers.", "bargaining_power_of_buyers": "High; digital borrowers compare interest rates and disbursal speeds across competing instant loan apps.", "bargaining_power_of_suppliers": "Moderate; requires diversified wholesale debt lines and equity capital to fund balance sheet loan growth.", "threat_of_substitutes": "High; bank pre-approved loans, credit card personal loans, and competing instant apps (KreditBee, MoneyTap).", "competitive_rivalry": "Intense; competing in the high-stakes instant personal loan space against specialized fintech lenders and consumer banks."}
    ),
    (
        "Lendingkart Technologies", "FinTech, Payments & InsurTech",
        "unorganized MSME proprietors, local retailers, and small manufacturing workshops",
        "seek fast collateral-free working capital loans under ₹10 lakh evaluated on business cash-flows rather than physical property assets",
        "Lendingkart MSME Working Capital Loans", "Algorithmic MSME Working Capital Finance",
        "delivers collateral-free business loans disbursed within 24-48 hours using proprietary 10,000+ data-point underwriting models and GST data parsing",
        [0.68, 0.84, 0.86, 0.92, 0.78, 0.40],
        {"political": "Supports government Atmanirbhar Bharat MSME priority sector lending objectives and CGTMSE credit guarantee programs.", "economic": "Fills the massive $300B+ MSME credit deficit in India by financing working capital for raw material purchases and inventory expansion.", "social": "Empowers first-generation small factory owners and retailers who lack ancestral property to pledge as traditional collateral.", "technological": "Proprietary Big Data credit scoring engine evaluating GST filings, bank cash flows, bureau history, and business stability metrics.", "legal": "Complies with RBI scale-based NBFC norms, digital loan disclosure rules, and statutory corporate lending compliances.", "environmental": "Paperless digital loan lifecycle supporting green micro-enterprises and eliminating physical paperwork dispatches."},
        [0.30, 0.68, 0.60, 0.42, 0.82],
        {"threat_of_new_entrants": "Moderate-low; underwriting algorithms trained on millions of Indian SME repayment cycles across 4,000+ towns create strong moats.", "bargaining_power_of_buyers": "Moderate; MSMEs value speed of fund arrival within 24 hours to capitalize on seasonal inventory discounts.", "bargaining_power_of_suppliers": "Moderate; relies on co-lending partnerships with public and private banks to expand balance sheet reach.", "threat_of_substitutes": "Moderate; informal moneylenders, trade credit from suppliers, and government Mudra loans offer alternative credit.", "competitive_rivalry": "High; competing with FlexiLoans, NeoGrowth, and small finance banks in the unsecured business loan space."}
    ),
    (
        "Mswipe Technologies", "FinTech, Payments & InsurTech",
        "independent merchant shopkeepers, mobile service professionals, and retail doctors",
        "need affordable portable card swipe machines, contact-less NFC payment acceptance, and automated merchant settlements",
        "Mswipe Wisepad & Android Smart POS", "Mobile Point-of-Sale (mPOS) & Merchant Acquiring",
        "pioneered pocket-sized mPOS card swiping terminals connecting via Bluetooth to smartphones, offering competitive merchant MDR fees and daily settlements",
        [0.66, 0.82, 0.86, 0.88, 0.78, 0.38],
        {"political": "Licensed by RBI as an online payment aggregator, actively supporting rural and semi-urban digital payment adoption mandates.", "economic": "Enables small merchants to accept debit and credit card payments, capturing higher transaction tickets than cash-only stores.", "social": "Levelled the playing field for neighborhood mom-and-pop shops, giving them the same card-swiping credibility as luxury malls.", "technological": "Engineered low-power Bluetooth mPOS card readers, Android-based touch billing devices, and QR-integrated sound terminals.", "legal": "Meets strict EMVCo Level 1 & 2 security standards, PCI-DSS compliance, and RBI card tokenization guidelines.", "environmental": "Digital e-slips sent via SMS reduce thermal paper usage and carbon emissions from manual cash handling."},
        [0.30, 0.72, 0.60, 0.48, 0.82],
        {"threat_of_new_entrants": "Moderate-low; field service distribution across 800+ Indian cities and hardware maintenance networks create operational moats.", "bargaining_power_of_buyers": "High; small merchants are sensitive to device rental fees and card transaction charges (MDR).", "bargaining_power_of_suppliers": "Moderate; dependent on international POS chip fabricators and acquiring bank sponsor arrangements.", "threat_of_substitutes": "High; free UPI QR codes and soundboxes have displaced entry-level debit card swiping for transactions under ₹500.", "competitive_rivalry": "High; competing against Pine Labs, Paytm POS, and bank-owned point-of-sale machines."}
    ),
    (
        "MobiKwik (One Mobikwik Systems)", "FinTech, Payments & InsurTech",
        "young digital consumers, online gamers, and utility bill payers",
        "seek instant digital credit at checkout, digital wallet recharges, and zero-fee peer-to-peer UPI transfers",
        "MobiKwik Wallet & ZIP Buy Now Pay Later", "Digital Wallet & Consumer BNPL Credit",
        "provides instant up to ₹60,000 ZIP credit lines usable across 4M+ online and offline merchants, with one-tap checkout and high cashback rewards",
        [0.65, 0.84, 0.88, 0.92, 0.78, 0.36],
        {"political": "Operates under RBI prepaid payment instrument (PPI) and payment aggregator licenses, supporting national digital financial expansion.", "economic": "Generates strong margins from high-frequency consumer BNPL interest, bill payment commissions, and merchant acquiring fees.", "social": "Provides crucial short-term credit buffers for young professionals and students managing month-end cash crunches before salary day.", "technological": "Proprietary algorithmic credit scoring engine, integrated Pocket UPI infrastructure, and automated Bharat BillPay (BBPS) integration.", "legal": "Adheres to RBI digital lending guidelines requiring direct lender balance sheet disbursals and strict customer data protections.", "environmental": "100% digital transactions, eliminating cash printing, coins, and paper bill receipts."},
        [0.32, 0.72, 0.60, 0.50, 0.85],
        {"threat_of_new_entrants": "Moderate-low; brand recognition built over a decade, 140M+ registered users, and merchant integrations deter new entrants.", "bargaining_power_of_buyers": "High; digital users actively compare cashback offers, credit limits, and interest-free repayment days across apps.", "bargaining_power_of_suppliers": "Moderate; partner NBFCs provide the underlying loan balance sheets for ZIP credit facilities.", "threat_of_substitutes": "High; bank credit cards, PayU LazyPay, and Paytm Postpaid offer competing BNPL services.", "competitive_rivalry": "Intense; battling in the fiercely competitive consumer wallet and BNPL lending space against major fintechs."}
    ),
    (
        "Jupiter Money (Amica Financial)", "FinTech, Payments & InsurTech",
        "digital-native Gen-Z professionals, salaried tech workers, and smart personal finance enthusiasts",
        "demand a refreshing 100% mobile neobanking experience with real-time spend analytics, automated savings pots, and rewarding debit cards",
        "Jupiter Smart Account & Auto-Save Pots", "Neobanking & Automated Personal Finance Experience",
        "features intelligent auto-budgeting by category, automated round-up savings Pots earning high interest, zero forex markups, and instant customer chat",
        [0.62, 0.82, 0.90, 0.95, 0.76, 0.35],
        {"political": "Operates under RBI Bank-as-a-Service (BaaS) and co-branding guidelines in partnership with Federal Bank and CSB Bank.", "economic": "Targets upwardly mobile young professionals with high disposable incomes, monetizing cross-sell of mutual funds, credit, and investments.", "social": "Brought a modern, visually stunning user experience to Indian banking, banishing slow legacy bank interfaces and long branch queues.", "technological": "Built on modern cloud-native microservices, providing instant transaction categorization, insights, and zero-latency UPI payments.", "legal": "Complies with RBI co-branded card and PPI guidelines, ensuring customer funds are legally held in licensed partner bank custody.", "environmental": "Paperless digital account opening via video KYC, eliminating physical paper documentation and travel to physical branches."},
        [0.35, 0.72, 0.65, 0.48, 0.84],
        {"threat_of_new_entrants": "Moderate; neobanking UI layer can be developed, but achieving scale and regulatory alignment requires deep execution.", "bargaining_power_of_buyers": "High; tech-savvy users easily migrate between Jupiter, Fi Money, and traditional private bank apps.", "bargaining_power_of_suppliers": "High; reliant on licensed sponsor banks (Federal Bank) for core banking ledger access and regulatory umbrellas.", "threat_of_substitutes": "High; modern private banking apps (HDFC Mobile, ICICI iMobile, Kotak 811) offer similar digital features.", "competitive_rivalry": "Intense head-to-head rivalry against Fi Money and modern digital banking offerings from established private banks."}
    ),
    (
        "Fi Money (Epifi Technologies)", "FinTech, Payments & InsurTech",
        "salaried tech employees, modern remote workers, and globetrotting young professionals",
        "seek automated smart deposits, zero-commission US stock investing, zero forex fee debit cards, and transparent financial tracking",
        "Fi Money Salary Account & FIT Rules", "Neobanking & Wealth-Tech for Salaried Professionals",
        "delivers automated programmable saving rules ('FIT Rules'), zero forex markup debit card for international travel, and seamless access to US equities and mutual funds",
        [0.62, 0.82, 0.90, 0.95, 0.76, 0.35],
        {"political": "Operates within RBI co-branded digital banking regulations in strategic infrastructure partnership with Federal Bank.", "economic": "Caters to high-earning knowledge economy professionals, capturing direct salary credits and wealth management transaction flows.", "social": "Encourages healthy financial habits among Indian youth through gamified savings goals and clear financial net worth dashboards.", "technological": "Sophisticated algorithmic financial engine featuring programmable rules ('Save ₹50 every time I order on Swiggy') and clean native UI.", "legal": "Strict adherence to RBI digital lending guidelines, customer data privacy laws, and Liberalised Remittance Scheme (LRS) limits for US stocks.", "environmental": "100% digital account lifecycle with paperless video KYC and eco-friendly recycled ocean plastic debit cards."},
        [0.35, 0.72, 0.65, 0.48, 0.84],
        {"threat_of_new_entrants": "Moderate; building programmable financial rules and intuitive UX requires top-tier engineering talent and banking partnerships.", "bargaining_power_of_buyers": "High; users demand flawless transaction reliability and can easily move salary credits back to traditional banks.", "bargaining_power_of_suppliers": "High; completely dependent on partner banks (Federal Bank) for regulatory license, clearing rails, and depository safety.", "threat_of_substitutes": "High; Jupiter Money, Kotak 811, and private bank apps offer comparable salary account services.", "competitive_rivalry": "Fierce direct rivalry with Jupiter Money and emerging digital platforms from major private banks."}
    ),
    (
        "Zaggle Prepaid Ocean Services", "FinTech, Payments & InsurTech",
        "corporate enterprises, HR departments, and corporate finance controllers",
        "need automated employee expense card management, tax-saving employee benefit allowances, and vendor payout automation",
        "Zaggle Save & Zaggle Zoyer SaaS", "Corporate Spend Management & Enterprise Fintech SaaS",
        "combines corporate prepaid expense cards with cloud software to automate employee travel claims, meal allowances, and accounts payable approvals",
        [0.65, 0.82, 0.85, 0.90, 0.78, 0.36],
        {"political": "Operates under RBI prepaid card issuance guidelines in collaboration with leading banking partners and corporate tax guidelines.", "economic": "Capitalizes on corporate digital transformation, replacing cumbersome physical expense vouchers with automated SaaS spend controls.", "social": "Streamlines employee reimbursements and maximizes take-home tax savings via automated food, fuel, and travel benefit cards.", "technological": "Unified cloud spend platform integrating optical character recognition (OCR) bill scanning, automated policy compliance, and ERP sync.", "legal": "Complies with Income Tax guidelines for employee perquisites, RBI prepaid instrument rules, and corporate governance standards.", "environmental": "Eliminates millions of paper expense receipts, physical cash vouchers, and manual filing cabinets across Indian corporate offices."},
        [0.28, 0.68, 0.58, 0.45, 0.80],
        {"threat_of_new_entrants": "Moderate-low; long-term enterprise corporate contracts, multi-bank issuing partnerships, and public market listing create moats.", "bargaining_power_of_buyers": "Moderate; enterprise CFOs negotiate competitive SaaS licensing fees, but switching platforms disrupts employee workflows.", "bargaining_power_of_suppliers": "Moderate; dependent on card issuing partner banks (IndusInd, Yes Bank) and card networks.", "threat_of_substitutes": "Moderate; corporate credit cards (Amex, HDFC) and global spend software (SAP Concur) compete for corporate clients.", "competitive_rivalry": "Moderate-high; competes against Happay, Enkash, and specialized corporate card platforms."}
    ),
    (
        "Cashfree Payments", "FinTech, Payments & InsurTech",
        "fast-growing e-commerce brands, marketplaces, gaming apps, and lending platforms",
        "require instant automated bulk payouts, split marketplace payments, and instant refund processing at scale",
        "Cashfree Payouts & Payment Gateway", "Automated Bulk Payouts & Marketplace Payment Rails",
        "leads India in automated bulk disbursals, processing vendor payouts and user refunds 24/7 in under 2 seconds across bank accounts, cards, and UPI",
        [0.66, 0.86, 0.88, 0.94, 0.80, 0.36],
        {"political": "Licensed by Reserve Bank of India (RBI) as a Payment Aggregator and Cross-Border Payment Aggregator (PA-CB).", "economic": "Essential infrastructure powering gig economy wage payouts (Zomato, Swiggy) and gaming withdrawals, capturing transactional fees.", "social": "Ensures delivery workers and gig professionals receive their hard-earned daily wages instantly into their bank accounts 24/7.", "technological": "High-throughput API architecture processing millions of real-time payouts with 99.9% uptime and intelligent banking rail auto-routing.", "legal": "Complies with RBI Payment Aggregator guidelines, strict anti-money laundering (AML) protocols, and customer transaction verification.", "environmental": "Paperless instant digital payment infrastructure eliminating physical cheques, demand drafts, and branch visits."},
        [0.30, 0.68, 0.62, 0.46, 0.82],
        {"threat_of_new_entrants": "Low; achieving direct core banking integrations with all major Indian banks and obtaining RBI PA licenses require immense credibility.", "bargaining_power_of_buyers": "Moderate-high; large enterprises process billions in payouts and negotiate tight basis-point fee structures.", "bargaining_power_of_suppliers": "Moderate-high; reliant on IMPS, NEFT, and UPI rail availability maintained by NPCI and RBI.", "threat_of_substitutes": "Moderate; Razorpay Payouts and direct corporate banking host-to-host integrations provide competing options.", "competitive_rivalry": "High; competing directly with Razorpay and PayU India in enterprise payouts and payment gateway solutions."}
    ),
    (
        "Instamojo", "FinTech, Payments & InsurTech",
        "independent creators, freelancers, direct-to-consumer (D2C) micro-brands, and boutique sellers",
        "seek simple payment link generation, instant online storefront creation, and easy payment collection without coding knowledge",
        "Instamojo Smart Pages & Online Store", "Creator Commerce & Micro-Merchant Payment Collection",
        "enables anyone to create a professional digital storefront and start collecting payments via payment links in under 5 minutes with zero technical setup",
        [0.64, 0.82, 0.88, 0.90, 0.78, 0.36],
        {"political": "Supports government digital commerce initiatives (ONDC) and micro-entrepreneurship empowerment across India.", "economic": "Enables first-time digital sellers and Instagram home businesses to formalize their commerce and accept secure online payments.", "social": "Catalyzes home-grown micro-entrepreneurship, allowing women bakers, artists, and educators to monetize their crafts nationwide.", "technological": "No-code Smart Pages landing page builder with integrated payment checkout, shipping integrations, and automated invoice delivery.", "legal": "Complies with RBI digital payment aggregator norms, consumer protection e-commerce rules, and standard KYC guidelines.", "environmental": "Empowers home-based micro-businesses, reducing commercial real estate demand and supporting local artisan production."},
        [0.35, 0.72, 0.58, 0.52, 0.80],
        {"threat_of_new_entrants": "Moderate; payment link tools are ubiquitous, but building an integrated store platform with merchant trust is defensible.", "bargaining_power_of_buyers": "High; micro-merchants are sensitive to percentage transaction fees and easily switch to Shopify or Razorpay Payment Links.", "bargaining_power_of_suppliers": "Moderate; reliant on upstream payment processing rails and acquiring bank gateways.", "threat_of_substitutes": "High; Razorpay Payment Links, Shopify, and social commerce platforms (Meesho) offer alternative sales avenues.", "competitive_rivalry": "Moderate-high; competes against Razorpay, Cashfree, and no-code e-commerce website builders."}
    ),
    (
        "Khatabook (Khatabook Technologies)", "FinTech, Payments & InsurTech",
        "traditional neighborhood kirana store owners, wholesalers, and micro-merchants",
        "need simple digital bookkeeping to track customer credit (udhaar) and automated payment collection reminders via WhatsApp",
        "Khatabook Digital Bahi Khata & QR Collections", "Digital Ledger Bookkeeping & MSME FinTech",
        "replaces paper bahi-khata notebooks with an intuitive mobile app, sending polite automated WhatsApp payment reminders that speed up credit recovery by 3x",
        [0.65, 0.82, 0.92, 0.92, 0.76, 0.35],
        {"political": "Empowers grassroots informal retail trade under national digital literacy and MSME formalization roadmaps.", "economic": "Directly improves working capital liquidity for small shopkeepers by accelerating collection of sticky consumer credit.", "social": "Eliminates awkward face-to-face arguments over unpaid neighborhood debts by offloading collection reminders to polite automated WhatsApp alerts.", "technological": "Offline-capable lightweight mobile app designed in 12 Indian regional languages, automatic cloud backup, and QR billing integration.", "legal": "Adheres to Indian digital consumer protection guidelines, explicit merchant consent frameworks, and data localization policies.", "environmental": "Eliminates millions of paper ledger bahi-khata registers and paper bill receipt books across Indian bazaars."},
        [0.35, 0.70, 0.55, 0.48, 0.82],
        {"threat_of_new_entrants": "Moderate-low; deep grassroots viral adoption among 10M+ registered merchants creates strong localized network effects.", "bargaining_power_of_buyers": "High; small merchants expect core bookkeeping to remain free and resist paying subscription fees.", "bargaining_power_of_suppliers": "Low; relies on standard telecommunications and cloud messaging APIs (WhatsApp Business).", "threat_of_substitutes": "Moderate-high; OkCredit, pen-and-paper ledgers, and billing POS software provide alternative bookkeeping.", "competitive_rivalry": "High; competing directly against OkCredit and merchant acquiring apps for primary engagement with small shop owners."}
    ),
    (
        "OkCredit", "FinTech, Payments & InsurTech",
        "grassroots retail shopkeepers, rural suppliers, and micro-distributors",
        "seek simple, reliable digital ledger recording of transactions with instant digital receipts sent to customers",
        "OkCredit Digital Ledger & OkStaff Payroll", "Micro-Merchant Bookkeeping & Staff Management",
        "delivers simple 100% paperless credit accounting, automatic balance updates sent via SMS, and integrated staff attendance and salary tracking",
        [0.64, 0.80, 0.90, 0.90, 0.75, 0.35],
        {"political": "Supports financial inclusion of micro-enterprises and digital literacy across non-metro Indian commercial districts.", "economic": "Helps marginal grocery and hardware shop owners maintain accurate credit ledgers, preventing loss of revenue from forgotten debts.", "social": "Builds trust between local community merchants and their customers through transparent, real-time transaction SMS receipts.", "technological": "Ultra-lightweight Android app operating seamlessly on low-cost smartphones and slow 2G/3G connectivity in remote areas.", "legal": "Complies with digital data security standards, merchant privacy disclosures, and mobile communication regulations.", "environmental": "Replaces traditional paper ledger notebooks and paper salary vouchers with clean digital records."},
        [0.35, 0.70, 0.55, 0.48, 0.82],
        {"threat_of_new_entrants": "Moderate; ledger recording software is conceptually simple, but establishing trusted brand identity with merchants requires years.", "bargaining_power_of_buyers": "High; small shopkeepers can revert to pen-and-paper notebooks if app experience is complicated.", "bargaining_power_of_suppliers": "Low; standard cloud and SMS gateway infrastructure.", "threat_of_substitutes": "High; Khatabook, manual registers, and merchant payment apps (PhonePe for Business).", "competitive_rivalry": "Intense head-to-head rivalry against Khatabook for leadership in micro-merchant digital accounting."}
    ),
    (
        "Digit Insurance (Go Digit Infoworks)", "FinTech, Payments & InsurTech",
        "young digital consumers, car and two-wheeler owners, and travel insurance buyers",
        "demand simple, zero-jargon insurance policies with self-inspection smartphone video claims and ultra-fast claim settlement",
        "Digit Motor, Health & Travel Insurance", "Full-Stack InsurTech & Simple Digital Insurance",
        "replaces 50-page complex insurance documents with simple summary documents, self-inspection video claims settled in minutes, and transparent pricing",
        [0.70, 0.85, 0.92, 0.95, 0.82, 0.36],
        {"political": "Licensed full-stack general insurer regulated by IRDAI; actively participates in regulatory sandboxes for novel insurance concepts.", "economic": "Rapidly expanding general insurance market share, achieving one of the fastest climbs to profitability among global insurtech unicorns.", "social": "Demystified insurance by writing policy wordings in plain language that 15-year-olds can understand, building high consumer trust.", "technological": "Smartphone-based self-inspection video claims using computer vision to assess car dent damage and auto-approve repair estimates.", "legal": "Strictly adheres to IRDAI solvency margin mandates, policyholder grievance resolution SLAs, and consumer disclosure norms.", "environmental": "100% paperless insurance operations, eliminating physical surveyor travel through smartphone video claim inspections."},
        [0.26, 0.65, 0.58, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; obtaining full-stack general insurance underwriting licenses from IRDAI requires ₹100+ Cr capital and regulatory clearances.", "bargaining_power_of_buyers": "Moderate-high; motor and travel insurance buyers easily compare premiums on aggregators like PolicyBazaar.", "bargaining_power_of_suppliers": "Moderate; reliant on global reinsurance companies (Munich Re, Swiss Re) to offload catastrophic risk portfolios.", "threat_of_substitutes": "Moderate; established legacy general insurers (ICICI Lombard, Bajaj Allianz, Tata AIG) and Acko General Insurance.", "competitive_rivalry": "High; competing fiercely against Acko in direct-to-consumer digital channels and against ICICI Lombard across auto dealerships."}
    ),
    (
        "Acko General Insurance", "FinTech, Payments & InsurTech",
        "digital-native urban car/bike owners, gig workers, and ride-hailing app users",
        "seek commission-free direct auto insurance, micro-insurance embedded in travel/food apps, and seamless doorstep car repair pickup",
        "Acko Direct Motor & Health Insurance", "Digital-First Direct-to-Consumer General Insurance",
        "eliminates insurance broker commissions to deliver up to 40% cheaper auto insurance, instant paperless claim payouts, and free vehicle repair pickup",
        [0.70, 0.84, 0.92, 0.96, 0.82, 0.36],
        {"political": "Regulated by IRDAI; pioneers embedded micro-insurance partnerships protecting millions of Ola cab passengers and Swiggy delivery workers.", "economic": "Direct-to-consumer digital model bypasses middleman commissions, passing cost savings back to urban consumers as lower annual premiums.", "social": "Transformed car insurance into a frictionless digital experience, eliminating physical inspections and lengthy garage paperwork.", "technological": "Proprietary algorithmic underwriting engine, embedded SDKs integrated directly inside Ola and Amazon apps, and mobile claim processing.", "legal": "Adheres to IRDAI solvency ratio mandates, Motor Vehicles Act mandatory third-party liability rules, and fair claim settlement codes.", "environmental": "Paperless digital insurance policies, zero paper claim forms, and efficient authorized garage network management."},
        [0.26, 0.65, 0.58, 0.44, 0.84],
        {"threat_of_new_entrants": "Low; full-stack insurance carrier licenses are heavily restricted by IRDAI, creating a high barrier to entry.", "bargaining_power_of_buyers": "Moderate-high; tech-savvy car owners compare policy costs online annually at renewal time.", "bargaining_power_of_suppliers": "Moderate; dependent on international reinsurance backing for high-ticket commercial risk underwriting.", "threat_of_substitutes": "Moderate; Digit Insurance, ICICI Lombard, and HDFC ERGO offer competing motor and health insurance.", "competitive_rivalry": "Intense rivalry against Digit Insurance in digital D2C motor and health insurance channels."}
    )
]

for item in sector3_data:
    add_c(*item)

print(f"Sector 3 added: {len(sector3_data)} companies. Total: {len(comps)}")

# ==============================================================================
# SECTOR 4: IT Services & Tech Consulting (22 companies)
# ==============================================================================
sector4_data = [
    (
        "Tata Consultancy Services (TCS)", "IT Services & Tech Consulting",
        "Global Fortune 500 enterprises, multinational financial institutions, and government mega-infrastructure departments",
        "demand mission-critical legacy modernization, secure enterprise cloud migration, and scalable AI business transformation",
        "TCS BaNCS Core Banking & Cognix Enterprise AI", "Enterprise IT Services & Core Banking Platforms",
        "delivers legendary institutional delivery reliability, unmatched scale with 600,000+ engineers, and the world-leading BaNCS banking platform",
        [0.68, 0.86, 0.88, 0.94, 0.76, 0.65],
        {"political": "Key technological partner for Government of India sovereign digital platforms (Passport Seva, India Post, MCA21) and cross-border trade.", "economic": "Major generator of foreign exchange earnings ($29B+ annual revenue), deeply tied to enterprise IT spending cycles in North America and Europe.", "social": "One of India's largest private sector employers, providing high-mobility engineering careers to hundreds of thousands of STEM graduates.", "technological": "Leading investments in generative AI enterprise suites, cloud-native migration with AWS/Azure, and proprietary TCS BaNCS platforms.", "legal": "Complies with global enterprise data protection regulations (GDPR, California CCPA, Indian DPDP), and US H-1B visa compliance.", "environmental": "Committed to Net-Zero emissions by 2030, operating green campus facilities across India and reducing enterprise client compute footprint."},
        [0.15, 0.65, 0.50, 0.40, 0.85],
        {"threat_of_new_entrants": "Very low; multi-decade client relationships with global central banks and Fortune 500 boards form an unassailable moat.", "bargaining_power_of_buyers": "Moderate; Fortune 500 CIOs negotiate aggressive multi-year renewal pricing, but high switching friction preserves long contracts.", "bargaining_power_of_suppliers": "Low-to-moderate; access to India's vast engineering graduate talent pool ensures continuous, cost-effective talent replenishment.", "threat_of_substitutes": "Moderate; global consulting giants (Accenture, IBM) and in-house Global Capability Centers (GCCs) compete for enterprise budgets.", "competitive_rivalry": "Intense head-to-head competition against Infosys, Accenture, Cognizant, and Wipro for multi-hundred million dollar digital deals."}
    ),
    (
        "Infosys Limited", "IT Services & Tech Consulting",
        "global enterprise CIOs, multinational retailers, and forward-thinking digital organizations",
        "seek generative AI-first enterprise transformation, automated cloud infrastructure, and human-centric digital experience design",
        "Infosys Topaz (AI-First) & Infosys Cobalt Cloud", "Generative AI Platforms & Enterprise Cloud Transformation",
        "features Topaz generative AI foundation models, Cobalt cloud suite with 35,000+ assets, and human-centric design consulting via Wongdoody",
        [0.66, 0.86, 0.88, 0.95, 0.76, 0.68],
        {"political": "Advises international corporate and public boards, actively contributing to global technology standards and Indian digital trade forums.", "economic": "Drives substantial foreign exchange inflows into India, sensitive to US enterprise discretionary tech spending and interest rates.", "social": "Iconic symbol of Indian corporate governance, middle-class meritocracy, and large-scale educational training at the Infosys Mysuru campus.", "technological": "Pioneering generative AI deployment across enterprise workflows, proprietary Topaz platform, automated software engineering agents.", "legal": "Strict adherence to SEC/NYSE reporting standards, Sarbanes-Oxley (SOX), international intellectual property laws, and data privacy.", "environmental": "Achieved carbon neutrality 30 years ahead of Paris Agreement targets, generating solar energy for 100% of its massive campus operations."},
        [0.16, 0.68, 0.52, 0.42, 0.85],
        {"threat_of_new_entrants": "Very low; massive global delivery centers, enterprise domain certifications, and $18B+ scale create high entry moats.", "bargaining_power_of_buyers": "Moderate; enterprise clients expect continuous productivity gains and price discounts driven by automation.", "bargaining_power_of_suppliers": "Low-to-moderate; premier employer of choice for engineering graduates with world-renowned corporate training infrastructure.", "threat_of_substitutes": "Moderate; GCC captive centers set up by US banks and tech firms in India compete for high-end engineering talent.", "competitive_rivalry": "Fierce rivalry against Tata Consultancy Services (TCS), Accenture, and Cognizant for flagship digital transformation contracts."}
    ),
    (
        "Wipro Limited", "IT Services & Tech Consulting",
        "multinational energy conglomerates, manufacturing enterprises, and global healthcare organizations",
        "require end-to-end IT infrastructure outsourcing, industrial IoT integration, and enterprise cybersecurity resilience",
        "Wipro FullStride Cloud & Wipro ai360", "Enterprise Infrastructure Services & Cloud Transformation",
        "combines deep domain expertise in energy and manufacturing utilities with the $1B FullStride Cloud ecosystem and global cybersecurity operations",
        [0.65, 0.84, 0.85, 0.92, 0.75, 0.65],
        {"political": "Engages with global energy and public utility infrastructure modernization programs across Europe, Americas, and Asia-Pacific.", "economic": "Navigating macroeconomic cycles in European and US enterprise tech spending, realigning business units for high-margin cloud consulting.", "social": "Deep philanthropic legacy through the Azim Premji Foundation, which directs corporate wealth to elementary education across rural India.", "technological": "Invested $1B in Wipro ai360 to train 250,000 employees in generative AI and embed intelligence across software delivery pipelines.", "legal": "Complies with cross-border transfer pricing regulations, multinational corporate governance rules, and international labor standards.", "environmental": "Ranked among top global tech firms for environmental sustainability, investing in campus water recycling and energy conservation."},
        [0.18, 0.70, 0.54, 0.44, 0.84],
        {"threat_of_new_entrants": "Low; multi-decade client entrenchment, global cybersecurity certifications, and multi-country delivery centers create moats.", "bargaining_power_of_buyers": "Moderate-high; enterprise buyers demand cost takeout guarantees and flexible consumption-based pricing.", "bargaining_power_of_suppliers": "Low-to-moderate; abundant availability of domestic software engineering talent, though niche AI specialists command high premiums.", "threat_of_substitutes": "Moderate; specialized consulting firms and captive Global Capability Centers offer competing models.", "competitive_rivalry": "High; competing fiercely with HCLTech, LTIMindtree, and Cognizant across infrastructure and application maintenance."}
    ),
    (
        "HCLTech", "IT Services & Tech Consulting",
        "high-tech hardware manufacturers, semiconductor firms, and telecommunications leaders",
        "need advanced product engineering R&D, silicon chip design verification, and automated digital workplace management",
        "HCLTech Supercharging Progress & Actian Data Platform", "Engineering R&D Services & Digital Operations",
        "leads global IT firms in pure-play Engineering and R&D (ERS) services, enterprise product design, and automated modern digital workplace management",
        [0.65, 0.85, 0.86, 0.94, 0.75, 0.65],
        {"political": "Aligns with global semiconductor supply chain diversification, supporting aerospace and defense engineering collaborations.", "economic": "Benefits from high-margin engineering software products (HCL Software) and steady recurring managed infrastructure services revenue.", "social": "Promotes technical skill development through innovative TechBee programs that hire and train high-school graduates into software engineers.", "technological": "World leader in embedded hardware engineering, 5G wireless protocol testing, silicon tape-out verification, and the Actian analytics engine.", "legal": "Meets international export control regulations (ITAR), complex intellectual property licensing laws, and global data privacy compliances.", "environmental": "Actively reduces carbon intensity of client cloud workloads, operating LEED-certified development centers across NCR, Chennai, and Bengaluru."},
        [0.18, 0.68, 0.52, 0.42, 0.82],
        {"threat_of_new_entrants": "Low; deep hardware testing labs, specialized RF test chambers, and silicon design expertise require massive capital investment.", "bargaining_power_of_buyers": "Moderate; tech hardware clients value HCLTech's specialized chip design IP and rarely switch mid-product development.", "bargaining_power_of_suppliers": "Low-to-moderate; steady talent pipeline from premier engineering colleges across South and North India.", "threat_of_substitutes": "Moderate; specialized ER&D firms (L&T Technology Services, Cyient) compete in specific industrial engineering niches.", "competitive_rivalry": "High; competes against TCS, Infosys, and global specialists like Capgemini in engineering and enterprise software services."}
    ),
    (
        "Tech Mahindra", "IT Services & Tech Consulting",
        "global telecom operators, network equipment vendors, and media entertainment conglomerates",
        "seek 5G telecom network rollout orchestration, OSS/BSS digital transformation, and automated customer experience engineering",
        "NXT.NOW Telecom 5G Platform & Comviva Digital Solutions", "Telecommunications Network Modernization & Enterprise Tech",
        "world's premier telecom IT services provider, delivering specialized 5G network design, automated OSS/BSS billing, and customer experience operations",
        [0.65, 0.84, 0.85, 0.92, 0.75, 0.62],
        {"political": "Partners with international telecommunications ministries on open RAN architecture, cyber defense, and telecom indigenization.", "economic": "Realigned around high-value enterprise AI deals while maintaining market leadership in global 5G network rollout spending.", "social": "Extensive workforce upskilling initiatives across 90+ countries, driving digital employment opportunities across non-metro Indian hubs.", "technological": "Deep proprietary telecom software portfolio via Comviva, network automation platforms, and software-defined networking (SDN/NFV) tools.", "legal": "Complies with strict telecom security regulations, GDPR subscriber data protection, and international intellectual property laws.", "environmental": "Engineers energy-efficient network sleep algorithms for cellular telecom towers, cutting power consumption for mobile network operators."},
        [0.20, 0.70, 0.55, 0.45, 0.84],
        {"threat_of_new_entrants": "Low; specialized telecom network domain protocols, OSS/BSS legacy interfaces, and carrier-grade certifications create strong moats.", "bargaining_power_of_buyers": "Moderate-high; global telecom telcos (AT&T, BT, Vodafone) face tight capital constraints and demand strict cost efficiencies.", "bargaining_power_of_suppliers": "Low-to-moderate; large-scale engineering workforce in Pune, Hyderabad, and Chennai.", "threat_of_substitutes": "Moderate; telecom hardware vendors (Ericsson, Nokia) offer in-house professional services.", "competitive_rivalry": "High; competes with Infosys, Wipro, and Amdocs in telecommunications transformation and digital enterprise consulting."}
    ),
    (
        "LTIMindtree", "IT Services & Tech Consulting",
        "enterprise CFOs, digital supply chain leaders, and multinational retail corporations",
        "need agile enterprise ERP cloud migration, automated financial close systems, and omnichannel supply chain analytics",
        "LTIMindtree Canvas & Infinity Cloud Platform", "Agile Enterprise ERP & Digital Transformation Consulting",
        "combines Larsen & Toubro's industrial engineering heritage with Mindtree's agile digital design, offering high-speed cloud replatforming",
        [0.65, 0.85, 0.86, 0.93, 0.75, 0.62],
        {"political": "Backed by the prestigious Larsen & Toubro conglomerate, enjoying high corporate governance standing in domestic and export markets.", "economic": "Emerged as India's 6th largest IT services powerhouse following the successful mega-merger of L&T Infotech and Mindtree.", "social": "Attracts top-tier digital talent through vibrant campus culture, agile engineering pods, and progressive workplace flexibility.", "technological": "Proprietary Canvas platform with automated code analysis, cloud migration accelerators, and deep expertise in Snowflake and Salesforce.", "legal": "Strict compliance with global financial reporting standards, enterprise software licensing rules, and international data residency laws.", "environmental": "Operating energy-efficient sustainable delivery centers in Bengaluru, Mumbai, and Chennai, targeting Net Zero water usage."},
        [0.20, 0.68, 0.54, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; $4B+ revenue scale, Tier-1 client references, and comprehensive enterprise cloud credentials form steep entry barriers.", "bargaining_power_of_buyers": "Moderate; mid-tier and large enterprises appreciate LTIMindtree's agility compared to the bureaucratic rigidity of larger rivals.", "bargaining_power_of_suppliers": "Low-to-moderate; strong employer brand attracts high-caliber engineers and cloud architects.", "threat_of_substitutes": "Moderate; mid-tier IT peers (Persistent, Coforge) and top-tier giants compete across digital cloud deals.", "competitive_rivalry": "Intense; competing in the high-growth mid-to-large tier against Coforge, Persistent, and HCLTech."}
    ),
    (
        "Persistent Systems", "IT Services & Tech Consulting",
        "Silicon Valley software product companies, healthcare innovators, and digital life sciences firms",
        "seek specialized digital product engineering, core software architecture design, and HIPAA-compliant healthcare data analytics",
        "Persistent Digital Product Engineering & Healthcare Cloud", "Digital Product Engineering & Life Sciences Software",
        "delivers deep software engineering DNA, trusted by 8 out of top 10 tech product companies to co-engineer core software products and cloud platforms",
        [0.64, 0.86, 0.86, 0.95, 0.76, 0.58],
        {"political": "Supports Indo-US digital engineering partnerships, facilitating collaborative technology development between Pune and Silicon Valley.", "economic": "Consistently delivers industry-leading quarterly revenue growth, insulated by high-margin product engineering contracts.", "social": "Recognized for high-trust employee culture and deep academic research collaborations with premier Indian engineering institutes.", "technological": "Specialized expertise in cloud-native microservices, software containerization, healthcare genomics data pipelines, and AI engineering.", "legal": "Strict adherence to US healthcare HIPAA data compliance, FDA software-as-a-medical-device regulations, and enterprise IP protection.", "environmental": "Promotes green software engineering principles, optimizing algorithmic compute efficiency and reducing cloud data center energy load."},
        [0.22, 0.65, 0.52, 0.42, 0.80],
        {"threat_of_new_entrants": "Moderate-low; long-term product co-engineering relationships and joint software patent filings create deep customer stickiness.", "bargaining_power_of_buyers": "Moderate; global software ISVs rarely replace the core engineering teams who wrote the foundational source code of their products.", "bargaining_power_of_suppliers": "Moderate; competition for high-end full-stack developers and AI researchers in Pune and Hyderabad is intense.", "threat_of_substitutes": "Moderate; in-house Silicon Valley engineering teams and specialized boutique product engineering firms.", "competitive_rivalry": "High; competing directly against EPAM, GlobalLogic, and LTIMindtree for high-value product engineering engagements."}
    ),
    (
        "Coforge", "IT Services & Tech Consulting",
        "commercial airlines, global travel distribution networks, and international insurance underwriters",
        "demand specialized airline passenger service system modernization, automated insurance policy administration, and low-latency cloud architectures",
        "Coforge Travel & Insurance Cloud Modernization Suite", "Specialized Travel, Transportation & Insurance IT Consulting",
        "delivers unmatched domain expertise in airline flight operations, hotel distribution, and insurance core systems, with industry-leading client retention",
        [0.65, 0.85, 0.85, 0.92, 0.75, 0.58],
        {"political": "Operates under global civil aviation and commercial trade compliance frameworks across North America and Western Europe.", "economic": "Beneficiary of post-pandemic travel technology infrastructure upgrades and insurance core platform modernization cycles.", "social": "Cultivates deep specialized industry business knowledge among engineers, enabling meaningful strategic conversations with airline executives.", "technological": "Deep partnerships with Duck Creek, Pega, and MuleSoft, delivering specialized low-latency microservices for travel reservation engines.", "legal": "Complies with IATA airline data standards, global insurance data security laws, and international consumer privacy frameworks.", "environmental": "Engineers digital self-service solutions for airlines and airports, eliminating millions of physical paper boarding passes and baggage tags."},
        [0.22, 0.65, 0.52, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; specialized domain expertise in legacy airline ticketing systems and insurance underwriting cannot be acquired overnight.", "bargaining_power_of_buyers": "Moderate; travel and insurance clients maintain multi-year sticky partnerships due to high switching risk on mission-critical booking engines.", "bargaining_power_of_suppliers": "Low-to-moderate; steady talent pipeline from specialized IT hubs in Greater Noida, Hyderabad, and Bengaluru.", "threat_of_substitutes": "Moderate; broad-spectrum IT giants attempt to compete, but often lack Coforge's surgical domain focus.", "competitive_rivalry": "High; competes against Persistent Systems, LTIMindtree, and specialized consulting firms."}
    ),
    (
        "Mphasis (Blackstone Group)", "IT Services & Tech Consulting",
        "global investment banks, mortgage originators, and payment networks",
        "require automated cloud-native banking architectures, cognitive mortgage underwriting, and legacy mainframe modernization",
        "Mphasis NextLabs & Front2Back Digital Transformation", "Cognitive Banking & Capital Markets IT Solutions",
        "specializes in Front2Back digital transformation, using cognitive microservices to modernize legacy banking mainframes into real-time cloud systems",
        [0.64, 0.85, 0.84, 0.93, 0.76, 0.55],
        {"political": "Advises major US financial institutions, adhering to Federal Reserve and SEC digital risk governance guidelines.", "economic": "Directly tied to US mortgage origination volumes, investment banking deal flow, and enterprise BFSI IT spending cycles.", "social": "Provides high-value financial technology careers, bridging complex Wall Street capital markets requirements with Indian engineering talent.", "technological": "Patented Front2Back methodology, proprietary Sparkle innovation labs, and quantum computing algorithm development for portfolio optimization.", "legal": "Complies with Gramm-Leach-Bliley Act (GLBA) financial privacy rules, international bank secrecy laws, and Sarbanes-Oxley mandates.", "environmental": "Optimizes high-frequency financial cloud compute operations, reducing algorithmic carbon footprint in global data centers."},
        [0.24, 0.68, 0.54, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; Wall Street banking security audits, regulatory clearances, and multi-decade domain trust create strong moats.", "bargaining_power_of_buyers": "Moderate-high; global banks maintain procurement panels that negotiate volume discounts across strategic IT vendors.", "bargaining_power_of_suppliers": "Low-to-moderate; deep talent pool in Bengaluru, Pune, and Chennai specialized in banking technology.", "threat_of_substitutes": "Moderate; global consulting firms and captive bank technology centers (JPMorgan, Goldman Sachs GCCs) in India.", "competitive_rivalry": "High; competing against Virtusa, LTIMindtree, and TCS for tier-1 investment banking IT contracts."}
    ),
    (
        "Birlasoft (CK Birla Group)", "IT Services & Tech Consulting",
        "heavy industrial manufacturers, automotive component makers, and life sciences corporations",
        "need deep domain expertise in SAP S/4HANA migrations, Oracle cloud ERP implementations, and connected shop-floor manufacturing execution systems",
        "Birlasoft Manufacturing ERP & Digital Supply Chain Platform", "Industrial Manufacturing & Enterprise ERP Consulting",
        "combines CK Birla Group's 160-year industrial manufacturing heritage with specialized ERP consulting to deliver digital shop-floor transformation",
        [0.64, 0.84, 0.84, 0.91, 0.75, 0.55],
        {"political": "Supports Make in India manufacturing digitization and global supply chain modernization programs.", "economic": "Benefits from industrial capital expenditure cycles, automotive manufacturing modernization, and enterprise cloud ERP upgrades.", "social": "Bridges traditional factory floor operations with cutting-edge cloud analytics, empowering shop-floor supervisors with real-time digital insights.", "technological": "Deep competency centers in SAP, Oracle Cloud, Microsoft Dynamics, and industrial IoT machine vision for automated quality inspection.", "legal": "Complies with global manufacturing product liability standards, enterprise IP governance, and international data security laws.", "environmental": "Implements smart energy management software across manufacturing shop-floors, identifying thermal and electricity waste in real time."},
        [0.24, 0.68, 0.54, 0.44, 0.80],
        {"threat_of_new_entrants": "Low; complex industrial shop-floor understanding, ERP implementation certifications, and industrial references form strong moats.", "bargaining_power_of_buyers": "Moderate; manufacturing clients demand proven ERP delivery track records to avoid disastrous production line stoppages.", "bargaining_power_of_suppliers": "Low-to-moderate; steady availability of SAP and Oracle certified software engineers across India.", "threat_of_substitutes": "Moderate; large IT services players (TCS, Wipro) maintain large ERP practices.", "competitive_rivalry": "Moderate-high; competes against Zensar, KPIT, and mid-tier enterprise software consulting firms."}
    ),
    (
        "Cyient Limited", "IT Services & Tech Consulting",
        "global aerospace OEMs, defense contractors, geospatial mapping agencies, and rail operators",
        "require precision mechanical design engineering, avionics embedded systems, geospatial GIS spatial analytics, and defense prototyping",
        "Cyient Aerospace Design & Geospatial Spatial Analytics", "Aerospace, Defense & Geospatial Engineering Solutions",
        "pioneers precision aircraft cabin and engine design, satellite geospatial GIS spatial data modeling, and mission-critical defense engineering",
        [0.72, 0.84, 0.82, 0.94, 0.78, 0.62],
        {"political": "Direct contributor to defense indigenization, aerospace offset programs, and bilateral Indo-US defense manufacturing cooperation.", "economic": "Thrives on commercial aerospace super-cycles (Boeing, Airbus order backlogs) and government spatial mapping investments.", "social": "Elevates India's reputation in precision aerospace engineering, designing complex aircraft structural components and flight avionics.", "technological": "Proprietary geospatial AI computer vision, digital twin engineering for jet engines, and DO-178C avionics safety certifications.", "legal": "Strict compliance with US International Traffic in Arms Regulations (ITAR), global military export controls, and aerospace safety mandates.", "environmental": "Engineers lightweight composite aerospace structures that reduce fuel burn and carbon emissions for commercial jetliners."},
        [0.22, 0.65, 0.52, 0.40, 0.80],
        {"threat_of_new_entrants": "Very low; aerospace safety certifications (AS9100), defense security clearances, and multi-decade OEM audit credentials form impenetrable barriers.", "bargaining_power_of_buyers": "Moderate; aircraft manufacturers maintain tightly certified vendor lists and rarely replace trusted engineering partners.", "bargaining_power_of_suppliers": "Moderate; competition for specialized aeronautical and aerospace stress analysis engineers.", "threat_of_substitutes": "Low-to-moderate; specialized defense R&D organizations offer internal alternatives, but rely on Cyient for capacity scale.", "competitive_rivalry": "Moderate; competes primarily with L&T Technology Services and Tata Elxsi in high-end engineering design."}
    ),
    (
        "Tata Elxsi", "IT Services & Tech Consulting",
        "luxury automotive OEMs, medical device innovators, and broadcast media networks",
        "demand cutting-edge autonomous driving software (ADAS), intuitive luxury car in-cabin UI/UX, and FDA-certified medical device software",
        "Autonomai ADAS Suite & Tethr Connected Vehicle Platform", "Design-Led Automotive & Medical Device Engineering",
        "combines award-winning industrial design studios with software engineering to deliver production-ready ADAS software and medical device interfaces",
        [0.66, 0.86, 0.86, 0.96, 0.78, 0.64],
        {"political": "Supports global automotive software-defined vehicle standards (AUTOSAR) and Make in India high-value design exports.", "economic": "Commands industry-topping EBITDA margins (28-30%) due to premium design-led engineering billing rates and specialized IP licensing.", "social": "Showcases India's transition from low-cost back-office coding to world-class aesthetic design and safety-critical software architecture.", "technological": "Proprietary Autonomai autonomous driving platform, simulation suites, and ISO 13485 compliant medical software design pipelines.", "legal": "Strict compliance with ISO 26262 automotive functional safety standards and US FDA 510(k) medical device software regulations.", "environmental": "Designs lightweight, aerodynamically efficient EV interfaces and smart energy management algorithms for electric vehicles."},
        [0.22, 0.62, 0.52, 0.40, 0.80],
        {"threat_of_new_entrants": "Low; pairing world-class industrial product designers with safety-critical embedded firmware engineers is exceptionally rare.", "bargaining_power_of_buyers": "Moderate; premium automotive OEMs pay top-dollar for Tata Elxsi's proprietary software IP and design track record.", "bargaining_power_of_suppliers": "Moderate; high demand for specialized UI/UX designers and embedded C++ automotive engineers.", "threat_of_substitutes": "Moderate; global automotive engineering service providers (KPIT, FEV) compete in functional software development.", "competitive_rivalry": "Moderate; occupies a high-margin, specialized design-plus-technology niche, facing limited direct competitors at its intersection."}
    ),
    (
        "L&T Technology Services (LTTS)", "IT Services & Tech Consulting",
        "global industrial manufacturing leaders, medical equipment innovators, and telecom infrastructure giants",
        "seek pure-play engineering research and development (ER&D), smart factory robotics, industrial IoT, and digital twin simulations",
        "LTTS Smart Manufacturing & Plant Engineering Suite", "Pure-Play Engineering Research & Development (ER&D)",
        "world's premier pure-play ER&D firm, boasting 1,000+ global engineering patents, turnkey industrial smart factory setups, and medical device innovation",
        [0.66, 0.86, 0.86, 0.95, 0.76, 0.65],
        {"political": "Backed by Larsen & Toubro; supports national industrial automation, advanced robotics, and bilateral aerospace technology transfers.", "economic": "Benefits from secular global growth in outsourced engineering R&D, as global manufacturers accelerate product design cycles.", "social": "Drives engineering excellence in India, employing over 23,000 specialized mechanical, electrical, and mechatronics engineers.", "technological": "Holds 1,000+ patents, operates proprietary smart manufacturing testbeds, and develops AI algorithms for predictive machine maintenance.", "legal": "Complies with international intellectual property protection treaties, export control classifications, and functional safety standards.", "environmental": "Engineers zero-waste smart factory layouts, energy-efficient HVAC designs, and industrial carbon capture pilot equipment."},
        [0.20, 0.65, 0.52, 0.40, 0.82],
        {"threat_of_new_entrants": "Low; deep physical testing laboratories, industrial plant engineering credentials, and patent portfolios create massive barriers.", "bargaining_power_of_buyers": "Moderate; industrial clients value LTTS's multidisciplinary engineering depth spanning mechanical, electrical, and software.", "bargaining_power_of_suppliers": "Low-to-moderate; premier employer of choice for core mechanical and electrical engineering talent in India.", "threat_of_substitutes": "Moderate; in-house corporate R&D centers and European engineering consultancies (Altran, Bertrandt) offer alternative resources.", "competitive_rivalry": "High; competing directly against HCLTech, Cyient, and Tata Elxsi for major global engineering research contracts."}
    ),
    (
        "Happiest Minds Technologies", "IT Services & Tech Consulting",
        "digital-native businesses, high-growth retail brands, and modern enterprise IT leaders",
        "demand born-digital agile cloud architectures, automated cybersecurity vulnerability monitoring, and generative AI workflow acceleration",
        "Happiest Minds Generative AI & Cloud Security Suite", "Born-Digital Agile Services & Cybersecurity",
        "operates as a 100% born-digital IT consultancy, delivering AI-first enterprise application engineering, zero-trust cybersecurity, and mindful delivery",
        [0.62, 0.84, 0.86, 0.94, 0.75, 0.55],
        {"political": "Supports Indian digital innovation and corporate entrepreneurship founded by industry veteran Ashok Soota.", "economic": "Maintains pure-play digital revenue exposure (95%+), avoiding low-margin legacy maintenance commoditization.", "social": "Pioneered 'Mindful IT' corporate culture emphasizing employee happiness, wellness, and transparent corporate governance.", "technological": "Built dedicated Generative AI business unit, proprietary automated vulnerability management tools, and IoT sensor platforms.", "legal": "Strict adherence to international data protection standards, SOC-2 compliance, and zero-trust cybersecurity frameworks.", "environmental": "Carbon-efficient cloud-first service delivery, minimizing physical data center infrastructure and operating energy-saving offices."},
        [0.26, 0.68, 0.55, 0.45, 0.80],
        {"threat_of_new_entrants": "Moderate-low; established reputation in digital-only architectures, strong executive leadership, and public market credibility.", "bargaining_power_of_buyers": "Moderate; digital enterprises demand cutting-edge AI and cloud skills and readily compensate for agile execution.", "bargaining_power_of_suppliers": "Moderate; high demand for skilled cloud-native full-stack developers and cybersecurity ethical hackers.", "threat_of_substitutes": "Moderate; mid-tier digital consultancies and boutique digital agencies compete for mid-market contracts.", "competitive_rivalry": "High; competing with Persistent Systems, Zensar, and Birlasoft in high-growth digital transformation deals."}
    ),
    (
        "KPIT Technologies", "IT Services & Tech Consulting",
        "global automotive OEMs, commercial vehicle manufacturers, and tier-1 automotive suppliers",
        "require dedicated software-defined vehicle (SDV) engineering, clean electric powertrain integration, and autonomous driving ADAS software",
        "KPIT Software-Defined Vehicle Architecture & Electrification Suite", "Automotive Software-Defined Vehicle (SDV) Engineering",
        "laser-focused exclusively on the automotive mobility sector, accelerating the global transition to software-defined, electric, and autonomous vehicles",
        [0.66, 0.86, 0.86, 0.96, 0.78, 0.72],
        {"political": "Strategic partner for international automotive consortia developing open standards for automotive software (SOAFEE, AUTOSAR).", "economic": "Direct beneficiary of the multi-billion dollar global automotive shift towards software-defined vehicles and electric powertrains.", "social": "Showcases Indian software engineering leadership at the heart of luxury European, American, and Asian automotive marques.", "technological": "World leader in vehicle operating systems, AUTOSAR adaptive platforms, battery management algorithms, and Level 3 autonomous driving.", "legal": "Strict compliance with ISO 26262 automotive safety integrity levels (ASIL-D), automotive cybersecurity (ISO 21434), and ASPICE standards.", "environmental": "Directly engineers high-efficiency battery charging software and motor control algorithms that maximize EV range and reduce energy waste."},
        [0.20, 0.62, 0.52, 0.38, 0.80],
        {"threat_of_new_entrants": "Very low; automotive safety certifications (ASIL-D), deep OEM code access, and 7,000+ dedicated auto software engineers form deep moats.", "bargaining_power_of_buyers": "Moderate; global automotive OEMs (BMW, Renault, Honda) partner with KPIT for multi-year strategic SDV platform co-development.", "bargaining_power_of_suppliers": "Moderate; fierce competition for specialized embedded C++, RTOS, and automotive electronics engineers in Pune and Munich.", "threat_of_substitutes": "Low-to-moderate; general IT service providers struggle to match KPIT's hyper-specialized automotive-only focus.", "competitive_rivalry": "Moderate; competes primarily with Tata Elxsi and specialized European automotive engineering houses (FEV, Elektrobit)."}
    ),
    (
        "Zensar Technologies (RPG Group)", "IT Services & Tech Consulting",
        "global retail chains, financial services institutions, and consumer technology companies",
        "seek digital experience engineering, omnichannel retail IT integration, and automated cloud infrastructure management",
        "Zensar Experience-Led Engineering & Smart Operations", "Experience-Led Digital Engineering & Enterprise IT",
        "delivers experience-led software development, robust omnichannel retail store integration, and predictable cloud operations backed by RPG Group",
        [0.64, 0.84, 0.84, 0.91, 0.75, 0.55],
        {"political": "Supports digital trade expansion, operating global delivery hubs across the US, UK, South Africa, and India.", "economic": "Benefits from consumer retail digital investments, online shopping cart optimizations, and enterprise cloud migrations.", "social": "Committed to RPG Group's 'Hello Happiness' cultural philosophy, fostering inclusive and supportive workplace environments.", "technological": "Proprietary digital transformation frameworks, automated cloud migration toolkits, and AI data engineering pipelines.", "legal": "Complies with global data privacy mandates, enterprise intellectual property agreements, and cross-border commercial laws.", "environmental": "Promotes energy-efficient software coding practices and green data center operations across international client facilities."},
        [0.26, 0.68, 0.55, 0.45, 0.80],
        {"threat_of_new_entrants": "Low; established enterprise client relationships, global delivery footprint, and conglomerate backing create entry barriers.", "bargaining_power_of_buyers": "Moderate-high; retail and BFSI clients benchmark pricing and SLA metrics against multiple mid-tier competitors.", "bargaining_power_of_suppliers": "Low-to-moderate; steady supply of software engineers across development hubs in Pune and Hyderabad.", "threat_of_substitutes": "Moderate; competing mid-tier IT service firms and boutique digital transformation consultancies.", "competitive_rivalry": "High; competes against Birlasoft, Sonata Software, and Hexaware in mid-sized enterprise IT deals."}
    ),
    (
        "Sonata Software", "IT Services & Tech Consulting",
        "travel technology operators, modern retail distributors, and ISVs seeking Microsoft cloud modernizations",
        "need proprietary platform-based digital business engineering, Microsoft Dynamics 365 migrations, and travel reservation systems",
        "Sonata Platformation & Modernization Ecosystem", "Platform-Based Digital Engineering & Microsoft Dynamics",
        "pioneers the 'Platformation' methodology to build scalable digital platform businesses, holding elite globally recognized Microsoft Partner status",
        [0.64, 0.84, 0.84, 0.92, 0.75, 0.55],
        {"political": "Facilitates global digital trade with specialized software delivery centers across North America, Europe, Australia, and India.", "economic": "Capitalizes on enterprise demand for scalable digital platform models and lucrative Microsoft enterprise cloud licensing ecosystems.", "social": "Fosters a deep engineering culture focused on long-term platform value creation rather than generic staff augmentation.", "technological": "Proprietary Platformation framework, advanced Microsoft Dynamics 365 cloud engineering, and generative AI enterprise integrations.", "legal": "Adheres to international software intellectual property laws, enterprise data privacy standards, and global commercial trade terms.", "environmental": "Optimizes enterprise software systems to run on high-efficiency, renewable-powered Microsoft Azure cloud data centers."},
        [0.25, 0.68, 0.55, 0.45, 0.80],
        {"threat_of_new_entrants": "Low; elite Microsoft Dynamics global partnership status and 30-year track record create defensible barriers.", "bargaining_power_of_buyers": "Moderate; clients value Sonata's proven track record in complex Microsoft ERP and travel distribution platform implementations.", "bargaining_power_of_suppliers": "Low-to-moderate; steady talent pipeline of certified Microsoft cloud engineers and software architects.", "threat_of_substitutes": "Moderate; global IT services firms maintain Microsoft practices, but Sonata provides dedicated executive focus.", "competitive_rivalry": "Moderate-high; competes against Coforge, Zensar, and mid-tier digital engineering consultancies."}
    ),
    (
        "Hexaware Technologies", "IT Services & Tech Consulting",
        "enterprise CIOs, mortgage processors, and healthcare payers",
        "seek automate-first IT operations, rapid cloud replatforming, and AI-driven business process operations",
        "Hexaware Amaze for Cloud & Tensai AI Automation", "Automate-First Cloud Replatforming & Cognitive Ops",
        "delivers automated cloud replatforming via proprietary 'Amaze' automation suites, cutting cloud migration timelines and operational run costs by up to 50%",
        [0.64, 0.85, 0.85, 0.93, 0.75, 0.55],
        {"political": "Advises international enterprises on automated IT operations while complying with global cross-border labor regulations.", "economic": "Drives industry-leading revenue growth by packaging automation IP that delivers guaranteed cost savings to enterprise customers.", "social": "Advocates an 'Automate Everything' mindset that upskills traditional software testers and support staff into high-value AI engineers.", "technological": "Proprietary Amaze cloud replatforming suite, Tensai automation platform, and generative AI automated code refactoring agents.", "legal": "Complies with global enterprise compliance standards, HIPAA healthcare security rules, and international data privacy statutes.", "environmental": "Automates server consolidation and workload optimization, dramatically reducing idle compute power consumption in enterprise data centers."},
        [0.24, 0.68, 0.54, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; proprietary automation software toolkits (Amaze) and established enterprise references form strong moats.", "bargaining_power_of_buyers": "Moderate; clients demand concrete ROI and cost reduction guarantees, which Hexaware's automated tools are designed to fulfill.", "bargaining_power_of_suppliers": "Low-to-moderate; robust recruitment and training operations across Mumbai, Chennai, and Pune.", "threat_of_substitutes": "Moderate; large IT service giants (Cognizant, Infosys) provide competing automated cloud migration services.", "competitive_rivalry": "High; competing against LTIMindtree, Persistent, and Virtusa for enterprise cloud and automation transformation deals."}
    ),
    (
        "Tanla Platforms", "IT Services & Tech Consulting",
        "leading enterprise banks, telecom carriers, and e-commerce companies",
        "require mission-critical, secure cloud communications (CPaaS), automated anti-phishing protection, and verified transactional messaging",
        "Wisely CPaaS Platform & Trubloq Anti-Spam Blockchain", "Cloud Communications (CPaaS) & Blockchain Messaging",
        "processes over 800 billion interactions annually, operating the world's largest blockchain-enabled commercial communications platform (Trubloq)",
        [0.68, 0.84, 0.86, 0.94, 0.82, 0.40],
        {"political": "Works closely with Telecom Regulatory Authority of India (TRAI) on commercial SMS regulations, scrubbers, and anti-fraud mandates.", "economic": "Captures high-margin transaction fee streams on vital enterprise OTPs, banking transactional SMS, and WhatsApp commercial messages.", "social": "Protects over 1 billion Indian mobile phone users from predatory financial scams, phishing attacks, and unsolicited spam SMS.", "technological": "Pioneered Trubloq, an enterprise distributed ledger (blockchain) tracking commercial communication consent, and the Wisely CPaaS suite.", "legal": "Strict compliance with TRAI Telecom Commercial Communications Customer Preference Regulations (TCCCPR), and digital consumer privacy laws.", "environmental": "100% digital cloud communication platform, eliminating physical paper authentication notices and postal mailers."},
        [0.25, 0.65, 0.62, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; exclusive blockchain integration with all major Indian telecom operators (Jio, Airtel, Vi) creates a near-impenetrable regulatory moat.", "bargaining_power_of_buyers": "Moderate; banks and enterprises require reliable 99.99% OTP delivery within seconds and cannot compromise on reliability.", "bargaining_power_of_suppliers": "High; dependent on underlying telecom network infrastructure and official carrier SMS termination tariffs.", "threat_of_substitutes": "Moderate; global CPaaS platforms (Twilio, Infobip) operate in India, but lack Tanla's native telecom carrier blockchain integration.", "competitive_rivalry": "High; competing primarily against Route Mobile in the domestic and international enterprise messaging space."}
    ),
    (
        "Route Mobile (Proximus Group)", "IT Services & Tech Consulting",
        "global tech platforms, omnichannel retailers, and commercial banks",
        "seek global omnichannel cloud messaging APIs, WhatsApp Business solutions, identity verification, and voice broadcasting",
        "Route Mobile Omnichannel CPaaS & WhatsApp Business API", "Global Omnichannel Cloud Communications (CPaaS)",
        "provides direct telecom network connectivity to 1,000+ mobile operators worldwide, offering high-throughput SMS, WhatsApp, RCS, and voice APIs",
        [0.66, 0.84, 0.86, 0.93, 0.80, 0.40],
        {"political": "Acquisition by Belgium's Proximus Group created a global telecom communications powerhouse spanning Europe, Asia, Africa, and the Americas.", "economic": "Benefits from rapid transition from legacy SMS to interactive rich communication services (RCS) and WhatsApp conversational commerce.", "social": "Enables seamless conversational customer support, instant flight updates, and transactional security for hundreds of millions of consumers.", "technological": "Global scalable API gateway architecture, automated failover routing, and rich interactive messaging (RCS) chatbots.", "legal": "Adheres to international telecommunications data privacy regulations, European GDPR, and domestic Indian TRAI guidelines.", "environmental": "Paperless digital cloud communications, powering digital ticketing, electronic receipts, and automated customer notifications."},
        [0.25, 0.66, 0.62, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; establishing direct SS7/SMPP interconnect agreements with 1,000+ global telecom operators takes decades of commercial negotiation.", "bargaining_power_of_buyers": "Moderate-high; enterprise buyers negotiate competitive pricing on high-volume bulk transactional messaging.", "bargaining_power_of_suppliers": "High; reliant on wholesale telecom carrier termination rates and Meta WhatsApp API platform policies.", "threat_of_substitutes": "Moderate; Tanla Platforms, Twilio, and Sinch provide competing global CPaaS infrastructure.", "competitive_rivalry": "Intense; battling head-to-head with Tanla Platforms in India and with Twilio/Sinch globally."}
    ),
    (
        "Sasken Technologies", "IT Services & Tech Consulting",
        "semiconductor chipmakers, satellite communications equipment vendors, and industrial device OEMs",
        "need deep embedded firmware engineering, satellite transceiver protocol stacks, and rugged automotive microcontroller design",
        "Sasken Embedded Software & Satellite Protocol Stacks", "Embedded Hardware Firmware & Satellite Telecommunications",
        "pioneers deep-tech embedded software development, specialized satellite transceiver communication stacks, and automotive infotainment firmware",
        [0.66, 0.82, 0.82, 0.95, 0.76, 0.52],
        {"political": "Supports India Semiconductor Mission, indigenous electronics manufacturing, and space/satellite communication technologies.", "economic": "Benefits from global semiconductor design cycles and increasing software content inside modern connected industrial and automotive hardware.", "social": "Showcases India's deep-tech hardware-software co-design capabilities, proving engineering excellence at the silicon and protocol layer.", "technological": "Deep proprietary IP in 3GPP satellite communication protocol stacks, Android embedded automotive platforms, and DSP audio algorithms.", "legal": "Strict compliance with semiconductor IP licensing rules, international patent protections, and telecom standard-essential patent (SEP) laws.", "environmental": "Engineers ultra-low-power embedded sleep algorithms, extending battery life in satellite handsets and remote industrial IoT sensors."},
        [0.26, 0.65, 0.54, 0.40, 0.78],
        {"threat_of_new_entrants": "Low; deep low-level C firmware, DSP assembly coding, and satellite protocol engineering require specialized talent that few possess.", "bargaining_power_of_buyers": "Moderate; global semiconductor firms (Qualcomm, Texas Instruments) rely on Sasken's specialized firmware teams for chip board-support packages.", "bargaining_power_of_suppliers": "Moderate; competition for specialized embedded hardware and firmware engineers.", "threat_of_substitutes": "Low-to-moderate; generic IT services companies lack the capability to write low-level silicon driver code.", "competitive_rivalry": "Moderate; competes with specialized global design houses and in-house semiconductor R&D teams."}
    ),
    (
        "Newgen Software Technologies", "IT Services & Tech Consulting",
        "large universal banks, insurance carriers, and government administrative departments",
        "require low-code digital business process automation, enterprise content management (ECM), and customer communication management (CCM)",
        "NewgenONE Low-Code Enterprise Automation Platform", "Low-Code Business Process & Content Automation",
        "delivers the comprehensive NewgenONE low-code platform, automating complex commercial loan underwriting, claims processing, and high-volume document archiving",
        [0.65, 0.84, 0.85, 0.94, 0.78, 0.45],
        {"political": "Powers mission-critical digital document and process workflows for major Indian government institutions and regulatory bodies.", "economic": "Achieves high-margin software license and recurring SaaS subscription revenues across 70+ countries in banking and healthcare.", "social": "Accelerates financial loan approvals and insurance claim settlements from days to minutes, significantly improving citizen satisfaction.", "technological": "Unified NewgenONE platform combining low-code application generation, robotic process automation (RPA), and AI-driven document extraction.", "legal": "Adheres to strict financial document retention regulations, electronic signature legal validity, and international banking compliance norms.", "environmental": "Directly eliminates millions of physical paper file folders and document archives through secure legal digital content repositories."},
        [0.26, 0.65, 0.52, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; 30-year track record of rock-solid stability in tier-1 global banks and complex regulatory document compliance create high moats.", "bargaining_power_of_buyers": "Moderate; enterprise banks rarely rip out deeply embedded core business process automation software due to immense operational risk.", "bargaining_power_of_suppliers": "Low-to-moderate; high internal product engineering stability in New Delhi development centers.", "threat_of_substitutes": "Moderate; global low-code process automation platforms (Pega, Appian, ServiceNow) compete for enterprise automation deals.", "competitive_rivalry": "Moderate; competes effectively against global giants Pega and Appian with superior value pricing and domain specialization."}
    )
]

for item in sector4_data:
    add_c(*item)

print(f"Sector 4 added: {len(sector4_data)} companies. Total: {len(comps)}")

with open(part1_path, "w", encoding="utf-8") as f:
    json.dump(comps, f, indent=2)
print("Updated part1.json successfully with Sectors 1, 2, 3, 4!")
