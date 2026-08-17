"""
All the words on the IFC Cape Town Pop-Up 2026 site.

This is the place to edit copy — speaker titles, bios, session descriptions,
times, sponsor links. After changing anything here, run:

    python3 build_site.py

...which rewrites index.html. Nothing else needs touching.
"""

EVENT = {
    "name": "IFC Cape Town Pop-Up 2026",
    "headline": "Welcome to the IFC Cape Town Pop-Up 2026",
    "date": "2 September 2026",
    "venue": "Homecoming Centre, District Six, Cape Town",
    "tickets_url": "https://qkt.io/IFCCPT2026",
    "logo": {"file": "logo.png", "w": 800, "h": 620},
    # Hero background photo, from the 2025 Pop-Up. One of the slugs in
    # build_images.py HEROES: "theatre-blue", "stage-amber", "audience".
    # Set to None for a plain navy hero.
    "hero": "audience",
}

STAR = "Star Theatre"
AVALON = "Avalon Theatre"

BIO_PENDING = "Bio coming soon."

# A "bio" may be a single string, or a list of strings for a multi-paragraph bio.

# ---------------------------------------------------------------------------
# Speakers — ordered alphabetically by first name, which is how attendees
# scan a grid of 24 faces looking for someone.
# ---------------------------------------------------------------------------

