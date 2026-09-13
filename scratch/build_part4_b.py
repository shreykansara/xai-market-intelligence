"""
Omniscope AI - Part 4B Generator
Builds Sectors 22, 23, 24 (52 companies):
- Sector 22: EdTech, Higher Education & Skill Development (18 companies)
- Sector 23: Digital Media, Gaming, Audio & Entertainment (18 companies)
- Sector 24: B2B Industrial Commerce, Manufacturing & Contract Electronics (16 companies)
Combines with scratch/part4_a.json to produce scratch/part4.json (114 companies).
"""
import json
from pathlib import Path

part4_b = []

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    part4_b.append({
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
# SECTOR 22: EdTech, Higher Education & Skill Development (18 companies)
# ==============================================================================
sector22_data = [
    (
        "PhysicsWallah (PW)", "EdTech, Higher Education & Skill Development",
        "aspirational middle and lower-middle-class students across Bharat preparing for JEE and NEET",
        "demand world-class IIT-JEE and NEET entrance coaching from charismatic educators without paying crippling Rs 1.5-lakh coaching fees",
        "PW Yakeen, Lakshya Batches & PW Vidyapeeth Hybrid Centers", "Democratized Affordable Test Preparation & Hybrid Coaching Centers",
        "shattered the coaching monopoly in India by delivering elite JEE/NEET video courses at Rs 3,000-4,000, educating over 10 million students with passionate teachers",
        [0.72, 0.94, 0.98, 0.94, 0.84, 0.70],
        {"political": "Supports National Education Policy (NEP 2020) goals of affordable, equitable educational access for non-metro youth.", "economic": "Unicorn EdTech that achieved sustained operational profitability through ultra-low marketing spend and viral teacher-student emotional resonance.", "social": "Empowered children of farmers, small shopkeepers, and rickshaw drivers to clear elite engineering and medical exams, creating massive upward social mobility.", "technological": "High-concurrency live streaming app capable of handling 500,000 simultaneous live video viewers, AI doubt-resolution bot (AI Guru), and digital smart classrooms.", "legal": "Consumer Protection Act compliance, transparent refund guidelines, and ASCI advertising standards for coaching results.", "environmental": "Online education eliminates inter-city student migration to coaching hubs, cutting travel carbon emissions and study paper consumption."},
        [0.25, 0.50, 0.35, 0.25, 0.72],
        {"threat_of_new_entrants": "Moderate; educational apps can be coded, but Alakh Pandey's messianic teacher trust and 10M YouTube community cannot be duplicated.", "bargaining_power_of_buyers": "Low; courses cost just Rs 3,500/year, making them irresistible value for students.", "bargaining_power_of_suppliers": "Moderate; top rockstar teachers are courted by venture-funded competitors, but PW offers internal faculty ownership.", "threat_of_substitutes": "Moderate from offline Kota coaching institutes (Allen, Resonance) and free YouTube lectures.", "competitive_rivalry": "Intense rivalry with Unacademy, Allen, and Vedantu."}
    ),
    (
        "Unacademy (Sorting Hat Technologies)", "EdTech, Higher Education & Skill Development",
        "civil service aspirants (UPSC), banking candidates, and competitive exam test takers",
        "need comprehensive live learning, top national educators, structured mock test series, and personalized mentor feedback",
        "Unacademy Plus Subscription & Unacademy Centres", "Comprehensive Multi-Exam Live Learning & Test Prep Platform",
        "built India's largest live learning platform, bringing the country's top educators in UPSC, SSC, and engineering straight to students' smartphones",
        [0.70, 0.90, 0.96, 0.95, 0.84, 0.70],
        {"political": "Aligned with government recruitment exam calendars and public education formalization policies.", "economic": "Transitioned to financial discipline and operational profitability; expanding physical hybrid centers in major educational hubs.", "social": "Allows students in remote towns to learn directly from former civil servants and top subject educators without moving to Delhi or Kota.", "technological": "Proprietary live classroom interactive technology with real-time student doubt-clearing, live polls, and detailed rank analytics.", "legal": "ASCI advertising standards for topper claims and consumer protection rules.", "environmental": "Digital live learning eliminates millions of printed test books and long-distance student travel."},
        [0.28, 0.52, 0.40, 0.28, 0.75],
        {"threat_of_new_entrants": "Moderate; high customer acquisition costs (CAC) make new entrant scaling challenging.", "bargaining_power_of_buyers": "Moderate; students compare subscription pricing and educator lists.", "bargaining_power_of_suppliers": "High; top celebrity educators command high salaries and can migrate between EdTech platforms.", "threat_of_substitutes": "High from PhysicsWallah and offline coaching centers.", "competitive_rivalry": "Fierce competition with PhysicsWallah, Adda247, and Allen."}
    ),
    (
        "Eruditus Executive Education", "EdTech, Higher Education & Skill Development",
        "senior corporate executives, business leaders, and mid-career professionals globally",
        "require elite executive education credentials and leadership diplomas from the world's most prestigious universities (MIT, Harvard, Wharton, INSEAD)",
        "Global Executive Programs & Customized Corporate Leadership Diplomas", "Elite Global Executive Education & University Partnership Platform",
        "is a global leader in professional executive upskilling, partnering with top Ivy League and global universities to deliver high-impact leadership diplomas",
        [0.72, 0.88, 0.94, 0.96, 0.85, 0.72],
        {"political": "Direct beneficiary of global corporate leadership transitions, AI workforce retraining mandates, and international higher education collaborations.", "economic": "High-ticket enterprise and executive pricing ($2,000 to $30,000 per program) delivers multi-million dollar global cash flows across 80+ countries.", "social": "Democratizes access to elite Ivy League faculty and curriculum for ambitious global leaders without requiring them to quit their jobs.", "technological": "Proprietary cohort-based learning platform, AI video simulation case studies, and global executive networking lounges.", "legal": "International university IP licensing agreements, accreditation compliance, and global data privacy standards.", "environmental": "Digital executive courses eliminate thousands of long-haul international flights for executive weekend seminars."},
        [0.18, 0.45, 0.45, 0.20, 0.55],
        {"threat_of_new_entrants": "Very low; establishing multi-year exclusive curriculum partnerships with MIT, Wharton, and Cambridge takes decades of institutional trust.", "bargaining_power_of_buyers": "Low to moderate; corporate CXOs and sponsors value Ivy League brand certification over program fees.", "bargaining_power_of_suppliers": "High; elite partner universities set curriculum standards and share substantial tuition royalties.", "threat_of_substitutes": "Moderate from full-time on-campus executive MBA programs.", "competitive_rivalry": "Low to moderate; competes globally with 2U/edX and Emeritus."}
    ),
    (
        "upGrad", "EdTech, Higher Education & Skill Development",
        "working professionals, college graduates, and career transitioners",
        "need accredited online Master's degrees, post-graduate diplomas in Data Science, AI, and Management, with personalized 1-on-1 industry mentorship",
        "Online University Degrees & Tech/Management Post-Graduate Programs", "Higher Education & Career Transformation Platform",
        "is South Asia's largest higher EdTech company, helping working professionals earn recognized degrees from top global universities while working full-time",
        [0.72, 0.90, 0.96, 0.95, 0.85, 0.72],
        {"political": "Direct beneficiary of University Grants Commission (UGC) regulations formally recognizing online degree equivalence in India.", "economic": "High average order values (>Rs 1.5 Lakhs) with high course completion rates (>85%) driven by intensive student hand-holding and placement support.", "social": "Enables engineers and managers to upgrade their skills for the AI economy, achieving an average 50%+ salary hike post-completion.", "technological": "Integrated learning management system, code evaluation sandboxes, automated resume scoring, and live industry case-study sessions.", "legal": "UGC online education regulations, AICTE approvals, and university joint-certification agreements.", "environmental": "Online degree delivery eliminates physical campus infrastructure resource consumption and daily commuting emissions."},
        [0.24, 0.50, 0.40, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; building university tie-ups and student placement networks requires substantial operational scale.", "bargaining_power_of_buyers": "Moderate; working professionals evaluate placement track records and university accreditation.", "bargaining_power_of_suppliers": "Moderate; university partners negotiate revenue splits.", "threat_of_substitutes": "Moderate from part-time evening MBA programs and free self-paced MOOCs (Coursera).", "competitive_rivalry": "Moderate to high with Simplilearn and Great Learning."}
    ),
    (
        "Vedantu", "EdTech, Higher Education & Skill Development",
        "K-12 schoolchildren and parents seeking personalized, interactive home tutoring",
        "need engaging, two-way interactive live online tutoring that keeps young students attentive and delivers personalized doubt solving",
        "WAVE Interactive Classroom & K-12 Live Tutoring", "Interactive Two-Way K-12 Live Learning Technology",
        "pioneered live online interactive tutoring in India with its patented WAVE platform, measuring student engagement and facial attentiveness in real-time",
        [0.70, 0.88, 0.95, 0.94, 0.84, 0.70],
        {"political": "Supports National Education Policy guidelines on digital interactive pedagogical methods for school education.", "economic": "Focusing on capital efficiency through hybrid learning centers (Vedantu Learning Centres) and affordable subscription tiers.", "social": "Connects children in Tier-2 and Tier-3 towns with inspiring master teachers, making science and mathematics fun and accessible.", "technological": "Patented WAVE 2.0 platform running on low bandwidth, real-time student quiz leaderboards, and AI facial attention telemetry.", "legal": "Consumer protection guidelines, child online safety standards, and truth-in-advertising compliance.", "environmental": "Digital learning eliminates paper notebooks and physical transit congestion around school tutoring hubs."},
        [0.28, 0.55, 0.38, 0.25, 0.74],
        {"threat_of_new_entrants": "Moderate; live video software is common, but patented interactive engagement tools and student retention require deep IP.", "bargaining_power_of_buyers": "High; parents evaluate multiple EdTech options and local neighborhood tuition teachers.", "bargaining_power_of_suppliers": "Moderate; qualified schoolteachers.", "threat_of_substitutes": "High from local offline neighborhood tuition centers and PhysicsWallah.", "competitive_rivalry": "High with PhysicsWallah, Unacademy, and offline coaching centers."}
    ),
    (
        "Simplilearn Solutions", "EdTech, Higher Education & Skill Development",
        "global tech professionals, cloud architects, and corporate IT workforces",
        "require industry-certified digital economy bootcamps in cloud computing, cybersecurity, DevOps, and project management (PMP)",
        "Digital Economy Bootcamps & Caltech / Purdue Post-Graduate Programs", "Digital Upskilling & Professional Certification Bootcamps",
        "has trained over 5 million professionals across 150 countries, partnering with top tech giants (AWS, Microsoft, IBM) and universities for career bootcamps",
        [0.72, 0.90, 0.95, 0.95, 0.85, 0.72],
        {"political": "Supports corporate workforce digital transformation and global tech talent retraining under IT industry skill missions.", "economic": "Acquired by global private equity giant Blackstone; high foreign currency revenue share (>60% from US and international markets) and strong EBITDA margins.", "social": "Bridges the critical global gap between traditional college IT curriculums and high-demand cloud/AI industry job requirements.", "technological": "Hands-on cloud simulation labs, automated coding project grading, and synchronized live cohort learning modules.", "legal": "Accredited education provider compliance (PMI, CompTIA, IIBA), and international student consumer protections.", "environmental": "Virtual cloud computing labs replace physical computer hardware training centers, cutting energy and electronic waste."},
        [0.22, 0.48, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; building partnerships with Purdue, Caltech, and enterprise software vendors requires proven completion metrics.", "bargaining_power_of_buyers": "Moderate; IT engineers seek recognized certifications to pass corporate promotion hurdles.", "bargaining_power_of_suppliers": "Moderate; university partners and industry certification bodies.", "threat_of_substitutes": "Moderate from Coursera, Udacity, and free tech documentation.", "competitive_rivalry": "Direct competition with upGrad and Great Learning."}
    ),
    (
        "Adda247", "EdTech, Higher Education & Skill Development",
        "aspirational youth in Tier-2, Tier-3, and rural India preparing for government recruitment exams",
        "need affordable test preparation in their local mother tongues (Hindi, Tamil, Telugu, Bengali, Marathi) for bank PO, SSC, railway, and state civil exams",
        "Vernacular Government Job Prep & Career Power Coaching", "Vernacular Test Prep Platform for Bharat",
        "is India's largest vernacular test prep platform, educating over 22 million monthly active students in 12 regional languages for government jobs",
        [0.72, 0.92, 0.96, 0.94, 0.84, 0.70],
        {"political": "Directly supports government recruitment preparation (IBPS, SSC, State PSCs) and vernacular digital inclusion under Digital India.", "economic": "Backed by Google; rapid revenue growth powered by high-volume micro-courses priced between Rs 500 and Rs 2,500 tailored to small-town incomes.", "social": "Provides rural youth from humble agricultural families with the knowledge to secure permanent government and banking jobs, changing family destinies.", "technological": "Lightweight mobile app engineered for low-bandwidth 3G/4G connectivity, offline test downloading, and regional language AI doubt solvers.", "legal": "Compliance with government exam fair practice standards and consumer transparency rules.", "environmental": "Completely eliminates the requirement for rural students to travel and rent rooms in distant state capital coaching hubs."},
        [0.26, 0.50, 0.35, 0.25, 0.68],
        {"threat_of_new_entrants": "Moderate; vernacular content creation across 12 languages requires localized regional educator networks.", "bargaining_power_of_buyers": "Moderate; small-town students are price-conscious, but find Adda247's entry price points highly affordable.", "bargaining_power_of_suppliers": "Low; large pool of passionate regional language educators.", "threat_of_substitutes": "Moderate from local small-town coaching shops and free YouTube channels.", "competitive_rivalry": "Moderate; dominates vernacular government test prep ahead of Testbook and Oliveboard."}
    ),
    (
        "Classplus", "EdTech, Higher Education & Skill Development",
        "independent coaching teachers, local tuition centers, and educational content creators across 3,000+ towns",
        "need their own branded mobile teaching app, automated student fee collection, anti-piracy video hosting, and digital test conduction",
        "Classplus Operating System for Educators", "B2B SaaS Platform for Teachers & Coaching Institutes",
        "empowers over 100,000 independent teachers to launch their own branded mobile apps, digitizing local tutoring and helping educators monetize their content nationally",
        [0.70, 0.90, 0.95, 0.96, 0.84, 0.70],
        {"political": "Aligned with Skill India and Digital India missions, enabling grassroots local teachers to transition into digital entrepreneurs.", "economic": "High-margin SaaS subscription model plus transaction revenue-share on course sales; rapid organic growth driven by local tutor word-of-mouth.", "social": "Empowers traditional neighborhood math and physics teachers to preserve their independent identity without being swallowed by centralized EdTech conglomerates.", "technological": "Patented anti-screen-recording video DRM security, automated batch scheduling, digital student attendance, and integrated UPI fee collection.", "legal": "Software IP protection, digital content copyright safeguards for teachers, and data privacy compliance.", "environmental": "SaaS software eliminates paper fee receipts, paper attendance registers, and printed test booklets across 100,000 classrooms."},
        [0.22, 0.48, 0.30, 0.20, 0.58],
        {"threat_of_new_entrants": "Low to moderate; network effects and high switching costs for teachers whose entire student database is hosted on Classplus.", "bargaining_power_of_buyers": "Low; coaching teachers find Classplus indispensable for student management and fee collection.", "bargaining_power_of_suppliers": "Low; cloud infrastructure (AWS) and video streaming CDNs.", "threat_of_substitutes": "Moderate from generic tools (Zoom, Google Meet, WhatsApp), but generic tools lack fee management and DRM security.", "competitive_rivalry": "Low to moderate; undisputed category creator and market leader ahead of Teachmint."}
    ),
    (
        "LEAD School", "EdTech, Higher Education & Skill Development",
        "budget private schools, small-town school owners, and Tier-2/3/4 students",
        "require an integrated school operating system that transforms traditional rote-learning budget schools into modern, English-medium smart schools",
        "LEAD Integrated School System & Teacher Pedagogical OS", "B2B Integrated School EdTech & Curriculum System",
        "partners with over 3,000 budget private schools across 400 cities, delivering integrated multimodal curriculum, smart TVs, and teacher training to 1.2M students",
        [0.72, 0.90, 0.96, 0.94, 0.85, 0.72],
        {"political": "Fully aligned with National Education Policy (NEP 2020) curriculum frameworks, activity-based learning, and foundational literacy.", "economic": "Sticky multi-year B2B school partnership contracts with high retention; school fees collected directly with zero consumer CAC.", "social": "Bridges the vast educational divide between elite metro private schools and small-town budget schools, giving rural children fluent English literacy.", "technological": "Teacher-guidance tablets with daily lesson plans, student audio-visual smart classroom software, and gamified practice apps for parents.", "legal": "CBSE/ICSE and state school board curriculum compliance, child digital privacy, and copyright protections.", "environmental": "Digital lesson plans and centralized textbook logistics optimize paper usage across thousands of budget schools."},
        [0.22, 0.48, 0.32, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; signing up 3,000 independent school managements and retraining their teacher staff requires massive ground presence.", "bargaining_power_of_buyers": "Low to moderate; budget school owners see immediate student enrollment growth after adopting LEAD.", "bargaining_power_of_suppliers": "Low; proprietary in-house curriculum and pedagogical content.", "threat_of_substitutes": "Moderate from traditional physical textbook publishers (NCERT, Oxford).", "competitive_rivalry": "Low to moderate; undisputed leader in budget private school transformation ahead of Next Education."}
    ),
    (
        "Cuemath", "EdTech, Higher Education & Skill Development",
        "parents of young children (K-12) across India, US, and the Middle East",
        "want their children to master fundamental mathematical logic, mental math, and analytical problem-solving rather than rote-memorizing formulas",
        "Cuemath Visual Math Curriculum & 1-on-1 Certified Math Tutors", "Visual Math Learning & Analytical Logic Platform",
        "has trained over 200,000 students globally using an innovative visual learning system that teaches children the 'why' behind mathematics through puzzles and geometry",
        [0.68, 0.88, 0.94, 0.94, 0.84, 0.72],
        {"political": "Supports NEP 2020 emphasis on foundational numeracy and mathematical thinking; accredited by STEM.org.", "economic": "High recurring monthly subscription fees and strong international revenue contribution from high-paying US and UAE diaspora parents.", "social": "Eliminates deep-seated math anxiety among young children, building confident analytical thinkers and future coders.", "technological": "Visual math interactive manipulatives, automated diagnostic math tests, and adaptive algorithmic problem difficulty scaling.", "legal": "Child online privacy protection (COPPA compliance), tutor background verification, and international consumer standards.", "environmental": "Digital gamified math puzzles eliminate printed math workbooks and plastic geometry toolkits."},
        [0.25, 0.50, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; math apps are plentiful, but Cuemath's curated teacher certification and visual pedagogical IP form a solid moat.", "bargaining_power_of_buyers": "Moderate; parents evaluate their child's school test performance and confidence.", "bargaining_power_of_suppliers": "Low; massive pool of educated homemakers and certified math teachers working flexibly from home.", "threat_of_substitutes": "Moderate from Kumon math centers and traditional school math classes.", "competitive_rivalry": "Moderate; competes with Kumon and online math platforms."}
    ),
    (
        "Allen Career Institute", "EdTech, Higher Education & Skill Development",
        "elite science students aiming for top All India Ranks in NEET medical and IIT-JEE engineering entrance exams",
        "demand rigorous, high-intensity classroom test preparation with proven track records of producing All India Rank 1 toppers",
        "Allen Classroom Coaching Programs & Allen Digital Test Prep", "Pre-Eminent Classroom Entrance Coaching & Digital Testing",
        "is the undisputed emperor of Kota coaching, producing multiple All India Rank 1 champions every single year and training over 300,000 students annually",
        [0.72, 0.92, 0.96, 0.92, 0.86, 0.70],
        {"political": "Subject to state government regulations on student mental health, coaching center safety standards, and fire safety norms in Kota.", "economic": "Immense financial strength; backed by Bodhi Tree Systems (Uday Shankar and James Murdoch), generating thousands of crores in high-margin classroom fees.", "social": "The ultimate academic dream temple for millions of ambitious Indian families seeking guaranteed medical and engineering admissions.", "technological": "Computerized OMR test evaluation, AI student test performance diagnostics, and seamless hybrid classroom streaming via Allen Digital.", "legal": "State coaching establishment acts, fire safety clearances, and strict consumer protection guidelines.", "environmental": "Green campus initiatives in Kota, automated digital test conduction cutting tons of physical paper exam sheets."},
        [0.20, 0.45, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; building Allen's 35-year pedagogical credibility and top faculty pool in Kota is nearly impossible for newcomers.", "bargaining_power_of_buyers": "Low; parents willingly pay Rs 1.5 Lakhs+ upfront because Allen's topper results speak for themselves.", "bargaining_power_of_suppliers": "Moderate; top faculty members receive multi-crore compensation packages to prevent poaching.", "threat_of_substitutes": "Moderate from online-only platforms (PhysicsWallah, Unacademy), but serious aspirants still prefer physical immersion.", "competitive_rivalry": "High with Aakash Educational Services in NEET, and FIITJEE in JEE."}
    ),
    (
        "Aakash Educational Services", "EdTech, Higher Education & Skill Development",
        "medical doctor aspirants preparing for the National Eligibility cum Entrance Test (NEET)",
        "need comprehensive biological and chemical science test preparation, standardized study modules, and exhaustive national mock test series",
        "Aakash Classroom Medical Coaching & National All India Test Series (AIATS)", "India's Apex Medical NEET Coaching & Test Prep Network",
        "is India's premier medical entrance coaching institution with over 300 physical classroom centers, training tens of thousands of future doctors annually",
        [0.72, 0.92, 0.96, 0.92, 0.86, 0.70],
        {"political": "Directly linked to National Testing Agency (NTA) NEET examination schedules and national medical admissions policies.", "economic": "Generates robust operating cash flows from over 300 physical classroom centers across India; high revenue visibility from multi-year student enrollments.", "social": "Has educated generations of India's medical doctors, creating trusted healthcare practitioners for communities nationwide.", "technological": "Aakash iTutor digital tablets, AIATS computer-adaptive test ranking against 100,000+ peers, and digital classroom smart boards.", "legal": "Coaching regulation compliances, consumer protection norms, and trademark protections.", "environmental": "Energy-efficient coaching centers and transitioning study materials to digital e-books on tablets."},
        [0.20, 0.45, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; replicating Aakash's 300+ physical center network, standardized medical curriculum, and medical faculty is a heavy barrier.", "bargaining_power_of_buyers": "Low to moderate; parents invest heavily in doctor career aspirations and trust Aakash's medical legacy.", "bargaining_power_of_suppliers": "Moderate; medical faculty and biology lecturers.", "threat_of_substitutes": "Moderate from Allen Career Institute and PhysicsWallah.", "competitive_rivalry": "Direct duopoly battle with Allen Career Institute in medical NEET coaching."}
    ),
    (
        "FIITJEE Limited", "EdTech, Higher Education & Skill Development",
        "exceptional mathematical and scientific minds aiming for single-digit All India Ranks in IIT-JEE Advanced",
        "demand the most intellectually rigorous, analytically demanding problem-solving training designed specifically to crack the world's toughest engineering exam",
        "Pinnacle Two-Year Integrated Classroom Program & All India Test Series", "Elite Analytical IIT-JEE Advanced Entrance Preparation",
        "is legendary for producing the highest percentage of top-100 All India Ranks in IIT-JEE Advanced, pioneering integrated school-coaching programs",
        [0.70, 0.90, 0.95, 0.90, 0.84, 0.68],
        {"political": "Complies with state coaching regulations and school education board integrated program guidelines.", "economic": "High-fee pricing structure justified by unmatched success rates in the elite IIT-JEE Advanced ranking lists; strong scholarship exam funnel (FTRE).", "social": "The gold standard for intellectually gifted students seeking admission into the prestigious original IIT campuses (Bombay, Delhi, Kanpur).", "technological": "Computer-based testing engines simulating the exact IIT-JEE Advanced testing interface, and analytical student error-pattern diagnostics.", "legal": "Coaching institute regulatory compliances, trademark protections, and consumer refund policies.", "environmental": "Transitioning to paperless computer-based testing across national examination centers."},
        [0.22, 0.48, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; cracking IIT Advanced requires specialized analytical faculty that take decades to train.", "bargaining_power_of_buyers": "Low; parents of gifted students specifically seek FIITJEE for its unmatched mathematical rigor.", "bargaining_power_of_suppliers": "Moderate; elite IIT alumni teachers.", "threat_of_substitutes": "Moderate from Allen and Resonance.", "competitive_rivalry": "High with Allen Career Institute and Sri Chaitanya."}
    ),
    (
        "Drishti IAS", "EdTech, Higher Education & Skill Development",
        "civil service aspirants preparing for the Union Public Service Commission (UPSC) exams",
        "need deep, intellectually profound, and lucid analysis of constitutional governance, ethics, current affairs, and Hindi/English literature",
        "Drishti UPSC Classroom Foundation & Drishti Current Affairs Journal", "Premier Civil Services Examination Coaching & Knowledge Hub",
        "is India's most respected UPSC coaching institute, founded by beloved educator Dr. Vikas Divyakirti, pioneering Hindi-medium civil service preparation",
        [0.75, 0.92, 0.98, 0.92, 0.86, 0.70],
        {"political": "Prepares future Indian Administrative Service (IAS) and Indian Police Service (IPS) officers who run the national government machinery.", "economic": "Phenomenal organic brand equity; massive student enrollments across Mukherjee Nagar, Karol Bagh, Prayagraj, and Jaipur with zero marketing spend.", "social": "Dr. Vikas Divyakirti's lectures on ethics, philosophy, and history have become viral cultural phenomena watched by tens of millions of citizens.", "technological": "Drishti Learning App with offline video caching, AI essay evaluation guidance, and daily current affairs audio podcasts.", "legal": "Delhi municipal commercial coaching norms, fire safety compliances, and consumer protection adherence.", "environmental": "Promotes digital e-magazines and online testing to reduce paper printouts in civil service study hubs."},
        [0.20, 0.45, 0.30, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; Dr. Divyakirti's intellectual stature, pedagogical clarity, and moral credibility form an unassailable cultural moat.", "bargaining_power_of_buyers": "Low; UPSC aspirants revere Drishti's classroom material and mentorship.", "bargaining_power_of_suppliers": "Low; proprietary curriculum developed by in-house researchers and former civil servants.", "threat_of_substitutes": "Moderate from Vajiram & Ravi and Vision IAS.", "competitive_rivalry": "Low in Hindi medium (undisputed monopoly); moderate in English medium against Vision IAS."}
    ),
    (
        "Khan Global Studies", "EdTech, Higher Education & Skill Development",
        "aspirants from humble rural backgrounds preparing for UPSC, BPSC, SSC, and defence exams",
        "demand deeply engaging, vernacular, and high-energy conceptual teaching delivered with humor, empathy, and rock-bottom affordable fees",
        "Khan Sir UPSC Foundation & State PCS Comprehensive Batches", "Grassroots Affordable Civil Services & Multi-Exam Test Prep",
        "founded by internet teaching sensation Khan Sir, delivering high-level geopolitical and scientific education to millions of students at sub-Rs 5,000 fees",
        [0.75, 0.94, 0.98, 0.92, 0.84, 0.70],
        {"political": "Supports grassroots civic education, national patriotism, and rural student inclusion into state and national civil services.", "economic": "Extraordinary unit economics: millions of students enrolled in digital batches generate massive cash flows despite rock-bottom course pricing.", "social": "Khan Sir is a folk hero across Bihar, UP, and India for his unique, entertaining teaching style that makes complex subjects crystal clear to villagers.", "technological": "High-concurrency streaming app capable of serving millions of concurrent students on basic Android smartphones, and map-based animation graphics.", "legal": "Coaching center safety compliances, registered educational trust governance, and trademark protection.", "environmental": "Digital video delivery saves millions of rural students from burning diesel traveling to distant city coaching hubs."},
        [0.20, 0.45, 0.25, 0.18, 0.55],
        {"threat_of_new_entrants": "Zero; Khan Sir's inimitable personality, comedic pedagogical genius, and massive public love cannot be manufactured.", "bargaining_power_of_buyers": "Low; courses cost mere hundreds to thousands of rupees, making education accessible to all.", "bargaining_power_of_suppliers": "Low; mission-driven internal team.", "threat_of_substitutes": "Low; students specifically demand Khan Sir's teaching style.", "competitive_rivalry": "Low; operates in a unique grassroots mass-market tier alongside PhysicsWallah."}
    ),
    (
        "Great Learning", "EdTech, Higher Education & Skill Development",
        "working IT professionals, business analysts, and corporate managers seeking career acceleration",
        "need comprehensive post-graduate programs in Artificial Intelligence, Data Science, Cloud Computing, and Business Analytics",
        "PG Program in Data Science, AI & Business Analytics", "High-Impact Professional Upskilling & Career Transition Platform",
        "has delivered over 100 million hours of learning across 170+ countries, partnering with premier institutions like UT Austin, Stanford, and Great Lakes",
        [0.72, 0.90, 0.95, 0.95, 0.85, 0.72],
        {"political": "Aligned with India's national AI mission and global executive skill certification standards.", "economic": "Acquired by BYJU'S group and operating with financial autonomy; high-ticket course pricing delivers steady corporate and B2C cash flows.", "social": "Empowered over 10,000 professionals to transition out of legacy IT testing and maintenance roles into high-paying modern AI engineering careers.", "technological": "Olympus learning management engine, cloud-based data science coding notebooks, and personalized AI mentor feedback.", "legal": "University joint-certification compliance, corporate training agreements, and intellectual property protections.", "environmental": "Virtual software development labs eliminate the environmental cost of running physical computer hardware academies."},
        [0.24, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; building university credibility and securing employer corporate hiring partnerships takes time.", "bargaining_power_of_buyers": "Moderate; working professionals research career transition case studies and salary placement reports.", "bargaining_power_of_suppliers": "Moderate; university academic partners and industry mentors.", "threat_of_substitutes": "Moderate from upGrad and Simplilearn.", "competitive_rivalry": "Direct rivalry with upGrad and Simplilearn."}
    ),
    (
        "Masai School", "EdTech, Higher Education & Skill Development",
        "college graduates, non-CS students, and youth seeking guaranteed software engineering jobs",
        "need intensive, hands-on software development training with an outcome-based Pay-After-Placement model (Pay zero tuition until placed in a high-paying tech job)",
        "Military-Style Full Stack Web Development & Data Analytics Bootcamps", "Outcome-Based Pay-After-Placement Coding Bootcamp",
        "pioneered the Pay-After-Placement model in India, training young college graduates through 1,200 hours of intensive coding to place them as software engineers",
        [0.72, 0.92, 0.96, 0.95, 0.84, 0.70],
        {"political": "Supports Skill India and National Skill Development Corporation (NSDC) initiatives on outcome-driven technical employability.", "economic": "Income Share Agreement (ISA) / Pay-After-Placement model aligns incentives completely: Masai only earns when the student secures a job paying >Rs 5 LPA.", "social": "Transforms non-computer-science graduates, rural students, and arts majors into software engineers earning six-figure salaries at tech startups.", "technological": "Automated code evaluation pipelines, GitHub project portfolio building, mock technical interviews, and daily 9-to-9 coding discipline.", "legal": "NBFC education financing partnerships, ISA legal compliance, and consumer protection disclosures.", "environmental": "Virtual digital coding academies replace traditional physical computer laboratories, saving energy and electronic waste."},
        [0.25, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; anyone can run a coding class, but absorbing upfront student training costs and managing placement risk requires capital.", "bargaining_power_of_buyers": "Low; students love the zero upfront tuition model where they only pay after getting placed.", "bargaining_power_of_suppliers": "Low; senior tech engineers and alumni act as instructors.", "threat_of_substitutes": "Moderate from traditional MCA degrees and self-taught online coding resources.", "competitive_rivalry": "Moderate; dominates the outcome-based coding bootcamp segment."}
    ),
    (
        "Scaler (InterviewBit)", "EdTech, Higher Education & Skill Development",
        "working software engineers seeking promotions into elite product companies (Google, Microsoft, Amazon)",
        "need advanced computer science upskilling in data structures, algorithms, distributed system design, and AI from current tech leaders",
        "Scaler Academy & Scaler School of Technology", "Advanced Software Engineering Upskilling & System Design Academy",
        "is the premier upskilling platform for software engineers in India, training 30,000+ developers in distributed systems with top-tier tech placements",
        [0.72, 0.90, 0.95, 0.96, 0.84, 0.72],
        {"political": "Supports national technology leadership and talent creation for India's high-tech semiconductor and software ecosystem.", "economic": "High-margin course fees (>Rs 2.5 Lakhs) with high completion and placement rates; launched Scaler School of Technology offering residential 4-year tech degrees.", "social": "Helps Indian engineers break out of repetitive IT service maintenance work into high-paying global product architecture and AI roles.", "technological": "Algorithmic code evaluation, distributed systems architectural simulation labs, and peer-to-peer code review systems.", "legal": "Consumer protection compliance, transparent placement disclosures, and intellectual property protections.", "environmental": "Digital upskilling models eliminate physical commutes and textbook printing."},
        [0.24, 0.48, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; building Scaler's curriculum depth in complex distributed systems and hiring manager network requires engineering prestige.", "bargaining_power_of_buyers": "Moderate; engineers evaluate placement statistics and average salary hikes (>120%).", "bargaining_power_of_suppliers": "Moderate; tech leaders from Google and Amazon act as paid mentors.", "threat_of_substitutes": "Moderate from LeetCode self-study and competing academies.", "competitive_rivalry": "Moderate; undisputed leader in advanced software engineering upskilling."}
    )
]

for item in sector22_data:
    add_c(*item)

print(f"Sector 22 added: {len(sector22_data)} companies. Total in Part 4B: {len(part4_b)}")

# ==============================================================================
# SECTOR 23: Digital Media, Gaming, Audio & Entertainment (18 companies)
# ==============================================================================
sector23_data = [
    (
        "Dream11 (Sporta Technologies)", "Digital Media, Gaming, Audio & Entertainment",
        "sports fans, cricket enthusiasts, and mobile gaming users across India",
        "want to showcase their sports knowledge, select fantasy teams, and compete with friends for massive cash prizes during live sporting matches",
        "Dream11 Fantasy Cricket & Sports Gaming Platform", "India's Apex Fantasy Sports & Sports Tech Platform",
        "is India's premier sports tech unicorn with 200+ million registered users, transforming sports fandom into interactive engagement as the official IPL partner",
        [0.78, 0.92, 0.98, 0.96, 0.84, 0.70],
        {"political": "Regulated under national online skill-gaming frameworks; recognized by the Supreme Court of India as a constitutionally protected game of skill.", "economic": "Highly profitable cash cow generating hundreds of millions of dollars in revenue; absorbed 28% GST on entry fees through high player retention.", "social": "Deeply integrated into Indian cricket viewing culture; millions of fans follow live matches with their fantasy team leaderboards open.", "technological": "Hyper-concurrency real-time leaderboard processing handling 10+ million simultaneous real-time score updates per second during IPL matches.", "legal": "Supreme Court rulings affirming fantasy sports as games of skill under Article 19(1)(g), and strict IT Ministry online gaming rules.", "environmental": "Pure-play digital entertainment with low carbon footprint; runs on energy-efficient cloud infrastructure."},
        [0.20, 0.48, 0.35, 0.20, 0.65],
        {"threat_of_new_entrants": "Low; network effects of multi-crore prize pools and 200 million sports fans create an insurmountable liquidity moat.", "bargaining_power_of_buyers": "Moderate; sports fans compare platform fees, but play where the prize pools and social friends are concentrated.", "bargaining_power_of_suppliers": "Moderate; sports leagues (BCCI/IPL) command high sponsorship rights.", "threat_of_substitutes": "Moderate from other real-money gaming formats (rummy, casual games).", "competitive_rivalry": "Low to moderate; undisputed market leader ahead of My11Circle and MPL."}
    ),
    (
        "Games24x7", "Digital Media, Gaming, Audio & Entertainment",
        "skill gamers, online rummy enthusiasts, and fantasy sports players across India",
        "demand fair, scientifically validated, and highly secure digital card games (RummyCircle) and sports fantasy leagues (My11Circle)",
        "RummyCircle & My11Circle Fantasy Cricket", "AI-Powered Online Skill Gaming & Behavioral Science Platform",
        "pioneered online rummy in India with RummyCircle, leveraging deep data science and behavioral algorithms to deliver hyper-personalized fair skill gaming",
        [0.78, 0.92, 0.96, 0.96, 0.84, 0.70],
        {"political": "Compliant with Supreme Court skill gaming jurisprudence, state gaming laws, and mandatory 28% GST on online gaming.", "economic": "Exceptional profitability and strong cash reserves; sustained revenue growth driven by high-lifetime-value digital card game players.", "social": "Modernized traditional Indian family card game rituals (rummy) into a secure, skill-based digital pastime.", "technological": "Patented RNG (Random Number Generator) certified by iTech Labs, real-time anti-fraud collusion detection, and AI responsible gaming limits.", "legal": "Supreme Court protection for skill gaming, IT Ministry online gaming self-regulatory guidelines, and strict KYC verification.", "environmental": "Cloud-native digital gaming infrastructure with zero physical paper playing cards or plastic chips."},
        [0.22, 0.48, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; real-money gaming requires deep anti-collusion fraud AI, regulatory compliance, and multi-crore marketing liquidity.", "bargaining_power_of_buyers": "Moderate; players switch between apps based on tournament bonuses, but value Games24x7's instant bank withdrawals.", "bargaining_power_of_suppliers": "Low; in-house proprietary game development.", "threat_of_substitutes": "Moderate from fantasy sports and casual games.", "competitive_rivalry": "High with Junglee Rummy and Dream11."}
    ),
    (
        "Nazara Technologies", "Digital Media, Gaming, Audio & Entertainment",
        "gamers, esports enthusiasts, sports news readers, and young children worldwide",
        "need diversified digital gaming entertainment: competitive esports tournaments, gamified early childhood learning, and real-time sports journalism",
        "Nodwin Gaming Esports, Sportskeeda & Kiddopia Gamified Learning", "India's Premier Listed Diversified Gaming & Esports Conglomerate",
        "is India's only publicly listed gaming and esports giant, operating global esports tournaments (Nodwin), Sportskeeda sports media, and Kiddopia for kids",
        [0.72, 0.90, 0.95, 0.95, 0.84, 0.70],
        {"political": "Key policy stakeholder in Ministry of Electronics and IT (MeitY) gaming policies; actively promotes esports under the Olympic vision.", "economic": "Diversified, non-real-money gaming portfolio cushions business from gambling tax fluctuations; strong recurring US subscription revenues from Kiddopia.", "social": "Pioneered professional esports in India, creating careers for professional gamers and streaming live gaming stadium championships to millions.", "technological": "Live esports broadcast production studios, gamified cognitive learning algorithms, and high-traffic digital sports journalism content engines.", "legal": "Global child privacy compliance (COPPA for Kiddopia), intellectual property game publishing rights, and SEBI listing governance.", "environmental": "Digital entertainment with low physical footprint; operates paperless digital media publishing and cloud esports streaming."},
        [0.22, 0.45, 0.35, 0.20, 0.62],
        {"threat_of_new_entrants": "Low; building Nazara's multi-segment global gaming portfolio (esports, kids IP, sports journalism) requires immense capital.", "bargaining_power_of_buyers": "Moderate; diverse audience across kids, gamers, and sports fans.", "bargaining_power_of_suppliers": "Moderate; game IP holders (Krafton/PUBG, Riot Games) partner with Nodwin for regional tournaments.", "threat_of_substitutes": "Moderate from traditional sports broadcasts and video streaming.", "competitive_rivalry": "Low to moderate; dominates Indian esports and kids subscription gaming."}
    ),
    (
        "WinZO Games", "Digital Media, Gaming, Audio & Entertainment",
        "mobile gamers and youth across Tier-2, Tier-3, and rural India",
        "need hyper-casual, fast-loading mobile multiplayer games (carrom, ludo, chess) localized in their regional mother tongues with micro-transactions",
        "WinZO Vernacular Social Gaming Platform (100+ Games)", "Vernacular Social Gaming & Micro-Transaction Platform for Bharat",
        "operates India's largest social gaming platform with 150+ million registered users, partnering with game developers to distribute 100+ games in 12 regional languages",
        [0.72, 0.90, 0.96, 0.96, 0.84, 0.70],
        {"political": "Compliant with national online gaming guidelines; strong advocate for Indian game developers under Make in India.", "economic": "Micro-transaction economic engine: monetizes small 2-to-10 rupee gameplay fees, generating high cash flow velocity and strong user retention.", "social": "Brings interactive digital fun and social connection to youth in small-town India who play familiar traditional games (Ludo, Carrom) with real opponents.", "technological": "Patented fraud-prevention algorithms, ultra-lightweight game client running on budget smartphones, and automated developer revenue-sharing APIs.", "legal": "Skill gaming legal compliance, state gaming regulations, and strict player identity verification.", "environmental": "Digital entertainment running on scalable cloud infrastructure with zero physical plastic gaming board waste."},
        [0.26, 0.52, 0.38, 0.22, 0.70],
        {"threat_of_new_entrants": "Low to moderate; building a 150-million-user multi-game platform with real-time matchmaking liquidity requires immense scale.", "bargaining_power_of_buyers": "Moderate; youth switch between casual game apps if cash bonuses dry up.", "bargaining_power_of_suppliers": "Low; hundreds of third-party game developers rely on WinZO for monetization.", "threat_of_substitutes": "High from free-to-play mobile games (Ludo King, Free Fire).", "competitive_rivalry": "Direct rivalry with MPL and Zupee."}
    ),
    (
        "Dailyhunt (VerSe Innovation)", "Digital Media, Gaming, Audio & Entertainment",
        "over 350 million non-English speaking citizens across Tier-2, Tier-3, and rural India",
        "need real-time local news, regional language entertainment, and viral short-form videos in their mother tongue without English language barriers",
        "Dailyhunt Vernacular News & Josh Short Video Platform", "India's Apex Vernacular News Discovery & Short Video Platform",
        "is India's premier vernacular media powerhouse with 350+ million users, delivering personalized news and viral short videos (Josh) in 15 Indian languages",
        [0.72, 0.90, 0.98, 0.96, 0.84, 0.70],
        {"political": "Direct beneficiary of Digital India and vernacular internet democratization; compliant with IT Intermediary Guidelines.", "economic": "Achieved multi-billion dollar valuation; high digital advertising monetization from national brands seeking targeted rural and tier-2/3 consumer reach.", "social": "Empowered 350+ million regional language speakers to stay informed about local district news, agriculture schemes, and national elections.", "technological": "Proprietary AI natural language processing (NLP) in 15 Indian scripts, real-time news recommendation graph, and low-latency video streaming.", "legal": "Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, and DPDP Act compliance.", "environmental": "Digital news reading saves millions of trees annually by eliminating physical newsprint paper consumption."},
        [0.25, 0.52, 0.35, 0.25, 0.72],
        {"threat_of_new_entrants": "Low; aggregating 100,000+ local news publisher feeds and training AI recommendation engines in 15 languages is a massive moat.", "bargaining_power_of_buyers": "Moderate; consumers browse for free and have alternative news sources, but love Dailyhunt's unified feed.", "bargaining_power_of_suppliers": "Low; local news publishers depend on Dailyhunt for digital traffic and ad-revenue sharing.", "threat_of_substitutes": "High from YouTube, Instagram Reels, and regional television news.", "competitive_rivalry": "Direct rivalry with Inshorts and ShareChat."}
    ),
    (
        "Inshorts", "Digital Media, Gaming, Audio & Entertainment",
        "busy urban professionals, corporate executives, and youth who have no time to read long newspapers",
        "need crisp, unbiased, and factual news summaries distilled into exactly 60 words, alongside hyper-local neighborhood community updates (Public App)",
        "Inshorts 60-Word News App & Public Hyperlocal Video Platform", "Concise 60-Word News Summaries & Hyperlocal Community Video",
        "pioneered the 60-word news format in India, keeping 10+ million busy professionals informed in seconds, and operating 'Public'—India's largest location-based video app",
        [0.70, 0.88, 0.96, 0.96, 0.84, 0.70],
        {"political": "Complies with digital news media guidelines and IT intermediary rules; maintains strict non-editorial, purely factual reporting.", "economic": "Strong financial profitability driven by high premium digital advertising yields; users open the app multiple times daily for quick news bites.", "social": "Solves information overload for urban youth, providing essential global, national, and business news in a rapid 60-second read.", "technological": "Algorithmic summarization paired with human editorial fact-checkers; hyper-localized video feeds based on precise GPS district tags.", "legal": "Copyright fair use news curation compliance, IT intermediary protections, and consumer data privacy standards.", "environmental": "Paperless digital news delivery eliminating physical paper waste and printing chemicals."},
        [0.26, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; summarizing news is simple, but building Inshorts' 10-million daily habit and brand trust takes years.", "bargaining_power_of_buyers": "Moderate; users appreciate the concise 60-word format and unbundled brevity.", "bargaining_power_of_suppliers": "Low; curated from public wire news feeds (PTI, ANI, Reuters).", "threat_of_substitutes": "Moderate from Twitter/X and Dailyhunt.", "competitive_rivalry": "Moderate; undisputed category leader in concise summary news."}
    ),
    (
        "ShareChat (Mohalla Tech)", "Digital Media, Gaming, Audio & Entertainment",
        "regional language internet users, small-town creators, and Bharat youth",
        "need a comfortable, native social networking space in their mother tongue to share WhatsApp status videos, regional memes, and voice chatrooms",
        "ShareChat Vernacular Social Network & Moj Short Video Platform", "India's Leading Vernacular Social Media & Short-Video Network",
        "is India's premier homegrown social network with over 325 million monthly active users, allowing users to express themselves in 15 Indian languages without English",
        [0.72, 0.90, 0.98, 0.96, 0.84, 0.70],
        {"political": "National champion of domestic social media under Make in India; compliant with IT Intermediary rules and cybersecurity directives.", "economic": "Substantial monetization through live audio chatroom micro-gifting, creator tipping, and targeted vernacular brand advertising.", "social": "Created a safe, culturally resonant digital town square for non-English speaking Indians who felt alienated on western social media apps.", "technological": "AI video recommendation engines (Moj), real-time low-latency multi-speaker audio chatroom infrastructure, and regional language NLP.", "legal": "Information Technology Act intermediary rules, content moderation guidelines, and DPDP Act data protection.", "environmental": "Pure-play cloud software running on energy-efficient cloud data centers with zero physical manufacturing footprint."},
        [0.26, 0.55, 0.35, 0.28, 0.78],
        {"threat_of_new_entrants": "Low; building network effects across 325 million active users and 15 regional languages is an insurmountable barrier.", "bargaining_power_of_buyers": "High; social media users have many entertainment choices and switch if content becomes repetitive.", "bargaining_power_of_suppliers": "Low; millions of grassroots content creators and meme makers.", "threat_of_substitutes": "High from Instagram Reels and YouTube Shorts.", "competitive_rivalry": "Fierce rivalry with Instagram Reels and YouTube Shorts in short videos."}
    ),
    (
        "Pocket FM", "Digital Media, Gaming, Audio & Entertainment",
        "audiobook listeners, long-commute travelers, and serial entertainment lovers in India and the US",
        "demand gripping, serialized episodic audio fiction (romance, fantasy, sci-fi) that can be listened to hands-free while commuting or working",
        "Pocket FM Serialized Audio Fiction & Audio OTT Platform", "Pioneer of Serialized Audio Fiction & Audio Entertainment OTT",
        "created the 'audio series' entertainment category globally, pioneering binge-worthy serialized audio storytelling with millions of paying listeners in India and the US",
        [0.70, 0.88, 0.96, 0.96, 0.84, 0.70],
        {"political": "Complies with digital media ethics codes, copyright licensing, and cross-border digital entertainment regulations.", "economic": "Disruptive micro-payment model: users pay per episode (coin micropayments), generating over $150M in annualized revenue run-rate across India and the US.", "social": "Revitalized the ancient art of oral storytelling, providing immersive audio drama entertainment that prevents screen fatigue and eye strain.", "technological": "AI-driven writer assistance tools, high-fidelity sound engineering with immersive spatial audio effects, and algorithmic story pacing analytics.", "legal": "Original story copyright ownership, writer royalty agreements, and international digital payment compliances.", "environmental": "Zero physical media footprint; audio streaming uses 10x less bandwidth and data center electrical power than video streaming."},
        [0.24, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Low to moderate; building a library of 100,000+ hours of original episodic audio fiction requires deep writer networks and IP.", "bargaining_power_of_buyers": "Moderate; listeners become addicted to serialized cliffhangers and willingly buy coins to unlock the next episode.", "bargaining_power_of_suppliers": "Low; independent creative story writers and voice artists.", "threat_of_substitutes": "Moderate from podcasts (Spotify), audiobooks (Audible), and video OTT.", "competitive_rivalry": "Direct rivalry with Kuku FM in Indian audio streaming."}
    ),
    (
        "Kuku FM", "Digital Media, Gaming, Audio & Entertainment",
        "self-improvement seekers, students, and aspirational youth across non-metro India",
        "need condensed audio book summaries, personal finance lessons, motivational stories, and historical biographies narrated in regional languages",
        "Vernacular Audio Book Summaries & Self-Improvement Podcasts", "Vernacular Audio Learning & Audio Book Platform for Bharat",
        "is India's leading vernacular audio learning platform with over 2.5 million paid subscribers, offering 50,000+ audio summaries in 7 Indian languages",
        [0.70, 0.88, 0.96, 0.96, 0.84, 0.70],
        {"political": "Promotes adult literacy, financial literacy, and personal development in regional languages under Digital India.", "economic": "Highly capital-efficient annual subscription model (Rs 399-899/year); low customer acquisition costs driven by viral educational content snippets.", "social": "Democratized the world's best non-fiction books (Rich Dad Poor Dad, Atomic Habits) for vernacular speakers who cannot read English.", "technological": "Proprietary audio compression technology for smooth streaming on 2G/3G networks, automated voice synthesis, and personalized book recommendation engines.", "legal": "Book summary copyright fair dealing compliance, author licensing partnerships, and consumer subscription rules.", "environmental": "Digital audio books eliminate millions of paper book printings, saving trees and chemical printing inks."},
        [0.25, 0.50, 0.35, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; audio recording is accessible, but building a library of 50,000 vernacular titles with 2.5M paid subscribers creates a moat.", "bargaining_power_of_buyers": "Moderate; small-town listeners find the annual subscription price very affordable for continuous self-learning.", "bargaining_power_of_suppliers": "Low; independent voice actors and content summarizers.", "threat_of_substitutes": "Moderate from Pocket FM and YouTube podcasts.", "competitive_rivalry": "Direct competition with Pocket FM in Indian audio platforms."}
    ),
    (
        "Pratilipi (Nasadiya Technologies)", "Digital Media, Gaming, Audio & Entertainment",
        "vernacular fiction readers, aspiring self-published writers, and Indian language story lovers",
        "demand a massive, free-to-read self-publishing platform for regional language novels, serialized romance, horror, and comics",
        "Pratilipi Self-Publishing Literature, Comics & Audio Web Series", "India's Largest Digital Storytelling & Self-Publishing Platform",
        "is India's largest Indian-language storytelling community, connecting over 350,000 authors with 30+ million monthly readers across 12 languages",
        [0.70, 0.88, 0.96, 0.95, 0.84, 0.70],
        {"political": "Celebrates India's rich linguistic diversity, fostering literature in Tamil, Telugu, Marathi, Bengali, Hindi, and Malayalam.", "economic": "Multi-tier IP monetization: successful written web novels are adapted into Pratilipi Comics, audiobooks, and licensed to OTT video producers.", "social": "Democratized writing in India, turning small-town homemakers, clerks, and teachers into celebrated novelists with millions of readers.", "technological": "Proprietary regional language typography keyboards, automated episodic coin-locking systems, and behavioral reading engagement algorithms.", "legal": "Copyright ownership agreements, digital author royalty distributions, and IT intermediary compliances.", "environmental": "Digital literature reading saves millions of paper book printings and warehouse shipping logistics emissions."},
        [0.22, 0.48, 0.30, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; building a community of 350,000 active Indian-language authors and millions of stories cannot be easily copied.", "bargaining_power_of_buyers": "Moderate; readers read free chapters and pay micro-coins to unlock advance chapters.", "bargaining_power_of_suppliers": "Low; authors benefit from Pratilipi's built-in 30-million reader distribution.", "threat_of_substitutes": "Moderate from physical novels and video streaming.", "competitive_rivalry": "Low to moderate; undisputed leader in regional digital self-published literature."}
    ),
    (
        "Sun TV Network", "Digital Media, Gaming, Audio & Entertainment",
        "over 100 million television viewers and families across Tamil Nadu, Andhra Pradesh, Karnataka, and Kerala",
        "need high-drama television serials, blockbuster South Indian regional movies, news broadcasts, and Sun NXT digital streaming",
        "Sun TV, KTV, Gemini TV & Sun NXT OTT Streaming", "South India's Dominant Regional Broadcasting & Media Titan",
        "is South Asia's most profitable television broadcaster, operating 37 satellite TV channels in 4 languages reaching 95%+ of South Indian households",
        [0.76, 0.94, 0.98, 0.92, 0.88, 0.72],
        {"political": "Founded by Kalanithi Maran; influential regional media institution with deep roots across southern Indian political and cultural discourse.", "economic": "Highest operating profit margins in Indian broadcasting (>60% EBITDA margin) with zero debt and massive cash balances funded by prime-time advertising.", "social": "Sun TV serials are the sacred nightly ritual for tens of millions of South Indian homemakers and families, defining regional pop culture.", "technological": "High-definition satellite uplinking, automated playout centers, and Sun NXT streaming app with multi-lingual audio tracks.", "legal": "Ministry of Information & Broadcasting satellite downlinking licenses, TRAI tariff orders, and copyright film ownership.", "environmental": "Digital broadcast transmission has low environmental footprint; solar rooftop generation across corporate studio facilities."},
        [0.15, 0.45, 0.35, 0.18, 0.50],
        {"threat_of_new_entrants": "Very low; dislodging Sun TV's 30-year regional channel positioning and exclusive prime-time serial habit is impossible.", "bargaining_power_of_buyers": "Low; FMCG advertisers must advertise on Sun TV to reach South Indian consumers.", "bargaining_power_of_suppliers": "Low; production houses and television serial artists rely on Sun TV for prime-time broadcast slots.", "threat_of_substitutes": "Moderate from digital YouTube and Netflix, but traditional TV retains overwhelming reach in the South.", "competitive_rivalry": "Moderate; competes with Zee Tamil and Star Vijay in Tamil; Gemini dominates Telugu."}
    ),
    (
        "Zee Entertainment Enterprises", "Digital Media, Gaming, Audio & Entertainment",
        "multi-lingual Indian families, international diaspora in 170+ countries, and digital streaming viewers",
        "demand multi-genre television drama serials, regional cinema, music broadcasting, and Zee5 digital on-demand streaming",
        "Zee TV, Zee Cinema, Zee Studios & ZEE5 OTT Platform", "Pioneering National Multi-Lingual Broadcasting & Entertainment Network",
        "pioneered private satellite television broadcasting in India in 1992, entertaining over 1.3 billion viewers globally across 50+ channels in 11 languages",
        [0.75, 0.92, 0.96, 0.92, 0.86, 0.70],
        {"political": "Historic pioneer of India's broadcast deregulation; compliant with Ministry of Information & Broadcasting regulations and TRAI tariff orders.", "economic": "Massive content monetization across domestic linear television advertising, subscription cable carriage fees, and ZEE5 digital subscriptions.", "social": "An integral fixture in Indian family living rooms for over three decades; pioneered iconic reality TV formats like Sa Re Ga Ma Pa and Dance India Dance.", "technological": "ZEE5 cloud streaming architecture with multi-CDN delivery, automated video transcoding, and AI personalized content recommendations.", "legal": "TRAI broadcast tariff regulations, Cinematograph Act film certification, and corporate listing governance.", "environmental": "Transitioning physical tape archives to cloud storage and operating energy-efficient broadcast production sets."},
        [0.20, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Low; launching 50 satellite channels and securing cable/DTH distribution into 150 million homes requires immense institutional scale.", "bargaining_power_of_buyers": "Moderate; advertisers allocate budgets across television networks and digital platforms.", "bargaining_power_of_suppliers": "Moderate; Bollywood actors, film producers, and television serial production houses.", "threat_of_substitutes": "High from digital streaming platforms (YouTube, Netflix, JioCinema).", "competitive_rivalry": "Intense rivalry with Star India / Disney-Reliance joint venture."}
    ),
    (
        "PVR INOX", "Digital Media, Gaming, Audio & Entertainment",
        "movie lovers, weekend families, youth, and corporate entertainment seekers across India",
        "demand grand, immersive cinematic experiences: giant IMAX screens, Dolby Atmos sound, luxurious recliner seating, and gourmet cinema dining",
        "PVR INOX Multiplexes, IMAX, 4DX & Director's Cut Luxury Cinemas", "India's Undisputed King of Multiplex Cinema Exhibition",
        "is India's largest film exhibitor following the historic mega-merger of PVR and INOX, operating over 1,700 screens across 360+ cinemas in 115 cities",
        [0.72, 0.92, 0.96, 0.92, 0.86, 0.76],
        {"political": "Complies with state cinema exhibition regulations, local municipal entertainment tax rules, and fire safety codes.", "economic": "Commanding market power: controls over 40% of Indian multiplex box office collections and drives massive high-margin Food & Beverage spends.", "social": "The definitive modern urban weekend entertainment ritual; transformed movie watching from single-screen halls into clean, air-conditioned luxury.", "technological": "Laser 4K projection, immersive Dolby Atmos multi-channel acoustic engineering, IMAX giant formats, and automated online ticket booking.", "legal": "Cinematograph Act certifications, mall anchor lease agreements, and antitrust competition clearances.", "environmental": "Energy-efficient laser projection cutting lamp electrical consumption by 40%; composting food court organic waste."},
        [0.15, 0.45, 0.30, 0.20, 0.55],
        {"threat_of_new_entrants": "Low; securing anchor mall positions, leasing 1,700 screens, and investing thousands of crores in projection equipment is prohibitive.", "bargaining_power_of_buyers": "Moderate; moviegoers choose multiplexes for visual grandeur, but decide visits based on film content quality.", "bargaining_power_of_suppliers": "Moderate to high; Bollywood and Hollywood film studios negotiate net box-office revenue shares.", "threat_of_substitutes": "Moderate from home streaming OTT (Netflix, Prime Video), but blockbuster spectacle films (RRR, KGF, Pathaan) demand the big screen.", "competitive_rivalry": "Low to moderate; undisputed national monopoly in organized multiplex cinema exhibition."}
    ),
    (
        "Saregama India (RP-Sanjiv Goenka Group)", "Digital Media, Gaming, Audio & Entertainment",
        "music lovers, digital streaming platforms, filmmakers, and retro nostalgia seekers",
        "need access to India's most iconic music catalog (Lata Mangeshkar, Kishore Kumar, RD Burman) and physical nostalgia music players (Carvaan)",
        "Saregama Music Library (140,000+ songs) & Saregama Carvaan", "India's Oldest Music Label, Publisher & Nostalgia Audio Device",
        "owns the most valuable music copyright vault in India with 140,000+ tracks spanning 120 years, earning perpetual digital streaming royalties on every platform",
        [0.72, 0.92, 0.96, 0.94, 0.86, 0.74],
        {"political": "Direct beneficiary of Indian Copyright Act amendments enforcing statutory royalty payments to music publishers across all digital media.", "economic": "Phenomenal pure-margin royalty engine: legacy songs incur zero marginal cost, earning compounding perpetual royalties from Spotify, YouTube, and Meta.", "social": "Preserves India's cultural musical soul; 'Carvaan' retro portable music player became the definitive emotional gift from adult children to elderly parents.", "technological": "AI digital audio remastering converting century-old analog recordings into pristine 24-bit lossless digital audio tracks.", "legal": "Indian Copyright Act statutory licensing, global digital music publishing rights, and trademark protections.", "environmental": "Digital streaming distribution produces zero physical plastic waste; Carvaan designed for multi-year durability."},
        [0.12, 0.38, 0.25, 0.15, 0.45],
        {"threat_of_new_entrants": "Zero; nobody can recreate the master recordings of Kishore Kumar, Mohammed Rafi, and Lata Mangeshkar.", "bargaining_power_of_buyers": "Low; digital streaming platforms (Spotify, Apple Music, YouTube) must license Saregama's catalog to attract Indian listeners.", "bargaining_power_of_suppliers": "Low; owns perpetual master copyrights to over 140,000 songs.", "threat_of_substitutes": "Low; classic golden-era Bollywood music cannot be substituted.", "competitive_rivalry": "Low to moderate; oligopoly with T-Series and Tips in music rights."}
    ),
    (
        "TIPS Industries", "Digital Media, Gaming, Audio & Entertainment",
        "music streaming listeners, Bollywood film lovers, and YouTube audiences globally",
        "need iconic 90s and 2000s Bollywood romantic hits and chart-topping contemporary music for digital streaming and social video creation",
        "Tips Bollywood Music Library & Digital Streaming Catalog", "Pure-Play Music Royalty & Audio Publishing Powerhouse",
        "is a pure-play music publishing powerhouse with 30,000+ iconic tracks, generating high-margin cash flows from 90+ million YouTube subscribers and global streaming",
        [0.70, 0.92, 0.96, 0.94, 0.85, 0.72],
        {"political": "Protected under national and international intellectual property laws and digital copyright frameworks.", "economic": "Exceptional business economics: EBITDA margins consistently >65% and return on capital >70% with zero debt and zero physical production assets.", "social": "Soundtrack of a generation: 90s Bollywood romance (Kumar Sanu, Alka Yagnik) enjoys massive nostalgic viral resurgence on Instagram Reels.", "technological": "Direct digital distribution via automated digital ingestion pipelines to Spotify, YouTube, Apple Music, and Amazon Music.", "legal": "Copyright Act compliance, automated digital rights management (Content ID) enforcement on YouTube, and SEBI listing governance.", "environmental": "100% green digital business with near-zero physical resource intensity and zero manufacturing waste."},
        [0.12, 0.38, 0.25, 0.15, 0.45],
        {"threat_of_new_entrants": "Zero; impossible to re-record iconic 90s blockbuster film soundtracks that form the bedrock of Indian pop culture.", "bargaining_power_of_buyers": "Low; streaming platforms require Tips's music catalog for Indian user retention.", "bargaining_power_of_suppliers": "Low; owns perpetual master sound recordings.", "threat_of_substitutes": "Low; specific beloved songs cannot be substituted.", "competitive_rivalry": "Low to moderate; operates alongside T-Series and Saregama in the music copyright oligopoly."}
    ),
    (
        "Shemaroo Entertainment", "Digital Media, Gaming, Audio & Entertainment",
        "classic cinema lovers, regional language audiences, and devotional viewers across India and overseas",
        "need classic Hindi films, regional Gujarati and Marathi cinema, devotional Bhakti content, and syndicated digital video feeds",
        "ShemarooMe OTT Streaming & Classic Bollywood Film Library", "Classic Bollywood Film Content, Devotional Media & Regional OTT",
        "has entertained India for over 60 years, curating over 3,700 classic film titles and dominating devotional video content on digital channels",
        [0.70, 0.90, 0.95, 0.92, 0.85, 0.70],
        {"political": "Complies with Ministry of Information & Broadcasting digital content guidelines and copyright licensing frameworks.", "economic": "Steady revenue syndication to third-party OTT platforms (Netflix, Prime Video), linear satellite channels, and digital YouTube ad revenues.", "social": "The guardian of classic Hindi and Gujarati cinema, bringing wholesome multi-generational entertainment to family households.", "technological": "High-definition 4K digital film restoration, digital rights management (DRM), and multi-platform OTT app deployment.", "legal": "Film copyright acquisitions, music synchronization agreements, and corporate governance compliance.", "environmental": "Digital streaming replaces legacy physical DVD/VCD plastic discs, eliminating packaging and electronic scrap."},
        [0.22, 0.48, 0.35, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; acquiring perpetual rights to thousands of vintage Bollywood films requires decades of capital deployments.", "bargaining_power_of_buyers": "Moderate; OTT platforms negotiate content syndication packages.", "bargaining_power_of_suppliers": "Low; extensive owned perpetual intellectual property library.", "threat_of_substitutes": "Moderate from new release movies and modern web series.", "competitive_rivalry": "Moderate; competes with Ultra Media and regional content distributors."}
    ),
    (
        "Mobile Premier League (MPL)", "Digital Media, Gaming, Audio & Entertainment",
        "mobile gamers, casual esports players, and competitive gaming fans across India, US, and Nigeria",
        "need competitive casual gaming tournaments (chess, 8-ball pool, fruit chop) with instant digital matchmaking and fair cash rewards",
        "MPL Mobile Gaming Platform & Casual Esports Tournaments", "Multi-Game Casual Esports & Skill Gaming Platform",
        "is a premier mobile gaming unicorn with 90+ million registered users, offering a wide array of competitive skill games and expanding into international gaming markets",
        [0.72, 0.90, 0.96, 0.95, 0.84, 0.70],
        {"political": "Complies with IT Ministry online gaming regulations, fair skill gaming classifications, and state-level legal frameworks.", "economic": "Expanding international presence in the United States and Africa to diversify revenue away from domestic gaming tax pressures.", "social": "Connects gamers across diverse geographical regions in friendly, real-time skill-based competitive sports and board games.", "technological": "Low-latency multiplayer game networking, proprietary anti-cheat security protocols, and automated instant UPI prize payouts.", "legal": "Skill gaming legal certifications, strict KYC verification, and international digital gaming compliance.", "environmental": "Cloud-based digital entertainment with zero physical gaming equipment manufacturing footprint."},
        [0.26, 0.52, 0.38, 0.22, 0.72],
        {"threat_of_new_entrants": "Moderate; casual games can be built, but MPL's player liquidity and matchmaking scale create a barrier.", "bargaining_power_of_buyers": "Moderate; gamers switch between apps based on tournament prize formats.", "bargaining_power_of_suppliers": "Low; in-house game development and revenue-share game publishers.", "threat_of_substitutes": "High from WinZO and standalone free-to-play mobile games.", "competitive_rivalry": "High with WinZO, Zupee, and Dream11."}
    ),
    (
        "Hungama Digital Media", "Digital Media, Gaming, Audio & Entertainment",
        "music listeners, telecom digital value-added service users, and regional video watchers",
        "need multi-lingual music streaming, Bollywood movie libraries, and gamified digital entertainment integrated with mobile telecom plans",
        "Hungama Music, Hungama Play & Hefty Games Web3 Platform", "Digital Music Streaming, Video OTT & Gaming Publisher",
        "is a pioneer of digital entertainment in India, providing digital music streaming, video OTT, and gaming content across 40+ countries",
        [0.70, 0.88, 0.95, 0.94, 0.84, 0.70],
        {"political": "Compliant with national digital content guidelines, telecom value-added service regulations, and copyright laws.", "economic": "Multi-channel monetization: direct-to-consumer app subscriptions, B2B bundling with major telecom carriers (Airtel, Vi), and international syndication.", "social": "Brought digital music and ringtones to Indian mobile users in the early 2000s, pioneering digital entertainment consumption.", "technological": "Cloud-based audio/video streaming, high-compression codecs for low-bandwidth networks, and Web3 gaming integrations.", "legal": "Music label licensing agreements, film distribution rights, and data protection compliance.", "environmental": "Digital streaming eliminates physical CD and DVD media manufacturing and packaging."},
        [0.25, 0.50, 0.38, 0.22, 0.68],
        {"threat_of_new_entrants": "Moderate; basic streaming apps can be created, but securing multi-label music licenses requires capital.", "bargaining_power_of_buyers": "High; users choose between Spotify, Wynk, JioSaavn, and YouTube Music.", "bargaining_power_of_suppliers": "High; major music labels (T-Series, Sony Music, Saregama) set licensing rates.", "threat_of_substitutes": "High from global music giants (Spotify, YouTube).", "competitive_rivalry": "Intense rivalry with Spotify, JioSaavn, and Gaana."}
    )
]

for item in sector23_data:
    add_c(*item)

print(f"Sector 23 added: {len(sector23_data)} companies. Total in Part 4B: {len(part4_b)}")

# ==============================================================================
# SECTOR 24: B2B Industrial Commerce, Manufacturing & Contract Electronics (16 companies)
# ==============================================================================
sector24_data = [
    (
        "Dixon Technologies", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "global consumer electronics giants (Samsung, Xiaomi, Motorola), telecom hardware makers, and lighting brands",
        "require massive, high-precision electronics manufacturing services (EMS), Surface Mount Technology (SMT) assembly, and rapid local scaling under Make in India",
        "EMS Manufacturing for Smart TVs, Smartphones, Laptops & Home Appliances", "India's Apex Electronic Manufacturing Services (EMS) Giant",
        "is India's largest domestic electronics manufacturer, producing over 30 million LED TVs, smartphones, laptops, and washing machines across 23 mega-factories",
        [0.85, 0.94, 0.96, 0.95, 0.86, 0.75],
        {"political": "Crown jewel of Government of India's Electronics Production Linked Incentive (PLI) scheme, driving mobile and IT hardware indigenization.", "economic": "Hyper-efficient manufacturing model with high asset turns, generating explosive revenue growth (>Rs 20,000 Cr) and strong return on capital (ROCE >30%).", "social": "Created over 25,000 skilled industrial electronics assembly jobs for Indian youth and women, transforming Noida into a global electronics hub.", "technological": "High-speed automated SMT lines placing 100,000 components per hour, cleanroom semi-conductor chip packaging, and robotic testing jigs.", "legal": "BIS electronics certifications, customs duty bonded manufacturing (MOOWR) compliance, and global customer quality audits.", "environmental": "Lead-free soldering processes, ISO 14001 certified green factories, and comprehensive e-waste recycling management."},
        [0.22, 0.52, 0.42, 0.22, 0.65],
        {"threat_of_new_entrants": "Low; building Dixon's 23-factory scale, automated SMT density, and tier-1 global brand trust requires billions in capital.", "bargaining_power_of_buyers": "Moderate; global electronics brands negotiate tight per-unit assembly margins, but depend heavily on Dixon to meet Indian PLI local value addition.", "bargaining_power_of_suppliers": "Moderate; display panels and semiconductor chipsets.", "threat_of_substitutes": "Moderate from international EMS giants (Foxconn India, Pegatron).", "competitive_rivalry": "Moderate; clear domestic market leader in consumer electronics EMS."}
    ),
    (
        "Amber Enterprises", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "leading room air conditioner brands (Voltas, Daikin, LG, Panasonic) and railway coach builders",
        "need outsourced original equipment design (ODM/OEM) manufacturing of air conditioners, inverter printed circuit boards, and railway HVAC systems",
        "Room Air Conditioner OEM/ODM Manufacturing & Railway HVAC Units", "Market-Dominating Air Conditioner ODM/OEM Manufacturer",
        "dominates Indian outsourced room AC manufacturing with over 70% market share, manufacturing air conditioners and critical components for top consumer brands",
        [0.80, 0.92, 0.96, 0.95, 0.86, 0.78],
        {"political": "Prime beneficiary of the Production Linked Incentive (PLI) for White Goods (air conditioners and LED components).", "economic": "Unmatched scale in AC manufacturing: backward-integrated into heat exchangers, sheet metal, injection molding, and inverter PCB assemblies.", "social": "Drives industrialization in non-metro manufacturing zones (Dehradun, Jhajjar, Pune), providing skilled assembly employment.", "technological": "Advanced heat exchanger copper fin forming, automated leak testing using helium mass spectrometers, and high-speed PCB surface mounting.", "legal": "BEE star rating compliance for manufactured ACs, BIS standards, and industrial factory safety regulations.", "environmental": "Manufactures air conditioners using eco-friendly R32 refrigerant; high-efficiency automated brazing reducing industrial gas emissions."},
        [0.18, 0.48, 0.40, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; building an integrated AC manufacturing capacity producing millions of units with full component backward integration is prohibitive.", "bargaining_power_of_buyers": "Moderate; AC brands negotiate pricing, but rely on Amber because building captive factories would cost more.", "bargaining_power_of_suppliers": "Moderate; rotary compressors (GMCC, Highly) and copper tubes.", "threat_of_substitutes": "Low; AC brands prefer outsourcing manufacturing to focus on marketing and distribution.", "competitive_rivalry": "Low to moderate; undisputed domestic monopoly in outsourced room AC manufacturing ahead of PG Electroplast."}
    ),
    (
        "Kaynes Technology India", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "defense aerospace agencies, Indian Railways, automotive EV makers, and industrial automation clients",
        "require ultra-high-reliability printed circuit board assemblies (PCBA), box builds, and specialized electronics for mission-critical applications",
        "Mission-Critical Defense, Aerospace & Railway Signaling Electronics", "High-Reliability Integrated Electronics Manufacturer (EMS)",
        "is India's premier high-reliability EMS player with 3+ decades of pedigree, manufacturing safety-critical signaling for Indian Railways and avionics for ISRO",
        [0.82, 0.90, 0.95, 0.96, 0.88, 0.75],
        {"political": "Direct beneficiary of Electronics PLI, SPECS capital subsidies, and setting up advanced semiconductor outsourced assembly and testing (OSAT) in Gujarat.", "economic": "High operating margins (>14% EBITDA) driven by specialized, low-volume high-mix mission-critical electronics with multi-year order books.", "social": "Ensures the safety of millions of railway passengers by manufacturing fail-safe automated train protection and railway electronic interlocking systems.", "technological": "Cleanroom electronic assembly, 3D X-ray inspection of multi-layer PCBAs, conformal coating, and advanced semiconductor packaging.", "legal": "Stringent aerospace certifications (AS9100D), defense clearances, and Indian Railways safety standards (CENELEC SIL-4).", "environmental": "Lead-free soldering processes, zero-effluent discharge PCBA cleaning, and solar-assisted manufacturing campuses in Mysuru and Manesar."},
        [0.20, 0.45, 0.40, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; qualifying for nuclear, aerospace, and SIL-4 railway safety takes over 5 years of continuous auditing and zero-defect records.", "bargaining_power_of_buyers": "Low to moderate; mission-critical clients cannot compromise on reliability and remain sticky long-term partners.", "bargaining_power_of_suppliers": "Moderate; aerospace-grade electronic semiconductors and precision passives.", "threat_of_substitutes": "Low; mission-critical systems require certified specialized electronic fabrication.", "competitive_rivalry": "Moderate; competes with Syrma SGS and Cyient DLM in high-mix electronics."}
    ),
    (
        "Syrma SGS Technology", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "medical device makers, automotive electronics Tier-1s, industrial IoT companies, and RFID logistics users",
        "demand precision design-led electronic manufacturing, custom magnetic components, RFID tags, and medical diagnostic hardware",
        "Custom Magnetics, RFID Transponders & Medical Electronic Assemblies", "Design-Led Electronics Manufacturing Services (EMS)",
        "is a pioneer in precision electronics manufacturing, having manufactured over 3 billion specialized electronic components and RFID tags across 12 facilities",
        [0.78, 0.90, 0.95, 0.95, 0.86, 0.75],
        {"political": "Supported under Electronics PLI and Make in India medical devices missions; active exporter of precision magnetics to Europe and USA.", "economic": "Diversified high-margin product mix: industrial, automotive, and healthcare electronics provide resilient, non-cyclical cash flows.", "social": "Manufactures life-saving electronic sub-assemblies for medical patient monitors, X-ray machines, and automated external defibrillators.", "technological": "High-precision automated coil winding for magnetic chokes, micro-RFID tag bonding, and automated optical PCBA inspection.", "legal": "ISO 13485 medical device quality certifications, IATF 16949 automotive standards, and international RoHS/REACH compliances.", "environmental": "RoHS compliant lead-free electronics assembly, closed-loop flux cleaning, and captive solar installations."},
        [0.22, 0.48, 0.40, 0.22, 0.62],
        {"threat_of_new_entrants": "Low to moderate; medical device and precision magnetics certifications require multi-year customer audits.", "bargaining_power_of_buyers": "Moderate; global OEM clients evaluate precision tolerances and engineering design capabilities.", "bargaining_power_of_suppliers": "Moderate; active semiconductor components and copper magnet wire.", "threat_of_substitutes": "Low; specialized custom magnetics and electronics have no alternatives.", "competitive_rivalry": "Moderate with Kaynes Technology and Cyient DLM."}
    ),
    (
        "Infra.Market", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "infrastructure contractors, real estate builders, and commercial project developers",
        "need centralized, transparent procurement of ready-mix concrete (RMC), cement, structural steel, tiles, and aggregates with guaranteed on-site delivery",
        "Tech-Enabled Construction Materials Procurement & Ready-Mix Concrete", "B2B Construction Materials Procurement & Private Label Manufacturing",
        "revolutionized India's construction supply chain, utilizing proprietary tech to deliver ready-mix concrete, cement, and steel to mega-infrastructure projects",
        [0.76, 0.92, 0.96, 0.94, 0.85, 0.74],
        {"political": "Direct beneficiary of National Infrastructure Pipeline (NIP) and formalization of construction materials trade under GST.", "economic": "Achieved unicorn status with strong profitability; backward-integrated into contract-manufacturing cement, concrete, and chemicals under its own private label.", "social": "Supplies certified, laboratory-tested concrete and construction materials for metro rail viaducts, expressways, and affordable housing.", "technological": "GPS tracking of ready-mix concrete transit mixers to prevent curing delays, automated batching plant quality telemetry, and digital procurement apps.", "legal": "BIS construction material certifications, RMC plant quality audits, and legal commercial contracting.", "environmental": "Promotes green concrete utilizing industrial fly ash and ground granulated blast-furnace slag (GGBS), cutting concrete carbon footprint by 30%."},
        [0.26, 0.52, 0.35, 0.24, 0.68],
        {"threat_of_new_entrants": "Moderate; tech platforms can be built, but managing physical ready-mix batching plants and heavy logistics is capital intensive.", "bargaining_power_of_buyers": "Moderate; contractors demand competitive pricing, but value Infra.Market's delivery timeliness to prevent work stoppages.", "bargaining_power_of_suppliers": "Low to moderate; cement mills and steel fabricators rely on Infra.Market for massive bulk off-take.", "threat_of_substitutes": "Moderate from dealing directly with fragmented local cement and stone suppliers.", "competitive_rivalry": "Moderate; clear dominant leader in tech-enabled construction materials."}
    ),
    (
        "Zetwerk Manufacturing", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "global industrial OEMs, energy infrastructure companies, and consumer tech brands across North America and India",
        "require custom precision manufacturing, heavy metal fabrication, CNC machining, and die casting delivered with guaranteed quality and on-time global shipping",
        "Custom Precision Metal Fabrication & Universal Manufacturing Network", "Global Contract Manufacturing & Precision Engineering Marketplace",
        "operates the world's largest universal manufacturing network with 10,000+ vetted factory partners, executing multi-thousand-ton precision fabrication globally",
        [0.76, 0.92, 0.95, 0.96, 0.85, 0.75],
        {"political": "Major engine of Make in India exports, enabling global companies to diversify manufacturing supply chains away from China to India.", "economic": "Achieved multi-billion dollar valuation and strong global revenue growth (>Rs 15,000 Cr) across aerospace, defense, solar, and industrial machinery.", "social": "Empowers thousands of small Indian precision machine workshops with steady global purchase orders, digitizing the MSME industrial ecosystem.", "technological": "Zetwerk Operating System (ZOS) providing real-time tracking of manufacturing stages across factories, automated CAD DFM analysis, and computerized quality checks.", "legal": "International manufacturing certifications (ASME, ISO 9001), export compliance, and commercial contract arbitration.", "environmental": "Optimizes workshop production capacity, eliminating idle energy waste and implementing scrap metal recycling across partner factories."},
        [0.22, 0.48, 0.35, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; building a vetted network of 10,000 fabrication workshops with guaranteed quality liability across North America and India is a massive moat.", "bargaining_power_of_buyers": "Moderate; international OEMs negotiate competitive batch pricing, but rely on Zetwerk for end-to-end quality guarantees.", "bargaining_power_of_suppliers": "Low; small precision machine workshops depend on Zetwerk for high-volume export business.", "threat_of_substitutes": "Moderate from direct factory sourcing in China or Vietnam.", "competitive_rivalry": "Low to moderate; unique dominant pioneer in global B2B contract manufacturing from India."}
    ),
    (
        "Moglix", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "manufacturing enterprises, auto plants, infrastructure sites, and corporate procurement heads",
        "need streamlined, digital procurement of maintenance, repair, and operations (MRO) supplies, industrial tools, safety gear, and electrical equipment",
        "Enterprise Digital MRO Procurement & Moglix Industrial Marketplace", "B2B Industrial Commerce & Digital Supply Chain Platform",
        "is India's largest B2B industrial e-commerce platform with 500,000+ industrial SKUs, automating procurement for over 500 large enterprise manufacturing plants",
        [0.72, 0.92, 0.95, 0.95, 0.84, 0.72],
        {"political": "Supports industrial supply chain formalization under Digital India and GST; backed by Ratan Tata.", "economic": "Unicorn industrial platform; high customer retention (>95%) among enterprise manufacturing plants by eliminating procurement leakages.", "social": "Equips millions of industrial factory workers with certified safety helmets, boots, and personal protective equipment (PPE).", "technological": "AI-powered vendor catalog mapping, automated GST invoice reconciliation, computerized punch-out catalogs, and warehouse inventory ERPs.", "legal": "BIS industrial safety equipment compliance, Legal Metrology, and commercial B2B contract standards.", "environmental": "Digital purchase orders and consolidated enterprise shipments eliminate thousands of redundant delivery trips, cutting transport emissions."},
        [0.25, 0.50, 0.32, 0.22, 0.65],
        {"threat_of_new_entrants": "Low to moderate; integrating with large corporate SAP/ERP systems and managing 500,000 industrial SKUs is a heavy barrier.", "bargaining_power_of_buyers": "Moderate; enterprise procurement managers demand volume discounts, but appreciate consolidated invoicing.", "bargaining_power_of_suppliers": "Low; tool manufacturers and safety brands rely on Moglix for national corporate distribution.", "threat_of_substitutes": "Moderate from traditional fragmented industrial hardware distributors.", "competitive_rivalry": "Moderate; dominates organized B2B industrial MRO procurement."}
    ),
    (
        "OfBusiness (Oxyzo Financial)", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "SME manufacturers, engineering fabrication workshops, and construction contractors",
        "require direct bulk procurement of raw materials (steel, polymers, chemicals, agricultural commodities) integrated with flexible working capital financing",
        "Bulk Raw Material Procurement & Oxyzo SME Working Capital Credit", "Integrated B2B Raw Material Commerce & SME Fintech Ecosystem",
        "is India's most profitable B2B commerce unicorn, uniquely combining high-volume raw material procurement (steel, polymers) with licensed NBFC cash-flow lending",
        [0.75, 0.94, 0.96, 0.95, 0.86, 0.74],
        {"political": "Direct contributor to MSME industrial empowerment; compliant with RBI NBFC lending norms and national digital trade frameworks.", "economic": "Phenomenal profitability: generated hundreds of crores in net profit by charging commerce take-rates while earning high-margin interest on working capital loans.", "social": "Unlocks critical liquidity for thousands of small Indian manufacturing workshops that traditional banks refuse to lend to without property collateral.", "technological": "Proprietary BidWork algorithmic raw material price discovery engine, automated GST transaction data underwriting, and digital e-way bill tracking.", "legal": "RBI non-banking financial company statutory regulations, fair practices code, and commercial contract compliances.", "environmental": "Bulk freight consolidation eliminates empty truck transport miles across industrial corridors."},
        [0.22, 0.48, 0.30, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; combining multi-thousand-crore bulk material trading with a licensed, profitable credit lending engine requires deep capital and risk underwriting.", "bargaining_power_of_buyers": "Low to moderate; SME workshops rely on OfBusiness for both raw material supply and financing.", "bargaining_power_of_suppliers": "Low to moderate; primary steel mills (SAIL, JSW) and polymer refiners appreciate OfBusiness's guaranteed cash off-take.", "threat_of_substitutes": "Moderate from traditional wholesale mandis and unorganized money lenders.", "competitive_rivalry": "Low to moderate; unique dominant dual-engine business model."}
    ),
    (
        "Bizongo", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "consumer brands, e-commerce giants, and pharmaceutical companies",
        "need custom packaging design, on-demand packaging procurement (corrugated boxes, pouches, labels), and automated supply chain vendor financing",
        "Procure Live Packaging Platform & Supply Chain Financing", "Tech-Enabled Custom Packaging & Vendor Management Platform",
        "is India's leading tech-enabled custom packaging and B2B vendor management platform, automating packaging procurement for top enterprises nationwide",
        [0.72, 0.90, 0.95, 0.95, 0.84, 0.72],
        {"political": "Supports plastic waste reduction policies, Extended Producer Responsibility (EPR), and sustainable packaging transitions.", "economic": "Achieved unicorn valuation; asset-light technology platform managing hundreds of packaging manufacturers with integrated invoice discounting.", "social": "Empowers small family-owned paper corrugated box and printing workshops with steady, high-margin corporate purchase orders.", "technological": "Automated 3D packaging structural design tools, digital artwork approval workflows, and algorithmic inventory replenishment tracking.", "legal": "Packaging legal metrology regulations, EPR environmental compliance certificates, and commercial B2B contract terms.", "environmental": "Pioneering sustainable, biodegradable, and recycled paper packaging alternatives that replace single-use plastics across e-commerce."},
        [0.25, 0.50, 0.35, 0.22, 0.65],
        {"threat_of_new_entrants": "Moderate; software platforms can be built, but managing multi-category packaging production across hundreds of vendors requires execution scale.", "bargaining_power_of_buyers": "Moderate; enterprise clients negotiate volume packaging rates.", "bargaining_power_of_suppliers": "Low; packaging converters and printers depend on Bizongo for enterprise demand.", "threat_of_substitutes": "Moderate from direct dealing with local box manufacturers.", "competitive_rivalry": "Low to moderate; dominant leader in tech-enabled custom packaging."}
    ),
    (
        "Captain Fresh", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "fish retailers, supermarket chains, restaurants, and global seafood export processors",
        "require freshly landed, graded, and temperature-controlled ocean fish and seafood with transparent digital auctions and unbroken cold chains",
        "Tech-Enabled B2B Seafood Harvest Platform & Coastal Chilling Hubs", "B2B Farm-to-Retail Seafood Supply Chain Platform",
        "is a tech-driven B2B seafood supply chain unicorn, aggregating marine harvest from coastal fishermen across 40+ landing centers and distributing to 30+ cities",
        [0.70, 0.90, 0.95, 0.94, 0.84, 0.72],
        {"political": "Direct beneficiary of Pradhan Mantri Matsya Sampada Yojana (PMMSY) modernizing coastal fisheries and seafood cold chains.", "economic": "High-velocity B2B commerce with rapid inventory turns; expanding profitable export distribution channels into the US and European seafood markets.", "social": "Empowers artisanal coastal fishermen with fair, transparent, app-based auction price realization within minutes of landing their boats.", "technological": "Computer-vision fish sizing and grading algorithms, automated cold-storage temperature telemetry, and predictive demand matching.", "legal": "FSSAI seafood processing compliance, Marine Products Export Development Authority (MPEDA) approvals, and export veterinary certifications.", "environmental": "Slashes post-harvest marine seafood spoilage from the typical 35% down to under 3%, preventing unnecessary oceanic overfishing."},
        [0.25, 0.50, 0.38, 0.22, 0.65],
        {"threat_of_new_entrants": "Low to moderate; setting up chilled collection infrastructure across 40 coastal fishing harbors requires deep local marine networks.", "bargaining_power_of_buyers": "Moderate; seafood retailers require dependable daily morning supply of fresh, non-spoiled fish.", "bargaining_power_of_suppliers": "Low to moderate; fishermen prefer Captain Fresh's prompt digital bank payments over delayed mandi broker credit.", "threat_of_substitutes": "Moderate from traditional wholesale coastal fish mandis.", "competitive_rivalry": "Low to moderate; pioneer and dominant market leader in tech-driven B2B seafood supply."}
    ),
    (
        "Cyient DLM", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "aerospace defense contractors, commercial avionics makers, and medical tech corporations",
        "need design-led, high-reliability electronic manufacturing services (EMS) for safety-critical aircraft cockpits, flight controls, and medical diagnostic systems",
        "Avionics Cockpit Electronics, Navigation Systems & Defense EMS", "Design-Led High-Reliability Electronics Manufacturing (EMS)",
        "is a pure-play design-led manufacturing specialist, providing mission-critical electronics for global aerospace giants and Indian defense forces",
        [0.80, 0.90, 0.95, 0.96, 0.88, 0.74],
        {"political": "Key partner for aerospace defense indigenization under Make in India; holds high-level defense production clearances.", "economic": "Strong financial profile with high return on invested capital; long-term multi-year contracts with global tier-1 aerospace systems integrators.", "social": "Secures passenger air travel safety by manufacturing zero-failure cockpit displays and fly-by-wire flight control electronics.", "technological": "Precision surface mount assembly in Class 100,000 cleanrooms, automated optical and 3D X-ray inspection, and environmental stress screening.", "legal": "AS9100D aerospace certification, FAA/EASA compliant manufacturing standards, and defense security clearances.", "environmental": "Zero-discharge effluent treatment for electronic flux cleaning, lead-free soldering processes, and energy-efficient manufacturing."},
        [0.20, 0.45, 0.40, 0.20, 0.58],
        {"threat_of_new_entrants": "Low; achieving flight-worthy aerospace certifications and qualifying as a supplier to Boeing and Airbus contractors takes over 5 years.", "bargaining_power_of_buyers": "Moderate; aerospace clients demand strict quality adherence and audit facilities continuously.", "bargaining_power_of_suppliers": "Moderate; specialized aerospace-certified electronic microchips and passives.", "threat_of_substitutes": "Low; critical avionics require certified high-reliability manufacturing.", "competitive_rivalry": "Moderate with Kaynes Technology and Centum Electronics."}
    ),
    (
        "Avalon Technologies", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "clean-tech solar inverter makers, industrial robotics, telecom infrastructure, and aerospace companies",
        "require fully integrated electronic manufacturing: PCB assembly, precision sheet metal fabrication, cable harnesses, and aerospace magnetics under one roof",
        "Full-Stack Box-Build Manufacturing, Cable Harnesses & Clean-Tech EMS", "End-to-End Box-Build & Precision Electronic Manufacturing",
        "is an integrated electronic manufacturing powerhouse with 12 manufacturing units across India and the US, delivering complete finished box-build assemblies",
        [0.78, 0.90, 0.95, 0.95, 0.86, 0.74],
        {"political": "Direct beneficiary of global supply chain diversification and US-India bilateral clean energy manufacturing agreements.", "economic": "High-margin box-build model: full integration from metal enclosures and cable harnesses to electronic assembly captures higher margins than pure assembly.", "social": "Produces critical electronics for clean solar inverters and medical ventilators, enabling green energy and advanced healthcare.", "technological": "Clean-tech power electronics manufacturing, automated wire harness crimping, CNC precision metal machining, and automated functional testing.", "legal": "AS9100 aerospace certification, ISO 13485 medical device standards, and international export compliances.", "environmental": "Lead-free soldering processes, captive solar rooftop generation, and complete metal scrap recycling."},
        [0.22, 0.48, 0.40, 0.22, 0.62],
        {"threat_of_new_entrants": "Low; providing end-to-end box-builds across sheet metal, plastics, cable harnesses, and PCB assembly requires diverse capital assets.", "bargaining_power_of_buyers": "Moderate; global industrial OEMs negotiate long-term delivery contracts.", "bargaining_power_of_suppliers": "Moderate; specialized electronic components and metal alloys.", "threat_of_substitutes": "Low; complex industrial box-builds require dedicated integrated manufacturing.", "competitive_rivalry": "Moderate; competes with Syrma SGS and Kaynes Technology."}
    ),
    (
        "Centum Electronics", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "space exploration agencies (ISRO), defense missile programs, and international satellite manufacturers",
        "demand space-qualified microelectronics, radiation-hardened modules, hybrid microcircuits, and radar electronic warfare subsystems",
        "Space-Qualified Hybrid Microcircuits & Satellite Payloads", "Advanced Defense & Space Microelectronics Manufacturing",
        "is India's premier space and defense electronics manufacturer, having delivered critical flight modules for 50+ ISRO satellite and lunar missions",
        [0.88, 0.90, 0.95, 0.98, 0.90, 0.75],
        {"political": "Key strategic supplier to ISRO, DRDO, and the Indian armed forces; critical contributor to India's sovereign satellite and missile capabilities.", "economic": "Protected, high-margin strategic defense and space contracts with high technical barriers to entry and long revenue visibility.", "social": "Powers India's space triumphs (Chandrayaan-3 lunar lander modules) and ensures national sovereign defense radar accuracy.", "technological": "Thick-film and thin-film hybrid microcircuits, radiation-hardened semiconductor packaging, and microelectronic hermetic sealing.", "legal": "Highest-level space qualification standards (ISRO-certified), DGQA military quality clearances, and defense export regulations.", "environmental": "Operates ultra-cleanroom manufacturing environments with zero toxic effluent discharge and energy-efficient environmental testing chambers."},
        [0.10, 0.35, 0.35, 0.15, 0.45],
        {"threat_of_new_entrants": "Zero; qualifying electronic modules for spaceflight vacuum and cosmic radiation takes decades of flawless flight heritage.", "bargaining_power_of_buyers": "Low to moderate; ISRO and DRDO rely on Centum for complex customized microelectronic modules.", "bargaining_power_of_suppliers": "Moderate; space-grade semiconductor dies and specialized ceramic substrates.", "threat_of_substitutes": "Zero; space applications require certified microelectronics.", "competitive_rivalry": "Low; occupies a specialized elite niche alongside Bharat Electronics."}
    ),
    (
        "Sona BLW Precision Forgings (Sona Comstar)", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "global and domestic electric vehicle (EV) manufacturers, hybrid car makers, and commercial vehicle OEMs",
        "need high-precision forged differential bevel gears, EV traction motor controllers, and integrated electric drive axles",
        "EV Traction Motors, Precision Forged Differential Gears & e-Axles", "Electric Vehicle Powertrain & Precision Forged Mobility Solutions",
        "is a global technology leader in electric mobility powertrains, deriving over 80% of its massive order book from global electric vehicle platforms",
        [0.80, 0.94, 0.96, 0.96, 0.86, 0.82],
        {"political": "Supports the global and domestic electric mobility transition under FAME II and automotive PLI schemes.", "economic": "Exceptional profitability (EBITDA margins >28%) and high return on capital employed; massive global EV order book exceeding Rs 22,000 Cr.", "social": "Accelerates the worldwide elimination of polluting internal combustion engines by making EV powertrains more efficient and affordable.", "technological": "Patented net-shape precision bevel gear forging, brushless permanent magnet EV traction motors, and integrated electric differential drive units.", "legal": "Stringent global automotive OEM quality certifications (IATF 16949), international patent protections, and listing governance.", "environmental": "Powers zero-emission electric vehicles globally; manufacturing plants certified for energy efficiency and metal recycling."},
        [0.20, 0.48, 0.40, 0.20, 0.60],
        {"threat_of_new_entrants": "Low; precision net-shape gear forging and EV traction motor software require deep intellectual property and OEM validation.", "bargaining_power_of_buyers": "Moderate; global EV makers (Tesla, European OEMs) negotiate volume pricing, but rely on Sona for precision gear longevity.", "bargaining_power_of_suppliers": "Moderate; specialized automotive alloy steel bars and rare-earth permanent magnets.", "threat_of_substitutes": "Low; all wheeled vehicles require differential gears and electric motors.", "competitive_rivalry": "Moderate globally; undisputed Indian technology leader in EV powertrain gears."}
    ),
    (
        "Bharat Forge (Kalyani Group)", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "global commercial vehicle makers, aerospace giants, oil & gas drillers, and the Indian Army",
        "require ultra-heavy, high-integrity forged steel crankshafts, jet engine turbine forgings, and indigenous 155mm heavy defense artillery guns",
        "Advanced Towed Artillery Gun System (ATAGS) & Heavy Automotive Crankshafts", "World's Largest Forging Company & Indigenous Defense Artillery Leader",
        "operates the world's largest forging capacity, supplying forged engine components to global automotive giants and engineering India's ATAGS 155mm defense howitzers",
        [0.85, 0.94, 0.96, 0.96, 0.88, 0.78],
        {"political": "National defense champion under Atmanirbhar Bharat; developed the world's longest-range 155mm/52-caliber artillery gun (ATAGS) for the Indian Army.", "economic": "Generates over Rs 12,000 Cr in consolidated revenues; dual engine: high-volume global automotive crankshafts balanced by high-margin defense and aerospace systems.", "social": "Secures national defense borders with indigenous artillery firepower and provides high-tech metallurgical manufacturing jobs in Pune.", "technological": "World's largest computerized hydraulic forging presses (up to 16,000 tons), aerospace titanium forging, and advanced artillery ballistics.", "legal": "Directorate General of Quality Assurance (DGQA) defense clearances, aviation airworthiness approvals, and international trade compliance.", "environmental": "Captive wind and solar installations in Maharashtra meeting substantial industrial energy needs; 100% recycling of forged steel flashings."},
        [0.15, 0.45, 0.38, 0.18, 0.55],
        {"threat_of_new_entrants": "Zero; installing 16,000-ton forging presses and developing artillery weapon metallurgy requires decades of capital and military clearances.", "bargaining_power_of_buyers": "Moderate; global truck OEMs rely on Bharat Forge for unbreakable engine crankshafts; Indian Army procures through defense procurement procedures.", "bargaining_power_of_suppliers": "Moderate; specialty alloy steel blooms.", "threat_of_substitutes": "Low; heavy-duty diesel engines and artillery gun barrels cannot be cast—they must be forged for structural strength.", "competitive_rivalry": "Low to moderate globally; undisputed leader in heavy forging."}
    ),
    (
        "Ramkrishna Forgings", "B2B Industrial Commerce, Manufacturing & Contract Electronics",
        "commercial vehicle OEMs (Tata Motors, Ashok Leyland, Volvo), Indian Railways, and international heavy equipment makers",
        "need safety-critical forged and machined automotive chassis components, front axle beams, steering knuckles, and forged railway wheelsets",
        "Forged Front Axle Beams, Steering Knuckles & Forged Railway Wheels", "Precision Heavy Forging & Machined Automotive Components",
        "is a leading global supplier of safety-critical forged automotive components, winning a historic 20-year Indian Railways contract to manufacture forged train wheels",
        [0.80, 0.92, 0.95, 0.94, 0.86, 0.78],
        {"political": "Direct beneficiary of Indian Railways indigenization mandates (Make in India forged wheel plant) and national commercial vehicle fleet revival.", "economic": "Strong financial outperformance with high capacity utilization; expanding high-margin value-added machined assemblies over raw forgings.", "social": "Supplies safety-critical components that keep millions of commercial freight trucks and passenger trains operating without mechanical axle failure.", "technological": "Fully automated robotic forging press lines (up to 12,500 tons), CNC precision machining centers, and automated ultrasonic crack testing.", "legal": "RDSO railway approvals, IATF 16949 automotive certifications, and corporate listing governance.", "environmental": "Energy-efficient electric induction billet heaters replacing oil-fired furnaces, cutting factory emissions and scale loss."},
        [0.20, 0.48, 0.38, 0.20, 0.62],
        {"threat_of_new_entrants": "Low; heavy forging presses (12,500 tons) and automotive OEM safety-critical vendor qualification take years of audits.", "bargaining_power_of_buyers": "Moderate; truck OEMs negotiate annual contracts, but rely on Ramkrishna for certified axle beams and steering components.", "bargaining_power_of_suppliers": "Moderate; carbon and alloy steel billets.", "threat_of_substitutes": "Low for heavy-duty commercial vehicle front axles and railway wheels.", "competitive_rivalry": "Moderate; competes with Bharat Forge and MM Forgings."}
    )
]

for item in sector24_data:
    add_c(*item)

print(f"Sector 24 added: {len(sector24_data)} companies. Total in Part 4B: {len(part4_b)}")

# Load part4_a.json and combine
part4_a_path = Path(__file__).parent / "part4_a.json"
with open(part4_a_path, "r", encoding="utf-8") as f:
    part4_a = json.load(f)

full_part4 = part4_a + part4_b
print(f"Combined Part 4 count: {len(full_part4)} companies (Expected: 114).")

# Save to scratch/part4.json
out_path = Path(__file__).parent / "part4.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(full_part4, f, indent=2)

print(f"SUCCESS: Saved {len(full_part4)} companies to {out_path}")
