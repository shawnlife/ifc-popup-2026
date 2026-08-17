# IFC Cape Town Pop-Up 2026 — Event Website Brief

## Project Overview
Build a mobile-first, single-page-app-style static website for the IFC Cape Town Pop-Up 2026 conference. The site will be hosted on GitHub Pages initially, then moved to a custom domain (likely ifc.shawnlife.com or similar). Attendees will scan a QR code on the day to access the schedule on their phones, so mobile experience is the top priority.

---

## Technical Requirements
- Single HTML file with embedded CSS and JS (no build tools, no frameworks)
- Must work perfectly on mobile (375px+) and desktop
- Font: **Graphik** — load via CSS @font-face or closest Google Fonts fallback (Inter is acceptable if Graphik unavailable)
- No external JS dependencies except what is absolutely needed
- All internal navigation via anchor links (no page reloads)
- Fast load time — images should be lazy loaded
- Accessible: keyboard navigable, sufficient colour contrast

---

## Colour Palette
- Primary orange: `#F49404`
- Primary dark (background): `#303249`
- White: `#FFFFFF`
- Light grey (cards/surfaces): `#3D3F5A` (slightly lighter than background)
- Muted text: `#A0A3C0`

---

## Site Structure — 3 Sections (Single Page, Tabbed Navigation)

Navigation bar at top with 3 tabs:
1. **Schedule**
2. **Sessions**
3. **Speakers**

On mobile, nav sticks to the top. Active tab is highlighted in orange. Clicking a tab scrolls to or reveals that section.

---

## Section 1: Schedule

### Hero (above schedule)
- IFC Pop-Up logo (file: `logo.png` — place in `/images/` folder)
- Headline: **Welcome to the IFC Cape Town Pop-Up 2026**
- Subtext: *2 September 2026 | Homecoming Centre, District Six, Cape Town*
- CTA button: **Get Your Tickets** → https://qkt.io/IFCCPT2026 (opens in new tab, orange button)

### Schedule Table
Display as a **vertical time-based list**. Each time slot shows the two concurrent sessions side by side (Star Theatre | Avalon Theatre). On mobile, stack them vertically with clear room labels.

For single-room slots (Opening, Closing, Remarks, Breaks, Lunch), span full width.

Session titles in the schedule should be **hyperlinked** to the corresponding anchor on the Sessions section.
Speaker names in the schedule should be **hyperlinked** to the corresponding anchor on the Speakers section.

#### Schedule Data:

| Time | Star Theatre | Avalon Theatre |
|------|-------------|----------------|
| 8:00 – 9:00 | **Registration** — In the lobby. Name tags, QR code to this site at info desk. Sponsors set up along lobby walls. | — |
| 9:00 – 9:15 | **Opening Remarks** — Nyasha and Shawn welcome everyone, housekeeping, thank sponsors | — |
| 9:15 – 10:00 | **OPENING PLENARY** — The Duality of Giving: The Rise and Reach of African Philanthropy As A Global Phenomenon — Olumide "Mide" Akerewusi *(joining virtually)* | — |
| 10:10 – 10:55 | **Session 1A** — The State of Fundraising in South Africa: Trends, Compliance, and What's Coming — Moderated by Delphino Machikicho with Jenni McLeod, Sophie Olivier, Farida Lavangee & Nick Rockey | **Session 1B** — A Playbook for Implementing AI in a Nonprofit Organisation — Ian Parsons |
| 10:55 – 11:20 | **Tea Break** — Free tea & coffee in the lobby. Coffee bar open for paid drinks. | — |
| 11:20 – 12:05 | **Session 2A** — The Power of a Supporter-Led Campaign: The Story of Paws on the Path — Angela Blackwell & Toni Erasmus | **Session 2B** — Using Your Team's Strengths for Corporate Partnerships: Director-Fundraiser Synergy — Miche Nicholas & Casey Prince |
| 12:15 – 13:00 | **Session 3A** — Funder Panel: What Donors Are Really Looking For — Moderated by Malusi Ntoyapi with Shona Young, Nomsa Muthaphuli & Nondumiso Mabuya | **Session 3B** — Profit For Purpose: The Need to Reframe Our Strategic Thinking — Damian Chapman |
| 13:00 – 14:00 | **Lunch** — Tafel Space. Boxed lunches by Cooktastic, drinks by Homecoming Centre. Bar open for additional purchases. | — |
| 14:00 – 14:45 | **Session 4A** — You Can't Build Tomorrow's Impact with Yesterday's Funding: A Social Enterprise Story — Leana de Beer | **Session 4B** — Small Donations, Big Impact: Recurring Donors for Sustainable Income — Alison Young |
| 14:55 – 15:40 | **Session 5A** — Impact Management and Measurement: The Impact Validation Fundraising Requires — Reana Rossouw & Colleen Francis | **Session 5B** — More Than Followers: Building a Community That Actually Takes Action — Roland Postma & Phano Liphoto |
| 15:40 – 16:00 | **Tea Break** — Free tea & coffee in the lobby. Coffee bar open for paid drinks. | — |
| 16:00 – 16:45 | **CLOSING PLENARY** — The CEO and the Fundraiser: Building a Culture Where Both Can Thrive — Chantel Cooper & Cheryl Manikam | — |
| 16:45 – 17:00 | **Closing Remarks** — Thank sponsors, share about IFC Amsterdam | — |