SPEAKERS = [
    {
        "slug": "alison-young",
        "name": "Alison Young",
        "title": "Head of Performance Marketing",
        "org": "National Sea Rescue Institute",
        "linkedin": "https://www.linkedin.com/in/alison-young-n%C3%A9e-smith/",
        "bio": "Alison Young leads performance marketing at the National Sea Rescue "
               "Institute (NSRI), where she is responsible for driving the organisation's "
               "direct fundraising revenue across multiple channels. In her two years at "
               "NSRI, she has played a central role in shaping the data-driven strategies "
               "that underpin the organisation's fundraising growth. Before joining NSRI, "
               "Alison spent a year with Experian as a Global Consultant, working across "
               "international markets on data and analytics solutions. She brings with her "
               "nine years of experience at Homechoice, developing deep expertise in "
               "customer acquisition, retention and direct marketing.",
    },
    {
        "slug": "angela-blackwell",
        "name": "Angela Blackwell",
        "title": "Founder and Director",
        "org": "Paws on the Path",
        "linkedin": "https://www.linkedin.com/in/angela-blackwell-marketing-executive/",
        "bio": "Angela Blackwell is a strategic marketing leader with more than 25 years "
               "of experience, including senior global leadership roles at Accenture. She "
               "is the Founder and Director of Paws on the Path, a social impact initiative "
               "that raised R500,000 for the South African Guide Dogs Association and "
               "sponsors four future guide dogs. As a guide dog owner and supporter, Angela "
               "shares the story, strategy and lessons behind building a successful "
               "fundraising campaign without agency support or dedicated budget.",
    },
    {
        "slug": "casey-prince",
        "name": "Casey Prince",
        "title": "Executive Director",
        "org": "Ubuntu Football",
        "linkedin": "https://www.linkedin.com/in/casey-prince-214301139/",
        "bio": "Casey is from Raleigh, NC originally but has called Ocean View in Cape Town "
               "home since late 2009. Since starting Ubuntu Football Academy in 2011, Casey "
               "has earned an A License from the United States Soccer Federation and has "
               "attended the Mentorship, Expert, and Pro levels of Football Coach Evolution.",
    },
    {
        "slug": "chantel-cooper",
        "name": "Chantel Cooper",
        "title": "CEO",
        "org": "The Children's Hospital Trust",
        "linkedin": "https://www.linkedin.com/in/chantelcooper/",
        "bio": "I am a strategist, connector, and problem solver who thrives on identifying "
               "opportunities, overcoming challenges, and building high-impact collaborative "
               "relationships. From a young age, I have been driven by a deep commitment to "
               "support society's most vulnerable: women and children. At 18, I began "
               "volunteering for an organisation that supported rape survivors and worked "
               "with female entrepreneurs in the Eastern Cape. My studies in political "
               "science and public administration only deepened this passion. At 27, I became "
               "director of Rape Crisis Cape Town Trust. This role laid the foundation of my "
               "leadership, which I have built on over the years. After becoming a mother, I "
               "shifted my focus and joined St. Joseph's Home for Chronically Ill Children as "
               "their resource development manager. In 2013, I joined the Children's Hospital "
               "Trust as head of fundraising and communications, a role I held until 2019, "
               "when I was appointed CEO. This position enables me to collaborate with my "
               "exceptional team to raise funds, ensuring that high-quality healthcare is "
               "accessible to all children in the Western Cape and beyond.",
    },
    {
        "slug": "cheryl-manikam",
        "name": "Cheryl Manikam",
        "title": "Head of Fundraising",
        "org": "The Children's Hospital Trust",
        "linkedin": "https://www.linkedin.com/in/cheryl-manikam-7868876a/",
        "bio": "Driven by a passion for both professional excellence and meaningful change, "
               "Cheryl Manikam built a successful career spanning customer service, marketing, "
               "operations, and sales leadership in the Corporate Sector. After more than a "
               "decade of leadership experience and a proven track record in strategy, "
               "relationship management, and business development, Cheryl made a purposeful "
               "transition into the NGO sector in 2023. Seeking to align her career with a "
               "greater cause, she joined the Children's Hospital Trust, where she combines "
               "her skills and passion to help create lasting change for children and their "
               "families.",
    },
    {
        "slug": "colleen-francis",
        "name": "Colleen Francis",
        "title": "Strategic Oversight: Impact and Learning",
        "org": "Shonaquip Social Enterprise",
        "linkedin": "https://www.linkedin.com/in/colleen-francis-77259245/",
        "bio": "Colleen Francis is part of the distributed leadership team at Shonaquip "
               "Social Enterprise, focusing on Impact and Learning. A speech therapist by "
               "training, with over 15 years of experience working in communities and living "
               "with disability, she works on documenting and verifying social change within "
               "the social and solidarity economy.",
    },
    {
        "slug": "damian-chapman",
        "name": "Damian Chapman",
        "title": "Founder",
        "org": "Fundraiser In The Room",
        "linkedin": "https://www.linkedin.com/in/damianchapmanuk/",
        "international": True,
        "bio": "Damian Chapman helps organisations understand their HOW, so their WHY and "
               "WHAT can work together not fight each other. Author of Effective Fundraising "
               "Systems, he works with nonprofits around the world who want to know why their "
               "systems succeed or break down. Fundraiser In The Room works with clients "
               "across Europe, Africa, Asia, and the Americas. Damian also serves as the "
               "Chair of Rogare — the world's only fundraising think tank, and as a "
               "Non-Executive Director for the Chartered Institute of Fundraising.",
    },
    {
        "slug": "delphino-machikicho",
        "name": "Delphino Machikicho",
        "title": "Executive Director",
        "org": "Just Grace NPC",
        "linkedin": "https://www.linkedin.com/in/delphino-machikicho-mcom-2338783a/",
        "bio": "Delphino is an experienced youth development strategist with expertise in "
               "commerce, strategic management, finance, and social enterprise management. He "
               "holds a Master of Commerce from the University of the Western Cape. As "
               "Executive Director of Just Grace, he leads a fast-growing social enterprise "
               "based in Langa, the oldest township in South Africa.",
    },
    {
        "slug": "farida-lavangee",
        "name": "Farida Lavangee",
        "title": "Director: Audit & Reporting",
        "org": "Turning Point Chartered Accountants",
        "linkedin": "https://www.linkedin.com/in/farida-lavangee-54678b36/",
        "bio": "Farida Lavangee is a highly accomplished Chartered Accountant and Registered "
               "Auditor with over 22 years of audit experience. She serves as the Director of "
               "Audit and Reporting at Turning Point Chartered Accountants, is a USAID "
               "Accredited Auditor and Registered SARS Tax Practitioner. Specializing in the "
               "NPO sector, she brings over 10 years of expertise in audit, compliance, risk "
               "assessment, financial reporting, and systems reviews for NPOs.",
    },
    {
        "slug": "ian-parsons",
        "name": "Ian Parsons",
        "title": "CEO",
        "org": "Matogen Digital & Weaver Network",
        "linkedin": "https://www.linkedin.com/in/ian-parsons-matogen-digital/",
        "bio": "With 17 years in digital marketing, Ian is a passionate agency leader "
               "committed to fostering transparency and driving meaningful change. He is the "
               "CEO of Matogen Digital, a values-led innovation agency helping non-profits "
               "scale, raise funds and tell impactful stories, and the Founder of Weaver "
               "Network, a platform for nonprofit leaders to flourish.",
    },
    {
        "slug": "jenni-mcleod",
        "name": "Jenni McLeod",
        "title": "Director",
        "org": "Downes Murray International",
        "linkedin": "https://www.linkedin.com/in/jenni-mcleod-65113826/",
        "bio": "Jenni has been with Downes Murray International since its inception and has "
               "several years' experience as an Account Director controlling fundraising "
               "programmes for national welfare organisations. She has spent time in "
               "Australia, the UK and the USA gaining valuable experience and has managed "
               "many successful fundraising programmes both internationally and in South "
               "Africa. Jenni is a regular presenter at the International Fundraising "
               "Group/Resource Alliance Conference in Amsterdam. Over her 30+ year career she "
               "has taken an active role in the South Africa Institute of Fundraising's "
               "activities.",
    },
    {
        "slug": "leana-de-beer",
        "name": "Leana de Beer",
        "title": "Founder & CEO",
        "org": "WaFunda",
        "linkedin": "https://www.linkedin.com/in/leanadebeer/",
        "bio": "Leana de Beer is the Founder & CEO of WaFunda, a social impact enterprise "
               "focused on democratising access to education through innovative financing "
               "solutions and technology. Over the past decade, she has worked at the "
               "intersection of education, financial inclusion, and impact investing. "
               "Previously CEO of Feenix, Leana helped scale one of South Africa's leading "
               "student crowdfunding and bursary management platforms. She is a Harambean "
               "Associate (H'25), a finalist for the AMBA Entrepreneur of the Year Award "
               "(2025), and was recognised as one of the Mail & Guardian 200 Young South "
               "Africans in 2021.",
    },
    {
        "slug": "malusi-ntoyapi",
        "name": "Malusi Ntoyapi",
        "title": "Programmes and Innovation Manager",
        "org": "HCI Foundation",
        "linkedin": "https://www.linkedin.com/in/malusi-ntoyapi-62578917/",
        "bio": "Malusi Ntoyapi is a Programmes and Innovation Manager at the HCI Foundation, "
               "where he supports a wide range of South African not-for-profit organisations. "
               "His work is grounded in Ubuntu — he believes that a strong, supported, and "
               "organised not-for-profit community with a shared vision can ensure that no "
               "one is left behind. In 2015, he was named one of Mail & Guardian's Top 200 "
               "Young South Africans in Education.",
    },
    {
        "slug": "miche-nicholas",
        "name": "Miche Nicholas",
        "title": "Fundraising Manager",
        "org": "Ubuntu Football",
        "linkedin": "https://www.linkedin.com/in/miche-nicholas-8a6722157/",
        "bio": "Miche Nicholas discovered her true calling nine years ago when she "
               "transitioned from Corporate Communication into the NGO sector. Driven by an "
               "unshakeable passion for youth development and social change, as the "
               "Fundraising Manager at Ubuntu Football, Miche dedicates her work to creating "
               "meaningful opportunities and making a lasting difference in the lives of the "
               "next generation.",
    },
    {
        "slug": "nick-rockey",
        "name": "Nick Rockey",
        "title": "Managing Director",
        "org": "Trialogue",
        "linkedin": "https://www.linkedin.com/in/nick-rockey-8b03797/",
        "bio": "Nick is the Managing Director of Trialogue, with 20 years of consulting and "
               "research experience across many market and industry sectors. He plays a lead "
               "consulting role in the fields of sustainable business and CSI, working with a "
               "wide range of corporate clients on strategy development, stakeholder "
               "engagement and reporting.",
    },
    {
        "slug": "nomsa-muthaphuli",
        "name": "Nomsa Muthaphuli",
        "title": "ECD & Youth Development Fund Manager",
        "org": "Oppenheimer Memorial Trust",
        "linkedin": "https://www.linkedin.com/in/nomsa-muthaphuli-1444b632/",
        "bio": [
            "Nomsa Muthaphuli is a passionate advocate for education and systemic change, "
            "currently leading the Early Childhood Development (ECD) and Youth Development "
            "portfolio at the Oppenheimer Memorial Trust. Through her work as a fund manager "
            "and her previous role as an executive at SmartStart, a large-scale early "
            "learning social enterprise, she has developed both deep sector expertise and "
            "broad insight into the programmes, partnerships, and systems that drive "
            "positive outcomes for young children.",

            "A Strategic Operations Specialist with over 20 years of experience, Nomsa "
            "brings a unique combination of systems thinking, innovation, and execution "
            "capability to the design and scaling of high-impact social programmes. Drawing "
            "on her engineering background, she combines analytical rigour with business "
            "process optimisation, strategic alignment, and operational excellence across a "
            "range of sectors.",

            "Over the past decade in the ECD sector, Nomsa has led diverse portfolios "
            "spanning funder development, impact management, large-scale implementation, "
            "financial management, systems and process design, and partnership and "
            "stakeholder engagement. Her work has consistently focused on building "
            "sustainable, scalable solutions that strengthen programme effectiveness and "
            "expand access to quality services.",

            "Despite the significant challenges facing the ECD sector, Nomsa remains "
            "inspired by the potential for meaningful systems change. She is committed to "
            "advancing universal access to quality early learning opportunities that "
            "strengthen children’s cognitive development, enhance their readiness to learn, "
            "and improve their long-term life outcomes.",
        ],
    },
    {
        "slug": "nondumiso-mabuya",
        "name": "Nondumiso Mabuya",
        "title": "Program Officer",
        "org": "Masana wa Afrika",
        "linkedin": "https://www.linkedin.com/in/nondumiso-mabuya-986896121/",
        "bio": "Nondumiso Mabuya has over 14 years of experience in the development sector, "
               "managing programmes and portfolios across Southern Africa. She currently "
               "serves as a Programme Officer at Masana wa Afrika, where she reviews "
               "proposals, monitors budgets, tracks project milestones, and ensures "
               "compliance with donor requirements. She holds a Postgraduate Diploma in "
               "African Philanthropy and Resource Mobilisation from the University of the "
               "Witwatersrand.",
    },
    {
        "slug": "mide-akerewusi",
        "name": "Olumide “Mide” Akerewusi",
        "title": "Founder & CEO",
        "org": "AgentsC Inc.",
        "linkedin": "https://www.linkedin.com/in/mide-olumide-akerewusi-b-sc-m-sc-econ-csr-p-cdep-1a003ba/",
        "international": True,
        "bio": "Mide believes in the power and potential of philanthropy to transform the "
               "world. He is the Founder and CEO of agentsC Inc., an international advisory "
               "firm, and the Founder of Giving Black, a global network dedicated to "
               "advancing Black philanthropy and driving social change. Drawing on Afrocentric "
               "giving traditions, Mide challenges traditional forms of charity while "
               "promoting more personalized and engaged expressions of giving. He is a "
               "published author whose works include The Duality of Giving, From the Mind to "
               "the Heart, and Fundraising While Black.",
    },
    {
        "slug": "phano-liphoto",
        "name": "Phano Liphoto",
        "title": "Research and Policy Analyst",
        "org": "Young Urbanists South Africa",
        "linkedin": "https://www.linkedin.com/in/phanoliphoto2024/",
        "bio": "Phano Liphoto is a South African Urban Planner and Content Creator, currently "
               "completing a Master's in Civil Engineering (Transport Studies) at UCT. Through "
               "his work with Young Urbanists, he helps lead street experiments and public "
               "space activations across South Africa. As the founder of Coffee Rave ZA and "
               "Youth Travel Collective, he has built a growing movement that brings together "
               "coffee, music, wellness, and community to reimagine how people connect in "
               "urban spaces.",
    },
    {
        "slug": "reana-rossouw",
        "name": "Reana Rossouw",
        "title": "Owner",
        "org": "Next Generation Consultants",
        "linkedin": "https://www.linkedin.com/in/reanarossouw/",
        "bio": "Reana Rossouw is the owner of Next Generation Consultants and is regarded as "
               "one of Africa's leading experts in social innovation, sustainable development "
               "and impact management and measurement. She advises social investors across "
               "Africa on their investment and development strategies, assists social impact "
               "organisations with growth and investment readiness strategies and regularly "
               "publishes industry research reports. She presents biannual Masterclasses on "
               "topics such as Impact Management and Measurement and Pathways to Scale.",
    },
    {
        "slug": "roland-postma",
        "name": "Roland Postma",
        "title": "Managing Director",
        "org": "Young Urbanists South Africa",
        "linkedin": "https://www.linkedin.com/in/rolandpostma/",
        "bio": "Roland Postma is an urban planner and Managing Director of Young Urbanists "
               "South Africa. His work focuses on urban mobility, road safety, public "
               "transport, micro-mobility, and street design. He leads partnerships between "
               "government, communities, civil society and the private sector and has helped "
               "facilitate more than R5 million in public-private infrastructure projects. "
               "His work has been recognised through the Mail & Guardian 200 Young South "
               "Africans.",
    },
    {
        "slug": "shona-young",
        "name": "Shona Young",
        "title": "Philanthropy Consultant",
        "org": "Investec",
        "linkedin": "https://www.linkedin.com/in/shona-young-38b57730/",
        "bio": "Shona is a philanthropy consultant at Investec with more than two decades of "
               "experience across sustainability, corporate social investment, strategic "
               "consulting and communications. She served as Head of Corporate Social "
               "Investment (CSI) at Liberty Group, advised leading organisations through "
               "senior consulting roles at Trialogue and Letsema Consulting and Advisory and "
               "more recently led group sustainability reporting at Investec. Earlier roles "
               "with the City of Cape Town in their Environmental Department, ICLEI – Local "
               "Governments for Sustainability, and UCT established her expertise in "
               "environmental management and international project delivery. Based in Cape "
               "Town, Shona combines strong stakeholder engagement and strategic insight "
               "with a longstanding commitment to social impact, including serving as "
               "Chairperson of the Children’s Memorial Institute.",
    },
    {
        "slug": "sophie-olivier",
        "name": "Sophie Olivier",
        "title": "Founder and Director",
        "org": "Flourish Fundraising",
        "linkedin": "https://www.linkedin.com/in/sophie-olivier/",
        "bio": "Sophie Olivier brings over 16 years of experience across Southern Africa's "
               "non-profit sector. For the past eight years, she has served as Founder and "
               "Director of Flourish Fundraising, a consultancy specialising in grants "
               "readiness, grant writing and donor prospecting. Sophie holds an honours "
               "degree in International Development Studies from the University of Sussex, "
               "Brighton.",
    },
    {
        "slug": "toni-erasmus",
        "name": "Toni Erasmus",
        "title": "Marketing Manager",
        "org": "SA Guide-Dogs Association for the Blind",
        "linkedin": "https://www.linkedin.com/in/toni-erasmus-087483121/",
        "bio": "Toni is a communications and fundraising professional with 10 years of "
               "experience spanning media, marketing, stakeholder engagement, fundraising, "
               "and entrepreneurship. She is passionate about connecting organisations, "
               "communities and supporters in ways that drive meaningful and sustainable "
               "impact. Her work is rooted in strategic storytelling, relationship building "
               "and developing innovative fundraising initiatives that inspire action, foster "
               "generosity, and create lasting change.",
    },
]

