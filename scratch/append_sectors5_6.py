"""
Appends Sector 5 (Enterprise Software, Cloud & SaaS - 22 companies) and
Sector 6 (Pharmaceuticals & Active Pharmaceutical Ingredients - 22 companies) to scratch/part1.json
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
# SECTOR 5: Enterprise Software, Cloud & SaaS (22 companies)
# ==============================================================================
sector5_data = [
    (
        "Zoho Corporation", "Enterprise Software, Cloud & SaaS",
        "global SMBs, digital-first enterprises, and privacy-conscious organizations",
        "demand a unified, comprehensive business operating system without predatory subscription price hikes or user tracking",
        "Zoho One & Zoho Books", "Unified Cloud Business Operating System",
        "delivers a complete 55+ app integrated business suite (CRM, Books, Mail, People) at a fraction of competitors' cost, with a strict zero-ad-tracking privacy pledge",
        [0.60, 0.85, 0.90, 0.96, 0.78, 0.65],
        {"political": "A champion of rural technological democratization, building world-class R&D campus hubs in Tenkasi and rural Tamil Nadu.", "economic": "Bootstrapped to multi-billion dollar enterprise valuation without external venture funding, generating massive recurring SaaS cash flows globally.", "social": "Pioneered Zoho Schools of Learning, recruiting talented rural youth straight out of school and training them into elite software architects.", "technological": "Built the entire vertical stack from owned physical data centers to proprietary programming languages, relational databases, and AI models.", "legal": "Industry leader in strict data privacy, rejecting third-party advertising trackers and complying with EU GDPR, US CCPA, and Indian DPDP Act.", "environmental": "Operates high-efficiency data centers and corporate campuses powered by company-owned 15 MW captive solar and wind farms in southern India."},
        [0.22, 0.65, 0.50, 0.44, 0.82],
        {"threat_of_new_entrants": "Low; developing 55+ interconnected, enterprise-grade business applications with global localization requires decades of engineering.", "bargaining_power_of_buyers": "Moderate; customers benefit from unmatched value pricing, and migrating an entire company's CRM, accounting, and HR off Zoho is painful.", "bargaining_power_of_suppliers": "Extremely low; owns its entire technology stack, server hardware, and network infrastructure, eliminating reliance on third-party cloud hyperscalers.", "threat_of_substitutes": "Moderate; Salesforce, Microsoft 365, Google Workspace, and Freshworks compete, but charge significantly higher standalone fees.", "competitive_rivalry": "High; competing globally against Salesforce, HubSpot, and Microsoft with superior pricing and unified database architecture."}
    ),
    (
        "Freshworks Inc.", "Enterprise Software, Cloud & SaaS",
        "mid-market IT teams, customer support leads, and fast-growing businesses",
        "seek affordable, modern customer service ticketing and IT service management (ITSM) software that is intuitive and deploys in days",
        "Freshdesk & Freshservice", "Modern Customer Support & IT Service Management SaaS",
        "provides intuitive customer ticketing across email, WhatsApp, and chat, coupled with ITIL-aligned IT service desk automation with near-zero setup overhead",
        [0.60, 0.84, 0.88, 0.95, 0.76, 0.50],
        {"political": "First Indian-founded SaaS unicorn to list on NASDAQ, blazing a trail for Indian enterprise product software companies on global bourses.", "economic": "Generates over $600M in annual recurring revenue (ARR) with strong net dollar retention from mid-market enterprise customers worldwide.", "social": "Created the 'Chennai SaaS Corridor', inspiring an entire generation of Indian software founders to build globally competitive product startups.", "technological": "Freddy AI generative engine automating support ticket resolution, predictive agent routing, and conversational customer self-service.", "legal": "Meets international enterprise SOC-2 Type II data security standards, ISO 27001 certifications, and international data privacy statutes.", "environmental": "Cloud-native SaaS deployed on high-efficiency public cloud infrastructure, driving paperless customer support ticketing globally."},
        [0.28, 0.70, 0.58, 0.48, 0.85],
        {"threat_of_new_entrants": "Moderate-low; establishing global distribution, 65,000+ paying business customers, and deep app marketplace integrations takes years.", "bargaining_power_of_buyers": "Moderate-high; mid-market customers demand simple transparent per-agent monthly pricing and easily compare features with Zendesk.", "bargaining_power_of_suppliers": "Moderate; relies on AWS public cloud infrastructure and third-party AI foundation model APIs.", "threat_of_substitutes": "High; Zendesk, ServiceNow (enterprise ITSM), and Salesforce Service Cloud compete aggressively for customer support teams.", "competitive_rivalry": "Fierce; battling Zendesk in customer ticketing and ServiceNow in mid-market IT service management."}
    ),
    (
        "Postman", "Enterprise Software, Cloud & SaaS",
        "software engineering teams, API developers, and enterprise software architects",
        "demand a unified collaborative platform to design, test, mock, document, and monitor REST/GraphQL APIs across developer teams",
        "Postman API Platform & Enterprise Workspaces", "Collaborative API Development & Governance Platform",
        "used by over 30 million software developers worldwide, standardizing the global API development lifecycle with shared team workspaces and automated testing",
        [0.60, 0.82, 0.88, 0.98, 0.74, 0.35],
        {"political": "Global technology standard originating from Bengaluru, demonstrating Indian engineering dominance in fundamental developer tooling.", "economic": "Captures high-margin enterprise SaaS subscription revenues from 98% of Fortune 500 tech teams who depend on Postman daily.", "social": "Deeply embedded in global developer culture, serving as the universal default tool taught in computer science universities worldwide.", "technological": "Industry-leading API testing runtime, automated mock servers, dynamic test scripting, Open API specification integration, and Postbot AI.", "legal": "Complies with global enterprise source code confidentiality agreements, SOC-2 security protocols, and international data privacy rules.", "environmental": "100% digital developer cloud platform, replacing physical API specification binders and manual testing hardware benches."},
        [0.25, 0.65, 0.50, 0.40, 0.75],
        {"threat_of_new_entrants": "Low; massive global developer community, ubiquitous API collection sharing, and deep IDE integrations create immense network effects.", "bargaining_power_of_buyers": "Moderate; individual developers use free tiers, but enterprise engineering leads gladly pay for enterprise security and workspace controls.", "bargaining_power_of_suppliers": "Low; standard public cloud compute and developer workstation distribution.", "threat_of_substitutes": "Moderate; open-source CLI tools (cURL, Insomnia, Swagger) exist, but lack Postman's rich collaborative enterprise governance.", "competitive_rivalry": "Low-to-moderate; uncontested category leader in collaborative API platform tooling globally."}
    ),
    (
        "Hasura", "Enterprise Software, Cloud & SaaS",
        "full-stack application developers, database architects, and enterprise engineering leads",
        "need instant automated GraphQL and REST APIs generated over existing relational databases with fine-grained role-based authorization",
        "Hasura GraphQL Engine & Data Federation", "Instant GraphQL Engine & Unified Data Access API",
        "eliminates months of repetitive backend CRUD coding by auto-generating instant high-performance GraphQL/REST APIs over PostgreSQL, MySQL, and Snowflake",
        [0.60, 0.80, 0.85, 0.98, 0.74, 0.35],
        {"political": "Founded in Bengaluru and San Francisco, showcasing cutting-edge Indian database infrastructure engineering on the global stage.", "economic": "Slashes enterprise application development timelines by 10x, saving millions of dollars in backend engineering wages.", "social": "Empowers frontend and mobile developers to query and manipulate backend enterprise data autonomously without waiting for backend engineers.", "technological": "High-performance Haskell-based compilation engine that compiles GraphQL queries directly into ultra-optimized single SQL queries in milliseconds.", "legal": "Adheres to enterprise data governance, role-based access control (RBAC), and SOC-2 data security compliances.", "environmental": "Radically reduces backend server CPU waste through compile-time SQL query optimization and automated connection pooling."},
        [0.28, 0.65, 0.50, 0.42, 0.75],
        {"threat_of_new_entrants": "Moderate-low; compiling complex nested GraphQL queries into single SQL joins with row-level security requires deep compiler engineering.", "bargaining_power_of_buyers": "Moderate; engineering teams that adopt Hasura find their entire frontend stack architected around its GraphQL schema, creating high retention.", "bargaining_power_of_suppliers": "Low; open-source core with commercial enterprise cloud extensions.", "threat_of_substitutes": "Moderate; custom manual backend APIs (Node.js/Go) or alternative GraphQL engines (Apollo, PostGraphile).", "competitive_rivalry": "Moderate; clear category pioneer and dominant leader in instant database GraphQL engines."}
    ),
    (
        "BrowserStack", "Enterprise Software, Cloud & SaaS",
        "web developers, QA automated test engineers, and mobile app release managers",
        "seek instant cloud access to thousands of real physical mobile devices and desktop browsers to test responsive web layouts and mobile apps",
        "BrowserStack Live, Automate & App Live", "Cloud-Based Real Device Testing Infrastructure",
        "provides on-demand instant access to 3,000+ real physical iOS and Android mobile devices and desktop browsers in the cloud, with zero hardware lab maintenance",
        [0.60, 0.82, 0.86, 0.96, 0.74, 0.38],
        {"political": "Bootstrapped Indian engineering success story, operating global real-device data centers powering 50,000+ international enterprises.", "economic": "Eliminates the millions of dollars companies would spend purchasing, updating, and maintaining physical smartphone testing hardware racks.", "social": "Ensures digital accessibility and bug-free web experiences for billions of global internet users on diverse budget smartphones.", "technological": "Complex proprietary hardware orchestration platform managing thousands of physical smartphones connected to USB hubs with sub-second video streaming.", "legal": "Complies with enterprise remote access security, device data wiping protocols after every test session, and SOC-2 compliance.", "environmental": "Consolidates hardware testing in centralized, energy-efficient device data centers, dramatically reducing electronic gadget waste worldwide."},
        [0.24, 0.65, 0.52, 0.40, 0.75],
        {"threat_of_new_entrants": "Low; physically maintaining, cooling, and automating thousands of real smartphones with custom firmware creates huge logistical moats.", "bargaining_power_of_buyers": "Moderate; QA leaders view BrowserStack as non-negotiable infrastructure for daily continuous integration / continuous deployment (CI/CD).", "bargaining_power_of_suppliers": "Moderate; reliant on purchasing bulk consumer hardware devices from Apple, Samsung, and Google.", "threat_of_substitutes": "Moderate; local software emulators (Android Studio, Xcode simulators) and competing cloud device farms (Sauce Labs).", "competitive_rivalry": "Moderate; dominant global brand recall in real-device cloud testing, competing with Sauce Labs and LambdaTest."}
    ),
    (
        "RateGain Travel Technologies", "Enterprise Software, Cloud & SaaS",
        "global hotel chains, regional airlines, and online travel booking aggregators",
        "need AI-powered dynamic room rate pricing intelligence, automated travel distribution, and social social media marketing optimization",
        "RateGain DaaS & RevGain AI Revenue Management", "AI-Powered Travel & Hospitality SaaS Solutions",
        "processes over 240 billion travel data points annually, empowering hotels and airlines to maximize guest revenue yield with real-time AI pricing intelligence",
        [0.62, 0.84, 0.85, 0.94, 0.75, 0.40],
        {"political": "Active participant in global tourism digitization initiatives, supporting tourism recovery and digital airline distribution standards.", "economic": "Direct beneficiary of the global post-pandemic travel boom, monetizing SaaS subscriptions and distribution transaction volume across 100+ countries.", "social": "Optimizes hotel pricing transparency and availability, helping travel providers match dynamic consumer holiday demand patterns.", "technological": "Proprietary AI revenue management algorithms, high-frequency price web scrapers across 2,000+ booking channels, and automated channel managers.", "legal": "Complies with global travel data regulations, fair consumer pricing disclosures, and international data privacy statutes.", "environmental": "Paperless cloud SaaS helping hospitality operators optimize room occupancy and operational resource allocation."},
        [0.26, 0.65, 0.54, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; managing integrations with 2,000+ global travel channels and petabytes of historical pricing data forms an entrenched moat.", "bargaining_power_of_buyers": "Moderate; hotel chains and airlines evaluate pricing accuracy and ROI, but switching revenue management software causes booking disruptions.", "bargaining_power_of_suppliers": "Low; standard cloud computing and commercial data center architecture.", "threat_of_substitutes": "Moderate; in-house airline yield management systems and hospitality tech providers (Amadeus, Sabre).", "competitive_rivalry": "Moderate-high; competes with IDeaS and SiteMinder in specialized hospitality distribution and revenue intelligence."}
    ),
    (
        "CleverTap", "Enterprise Software, Cloud & SaaS",
        "consumer mobile apps, digital streaming platforms, and e-commerce growth teams",
        "require real-time user behavioral analytics, predictive customer churn modeling, and automated omnichannel push notification campaigns",
        "CleverTap Customer Lifecycle Management & Tesseract DB", "Customer Engagement & Retention Automation SaaS",
        "features a proprietary in-memory database (Tesseract) that processes real-time user actions to trigger hyper-personalized notifications that boost retention by 30%",
        [0.60, 0.82, 0.88, 0.95, 0.75, 0.35],
        {"political": "Founded in Mumbai, powering global consumer engagement across 10,000+ digital applications in Asia, Americas, and Europe.", "economic": "Enables digital consumer apps to maximize customer lifetime value (LTV) and reduce expensive customer acquisition cost (CAC) burn.", "social": "Helps digital apps communicate relevant, timely alerts (flight delays, order updates, medicine reminders) rather than blind spam.", "technological": "Proprietary patented Tesseract database optimized specifically for user journey stream processing with sub-second behavioral segmentation.", "legal": "Strict compliance with mobile OS notification privacy permissions (Apple iOS tracking transparency), GDPR, and Indian DPDP Act.", "environmental": "Cloud-based digital communication algorithms replacing physical paper mailers and printed marketing promotional flyers."},
        [0.30, 0.68, 0.55, 0.45, 0.82],
        {"threat_of_new_entrants": "Moderate-low; building a custom in-memory database capable of processing billions of real-time mobile app events requires deep systems IP.", "bargaining_power_of_buyers": "Moderate; mobile apps compare user retention metrics, but migrating event tracking SDKs requires engineering refactoring.", "bargaining_power_of_suppliers": "Low; cloud infrastructure hosted on AWS and Google Cloud.", "threat_of_substitutes": "Moderate; MoEngage, Braze, and WebEngage provide competing customer engagement automation platforms.", "competitive_rivalry": "Intense; fierce global battle against MoEngage, Braze, and Iterable for leadership in mobile customer lifecycle management."}
    ),
    (
        "MoEngage", "Enterprise Software, Cloud & SaaS",
        "omnichannel consumer retail brands, BFSI mobile apps, and digital telecom operators",
        "seek insight-led customer engagement across web, mobile, WhatsApp, and email with automated predictive AI marketing journeys",
        "MoEngage Sherpa AI & Omnichannel Engagement Suite", "Customer Engagement Platform & Predictive Marketing Automation",
        "delivers AI-powered marketing journey automation (Sherpa AI) that predicts the best time, channel, and content to engage each individual consumer",
        [0.60, 0.82, 0.88, 0.95, 0.75, 0.35],
        {"political": "Rapidly expanding Indian SaaS champion, empowering enterprise brands across 35+ countries in North America, Europe, and Southeast Asia.", "economic": "Captures surging enterprise demand for personalized customer retention, driving higher conversion rates for retail and banking clients.", "social": "Enables thoughtful consumer communication by analyzing real-time intent, eliminating unwanted marketing noise across digital channels.", "technological": "Sherpa AI algorithms for automated message copy generation, predictive churn analysis, and omnichannel messaging orchestration.", "legal": "Adheres to international enterprise data security standards, ISO 27001, SOC-2 Type II, and consumer communication consent guidelines.", "environmental": "Pure digital customer engagement SaaS, operating on energy-efficient cloud servers and eliminating physical direct mail waste."},
        [0.30, 0.68, 0.55, 0.45, 0.82],
        {"threat_of_new_entrants": "Moderate-low; deep mobile SDK integrations across 1,200+ global brands and billions of processed user profiles create strong defensibility.", "bargaining_power_of_buyers": "Moderate; growth marketers demand demonstrable uplift in engagement metrics and evaluate platform pricing per monthly active user (MAU).", "bargaining_power_of_suppliers": "Low; standard public cloud infrastructure.", "threat_of_substitutes": "Moderate; CleverTap, Braze, and Salesforce Marketing Cloud.", "competitive_rivalry": "Fierce; competing head-to-head with CleverTap in Asia-Pacific and with Braze in Western enterprise markets."}
    ),
    (
        "Icertis", "Enterprise Software, Cloud & SaaS",
        "Global Fortune 500 general counsels, chief procurement officers, and enterprise compliance leads",
        "demand AI-driven contract lifecycle management (CLM) to surface contractual risks, automate compliance, and accelerate revenue closing",
        "Icertis Contract Intelligence (ICI) Platform", "Enterprise Contract Intelligence & Risk Governance",
        "transforms static paper contracts into strategic enterprise assets, using generative AI to analyze contract obligations and ensure regulatory compliance",
        [0.65, 0.85, 0.86, 0.96, 0.82, 0.35],
        {"political": "Trusted by multinational defense contractors, healthcare giants, and government bodies to govern mission-critical enterprise contracts.", "economic": "Protects billions of dollars in enterprise contract leakage, penalty liabilities, and missed procurement rebate discounts for Global 2000 firms.", "social": "Brings transparency and legal clarity to commercial agreements, ensuring fair labor standards and ethical supplier commitments.", "technological": "Pioneered Icertis Contract Intelligence (ICI) integrating generative AI models with proprietary enterprise contract graph databases.", "legal": "Strict adherence to international corporate law, electronic signature legality, Sarbanes-Oxley audit trails, and global data privacy.", "environmental": "Eliminates millions of physical printed legal agreements, paper redlines, and courier shipments across global corporate operations."},
        [0.22, 0.65, 0.52, 0.38, 0.78],
        {"threat_of_new_entrants": "Very low; enterprise-wide legal contract data is hyper-sensitive; establishing multi-decade trust with Fortune 500 legal teams creates an insurmountable moat.", "bargaining_power_of_buyers": "Moderate; Global 2000 enterprises pay premium annual licenses because contract errors or compliance lapses cost orders of magnitude more.", "bargaining_power_of_suppliers": "Low; strategic technical alliances with Microsoft Azure and SAP provide deep cloud distribution.", "threat_of_substitutes": "Moderate; generic document management systems and emerging legal-tech startups, but none match Icertis's enterprise scale.", "competitive_rivalry": "Low-to-moderate; recognized as the global market leader in enterprise Contract Lifecycle Management alongside DocuSign CLM."}
    ),
    (
        "LeadSquared (MarketXpander Services)", "Enterprise Software, Cloud & SaaS",
        "high-velocity sales teams, higher education admissions, and financial lending field forces",
        "require rapid lead distribution, automated field sales rep tracking, and high-velocity conversion pipeline automation",
        "LeadSquared Sales Execution CRM & Field Force Automation", "High-Velocity Sales Execution & Field Force Automation CRM",
        "built specifically to accelerate high-velocity sales pipelines, eliminating lead leakage with zero-wait lead distribution and mobile field force tracking",
        [0.60, 0.84, 0.86, 0.92, 0.75, 0.35],
        {"political": "Supports digital sales operations across Indian higher education institutions, financial services, and healthcare clinics.", "economic": "Powers sales execution for over 2,000 businesses, driving accelerated lead conversion and reduced sales onboarding cycles.", "social": "Empowers frontline sales agents with transparent mobile workflows, automated call logging, and instant performance recognition.", "technological": "Proprietary sales execution engine with visual workflow automation, geo-fenced mobile check-ins for field reps, and dialer integration.", "legal": "Complies with Indian TRAI tele-calling guidelines, consumer communication privacy laws, and international data security standards.", "environmental": "Paperless digital lead capture and automated digital document collection, eliminating manual physical application forms."},
        [0.28, 0.68, 0.54, 0.44, 0.80],
        {"threat_of_new_entrants": "Moderate-low; deep vertical specialization in education admissions and lending field operations creates defensible moats.", "bargaining_power_of_buyers": "Moderate; sales leaders value measurable sales conversion velocity gains over generic CRM platforms.", "bargaining_power_of_suppliers": "Low; cloud infrastructure hosted on AWS.", "threat_of_substitutes": "Moderate; general-purpose CRMs like Salesforce, Zoho CRM, and HubSpot compete for enterprise sales budgets.", "competitive_rivalry": "Moderate-high; dominates high-velocity Indian education and lending sales against generic global CRM tools."}
    ),
    (
        "Darwinbox", "Enterprise Software, Cloud & SaaS",
        "multinational enterprises across Asia, corporate HR leaders, and distributed workforces",
        "need an agile, mobile-first Human Capital Management (HCM) platform tailored for Asian organizational structures and multi-country payroll",
        "Darwinbox Enterprise HCM & Talent Management", "Mobile-First Enterprise Human Capital Management (HCM)",
        "features an intuitive consumer-grade mobile app for employees, voice-enabled leave applications, automated multi-country payroll, and talent intelligence",
        [0.62, 0.84, 0.88, 0.94, 0.78, 0.36],
        {"political": "Asian SaaS unicorn headquartered in Hyderabad, empowering regional conglomerates across India, Southeast Asia, and the Middle East.", "economic": "Replaces rigid Western legacy HR software (SAP SuccessFactors, Oracle) with a flexible cloud platform that costs 40% less.", "social": "Humanizes enterprise workforce management, providing front-line factory workers and corporate executives with equal mobile access to HR services.", "technological": "Voice-first mobile interface (Darwinbox Assistant), facial recognition attendance tracking, and predictive employee attrition AI models.", "legal": "Complies with diverse national labor codes, statutory provident fund (PF) regulations, tax deductions, and regional data residency laws.", "environmental": "Eliminates paper salary slips, physical performance appraisal forms, and paper employee onboarding files across 850+ enterprises."},
        [0.25, 0.68, 0.52, 0.42, 0.82],
        {"threat_of_new_entrants": "Low; building comprehensive localized payroll engines across 100+ countries with statutory compliance forms steep barriers.", "bargaining_power_of_buyers": "Moderate; enterprise HR teams choose Darwinbox for superior employee mobile adoption, but enterprise procurement negotiates firmly.", "bargaining_power_of_suppliers": "Low; cloud architecture deployed on modern public cloud platforms.", "threat_of_substitutes": "Moderate; global legacy enterprise giants (Workday, SAP SuccessFactors, Oracle HCM) and mid-market HR software.", "competitive_rivalry": "High; competing fiercely against Workday and SAP in large Asian enterprise accounts."}
    ),
    (
        "InMobi (Glance InMobi Group)", "Enterprise Software, Cloud & SaaS",
        "global brand advertisers, mobile app publishers, and smartphone consumers",
        "demand programmatic mobile ad monetization, interactive rich-media creative campaigns, and lock-screen content discovery",
        "InMobi Advertising Exchange & Glance Smart Lock Screen", "Mobile Advertising Exchange & Lock-Screen Discovery Platform",
        "pioneers the Glance AI smart lock screen serving 250M+ active users, alongside a global programmatic ad exchange reaching 2B+ mobile devices",
        [0.64, 0.85, 0.90, 0.96, 0.78, 0.36],
        {"political": "India's first tech unicorn, representing domestic artificial intelligence and digital advertising innovation on the global stage.", "economic": "Generates hundreds of millions in programmatic advertising revenue, monetizing high-intent mobile smartphone attention globally.", "social": "Transformed inert smartphone lock screens into dynamic AI-curated surfaces for news, live gaming, and short-form entertainment.", "technological": "Real-time programmatic bidding engine handling 100B+ daily ad auctions, on-device AI content recommendation, and interactive rich media.", "legal": "Adheres to mobile operating system privacy frameworks (Apple IDFA restrictions), GDPR, and Indian DPDP consumer consent regulations.", "environmental": "Pure digital media and software discovery platform operating on efficient cloud computing infrastructure."},
        [0.28, 0.68, 0.60, 0.46, 0.84],
        {"threat_of_new_entrants": "Low; exclusive pre-installed lock-screen partnership agreements with major smartphone OEMs (Samsung, Xiaomi) create massive moats.", "bargaining_power_of_buyers": "Moderate-high; global ad agencies and brands demand verified click-through attribution and brand-safe inventory.", "bargaining_power_of_suppliers": "High; dependent on mobile operating systems and hardware smartphone manufacturer distribution alliances.", "threat_of_substitutes": "High; Google Ads, Meta Ads, and TikTok command dominant shares of global digital advertising budgets.", "competitive_rivalry": "Fierce; battling global ad-tech giants and programmatic supply-side platforms (The Trade Desk, Criteo) for brand advertiser budgets."}
    ),
    (
        "Gupshup", "Enterprise Software, Cloud & SaaS",
        "banks, retail e-commerce brands, and customer engagement managers",
        "seek conversational AI commerce, automated WhatsApp business messaging chatbots, and instant customer service interaction",
        "Gupshup Conversation Cloud & Bot Studio", "Conversational AI & WhatsApp Commerce Platform",
        "processes over 10 billion conversational messages monthly, enabling businesses to sell products, issue tickets, and resolve support directly within WhatsApp",
        [0.64, 0.84, 0.88, 0.94, 0.78, 0.36],
        {"political": "Supports digital commerce democratization under the Open Network for Digital Commerce (ONDC) via conversational WhatsApp shopping.", "economic": "Monetizes transactional conversational commerce fees, transforming everyday messaging apps into active revenue-generating storefronts.", "social": "Allows everyday Indian consumers who cannot navigate complex websites to purchase bus tickets and order groceries through natural chat.", "technological": "Domain-specific conversational generative AI models, low-code Bot Studio for automated workflow creation, and WhatsApp multi-agent routing.", "legal": "Strict compliance with telecommunications messaging guidelines, Meta WhatsApp Business policies, and financial data security rules.", "environmental": "Paperless conversational billing and electronic receipt delivery, eliminating physical paper brochures and transaction slips."},
        [0.28, 0.68, 0.62, 0.46, 0.82],
        {"threat_of_new_entrants": "Moderate-low; official WhatsApp Business Solution Provider (BSP) status and enterprise carrier relationships create high moats.", "bargaining_power_of_buyers": "Moderate-high; enterprise marketing teams compare per-conversation messaging pricing across competing conversational platforms.", "bargaining_power_of_suppliers": "High; fundamentally dependent on Meta's WhatsApp Business platform pricing policies and API terms.", "threat_of_substitutes": "Moderate; mobile apps, SMS messaging, and traditional website storefronts.", "competitive_rivalry": "High; competing against Yellow.ai, Haptik, and global CPaaS platforms in enterprise conversational commerce."}
    ),
    (
        "Chargebee", "Enterprise Software, Cloud & SaaS",
        "high-growth SaaS founders, subscription app operators, and enterprise finance controllers",
        "need automated recurring subscription billing, multi-currency invoicing, and GAAP-compliant revenue recognition",
        "Chargebee Subscription Management & Retention Platform", "Subscription Billing & Recurring Revenue Management SaaS",
        "automates complex recurring billing workflows, handles global tax compliance in 100+ countries, and reduces involuntary churn with automated dunning",
        [0.62, 0.84, 0.86, 0.95, 0.76, 0.35],
        {"political": "Founded in Chennai, operating global subscription billing infrastructure powering thousands of fast-growing internet businesses worldwide.", "economic": "Vital financial infrastructure capturing recurring subscription transaction volume across global software and e-commerce companies.", "social": "Enables small indie software developers and scaling startups to monetize software products globally without building complex billing logic.", "technological": "Flexible subscription lifecycle engine supporting usage-based pricing, multi-gateway failover, and automated revenue recognition (ASC 606).", "legal": "Meets international accounting standards (IFRS 15, ASC 606), PCI-DSS Level 1 compliance, and global sales tax / VAT calculations.", "environmental": "Pure digital financial billing software eliminating paper invoicing, postal mailings, and manual bookkeeping."},
        [0.26, 0.65, 0.52, 0.42, 0.80],
        {"threat_of_new_entrants": "Low; complex tax rules across 100+ countries, accounting compliance certifications, and payment gateway connections form deep moats.", "bargaining_power_of_buyers": "Moderate; once a company's subscription billing is integrated into Chargebee, switching costs are exceptionally high.", "bargaining_power_of_suppliers": "Low; standard cloud computing and payment gateway APIs.", "threat_of_substitutes": "Moderate; Stripe Billing and Recurly offer competing subscription management solutions.", "competitive_rivalry": "Moderate-high; competes primarily against Stripe Billing and Recurly for fast-growing global subscription businesses."}
    ),
    (
        "Kissflow", "Enterprise Software, Cloud & SaaS",
        "business operations managers, enterprise department heads, and non-technical workflow leads",
        "seek intuitive no-code workflow automation to streamline internal procurement approvals, HR onboarding, and operational requests",
        "Kissflow Work Platform & Low-Code Suite", "No-Code Digital Workplace & Workflow Automation",
        "democratizes business process automation, allowing non-technical business users to build automated workflow approval apps in minutes without coding",
        [0.60, 0.82, 0.85, 0.93, 0.75, 0.35],
        {"political": "Pioneering Chennai SaaS enterprise, demonstrating that world-class no-code workflow software can be built from non-metro Indian talent.", "economic": "Helps global enterprises eliminate internal operational bottlenecks, saving thousands of employee hours spent chasing email approvals.", "social": "Empowers business professionals ('citizen developers') to solve their own software problems without waiting for backlogged IT departments.", "technological": "Visual drag-and-drop process builder, dynamic rule-based routing, contextual collaboration boards, and mobile approval notifications.", "legal": "Complies with enterprise audit trail requirements, SOC-2 security protocols, and international customer data privacy standards.", "environmental": "Completely eliminates physical paper approval routing slips, paper expense vouchers, and printed purchase requisitions."},
        [0.32, 0.68, 0.50, 0.46, 0.80],
        {"threat_of_new_entrants": "Moderate-low; 10,000+ customer deployments, mature workflow engine, and trusted global brand recall create stability.", "bargaining_power_of_buyers": "Moderate; operations managers appreciate Kissflow's simplicity compared to complex enterprise platforms like ServiceNow.", "bargaining_power_of_suppliers": "Low; public cloud infrastructure hosted on Google Cloud.", "threat_of_substitutes": "Moderate-high; Monday.com, Asana, and Microsoft Power Automate compete for digital workplace automation.", "competitive_rivalry": "High; competing against Monday.com, Smartsheet, and Microsoft Power Apps in the global work management space."}
    ),
    (
        "Wingify (VWO)", "Enterprise Software, Cloud & SaaS",
        "digital product managers, e-commerce marketers, and conversion rate optimization (CRO) specialists",
        "need fast, reliable A/B testing, website heatmaps, and user session recordings to maximize online checkout conversion rates",
        "VWO Testing, Insights & Personalization Platform", "A/B Testing & Experience Optimization Platform",
        "empowers companies to run scientific A/B tests on websites without engineering dependencies, analyzing user behavior with heatmaps to boost sales conversion",
        [0.60, 0.82, 0.85, 0.94, 0.74, 0.35],
        {"political": "Bootstrapped Indian software pioneer founded by Paras Chopra in New Delhi, serving Fortune 500 brands in 90+ countries without VC funding.", "economic": "Delivers extraordinary ROI to e-commerce and SaaS brands by finding small conversion rate improvements that unlock millions in sales.", "social": "Championed scientific, data-driven decision making over subjective corporate guesswork in website design and product development.", "technological": "Ultra-lightweight JavaScript tracking snippet with asynchronous execution preventing website slowdown, integrated with full-stack server-side testing.", "legal": "Strictly adheres to user privacy standards, cookie consent rules, GDPR, and anonymized session recordings without capturing sensitive PII.", "environmental": "Pure digital software optimization platform operating on clean cloud data centers."},
        [0.28, 0.65, 0.50, 0.44, 0.78],
        {"threat_of_new_entrants": "Moderate-low; complex asynchronous JavaScript execution without page flickering and statistical confidence engines form moats.", "bargaining_power_of_buyers": "Moderate; digital marketers benchmark VWO pricing against Optimizely and appreciate VWO's integrated insights suite.", "bargaining_power_of_suppliers": "Low; standard cloud computing and global CDN edge infrastructure.", "threat_of_substitutes": "Moderate; Optimizely, Adobe Target, and open-source testing tools.", "competitive_rivalry": "Moderate; dominant global challenger against Optimizely, winning customers with superior ease of use and integrated user behavior analytics."}
    ),
    (
        "Entropik Tech", "Enterprise Software, Cloud & SaaS",
        "global consumer brands, media agencies, and UX design researchers",
        "seek emotion AI and neuromarketing insights to measure subconscious consumer attention and facial micro-expressions during video ads and product tests",
        "Entropik Qatalyst & Decode Neuromarketing AI", "Emotion AI & Neuromarketing Research SaaS",
        "world leader in Emotion AI, utilizing webcam-based eye-tracking, facial expression coding, and voice tonality analysis to quantify human emotional responses",
        [0.62, 0.82, 0.86, 0.96, 0.75, 0.35],
        {"political": "Founded in Bengaluru, holding 40+ global emotion AI patents and representing Indian deep-tech cognitive computing leadership.", "economic": "Helps global consumer brands (P&G, Unilever) optimize multi-million dollar ad campaigns before public launch, ensuring maximum ROI.", "social": "Deepens scientific understanding of human-computer interaction, helping media creators design content that genuinely resonates with audiences.", "technological": "Deep neural networks trained on millions of facial emotion data points, real-time eye-gaze tracking via consumer webcams, and voice analysis.", "legal": "Complies with strict biometric data privacy regulations, explicit user opt-in consent for webcam research, and GDPR compliance.", "environmental": "Replaces expensive physical consumer focus group facilities and international travel with remote digital webcam studies."},
        [0.24, 0.65, 0.52, 0.40, 0.75],
        {"threat_of_new_entrants": "Low; patented computer vision algorithms, massive proprietary emotion training datasets, and scientific credibility form deep moats.", "bargaining_power_of_buyers": "Moderate; consumer insight heads pay premium SaaS subscription fees for quantifiable, objective neuromarketing metrics.", "bargaining_power_of_suppliers": "Low; proprietary machine learning software deployed on cloud GPU instances.", "threat_of_substitutes": "Low-to-moderate; traditional subjective qualitative surveys and manual focus groups lack subconscious biometric precision.", "competitive_rivalry": "Low-to-moderate; recognized as an elite global pioneer in consumer Emotion AI alongside Affectiva."}
    ),
    (
        "Druva Data Solutions", "Enterprise Software, Cloud & SaaS",
        "enterprise CISOs, IT infrastructure directors, and corporate risk officers",
        "demand 100% SaaS cloud data protection, automated ransomware recovery, and centralized backup across endpoints, Microsoft 365, and AWS",
        "Druva Data Resiliency Cloud", "Cloud-Native Enterprise Data Protection & Cyber Resilience",
        "pioneered 100% serverless cloud data protection, enabling enterprises to backup and instantly recover petabytes of corporate data from ransomware attacks",
        [0.64, 0.84, 0.86, 0.96, 0.78, 0.40],
        {"political": "Founded in Pune and Silicon Valley, protecting mission-critical corporate data for over 5,000 global enterprises.", "economic": "Generates predictable high-margin recurring enterprise SaaS revenues, benefiting from surging corporate spending on ransomware defense.", "social": "Protects modern remote and hybrid corporate workforces from devastating data loss caused by lost laptops or sophisticated cybercrime.", "technological": "Serverless cloud-native architecture built entirely on AWS, featuring global data deduplication, air-gapped immutable backups, and AI recovery.", "legal": "Complies with stringent enterprise compliance standards (SOC-2, HIPAA, FedRAMP, GDPR) and legal hold discovery requirements.", "environmental": "Eliminates on-premise enterprise backup tape libraries, cooling power waste, and dedicated secondary physical recovery data centers."},
        [0.22, 0.65, 0.52, 0.40, 0.80],
        {"threat_of_new_entrants": "Low; building an enterprise-grade cloud backup platform capable of protecting exabytes of data with air-gapped security takes years.", "bargaining_power_of_buyers": "Moderate; enterprise CISOs prioritize data recoverability and compliance track records over small software pricing differences.", "bargaining_power_of_suppliers": "Moderate; heavily integrated with Amazon Web Services (AWS) as the underlying cloud infrastructure partner.", "threat_of_substitutes": "Moderate; legacy on-premises backup vendors (Commvault, Veritas) and cloud competitors (Veeam, Rubrik, Cohesity).", "competitive_rivalry": "High; competing fiercely against Rubrik, Cohesity, and Veeam for enterprise cloud data resilience dominance."}
    ),
    (
        "Whatfix (Quickwork Technologies)", "Enterprise Software, Cloud & SaaS",
        "enterprise CIOs, digital transformation leaders, and corporate training heads",
        "seek automated in-app interactive guidance tours, step-by-step software task walkthroughs, and user onboarding acceleration",
        "Whatfix Digital Adoption Platform (DAP)", "Digital Adoption Solutions & In-App User Guidance",
        "overlays interactive real-time guidance on any enterprise software (Salesforce, SAP, Workday), cutting employee training time by 60% and eliminating support tickets",
        [0.60, 0.82, 0.85, 0.94, 0.74, 0.35],
        {"political": "Founded in Bengaluru, driving digital employee productivity across hundreds of Global Fortune 1000 enterprises.", "economic": "Maximizes enterprise software ROI, ensuring expensive ERP and CRM investments are fully adopted rather than abandoned by employees.", "social": "Reduces software anxiety and cognitive fatigue for non-technical employees navigating complex modern corporate software interfaces.", "technological": "No-code contextual interactive overlay technology, automated cross-application journey tracking, and AI product analytics.", "legal": "Complies with enterprise security protocols, zero-data logging of sensitive customer input fields, and international data privacy statutes.", "environmental": "Eliminates physical corporate software training manuals, in-person training travel, and printed workflow documentation."},
        [0.26, 0.65, 0.52, 0.42, 0.78],
        {"threat_of_new_entrants": "Moderate-low; patented in-app DOM manipulation engines, enterprise security clearances, and deep integrations form moats.", "bargaining_power_of_buyers": "Moderate; enterprise CIOs evaluate user adoption metrics, but appreciate Whatfix's responsive customer support.", "bargaining_power_of_suppliers": "Low; cloud architecture hosted on leading cloud providers.", "threat_of_substitutes": "Moderate; WalkMe and Pendo offer competing digital adoption platforms.", "competitive_rivalry": "Intense head-to-head competition against WalkMe for leadership in global enterprise digital adoption solutions."}
    ),
    (
        "HighRadius Corporation", "Enterprise Software, Cloud & SaaS",
        "enterprise CFOs, corporate treasurers, and credit risk managers",
        "require autonomous finance software to automate accounts receivable, cash application, credit risk underwriting, and treasury management",
        "HighRadius Autonomous Finance Platform", "Autonomous Accounts Receivable & Treasury Management SaaS",
        "processes over $7.7 trillion in business transactions annually, using machine learning to automate order-to-cash and treasury operations",
        [0.64, 0.85, 0.86, 0.96, 0.78, 0.35],
        {"political": "Founded in Hyderabad and Houston, representing elite Indian enterprise financial technology innovation in Global Fortune 500 finance departments.", "economic": "Slashes days sales outstanding (DSO) by 20% and automates 90%+ of manual cash reconciliations for global blue-chip clients.", "social": "Transforms corporate accounting teams from mundane manual spreadsheet data-entry clerks into strategic cash-flow advisors.", "technological": "Proprietary machine learning models trained on trillions of historical B2B payment behaviors, automated bank invoice matching, and credit AI.", "legal": "Strict adherence to Sarbanes-Oxley internal financial control audits, banking data security standards, and international compliance.", "environmental": "Drives end-to-end digital electronic billing and automated reconciliations, eliminating paper checks and postal statements."},
        [0.22, 0.65, 0.50, 0.38, 0.78],
        {"threat_of_new_entrants": "Low; managing sensitive multi-billion dollar corporate cash applications requires unshakeable enterprise trust and deep ERP integrations.", "bargaining_power_of_buyers": "Moderate; enterprise CFOs pay high SaaS fees because automated cash recovery directly expands working capital by millions.", "bargaining_power_of_suppliers": "Low; cloud infrastructure deployed on Microsoft Azure and AWS.", "threat_of_substitutes": "Low-to-moderate; legacy ERP cash modules (SAP, Oracle) lack HighRadius's autonomous machine learning capabilities.", "competitive_rivalry": "Low-to-moderate; clear global category leader in Autonomous Finance and Order-to-Cash software."}
    ),
    (
        "Zenoti (Sovalabs Software)", "Enterprise Software, Cloud & SaaS",
        "luxury spa chains, premium salon franchises, and medical spa networks",
        "need an all-in-one cloud management software to automate appointment bookings, multi-location point-of-sale, staff commissions, and guest loyalty",
        "Zenoti Salon & Spa Management Cloud", "Specialized Spa, Salon & Wellness Enterprise Software",
        "world's premier cloud platform for the beauty and wellness industry, powering 25,000+ businesses across 50 countries with seamless mobile checkouts",
        [0.60, 0.84, 0.88, 0.94, 0.75, 0.35],
        {"political": "Founded in Hyderabad and Seattle, showcasing specialized vertical SaaS excellence built by seasoned Indian enterprise software veterans.", "economic": "Drives recurring SaaS subscriptions and payment processing fees across premier luxury wellness chains worldwide.", "social": "Empowers salon stylists and spa therapists with mobile appointment calendars, transparent commission tracking, and digital tips.", "technological": "Consumer mobile booking apps, AI smart scheduling to maximize chair utilization, touchless check-in, and automated inventory replenishment.", "legal": "Complies with international PCI-DSS payment compliance, customer data privacy regulations, and regional tip taxation laws.", "environmental": "Paperless salon operations, eliminating physical appointment books, printed receipts, and plastic gift cards."},
        [0.25, 0.65, 0.52, 0.40, 0.78],
        {"threat_of_new_entrants": "Low; deep specialized domain features (chair scheduling, tip splitting, medical consent forms) create strong vertical moats.", "bargaining_power_of_buyers": "Moderate; enterprise salon chains (Toni&Guy, Massage Heights) rarely switch because core daily operations run entirely on Zenoti.", "bargaining_power_of_suppliers": "Low; cloud software hosted on AWS and Microsoft Azure.", "threat_of_substitutes": "Moderate; generic POS systems (Square, Toast) lack the specialized appointment and commission rules of beauty businesses.", "competitive_rivalry": "Moderate; dominant global category leader in multi-location enterprise salon and spa management software."}
    ),
    (
        "Ameyo (Drishti-Soft Solutions)", "Enterprise Software, Cloud & SaaS",
        "contact center operators, customer experience directors, and customer support BPOs",
        "seek omnichannel contact center software, conversational IVR, intelligent automatic call distribution (ACD), and predictive auto-dialers",
        "Ameyo Contact Center Suite & Video KYC Platform", "Omnichannel Contact Center Software & Customer Experience",
        "powers mission-critical customer interactions across 2,000+ enterprises in 60 countries, delivering high-performance predictive dialers and video KYC",
        [0.62, 0.82, 0.86, 0.93, 0.76, 0.36],
        {"political": "Supports government citizen grievance helplines and domestic BFSI customer support infrastructure under digital India initiatives.", "economic": "Lowers customer interaction costs for banks and e-commerce companies by routing inquiries to optimal voice and digital channels.", "social": "Improves customer resolution times for citizens reaching out for emergency services, banking help, or e-commerce delivery updates.", "technological": "High-density computer telephony integration (CTI), WebRTC in-browser agent desktops, and AI sentiment analysis on live voice calls.", "legal": "Strict compliance with DoT telecommunications regulations, TRAI call recording mandates, and banking customer data confidentiality.", "environmental": "Cloud contact center software enabling remote work-from-home agents, eliminating office commute emissions."},
        [0.28, 0.68, 0.55, 0.45, 0.80],
        {"threat_of_new_entrants": "Moderate-low; complex telecommunications carrier protocol integration and regulatory compliance create solid barriers.", "bargaining_power_of_buyers": "Moderate-high; BPO and enterprise contact centers negotiate aggressively on per-agent seat licensing costs.", "bargaining_power_of_suppliers": "Moderate; dependent on underlying telecommunications bandwidth and cloud VoIP trunk providers.", "threat_of_substitutes": "Moderate; global cloud contact center platforms (Genesys, Five9, Talkdesk) compete for enterprise deals.", "competitive_rivalry": "High; competes against Exotel, Knowlarity, and global contact center software providers in emerging markets."}
    )
]

for item in sector5_data:
    add_c(*item)

print(f"Sector 5 added: {len(sector5_data)} companies. Total: {len(comps)}")

# ==============================================================================
# SECTOR 6: Pharmaceuticals & Active Pharmaceutical Ingredients (22 companies)
# ==============================================================================
sector6_data = [
    (
        "Sun Pharmaceutical Industries", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "global chronic patients, dermatologists, and healthcare systems",
        "demand affordable, high-quality specialty branded formulations for complex dermatological, ophthalmological, and oncology conditions",
        "Ilumya (Tildrakizumab) & Specialty Dermatology Portfolio", "Specialty Branded Formulations & Global Generics",
        "India's largest pharmaceutical company, delivering FDA-approved novel biologics for plaque psoriasis, specialty eye care, and generic medicines across 100+ countries",
        [0.72, 0.86, 0.94, 0.90, 0.85, 0.65],
        {"political": "Vital strategic asset supporting India's title as 'Pharmacy of the World'; active participant in national Bulk Drug and Pharma PLI schemes.", "economic": "Generates multi-billion dollar export revenues, successfully pivoting from commoditized generics to high-margin proprietary specialty biologics.", "social": "Provides affordable life-saving medications for chronic cardiovascular, diabetes, and neurological diseases to millions of Indian families.", "technological": "State-of-the-art R&D centers in Vadodara and Gurugram filing hundreds of international patents annually in complex drug delivery systems.", "legal": "Meets rigorous US FDA cGMP manufacturing standards, European EMA inspections, and Indian CDSCO drug price control regulations (DPCO).", "environmental": "Zero Liquid Discharge (ZLD) effluent treatment across manufacturing facilities, recycling millions of liters of industrial water."},
        [0.20, 0.65, 0.52, 0.40, 0.82],
        {"threat_of_new_entrants": "Very low; multi-hundred million dollar clinical trials, global regulatory approvals, and massive chemical synthesis plants form insurmountable moats.", "bargaining_power_of_buyers": "Moderate-low; proprietary specialty branded drugs (Ilumya) command significant pricing power from healthcare insurers.", "bargaining_power_of_suppliers": "Low-to-moderate; vertically integrated with in-house active pharmaceutical ingredient (API) manufacturing plants.", "threat_of_substitutes": "Low-to-moderate; alternative branded formulations exist, but specialty biologics have limited direct substitutes.", "competitive_rivalry": "Moderate-high; competes globally with Teva, Viatris, and Novartis in generics, and AbbVie in dermatology."}
    ),
    (
        "Dr. Reddy's Laboratories", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "global healthcare providers, cancer patients, and retail pharmacies",
        "need affordable biosimilars, complex oncology injectables, and reliable global supply of active pharmaceutical ingredients",
        "Peg-grafeel Biosimilar & Oncology Injectables", "Biosimilars, Complex Generics & Active Pharmaceutical Ingredients",
        "pioneers affordable biosimilar oncology therapies, complex injectable manufacturing, and trusted bulk active ingredients across 66 global markets",
        [0.70, 0.85, 0.92, 0.92, 0.84, 0.68],
        {"political": "Deeply engaged in international health diplomacy, supplying affordable medicines across emerging markets in Russia, CIS, and LatAm.", "economic": "Maintains a high-margin portfolio of Para-IV first-to-file generic drug opportunities in the US market, funding long-term biosimilar R&D.", "social": "Founded by visionary Dr. K. Anji Reddy with the mission of making life-saving medicines accessible to the poorest cancer patients.", "technological": "Pioneering continuous bioprocessing for monoclonal antibodies, complex synthetic peptide chemistry, and AI-driven molecular modeling.", "legal": "Adheres to US FDA 21 CFR Part 211 cGMP standards, complex patent litigation settlements, and international intellectual property law.", "environmental": "Committed to 100% renewable power by 2030, recognized as a global sustainability leader in pharmaceutical chemical manufacturing."},
        [0.22, 0.65, 0.54, 0.40, 0.82],
        {"threat_of_new_entrants": "Low; developing complex sterile injectables and biosimilar cell-lines requires specialized cleanrooms and multi-year regulatory testing.", "bargaining_power_of_buyers": "Moderate; US pharmacy benefit managers negotiate aggressively, but biosimilar oncology therapies enjoy strong pricing resilience.", "bargaining_power_of_suppliers": "Moderate; backward integration into bulk chemical intermediates mitigates raw material supply chain shocks.", "threat_of_substitutes": "Low-to-moderate; biosimilar biologics have virtually zero therapeutic substitutes for treating severe autoimmune and cancer indications.", "competitive_rivalry": "High; competing against Sun Pharma, Cipla, and global generic giants in high-value sterile injectables."}
    ),
    (
        "Cipla Limited", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "asthma patients, respiratory care specialists, and developing world healthcare programs",
        "seek affordable metered-dose inhalers, high-efficacy respiratory treatments, and equitable access to life-saving antiretrovirals",
        "Foracort, Seroflo Inhalers & Generic ARV Therapies", "Respiratory Formulations & Global Public Health Therapeutics",
        "world leader in affordable respiratory inhalers, famous for democratizing HIV treatment globally and offering unmatched aerosol drug delivery technology",
        [0.70, 0.85, 0.95, 0.90, 0.82, 0.65],
        {"political": "Global humanitarian reputation established by Dr. Y.K. Hamied providing $1-a-day HIV drugs to Africa; active champion of affordable medicines.", "economic": "Enjoys commanding domestic market leadership in chronic respiratory care with over 65% market share in Indian inhalers.", "social": "Deeply revered by Indian doctors and chronic asthma patients, championing clean lung health via public awareness campaigns (Breathefree).", "technological": "World-class aerodynamic device engineering for Dry Powder Inhalers (DPI) and pressurized Metered Dose Inhalers (pMDI) with sub-micron particle control.", "legal": "Complies with CDSCO national essential medicines lists, global patent opposition mechanisms, and US FDA inhalation device standards.", "environmental": "Pioneering the transition to eco-friendly medical propellants with near-zero Global Warming Potential (GWP) across all consumer inhalers."},
        [0.22, 0.62, 0.50, 0.38, 0.80],
        {"threat_of_new_entrants": "Very low; precision aerosol engineering, plastic valve tooling, and pulmonary deposition clinical trials form impenetrable moats.", "bargaining_power_of_buyers": "Low-to-moderate; chronic asthma and COPD patients develop intense brand loyalty to specific inhaler mouthpieces and dosing counters.", "bargaining_power_of_suppliers": "Low-to-moderate; high internal backward integration into active drug substances (budesonide, formoterol).", "threat_of_substitutes": "Low; inhalation is the gold-standard medical therapy for obstructive airway diseases with no oral substitute matching its direct lung efficacy.", "competitive_rivalry": "Moderate; dominant near-monopoly in domestic respiratory care, competing globally with GSK and AstraZeneca."}
    ),
    (
        "Lupin Limited", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "cardiovascular patients, pediatric specialists, and international anti-tuberculosis programs",
        "demand reliable global supply of anti-TB therapies, complex generic inhalation aerosols, and cardiovascular branded formulations",
        "Lupihaler Respiratory Portfolio & Global Anti-TB Range", "Cardiovascular, Respiratory & Anti-Infective Therapeutics",
        "world's largest manufacturer of anti-tuberculosis active drugs, with a fast-growing global portfolio of complex generic injectables and inhalation products",
        [0.68, 0.84, 0.92, 0.88, 0.82, 0.62],
        {"political": "Crucial partner to World Health Organization (WHO) and government health ministries in global campaigns to eradicate tuberculosis.", "economic": "Balances steady domestic formulation sales across cardiovascular and diabetes therapies with US generic market revenues.", "social": "Safeguards millions of underprivileged families worldwide from infectious tuberculosis and chronic cardiovascular diseases.", "technological": "High-containment fermentation plants, advanced pulmonary drug formulation capabilities, and automated sterile injectable manufacturing.", "legal": "Complies with stringent US FDA warning letter resolution audits, WHO pre-qualification standards, and Indian drug price controls.", "environmental": "Invests in zero liquid discharge wastewater treatment and solvent recovery systems across Pithampur, Tarapur, and Ankleshwar plants."},
        [0.24, 0.66, 0.54, 0.40, 0.82],
        {"threat_of_new_entrants": "Low; massive specialized chemical fermentation infrastructure and global health tender pre-qualifications protect market position.", "bargaining_power_of_buyers": "Moderate-high; institutional public health agencies (WHO, PAHO) procure anti-TB medications via competitive tenders.", "bargaining_power_of_suppliers": "Low-to-moderate; strong domestic API synthesis capabilities limit external vendor dependency.", "threat_of_substitutes": "Low-to-moderate; standard multi-drug antibiotic regimens for TB have established clinical protocol guidelines.", "competitive_rivalry": "High; competing against Cipla, Sun Pharma, and global generic manufacturers in respiratory and cardiovascular therapy segments."}
    ),
    (
        "Torrent Pharmaceuticals", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "cardiologists, psychiatrists, and chronic care patients managing lifelong conditions",
        "need trusted, high-potency branded prescription medications for hypertension, cardiovascular health, and central nervous system (CNS) disorders",
        "Chymoral Forte, Losar & Shelcal Formulations", "Specialized Chronic Cardiovascular & CNS Formulations",
        "delivers over 75% of revenues from high-margin chronic and sub-chronic therapies, backed by deep doctor relationships and pristine brand trust",
        [0.66, 0.86, 0.90, 0.88, 0.82, 0.60],
        {"political": "Supports domestic healthcare resilience and Make in India pharmaceutical manufacturing; engages on national drug price control policies.", "economic": "Commands superior operational margins due to high chronic prescription share, insulating revenues from short-term acute illness fluctuations.", "social": "Trusted by generations of Indian cardiologists and physicians for consistent therapeutic bioavailability and patient compliance.", "technological": "Specialized drug delivery research, controlled-release matrix tablets, and advanced sterile manufacturing complexes in Indrad and Baddi.", "legal": "Complies with strict CDSCO good manufacturing practices, European regulatory approvals, and domestic pharmaceutical trademark protections.", "environmental": "Operates modern green manufacturing complexes with automated solvent recovery and energy-saving HVAC filtration systems."},
        [0.22, 0.62, 0.50, 0.38, 0.80],
        {"threat_of_new_entrants": "Low; establishing multi-decade personal prescription relationships with over 100,000 specialist doctors creates formidable moats.", "bargaining_power_of_buyers": "Low; patients suffering from chronic cardiac or psychiatric disorders strictly follow trusted doctor prescriptions with zero brand switching.", "bargaining_power_of_suppliers": "Low-to-moderate; robust supplier network for bulk active pharmaceutical ingredients.", "threat_of_substitutes": "Low-to-moderate; therapeutic substitution is heavily discouraged by treating cardiologists and psychiatrists.", "competitive_rivalry": "Moderate-high; competes against Sun Pharma, Mankind, and Abbott in Indian domestic chronic prescription markets."}
    ),
    (
        "Mankind Pharma", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "mass-market Tier-2/3 Indian families, rural consumers, and retail chemist shops",
        "seek ultra-affordable quality medicines for common infections, pain management, pregnancy diagnostics, and consumer wellness",
        "Prega News, Manforce & Moxikind-CV", "Mass-Market Consumer Healthcare & Affordable Therapeutics",
        "leads India in mass-market domestic pharmaceutical volume, providing affordable life-saving antibiotics alongside iconic household consumer health brands",
        [0.66, 0.86, 0.94, 0.82, 0.80, 0.55],
        {"political": "Directly supports government healthcare accessibility missions, providing high-quality medications at prices affordable to common citizens.", "economic": "Generates 95%+ of revenues from India's domestic market, boasting the deepest semi-urban distribution network reaching 80%+ of all chemists.", "social": "A household name in non-metro India, famous for destigmatizing personal health and delivering affordable pregnancy test kits (Prega News).", "technological": "Modernized formulation research centers in Manesar and Paonta Sahib, developing multi-ingredient fixed-dose combinations with proven stability.", "legal": "Complies with CDSCO pricing regulations (NLEM), consumer health advertising guidelines, and statutory corporate governance standards.", "environmental": "Operates eco-friendly manufacturing units in Himachal Pradesh and Sikkim with progressive wastewater recycling."},
        [0.20, 0.65, 0.48, 0.42, 0.84],
        {"threat_of_new_entrants": "Very low; a field force of 15,000+ medical reps covering every district chemist in India forms an impenetrable distribution fortress.", "bargaining_power_of_buyers": "Moderate-low; consumers and retail chemists trust Mankind's accessible price points and high brand recall.", "bargaining_power_of_suppliers": "Low; massive purchasing scale allows Mankind to command favorable pricing terms from bulk API suppliers.", "threat_of_substitutes": "Moderate; local generic manufacturers exist, but lack Mankind's doctor trust and national marketing presence.", "competitive_rivalry": "High; competing against Alkem Laboratories, Sun Pharma, and Abbott in domestic acute and chronic therapy markets."}
    ),
    (
        "Alkem Laboratories", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "general practitioners, pediatricians, and patients suffering from acute bacterial infections",
        "require dependable, clinically proven oral antibiotics and gastrointestinal therapies with rapid bio-absorption",
        "Clavam (Amoxicillin + Clavulanic Acid) & Pan-D", "Anti-Infective Formulations & Gastrointestinal Healthcare",
        "market leader in Indian anti-infective formulations, renowned for its flagship antibiotic Clavam and gastrointestinal therapies trusted by millions of doctors",
        [0.65, 0.84, 0.90, 0.84, 0.80, 0.58],
        {"political": "Key supplier of vital antibiotic treatments supporting national disease surveillance and infection control programs.", "economic": "Stable cash generation driven by acute therapeutic demand, expanding aggressively into higher-margin chronic cardiovascular and diabetes segments.", "social": "Trusted by Indian families for decades to treat severe respiratory and bacterial infections in children and elderly patients.", "technological": "Pioneered specialized moisture-barrier packaging and advanced dry-syrup suspension stability for delicate beta-lactam antibiotic molecules.", "legal": "Adheres to national drug price control orders (DPCO), CDSCO quality standards, and international cGMP manufacturing compliances.", "environmental": "Operates dedicated antibiotic waste treatment plants, preventing antimicrobial resistance (AMR) environmental contamination."},
        [0.22, 0.64, 0.52, 0.40, 0.82],
        {"threat_of_new_entrants": "Low; entrenched doctor prescription habits for antibiotics like Clavam and massive production scale create significant barriers.", "bargaining_power_of_buyers": "Low-to-moderate; acute infection patients require rapid cure and strictly purchase the exact brand prescribed by their physician.", "bargaining_power_of_suppliers": "Moderate; reliant on bulk active ingredients (Penicillin derivatives) sourced from domestic and international suppliers.", "threat_of_substitutes": "Low-to-moderate; alternative antibiotic formulations exist, but Clavam remains the clinical benchmark for co-amoxiclav therapy.", "competitive_rivalry": "Moderate-high; competes against Mankind Pharma, Sun Pharma, and GSK in anti-infectives and gastrointestinal medicines."}
    ),
    (
        "Glenmark Pharmaceuticals", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "dermatology specialists, respiratory patients, and novel molecule oncology researchers",
        "demand cutting-edge dermatology solutions for complex skin diseases, fixed-dose triple respiratory inhalers, and novel chemical entities",
        "Fabiflu, Ryaltris & Candid Dermatology Suite", "Dermatology Innovation & Novel Molecule Therapeutics",
        "pioneered novel global respiratory sprays like Ryaltris, while commanding leadership in anti-fungal dermatology (Candid) across India and emerging markets",
        [0.68, 0.84, 0.88, 0.92, 0.82, 0.60],
        {"political": "Delivered India's first approved oral COVID-19 therapy (Favipiravir / FabiFlu), demonstrating agile national crisis response.", "economic": "Extracts high-margin licensing royalties from global partnerships for Ryaltris in North America, Europe, and Japan.", "social": "Deep clinical focus on improving the quality of life for millions suffering from chronic skin conditions, respiratory distress, and allergies.", "technological": "Innovates via specialized Ichnos Sciences subsidiary developing novel bispecific antibodies for oncology and autoimmune diseases.", "legal": "Complies with US FDA, European Medicines Agency (EMA), and CDSCO clinical trial protocols and patent governance.", "environmental": "Implements green chemistry principles across API plants, reducing hazardous chemical solvents in drug manufacturing."},
        [0.24, 0.65, 0.54, 0.40, 0.80],
        {"threat_of_new_entrants": "Low; complex topical dermatology formulation science and multi-country clinical trials create steep entry barriers.", "bargaining_power_of_buyers": "Moderate; dermatologists and respiratory physicians maintain high brand loyalty to proven clinical formulations.", "bargaining_power_of_suppliers": "Low-to-moderate; integrated formulation plants backed by internal API manufacturing in Gujarat.", "threat_of_substitutes": "Moderate; alternative topical antifungals and nasal sprays exist, but Ryaltris holds unique dual-action clinical approval.", "competitive_rivalry": "High; competes with Sun Pharma and Cipla in dermatology and respiratory therapeutics."}
    ),
    (
        "Zydus Lifesciences", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "specialty physicians, dialysis patients, and global generic distributors",
        "seek novel target-discovery molecules for liver diseases, biosimilars for rheumatoid arthritis, and affordable oral solid dosage generics",
        "Lipaglyn (Saroglitazar) & ZyCoV-D DNA Vaccine", "Novel Chemical Discovery & Biosimilars",
        "discovered India's first indigenously developed New Chemical Entity (Lipaglyn) for diabetic dyslipidemia and NAFLD/NASH liver disease",
        [0.72, 0.84, 0.88, 0.94, 0.82, 0.62],
        {"political": "Pioneered the world's first plasmid DNA vaccine during the pandemic, representing flagship Indian biotechnology innovation.", "economic": "Enjoys growing global revenue from novel chemical licensing, US generic market opportunities, and specialty wellness products (Sugar Free).", "social": "Brings cutting-edge molecular therapies to Indian patients suffering from fatty liver disease at 90% lower cost than western imports.", "technological": "Extensive research laboratories in Ahmedabad conducting discovery biology, target identification, and automated high-throughput screening.", "legal": "Strict adherence to US FDA regulatory mandates, global patent registrations for novel chemical entities, and CDSCO compliance.", "environmental": "Green manufacturing sites certified for environmental safety, extensive solar energy utilization, and zero hazardous liquid discharge."},
        [0.22, 0.64, 0.52, 0.38, 0.80],
        {"threat_of_new_entrants": "Very low; novel molecule discovery and clinical trials require 10+ years of dedicated scientific investment and hundreds of crores.", "bargaining_power_of_buyers": "Moderate-low; patented novel chemical entities (Lipaglyn) face virtually zero direct bioequivalent generic competition.", "bargaining_power_of_suppliers": "Low-to-moderate; high internal API synthesis and formulation capabilities.", "threat_of_substitutes": "Low-to-moderate; standard lifestyle management and statins compete, but Lipaglyn holds unique dual PPAR-alpha/gamma approval.", "competitive_rivalry": "Moderate-high; competes with Sun Pharma, Dr. Reddy's, and Torrent in domestic and US formulation markets."}
    ),
    (
        "Aurobindo Pharma", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "global hospital networks, national health services, and generic pharmacy chains",
        "require ultra-cost-effective, high-volume generic oral solid medications, sterile injectable cephalosporins, and vertically integrated APIs",
        "Sterile Cephalosporin Injectables & Bulk Oral Generics", "High-Volume Generic Manufacturing & Sterile Parenterals",
        "world's cost-efficiency powerhouse in generic manufacturing, producing over 35 billion doses annually with deep vertical integration from basic chemicals",
        [0.68, 0.85, 0.85, 0.88, 0.82, 0.60],
        {"political": "Major beneficiary of the Indian Government's Production Linked Incentive (PLI) scheme for Key Starting Materials and Bulk Active Drugs.", "economic": "Top 3 generic pharmaceutical supplier by prescription volume in the United States, generating massive foreign exchange revenues.", "social": "Guarantees uninterrupted, ultra-affordable access to essential antibiotics, antiretrovirals, and cardiovascular medicines worldwide.", "technological": "World's largest single-site sterile injectable and oral solid manufacturing facilities with automated high-speed packaging lines in Hyderabad.", "legal": "Complies with US FDA cGMP inspections, European regulatory certifications, and international bulk chemical safety laws.", "environmental": "Investing heavily in green chemical synthesis, biological wastewater treatment plants, and captive solar energy in Andhra Pradesh."},
        [0.20, 0.70, 0.48, 0.44, 0.85],
        {"threat_of_new_entrants": "Very low; unmatched 35-billion dose manufacturing scale and backward chemical integration make it impossible for new entrants to compete on cost.", "bargaining_power_of_buyers": "High; US pharmaceutical wholesalers (McKesson, AmerisourceBergen) negotiate aggressively on high-volume commoditized generics.", "bargaining_power_of_suppliers": "Extremely low; deep vertical integration into raw chemical intermediates shields Aurobindo from supplier pricing power.", "threat_of_substitutes": "Moderate; competing generic manufacturers (Teva, Cipla) supply identical chemical bioequivalents.", "competitive_rivalry": "Intense; fierce global price competition in oral generic tablets and hospital sterile injectables."}
    ),
    (
        "Divi's Laboratories", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "Global Top 10 Big Pharma innovator companies and life sciences multinationals",
        "demand high-purity custom chemical synthesis, contract development and manufacturing (CDMO), and bulk active ingredients like Naproxen and Dextromethorphan",
        "Divi's Custom Synthesis & Active Pharmaceutical Ingredients", "Custom Synthesis & High-Purity Active Pharmaceutical Ingredients (API)",
        "world leader in custom chemical synthesis for innovator pharmaceuticals, commanding 60%+ global market share in active ingredients like Naproxen",
        [0.66, 0.88, 0.84, 0.94, 0.80, 0.65],
        {"political": "Strategic pillar of India's chemical independence; partners with global innovators to secure reliable pharmaceutical active ingredients.", "economic": "Enjoys extraordinary EBITDA margins (35-40%) driven by high-entry-barrier custom chemical synthesis and trusted Big Pharma intellectual property agreements.", "social": "The invisible backbone of global medicine, manufacturing the core active molecules that cure headaches, coughs, and cardiovascular ailments worldwide.", "technological": "Mastery over complex chemical reactions, continuous flow chemistry, high-hazard nitration, cryogenic reactions, and enzyme catalysis.", "legal": "Pristine regulatory compliance history with US FDA inspections across Hyderabad and Vizag facilities, with zero IP dispute violations.", "environmental": "World-class environmental treatment facilities with multi-stage reverse osmosis, zero liquid discharge, and green solvent recycling."},
        [0.18, 0.62, 0.52, 0.35, 0.75],
        {"threat_of_new_entrants": "Very low; multi-decade trust with Big Pharma to protect proprietary chemical IP, combined with massive chemical reactor capacity, forms an unassailable moat.", "bargaining_power_of_buyers": "Moderate; innovator pharma clients pay premium prices for Divi's flawless purity, reliability, and regulatory audit certainty.", "bargaining_power_of_suppliers": "Low-to-moderate; purchasing power over basic chemical building blocks from domestic and global chemical manufacturers.", "threat_of_substitutes": "Low; custom synthesized molecules are locked into innovator drug regulatory filings with the US FDA for the patent lifespan.", "competitive_rivalry": "Low-to-moderate; virtually uncontested in its core API molecules, competing globally with Lonza and Siegfried in custom CDMO."}
    ),
    (
        "Biocon Limited (Kiran Mazumdar-Shaw)", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "diabetes patients, cancer clinics, and global health systems",
        "seek affordable biosimilar insulins, monoclonal antibody biosimilars for oncology, and complex biological therapeutics",
        "Semglee (Glargine Biosimilar) & Ogivri (Trastuzumab)", "Commercial Biosimilars & Biopharmaceutical Innovation",
        "pioneered Asia's premier biopharmaceutical innovation engine, achieving the historic milestone of the first interchangeable biosimilar insulin approved by the US FDA",
        [0.72, 0.86, 0.92, 0.96, 0.85, 0.65],
        {"political": "Flagship symbol of Indian high-tech biotechnology innovation; active contributor to national biotechnology strategy and global biosimilar frameworks.", "economic": "Transformative global acquisition of Viatris biosimilar assets established a fully integrated worldwide commercial biopharma footprint.", "social": "Democratized access to lifesaving insulin and monoclonal antibodies, slashing therapy costs for millions of diabetic and cancer patients worldwide.", "technological": "World-class recombinant mammalian cell culture fermentation, continuous biological processing, and analytical characterization complexes in Bengaluru and Malaysia.", "legal": "Meets stringent US FDA interchangeable biosimilar regulatory standards, European EMA approvals, and complex patent clearance pathways.", "environmental": "High-efficiency green biomanufacturing plants with comprehensive water recycling and biological waste composting."},
        [0.20, 0.65, 0.54, 0.38, 0.80],
        {"threat_of_new_entrants": "Very low; developing interchangeable biosimilars requires $100M+ per molecule, living cell lines, and multi-year clinical trials.", "bargaining_power_of_buyers": "Moderate; pharmacy benefit managers in the US and state health authorities negotiate volume discounts, but Biocon's interchangeability provides leverage.", "bargaining_power_of_suppliers": "Moderate; relies on specialized single-use bioreactor bags, cell culture media, and specialized chromatography resins.", "threat_of_substitutes": "Low; biosimilar insulins and monoclonal antibodies represent standard-of-care clinical biologics with no simple chemical substitutes.", "competitive_rivalry": "Moderate-high; competing against Samsung Bioepis, Celltrion, and Sandoz in the high-stakes global biosimilars arena."}
    ),
    (
        "Laurus Labs", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "multinational pharmaceutical innovators, global antiretroviral distributors, and contract biotech companies",
        "need complex chemistry CDMO services, high-potency active ingredients, and affordable antiretroviral (ARV) intermediates",
        "Laurus Antiretroviral APIs & Specialized CDMO Synthesis", "Antiretroviral APIs & Biocatalytic CDMO Synthesis",
        "dominates global supply of first-line antiretroviral active pharmaceutical ingredients, expanding aggressively into animal health and precision biocatalytic CDMO",
        [0.68, 0.85, 0.88, 0.92, 0.80, 0.62],
        {"political": "Beneficiary of India's Bulk Drug PLI scheme; vital contributor to international HIV eradication partnerships with the Global Fund and PEPFAR.", "economic": "Diversifying revenue streams from commoditized ARV APIs into high-margin custom synthesis, formulations, and precision fermentation biotechnology.", "social": "Supplies affordable active ingredients that treat millions of HIV/AIDS patients across Africa, India, and Southeast Asia.", "technological": "High-potency API synthesis suites, biocatalysis, continuous manufacturing, and advanced flow chemistry capabilities in Visakhapatnam.", "legal": "Complies with US FDA cGMP standards, WHO quality pre-qualifications, and international patent licensing agreements.", "environmental": "Invests in zero liquid discharge plants and green biocatalytic reactions that replace hazardous chemical reagents with natural enzymes."},
        [0.24, 0.68, 0.55, 0.40, 0.82],
        {"threat_of_new_entrants": "Low; high-potency chemical handling certifications, massive multi-ton reactor volume, and WHO audits form defensible moats.", "bargaining_power_of_buyers": "Moderate-high; institutional HIV procurement agencies dictate tender pricing, offset by growing high-margin custom CDMO clients.", "bargaining_power_of_suppliers": "Moderate; purchasing basic chemical building blocks from domestic and Asian suppliers.", "threat_of_substitutes": "Low-to-moderate; alternative ARV chemical synthesizers exist, but Laurus holds structural cost leadership.", "competitive_rivalry": "Moderate-high; competes with Divi's Laboratories, Syngene, and Aarti Industries in contract custom synthesis."}
    ),
    (
        "IPCA Laboratories", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "rheumatoid arthritis patients, orthopedic doctors, and international antimalarial procurement agencies",
        "require trusted non-steroidal anti-inflammatory formulations, malaria eradication therapies, and backward-integrated bulk active ingredients",
        "Zerodol (Aceclofenac Formulations) & Lariago Antimalarials", "Pain Management, Rheumatology & Antimalarial Formulations",
        "market leader in Indian pain management with its flagship Zerodol franchise, combined with global leadership in life-saving artemisinin antimalarials",
        [0.66, 0.84, 0.90, 0.86, 0.80, 0.60],
        {"political": "Vital partner in national vector-borne disease control programs and global malaria eradication initiatives supported by WHO.", "economic": "Generates exceptional domestic prescription cash flows driven by the Zerodol pain-management brand, India's top-selling pharmaceutical brand.", "social": "Relieves debilitating chronic joint pain and arthritis for tens of millions of elderly Indian citizens, restoring daily mobility.", "technological": "Advanced formulation science in sustained-release pain management and deep organic synthesis for complex antimalarial intermediates.", "legal": "Complies with Indian CDSCO regulations, international WHO pre-qualifications, and active cGMP environmental standards.", "environmental": "Operates comprehensive wastewater treatment plants, biological remediation ponds, and solvent recycling units across Ratlam and Silvassa."},
        [0.22, 0.64, 0.50, 0.38, 0.80],
        {"threat_of_new_entrants": "Low; deep brand equity of Zerodol among Indian orthopedic surgeons and complete vertical integration create significant barriers.", "bargaining_power_of_buyers": "Low-to-moderate; arthritis patients experience immediate pain relief with Zerodol and rarely switch to generic alternatives.", "bargaining_power_of_suppliers": "Low; 100% backward integrated into active aceclofenac chemical synthesis, shielding IPCA from supplier price increases.", "threat_of_substitutes": "Moderate; competing NSAID pain relievers (diclofenac, paracetamol combinations) exist, but Zerodol dominates physician preference.", "competitive_rivalry": "Moderate; dominates orthopedic pain management, competing with Sun Pharma and Torrent in chronic therapies."}
    ),
    (
        "Abbott India", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "thyroid patients, pregnant women, pediatricians, and chronic metabolic disease managers",
        "demand trusted, clinically established branded formulations for thyroid balance, women's health, and gastrointestinal care",
        "Thyronorm, Duphaston & Udiliv", "Trusted Branded Prescription Formulations & Metabolic Care",
        "operates India's most iconic branded prescription portfolio, featuring market-leading Thyronorm used by millions of hypothyroid patients daily",
        [0.68, 0.86, 0.94, 0.88, 0.84, 0.60],
        {"political": "Seamlessly integrates multinational healthcare standards with deep domestic Indian manufacturing and community health education.", "economic": "Generates exceptional return on capital employed (ROCE > 40%) driven by high doctor loyalty to iconic chronic brands.", "social": "Essential to the daily health routine of millions of Indian women managing thyroid disorders (Thyronorm) and high-risk pregnancies (Duphaston).", "technological": "High-precision micro-dose tablet formulation guaranteeing exact hormonal bioavailability (microgram level) across shelf-life.", "legal": "Adheres to stringent National List of Essential Medicines (NLEM) pricing controls and international pharmacovigilance standards.", "environmental": "Operates state-of-the-art zero-waste manufacturing facilities in Goa with certified clean energy consumption."},
        [0.18, 0.60, 0.50, 0.35, 0.78],
        {"threat_of_new_entrants": "Very low; Thyronorm and Duphaston hold virtually unshakeable brand equity built over decades of clinical trust.", "bargaining_power_of_buyers": "Low; hypothyroid patients avoid changing thyroid hormone brands due to severe risks of hormonal re-calibration.", "bargaining_power_of_suppliers": "Low-to-moderate; diversified sourcing of active pharmaceutical compounds.", "threat_of_substitutes": "Low; medical specialists explicitly write 'Do Not Substitute' on Thyronorm prescriptions.", "competitive_rivalry": "Moderate; dominates its core chronic therapy segments against domestic generic challengers."}
    ),
    (
        "Sanofi India", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "diabetic patients, pediatricians, and cardiovascular disease managers",
        "seek gold-standard basal insulin therapies, life-saving pediatric vaccines, and trusted anti-allergy antihistamines",
        "Lantus (Insulin Glargine) & Allegra", "Basal Insulins, Pediatric Vaccines & Anti-Allergy Formulations",
        "sets the global clinical standard in 24-hour once-daily basal insulin therapy (Lantus) and non-drowsy allergy relief (Allegra) across India",
        [0.70, 0.86, 0.94, 0.92, 0.84, 0.62],
        {"political": "Partners with Indian healthcare authorities and diabetes task forces to combat India's massive national diabetes epidemic.", "economic": "Captures high recurring cash flows from lifelong insulin-dependent diabetic patients and pediatric vaccination programs.", "social": "Saves countless lives daily by preventing severe diabetic ketoacidosis and providing dependable 24-hour glycemic control.", "technological": "Advanced recombinant DNA insulin analogue production, disposable SoloSTAR insulin pens, and temperature-controlled cold chain logistics.", "legal": "Complies with CDSCO drug regulations, cold-chain regulatory guidelines, and international biological manufacturing safety codes.", "environmental": "Comprehensive insulin pen recycling initiatives and sustainable cold chain packaging reducing dry-ice and plastic waste."},
        [0.20, 0.62, 0.52, 0.35, 0.80],
        {"threat_of_new_entrants": "Very low; recombinant insulin biological manufacturing and global cold chain logistics create immense entry moats.", "bargaining_power_of_buyers": "Low-to-moderate; diabetic patients rely on Lantus for consistent nighttime blood sugar control and rarely risk switching.", "bargaining_power_of_suppliers": "Low; vertically integrated within global Sanofi biological manufacturing network.", "threat_of_substitutes": "Moderate; biosimilar glargine insulins (Biocon Semglee) compete on price, but Lantus retains strong doctor loyalty.", "competitive_rivalry": "Moderate; competes with Novo Nordisk and Biocon in the Indian diabetes and insulin market."}
    ),
    (
        "GlaxoSmithKline Pharmaceuticals India (GSK India)", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "pediatricians, general physicians, and parents seeking childhood immunization",
        "require gold-standard pediatric vaccines, broad-spectrum antibiotic syrups, and trusted dermatological treatments",
        "Augmentin, Calpol & Infanrix Hexa Vaccines", "Pediatric Vaccines & Primary Care Anti-Infectives",
        "manufactures India's most trusted fever relief medication (Calpol) and gold-standard pediatric multi-disease vaccines",
        [0.70, 0.86, 0.95, 0.90, 0.84, 0.60],
        {"political": "Vital partner in national immunization programs and pediatric infection control with a 100-year institutional presence in India.", "economic": "Dominates retail pharmacy sales across India with iconic paracetamol brand Calpol and premier antibiotic Augmentin.", "social": "Calpol is universally recognized by Indian mothers and doctors as the first line of compassionate defense against childhood fevers.", "technological": "Advanced vaccine antigen stabilization, sterile vaccine vial filling, and tamper-evident packaging technologies.", "legal": "Adheres to strict CDSCO essential medicine price regulations, pharmacovigilance safety reporting, and cGMP compliance.", "environmental": "Operates ultra-modern green manufacturing campus in Nashik with zero liquid discharge and renewable energy installations."},
        [0.18, 0.62, 0.48, 0.36, 0.80],
        {"threat_of_new_entrants": "Very low; century-old household brand trust for Calpol and complex vaccine manufacturing create insurmountable barriers.", "bargaining_power_of_buyers": "Low-to-moderate; parents and pediatricians demand verified brand authenticity for sick children, willingly paying modest premiums.", "bargaining_power_of_suppliers": "Low; strong corporate procurement scale for active pharmaceutical ingredients.", "threat_of_substitutes": "Moderate; generic paracetamol and amoxicillin brands exist, but Calpol and Augmentin maintain commanding physician prescription preference.", "competitive_rivalry": "Moderate; dominates primary healthcare against domestic generic challengers."}
    ),
    (
        "Pfizer Limited India", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "hospital ICUs, critical care specialists, and infant healthcare providers",
        "demand life-saving critical care hospital injectables, pneumococcal infant vaccines, and advanced oncology targeted therapies",
        "Prevenar 13, Magnex & Meronem Critical Care", "Pneumococcal Vaccines & Hospital Critical Care Therapeutics",
        "delivers the gold-standard Prevenar 13 pediatric pneumococcal vaccine and vital hospital anti-infectives (Meronem, Magnex) for severe ICU infections",
        [0.72, 0.86, 0.94, 0.94, 0.85, 0.62],
        {"political": "Supports national childhood pneumonia eradication and antimicrobial stewardship programs across Indian hospital networks.", "economic": "Generates strong cash flows from high-value hospital critical care injectables and premium pediatric vaccines.", "social": "Protects millions of infants from life-threatening pneumococcal meningitis and provides ICU patients with vital last-resort antibiotics.", "technological": "Pioneered complex multi-valent polysaccharide-protein conjugate vaccine manufacturing and sterile lyophilized injectable synthesis.", "legal": "Complies with stringent hospital procurement guidelines, international patent protections, and drug pricing regulations.", "environmental": "Operates environmentally sustainable manufacturing sites with comprehensive solvent recovery and medical waste neutralization."},
        [0.20, 0.64, 0.52, 0.35, 0.78],
        {"threat_of_new_entrants": "Very low; conjugate vaccine manufacturing and sterile critical care injectable infrastructure require immense specialized capital.", "bargaining_power_of_buyers": "Moderate-low; ICU intensivists treating septic shock rely on trusted critical care brands like Meronem with zero compromise.", "bargaining_power_of_suppliers": "Low; supported by global Pfizer biological and chemical supply chains.", "threat_of_substitutes": "Moderate; generic meropenem and pneumonia vaccines (Serum Institute Pneumosil) compete on price in tender markets.", "competitive_rivalry": "Moderate; leads hospital critical care segments against domestic generic injectable manufacturers."}
    ),
    (
        "Natco Pharma", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "oncology patients, hepatitis-C sufferers, and international generic distributors",
        "seek life-saving cancer medications and hepatitis cures at a fraction of Western monopoly prices through patent challenges",
        "Veenat (Imatinib), Geftinat & Hepcinat", "Complex Oncology Generics & Patent Litigation Specialists",
        "renowned globally for challenging Western pharmaceutical monopolies, slashing the cost of life-saving leukemia and hepatitis-C treatments by 95%",
        [0.72, 0.85, 0.94, 0.92, 0.86, 0.60],
        {"political": "Champion of compulsory licensing under Section 84 of the Indian Patents Act, upholding developing world access to life-saving medicines.", "economic": "Enjoys extraordinary windfalls from Para-IV first-to-file generic litigations in the US market (e.g., generic Revlimid).", "social": "Saved hundreds of thousands of cancer patients in India and emerging nations from financial ruin by providing affordable oncology drugs.", "technological": "High-potency active pharmaceutical ingredient (HPAPI) isolation suites, synthetic organic chemistry, and complex oncology delivery systems.", "legal": "Master of international patent litigation, successfully defending generic drug approvals in Indian and US federal courts.", "environmental": "Operates high-containment oncology manufacturing plants in Hyderabad with advanced chemical scrubbers and zero liquid discharge."},
        [0.25, 0.65, 0.54, 0.38, 0.82],
        {"threat_of_new_entrants": "Low; navigating complex international patent litigation while synthesizing hazardous cytotoxic oncology molecules forms a high moat.", "bargaining_power_of_buyers": "Moderate-low; cancer patients and oncologists enthusiastically prescribe Natco's affordable generic equivalents.", "bargaining_power_of_suppliers": "Low-to-moderate; backward integration into cytotoxic oncology active ingredients.", "threat_of_substitutes": "Low; generic versions of life-saving cancer therapies have no non-medical substitutes.", "competitive_rivalry": "Moderate-high; competes against Dr. Reddy's, Sun Pharma, and Cipla in specialized oncology generics."}
    ),
    (
        "Ajanta Pharma", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "ophthalmologists, dermatologists, and cardiology practitioners in emerging markets",
        "need first-to-market specialty branded formulations in eye-drops, dermatology creams, and cardiovascular medicines",
        "Bimat LS & Melacare Specialized Formulations", "Specialty Ophthalmology, Dermatology & Emerging Market Branded Generics",
        "delivers first-to-market specialty branded generics, dominating Indian ophthalmology eye-drops and emerging market branded formulations across Africa and Asia",
        [0.65, 0.84, 0.90, 0.88, 0.80, 0.58],
        {"political": "Supports Indian export growth across high-potential emerging markets in Francophone Africa, Middle East, and Southeast Asia.", "economic": "Consistently generates superior return on equity (ROE > 20%) by identifying niche specialty therapy gaps neglected by larger competitors.", "social": "Provides high-quality ophthalmic solutions that prevent glaucoma-induced blindness and restore eyesight across developing markets.", "technological": "Specialized sterile blow-fill-seal (BFS) technology for preservative-free ophthalmic eye drops and advanced topical dermatology creams.", "legal": "Complies with CDSCO regulations, international emerging market regulatory registrations, and US FDA generic approvals.", "environmental": "State-of-the-art manufacturing facilities in Dahej and Guwahati operating with automated energy management and water recycling."},
        [0.24, 0.65, 0.52, 0.40, 0.80],
        {"threat_of_new_entrants": "Moderate-low; sterile eye drop blow-fill-seal manufacturing and deep doctor prescription networks in specialty niches create barriers.", "bargaining_power_of_buyers": "Moderate-low; ophthalmologists and dermatologists prescribe trusted brands with high patient adherence.", "bargaining_power_of_suppliers": "Low-to-moderate; balanced chemical sourcing network across Indian and global fine chemical suppliers.", "threat_of_substitutes": "Moderate; competing eye drop formulations exist, but Ajanta commands leadership in specialized glaucoma therapies.", "competitive_rivalry": "Moderate; competes with Sun Pharma and Micro Labs in specialized ophthalmic care."}
    ),
    (
        "Gland Pharma (Fosun Pharma)", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "multinational pharmaceutical corporations, hospital groups, and injectable distributors",
        "demand sterile, contamination-free generic injectable manufacturing (CDMO) in vials, ampoules, and pre-filled syringes",
        "Sterile Parenteral Injectables & Complex Biologics", "Pure-Play Sterile Injectables Contract Manufacturing (CDMO)",
        "world's premier pure-play sterile injectable manufacturer, operating pristine FDA-approved aseptic cleanrooms with zero contamination recalls",
        [0.68, 0.86, 0.88, 0.94, 0.84, 0.62],
        {"political": "Vital component of global hospital supply chains, exporting essential sterile injectable anesthetics and antibiotics worldwide.", "economic": "High-margin B2B business-to-business model with predictable long-term contract manufacturing agreements with global pharma giants.", "social": "Supplies life-critical operating theater anesthetics, anticoagulants, and ICU emergency injectables that sustain surgical care globally.", "technological": "Advanced robotic aseptic filling lines, isolator technology, lyophilization chambers, and high-speed pre-filled syringe (PFS) assembly.", "legal": "Unblemished regulatory inspection track record with US FDA, European MHRA, and Australian TGA across all Hyderabad manufacturing units.", "environmental": "Operates high-efficiency sterile cleanrooms with advanced HEPA air filtration and zero liquid discharge industrial water recovery."},
        [0.20, 0.65, 0.52, 0.38, 0.78],
        {"threat_of_new_entrants": "Very low; sterile injectable plants require extreme regulatory scrutiny; even microscopic particulate contamination shuts down plants.", "bargaining_power_of_buyers": "Moderate; global pharma partners value Gland's pristine regulatory compliance and cannot risk drug shortages from FDA warning letters.", "bargaining_power_of_suppliers": "Moderate; relies on specialized medical-grade borosilicate glass vials, rubber stoppers, and active drug substances.", "threat_of_substitutes": "Low; hospital intravenous and intramuscular injectable delivery has no clinical alternative for emergency and surgical therapies.", "competitive_rivalry": "Low-to-moderate; recognized as an elite global leader in sterile injectables alongside Hospira (Pfizer) and Fresenius Kabi."}
    ),
    (
        "JB Chemicals & Pharmaceuticals", "Pharmaceuticals & Active Pharmaceutical Ingredients",
        "general physicians, gastro specialists, and international lozenge brand owners",
        "seek proven gastrointestinal antacids, calcium-channel hypertension medications, and specialized contract medicated lozenges",
        "Rantac (Ranitidine Formulations), Cilacar & Medicated Lozenges", "Gastrointestinal, Hypertension & Medicated Lozenges",
        "manufactures India's iconic antacid brand Rantac, market-leading hypertension drug Cilacar, and ranks as the world's top contract lozenge maker",
        [0.66, 0.85, 0.92, 0.86, 0.80, 0.58],
        {"political": "Supports national healthcare affordability and exports medicated wellness lozenges and formulations to over 40 global markets.", "economic": "Delivering industry-leading domestic prescription growth backed by majority ownership and strategic transformation under KKR.", "social": "Rantac has been a staple in Indian household medicine cabinets for 35+ years, providing fast relief from gastric acidity and ulcers.", "technological": "Proprietary medicated lozenge manufacturing science with controlled active drug release, flavor masking, and automated high-speed packaging.", "legal": "Complies with CDSCO regulations, international US FDA and EU cGMP standards, and food/drug safety lozenge compliances.", "environmental": "Modernized manufacturing plants in Panoli and Daman operating with energy-efficient boilers and zero liquid discharge."},
        [0.22, 0.64, 0.50, 0.38, 0.80],
        {"threat_of_new_entrants": "Low; massive doctor prescription loyalty for Rantac and Cilacar and specialized confectionery-pharmaceutical lozenge tech form moats.", "bargaining_power_of_buyers": "Low-to-moderate; patients rely on Cilacar for precise blood pressure control and strictly avoid changing prescribed hypertension tablets.", "bargaining_power_of_suppliers": "Low-to-moderate; strong domestic sourcing of bulk chemical intermediates.", "threat_of_substitutes": "Moderate; competing proton-pump inhibitors (pantoprazole) exist, but Rantac maintains deep loyalty among general practitioners.", "competitive_rivalry": "Moderate; dominates its core gastro and calcium-channel blocker therapy segments against domestic peers."}
    )
]

for item in sector6_data:
    add_c(*item)

print(f"Sector 6 added: {len(sector6_data)} companies. Total: {len(comps)}")

with open(part1_path, "w", encoding="utf-8") as f:
    json.dump(comps, f, indent=2)
print(f"COMPLETED PART 1: {len(comps)} companies written to {part1_path}!")
