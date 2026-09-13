"""
Omniscope AI - Part 2B Generator
Builds Sectors 10, 11, 12 (66 companies):
- Sector 10: Direct-to-Consumer (D2C) & New-Age Lifestyle Brands (22 companies)
- Sector 11: Apparel, Fashion, Footwear & Jewelry (22 companies)
- Sector 12: Retail, Quick Commerce & E-Commerce Marketplaces (22 companies)
Combines with scratch/part2_a.json to produce scratch/part2.json (131 companies).
"""
import json
from pathlib import Path

part2_b = []

def add_c(name, sector, customer, need, product, category, benefit, p_scores, p_det, po_scores, po_det):
    part2_b.append({
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
# SECTOR 10: Direct-to-Consumer (D2C) & New-Age Lifestyle Brands (22 companies)
# ==============================================================================
sector10_data = [
    (
        "Honasa Consumer (Mamaearth)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "millennial parents and digital-savvy young women across India",
        "demand certified toxin-free, safe baby care and natural skin formulations free from parabens, sulfates, and mineral oil",
        "Mamaearth Onion Hair Oil & Ubtan Face Wash", "Toxin-Free Natural Personal Care Products",
        "pioneered MadeSafe-certified toxin-free personal care in India, building a house-of-brands (The Derma Co, Aqualogica) with rapid digital discovery",
        [0.64, 0.84, 0.94, 0.92, 0.82, 0.75],
        {"political": "Benefits from Digital India and national e-commerce logistics infrastructure expansion.", "economic": "High-margin digital-first brand that successfully transitioned to omnichannel general trade retail across 100,000+ stores.", "social": "Resonates with environmentally conscious millennial mothers seeking safe, non-toxic products for their infants.", "technological": "Proprietary consumer listening algorithms that detect emerging skincare ingredient trends (Ubtan, Onion, Niacinamide) and launch SKUs in 90 days.", "legal": "FSSAI, CDSCO personal care compliance, and strict ASCI adherence on natural/toxin-free marketing claims.", "environmental": "Certified plastic positive (recycles more plastic than it uses) and plants a tree for every direct website order."},
        [0.45, 0.65, 0.40, 0.42, 0.82],
        {"threat_of_new_entrants": "High; low barrier to contract-manufacture cosmetic formulations, but scaling marketing and omnichannel distribution is difficult.", "bargaining_power_of_buyers": "High; consumers readily switch between D2C beauty brands (Plum, WOW, Minimalist) based on discounts.", "bargaining_power_of_suppliers": "Low; outsourced third-party contract manufacturers compete aggressively for D2C formulation volumes.", "threat_of_substitutes": "High from legacy FMCG majors (HUL, L'Oréal, Dabur).", "competitive_rivalry": "Intense digital customer acquisition cost (CAC) warfare on Meta and Google ad networks."}
    ),
    (
        "Imagine Marketing (boAt Lifestyle)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "Indian Gen-Z youth, college students, and young working professionals",
        "want ultra-stylish, bass-heavy wireless earphones, party speakers, and smartwatches without paying exorbitant Apple or Sony prices",
        "boAt Airdopes, Rockerz & BassHeads Series", "Aspirational Consumer Audio & Wearables",
        "rules Indian personal audio and smartwatches with over 30% market share, delivering 'boAt Signature Bass' and trendy aesthetics at unbeatable value",
        [0.68, 0.86, 0.96, 0.90, 0.80, 0.65],
        {"political": "Major beneficiary of Government of India's Phased Manufacturing Programme (PMP) and electronics PLI, shifting production from China to India (Dixon/Optiemus).", "economic": "Fastest-growing consumer tech brand in Asia, achieving scale through relentless inventory turnover and aggressive e-commerce pricing.", "social": "Transformed headphones into a youth fashion accessory ('boAtheads'), endorsed by Bollywood youth icons and cricket stars.", "technological": "Bluetooth 5.3 fast-pairing, low-latency gaming modes, IPX water-resistance, and indigenously developed boAt Hearables companion app.", "legal": "BIS (Bureau of Indian Standards) certification for lithium batteries and Legal Metrology rules.", "environmental": "Pioneered 'Do Your Bit' e-waste takeback initiatives for discarded earphones and electronic recycling."},
        [0.40, 0.68, 0.45, 0.38, 0.85],
        {"threat_of_new_entrants": "Moderate; hardware can be white-labeled, but matching boAt's massive brand equity and retail distribution is very hard.", "bargaining_power_of_buyers": "High; youth consumers are extremely price-conscious and sensitive to festive sales discounts.", "bargaining_power_of_suppliers": "Moderate; dependent on Bluetooth chipset vendors (Qualcomm, Bestechnic) and lithium battery cells.", "threat_of_substitutes": "Moderate from smartphone bundled earbuds and generic Chinese audio gear.", "competitive_rivalry": "Fierce competition with Noise, Boult Audio, and OnePlus in wireless earbuds."}
    ),
    (
        "Noise (Nexxbase Technologies)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "health-conscious Indian youth, fitness enthusiasts, and smartwatch buyers",
        "need sleek, feature-packed smartwatches with Bluetooth calling, health telemetry, and vibrant AMOLED screens at accessible prices",
        "ColorFit Smartwatch Series & Noise Buds", "Connected Smart Wearables & Lifestyle Audio",
        "stands as India's #1 smartwatch brand, democratizing digital fitness tracking, SpO2 monitoring, and AMOLED displays for millions of young Indians",
        [0.68, 0.86, 0.95, 0.92, 0.80, 0.65],
        {"political": "Active participant in local electronics manufacturing under Make in India, assembling millions of smartwatches domestically.", "economic": "High-velocity boot-strapped business model generating sustained profitability without reckless venture capital burn.", "social": "Promotes active lifestyles and daily step targets among urban sedentary office workers and students.", "technological": "Proprietary NoiseFit health OS, algorithms for blood-oxygen and sleep tracking, and vivid high-refresh-rate AMOLED displays.", "legal": "BIS certification and consumer data privacy compliance for health telemetry stored in companion apps.", "environmental": "Promotes e-waste collection and phasing out non-recyclable packaging materials."},
        [0.38, 0.68, 0.45, 0.35, 0.82],
        {"threat_of_new_entrants": "Moderate; white-label smartwatch makers enter, but building a trusted connected app ecosystem takes sustained investment.", "bargaining_power_of_buyers": "High; consumers cross-shop Noise vs. Fire-Boltt vs. boAt on Amazon and Flipkart.", "bargaining_power_of_suppliers": "Moderate; display panels and optical sensor modules sourced from global electronics suppliers.", "threat_of_substitutes": "Moderate from traditional quartz watches and luxury smartwatches (Apple Watch, Samsung).", "competitive_rivalry": "High; continuous price wars and feature additions at sub-Rs 2,000 price points."}
    ),
    (
        "Sugar Cosmetics", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "young Indian women, working professionals, and makeup lovers across metros and Tier-2 cities",
        "demand long-lasting, smudge-proof, and transfer-resistant makeup specifically formulated to survive India's humid, tropical climates",
        "Matte As Hell Crayon Lipstick & Ace of Face Foundation", "High-Pigment Long-Wear Cosmetics for Indian Skin",
        "engineered bold, high-pigment matte cosmetics designed specifically to suit warm Indian undertones and endure tropical heat and sweat",
        [0.62, 0.84, 0.95, 0.88, 0.80, 0.65],
        {"political": "Compliant with Indian cosmetic safety norms and National Cosmetics Rules under CDSCO.", "economic": "Rapid expansion from online-only to 45,000+ retail counters and exclusive brand outlets across 500+ Indian cities.", "social": "Celebrates bold, unapologetic women empowerment and self-expression, breaking traditional subservient beauty stereotypes.", "technological": "High-pigment micronized color dispersion technology, transfer-resistant polymer films, and virtual makeup try-on AI on mobile app.", "legal": "Cruelty-free formulation standards and BIS cosmetics testing compliance.", "environmental": "Transitioning to recyclable paper board secondary packaging and cruelty-free formulation certifications."},
        [0.42, 0.65, 0.40, 0.40, 0.80],
        {"threat_of_new_entrants": "High; indie cosmetics brands emerge continuously on Instagram, but few achieve national retail scale.", "bargaining_power_of_buyers": "High; young women love experimenting with different lipstick and eyeliner brands.", "bargaining_power_of_suppliers": "Moderate; international cosmetic color laboratories in Germany and Italy alongside domestic formulators.", "threat_of_substitutes": "High from legacy makeup leaders (Maybelline, Lakmé, Nykaa).", "competitive_rivalry": "Intense rivalry with Lakmé, Colorbar, and Nykaa Cosmetics in malls and beauty stores."}
    ),
    (
        "Plum Goodness", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "conscious consumers and clean-beauty enthusiasts across Indian metros",
        "need 100% vegan, cruelty-free, and ethically formulated skincare and haircare powered by proven botanicals and science-backed actives",
        "Green Tea Pore Cleansing Range & Vitamin C Serum", "100% Vegan & Science-Backed Clean Beauty",
        "built India's first 100% vegan beauty brand, offering gentle, skin-friendly green tea and niacinamide formulas with complete ethical transparency",
        [0.62, 0.82, 0.93, 0.86, 0.80, 0.82],
        {"political": "Compliant with national cosmetic regulations and animal cruelty-free testing guidelines.", "economic": "Consistent sustainable growth across both online channels and organized retail beauty shelves (Shoppers Stop, Nykaa Luxe).", "social": "Strong appeal among ethically minded Gen-Z consumers passionate about animal welfare and clean personal care.", "technological": "Cold-pressed botanical extraction and stabilized Vitamin C active delivery systems for enhanced skin absorption.", "legal": "PETA-certified cruelty-free, vegan certified, and compliant with CDSCO standards.", "environmental": "Industry-leading empty bottle recycling program (Empties4Good) rewarding consumers for returning used plastic containers."},
        [0.44, 0.64, 0.38, 0.38, 0.78],
        {"threat_of_new_entrants": "High; low manufacturing entry hurdles in skincare, but brand authenticity is difficult to simulate.", "bargaining_power_of_buyers": "High; consumers actively browse ingredients and compare prices on e-commerce.", "bargaining_power_of_suppliers": "Low to moderate; specialty green tea extracts and cosmetic emulsifiers.", "threat_of_substitutes": "High from commercial dermatological brands and herbal Ayurvedic options.", "competitive_rivalry": "Fierce with Mamaearth, Minimalist, and Dot & Key."}
    ),
    (
        "WOW Skin Science", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "mass-premium Indian and US consumers seeking natural hair and skincare solutions",
        "want effective hair fall control and scalp detox solutions free from harsh sulfates, silicones, and parabens",
        "Apple Cider Vinegar Shampoo & Onion Black Seed Hair Oil", "Sulfate-Free Botanical Personal Care Formulations",
        "sparked the apple cider vinegar haircare craze in India and on Amazon US, offering natural botanical extracts that detoxify scalp and hair follicles",
        [0.60, 0.80, 0.90, 0.86, 0.78, 0.70],
        {"political": "Complies with CDSCO cosmetics guidelines and US FDA OTC cosmetics export requirements.", "economic": "Early pioneer of Amazon-first brand scaling, generating substantial cross-border export revenues alongside domestic sales.", "social": "Educated mass consumers on the damaging drying effects of harsh chemical sulfates and synthetic silicones.", "technological": "Built-in brush applicators for face washes and targeted comb nozzles for direct scalp oil application.", "legal": "Truth-in-advertising compliance and BIS cosmetics standard protocols.", "environmental": "Paraben-free and cruelty-free formulas; phasing out non-recyclable multi-material pump dispensers."},
        [0.48, 0.66, 0.38, 0.40, 0.82],
        {"threat_of_new_entrants": "High; hundreds of white-label natural brands copy trending ingredients.", "bargaining_power_of_buyers": "High; digital consumers easily switch based on influencer discounts and promotions.", "bargaining_power_of_suppliers": "Low; widely available botanical oils, apple cider vinegar, and packaging bottles.", "threat_of_substitutes": "High from multinational anti-dandruff and anti-hairfall shampoos (Head & Shoulders, Dove).", "competitive_rivalry": "Intense rivalry with Mamaearth, Pilgrim, and Biotique."}
    ),
    (
        "Wakefit", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "urban millennial households and new homeowners across Indian cities",
        "need high-quality, orthopedic memory foam mattresses and ergonomic home furniture without paying traditional 100% retailer markups",
        "Wakefit Orthopedic Memory Foam Mattress & Ergonomic Sleep Solutions", "Direct-to-Consumer Sleep & Home Furniture",
        "disrupted the traditional mattress cartel with a 100-night free home trial and factory-direct pricing, saving consumers over 50% on orthopedic mattresses",
        [0.64, 0.85, 0.94, 0.90, 0.80, 0.72],
        {"political": "Supports domestic manufacturing under Make in India, operating large-scale automated foam and woodworking factories.", "economic": "High-ticket repeat purchases transitioning from pure sleep mattresses into full-home furniture (sofas, beds, wardrobes, study desks).", "social": "Educated urban Indians on sleep ergonomics and spinal alignment, pioneering the famous 100-night sleep trial.", "technological": "Proprietary memory foam density profiling, vacuum roll-pack mattress compression machinery, and AI demand forecasting.", "legal": "BIS certification for foam durability and consumer protection warranty enforcement.", "environmental": "FSC-certified sustainable engineered wood procurement and non-toxic VOC-free foam formulations."},
        [0.35, 0.60, 0.42, 0.35, 0.75],
        {"threat_of_new_entrants": "Moderate; building national factory-direct delivery logistics and reverse logistics for 100-night trials requires capital.", "bargaining_power_of_buyers": "High; consumers research mattress reviews and compare firmness levels and warranties extensively.", "bargaining_power_of_suppliers": "Moderate; polyurethane chemicals (TDI/polyols) fluctuate with global petrochemical cycles.", "threat_of_substitutes": "Moderate from traditional cotton/coir mattresses and legacy brands (Kurlon, Sleepwell).", "competitive_rivalry": "High with The Sleep Company, SleepyCat, and Duroflex."}
    ),
    (
        "Sleepwell (Sheela Foam)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "multi-generational Indian families and commercial hospitality chains",
        "demand proven, durable, and highly resilient polyurethane foam mattresses and cushioning backed by five decades of sleep engineering",
        "Sleepwell Pro Comfort & Ortho Mattress Series", "Engineered Polyurethane Foam & Comfort Solutions",
        "leads India's organized mattress industry with Sheela Foam's unmatched chemical manufacturing scale, supplying both consumers and automotive seating",
        [0.66, 0.86, 0.92, 0.86, 0.82, 0.68],
        {"political": "Compliance with industrial safety and environmental standards for polyurethane chemical processing plants.", "economic": "Massive backward integration into PU foam chemistry provides insurmountable cost advantages over pure marketing D2C startups.", "social": "The most recognized legacy mattress brand in India, trusted for durability, back support, and nationwide dealer availability.", "technological": "Continuous variable pressure foaming technology, Neem Fresche anti-microbial treatments, and contoured pocket spring integration.", "legal": "Bureau of Indian Standards compliance and strict fire-retardant safety standards for automotive/railway foam.", "environmental": "Recycling foam scrap into bonded foam mattresses and implementing low-emission chlorofluorocarbon-free blowing agents."},
        [0.25, 0.55, 0.45, 0.32, 0.70],
        {"threat_of_new_entrants": "Low; building Sheela Foam's multi-location chemical continuous foaming plants requires heavy capital and hazardous chemical licenses.", "bargaining_power_of_buyers": "Moderate; consumers trust Sleepwell's multi-year warranties through 10,000+ local mattress dealer networks.", "bargaining_power_of_suppliers": "High; dependent on international petrochemical suppliers for TDI and polyols.", "threat_of_substitutes": "Moderate from modern D2C roll-packed foam mattresses and coir beds.", "competitive_rivalry": "Moderate to high with Kurl-on and modern D2C challengers (Wakefit)."}
    ),
    (
        "The Whole Truth Foods", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "fitness-conscious youth, clean-eating professionals, and health enthusiasts",
        "demand 100% transparent food products with zero hidden sugars, zero artificial sweeteners, zero emulsifiers, and zero misleading health claims",
        "The Whole Truth Protein Bars & Single-Origin Dark Chocolates", "100% Clean-Label Packaged Nutrition Foods",
        "pioneered radical food transparency in India by printing all 5 to 6 simple ingredients in giant font on the front of the pack, with zero hidden additives",
        [0.62, 0.82, 0.94, 0.86, 0.82, 0.78],
        {"political": "Strong advocate for clean food labeling reforms and tightening FSSAI regulations against deceptive front-of-pack health claims.", "economic": "Commands premium pricing power due to an intensely loyal cult following of health purists willing to pay for uncompromised ingredient quality.", "social": "Exposes widespread deceptive marketing in protein powders and energy bars through witty, educational consumer awareness content.", "technological": "Proprietary date-sweetened non-sticky bar pressing technology and cold-stone ground bean-to-bar dark chocolate refining.", "legal": "FSSAI compliance, accurate nutrition declarations, and strict truth-in-advertising adherence.", "environmental": "Uses whole food ingredients (cashews, dates, cocoa) with low processing footprint and sustainable craft paper packaging."},
        [0.38, 0.58, 0.40, 0.36, 0.72],
        {"threat_of_new_entrants": "Moderate; clean recipes can be copied, but earning radical consumer trust requires unwavering moral consistency.", "bargaining_power_of_buyers": "Moderate; customers appreciate transparency, but price per bar is higher than mass energy bars.", "bargaining_power_of_suppliers": "Moderate; premium whey protein isolate, dates, and unadulterated cocoa beans.", "threat_of_substitutes": "High from mass protein bars (RiteBite Max Protein) and homemade dry fruit snacks.", "competitive_rivalry": "Moderate; operates in a high-trust clean-label niche competing with Yoga Bar."}
    ),
    (
        "Country Delight", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "quality-conscious urban households and families with young children in Tier-1 cities",
        "need 100% unadulterated, farm-fresh cow and buffalo milk and daily farm produce delivered directly to their doorstep by 7:00 AM daily",
        "Farm-to-Doorstep Desi Cow Milk, VIP Buffalo Milk & Farm Produce", "Direct-to-Consumer Fresh Dairy & Kitchen Essentials",
        "tests milk across 26 parameters at the farm gate and delivers fresh, unadulterated milk within 24-36 hours of milking via an automated morning subscription app",
        [0.68, 0.86, 0.95, 0.92, 0.84, 0.74],
        {"political": "Supports dairy food safety standards, providing consumers with free home milk adulteration testing kits.", "economic": "High-frequency daily subscription model generates predictable monthly recurring revenue with high customer lifetime value.", "social": "Addresses the deep urban fear of chemical milk adulteration (detergents, starch, urea) common in unorganized milk supply.", "technological": "IoT-enabled farm-gate milk testing sensors, cold-chain temperature telemetry, and hyper-dense morning doorstep delivery routing.", "legal": "FSSAI food safety regulations, weight and measurement standards, and cold-chain compliance.", "environmental": "Uses recyclable glass bottles and food-grade pouches; optimizes delivery routes to reduce urban vehicle emissions."},
        [0.32, 0.55, 0.40, 0.30, 0.72],
        {"threat_of_new_entrants": "Low to moderate; setting up farm-level testing and hyper-early morning last-mile delivery fleets is operationally punishing.", "bargaining_power_of_buyers": "Moderate; consumers pay a premium for guaranteed purity, but switch if delivery is late.", "bargaining_power_of_suppliers": "Low to moderate; works directly with hundreds of dairy farmers offering fair, prompt milk payouts.", "threat_of_substitutes": "High from Amul, Mother Dairy, and local neighborhood milk vendors.", "competitive_rivalry": "Moderate; competes with Akshayakalpa, Otipy, and quick-commerce milk delivery."}
    ),
    (
        "Licious (Delightful Gourmet)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "urban meat lovers and culinary homemakers across India's top metros",
        "demand tender, clean, antibiotic-residue-free chicken, mutton, and fresh seafood delivered with zero chemical preservatives or foul odors",
        "Farm-to-Fork Fresh Meat, Seafood & Ready-to-Cook Marinades", "D2C Fresh Meat & Gourmet Protein Ecosystem",
        "built India's first farm-to-fork cold chain meat unicorn, guaranteeing 0-4 deg C cold chain, 150+ food safety checks, and zero chemical preservatives",
        [0.66, 0.85, 0.94, 0.92, 0.84, 0.72],
        {"political": "Formalizes and modernizes India's unorganized meat sector under modern veterinary and food hygiene standards.", "economic": "Premiumization of a historically unorganized 90% commodity market; expands into high-margin ready-to-cook kebabs and spreads.", "social": "Liberated urban meat buyers from having to visit chaotic, unhygienic traditional wet markets.", "technological": "State-of-the-art cold-chain temperature monitoring from farm to delivery box, computerized portion cutting, and vacuum packaging.", "legal": "FSSAI central meat processing licenses, humane slaughter norms, and municipal meat trade regulations.", "environmental": "Zero chemical runoff, biological effluent treatment at processing hubs, and eco-friendly insulated packaging."},
        [0.30, 0.55, 0.42, 0.32, 0.72],
        {"threat_of_new_entrants": "Low; building an unbroken certified cold chain and bio-secure meat sourcing network requires massive capex.", "bargaining_power_of_buyers": "Moderate; meat eaters pay for hygiene and tenderness, but compare prices against local butchers.", "bargaining_power_of_suppliers": "Moderate; biosecure poultry and livestock contract farms.", "threat_of_substitutes": "High from local street-corner wet-market butchers and FreshToHome.", "competitive_rivalry": "Moderate; duopoly battle with FreshToHome alongside quick-commerce dark stores."}
    ),
    (
        "FreshToHome", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "seafood and poultry lovers in India and the Middle East",
        "need 100% chemical-free, formalin-free fresh ocean fish and antibiotic-free chicken delivered straight from coastal fishermen",
        "Chemical-Free Marine Catch, Poultry & Mutton", "Direct Fishermen-to-Consumer Fresh Seafood & Meat",
        "empowers 4,000+ coastal fishermen via patent-pending AI auction software, delivering fresh non-formalin ocean fish within 24 hours of landing",
        [0.66, 0.85, 0.94, 0.91, 0.84, 0.70],
        {"political": "Supports coastal fishermen livelihoods through direct digital auctions and fair price realization, eliminating predatory middlemen.", "economic": "Expanding profitable overseas operations in UAE and Saudi Arabia alongside rapid domestic tier-1 and tier-2 city growth.", "social": "Guarantees that children and families eat ocean fish completely free of lethal carcinogenic preservative chemicals like formalin.", "technological": "Commodities-exchange auction mobile app for fishermen, computerized chill-vat temperature logging, and automated fish de-scaling.", "legal": "FSSAI compliance, export-grade seafood quality approvals (MPEDA), and Halal certifications.", "environmental": "Promotes sustainable coastal fishing practices, avoids bottom-trawling damage, and uses food-grade recyclable chill packs."},
        [0.30, 0.55, 0.42, 0.30, 0.70],
        {"threat_of_new_entrants": "Low; direct coastal auction relationships across 40+ Indian fishing harbors cannot be replicated easily.", "bargaining_power_of_buyers": "Moderate; seafood lovers prioritize chemical-free freshness over small price differences.", "bargaining_power_of_suppliers": "Low to moderate; fishermen prefer FreshToHome's instant digital payments over traditional delayed mandi credit.", "threat_of_substitutes": "High from local fish markets and Licious.", "competitive_rivalry": "Direct rivalry with Licious and quick-commerce delivery apps."}
    ),
    (
        "Epigamia (Drums Food International)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "urban health-conscious youth, fitness enthusiasts, and dairy lovers",
        "need high-protein, delicious, and low-sugar Greek yogurt, smoothies, and lactose-free milk for clean everyday snacking",
        "Epigamia Greek Yogurt, Protein Milkshakes & Plant-Based Yogurts", "Value-Added Gourmet & High-Protein Dairy",
        "introduced authentic Greek yogurt to India, straining real milk to deliver double the protein of regular curd in exciting gourmet fruit flavors",
        [0.62, 0.82, 0.92, 0.86, 0.80, 0.70],
        {"political": "Compliant with FSSAI dairy nutritional labeling, probiotic culture claims, and food safety standards.", "economic": "Commands premium snack margins compared to plain commodity curd, benefiting from modern trade and quick-commerce distribution.", "social": "Pioneered guilt-free healthy snacking among urban desk workers replacing fried snacks with high-protein Greek yogurt.", "technological": "Continuous centrifugal whey separation, cold aseptic fruit purée blending, and extended fresh shelf-life without chemical preservatives.", "legal": "FSSAI food licensing and advertising claims verification.", "environmental": "Launched dairy cup recycling initiatives and eco-friendly plant-based coconut yogurt alternatives."},
        [0.35, 0.60, 0.40, 0.38, 0.74],
        {"threat_of_new_entrants": "Moderate; yogurt technology is accessible, but building cold-chain refrigerated retail shelf presence is costly.", "bargaining_power_of_buyers": "High; consumers treat Greek yogurt as a discretionary snack and have many alternative healthy snacks.", "bargaining_power_of_suppliers": "Moderate; farm-fresh milk procurement and imported European probiotic culture strains.", "threat_of_substitutes": "High from traditional curd (dahi), ice creams, and protein bars.", "competitive_rivalry": "High with dairy giants (Amul, Mother Dairy) launching competing Greek yogurts at lower prices."}
    ),
    (
        "Blue Tokai Coffee Roasters", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "urban coffee connoisseurs, creative professionals, and specialty coffee lovers",
        "crave freshly roasted, single-origin Indian Arabica coffee beans and expertly brewed pour-overs, rejecting bitter chicory instant powders",
        "Single-Origin Specialty Coffee Beans & Artisanal Cafes", "Farm-Direct Specialty Indian Coffee Ecosystem",
        "sparked India's third-wave coffee revolution, sourcing directly from India's finest coffee estates and custom-roasting small batches on demand",
        [0.64, 0.84, 0.94, 0.88, 0.82, 0.78],
        {"political": "Promotes Indian specialty coffee globally with the Coffee Board of India; directly supports estate biodiversity.", "economic": "Thriving omnichannel model: lucrative subscription beans, corporate office cafes, ready-to-drink cans, and 80+ aesthetic sit-down cafes.", "social": "Created a sophisticated coffee appreciation culture in India, educating consumers on roast profiles, acidity, and elevation notes.", "technological": "Giesen small-batch drum roasters with automated roast-profile temperature profiling, and nitrogen cold-brew canning.", "legal": "FSSAI compliance, fair-trade estate sourcing verification, and weights and measures adherence.", "environmental": "Sourced exclusively from shade-grown estates that preserve bird biodiversity in the Western Ghats; compostable takeaway cups."},
        [0.32, 0.52, 0.38, 0.35, 0.70],
        {"threat_of_new_entrants": "Moderate; independent micro-roasters emerge, but Blue Tokai's estate exclusivity and cafe footprint create a moat.", "bargaining_power_of_buyers": "Moderate; specialty coffee enthusiasts are brand-loyal, but casual cafe-goers have many choices.", "bargaining_power_of_suppliers": "Low to moderate; long-term transparent pricing partnerships with top coffee estates in Chikmagalur and Coorg.", "threat_of_substitutes": "High from commercial coffee chains (Starbucks, Third Wave) and instant coffee.", "competitive_rivalry": "Intense rivalry with Third Wave Coffee, Subko, and Starbucks in metro cafe clusters."}
    ),
    (
        "Third Wave Coffee", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "tech workers, founders, students, and remote professionals seeking productive cafe spaces",
        "need high-speed Wi-Fi, modern ergonomic seating, specialty espresso beverages, and artisanal quick bites in neighborhood cafe hubs",
        "Specialty Arabica Espressos, Pour-Overs & Third Wave Cafes", "Specialty Coffee Roastery & Modern Urban Cafes",
        "delivers premium 100% Arabica specialty coffee paired with vibrant co-working cafe environments, scaling rapidly across Indian tech corridors",
        [0.64, 0.85, 0.94, 0.88, 0.80, 0.72],
        {"political": "Complies with municipal shop and establishment licenses, fire safety norms, and food handling regulations.", "economic": "Rapid venture-backed retail expansion across Bengaluru, Mumbai, Delhi-NCR, and Pune, achieving strong average bill values.", "social": "The unofficial co-working space and meeting ground for India's startup ecosystem; popular for pitch meetings and focused work.", "technological": "La Marzocco espresso machines, automated bean grinders, digital loyalty mobile app, and dark-kitchen delivery integration.", "legal": "FSSAI food licensing, fire safety certifications, and GST hospitality compliance.", "environmental": "Encourages reusable tumblers, paper straws, and energy-efficient cafe lighting."},
        [0.34, 0.58, 0.40, 0.36, 0.76],
        {"threat_of_new_entrants": "Moderate; cafe real estate is competitive, but building an 80+ outlet branded coffee chain requires heavy capital.", "bargaining_power_of_buyers": "Moderate to high; consumers choose among Starbucks, Blue Tokai, and Costa Coffee.", "bargaining_power_of_suppliers": "Moderate; specialized coffee beans, dairy, and cafe bakery suppliers.", "threat_of_substitutes": "High from traditional tea stalls (Chaayos), coworking spaces, and home brewing.", "competitive_rivalry": "Fierce competition with Starbucks, Blue Tokai, and abcoffee."}
    ),
    (
        "Vahdam Teas", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "global tea connoisseurs and wellness seekers in the US, Europe, and India",
        "demand fresh, authentic, handpicked loose-leaf Indian Darjeeling and Assam teas without passing through multi-tier export middlemen",
        "Single-Estate Darjeeling, Assam Teas & Herbal Turmeric Blends", "Direct Farm-to-Cup Global Indian Tea Brand",
        "eliminated decades of colonial middlemen to deliver garden-fresh Indian teas directly to global consumers, endorsed by Oprah Winfrey and Ellen DeGeneres",
        [0.68, 0.86, 0.94, 0.90, 0.82, 0.82],
        {"political": "Promotes Indian tea GI heritage on the global stage; partnered with Tea Board of India and awarded national export accolades.", "economic": "Generates >80% of revenue in foreign currencies (USD, EUR) via Amazon global selling and international specialty grocers.", "social": "TEAch Me initiative directs 1% of revenue towards the education of tea estate workers' children in Darjeeling and Assam.", "technological": "Nitrogen-vacuum packaging at origin within days of harvest, and advanced D2C global logistics integration.", "legal": "US FDA, USDA Organic, Non-GMO Project, and European Union organic import certifications.", "environmental": "Certified Climate Neutral and Plastic Neutral brand, utilizing biodegradable pyramid tea bags made from corn starch."},
        [0.28, 0.50, 0.35, 0.30, 0.68],
        {"threat_of_new_entrants": "Low; building global cross-border e-commerce brand credibility and retail distribution in Whole Foods takes years.", "bargaining_power_of_buyers": "Moderate; global tea lovers pay a premium for authenticated fresh flush teas.", "bargaining_power_of_suppliers": "Low to moderate; direct estate procurement offers tea growers higher prices than traditional auction brokers.", "threat_of_substitutes": "Moderate from traditional multinational tea bag brands (Twinings, Lipton).", "competitive_rivalry": "Low to moderate in high-end global D2C Indian tea exports."}
    ),
    (
        "Minimalist (Uprising Science)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "educated, ingredient-savvy skincare shoppers across India and international markets",
        "demand clinical-grade, transparent active skincare serums (Niacinamide, Salicylic Acid, Retinol) without marketing hype or inflated price tags",
        "Minimalist Niacinamide 10%, Salicylic Acid 2% & Alpha Arbutin Serums", "Science-Backed Active Ingredient Clinical Skincare",
        "disrupted the Indian beauty market with radical ingredient transparency and peer-reviewed clinical data, offering high-potency actives at sub-Rs 600",
        [0.64, 0.85, 0.94, 0.92, 0.82, 0.75],
        {"political": "Complies with CDSCO drug and cosmetic rules and international cosmetics safety standards across 10+ export countries.", "economic": "Hyper-efficient R&D and low marketing burn; word-of-mouth efficacy driven by Reddit and skin-enthusiast communities.", "social": "Empowered millions of Indian consumers to decode skincare labels and understand how active molecules treat acne, hyperpigmentation, and aging.", "technological": "In-house formulation laboratory in Jaipur testing ingredient stability, skin penetration enhancers, and clinical efficacy metrics.", "legal": "Strict adherence to cosmetic ingredient labeling and claim substantiation laws.", "environmental": "Fragrance-free, dye-free, essential-oil-free, and packaged in UV-protective amber glass dropper bottles."},
        [0.36, 0.60, 0.38, 0.35, 0.78],
        {"threat_of_new_entrants": "Moderate; active ingredient skincare is popular, but Minimalist's scientific credibility and formulation stability are hard to copy.", "bargaining_power_of_buyers": "Moderate to high; consumers compare active percentages and prices against The Ordinary and Derma Co.", "bargaining_power_of_suppliers": "Moderate; specialized active pharmaceutical-grade cosmetic raw materials (BASF, Croda).", "threat_of_substitutes": "High from dermatological prescription creams and mainstream beauty brands.", "competitive_rivalry": "Direct rivalry with The Ordinary, The Derma Co (Honasa), and Plum ThinkDerma."}
    ),
    (
        "mCaffeine (PEP Technologies)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "millennial and Gen-Z urban youth seeking invigorating, sensory personal care rituals",
        "need effective body exfoliation, tan removal, and cellulite reduction powered by natural caffeinated Arabica coffee granules",
        "Original Coffee Body Scrub & Naked & Raw Coffee Face Wash", "Caffeine-Infused Body & Personal Care",
        "created India's first caffeinated personal care brand, making coffee scrubs a viral youth grooming sensation with millions of jars sold",
        [0.62, 0.82, 0.93, 0.86, 0.79, 0.75],
        {"political": "Complies with CDSCO guidelines and Indian national beauty manufacturing standards.", "economic": "Pioneered the specialized body scrub category in India, creating high-margin repeat consumption across e-commerce and quick commerce.", "social": "Caters to youth obsession with coffee aroma and visible instant skin exfoliation results for tan removal.", "technological": "Micro-ground roasted coffee bean formulation that retains antioxidant caffeic acid without clogging bathroom drains.", "legal": "PETA-certified vegan and cruelty-free, FDA approved cosmetic facilities.", "environmental": "Plastic-neutral certified brand; incorporates upcycled coffee grounds into skincare to reduce organic waste."},
        [0.40, 0.65, 0.38, 0.38, 0.78],
        {"threat_of_new_entrants": "Moderate; coffee theme can be imitated, but mCaffeine has deep first-mover category dominance.", "bargaining_power_of_buyers": "High; consumers love trying new beauty scrubs and look for festive sales.", "bargaining_power_of_suppliers": "Low; abundant roasted Indian Arabica and Robusta coffee beans.", "threat_of_substitutes": "High from traditional loofahs, ubtans, and generic body washes.", "competitive_rivalry": "Moderate to high with WOW Skin Science and body care startups."}
    ),
    (
        "Bombay Shaving Company (Visage Lines)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "modern Indian men seeking premium, irritation-free shaving and beard styling experiences",
        "need precision safety razors, soothing shaving foams, and beard grooming kits that elevate mundane morning shaving into an enjoyable ritual",
        "Precision Safety Razor, Charcoal Shaving Foam & Beard Growth Kits", "Premium Men's Shaving, Grooming & Hair Care",
        "reinvented traditional wet shaving for young Indian men with engineered single-blade safety razors, charcoal shaving foams, and salon-grade trimmers",
        [0.62, 0.82, 0.92, 0.86, 0.80, 0.68],
        {"political": "Supports domestic hardware fabrication and consumer packaging under Make in India.", "economic": "Rapid expansion across 70,000+ retail salons and modern trade outlets, backed by strategic investment from Colgate-Palmolive.", "social": "Inspires modern Indian men to take pride in self-care, grooming, and beard maintenance without social stigma.", "technological": "Engineered die-cast zinc razor heads with optimized blade gap angles to prevent ingrown hairs and razor burn on sensitive Indian skin.", "legal": "BIS certification for electrical grooming appliances and compliance with Legal Metrology packaging rules.", "environmental": "Promotes reusable metal safety razors that eliminate millions of disposable plastic cartridge razor heads."},
        [0.38, 0.65, 0.40, 0.38, 0.80],
        {"threat_of_new_entrants": "Moderate; men's grooming is attractive, but breaking into barber shops and retail counters is capital intensive.", "bargaining_power_of_buyers": "High; men compare prices against Gillette and local barbershop services.", "bargaining_power_of_suppliers": "Moderate; precision metal tooling, razor blade steel (Feather/Super-Max), and aerosol cans.", "threat_of_substitutes": "High from multinational giant Gillette and electrical multi-trimmers (Philips).", "competitive_rivalry": "Intense rivalry with Gillette in razors, and Beardo in beard styling."}
    ),
    (
        "Beardo (Zed Lifestyle)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "masculine Indian youth, bikers, and men passionate about full beard styling and rugged grooming",
        "want potent beard growth oils, mustache styling waxes, and masculine fragrances crafted specifically for thick Indian facial hair",
        "Beardo Beard Growth Oil, Godfather Perfume & Beard Clay Wax", "Masculine Beard Styling, Fragrance & Hair Grooming",
        "created the beard grooming movement in India, empowering men to embrace full, stylish facial hair with masculine grooming formulations",
        [0.62, 0.82, 0.92, 0.85, 0.78, 0.65],
        {"political": "Fully compliant with Indian cosmetic regulations; acquired by FMCG major Marico to strengthen digital-first male grooming.", "economic": "High gross margin profile powered by impulse fragrance purchases and beard oil loyalty across Tier-1 and Tier-2 towns.", "social": "Cultural pioneer that made beards fashionable and professional across corporate and social India.", "technological": "Redensyl and procapil active peptide hair-growth formulations combined with natural cedarwood and argan oils.", "legal": "CDSCO cosmetic safety compliance and ASCI advertising standards.", "environmental": "Transitioning to recyclable glass dropper packaging and sulfate-free grooming formulations."},
        [0.40, 0.64, 0.38, 0.38, 0.78],
        {"threat_of_new_entrants": "Moderate; low technical formulation barrier, but Beardo possesses strong rugged masculine branding.", "bargaining_power_of_buyers": "High; young men explore multiple cologne and styling brands.", "bargaining_power_of_suppliers": "Low; abundant carrier oils and fragrance compounds.", "threat_of_substitutes": "High from clean-shaven looks and generic hair gels.", "competitive_rivalry": "Intense rivalry with Bombay Shaving Company, Ustraa, and Wild Stone."}
    ),
    (
        "Kapiva (Adret Retail)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "modern urban professionals seeking convenient, daily Ayurvedic health and vitality solutions",
        "need authentic, pure Himalayan Shilajit, herbal juices, and Ayurvedic effervescents that fit into fast-paced contemporary lifestyles",
        "Kapiva Pure Himalayan Shilajit & Aloe Vera / Amla Juices", "Modern Functional Ayurvedic Nutrition & Wellness",
        "modernized ancient Ayurveda for young urbanites, testing pure Himalayan Shilajit across 7 purity gates and creating tasty daily herbal juices",
        [0.66, 0.84, 0.94, 0.88, 0.82, 0.74],
        {"political": "Strong alignment with Ministry of AYUSH initiatives promoting evidence-based traditional medicine and herbal wellness.", "economic": "Rapid growth across Amazon, quick-commerce, and modern trade, backed by high repeat order rates for daily vitality supplements.", "social": "Destigmatized Shilajit and Ayurvedic herbs for youth, rebranding them as clean, natural vitality and stamina boosters.", "technological": "Automated cold-pressed botanical juice extraction and advanced lab testing (heavy metals, microbiological purity) for every batch.", "legal": "AYUSH manufacturing licenses, FSSAI compliance, and heavy-metal safety certifications.", "environmental": "Ethical high-altitude wild harvesting of Shilajit from Himalayan rock faces and organic amla farming partnerships."},
        [0.35, 0.60, 0.38, 0.35, 0.74],
        {"threat_of_new_entrants": "Moderate; many small herbal sellers exist on Amazon, but consumer trust in Shilajit purity requires certified lab reports.", "bargaining_power_of_buyers": "Moderate to high; consumers compare prices and certifications across Ayurvedic brands.", "bargaining_power_of_suppliers": "Moderate; authentic high-altitude resin suppliers and seasonal amla harvests.", "threat_of_substitutes": "High from multivitamins, energy drinks, and traditional Ayurvedic pharmacies (Baidyanath, Dabur).", "competitive_rivalry": "High with Upakarma Ayurveda, Dabur, and Patanjali."}
    ),
    (
        "The Sleep Company (Comfort Grid)", "Direct-to-Consumer (D2C) & New-Age Lifestyle Brands",
        "pain-conscious urban dwellers, tech professionals, and long-hour desk workers",
        "need revolutionary mattress and ergonomic chair cushioning that relieves pressure points without trapping body heat like conventional foam",
        "SmartGRID Orthopedic Mattress & Stylux Office Chairs", "Patented SmartGRID Sleep & Ergonomic Seating Technology",
        "introduced Asia's first patented hyper-elastic SmartGRID material developed with DRDO scientists, replacing obsolete memory foam with smart posture-adaptive comfort",
        [0.65, 0.85, 0.93, 0.92, 0.82, 0.72],
        {"political": "Supports indigenization of high-tech polymer manufacturing under Make in India; collaborated with defense polymer scientists.", "economic": "Rapid growth with higher average order values (>Rs 25,000) than memory foam peers; scaling company-owned experience stores in metros.", "social": "Solves chronic back pain and heat buildup for desk-bound software engineers and sedentary urban professionals.", "technological": "Patented Japanese food-grade hyper-elastic polymer grid that isolates motion, flexes under hips/shoulders, and remains 100% breathable.", "legal": "Global patent protection on SmartGRID architecture and BIS product testing certifications.", "environmental": "Uses non-toxic, food-grade hyper-elastic polymers that are 100% recyclable and contain zero carcinogenic foam off-gassing chemicals."},
        [0.26, 0.55, 0.42, 0.32, 0.70],
        {"threat_of_new_entrants": "Low; patented SmartGRID polymer technology prevents competitors from copying the core mechanical comfort architecture.", "bargaining_power_of_buyers": "Moderate; customers pay a premium for verified back pain relief and long 10-year warranties.", "bargaining_power_of_suppliers": "Moderate; specialized polymer raw materials and precision grid extrusion machinery.", "threat_of_substitutes": "Moderate from memory foam mattresses (Wakefit) and spring mattresses.", "competitive_rivalry": "Moderate to high with Wakefit and Sleepwell in premium orthopedic sleep categories."}
    )
]

for item in sector10_data:
    add_c(*item)

print(f"Sector 10 added: {len(sector10_data)} companies. Total: {len(part2_b)}")

# ==============================================================================
# SECTOR 11: Apparel, Fashion, Footwear & Jewelry (22 companies)
# ==============================================================================
sector11_data = [
    (
        "Titan Company", "Apparel, Fashion, Footwear & Jewelry",
        "Indian consumers seeking trusted precious jewelry, watches, eyewear, and lifestyle accessories",
        "need guaranteed karat purity in gold jewelry, impeccable craftsmanship, and trusted horological designs backed by the Tata hallmark of ethics",
        "Tanishq Gold & Diamond Jewelry, Titan Watches & Titan Eye+", "Precious Jewelry, Watches & Lifestyle Ecosystem",
        "stands as India's apex lifestyle powerhouse with Tanishq holding leadership in hallmarked gold and Titan commanding over 50% of the organized watch market",
        [0.75, 0.92, 0.98, 0.90, 0.88, 0.80],
        {"political": "Complies strictly with mandatory BIS hallmarking regulations, gold import duties, and anti-money laundering PMLA cash disclosures.", "economic": "Titan generates over Rs 45,000 Cr in revenue, delivering exceptional return on capital (ROCE >30%) through the Tanishq jewelry engine.", "social": "Tanishq transformed Indian bridal jewelry buying from secretive family goldsmiths to transparent Karatmeter purity testing.", "technological": "XRF Karatmeter machines for instant gold purity verification, 3D computer-aided jewelry design, and indigenous quartz watch movements.", "legal": "100% BIS hallmarked gold, SEBI compliance, and consumer protection jewelry buyback guarantees.", "environmental": "Responsible gold sourcing, recycled gold refiners, and water-recycling manufacturing campuses in Hosur."},
        [0.22, 0.48, 0.40, 0.25, 0.65],
        {"threat_of_new_entrants": "Low; building Tanishq's multi-decade trust, capital-heavy gold inventory, and store network is nearly impossible.", "bargaining_power_of_buyers": "Moderate; consumers demand fair making charges, but trust Tanishq's purity above all competitors.", "bargaining_power_of_suppliers": "Low; bullion banks supply gold under RBI consignment quotas.", "threat_of_substitutes": "Low; gold jewelry is deeply embedded in Indian weddings, rituals, and household wealth preservation.", "competitive_rivalry": "Moderate to high with Kalyan Jewellers, Malabar Gold, and regional family jewellers."}
    ),
    (
        "CaratLane", "Apparel, Fashion, Footwear & Jewelry",
        "modern working women, self-purchasing professionals, and young couples seeking lightweight jewelry",
        "need chic, affordable, and lightweight diamond and gold jewelry designed for daily office and casual wear rather than heavy wedding vaults",
        "CaratLane Everyday Fine Jewelry & Shaya Silver", "Lightweight Everyday Diamond & Fine Jewelry",
        "revolutionized modern fine jewelry in India, delivering stunning 14K and 18K lightweight designs backed by Titan and Tanishq trust",
        [0.72, 0.88, 0.95, 0.92, 0.86, 0.75],
        {"political": "BIS hallmarking compliance and adherence to digital invoice disclosure rules for jewelry retail.", "economic": "Titan acquired full ownership at a multi-billion dollar valuation, expanding CaratLane across 250+ omnichannel retail stores.", "social": "Pioneered the 'self-purchase' movement for urban working women who buy fine jewelry for themselves rather than waiting for family gifting.", "technological": "Proprietary virtual 3D try-on app, CAD rapid jewelry prototyping, and localized 'Try at Home' doorstep jeweler service.", "legal": "BIS hallmarked gold and SGL/IGI certified natural diamonds.", "environmental": "Zero-waste micro-casting jewelry manufacturing and recycled gold utilization."},
        [0.28, 0.52, 0.40, 0.28, 0.70],
        {"threat_of_new_entrants": "Moderate; many online diamond sites launch, but CaratLane's backing by Titan/Tanishq creates unbeatable consumer trust.", "bargaining_power_of_buyers": "Moderate; young women compare designs and making charges across modern jewelers.", "bargaining_power_of_suppliers": "Moderate; certified diamond cutters (Surat) and gold bullion suppliers.", "threat_of_substitutes": "Moderate from lab-grown diamond jewelry and fashion demi-fine silver brands.", "competitive_rivalry": "Direct rivalry with BlueStone and Mia by Tanishq."}
    ),
    (
        "Kalyan Jewellers", "Apparel, Fashion, Footwear & Jewelry",
        "families and bridal jewelry buyers across South, West, and North India and the GCC",
        "require authentic regional temple jewelry, heavy wedding sets, and transparent pricing backed by 4-level product certifications",
        "Muhurat Wedding Jewelry & Regional Gold Collections", "Pan-India Multi-Regional Bridal & Gold Jewelry",
        "operates one of India's largest jewelry showroom networks, pioneering hyper-localized regional jewelry designs and transparent price breakdowns",
        [0.70, 0.90, 0.96, 0.86, 0.86, 0.74],
        {"political": "Adheres to mandatory BIS hallmarking, bullion import duty fluctuations, and GST Council tax mandates.", "economic": "Rapid showroom expansion via asset-light franchisee-owned company-operated (FOCO) model driving return on capital employed.", "social": "Deep regional resonance across Kerala, Tamil Nadu, and Telugu states; endorsed by Amitabh Bachchan for transparent purity standards.", "technological": "Computerized inventory tracking across 200+ mega-showrooms, digital gold savings schemes, and automated karat verification.", "legal": "BIS hallmarked gold, IGI certified diamonds, and complete compliance with RBI precious metal regulations.", "environmental": "Promotes gold recycling through old-gold exchange counters, reducing dependency on newly mined imported gold bullion."},
        [0.25, 0.50, 0.42, 0.25, 0.70],
        {"threat_of_new_entrants": "Low; retail jewelry requires hundreds of crores in showroom inventory, local landlord trust, and multi-decade brand goodwill.", "bargaining_power_of_buyers": "Moderate; buyers compare making charges and gold rates across Kalyan, Joyalukkas, and Tanishq.", "bargaining_power_of_suppliers": "Low; gold procured via nominated banks under RBI metal loan schemes.", "threat_of_substitutes": "Low; cultural indispensability of bridal gold jewelry in Indian matrimony.", "competitive_rivalry": "High with Tanishq, Malabar Gold, Joyalukkas, and Senco Gold."}
    ),
    (
        "Senco Gold & Diamonds", "Apparel, Fashion, Footwear & Jewelry",
        "eastern Indian families, wedding shoppers, and lovers of intricate handcrafted Bengali jewelry",
        "demand world-renowned lightweight, handcrafted Bengali karigari gold filigree and delicate bridal jewelry at transparent making charges",
        "Everlite Lightweight Fine Jewelry & Vivaha Bridal Collection", "Handcrafted Bengali Karigari Fine Jewelry",
        "celebrates centuries of Bengal's master artisans (Karigars), delivering stunning filigree craftsmanship that maximizes visual grandeur while keeping gold weight light",
        [0.68, 0.88, 0.94, 0.86, 0.85, 0.72],
        {"political": "Supports master karigar craftsman welfare schemes and adheres to national BIS hallmarking guidelines.", "economic": "Dominant market leader in Kolkata and Eastern India, successfully expanding across North and West India with high capital efficiency.", "social": "Bengali karigars are globally renowned for exquisite craftsmanship; Senco brings their heritage art to national retail prominence.", "technological": "Computerized precision casting combined with traditional handmade filigree; robust digital gold omnichannel presence.", "legal": "100% BIS hallmark certified gold and certified natural diamonds.", "environmental": "Supports traditional low-energy artisanal hand-tool jewelry fabrication and promotes circular gold exchange."},
        [0.26, 0.52, 0.40, 0.26, 0.68],
        {"threat_of_new_entrants": "Low in Eastern India; Senco's 85-year legacy and relationship with thousands of master karigars form a cultural moat.", "bargaining_power_of_buyers": "Moderate; Bengali consumers are discerning gold connoisseurs who evaluate intricate workmanship.", "bargaining_power_of_suppliers": "Moderate; relies on skilled traditional artisans and nominated bullion banks.", "threat_of_substitutes": "Low for celebratory bridal wedding gold.", "competitive_rivalry": "Moderate in East India with PC Chandra and Anjali Jewellers; national competition from Tanishq and Kalyan."}
    ),
    (
        "Joyalukkas India", "Apparel, Fashion, Footwear & Jewelry",
        "South Indian bridal families and the global Indian diaspora across the Middle East",
        "need grand, opulent wedding gold jewelry collections and pure coins with guaranteed international exchange privileges",
        "Joyalukkas Wedding Gold Collection & Pride Diamonds", "Grand Scale Bridal Jewelry & International Retail Network",
        "operates massive multi-floor jewelry showrooms across India and 11 countries, serving the Indian diaspora with unmatched gold design diversity",
        [0.70, 0.90, 0.96, 0.85, 0.85, 0.72],
        {"political": "Cross-border bullion trade compliance with RBI and UAE central bank regulations; mandatory hallmarking adherent.", "economic": "Enormous revenue generation from Gulf NRI remittances and grand flagship jewelry showrooms across southern India.", "social": "Deep trust among Malayali and South Indian diaspora families who purchase wedding gold in Dubai and redeem in Kerala.", "technological": "Global inventory ERP, secure diamond testing gemological labs, and digital gold advance booking schemes.", "legal": "BIS hallmarking, anti-money laundering international compliance, and strict Kimberley Process diamond certification.", "environmental": "Old gold refiners and energy-efficient showroom illumination design."},
        [0.25, 0.50, 0.42, 0.24, 0.70],
        {"threat_of_new_entrants": "Low; requires enormous working capital to stock tens of thousands of kilograms of gold across international showrooms.", "bargaining_power_of_buyers": "Moderate; gold buyers negotiate making charges, but value Joyalukkas's international exchange network.", "bargaining_power_of_suppliers": "Low; international bullion liquidity from global banks.", "threat_of_substitutes": "Low; essential bridal cultural asset.", "competitive_rivalry": "High with Malabar Gold, Kalyan Jewellers, and Bhima Jewellers."}
    ),
    (
        "Trent Limited (Zudio & Westside)", "Apparel, Fashion, Footwear & Jewelry",
        "value-seeking Indian youth, college students, and middle-class fashion shoppers",
        "crave hyper-trendy, runway-inspired fast fashion and modern lifestyle apparel refreshed every two weeks at sub-Rs 999 price points",
        "Zudio Fast Fashion & Westside Curated Brands", "Value Fast Fashion & Curated Departmental Retail",
        "created India's greatest retail fast-fashion phenomenon with Zudio, delivering Zara-like style velocity where 100% of merchandise is priced under Rs 999",
        [0.72, 0.90, 0.96, 0.92, 0.84, 0.76],
        {"political": "Complies with Indian textile trade regulations, GST garment rates, and municipal retail commercial zoning.", "economic": "Industry-leading retail performance; Zudio achieved unprecedented sales densities (>Rs 18,000/sq.ft) and hyper-rapid store payback within 12 months.", "social": "Democratized trendy, contemporary youth fashion for Tier-2 and Tier-3 Indian youth who previously could only afford unbranded roadside clothes.", "technological": "High-velocity supply chain with 15-day design-to-rack turnaround, automated replenishment, and data-driven SKU discontinuation.", "legal": "Textile labeling compliance, Legal Metrology Act, and corporate governance excellence under the Tata Group.", "environmental": "Efficient logistics minimizing inventory write-offs; zero warehouse dead stock due to rapid inventory turns."},
        [0.30, 0.52, 0.35, 0.35, 0.78],
        {"threat_of_new_entrants": "Moderate; many retail brands attempt fast fashion, but nobody matches Zudio's Tata-backed supply chain velocity and unit economics.", "bargaining_power_of_buyers": "Moderate; youth love Zudio's prices and flock in droves, making customer acquisition organic with zero marketing spend.", "bargaining_power_of_suppliers": "Low; garment contract manufacturers in Tirupur and Surat compete aggressively for Zudio's massive predictable volumes.", "threat_of_substitutes": "High from Max Fashion, Reliance Trends, and unorganized street markets.", "competitive_rivalry": "Intense rivalry with Reliance Trends and Max Fashion (Landmark Group)."}
    ),
    (
        "Aditya Birla Fashion and Retail (ABFRL)", "Apparel, Fashion, Footwear & Jewelry",
        "corporate executives, working professionals, and urban menswear shoppers",
        "need sharp, distinguished formal office wear, premium casual attire, and aspirational menswear from trusted heritage brands",
        "Louis Philippe, Van Heusen, Peter England & Allen Solly", "Branded Premium & Mass-Prestige Menswear Portfolio",
        "dominates Indian men's formal and smart-casual wardrobes with four iconic brands spanning mass-market (Peter England) to super-premium luxury",
        [0.68, 0.88, 0.94, 0.88, 0.84, 0.74],
        {"political": "Engages with Ministry of Textiles on domestic fabric processing and cotton yarn export-import policies.", "economic": "Consolidated fashion conglomerate generating over Rs 12,000 Cr across 4,000+ brand stores and Pantaloons retail department network.", "social": "Louis Philippe 'The Upper Crest' and Van Heusen are the definitive status symbols for Indian corporate promotions and business interviews.", "technological": "Omnichannel store fulfillment, 3D body sizing algorithms, wrinkle-free fabric treatments, and digitized loyalty programs.", "legal": "Consumer protection guidelines, garment safety standards, and intellectual property brand enforcement.", "environmental": "Pioneered sustainable apparel initiative 'ReEarth', committing to sustainable cotton sourcing and water conservation in fabric dyeing."},
        [0.30, 0.58, 0.40, 0.32, 0.76],
        {"threat_of_new_entrants": "Low to moderate; building a multi-decade menswear brand with national consumer prestige takes decades of retail presence.", "bargaining_power_of_buyers": "Moderate; professionals pay full price for premium fits, but look for end-of-season sales on casual collections.", "bargaining_power_of_suppliers": "Moderate; massive purchasing scale from textile mills (Grasim, Vardhman) secures preferential fabric rates.", "threat_of_substitutes": "Moderate from international fast fashion brands (Zara, H&M, Uniqlo).", "competitive_rivalry": "High with Raymond, Blackberrys, and Arvind Fashions (Arrow/Tommy Hilfiger)."}
    ),
    (
        "Raymond Limited", "Apparel, Fashion, Footwear & Jewelry",
        "gentlemen, wedding grooms, and discerning connoisseurs of bespoke tailoring",
        "demand the finest worsted wool suiting fabrics, impeccable made-to-measure tailoring, and timeless masculine elegance",
        "The Complete Man Suiting Fabric & Raymond Made-to-Measure", "Worsted Suiting, Bespoke Tailoring & Premium Lifestyle",
        "embodies 'The Complete Man' for over 90 years, operating the world's largest integrated manufacturer of worsted suiting fabric with 20,000+ designs",
        [0.68, 0.88, 0.94, 0.86, 0.84, 0.72],
        {"political": "Key industry leader under the Ministry of Textiles; revitalizing Indian khadi and traditional weaver clusters.", "economic": "Unlocks high shareholder value through strategic demergers (lifestyle apparel vs. real estate); deep pricing power in worsted wool suiting.", "social": "'The Complete Man' advertising campaign redefined Indian masculinity around empathy, family values, and timeless sartorial grace.", "technological": "Super 250s ultra-fine wool weaving technology, automated laser fabric cutters, and 3D digital bespoke tailoring measurement booths.", "legal": "Strict compliance with international textile trade agreements and wool mark certifications.", "environmental": "Advanced zero-liquid discharge textile dyeing plants and sustainable Australian merino wool sourcing ethics."},
        [0.24, 0.50, 0.40, 0.28, 0.65],
        {"threat_of_new_entrants": "Low; worsted wool manufacturing requires specialized European loom machinery, wool-sorting expertise, and century-old trust.", "bargaining_power_of_buyers": "Low to moderate; suiting buyers and wedding parties view Raymond fabric as non-negotiable for custom-tailored suits.", "bargaining_power_of_suppliers": "Moderate; Australian and New Zealand merino wool fleece auctions determine raw fiber costs.", "threat_of_substitutes": "Moderate from ready-made readymade suits and western blazers.", "competitive_rivalry": "Low to moderate; undisputed leader in fine suiting fabrics ahead of OCM and Digjam."}
    ),
    (
        "Vedant Fashions (Manyavar & Mohey)", "Apparel, Fashion, Footwear & Jewelry",
        "Indian grooms, brides, and wedding attendees seeking opulent ethnic celebration wear",
        "need impeccably styled, regal sherwanis, kurtas, lehengas, and ethnic celebration wear for multi-day Indian weddings and festivals",
        "Manyavar Grooms Wear & Mohey Bridal Lehengas", "Branded Indian Celebration & Ethnic Wedding Wear",
        "rules Indian celebration wear with Manyavar holding over 40% organized market share, transforming unbranded wedding shopping into a prestigious branded retail experience",
        [0.68, 0.88, 0.96, 0.88, 0.84, 0.72],
        {"political": "Supports indigenous handloom, zardozi embroidery, and traditional Indian textile craftsmanship under Make in India.", "economic": "Industry-leading financial metrics: gross margins exceeding 67% and ROCE >35% powered by an asset-light franchisee store model.", "social": "Cultural phenomenon: Manyavar made wearing traditional sherwanis and kurtas the aspirational cultural mandate for every Indian groom.", "technological": "Centralized algorithmic inventory management in Kolkata replenishing 600+ stores nationally with zero end-of-season markdown discounts.", "legal": "Intellectual property design registrations protecting proprietary embroidery patterns against local counterfeiters.", "environmental": "Encourages heirloom wedding wear durability, sustainable silk sourcing, and fabric scrap recycling."},
        [0.26, 0.48, 0.35, 0.25, 0.62],
        {"threat_of_new_entrants": "Low; building Manyavar's pan-India 600+ wedding store footprint and emotional wedding advertising resonance requires massive capital.", "bargaining_power_of_buyers": "Low; weddings are once-in-a-lifetime celebrations and families willingly pay full price for groom sherwanis.", "bargaining_power_of_suppliers": "Low; fragmented network of thousands of skilled embroidery artisans across Bengal and Uttar Pradesh.", "threat_of_substitutes": "Moderate from local bespoke wedding tailors and local ethnic bazaars (Chandni Chowk).", "competitive_rivalry": "Low to moderate; dominant organized national player with limited organized corporate competition."}
    ),
    (
        "Page Industries (Jockey India)", "Apparel, Fashion, Footwear & Jewelry",
        "men, women, and youth across urban and semi-urban India",
        "demand supreme cotton comfort, breathable elastic waistbands, and long-lasting durability in daily innerwear, loungewear, and athleisure",
        "Jockey Men's & Women's Innerwear, Loungewear & Athleisure", "Premium Everyday Innerwear & Athleisure Apparel",
        "operates the world's most successful Jockey franchise, distributing premium, comfortable innerwear and athleisure across 110,000+ retail outlets and 1,300+ exclusive stores",
        [0.66, 0.90, 0.96, 0.86, 0.84, 0.74],
        {"political": "Complies with Indian textile labor laws and factory safety standards across massive captive manufacturing units in Karnataka.", "economic": "Legendary stock market compounder; exceptional pricing power, zero promotional discounts, and return on equity consistently >40%.", "social": "Jockey transformed Indian innerwear from an embarrassing hidden commodity into a confident, visible lifestyle fashion statement.", "technological": "Micro-modal fabric blends, seam-free ultrasonic bonding, StayDry sweat-wicking technology, and automated cutting tables.", "legal": "Exclusive master licensee agreement with Jockey International (USA) extending through 2040.", "environmental": "OEKO-TEX certified non-toxic fabric dyeing, zero-discharge garment wash facilities, and captive solar energy."},
        [0.28, 0.50, 0.35, 0.30, 0.70],
        {"threat_of_new_entrants": "Low; replicating Jockey's 110,000-retailer distribution web and sacred consumer fit loyalty is an insurmountable barrier.", "bargaining_power_of_buyers": "Low; consumers buy Jockey innerwear as an essential non-discretionary necessity with near-zero brand switching.", "bargaining_power_of_suppliers": "Low; in-house backward-integrated knitting, dyeing, and elastic manufacturing operations.", "threat_of_substitutes": "Moderate from mass hosiery brands (Rupa, Lux, Dollar) and modern D2C innerwear startups.", "competitive_rivalry": "Moderate; clear undisputed leader in the premium innerwear segment with Van Heusen Innerwear as a distant challenger."}
    ),
    (
        "Metro Brands", "Apparel, Fashion, Footwear & Jewelry",
        "discerning urban families and professionals seeking quality footwear for work, casual, and party wear",
        "need durable, comfortable leather shoes, formal footwear, and trendy casual sandals backed by exceptional in-store service",
        "Metro, Mochi, Walkway & Crocs India Retail", "Multi-Brand Footwear & Accessories Retail Chain",
        "operates India's most profitable multi-brand footwear retail chain with 800+ stores, holding exclusive national distribution partnerships with Crocs and FitFlop",
        [0.66, 0.88, 0.95, 0.88, 0.82, 0.72],
        {"political": "Complies with Bureau of Indian Standards (BIS) mandatory quality control orders (QCO) for footwear manufacturing and import.", "economic": "Highest EBITDA margins in Indian footwear retail (>30%), backed by disciplined inventory turnover and zero debt.", "social": "Multi-generational brand loyalty; Metro and Mochi stores are premier family shoe destinations in Indian malls and high streets.", "technological": "Algorithm-driven inventory replenishment, RFID shoe tracking, and digital customer relationship management driving 70% repeat purchases.", "legal": "BIS quality compliance, exclusive brand licensing contracts, and leasehold retail agreements.", "environmental": "Encourages sustainable footwear materials, polyurethane recycling, and cardboard-minimalist shoe packaging."},
        [0.30, 0.54, 0.38, 0.30, 0.72],
        {"threat_of_new_entrants": "Low; building a profitable national mall footwear retail network requires deep retail real estate relationships and vendor scale.", "bargaining_power_of_buyers": "Moderate; shoppers compare footwear designs and prices across adjacent mall shoe stores.", "bargaining_power_of_suppliers": "Low; fragmented contract footwear manufacturers produce exclusively to Metro's stringent technical specifications.", "threat_of_substitutes": "Moderate from sneaker brands (Nike, Puma) and unorganized shoe bazaars.", "competitive_rivalry": "Moderate to high with Bata India and Reliance Footprint."}
    ),
    (
        "Relaxo Footwears", "Apparel, Fashion, Footwear & Jewelry",
        "mass-market and rural consumers across India seeking unbeatable daily footwear durability",
        "need ultra-durable, waterproof rubber slippers, flip-flops, and affordable casual sandals that withstand rugged daily use at pocket-friendly prices",
        "Hawaii Slippers, Sparx Sports Shoes, Flite & Bahamas", "Mass-Market Rubber Footwear, Flip-Flops & Athleisure",
        "stands as India's largest footwear manufacturer by volume, producing over 600,000 pairs of slippers and shoes daily across 8 mega-plants in Northern India",
        [0.66, 0.90, 0.96, 0.85, 0.82, 0.70],
        {"political": "Direct beneficiary of BIS quality control orders that curb sub-standard cheap footwear dumping from overseas.", "economic": "Immense operational scale enables low unit manufacturing costs; Sparx brand successfully elevated company into higher-margin youth sneakers.", "social": "Relaxo Hawaii chappal is the quintessential working-class footwear of India, worn by farmers, construction workers, and families nationwide.", "technological": "Automated rubber compounding, injection molding machines, and EVA foam direct vulcanization lines in Haryana and Rajasthan.", "legal": "Mandatory BIS footwear certification and labor compliance across massive industrial manufacturing units.", "environmental": "Recycling rubber flash scrap into secondary footwear components and solar rooftop energy integration."},
        [0.26, 0.60, 0.42, 0.35, 0.74],
        {"threat_of_new_entrants": "Low; matching Relaxo's mega-scale rubber vulcanization economics and 50,000-retailer distribution reach is near impossible.", "bargaining_power_of_buyers": "High; rural and semi-urban consumers expect durable slippers for under Rs 150-200 and resist price hikes.", "bargaining_power_of_suppliers": "Moderate; natural rubber prices fluctuate with Kerala plantation yields and crude oil EVA polymer prices.", "threat_of_substitutes": "Moderate from unorganized plastic injection slippers and local footwear makers.", "competitive_rivalry": "High with Walkaroo, Paragon, and Campus Activewear."}
    ),
    (
        "Campus Activewear", "Apparel, Fashion, Footwear & Jewelry",
        "semi-urban youth, college students, and budget-conscious athletic runners across Tier-2/3 India",
        "seek trendy, high-cushion sports sneakers and running shoes that mirror international styles (Nike, Puma) at affordable sub-Rs 2,000 prices",
        "Campus Running Shoes & Lifestyle Sneakers", "Affordable Youth Athleisure & Sports Footwear",
        "rules Indian sports footwear with over 17% market share, bringing high-tech air-capsule cushioning and modern sneaker culture to aspirational youth",
        [0.66, 0.88, 0.95, 0.88, 0.82, 0.70],
        {"political": "Complies with BIS mandatory Footwear Quality Control Order (QCO) enforcing rigorous physical durability tests.", "economic": "Backward-integrated manufacturing in Himachal Pradesh and Uttarakhand enables rapid speed-to-market and attractive entry pricing.", "social": "Taps into the explosive sneakerhead and fitness culture among youth in Tier-2 and Tier-3 Indian towns.", "technological": "Phylon shock-absorbing midsoles, TPU support shanks, knitted breathable uppers, and automated sole injection lines.", "legal": "BIS certification standards, trademark IP protection, and Legal Metrology compliance.", "environmental": "Phasing out toxic solvent-based shoe adhesives in favor of water-based bonding chemicals."},
        [0.32, 0.60, 0.40, 0.35, 0.76],
        {"threat_of_new_entrants": "Moderate; small sneaker startups launch, but scaling pan-India distribution across 20,000+ shoe stores requires heavy working capital.", "bargaining_power_of_buyers": "High; youth compare styling, colors, and prices against Sparx, Asian, and Puma sales.", "bargaining_power_of_suppliers": "Low to moderate; in-house manufacturing of shoe soles, uppers, and assembly.", "threat_of_substitutes": "Moderate from international athletic brands (Puma, Skechers) and regional sneaker makers.", "competitive_rivalry": "Intense rivalry with Relaxo Sparx, Asian Footwears, and Abros."}
    ),
    (
        "Bata India", "Apparel, Fashion, Footwear & Jewelry",
        "multi-generational Indian families, schoolchildren, and office-goers",
        "need reliable, comfortable, and standardized school shoes, formal office leather footwear, and everyday walking sandals",
        "Bata School Shoes, Hush Puppies, Power & Comfit", "Multi-Generational Family Footwear & School Shoes",
        "has shod Indian feet for over 90 years with 2,000+ stores, holding unmatched brand trust in school shoes and comfortable daily walking footwear",
        [0.66, 0.88, 0.95, 0.86, 0.84, 0.72],
        {"political": "Adheres to BIS Quality Control Orders (QCO) and engages with the Council for Leather Exports (CLE).", "economic": "Premiumization strategy expanding casual sneakers (Sneaker Studio) and licensing international brands (Hush Puppies, Nine West).", "social": "Bata is so deeply woven into Indian culture that most citizens believe it is an indigenous Indian company; synonymous with school reopening.", "technological": "OrthoLite memory footbeds, anti-bacterial linings, flexible strobel construction, and ERP-connected nationwide store replenishment.", "legal": "BIS quality certifications, leather trade regulations, and municipal retail lease compliances.", "environmental": "Tannery effluent treatment plants adhering to zero discharge and eco-friendly packaging cartons."},
        [0.28, 0.55, 0.40, 0.30, 0.74],
        {"threat_of_new_entrants": "Low; building Bata's 2,000-store high street and franchise footprint across every Indian district headquarters takes a century.", "bargaining_power_of_buyers": "Moderate; parents trust Bata school shoes for unyielding durability, but compare fashion footwear prices.", "bargaining_power_of_suppliers": "Moderate; procurement from domestic leather clusters (Agra, Kanpur) and international licensors.", "threat_of_substitutes": "High from modern sneaker brands and local footwear stores.", "competitive_rivalry": "High with Metro Brands, Khadim, and Relaxo."}
    ),
    (
        "Fabindia", "Apparel, Fashion, Footwear & Jewelry",
        "culturally conscious urban consumers, intellectuals, and craft connoisseurs",
        "seek authentic, handcrafted handloom ethnic apparel, natural dyed khadi garments, and traditional artisanal home furnishings",
        "Handloom Kurtas, Khadi Ethnic Wear & Artisanal Home Decor", "Artisanal Handcrafted Ethnic Lifestyle & Home Decor",
        "connects over 55,000 rural craft artisans directly with urban consumers, pioneering contemporary handcrafted ethnic wear and sustainable lifestyle living",
        [0.68, 0.86, 0.94, 0.85, 0.84, 0.82],
        {"political": "Celebrates Khadi, Handloom Board, and rural handicraft revival policies, providing sustainable employment in remote villages.", "economic": "Premium lifestyle margins supported by large experience centers combining ethnic fashion, organic food, and home furnishings.", "social": "The quintessential wardrobe choice for Indian artists, academics, and conscious elites valuing traditional handblock printing (Ajrakh, Dabu, Bagru).", "technological": "Computerized supply-chain aggregation connecting decentralized craft clusters, natural vegetable dyeing standardization, and e-commerce.", "legal": "Handloom Mark certifications, Geographical Indication (GI) respect, and fair-trade wage audits.", "environmental": "Pioneered sustainable fashion: hand-spun organic cotton, azo-free natural vegetable dyes, and zero synthetic microfiber shedding."},
        [0.30, 0.50, 0.38, 0.32, 0.68],
        {"threat_of_new_entrants": "Low; direct relationships with 55,000 rural master craftspersons and artisanal cooperatives cannot be built overnight.", "bargaining_power_of_buyers": "Moderate; customers appreciate artisan heritage and accept higher price points for handmade authenticity.", "bargaining_power_of_suppliers": "Low to moderate; decentralized village craft groups rely on Fabindia for guaranteed livelihood orders.", "threat_of_substitutes": "Moderate from commercial ethnic wear brands (W, Biba, Westside) and Khadi Gramodyog.", "competitive_rivalry": "Moderate; competes with Anokhi, Jaypore (ABFRL), and Good Earth."}
    ),
    (
        "Sabyasachi Couture", "Apparel, Fashion, Footwear & Jewelry",
        "high-net-worth brides, royal families, global celebrities, and luxury connoisseurs",
        "demand the pinnacle of Indian royal bridal heritage, handwoven Banarasi textiles, antique zardozi embroidery, and high-jewelry opulence",
        "Sabyasachi Bridal Lehengas, Heritage Fine Jewelry & Accessories", "Ultra-Luxury Heritage Bridal Couture & High Jewelry",
        "stands as India's foremost global luxury house, redefining bridal grandeur with antique Bengal embroidery, royal velvets, and international collaborations (Bergdorf Goodman, Estée Lauder)",
        [0.68, 0.88, 0.96, 0.86, 0.86, 0.75],
        {"political": "Celebrates India's apex luxury soft power globally; champions the preservation of dying handloom weaving and zardozi traditions.", "economic": "Commanding pricing power with bridal lehengas priced from Rs 4 Lakhs to Rs 20 Lakhs+, operating high-revenue flagship mansions in Mumbai, Delhi, and New York.", "social": "The ultimate dream bridal aspiration for millions of Indian brides; revolutionized wedding aesthetics with vintage nostalgia and royal Bengal aesthetics.", "technological": "Archival textile restoration, hand-drawn bespoke miniature paintings for prints, and high-security serialized authenticity tags.", "legal": "Strict global copyright and trademark enforcement against counterfeit bridal knockoffs.", "environmental": "Promotes slow luxury: hand-spun, hand-dyed heirloom garments designed to be passed down through generations rather than discarded."},
        [0.15, 0.35, 0.30, 0.20, 0.50],
        {"threat_of_new_entrants": "Extremely low; Sabyasachi's global design genius, celebrity aura, and royal heritage prestige form an unassailable luxury moat.", "bargaining_power_of_buyers": "Low; affluent brides accept long waiting lists and non-negotiable couture pricing.", "bargaining_power_of_suppliers": "Low; master weavers and embroiderers in Bengal and Varanasi revere the design house for consistent royal patronage.", "threat_of_substitutes": "Low; a Sabyasachi bridal piece is an unmatched cultural status symbol.", "competitive_rivalry": "Low to moderate with luxury couture designers (Manish Malhotra, Tarun Tahiliani)."}
    ),
    (
        "Go Colors (Go Fashion India)", "Apparel, Fashion, Footwear & Jewelry",
        "Indian women and young girls seeking the perfect bottom-wear pairing for kurtas and tops",
        "need instant access to comfortable leggings, palazzos, pants, and jeggings in every conceivable color, fabric, and fit under one roof",
        "Women's Bottom-Wear Portfolio (Leggings, Palazzos, Jeggings, Pants)", "Specialized Women's Bottom-Wear Retail Chain",
        "created and dominates the branded women's bottom-wear category in India with 650+ stores offering 50+ bottom-wear styles in 120+ vibrant colors",
        [0.66, 0.86, 0.94, 0.88, 0.82, 0.72],
        {"political": "Complies with Indian textile trade standards, factory safety norms, and retail establishment regulations.", "economic": "High inventory turns and compact store formats (300-500 sq.ft) generate strong ROCE (>25%) and fast store-level payback.", "social": "Solved the universal daily frustration of Indian women trying to find exact color-matching leggings for their ethnic kurtas.", "technological": "Color-matching inventory replenishment software, four-way stretch elastane fabric engineering, and seamless omnichannel fulfillment.", "legal": "Legal Metrology Act compliance and registered design trademarks.", "environmental": "High-durability cotton-lycra blends that resist pilling and color bleeding across repeated washings."},
        [0.32, 0.52, 0.38, 0.30, 0.68],
        {"threat_of_new_entrants": "Moderate; making leggings is simple, but holding 120 colors in every size across 650 exclusive stores requires inventory mastery.", "bargaining_power_of_buyers": "Moderate; women appreciate Go Colors' fit consistency and shade availability.", "bargaining_power_of_suppliers": "Low; outsourced contract knitting and dyeing clusters in Tirupur compete for Go Colors' bulk business.", "threat_of_substitutes": "Moderate from local tailor-stitched salwars and unbranded local hosiery shops.", "competitive_rivalry": "Low to moderate; undisputed category specialist with Twin Birds as a smaller regional peer."}
    ),
    (
        "Dollar Industries", "Apparel, Fashion, Footwear & Jewelry",
        "mass-market consumers, farmers, and working men across Northern and Eastern India",
        "need durable, highly absorbent cotton vests, briefs, thermal winter wear, and socks at affordable everyday prices",
        "Dollar Bigboss Vests & Briefs, Dollar Ultra Thermal Wear", "Mass Hosiery, Innerwear & Thermal Winterwear",
        "holds over 15% organized market share in Indian hosiery, operating modern spinning and knitting mills in Tirupur with deep rural distribution",
        [0.65, 0.88, 0.94, 0.84, 0.82, 0.70],
        {"political": "Compliant with Ministry of Textiles initiatives, cotton MSP policies, and state industrial safety guidelines.", "economic": "Consistent growth driven by rural consumption and undisputed leadership in northern winter thermal wear (Dollar Ultra).", "social": "Deep presence across millions of rural kirana and apparel shops; endorsed by Bollywood superstars (Akshay Kumar) for masculine strength.", "technological": "Backward-integrated 40,000-spindle spinning mills, circular high-gauge knitting machines, and anti-shrink fabric processing.", "legal": "BIS hosiery testing standards and corporate governance standards.", "environmental": "6 MW captive wind and solar energy generation meeting the majority of manufacturing power requirements in Tamil Nadu."},
        [0.30, 0.60, 0.40, 0.32, 0.75],
        {"threat_of_new_entrants": "Low; building a 120,000-retailer rural wholesale network requires decades of distributor credit relationships.", "bargaining_power_of_buyers": "High; rural consumers are extremely price-sensitive and expect long fabric life.", "bargaining_power_of_suppliers": "Moderate; raw cotton lint prices fluctuate with agricultural monsoon harvests.", "threat_of_substitutes": "High from regional hosiery brands (Lux, Rupa, Amul Macho).", "competitive_rivalry": "Fierce triopoly battle with Rupa & Company and Lux Industries."}
    ),
    (
        "Rupa & Company", "Apparel, Fashion, Footwear & Jewelry",
        "budget-conscious men, women, and kids across urban and semi-urban India",
        "need comfortable, everyday knitted cotton vests, briefs, loungewear, and activewear with proven washing machine durability",
        "Rupa Frontline, Euro & Jon Innerwear Collections", "Knitted Hosiery, Daily Innerwear & Casual Casuals",
        "stands as India's largest knitted innerwear manufacturer by capacity, producing over 1 million pieces of hosiery daily across 4 state-of-the-art plants",
        [0.65, 0.88, 0.94, 0.84, 0.82, 0.70],
        {"political": "Supports domestic garment manufacturing under Make in India; complies with textile worker welfare legislation.", "economic": "Robust balance sheet with zero long-term debt, driving premiumization via modern youth brands (Euro, FCUK licensing).", "social": "Rupa Frontline 'Yeh Aaram Ka Maamla Hai' is a legendary advertising slogan recognized across all Indian states.", "technological": "Imported high-speed circular knitting machines, automated bleach and dye monitoring, and laser-assisted waistband attachment.", "legal": "BIS quality compliance, trademark enforcement, and Legal Metrology standards.", "environmental": "Modern effluent treatment plant with reverse osmosis recycling 95% of water used in fabric dyeing."},
        [0.30, 0.60, 0.40, 0.32, 0.75],
        {"threat_of_new_entrants": "Low; low manufacturing margins and massive scale requirements deter new corporate players.", "bargaining_power_of_buyers": "High; consumers readily switch between Frontline, Cozi, and Bigboss based on pricing.", "bargaining_power_of_suppliers": "Moderate; raw cotton yarn and spandex elastic tape suppliers.", "threat_of_substitutes": "Moderate from local unorganized hosiery and premium international brands.", "competitive_rivalry": "Relentless market share struggle with Lux Industries and Dollar Industries."}
    ),
    (
        "Lux Industries", "Apparel, Fashion, Footwear & Jewelry",
        "mass-market consumers, youth, and athletes across India",
        "demand soft, durable cotton innerwear, stylish boxers, and sweat-wicking gym athleisure at mass-affordable price points",
        "Lux Cozi, ONN Premium Wear & Lyra Women's Leggings", "Mass-Market & Premium Innerwear, Loungewear & Leggings",
        "leads the Indian innerwear sector in manufacturing efficiency, selling hundreds of millions of garments annually powered by Varun Dhawan and Sourav Ganguly campaigns",
        [0.65, 0.88, 0.94, 0.85, 0.82, 0.70],
        {"political": "Complies with Indian textile labor laws and factory safety guidelines across major integrated manufacturing facilities.", "economic": "Successfully diversified from pure men's mass hosiery into high-growth women's leggings (Lyra) and premium men's innerwear (ONN).", "social": "'Apna Luck Pehen Ke Chalo' (Lux Cozi) is deeply ingrained in Indian youth vernacular culture and sports sponsorship.", "technological": "High-efficiency mega-facility in Dankuni, West Bengal integrating knitting, processing, cutting, and packaging under one automated roof.", "legal": "BIS quality certifications and strict monitoring of packaging metrology rules.", "environmental": "Captive solar installations and sustainable dyeing practices minimizing chemical oxygen demand (COD) in wastewater."},
        [0.30, 0.60, 0.40, 0.32, 0.75],
        {"threat_of_new_entrants": "Low; unmatched manufacturing scale and deep distributor penetration create strong defensive moats.", "bargaining_power_of_buyers": "High; consumers expect dependable comfort at accessible price coins (Rs 70-150).", "bargaining_power_of_suppliers": "Moderate; cotton spinning yarn price movements directly affect gross margins.", "threat_of_substitutes": "Moderate from local unbranded innerwear.", "competitive_rivalry": "Intense rivalry with Dollar Industries and Rupa & Company."}
    ),
    (
        "Khadim India", "Apparel, Fashion, Footwear & Jewelry",
        "middle and lower-middle-class families across Eastern and Southern India",
        "need affordable, stylish leather and utility footwear for daily commuting, festive visits, and school needs",
        "Khadim Footwear, British Walkers & Cleo Sandals", "Affordable Family Footwear & Utility Retail Chain",
        "dominates Eastern India footwear retail with 850+ stores, providing durable leather and casual shoes at democratized family-friendly price points",
        [0.64, 0.86, 0.92, 0.84, 0.80, 0.68],
        {"political": "Adheres to BIS mandatory footwear Quality Control Orders (QCO) and Council for Leather Exports policies.", "economic": "Dual business model: high-margin retail store network complemented by extensive B2B wholesale distribution across 10,000+ dealers.", "social": "The trusted family footwear choice in Kolkata and Eastern India for Durga Puja festive shoe purchases.", "technological": "Direct-injected PU sole processing, automated leather stitching, and computerized retail inventory tracking.", "legal": "BIS footwear quality compliance and retail lease regulations.", "environmental": "Zero hazardous chemical adhesives in sole bonding and recycling leather scrap waste."},
        [0.32, 0.60, 0.40, 0.32, 0.72],
        {"threat_of_new_entrants": "Moderate; independent shoe stores exist, but building an 850-store branded retail footprint is difficult.", "bargaining_power_of_buyers": "Moderate to high; price-conscious families compare designs across high street shoe shops.", "bargaining_power_of_suppliers": "Low to moderate; network of small and medium footwear fabricators in Eastern India.", "threat_of_substitutes": "Moderate from Bata India and unorganized footwear markets.", "competitive_rivalry": "High with Bata India and Sreeleathers in Eastern India."}
    ),
    (
        "Mirza International (Red Tape)", "Apparel, Fashion, Footwear & Jewelry",
        "fashion-forward youth, college students, and professionals seeking premium aesthetics at accessible prices",
        "demand stylish leather boots, casual sneakers, and fast-fashion streetwear without paying exorbitant multinational brand prices",
        "Red Tape Leather Footwear & Athleisure Casuals", "Casual Leather Footwear & Value-Fashion Apparel",
        "transformed from a leather shoe exporter into India's fastest-growing youth fashion brand, delivering leather boots and trendy sneakers across 500+ stores",
        [0.65, 0.86, 0.94, 0.86, 0.82, 0.70],
        {"political": "Compliant with BIS footwear standards and Ministry of Commerce export regulations for leather goods.", "economic": "Exceptional retail store expansion and e-commerce growth; demerged retail business to unlock pure-play fashion shareholder value.", "social": "Red Tape is a major status symbol among college youth in North India seeking rugged, stylish boots and casual fashion.", "technological": "In-house leather tanneries in Unnao, robotic sole stitching, and data-driven e-commerce flash sales algorithms.", "legal": "BIS certifications and consumer protection warranty guidelines.", "environmental": "State-of-the-art tannery effluent treatment with zero chrome discharge to protect the Ganges river basin."},
        [0.32, 0.58, 0.40, 0.32, 0.74],
        {"threat_of_new_entrants": "Moderate; apparel entry is easy, but establishing high-quality leather footwear manufacturing requires tanneries.", "bargaining_power_of_buyers": "Moderate; youth love Red Tape's steep e-commerce discounts and bold styling.", "bargaining_power_of_suppliers": "Low; backward-integrated into captive leather tanneries and shoe upper fabrication.", "threat_of_substitutes": "High from international sneaker brands (Puma, Adidas) and fast fashion stores.", "competitive_rivalry": "High with Woodland in rugged leather boots, and Campus in casual sneakers."}
    )
]

for item in sector11_data:
    add_c(*item)

print(f"Sector 11 added: {len(sector11_data)} companies. Total: {len(part2_b)}")

# ==============================================================================
# SECTOR 12: Retail, Quick Commerce & E-Commerce Marketplaces (22 companies)
# ==============================================================================
sector12_data = [
    (
        "Reliance Retail", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "every Indian consumer across grocery, electronics, fashion, and pharma in 7,000+ towns",
        "need convenient, affordable, and comprehensive retail shopping across hypermarkets, neighborhood grocery stores, electronics, and digital delivery",
        "Smart Bazaar, Reliance Digital, Trends & JioMart", "Omnichannel Retail & Digital Commerce Ecosystem",
        "stands as India's largest retailer with over 18,000 stores and 300 million registered customers, integrating physical supermarkets with JioMart digital fulfillment",
        [0.82, 0.96, 0.98, 0.94, 0.88, 0.78],
        {"political": "Direct alignment with national retail policy, farmer direct procurement, and digitized merchant integration (kirana onboarding).", "economic": "Generates over Rs 3,00,000 Cr in gross revenue; massive balance sheet power enables unprecedented supply chain and warehouse capex.", "social": "Touches the daily lives of 1 in 4 Indian citizens; democratized modern supermarket shopping in Tier-2, 3, and 4 towns.", "technological": "JioMart automated micro-fulfillment centers, AI-driven stock forecasting, self-checkout kiosks, and integration with WhatsApp ordering.", "legal": "FDI e-commerce norms, FSSAI licensing, Legal Metrology, and Competition Commission of India (CCI) oversight.", "environmental": "Extensive solarization of mega-warehouses, electric delivery fleets (EV3-wheelers), and plastic waste collection systems."},
        [0.18, 0.50, 0.25, 0.25, 0.65],
        {"threat_of_new_entrants": "Practically impossible; no entity can match Reliance Retail's 18,000-store physical footprint and multi-billion dollar capital moat.", "bargaining_power_of_buyers": "Moderate; consumers enjoy steep discounts and loyalty points, but have alternative neighborhood stores.", "bargaining_power_of_suppliers": "Low; FMCG and electronics brands must sell through Reliance Retail, giving Reliance tremendous purchasing discount power.", "threat_of_substitutes": "Moderate from neighborhood unorganized kirana shops and quick commerce.", "competitive_rivalry": "Moderate; leads the physical retail market by a massive margin ahead of DMart and Tata/Trent."}
    ),
    (
        "Avenue Supermarts (DMart)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "budget-conscious middle and lower-middle-class Indian families",
        "demand the absolute lowest grocery, staple, and household goods prices in town without gimmicks or loyalty fees",
        "DMart Hypermarkets & DMart Ready", "Low-Price High-Velocity Brick-and-Mortar Supermarkets",
        "pioneered India's most profitable grocery retail model: owning real estate, paying suppliers in 10 days for massive cash discounts, and passing all savings to shoppers",
        [0.70, 0.94, 0.98, 0.88, 0.86, 0.74],
        {"political": "Operates strictly within municipal commercial development zoning and conforms to state retail trade policies.", "economic": "Consistently generates the highest sales per square foot in Indian retail with negative working capital cycles and rock-solid balance sheets.", "social": "The ultimate monthly grocery destination for middle-class Indian families who wait in weekend queues for unmatched grocery savings.", "technological": "Hyper-optimized warehouse pallet cross-docking, automated inventory re-ordering, and lean point-of-sale checkout scanners.", "legal": "FSSAI food safety regulations, fire safety clearances, and strict Legal Metrology compliance.", "environmental": "Energy-efficient store layouts with zero decorative frills, LED high-bay lighting, and cardboard carton recycling."},
        [0.22, 0.48, 0.22, 0.28, 0.68],
        {"threat_of_new_entrants": "Low; replicating DMart's owned-real-estate strategy and 10-day supplier payment goodwill takes billions of dollars and decades.", "bargaining_power_of_buyers": "Low to moderate; customers already receive the lowest market prices in town, creating fanatical store loyalty.", "bargaining_power_of_suppliers": "Extremely low; FMCG brands willingly give DMart their best prices because DMart pays them in 10 days vs. the 45-day industry average.", "threat_of_substitutes": "Moderate from quick-commerce apps for top-up purchases, but DMart dominates planned monthly bulk grocery baskets.", "competitive_rivalry": "Moderate; operates with distinct structural cost superiority over Reliance Smart and Spencer's."}
    ),
    (
        "Shoppers Stop", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "affluent urban shoppers, fashion enthusiasts, and luxury beauty seekers",
        "need premier departmental shopping environments offering curated international fashion, premium cosmetics, and personal shopper styling",
        "Shoppers Stop Department Stores & SS Beauty", "Premium Multi-Brand Departmental & Luxury Beauty Retail",
        "pioneered modern department store retail in India, serving over 9 million First Citizen loyalty members with curated luxury beauty and apparel brands",
        [0.66, 0.86, 0.94, 0.88, 0.82, 0.70],
        {"political": "Complies with municipal mall retail regulations, commercial leasing standards, and consumer protection laws.", "economic": "High-margin beauty and luxury cosmetics segment driving strong store sales growth; strong contribution from private label apparel.", "social": "Aspirational shopping destination for urban middle and upper-middle-class Indians seeking premium brands under one roof.", "technological": "Omnichannel integration, personalized AI styling assistants, smart fitting rooms, and digital loyalty reward redemption.", "legal": "Consumer protection regulations, authentic cosmetic import compliance, and legal leasehold covenants.", "environmental": "Green building mall certifications, energy-efficient store HVAC, and eco-friendly shopping bags."},
        [0.30, 0.54, 0.38, 0.32, 0.72],
        {"threat_of_new_entrants": "Moderate; building a 100-store premium department store chain requires anchor tenant positioning in premier malls.", "bargaining_power_of_buyers": "Moderate; affluent shoppers have choices among individual standalone brand stores and online luxury portals.", "bargaining_power_of_suppliers": "Moderate; international cosmetic brands (MAC, Estée Lauder, Clinique) negotiate concession store terms.", "threat_of_substitutes": "High from Nykaa Luxe and direct brand mono-brand stores.", "competitive_rivalry": "High with Lifestyle (Landmark Group) and Tata CliQ Luxury."}
    ),
    (
        "Flipkart", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "hundreds of millions of digital shoppers across metros, tier-2, tier-3, and rural India",
        "need a massive online selection of smartphones, electronics, fashion, and appliances with guaranteed delivery and easy cash-on-delivery",
        "Flipkart Marketplace, SuperCoins & The Big Billion Days", "Horizontal Multi-Category E-Commerce Marketplace",
        "built India's indigenous e-commerce revolution, pioneering Cash on Delivery, 30-day returns, and the historic Big Billion Days festive shopping extravaganza",
        [0.76, 0.92, 0.98, 0.96, 0.85, 0.74],
        {"political": "Monitored closely under DPIIT FDI e-commerce guidelines and proposed national e-commerce policies regarding marketplace neutrality.", "economic": "Powers hundreds of billions of rupees in gross merchandise value (GMV); backed by Walmart, driving massive supply chain investments.", "social": "Brought modern electronic appliances and smartphones into millions of small-town Indian homes that lacked physical malls.", "technological": "Proprietary search and recommendation engines, vernacular voice search in 11 Indian languages, and automated fulfillment sorting centers.", "legal": "Competition Commission of India (CCI) scrutiny, consumer protection e-commerce rules, and DPDP Act compliance.", "environmental": "Pioneered EV delivery fleet adoption (EV100 initiative), eliminated single-use plastic packaging across supply chain fulfillment hubs."},
        [0.25, 0.60, 0.35, 0.30, 0.75],
        {"threat_of_new_entrants": "Very low; building a nationwide automated logistics backbone (Ekart) and buyer-seller ecosystem costs billions of dollars.", "bargaining_power_of_buyers": "High; consumers actively compare smartphone and TV prices between Flipkart and Amazon during festive sales.", "bargaining_power_of_suppliers": "Moderate; large electronics brands negotiate exclusive launch windows, but millions of marketplace third-party sellers are price-takers.", "threat_of_substitutes": "Moderate from Amazon India, quick-commerce dark stores, and physical electronics stores (Croma, Reliance Digital).", "competitive_rivalry": "Intense, historic duopoly battle with Amazon India."}
    ),
    (
        "Blinkit", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "busy urban professionals, working couples, and young families in top Indian metros",
        "need instant delivery of daily milk, bread, fresh vegetables, emergency stationery, and electronics in under 10 minutes",
        "Blinkit 10-Minute Hyperlocal Delivery & Dark Store Network", "Hyperlocal 10-Minute Quick Commerce Platform",
        "pioneered the 10-minute quick commerce revolution in India, operating a dense network of localized dark stores that deliver groceries and electronics in 8-12 minutes",
        [0.72, 0.90, 0.96, 0.96, 0.82, 0.70],
        {"political": "Engages with state labor departments on gig worker social security codes and municipal dark-store zoning regulations.", "economic": "Acquired by Zomato; fastest-growing retail business in India, turning contribution-margin positive through dense dark-store order clustering.", "social": "Fundamentally altered urban consumption behavior, eliminating the concept of planned weekly grocery trips for millions of city dwellers.", "technological": "Algorithmic dark-store rack layouts enabling 2-minute order picking, real-time rider dispatch telemetry, and predictive stocking.", "legal": "FSSAI licensing for dark stores, Legal Metrology compliance, and gig workforce legal frameworks.", "environmental": "Accelerating transition to 100% electric delivery 2-wheelers and paper bag packaging."},
        [0.32, 0.58, 0.35, 0.32, 0.82],
        {"threat_of_new_entrants": "Moderate; high capital burn required to build localized dark-store density and rider fleets.", "bargaining_power_of_buyers": "High; urban users keep Blinkit, Zepto, and Instamart on their phones and choose whichever delivers fastest.", "bargaining_power_of_suppliers": "Low; FMCG brands view quick commerce as their fastest-growing sales channel and pay high ad-rates for top search placement.", "threat_of_substitutes": "Moderate from local kirana stores and traditional supermarkets.", "competitive_rivalry": "Fierce triopoly war with Zepto and Swiggy Instamart."}
    ),
    (
        "Zepto (KiranaKart Technologies)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "Gen-Z youth, tech professionals, and modern households seeking hyper-speed grocery and cafe treats",
        "demand lightning-fast 10-minute grocery delivery combined with piping-hot brewed coffee, fresh snacks, and curated electronics",
        "Zepto 10-Minute Delivery & Zepto Cafe", "Quick-Commerce Dark Store Network & On-Demand Micro-Cafe",
        "reaches consumers in 10 minutes with surgical dark-store precision, pioneering Zepto Cafe to deliver freshly brewed tea, coffee, and croissants alongside groceries",
        [0.70, 0.90, 0.96, 0.96, 0.82, 0.68],
        {"political": "Complies with gig economy labor welfare directives, local municipal permissions, and traffic safety rules for delivery fleets.", "economic": "Achieved multi-billion dollar valuation and rapid path to EBITDA breakeven through high order density and advertising monetization.", "social": "Founded by teenage Stanford dropouts, becoming an inspirational beacon of Indian youth entrepreneurial hustle.", "technological": "Proprietary picker app guiding warehouse workers to retrieve items within 90 seconds, and dynamic route optimization.", "legal": "FSSAI compliance, dark store commercial registrations, and consumer privacy protections.", "environmental": "Rapidly deploying EV delivery bikes and utilizing recyclable paper delivery bags."},
        [0.35, 0.60, 0.35, 0.32, 0.82],
        {"threat_of_new_entrants": "Moderate; requires hundreds of millions of dollars of venture capital to secure dark-store leases and rider liquidity.", "bargaining_power_of_buyers": "High; urban consumers have near-zero brand loyalty and switch based on delivery fee or item availability.", "bargaining_power_of_suppliers": "Low; consumer brands compete aggressively for banner ads and prominent catalog placement inside Zepto.", "threat_of_substitutes": "Moderate from Blinkit, Instamart, and street vendors.", "competitive_rivalry": "Relentless market share competition with Blinkit and Swiggy Instamart."}
    ),
    (
        "Swiggy Instamart", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "urban consumers, foodies, and households needing groceries, fresh produce, and party supplies on demand",
        "need instant grocery and convenience delivery seamlessly unified with food delivery within a single high-trust super-app",
        "Instamart Quick Grocery & Swiggy One Membership", "Integrated Quick Commerce & Consumer Food Super-App",
        "powers millions of daily instant orders by leveraging Swiggy's massive delivery fleet and 1-tier Swiggy One subscription ecosystem",
        [0.72, 0.90, 0.96, 0.95, 0.82, 0.70],
        {"political": "Operates within municipal trade licensing and engages in national gig-worker platform policy consultations.", "economic": "Substantial operational synergy with food delivery: shared delivery fleet balances peak meal hours with daytime grocery replenishment.", "social": "Essential daily utility for urban Indians; Swiggy One membership creates sticky habitual behavior across food and groceries.", "technological": "Unified app architecture, machine learning dark-store inventory replenishment, and dynamic rider routing algorithms.", "legal": "FSSAI food hygiene licensing, consumer protection e-commerce rules, and statutory listing compliance.", "environmental": "Aggressive EV fleet transition and sustainable packaging protocols across fulfillment dark stores."},
        [0.32, 0.58, 0.35, 0.30, 0.80],
        {"threat_of_new_entrants": "Moderate; building a parallel quick-commerce delivery network requires massive balance sheet strength.", "bargaining_power_of_buyers": "High; consumers compare prices and wait times with Blinkit and Zepto.", "bargaining_power_of_suppliers": "Low; brands pay premium promotional fees to reach Swiggy's high-spending urban user base.", "threat_of_substitutes": "Moderate from physical supermarkets and dark-store rivals.", "competitive_rivalry": "Intense triopoly rivalry with Blinkit and Zepto."}
    ),
    (
        "Nykaa (FSN E-Commerce Ventures)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "modern Indian women, beauty enthusiasts, and luxury cosmetics consumers",
        "demand 100% authentic, curated beauty, skincare, and luxury cosmetics backed by trusted beauty tutorials and advice",
        "Nykaa Beauty Marketplace & Nykaa Luxe Stores", "Omnichannel Beauty & Personal Care Lifestyle Platform",
        "built India's premier beauty destination with 100% guaranteed product authenticity, seamlessly blending e-commerce content with 150+ high-end retail stores",
        [0.70, 0.88, 0.96, 0.92, 0.85, 0.74],
        {"political": "Compliant with national e-commerce policies and CDSCO regulations against counterfeit imported cosmetics.", "economic": "Rare profitable consumer internet powerhouse; high average order values and strong advertising revenues from global beauty conglomerates.", "social": "Founded by investment banker Falguni Nayar; transformed Indian women's relationship with self-care and beauty empowerment.", "technological": "Curated beauty content video platform, personalized AI skin-tone finder, and automated cosmetic temperature-controlled warehousing.", "legal": "Strict supplier authentication contracts, consumer protection guidelines, and intellectual property brand safety.", "environmental": "Eco-friendly recyclable cardboard packaging and expansion of sustainable, cruelty-free 'Conscious at Nykaa' beauty brands."},
        [0.28, 0.52, 0.38, 0.30, 0.72],
        {"threat_of_new_entrants": "Low; earning deep consumer trust in product authenticity and securing exclusive luxury brand contracts (Charlotte Tilbury, Huda Beauty) is difficult.", "bargaining_power_of_buyers": "Moderate; beauty buyers are loyal to Nykaa's reward points and authenticity, but cross-shop festive discounts.", "bargaining_power_of_suppliers": "Moderate; global beauty giants partner with Nykaa as their definitive gateway to the Indian market.", "threat_of_substitutes": "Moderate from multi-category e-commerce (Amazon, Myntra) and physical beauty retail.", "competitive_rivalry": "Moderate to high with Tata CliQ Palette, Tira (Reliance Retail), and Purplle."}
    ),
    (
        "Meesho (Fashnear Technologies)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "price-conscious consumers, homemakers, and small-town shoppers across Bharat (Tier-2, 3, 4+ towns)",
        "need ultra-affordable unbranded fashion, home utilities, and accessories delivered with free shipping and zero seller commissions",
        "Meesho Zero-Commission Social Marketplace", "Democratized Value E-Commerce for Bharat",
        "revolutionized e-commerce for Bharat with a 0% seller commission model, unlocking millions of small manufacturers and making fashion affordable at sub-Rs 300",
        [0.72, 0.92, 0.98, 0.94, 0.82, 0.70],
        {"political": "Praised for empowering micro, small, and medium enterprises (MSMEs) and women home resellers under Digital India.", "economic": "Asset-light third-party logistics model; achieved order-volume parity with legacy e-commerce giants through hyper-lean operational costs.", "social": "Democratized online shopping for 150+ million first-time internet users in rural and non-metro India.", "technological": "Lightweight Android app optimized for low-end smartphones and slow 3G/4G connections, and AI-driven catalog recommendations.", "legal": "Marketplace intermediary guidelines under IT Act and consumer protection rules.", "environmental": "Collaborates with third-party logistics partners to optimize delivery vehicle load capacities and minimize packaging layers."},
        [0.32, 0.65, 0.30, 0.32, 0.78],
        {"threat_of_new_entrants": "Moderate; zero-commission marketplace economics require massive scale and low fraud rates to survive.", "bargaining_power_of_buyers": "High; Bharat consumers are exceptionally price-sensitive and compare prices to local weekly haats and bazaars.", "bargaining_power_of_suppliers": "Low; over 1 million small manufacturers and wholesalers rely on Meesho for national market access.", "threat_of_substitutes": "High from local street markets and Shopsy (Flipkart).", "competitive_rivalry": "Direct competition with Shopsy (Flipkart) and Amazon Bazaar."}
    ),
    (
        "FirstCry (Brainbees Solutions)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "expectant parents, new mothers, and families with babies and young children",
        "need a complete, trusted one-stop shopping destination for baby diapers, maternity essentials, infant nutrition, toys, and kids' clothing",
        "FirstCry SuperStore & Babyhug In-House Brand", "Omnichannel Baby, Kids & Maternity Commerce Platform",
        "stands as Asia's largest baby and kids retail powerhouse, combining an expansive online catalog with 1,000+ specialized neighborhood stores and hospital gifting programs",
        [0.70, 0.88, 0.96, 0.90, 0.84, 0.74],
        {"political": "Supports child healthcare and safety standards, adhering to BIS norms for baby feeding bottles and toys.", "economic": "Highly profitable private label brand (Babyhug) accounts for significant revenue share, boosting retail gross margins.", "social": "Deep emotional trust with mothers; hospital gift hampers touch millions of Indian parents right at the birth of their newborn.", "technological": "Integrated omnichannel inventory tracking, personalized parenting milestone app, and automated regional mother-and-child fulfillment centers.", "legal": "BIS toy safety standards, FSSAI baby infant food compliance, and consumer protection regulations.", "environmental": "Uses non-toxic BPA-free baby plastics and organic cotton baby clothing lines."},
        [0.25, 0.50, 0.35, 0.28, 0.65],
        {"threat_of_new_entrants": "Low; baby and child care requires immense parental safety trust and specialized multi-category inventory that general retailers struggle to manage.", "bargaining_power_of_buyers": "Moderate; parents prioritize infant health and hygiene safety over cheap unbranded alternatives.", "bargaining_power_of_suppliers": "Low to moderate; global baby brands (Pampers, Chicco, Johnson's) rely heavily on FirstCry's parenting distribution.", "threat_of_substitutes": "Moderate from local chemist shops and general supermarkets.", "competitive_rivalry": "Low to moderate; clear undisputed national leader in the organized baby and kids retail segment."}
    ),
    (
        "Lenskart", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "spectacle wearers, contact lens users, and sunglass lovers across India, Southeast Asia, and the Middle East",
        "need precision eye testing, stylish trendy frames, and accurate prescription lenses at transparent, affordable prices",
        "Lenskart Robotic Eyewear & Vincent Chase / John Jacobs Collections", "Omnichannel Prescription Eyewear & Optical Technology",
        "transformed eyewear from a medical prosthetic into a fashionable accessory with 2,000+ omnichannel stores, 3D face-analysis try-ons, and robotic lens manufacturing",
        [0.70, 0.90, 0.96, 0.95, 0.85, 0.74],
        {"political": "Supports National Programme for Control of Blindness; provides free digital eye testing across all retail outlets.", "economic": "Built the world's largest eyewear manufacturing mega-factory in Bhiwadi, cutting lens fabrication costs by over 70% and driving global expansion.", "social": "Eliminated the stigma of wearing glasses for Indian youth, offering affordable Buy-One-Get-One (Gold Membership) fashion frames.", "technological": "Automated German robotic edgers and laser cutters with zero human touch; 3D face-mapping algorithms for virtual optical try-ons.", "legal": "BIS standards for optical lenses and CDSCO medical device regulations for corrective prescription eyewear.", "environmental": "Automated precision manufacturing cuts plastic lens grinding waste; eco-friendly bio-acetate frame collections."},
        [0.22, 0.50, 0.32, 0.26, 0.65],
        {"threat_of_new_entrants": "Low; building a 2,000-store optical chain and an automated mega-factory producing 50 million pairs of glasses annually is prohibitive.", "bargaining_power_of_buyers": "Moderate; consumers love the BOGO membership deals and free eye tests, creating high customer lifetime value.", "bargaining_power_of_suppliers": "Low; backward-integrated into owned lens fabrication and frame casting.", "threat_of_substitutes": "Moderate from local independent opticians and Titan Eye+.", "competitive_rivalry": "Moderate; dominates the organized eyewear market with Titan Eye+ as a primary corporate competitor."}
    ),
    (
        "Purplle (Manash Lifestyle)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "beauty lovers and young women in Tier-2, Tier-3, and semi-urban Indian cities",
        "need personalized, budget-friendly beauty and skincare products tailored to diverse Indian complexions without paying metro salon prices",
        "Purplle Beauty Marketplace & In-House Brands (Good Vibes)", "Affordable Personalized Beauty Discovery Platform",
        "empowers women in Bharat with personalized beauty discovery, driving millions of affordable orders through proprietary recommendation technology and Good Vibes naturals",
        [0.64, 0.85, 0.94, 0.92, 0.82, 0.72],
        {"political": "Complies with national e-commerce guidelines and cosmetics regulatory standards.", "economic": "Achieved unicorn valuation with high capital efficiency by focusing sharply on high-growth, underserved Tier-2/3 beauty shoppers.", "social": "Democratizes modern skincare and beauty awareness in non-metro towns where physical branded beauty counters do not exist.", "technological": "AI-driven Beauty Intelligence recommendation engine mapping skin tones and skin types to specific cosmetic ingredients.", "legal": "CDSCO cosmetics compliance and truth-in-advertising guidelines.", "environmental": "Transitioning to recyclable paper packaging and promoting clean herbal skincare formulations."},
        [0.34, 0.60, 0.38, 0.35, 0.78],
        {"threat_of_new_entrants": "Moderate; beauty marketplaces face heavy customer acquisition costs on social media.", "bargaining_power_of_buyers": "High; value-conscious Tier-2 consumers cross-shop sales discounts on Nykaa and Amazon.", "bargaining_power_of_suppliers": "Low to moderate; indie cosmetics brands rely on Purplle for targeted non-metro distribution.", "threat_of_substitutes": "High from Nykaa and local neighborhood cosmetics shops.", "competitive_rivalry": "Intense rivalry with Nykaa in online beauty retail."}
    ),
    (
        "IndiaMART InterMESH", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "Indian small and medium enterprises (MSMEs), manufacturers, and wholesale buyers",
        "need verified, cost-effective business leads and direct discovery to buy and sell industrial machinery, raw materials, and wholesale supplies",
        "IndiaMART B2B Marketplace & Lead Management System", "B2B SME Discovery & Matchmaking Marketplace",
        "stands as India's largest B2B discovery platform with over 7.5 million suppliers, 175 million buyers, and 100 million listed products",
        [0.72, 0.92, 0.96, 0.94, 0.84, 0.72],
        {"political": "Critical engine for MSME growth, partnering with Government of India's Champions portal and national industrial directories.", "economic": "Exceptional subscription cash flows: collects annual subscription fees upfront from suppliers, generating debt-free multi-crore cash reserves.", "social": "The economic lifeline of Indian industrial clusters (Rajkot, Ludhiana, Surat, Coimbatore), connecting small workshop owners directly to national buyers.", "technological": "AI/NLP behavioral matchmaking algorithms, instant buyer requirement distribution, and integrated conversational RFQ tools.", "legal": "IT Act intermediary safe harbor, verified vendor KYC certifications, and trademark protection.", "environmental": "Pure-play digital software matchmaking platform with minimal direct environmental footprint; promotes local domestic sourcing to cut freight emissions."},
        [0.20, 0.45, 0.25, 0.25, 0.58],
        {"threat_of_new_entrants": "Low; the network effect of 7.5 million suppliers and 175 million buyers creates an insurmountable two-sided marketplace moat.", "bargaining_power_of_buyers": "Low; SME suppliers willingly renew paid subscription tiers because IndiaMART generates their primary business revenue leads.", "bargaining_power_of_suppliers": "None; buyers use the discovery platform completely free.", "threat_of_substitutes": "Moderate from Google Search, TradeIndia, and physical trade expos.", "competitive_rivalry": "Low to moderate; dominant undisputed leader in Indian B2B online discovery ahead of TradeIndia."}
    ),
    (
        "TradeIndia (Infocom Network)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "industrial manufacturers, exporters, and wholesale traders across India",
        "require targeted trade leads, international buyer matchmaking, and digital trade catalogs for machinery, chemicals, and industrial goods",
        "TradeIndia B2B Portal & Digital Trade Solutions", "B2B Industrial Discovery & Export Marketplace",
        "pioneered online B2B directories in India, facilitating billions of dollars in domestic and export transactions for over 5 million registered businesses",
        [0.70, 0.90, 0.94, 0.90, 0.84, 0.70],
        {"political": "Supports export promotion councils (FIEO, EEPC) and SME digital empowerment initiatives.", "economic": "Predictable subscription revenues from manufacturing exporters and industrial suppliers across Tier-1 and Tier-2 industrial belts.", "social": "Empowers traditional family manufacturing businesses to find export buyers across the Middle East, Africa, and Europe.", "technological": "Digital product catalogs, automated inquiry routing, and mobile CRM applications for small business sales teams.", "legal": "Compliance with digital intermediary regulations and commercial dispute arbitration mechanisms.", "environmental": "Digital trade catalogs replace millions of printed paper industrial directories and trade fair brochures."},
        [0.26, 0.50, 0.30, 0.28, 0.65],
        {"threat_of_new_entrants": "Low; building a 5-million business directory and verified supplier database requires decades of tele-sales operations.", "bargaining_power_of_buyers": "Moderate; suppliers evaluate lead generation conversion rates against IndiaMART.", "bargaining_power_of_suppliers": "None; buyers browse industrial catalogs for free.", "threat_of_substitutes": "High from IndiaMART and Google Business profiles.", "competitive_rivalry": "Direct competitor to IndiaMART in domestic SME matchmaking."}
    ),
    (
        "Udaan (Hiveloop Technology)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "neighborhood kirana stores, small retail chemists, and rural shopkeepers",
        "need direct wholesale procurement of FMCG goods, staples, and electronics with transparent pricing, working capital credit, and doorstep delivery",
        "Udaan B2B Wholesale Commerce & Trade Credit Platform", "B2B Wholesale E-Commerce & Kirana Supply Chain",
        "connected over 3 million neighborhood retailers directly with national FMCG brands and millers, eliminating multi-tier wholesale distributor middlemen",
        [0.72, 0.90, 0.95, 0.94, 0.84, 0.72],
        {"political": "Works within state agricultural produce marketing committee (APMC) frameworks and digital trade formalization policies.", "economic": "Powers massive wholesale trade volume across Bharat, providing crucial short-term working capital trade credit to small retailers.", "social": "Empowers small corner kirana stores to compete with modern hypermarkets by providing them with the same wholesale price discounts.", "technological": "High-throughput wholesale order routing, automated freight dispatch, and algorithmic credit underwriting via transaction data.", "legal": "FSSAI compliance for bulk food staples, RBI NBFC regulations for trade credit lending, and GST compliance.", "environmental": "Consolidates wholesale shipments to neighborhood stores, eliminating multiple unorganized diesel tempos and reducing urban traffic congestion."},
        [0.28, 0.58, 0.38, 0.30, 0.74],
        {"threat_of_new_entrants": "Moderate; building a national wholesale logistics and warehousing network requires hundreds of millions of dollars.", "bargaining_power_of_buyers": "Moderate; kirana owners compare prices with traditional local wholesale mandis.", "bargaining_power_of_suppliers": "Moderate; FMCG brands balance Udaan with their traditional authorized distributor networks.", "threat_of_substitutes": "High from traditional wholesale mandis and Jiomart B2B.", "competitive_rivalry": "Intense rivalry with Reliance JioMart B2B and traditional FMCG wholesale distributors."}
    ),
    (
        "Pepperfry (Trendsutra)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "new urban homeowners, apartment dwellers, and interior decor enthusiasts",
        "need a massive online selection of quality wooden furniture, modular sofas, and home decor backed by doorstep assembly and physical touch-and-feel studios",
        "Pepperfry Managed Marketplace & Studio Pepperfry Experience Centers", "Omnichannel Managed Furniture & Home Living Marketplace",
        "stands as India's leading online furniture destination, operating 200+ Studio Pepperfry experience centers and a specialized heavy-item logistics network",
        [0.66, 0.85, 0.93, 0.90, 0.82, 0.74],
        {"political": "Supports furniture industrial clusters in Jodhpur, Saharanpur, and Channapatna under Make in India.", "economic": "High average order values (>Rs 18,000) and strong marketplace commission take-rates on home decor and furniture.", "social": "Made buying furniture online acceptable and safe for Indian families through offline Studio consultations and 3D room visualization.", "technological": "Proprietary heavy-furniture logistics tracking (Pepcart), 3D AR furniture room-placement, and modular flat-pack engineering.", "legal": "Consumer protection warranty rules and Legal Metrology Act packaged commodity compliances.", "environmental": "Promotes legally harvested sustainable sheesham and teak wood; transitions to recycled protective cardboard corner packaging."},
        [0.32, 0.55, 0.40, 0.32, 0.70],
        {"threat_of_new_entrants": "Low; building a specialized nationwide heavy-cargo delivery fleet that handles fragile wooden furniture without damage is a major barrier.", "bargaining_power_of_buyers": "Moderate; furniture is a high-involvement long-term investment, so buyers research multiple stores and local carpenters.", "bargaining_power_of_suppliers": "Low to moderate; fragmented artisanal furniture workshops in Rajasthan rely on Pepperfry for national market access.", "threat_of_substitutes": "High from traditional local timber furniture markets and D2C brands (Wakefit, Urban Ladder).", "competitive_rivalry": "Moderate; competes with Wakefit, IKEA India, and local furniture bazaars."}
    ),
    (
        "Urban Company", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "busy urban homeowners and professionals across India and global cities",
        "need verified, background-checked, and standardized home services (AC repair, deep cleaning, plumbing, at-home salon) delivered on time",
        "Standardized Home Services & Urban Company Salon at Home", "Managed On-Demand Home & Personal Services Platform",
        "standardized the chaotic Indian home services industry, training and empowering 50,000+ independent service professionals with guaranteed quality standards",
        [0.72, 0.90, 0.96, 0.95, 0.84, 0.74],
        {"political": "Aligned with Skill India Mission and National Skill Development Corporation (NSDC), formalizing and certifying unorganized service technicians.", "economic": "Exceptional unit economics and take-rates (>25%), generating strong operating cash flows with international operations in UAE and Singapore.", "social": "Dramatically increased middle-class micro-entrepreneur incomes: service partners earn 2-3x more than unorganized manual labor.", "technological": "Automated technician dispatch, IoT smart AC diagnostic tools, in-app service training video modules, and transparent upfront pricing.", "legal": "Intermediary guidelines, consumer protection standards, and partner insurance coverage protocols.", "environmental": "Standardized eco-friendly cleaning chemicals, water-saving foam jet AC cleaning tools, and battery recycling for tools."},
        [0.22, 0.50, 0.30, 0.25, 0.62],
        {"threat_of_new_entrants": "Low; establishing standardized quality training centers, background verifications, and brand trust across 50,000 gig professionals is an immense moat.", "bargaining_power_of_buyers": "Moderate; customers appreciate standardized pricing and background-checked trust, making them loyal to the platform.", "bargaining_power_of_suppliers": "Low; individual service technicians and beauticians depend on Urban Company for a steady stream of high-paying jobs.", "threat_of_substitutes": "Moderate from local unvetted neighborhood handymen and traditional beauty parlors.", "competitive_rivalry": "Low to moderate; undisputed dominant market leader in organized home services across urban India."}
    ),
    (
        "BigBasket (Supermarket Grocery Supplies / Tata)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "urban Indian households, weekly planners, and discerning culinary home chefs",
        "demand a comprehensive 50,000+ item grocery selection, certified organic farm produce, and scheduled convenient delivery slots without missing items",
        "BigBasket Scheduled Delivery & BB Daily Fresh Subscriptions", "Full-Basket Online Supermarket & Farm-Direct Produce",
        "operates India's largest full-basket online supermarket with Tata Group backing, sourcing fresh produce directly from 30,000+ farmers across 60+ collection centers",
        [0.72, 0.90, 0.96, 0.94, 0.85, 0.78],
        {"political": "Supports direct farmer procurement bypassing middlemen, compliant with national food logistics regulations.", "economic": "High average basket size (>Rs 1,500) driven by planned monthly grocery shopping; high gross margins from private label staples (Royal, Fresho).", "social": "The pioneer of online grocery in India, building multi-year trust with families for delivering fresh, unbruised fruits and vegetables.", "technological": "High-density automated fulfillment warehouses, cold-chain refrigerated delivery vans, and predictive AI fresh produce ordering.", "legal": "FSSAI central licensing, organic certifications for Fresho Organic, and Legal Metrology compliance.", "environmental": "Massive electric vehicle delivery fleet rollout, battery-swapping stations, and collection of reusable plastic delivery crates."},
        [0.26, 0.55, 0.32, 0.30, 0.75],
        {"threat_of_new_entrants": "Low; building a 50,000-SKU temperature-controlled warehouse network and farmer-sourcing cold chain requires massive capital.", "bargaining_power_of_buyers": "Moderate; planned grocery buyers value BigBasket's item completeness and scheduled delivery reliability.", "bargaining_power_of_suppliers": "Low; FMCG brands and farmers rely on BigBasket's massive purchasing volume.", "threat_of_substitutes": "High from quick-commerce dark stores (Blinkit, Zepto) for top-up needs, and DMart for physical bulk buying.", "competitive_rivalry": "High with JioMart, Amazon Fresh, and quick commerce platforms."}
    ),
    (
        "Spencer's Retail (RP-Sanjiv Goenka Group)", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "affluent urban shoppers and gourmet food lovers in Eastern and Northern India",
        "need upscale supermarket shopping offering international specialty foods, imported cheeses, exotic fresh produce, and premium lifestyle goods",
        "Spencer's Gourmet Hypermarkets & Nature's Basket", "Upscale Gourmet Grocery & Specialty Food Hypermarket",
        "stands as India's pioneer in experiential food retail, combining Spencer's hypermarkets with Nature's Basket to offer the country's finest imported gourmet curation",
        [0.66, 0.85, 0.92, 0.86, 0.82, 0.72],
        {"political": "Complies with municipal retail licensing, food import regulations, and Legal Metrology standards.", "economic": "Commands higher average spend per customer driven by high-margin imported condiments, artisanal cheeses, and gourmet bakery.", "social": "Aspirational shopping experience for urban food connoisseurs, expatriates, and NRI families who cook international cuisines.", "technological": "Omnichannel store delivery within 2 hours, computerized humidity-controlled display chillers, and digital loyalty rewards.", "legal": "FSSAI compliance for imported packaged foods, labeling norms, and liquor retail licensing where applicable.", "environmental": "Promotes sustainable paper and jute shopping bags; utilizes energy-efficient refrigeration compressors."},
        [0.32, 0.54, 0.40, 0.32, 0.72],
        {"threat_of_new_entrants": "Moderate; specialty gourmet sourcing requires cold-chain import networks and premium mall real estate.", "bargaining_power_of_buyers": "Moderate; affluent gourmet buyers are quality-sensitive rather than price-sensitive.", "bargaining_power_of_suppliers": "Moderate; international gourmet specialty food importers (olive oils, cheeses, chocolates).", "threat_of_substitutes": "Moderate from modern quick-commerce gourmet tabs and high-end standalone grocers.", "competitive_rivalry": "Moderate to high with Foodhall and premium supermarket chains."}
    ),
    (
        "V-Mart Retail", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "aspirational middle and lower-middle-class families across Tier-2, Tier-3, and Tier-4 towns",
        "crave modern, air-conditioned family apparel and lifestyle department store shopping at affordable, localized price points",
        "V-Mart Family Fashion Department Stores & Unlimited Fashion", "Value Fashion Departmental Retail for Bharat",
        "pioneered modern retail in small-town India ('The King of Tier-2 Retail'), operating 450+ stores that bring mall-quality fashion to semi-urban families",
        [0.68, 0.88, 0.95, 0.86, 0.82, 0.70],
        {"political": "Complies with state commercial retail shop regulations and supports local employment in non-metro towns.", "economic": "Ultra-lean store fit-out costs and direct manufacturing sourcing deliver high inventory turns and attractive return on invested capital.", "social": "Provides a respectful, modern air-conditioned retail shopping experience for families who historically only had crowded local street stalls.", "technological": "Centralized computerized point-of-sale inventory replenishment, automated warehouse dispatch, and omni-channel customer WhatsApp messaging.", "legal": "Legal Metrology Act, standard garment labeling rules, and fire safety norms.", "environmental": "Energy-efficient LED lighting across stores and reduction of single-use plastic carry bags."},
        [0.32, 0.60, 0.38, 0.35, 0.76],
        {"threat_of_new_entrants": "Moderate; opening standalone stores is possible, but scaling an optimized 450-store Tier-3 supply chain is very challenging.", "bargaining_power_of_buyers": "High; small-town shoppers have limited disposable income and scrutinize every rupee spent on clothes.", "bargaining_power_of_suppliers": "Low; garment contract fabricators in Ludhiana and Surat produce exclusively for V-Mart's large volume orders.", "threat_of_substitutes": "High from local unorganized town bazaars and Zudio.", "competitive_rivalry": "Intense rivalry with Zudio, Style Baazar, and Vishal Mega Mart."}
    ),
    (
        "Vishal Mega Mart", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "mass-market working-class families and budget shoppers across Tier-1, 2, and 3 India",
        "need a hyper-value one-stop destination for discount clothing, packaged grocery staples, cookware, and household plastic essentials",
        "Vishal Mega Mart Discount Department Stores", "Hyper-Value Apparel, Grocery & Household Goods Megastores",
        "operates 550+ mega-stores delivering massive basket value, where families can buy a complete outfit, monthly rice, and cookware under one roof at bottom-dollar prices",
        [0.68, 0.90, 0.96, 0.86, 0.82, 0.70],
        {"political": "Compliant with state commercial establishment acts and consumer retail standards; major generator of grassroots youth employment.", "economic": "High revenue per store driven by a powerful blend of high-margin private label apparel and high-velocity packaged grocery staples.", "social": "The definitive family weekend shopping hub for industrial workers, auto drivers, teachers, and small-town families.", "technological": "High-speed billing systems, barcode inventory tracking, automated central distribution hubs, and digital discount coupons.", "legal": "FSSAI compliance for private label food staples, Legal Metrology, and commercial fire safety.", "environmental": "Minimizes packaging waste through bulk packaging and encourages multi-use canvas shopping bags."},
        [0.30, 0.62, 0.38, 0.35, 0.76],
        {"threat_of_new_entrants": "Low to moderate; operating 550+ large-format discount stores with profitable unit economics requires massive operational discipline.", "bargaining_power_of_buyers": "High; customers are strictly bargain hunters looking for the cheapest viable family clothing and staples.", "bargaining_power_of_suppliers": "Low; manufacturers must offer aggressive bulk discounts to get onto Vishal Mega Mart shelves.", "threat_of_substitutes": "High from local town weekly haats and regional value grocers.", "competitive_rivalry": "High with V-Mart, Reliance Smart, and DMart."}
    ),
    (
        "City Kart Retail", "Retail, Quick Commerce & E-Commerce Marketplaces",
        "budget-conscious rural and small-town youth across Uttar Pradesh, Bihar, and Jharkhand",
        "seek trendy, ultra-affordable fast-fashion apparel, festive wear, and footwear suited to local Hindi-heartland tastes at sub-Rs 500 price points",
        "City Kart Family Value Fashion Stores", "Hyper-Affordable Fast Fashion for Heart-Land India",
        "brings fast fashion to the grassroots of UP and Bihar with 100+ stores, delivering vibrant festival fashion and winter wear tailored to local cultural aesthetics",
        [0.66, 0.86, 0.94, 0.84, 0.80, 0.68],
        {"political": "Supports regional commercial development and youth retail employment in underdeveloped districts of eastern India.", "economic": "Lean capital expenditure per store allows rapid breakeven in tier-3 and tier-4 towns with populations under 100,000.", "social": "Celebrates local festivities (Chhath Puja, Eid, Diwali) with specialized regional ethnic clothing collections.", "technological": "Computerized regional warehouse distribution, localized trend forecasting, and low-cost POS retail billing systems.", "legal": "Textile labeling compliance, Legal Metrology rules, and local trade licenses.", "environmental": "Energy-efficient store cooling and cardboard packaging recycling."},
        [0.35, 0.65, 0.38, 0.38, 0.78],
        {"threat_of_new_entrants": "Moderate; local cloth merchants compete, but lack City Kart's organized store layout and centralized bulk buying power.", "bargaining_power_of_buyers": "High; rural shoppers evaluate fabric weight and price fiercely.", "bargaining_power_of_suppliers": "Low; relies on bulk garment manufacturers across Delhi-NCR and Surat.", "threat_of_substitutes": "High from local weekly village bazaars and V-Mart.", "competitive_rivalry": "High with V-Mart and local traditional garment merchants."}
    )
]

for item in sector12_data:
    add_c(*item)

print(f"Sector 12 added: {len(sector12_data)} companies. Total in Part 2B: {len(part2_b)}")

# Load part2_a.json and combine
part2_a_path = Path(__file__).parent / "part2_a.json"
with open(part2_a_path, "r", encoding="utf-8") as f:
    part2_a = json.load(f)

full_part2 = part2_a + part2_b
print(f"Combined Part 2 count: {len(full_part2)} companies (Expected: 131).")

# Save to scratch/part2.json
out_path = Path(__file__).parent / "part2.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(full_part2, f, indent=2)

print(f"SUCCESS: Saved {len(full_part2)} companies to {out_path}")