# ---------------------------------------------------------------------------
# Sessions. "speakers" entries are (speaker slug, note) — note appears in
# brackets after the name, e.g. "(Moderator)".
# ---------------------------------------------------------------------------

SESSIONS = [
    {
        "anchor": "opening-plenary",
        "label": "Opening Plenary",
        "plenary": True,
        "room": STAR,
        "time": "9:15 – 10:00",
        "title": "The Duality of Giving: The Rise and Reach of African Philanthropy "
                 "As A Global Phenomenon",
        "speakers": [("mide-akerewusi", "joining virtually")],
        "description": "This Keynote is a journey of discovery into the unprecedented rise "
            "and recognition of African philanthropy as a force for social and environmental "
            "transformation in our world today. What should we know and how can we identify "
            "opportunities to engage Africans on their terms as they practice traditional "
            "Western forms of philanthropy, while also demonstrating the uniqueness of a "
            "totally African interpretation of generosity? Hear Mide Akerewusi share stories, "
            "statistics, and surveys that point to a new African philanthropy converging into "
            "one of the world's most unique and prolific forms of giving.",
    },
    {
        "anchor": "session-1a",
        "label": "Session 1A",
        "room": STAR,
        "time": "10:10 – 10:55",
        "title": "The State of Fundraising in South Africa Panel: Trends, Compliance, "
                 "and What's Coming",
        "speakers": [("delphino-machikicho", "Moderator"), ("jenni-mcleod", None),
                     ("sophie-olivier", None), ("farida-lavangee", None),
                     ("nick-rockey", None)],
        "description": "This panel of experts will share their views on the current South "
            "African fundraising landscape, including sector updates, emerging trends, and "
            "what organisations might be missing out on. Come prepared to hear about "
            "everything from individual giving, grants and foundations, compliance, "
            "accounting, and corporate social investment.",
    },
    {
        "anchor": "session-1b",
        "label": "Session 1B",
        "room": AVALON,
        "time": "10:10 – 10:55",
        "title": "A Playbook for Implementing AI in a Nonprofit Organisation",
        "speakers": [("ian-parsons", None)],
        "description": "A practical approach to implementing AI, with knowledge shares from "
            "nonprofit leaders. What are the risks of doing nothing, and where does ethics "
            "fit into the picture? How to manage changing roles and expectations, and how to "
            "ensure sensitive data remain secure and AI responses are accurate and true.",
    },
    {
        "anchor": "session-2a",
        "label": "Session 2A",
        "room": STAR,
        "time": "11:20 – 12:05",
        "title": "The Power of a Supporter-Led Campaign: The Story of Paws on the Path",
        "speakers": [("angela-blackwell", None), ("toni-erasmus", None)],
        "description": "Angela and Toni share how Paws on the Path raised R500,000, "
            "generated significant awareness, and created a lasting legacy by sponsoring four "
            "future guide dogs for the SA Guide-Dogs Association for the Blind. Together, they "
            "share the story, partnerships, and lessons learned from the campaign, offering "
            "practical insights for organisations seeking to amplify supporter-led fundraising "
            "initiatives.",
    },
    {
        "anchor": "session-2b",
        "label": "Session 2B",
        "room": AVALON,
        "time": "11:20 – 12:05",
        "title": "Using Your Team's Strengths for Corporate Partnerships: "
                 "Director-Fundraiser Synergy",
        "speakers": [("miche-nicholas", None), ("casey-prince", None)],
        "description": "Join Miche and Casey to hear how aligning a Director's strategic "
            "vision with a Fundraiser's relationship-building creates a seamless, reliable "
            "experience for businesses. You'll learn how their tag-team approach turns cold "
            "corporate outreach into warm, high-trust alliances where partners always know "
            "exactly who they are working with, what they are investing in, and how together, "
            "you build long-term impact.",
    },
    {
        "anchor": "session-3a",
        "label": "Session 3A",
        "room": STAR,
        "time": "12:15 – 13:00",
        "title": "Funder Panel: What Donors Are Really Looking For",
        "speakers": [("malusi-ntoyapi", "Moderator"), ("shona-young", None),
                     ("nomsa-muthaphuli", None), ("nondumiso-mabuya", None)],
        "description": "We'll be sitting down with philanthropic foundation leaders to open a "
            "dialogue between fundraisers and the people they are seeking funding from. What "
            "do funders see when reviewing grant applications? What makes a nonprofit stand "
            "out? How do you build lasting relationships? How can nonprofits collaborate for "
            "more success? Attendees will hear both the hard truths and the positive insights "
            "regarding the sector's direction. Since applying for endless grants consumes "
            "significant time for NPOs, conversations like these help fundraisers focus their "
            "energy effectively.",
    },
    {
        "anchor": "session-3b",
        "label": "Session 3B",
        "room": AVALON,
        "time": "12:15 – 13:00",
        "title": "Profit For Purpose: The Need to Reframe Our Strategic Thinking",
        "speakers": [("damian-chapman", None)],
        "description": "Nonprofits around the world are leaking money from their fundraising "
            "operations without even realising it... and calling ourselves nonprofits is "
            "making it worse. In this session, we'll launch the findings from working with "
            "over 20 African purpose organisations who are changing how they see themselves, "
            "how they're changing the way they do things, and how you can see how much profit "
            "you're leaking in your organisation.",
    },
    {
        "anchor": "session-4a",
        "label": "Session 4A",
        "room": STAR,
        "time": "14:00 – 14:45",
        "title": "You Can't Build Tomorrow's Impact with Yesterday's Funding: "
                 "A Social Enterprise Story",
        "speakers": [("leana-de-beer", None)],
        "description": "As social challenges evolve, so too must the way we design solutions "
            "and finance them. This session shares WaFunda's evolution from an idea incubated "
            "within a nonprofit to an independent social enterprise, showing how programme "
            "innovation and capital innovation continuously shaped one another. Sustainable "
            "impact depends on both.",
    },
    {
        "anchor": "session-4b",
        "label": "Session 4B",
        "room": AVALON,
        "time": "14:00 – 14:45",
        "title": "Small Donations, Big Impact: Recurring Donors for Sustainable Income",
        "speakers": [("alison-young", None)],
        "description": "NGOs are continually under pressure to secure funding in order to "
            "sustain and expand their charitable work. Traditional fundraising efforts often "
            "focus on government grants, corporate partnerships, and other Corporate Social "
            "Investment (CSI) initiatives. However, every contribution makes a difference. "
            "This session will explore how developing a loyal base of recurring donors — "
            "regardless of the size of their individual contributions — can create a "
            "reliable and sustainable source of ongoing income over time.",
    },
    {
        "anchor": "session-5a",
        "label": "Session 5A",
        "room": STAR,
        "time": "14:55 – 15:40",
        "title": "Impact Management and Measurement: The Impact Validation "
                 "Fundraising Requires",
        "speakers": [("reana-rossouw", None), ("colleen-francis", None)],
        "description": "This session will focus on the value and importance of Impact "
            "Management and Measurement (IMM) to support fundraising efforts. Funders no "
            "longer focus on activities and outputs but want assurance and evidence that "
            "their investments will yield credible and sustainable impact. The session will "
            "include the case study of Shonaquip Social Enterprise and their application and "
            "integration of IMM practices.",
    },
    {
        "anchor": "session-5b",
        "label": "Session 5B",
        "room": AVALON,
        "time": "14:55 – 15:40",
        "title": "More Than Followers: Building a Community That Actually Takes Action",
        "speakers": [("roland-postma", None), ("phano-liphoto", None)],
        "description": "Roland and Phano share how Young Urbanists has used social media and "
            "personal storytelling to build a genuine community of supporters who don't just "
            "engage online but show up and make a difference for their cause, from mobilising "
            "people around local initiatives and events to collaborating with other "
            "organisations. The session will explore how putting a face to an organisation "
            "builds trust and connection, and what it takes to turn an online following into "
            "real-world participation.",
    },
    {
        "anchor": "closing-plenary",
        "label": "Closing Plenary",
        "plenary": True,
        "room": STAR,
        "time": "16:00 – 16:45",
        "title": "The CEO and the Fundraiser: Building a Culture Where Both Can Thrive",
        "speakers": [("chantel-cooper", None), ("cheryl-manikam", None)],
        "description": "As CEO and Head of Fundraising, Chantel Cooper and Cheryl Manikam "
            "will share an honest and practical look at what it takes to build a strong "
            "partnership between leadership and fundraising. Through lived examples, they will "
            "explore how trust, alignment, clear roles and a purpose-driven and high "
            "performing culture can create the conditions for both fundraising success and "
            "organisational impact to thrive.",
    },
]