---

## Section 2: Sessions

Each session gets its own card with:
- Session title (large, orange)
- Room label badge (Star Theatre / Avalon Theatre) + Plenary badge where applicable
- Speaker name(s) — each hyperlinked to their anchor on the Speakers section
- Session description (full text below)
- International speaker badge where applicable (Mide, Damian)

Each session card has an HTML anchor ID for deep linking from the schedule.

### Session Data:

**Anchor: #opening-plenary**
**OPENING PLENARY — Star Theatre**
*The Duality of Giving: The Rise and Reach of African Philanthropy As A Global Phenomenon*
Speaker: [Olumide "Mide" Akerewusi](#mide-akerewusi) *(International — joining virtually)*
Description: This Keynote is a journey of discovery into the unprecedented rise and recognition of African philanthropy as a force for social and environmental transformation in our world today. What should we know and how can we identify opportunities to engage Africans on their terms as they practice traditional Western forms of philanthropy, while also demonstrating the uniqueness of a totally African interpretation of generosity? Hear Mide Akerewusi share stories, statistics, and surveys that point to a new African philanthropy converging into one of the world's most unique and prolific forms of giving.

---

**Anchor: #session-1a**
**Session 1A — Star Theatre**
*The State of Fundraising in South Africa: Trends, Compliance, and What's Coming*
Speakers: [Delphino Machikicho](#delphino-machikicho) (Moderator), [Jenni McLeod](#jenni-mcleod), [Sophie Olivier](#sophie-olivier), [Farida Lavangee](#farida-lavangee), [Nick Rockey](#nick-rockey)
Description: This panel of experts will share their views on the current South African fundraising landscape, including sector updates, emerging trends, and what organisations might be missing out on. Come prepared to hear about everything from individual giving, grants and foundations, compliance, accounting, and corporate social investment.

---

**Anchor: #session-1b**
**Session 1B — Avalon Theatre**
*A Playbook for Implementing AI in a Nonprofit Organisation*
Speaker: [Ian Parsons](#ian-parsons)
Description: A practical approach to implementing AI, with knowledge shares from nonprofit leaders. What are the risks of doing nothing, and where does ethics fit into the picture? How to manage changing roles and expectations, and how to ensure sensitive data remain secure and AI responses are accurate and true.

---

**Anchor: #session-2a**
**Session 2A — Star Theatre**
*The Power of a Supporter-Led Campaign: The Story of Paws on the Path*
Speakers: [Angela Blackwell](#angela-blackwell), [Toni Erasmus](#toni-erasmus)
Description: Angela and Toni share how Paws on the Path raised R500,000, generated significant awareness, and created a lasting legacy by sponsoring four future guide dogs for the SA Guide-Dogs Association for the Blind. Together, they share the story, partnerships, and lessons learned from the campaign, offering practical insights for organisations seeking to amplify supporter-led fundraising initiatives.

---

**Anchor: #session-2b**
**Session 2B — Avalon Theatre**
*Using Your Team's Strengths for Corporate Partnerships: Director-Fundraiser Synergy*
Speakers: [Miche Nicholas](#miche-nicholas), [Casey Prince](#casey-prince)
Description: Join Miche and Casey to hear how aligning a Director's strategic vision with a Fundraiser's relationship-building creates a seamless, reliable experience for businesses. You'll learn how their tag-team approach turns cold corporate outreach into warm, high-trust alliances where partners always know exactly who they are working with, what they are investing in, and how together, you build long-term impact.

---

**Anchor: #session-3a**
**Session 3A — Star Theatre**
*Funder Panel: What Donors Are Really Looking For*
Speakers: [Malusi Ntoyapi](#malusi-ntoyapi) (Moderator), [Shona Young](#shona-young), [Nomsa Muthaphuli](#nomsa-muthaphuli), [Nondumiso Mabuya](#nondumiso-mabuya)
Description: We'll be sitting down with philanthropic foundation leaders to open a dialogue between fundraisers and the people they are seeking funding from. What do funders see when reviewing grant applications? What makes a nonprofit stand out? How do you build lasting relationships? How can nonprofits collaborate for more success? Attendees will hear both the hard truths and the positive insights regarding the sector's direction. Since applying for endless grants consumes significant time for NPOs, conversations like these help fundraisers focus their energy effectively.

---

**Anchor: #session-3b**
**Session 3B — Avalon Theatre**
*Profit For Purpose: The Need to Reframe Our Strategic Thinking*
Speaker: [Damian Chapman](#damian-chapman) *(International)*
Description: Nonprofits around the world are leaking money from their fundraising operations without even realising it... and calling ourselves nonprofits is making it worse. In this session, we'll launch the findings from working with over 20 African purpose organisations who are changing how they see themselves, how they're changing the way they do things, and how you can see how much profit you're leaking in your organisation.

---

**Anchor: #session-4a**
**Session 4A — Star Theatre**
*You Can't Build Tomorrow's Impact with Yesterday's Funding: A Social Enterprise Story*
Speaker: [Leana de Beer](#leana-de-beer)
Description: As social challenges evolve, so too must the way we design solutions and finance them. This session shares WaFunda's evolution from an idea incubated within a nonprofit to an independent social enterprise, showing how programme innovation and capital innovation continuously shaped one another. Sustainable impact depends on both.

---

**Anchor: #session-4b**
**Session 4B — Avalon Theatre**
*Small Donations, Big Impact: Recurring Donors for Sustainable Income*
Speaker: [Alison Young](#alison-young)
Description: NGOs are continually under pressure to secure funding in order to sustain and expand their charitable work. Traditional fundraising efforts often focus on government grants, corporate partnerships, and other Corporate Social Investment (CSI) initiatives. However, every contribution makes a difference. This session will explore how developing a loyal base of recurring donors — regardless of the size of their individual contributions — can create a reliable and sustainable source of ongoing income over time.

---

**Anchor: #session-5a**
**Session 5A — Star Theatre**
*Impact Management and Measurement: The Impact Validation Fundraising Requires*
Speakers: [Reana Rossouw](#reana-rossouw), [Colleen Francis](#colleen-francis)
Description: This session will focus on the value and importance of Impact Management and Measurement (IMM) to support fundraising efforts. Funders no longer focus on activities and outputs but want assurance and evidence that their investments will yield credible and sustainable impact. The session will include the case study of Shonaquip Social Enterprise and their application and integration of IMM practices.

---

**Anchor: #session-5b**
**Session 5B — Avalon Theatre**
*More Than Followers: Building a Community That Actually Takes Action*
Speakers: [Roland Postma](#roland-postma), [Phano Liphoto](#phano-liphoto)
Description: Roland and Phano share how Young Urbanists has used social media and personal storytelling to build a genuine community of supporters who don't just engage online but show up and make a difference for their cause, from mobilising people around local initiatives and events to collaborating with other organisations. The session will explore how putting a face to an organisation builds trust and connection, and what it takes to turn an online following into real-world participation.

---

**Anchor: #closing-plenary**
**CLOSING PLENARY — Star Theatre**
*The CEO and the Fundraiser: Building a Culture Where Both Can Thrive*
Speakers: [Chantel Cooper](#chantel-cooper), [Cheryl Manikam](#cheryl-manikam)
Description: As CEO and Head of Fundraising, Chantel Cooper and Cheryl Manikam will share an honest and practical look at what it takes to build a strong partnership between leadership and fundraising. Through lived examples, they will explore how trust, alignment, clear roles and a purpose-driven and high performing culture can create the conditions for both fundraising success and organisational impact to thrive.

---

## Section 3: Speakers

Display as a **grid of cards** — 3 columns on desktop, 2 columns on tablet, 1 column on mobile.

Each speaker card contains:
- Headshot (circular or rounded square, from `/images/headshots/` folder — filename should match speaker slug e.g. `chantel-cooper.jpg`)
- Full name (bold)
- Title & Organisation (muted)
- Short bio (collapsed by default on mobile, expandable on tap)
- LinkedIn button/icon → opens in new tab

Each card has an HTML anchor ID for deep linking from schedule and sessions.

### Speaker Data (anchor ID | name | title | org | LinkedIn | headshot filename):

| Anchor | Name | Title | Organisation | LinkedIn |
|--------|------|-------|-------------|---------|
| #chantel-cooper | Chantel Cooper | CEO | The Children's Hospital Trust | https://www.linkedin.com/in/chantelcooper/ |
| #cheryl-manikam | Cheryl Manikam | Head of Fundraising | The Children's Hospital Trust | https://www.linkedin.com/in/cheryl-manikam-7868876a/ |
| #alison-young | Alison Young | Head of Performance Marketing | National Sea Rescue Institute | https://www.linkedin.com/in/alison-young-n%C3%A9e-smith/ |
| #casey-prince | Casey Prince | Executive Director | Ubuntu Football | https://www.linkedin.com/in/casey-prince-214301139/ |
| #miche-nicholas | Miche Nicholas | Fundraising Manager | Ubuntu Football | https://www.linkedin.com/in/miche-nicholas-8a6722157/ |
| #reana-rossouw | Reana Rossouw | Owner | Next Generation Consultants | https://www.linkedin.com/in/reanarossouw/ |
| #damian-chapman | Damian Chapman | Founder | Fundraiser In The Room | https://www.linkedin.com/in/damianchapmanuk/ |
| #colleen-francis | Colleen Francis | Strategic Oversight: Impact and Learning | Shonaquip Social Enterprise | https://www.linkedin.com/in/colleen-francis-77259245/ |
| #leana-de-beer | Leana de Beer | Founder & CEO | WaFunda | https://www.linkedin.com/in/leanadebeer/ |
| #sophie-olivier | Sophie Olivier | Founder and Director | Flourish Fundraising | https://www.linkedin.com/in/sophie-olivier/ |
| #angela-blackwell | Angela Blackwell | Founder and Director | Paws on the Path | https://www.linkedin.com/in/angela-blackwell-marketing-executive/ |
| #toni-erasmus | Toni Erasmus | Marketing Manager | SA Guide-Dogs Association for the Blind | https://www.linkedin.com/in/toni-erasmus-087483121/ |
| #delphino-machikicho | Delphino Machikicho | Executive Director | Just Grace NPC | https://www.linkedin.com/in/delphino-machikicho-mcom-2338783a/ |
| #farida-lavangee | Farida Lavangee | Director: Audit & Reporting | Turning Point Chartered Accountants | https://www.linkedin.com/in/farida-lavangee-54678b36/ |
| #jenni-mcleod | Jenni McLeod | Director | Downes Murray International | https://www.linkedin.com/in/jenni-mcleod-65113826/ |
| #mide-akerewusi | Olumide "Mide" Akerewusi | Founder & CEO | AgentsC Inc. | https://www.linkedin.com/in/mide-olumide-akerewusi-b-sc-m-sc-econ-csr-p-cdep-1a003ba/ |
| #phano-liphoto | Phano Liphoto | Research And Policy Analyst | Young Urbanists South Africa | https://www.linkedin.com/in/phanoliphoto2024/ |
| #nick-rockey | Nick Rockey | Managing Director | Trialogue | https://www.linkedin.com/in/nick-rockey-8b03797/ |
| #roland-postma | Roland Postma | Managing Director | Young Urbanists South Africa | https://www.linkedin.com/in/rolandpostma/ |
| #ian-parsons | Ian Parsons | CEO | Matogen Digital & Weaver Network | https://www.linkedin.com/in/ian-parsons-matogen-digital/ |
| #malusi-ntoyapi | Malusi Ntoyapi | Programmes and Innovation Manager | HCI Foundation | https://www.linkedin.com/in/malusi-ntoyapi-62578917/ |
| #nondumiso-mabuya | Nondumiso Mabuya | Program Officer | Masana wa Afrika | https://www.linkedin.com/in/nondumiso-mabuya-986896121/ |
| #shona-young | Shona Young | Strategic Philanthropy | Investec Wealth & Investment | https://www.linkedin.com/in/shona-young-38b57730/ |
| #nomsa-muthaphuli | Nomsa Muthaphuli | ECD & Youth Fund Manager | Oppenheimer Memorial Trust | https://www.linkedin.com/in/nomsa-muthaphuli-1444b632/ |

### Speaker Bios:

**Chantel Cooper:** I am a strategist, connector, and problem solver who thrives on identifying opportunities, overcoming challenges, and building high-impact collaborative relationships. From a young age, I have been driven by a deep commitment to support society's most vulnerable: women and children. At 18, I began volunteering for an organisation that supported rape survivors and worked with female entrepreneurs in the Eastern Cape. My studies in political science and public administration only deepened this passion. At 27, I became director of Rape Crisis Cape Town Trust. This role laid the foundation of my leadership, which I have built on over the years. After becoming a mother, I shifted my focus and joined St. Joseph's Home for Chronically Ill Children as their resource development manager. In 2013, I joined the Children's Hospital Trust as head of fundraising and communications, a role I held until 2019, when I was appointed CEO. This position enables me to collaborate with my exceptional team to raise funds, ensuring that high-quality healthcare is accessible to all children in the Western Cape and beyond.

**Cheryl Manikam:** Driven by a passion for both professional excellence and meaningful change, Cheryl Manikam built a successful career spanning customer service, marketing, operations, and sales leadership in the Corporate Sector. After more than a decade of leadership experience and a proven track record in strategy, relationship management, and business development, Cheryl made a purposeful transition into the NGO sector in 2023. Seeking to align her career with a greater cause, she joined the Children's Hospital Trust, where she combines her skills and passion to help create lasting change for children and their families.

**Alison Young:** Alison Young leads performance marketing at the National Sea Rescue Institute (NSRI), where she is responsible for driving the organisation's direct fundraising revenue across multiple channels. In her two years at NSRI, she has played a central role in shaping the data-driven strategies that underpin the organisation's fundraising growth. Before joining NSRI, Alison spent a year with Experian as a Global Consultant, working across international markets on data and analytics solutions. She brings with her nine years of experience at Homechoice, developing deep expertise in customer acquisition, retention and direct marketing.

**Casey Prince:** Casey is from Raleigh, NC originally but has called Ocean View in Cape Town home since late 2009. Since starting Ubuntu Football Academy in 2011, Casey has earned an A License from the United States Soccer Federation and has attended the Mentorship, Expert, and Pro levels of Football Coach Evolution.

**Miche Nicholas:** Miche Nicholas discovered her true calling nine years ago when she transitioned from Corporate Communication into the NGO sector. Driven by an unshakeable passion for youth development and social change, as the Fundraising Manager at Ubuntu Football, Miche dedicates her work to creating meaningful opportunities and making a lasting difference in the lives of the next generation.

**Reana Rossouw:** Reana Rossouw is the owner of Next Generation Consultants and is regarded as one of Africa's leading experts in social innovation, sustainable development and impact management and measurement. She advises social investors across Africa on their investment and development strategies, assists social impact organisations with growth and investment readiness strategies and regularly publishes industry research reports. She presents biannual Masterclasses on topics such as Impact Management and Measurement and Pathways to Scale.

**Damian Chapman:** Damian Chapman helps organisations understand their HOW, so their WHY and WHAT can work together not fight each other. Author of Effective Fundraising Systems, he works with nonprofits around the world who want to know why their systems succeed or break down. Fundraiser In The Room works with clients across Europe, Africa, Asia, and the Americas. Damian also serves as the Chair of Rogare — the world's only fundraising think tank, and as a Non-Executive Director for the Chartered Institute of Fundraising.

**Colleen Francis:** Colleen Francis is part of the distributed leadership team at Shonaquip Social Enterprise, focusing on Impact and Learning. A speech therapist by training, with over 15 years of experience working in communities and living with disability, she works on documenting and verifying social change within the social and solidarity economy.

**Leana de Beer:** Leana de Beer is the Founder & CEO of WaFunda, a social impact enterprise focused on democratising access to education through innovative financing solutions and technology. Over the past decade, she has worked at the intersection of education, financial inclusion, and impact investing. Previously CEO of Feenix, Leana helped scale one of South Africa's leading student crowdfunding and bursary management platforms. She is a Harambean Associate (H'25), a finalist for the AMBA Entrepreneur of the Year Award (2025), and was recognised as one of the Mail & Guardian 200 Young South Africans in 2021.

**Sophie Olivier:** Sophie Olivier brings over 16 years of experience across Southern Africa's non-profit sector. For the past eight years, she has served as Founder and Director of Flourish Fundraising, a consultancy specialising in grants readiness, grant writing and donor prospecting. Sophie holds an honours degree in International Development Studies from the University of Sussex, Brighton.

**Angela Blackwell:** Angela Blackwell is a strategic marketing leader with more than 25 years of experience, including senior global leadership roles at Accenture. She is the Founder and Director of Paws on the Path, a social impact initiative that raised R500,000 for the South African Guide Dogs Association and sponsors four future guide dogs. As a guide dog owner and supporter, Angela shares the story, strategy and lessons behind building a successful fundraising campaign without agency support or dedicated budget.

**Toni Erasmus:** Toni is a communications and fundraising professional with 10 years of experience spanning media, marketing, stakeholder engagement, fundraising, and entrepreneurship. She is passionate about connecting organisations, communities and supporters in ways that drive meaningful and sustainable impact. Her work is rooted in strategic storytelling, relationship building and developing innovative fundraising initiatives that inspire action, foster generosity, and create lasting change.

**Delphino Machikicho:** Delphino is an experienced youth development strategist with expertise in commerce, strategic management, finance, and social enterprise management. He holds a Master of Commerce from the University of the Western Cape. As Executive Director of Just Grace, he leads a fast-growing social enterprise based in Langa, the oldest township in South Africa.

**Farida Lavangee:** Farida Lavangee is a highly accomplished Chartered Accountant and Registered Auditor with over 22 years of audit experience. She serves as the Director of Audit and Reporting at Turning Point Chartered Accountants, is a USAID Accredited Auditor and Registered SARS Tax Practitioner. Specializing in the NPO sector, she brings over 10 years of expertise in audit, compliance, risk assessment, financial reporting, and systems reviews for NPOs.

**Jenni McLeod:** Jenni has been with Downes Murray International since its inception and has several years' experience as an Account Director controlling fundraising programmes for national welfare organisations. She has spent time in Australia, the UK and the USA gaining valuable experience and has managed many successful fundraising programmes both internationally and in South Africa. Jenni is a regular presenter at the International Fundraising Group/Resource Alliance Conference in Amsterdam. Over her 30+ year career she has taken an active role in the South Africa Institute of Fundraising's activities.

**Olumide "Mide" Akerewusi:** Mide believes in the power and potential of philanthropy to transform the world. He is the Founder and CEO of agentsC Inc., an international advisory firm, and the Founder of Giving Black, a global network dedicated to advancing Black philanthropy and driving social change. Drawing on Afrocentric giving traditions, Mide challenges traditional forms of charity while promoting more personalized and engaged expressions of giving. He is a published author whose works include The Duality of Giving, From the Mind to the Heart, and Fundraising While Black.

**Phano Liphoto:** Phano Liphoto is a South African Urban Planner and Content Creator, currently completing a Master's in Civil Engineering (Transport Studies) at UCT. Through his work with Young Urbanists, he helps lead street experiments and public space activations across South Africa. As the founder of Coffee Rave ZA and Youth Travel Collective, he has built a growing movement that brings together coffee, music, wellness, and community to reimagine how people connect in urban spaces.

**Nick Rockey:** Nick is the Managing Director of Trialogue, with 20 years of consulting and research experience across many market and industry sectors. He plays a lead consulting role in the fields of sustainable business and CSI, working with a wide range of corporate clients on strategy development, stakeholder engagement and reporting.

**Roland Postma:** Roland Postma is an urban planner and Managing Director of Young Urbanists South Africa. His work focuses on urban mobility, road safety, public transport, micro-mobility, and street design. He leads partnerships between government, communities, civil society and the private sector and has helped facilitate more than R5 million in public-private infrastructure projects. His work has been recognised through the Mail & Guardian 200 Young South Africans.

**Ian Parsons:** With 17 years in digital marketing, Ian is a passionate agency leader committed to fostering transparency and driving meaningful change. He is the CEO of Matogen Digital, a values-led innovation agency helping non-profits scale, raise funds and tell impactful stories, and the Founder of Weaver Network, a platform for nonprofit leaders to flourish.

**Malusi Ntoyapi:** Malusi Ntoyapi is a Programmes and Innovation Manager at the HCI Foundation, where he supports a wide range of South African not-for-profit organisations. His work is grounded in Ubuntu — he believes that a strong, supported, and organised not-for-profit community with a shared vision can ensure that no one is left behind. In 2015, he was named one of Mail & Guardian's Top 200 Young South Africans in Education.

**Nondumiso Mabuya:** Nondumiso Mabuya has over 14 years of experience in the development sector, managing programmes and portfolios across Southern Africa. She currently serves as a Programme Officer at Masana wa Afrika, where she reviews proposals, monitors budgets, tracks project milestones, and ensures compliance with donor requirements. She holds a Postgraduate Diploma in African Philanthropy and Resource Mobilisation from the University of the Witwatersrand.

**Shona Young:** Bio to be added.

**Nomsa Muthaphuli:** Bio to be added.

---

## Sponsor Footer

Below all sections, display a **sponsors footer** with the heading "Thank You to Our Sponsors" and logos in a horizontal responsive row. Each logo links to the sponsor's website and opens in a new tab. Logo files are in `/images/sponsors/`.

| Sponsor | URL |
|---------|-----|
| The Resource Alliance | https://resource-alliance.org/ |
| CCA Recruitment & Consulting | https://www.charitycareersafrica.com/ |
| Fundraising Beyond Borders | https://fundraisingbeyondborders.com/ |
| Donorbox | https://donorbox.org/ |
| Downes Murray International | http://dmi.co.za/ |
| Turning Point Chartered Accountants | https://tpcsa.co.za/ |
| LIFEbrand | https://lifebrand.co.za/ |
| Matogen Digital | https://matogen.com/ |
| Weaver Network | https://weaver-network.org/ |

---

## Image File Structure

All images should be placed in the same directory as the HTML file or in subfolders:

```
index.html
/images/
  logo.png               ← IFC Pop-Up logo
  /headshots/
    chantel-cooper.jpg
    cheryl-manikam.jpg
    alison-young.jpg
    casey-prince.jpg
    miche-nicholas.jpg
    reana-rossouw.jpg
    damian-chapman.jpg
    colleen-francis.jpg
    leana-de-beer.jpg
    sophie-olivier.jpg
    angela-blackwell.jpg
    toni-erasmus.jpg
    delphino-machikicho.jpg
    farida-lavangee.jpg
    jenni-mcleod.jpg
    mide-akerewusi.jpg
    phano-liphoto.jpg
    nick-rockey.jpg
    roland-postma.jpg
    ian-parsons.jpg
    malusi-ntoyapi.jpg
    nondumiso-mabuya.jpg
    shona-young.jpg
    nomsa-muthaphuli.jpg
  /sponsors/
    resource-alliance.png
    cca.png
    fundraising-beyond-borders.png
    donorbox.png
    downes-murray.png
    turning-point.png
    lifebrand.png
    matogen.png
    weaver-network.png
```

---

## Design Notes

- Background: dark navy `#303249` throughout
- Text: white on dark backgrounds, use `#A0A3C0` for secondary/muted text
- Accent: orange `#F49404` for headings, active states, buttons, badges
- Cards/surfaces: slightly lighter than background `#3D3F5A`
- Borders: subtle, `1px solid rgba(255,255,255,0.08)`
- Border radius: 12px on cards
- Font: Graphik (fallback: Inter, then system-ui)
- Schedule rows alternate subtle background for readability
- Star Theatre column has a subtle orange left border
- Avalon Theatre column has a subtle white/muted left border
- On mobile, the two session columns stack: Star first (labelled clearly), then Avalon below it
- Speaker headshots: circular, 120px diameter on cards
- LinkedIn button: small icon button, opens in new tab
- All external links open in new tab
- Smooth scroll behaviour
- Sticky nav on scroll

---

## Key UX Notes for Mobile (Priority)

- Nav tabs must be large enough to tap easily (min 44px height)
- Session cards should be full width on mobile
- Speaker bios should be collapsible (tap to expand) on mobile to avoid overwhelming scroll
- Schedule time column should be narrow and bold, content fills remaining width
- Breaks and lunch rows should be visually distinct (lighter/different background)
- Plenary sessions should be visually distinct (full-width, slightly more prominent)
- No horizontal scroll on any screen size
