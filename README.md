# CI-Strains-Pro 🌿

![Status: Phase 9 COMPLETE](https://img.shields.io/badge/Status-Phase%209%20COMPLETE-brightgreen)
![Partner: Amazon Q](https://img.shields.io/badge/AI_Partner-Amazon_Q-blueviolet)
![Data Tier: Premium](https://img.shields.io/badge/Data_Tier-Premium-gold)
![Strains: 21,400](https://img.shields.io/badge/Strains-21,400-blue)

**Cannabis Intelligence (CI)** is the new standard for validated cultivation data.  
This repo is the professional "Clean Room" — transforming **21,706 raw HTML archives** into **21,400 AI-validated strains** with commercial-grade intelligence.

**🔒 LIVE NOW**: [strains.loyal9.app](https://strains.loyal9.app) - Verify every strain against timestamped HTML archives

---

## 🏆 What We Just Built (January 29, 2026)

**Phase 6-9: Full Extraction Pipeline COMPLETE**

✅ **Phase 6**: 21,943 breeders extracted & standardized (519 unique breeders)  
✅ **Phase 7**: 21,706 HTML files unified in S3 (100% archive coverage)  
✅ **Phase 8**: 21,361 strains with full botanical data (38 fields extracted)  
✅ **Phase 9**: 21,400 strains AI-validated (39,681 corrections, $0.04 cost)  
✅ **95% confidence rate** (only 1,089 strains flagged for review)  
✅ **100% source traceability** (every strain → URL + S3 archive)  
✅ **Production-ready dataset** with validated strain names & breeders  

**This is what AI-accelerated data engineering looks like.**

From raw HTML to validated dataset in 4 phases. Gemini 2.0 Flash processed 21,400 strains in 45 minutes with exponential backoff handling rate limits. Cost: $0.04 (96% under budget). Ready for deduplication & master merge.

**Previous Achievement (Jan 17)**: Phase 5 Master Dataset + Marketplace Strategy - 3-tier pricing model ($500-$12,500)

---

## 🎯 The CI Vision
Turn messy cannabis data into the world's most comprehensive cultivation ecosystem — blending AI science with real-world growing documentation.

## 📋 Roadmap at a Glance

| Phase | Milestone                          | Status       | Target   |
|-------|------------------------------------|--------------|----------|
| 1     | Foundation Database (15k Strains)  | ✅ Complete  | Research |
| 2     | Source of Truth & Inventory        | ✅ Complete  | Mapping  |
| 3     | Enhanced S3 Extraction (20K+)      | ✅ Complete  | Proof    |
| 4     | Source of Truth Viewer             | ✅ Complete  | Trust    |
| 5     | Master Dataset & Marketplace       | ✅ Complete  | **$15K** |
| 6     | Breeder Extraction (21,943)        | ✅ Complete  | Quality  |
| 7     | S3 Unified Inventory (21,706)      | ✅ Complete  | Archive  |
| 8     | Full Botanical Extraction (21,361) | ✅ Complete  | Data     |
| 9     | Vertex AI Validation (21,400)      | ✅ Complete  | **$0.04**|
| 10    | Deduplication & Master Merge       | 🚧 In Progress | Clean  |
| 11    | Gumroad Launch (Raw Tier)          | 📋 Planned | $5K      |
| 12    | Clean + AI Tiers                   | 📋 Planned | $50K     |

## 📊 Current Pipeline Status (Jan 29, 2026)

### Phase 2: Source of Truth ✅ COMPLETE
- **Total Inventory**: 14,840 strain URLs mapped to seed banks
- **S3 Archive**: 19,776 HTML pages with metadata
- **Coverage**: 100% HTML archive achieved
- **Mapping**: Full URL-to-seedbank distribution established

### Phase 3: S3 Unified Inventory ✅ COMPLETE
- **Consolidated S3 Structure**: 21,706 HTML files in unified location
- **Metadata System**: 21,706 JSON files with URL-to-hash mappings
- **Elite Integration**: 3,153 elite seed bank strains added to inventory
- **Ready for Extraction**: All 19 seed banks accessible via unified S3 path

### Phase 3: Enhanced S3 Extraction ✅ COMPLETE

**Total Database**: **21,706 strains** across 19 seed banks (exceeded 20K milestone by 1,706!)

### Phase 4: Source of Truth Viewer ✅ COMPLETE
- **CloudFront Distribution**: Free-tier CDN with signed URLs (5-min expiration)
- **Lambda Function**: URL validation + signed URL generation via Secrets Manager
- **Frontend**: Legal disclaimer, GA4 tracking, seed bank filters, strain search
- **Security**: Multi-layer legal protection, watermarks, opt-out process
- **Domain**: strains.loyal9.app (SSL configured)
- **Cost**: $0.40/month (Secrets Manager only, all else free tier)

### Phase 5: Master Dataset (Raw Data) ✅ COMPLETE
- **Total Strains**: 23,000 (removed 9 non-product pages)
- **Botanical Fields**: 38 fields (genetics, cannabinoids, effects, cultivation)
- **Source Traceability**: 100% (every strain has URL + S3 archive key)
- **Data Quality**: 96.87% (Vertex AI validation)
- **Output**: `pipeline/05_master_dataset/output/master_strains_raw.csv`
- **Sample**: 100-row sample for marketplace preview
- **Documentation**: DATA_DICTIONARY.md, VALIDATION_REPORT.md, SEED_BANK_COVERAGE.md, LICENSE.md

### Phase 6: Breeder Extraction ✅ COMPLETE
- **Total Breeders**: 21,943 strains with breeder data
- **Standardization**: 580 raw → 519 unique breeders
- **Coverage**: 100% across 19 seed banks
- **Output**: `all_breeders_cleaned.csv` with standardized names

### Phase 7: S3 Unified Inventory ✅ COMPLETE
- **Total Files**: 21,706 HTML files in unified S3 structure
- **Metadata**: 21,706 JSON files with URL-to-hash mappings
- **Archive Coverage**: 100% of extracted strains
- **Purpose**: Single source of truth for re-extraction

### Phase 8: Full Botanical Extraction ✅ COMPLETE
- **Total Strains**: 21,361 strains with complete profiles
- **Fields Extracted**: 38 botanical fields per strain
- **Success Rate**: 98.4% (345 duplicates removed)
- **Output**: `all_strains_extracted.csv` ready for validation

### Phase 9: Vertex AI Validation ✅ COMPLETE
- **Total Validated**: 21,400 strains (Gemini 2.0 Flash)
- **Corrections Made**: 39,681 (1.85 per strain)
- **Flagged for Review**: 1,089 (5.1%)
- **Cost**: $0.04 (96% under budget)
- **Runtime**: 45 minutes with rate limit handling
- **Output**: `all_strains_validated.csv` with confidence scores

| Seed Bank              | Status       | Strains Extracted | Columns | Data Coverage |
|------------------------|--------------|-------------------|---------|---------------|
| Attitude Seed Bank     | ✅ Complete  | 7,673             | 95      | 45.2%         |
| Crop King              | ✅ Complete  | 3,336             | 97      | 54.1%         |
| North Atlantic         | ✅ Complete  | 2,727             | 118     | 52.1%         |
| Gorilla Seed Bank      | ✅ Complete  | 2,009             | 51      | 30.9% THC     |
| Neptune                | ✅ Complete  | 1,995             | 111     | 48.3%         |
| Multiverse Beans       | ✅ Complete  | 799               | 83      | 43.7%         |
| Herbies Seeds          | ✅ Complete  | 753               | 35      | 99.9% THC     |
| Sensi Seeds            | ✅ Complete  | 620               | 131     | 46.7%         |
| Seed Supreme           | ✅ Complete  | 353               | 1,477   | 51.8%         |
| Mephisto Genetics      | ✅ Complete  | 245               | 83      | 55.6%         |
| Exotic Genetix         | ✅ Complete  | 227               | 10      | Genetics      |
| Amsterdam Marijuana    | ✅ Complete  | 163               | 66      | 97.5% THC     |
| Barney's Farm          | ✅ Complete  | 88                | 94      | 60.6%         |
| Royal Queen Seeds      | ✅ Complete  | 67                | 115     | 58.4%         |
| Dutch Passion          | ✅ Complete  | 44                | 160     | 56.8%         |
| Seeds Here Now         | ✅ Complete  | 43                | 150     | 48.6%         |
| ILGM                   | ✅ Complete  | 133             | 25      | 97.7% THC     |
| Great Lakes Genetics   | ✅ Complete  | 16                | 41      | 52.5%         |
| Seedsman               | ✅ Complete  | 866               | 79      | 100% THC      |

**Latest Achievement**: **JavaScript Rescrape & Extraction Mission - 100% Success!** 🎯  
**Rescrape**: 1,011/1,011 URLs with JavaScript rendering (4h 24m, zero failures)  
**Extraction**: 999/1,011 strains extracted (98.8% success rate)  
- **ILGM**: 133/133 strains, 25 columns, 97.7% THC coverage (from 6.8%)  
- **Seedsman**: 866/878 strains, 79 columns, 100% THC coverage (from 0%)  
**Total Database**: **21,395 strains** across 19 seed banks - ALL COMPLETE!

## 💰 Project Economics (29 Days)
**Total Investment**: **$116.88**  
- AWS: $25.62 (S3 storage, CloudFront, Lambda, Secrets Manager)  
- Bright Data: $41.27 (proxy network)  
- ScrapingBee: $49.99 (monthly sub)  
- Google Cloud: $0.00 (credits - $1,200+ remaining)  

**ROI Target**: $15K (Phase 5 completion)  
**Current Status**: Phase 9 COMPLETE - 21,400 validated strains ready for deduplication

## 🛠 Transparency & Attribution – The Real Human-AI Partnership

This project is **not** "AI-generated."  
It is **AI-accelerated**, **human-directed**, and **human-verified** at every critical step.

A solo human had the vision, paid the bills, did the brutal manual grinds (32+ hours of lineage cleaning alone), fixed the bugs, and made the final calls.  
The AIs provided speed, scale, and second opinions — but the soul, scrutiny, and sweat came from one person.

**Shannon Goddard** (The Architect & The Grind)  
- 19 years of operational leadership and deep cannabis domain expertise  
- Designed the vision, roadmap, and ecosystem  
- Performed all manual deep dives, bug fixes, and quality gates  
- Paid for everything (Bright Data, ScrapingBee, AWS, coffee, sanity)

**Amazon Q** (The Builder & Infrastructure Partner)  
- Built the heavy-lifting backbone: S3 archival logic, bulletproof scraping pipelines, seed-bank processors, and high-volume extraction scripts  
- Designed and executed JavaScript rescrape mission: 1,011/1,011 URLs (100% success, 4h 24m, $0 cost)  
- Created JS extraction pipelines for ILGM and Seedsman: 999/1,011 strains extracted (98.8% success)  
- Co-designed the production-grade architecture that scaled to 21,400 validated strains across 19 seed banks  
- Built Source of Truth Viewer infrastructure in under 2 minutes: CloudFront distribution, Lambda function, frontend with legal framework, GA4 tracking, and security layers (11 files, zero errors)
- Designed marketplace strategy: 3-tier pricing model ($500-$12,500), commercial license with legal protections, comprehensive documentation package (data dictionary, validation report, seed bank coverage), and 26-task launch checklist for Gumroad deployment
- Executed Phases 6-9: Breeder extraction (21,943 strains), S3 unification (21,706 files), full botanical extraction (21,361 strains), and Vertex AI validation (39,681 corrections at $0.04)

**Gemini Flash 2.0** (The Auditor & Validation Partner)  
- Ran the initial 100% URL verification sweep on 15,778 records  
- Performed Phase 3 HTML enhancement (93% success on 13,328+ strains)  
- Designed the Source of Truth flagging system and confidence scoring  
- Validated 21,400 strains in Phase 9: 39,681 corrections with 95% confidence rate
- Provided strategic mapping and second-pair-of-eyes validation across the CI Ecosystem

**Grok** (The Word Master & Hype Sidekick)  
- Polished the daily build log, README sections, and narrative throughout the journey  
- Kept the transparency real, the tone honest, and the motivation high  
- Served as the external sounding board for roadmap sanity checks and motivational boosts

**The Real Breakdown**  
The AIs provided **scale** and **speed**.  
The human provided **vision**, **scrutiny**, **endurance**, and **the willingness to swear at spreadsheets at 3 a.m.**  

"The AI did the heavy lifting; Shannon did the heavier lifting."  
🌿 Built with blood, sweat, coffee, Vertex credits, and a whole lot of cursing — all in public.

[View the Full Ecosystem Roadmap](./docs/ROADMAP.md)  
## 🌿 Powered by Cannabis Intelligence
> *[Mission Statement Snippet]*: Establishing the global standard for validated botanical data through Human-AI partnership.

![CI Power Icon](./assets/branding/ci-badge-color.svg)

**[Read more about the CI Vision & Logo Concept](./assets/docs/logo_concept.md)**