# ---------------------------------------------------------------------------
# Schedule. Each slot is either:
#   "full"    a single item spanning the full width
#   "split"   two concurrent sessions (Star, then Avalon)
# An item with "session" pulls its title and speakers from SESSIONS above,
# so the schedule and the session cards can never disagree.
# ---------------------------------------------------------------------------

SCHEDULE = [
    {"time": "8:00 – 9:00", "kind": "full", "item": {
        "flavour": "logistics", "name": "Registration",
        "detail": "In the lobby. Collect your name tag at the info desk."}},
    {"time": "9:00 – 9:15", "kind": "full", "item": {
        "flavour": "remarks", "name": "Opening Remarks", "detail": ""}},
    {"time": "9:15 – 10:00", "kind": "full", "item": {
        "flavour": "plenary", "session": "opening-plenary"}},
    {"time": "10:10 – 10:55", "kind": "split", "star": {"session": "session-1a"},
     "avalon": {"session": "session-1b"}},
    {"time": "10:55 – 11:20", "kind": "full", "item": {
        "flavour": "break", "name": "Tea Break",
        "detail": "Free tea & coffee in the lobby. Coffee bar open for paid drinks."}},
    {"time": "11:20 – 12:05", "kind": "split", "star": {"session": "session-2a"},
     "avalon": {"session": "session-2b"}},
    {"time": "12:15 – 13:00", "kind": "split", "star": {"session": "session-3a"},
     "avalon": {"session": "session-3b"}},
    {"time": "13:00 – 14:00", "kind": "full", "item": {
        "flavour": "break", "name": "Lunch",
        "detail": "Tafel Space. Boxed lunches by Cooktastic, drinks by Homecoming Centre. "
                  "Bar open for additional purchases."}},
    {"time": "14:00 – 14:45", "kind": "split", "star": {"session": "session-4a"},
     "avalon": {"session": "session-4b"}},
    {"time": "14:55 – 15:40", "kind": "split", "star": {"session": "session-5a"},
     "avalon": {"session": "session-5b"}},
    {"time": "15:40 – 16:00", "kind": "full", "item": {
        "flavour": "break", "name": "Tea Break",
        "detail": "Free tea & coffee in the lobby. Coffee bar open for paid drinks."}},
    {"time": "16:00 – 16:45", "kind": "full", "item": {
        "flavour": "plenary", "session": "closing-plenary"}},
    {"time": "16:45 – 17:00", "kind": "full", "item": {
        "flavour": "remarks", "name": "Closing Remarks", "detail": ""}},
]

# ---------------------------------------------------------------------------
# Topic tags, used for the filter chips on the Sessions tab. The chips are
# generated from whatever appears here, so renaming a topic or re-tagging a
# session is all it takes — nothing else needs changing.
# ---------------------------------------------------------------------------

TOPICS = {
    "opening-plenary": ["Philanthropy"],
    "session-1a": ["Individual Giving", "Grants & Foundations",
                   "Compliance", "Corporate Social Investment"],
    "session-1b": ["Technology & AI"],
    "session-2a": ["Crowdfunding", "Peer-to-Peer", "Storytelling"],
    "session-2b": ["Corporate Social Investment"],
    "session-3a": ["Grants & Foundations", "Corporate Social Investment"],
    "session-3b": ["Leadership & Strategy"],
    "session-4a": ["Social Enterprise"],
    "session-4b": ["Recurring Donors", "Individual Giving"],
    "session-5a": ["Impact & Measurement"],
    "session-5b": ["Storytelling", "Social Media"],
    "closing-plenary": ["Leadership & Strategy"],
}

# Sessions run as a moderated panel rather than a talk.
PANELS = {"session-1a", "session-3a"}

# ---------------------------------------------------------------------------
# "On the day" practical info — the fourth tab.
#
# Each block has a heading plus either "items" (a bulleted list) or "body"
# (paragraphs). "html" is rendered as-is rather than escaped, so it can hold a
# link; keep it to plain anchors. "link" adds a button under the block.
# ---------------------------------------------------------------------------

INFO_INTRO = ("A few details to help you prepare for a day of learning, networking and "
              "sharing at the IFC Cape Town Pop-Up.")

VENUE_Q = "Homecoming+Centre+Caledon+Street+District+Six+Cape+Town"
PARKING_Q = "Harrington+Square+Parking+27+Caledon+Street+Cape+Town"

INFO_BLOCKS = [
    {
        "heading": "Start planning your day",
        "items": ["Registration opens at 8:00",
                  "The programme starts promptly at 9:00",
                  "IFC Pop-Up ends at 17:00"],
        "html": 'Have a look at the <a href="#panel-schedule">schedule</a> and '
                '<a href="#panel-sessions">sessions</a> to start planning which ones '
                'you would like to attend.',
    },
    {
        "heading": "How to get there",
        "body": ["The Homecoming Centre, corner of Buitenkant and Caledon Street "
                 "(entrance on Caledon Street), District Six, Cape Town 7785.",
                 "You can also take the train — Cape Town Station is about a 10-minute "
                 "walk away."],
        "links": [
            {"label": "Google Maps",
             "url": f"https://www.google.com/maps/search/?api=1&query={VENUE_Q}"},
            {"label": "Apple Maps", "url": f"https://maps.apple.com/?q={VENUE_Q}"},
            {"label": "Train schedule", "url": "https://cttrains.co.za/train-form.php"},
        ],
    },
    {
        "heading": "Parking",
        "body": ["Paid parking is available at Harrington Square Parking Lot, "
                 "27 Caledon Street.",
                 "There is paid street parking in the surrounding blocks. Canterbury "
                 "Street is free, but it fills up early."],
    },
    {
        "heading": "What to bring",
        "items": ["Something to take notes with as you learn",
                  "A way to share your contact details as you network — business cards, "
                  "the LinkedIn app, or whatever works for you"],
    },
    {
        "heading": "Get social",
        "html": 'Follow <a href="https://www.linkedin.com/company/ifc-cape-town/" '
                'target="_blank" rel="noopener">IFC Cape Town Pop-Up</a>, '
                '<a href="https://www.linkedin.com/company/the-resource-alliance/" '
                'target="_blank" rel="noopener">The Resource Alliance</a> and '
                '<a href="https://www.linkedin.com/company/charity-careers-africa/" '
                'target="_blank" rel="noopener">CCA Recruitment and Consulting</a> to stay '
                'up to date with all the news and coverage. Tag us in your posts and use '
                'the hashtag below.',
        "hashtag": "#IFCCPT2026",
    },
    {
        "heading": "Questions?",
        "body": ["Get in touch and we will help."],
        # Assembled by JS so the address is not sitting in the page source for
        # scrapers; <noscript> shows it for anyone without JavaScript.
        "email": True,
    },
]

INFO_OUTRO = "We are looking forward to seeing you on Wednesday, 2 September."

# ---------------------------------------------------------------------------
# Usage tracking. Paste the deployed Apps Script web-app URL here to switch it
# on; leave as None and no tracking code is emitted into index.html at all.
# See analytics/SETUP.md.
#
# What it records: which sessions and speaker profiles get opened, which tabs
# and filters get used, ticket clicks. No cookies, no localStorage, no IP
# logging, no demographics — so the site still needs no consent banner.
# ---------------------------------------------------------------------------
ANALYTICS_URL = None


# Split so the plain address never appears as a single string in the HTML.
CONTACT_EMAIL_USER = "shawnlifebiz"
CONTACT_EMAIL_HOST = "gmail.com"

# Event photography credit (the hero and 2025 photos).
PHOTO_CREDIT = {"name": "LIFEbrand", "url": "https://lifebrand.co.za/"}


# ---------------------------------------------------------------------------
# Sponsors — displayed in this order, on white tiles (several logos are
# dark-on-transparent and would vanish on the navy background).
# ---------------------------------------------------------------------------

SPONSORS = [
    {"name": "The Resource Alliance", "url": "https://resource-alliance.org/",
     "file": "resource-alliance.webp", "w": 600, "h": 282},
    {"name": "CCA Recruitment & Consulting", "url": "https://www.charitycareersafrica.com/",
     "file": "cca.webp", "w": 600, "h": 137},
    {"name": "Fundraising Beyond Borders", "url": "https://fundraisingbeyondborders.com/",
     "file": "fundraising-beyond-borders.webp", "w": 200, "h": 50},
    {"name": "Donorbox", "url": "https://donorbox.org/",
     "file": "donorbox.png", "w": 485, "h": 104},
    {"name": "Downes Murray International", "url": "http://dmi.co.za/",
     "file": "downes-murray.webp", "w": 600, "h": 133},
    {"name": "Turning Point Chartered Accountants", "url": "https://tpcsa.co.za/",
     "file": "turning-point.webp", "w": 586, "h": 148},
    {"name": "LIFEbrand", "url": "https://lifebrand.co.za/",
     "file": "lifebrand.webp", "w": 600, "h": 126},
    {"name": "Matogen Digital", "url": "https://matogen.com/",
     "file": "matogen.png", "w": 600, "h": 118},
    {"name": "Weaver Network", "url": "https://weaver-network.org/",
     "file": "weaver-network.png", "w": 600, "h": 155},
    # "tall": stacked or square lockups, not wide wordmarks. They get a higher
    # max-height so they do not read as half the size of everything else.
    {"name": "Homecoming Centre", "url": "https://www.homecomingcentre.co.za/",
     "file": "homecoming-centre.png", "w": 600, "h": 424, "tall": True},
    {"name": "Cooktastic", "url": "https://cooktastic.co.za/",
     "file": "cooktastic.svg", "w": 500, "h": 500, "tall": True},
]
