"""
Demo data for AI Job Mentor for Informal Workers.
Includes worker profiles, job listings, training programmes, and government schemes.
"""

from typing import Any

# ---------------------------------------------------------------------------
# Demo worker profiles
# ---------------------------------------------------------------------------

DEMO_WORKERS = [
    {
        "id": "W001",
        "name": "Ramesh Kumar",
        "age": 32,
        "gender": "Male",
        "location": "Chennai, Tamil Nadu",
        "education": "Class 10 (SSC)",
        "current_occupation": "Construction Labour",
        "monthly_income": 8000,
        "languages": ["Tamil", "Basic Hindi"],
        "skills": ["Manual Labour", "Basic Masonry", "Loading/Unloading"],
        "experience_years": 8,
        "has_smartphone": True,
        "has_bank_account": True,
        "family_size": 4,
        "ration_card": "BPL",
    },
    {
        "id": "W002",
        "name": "Meena Devi",
        "age": 27,
        "gender": "Female",
        "location": "Patna, Bihar",
        "education": "Class 8",
        "current_occupation": "Domestic Worker",
        "monthly_income": 5500,
        "languages": ["Hindi", "Bhojpuri"],
        "skills": ["Cooking", "Childcare", "Cleaning", "Stitching"],
        "experience_years": 5,
        "has_smartphone": False,
        "has_bank_account": True,
        "family_size": 5,
        "ration_card": "AAY",
    },
    {
        "id": "W003",
        "name": "Suresh Babu",
        "age": 40,
        "gender": "Male",
        "location": "Mumbai, Maharashtra",
        "education": "Class 12 (HSC)",
        "current_occupation": "Street Vendor",
        "monthly_income": 12000,
        "languages": ["Hindi", "Marathi", "Basic English"],
        "skills": ["Sales", "Inventory Management", "Customer Service", "Basic Accounting"],
        "experience_years": 15,
        "has_smartphone": True,
        "has_bank_account": True,
        "family_size": 3,
        "ration_card": "PHH",
    },
    {
        "id": "W004",
        "name": "Lakshmi S",
        "age": 35,
        "gender": "Female",
        "location": "Coimbatore, Tamil Nadu",
        "education": "ITI Certificate",
        "current_occupation": "Garment Worker",
        "monthly_income": 9500,
        "languages": ["Tamil", "Basic English"],
        "skills": ["Tailoring", "Machine Operation", "Quality Control", "Pattern Making"],
        "experience_years": 10,
        "has_smartphone": True,
        "has_bank_account": True,
        "family_size": 4,
        "ration_card": "PHH",
    },
    {
        "id": "W005",
        "name": "Arjun Singh",
        "age": 24,
        "gender": "Male",
        "location": "Delhi",
        "education": "Class 12",
        "current_occupation": "Delivery Boy",
        "monthly_income": 14000,
        "languages": ["Hindi", "Punjabi", "Basic English"],
        "skills": ["Driving (2-wheeler)", "Navigation", "Customer Service", "Smartphone Use"],
        "experience_years": 2,
        "has_smartphone": True,
        "has_bank_account": True,
        "family_size": 5,
        "ration_card": "PHH",
    },
]

# ---------------------------------------------------------------------------
# Job listings
# ---------------------------------------------------------------------------

JOB_LISTINGS = [
    {
        "id": "J001",
        "title": "Construction Supervisor",
        "category": "Construction",
        "employer": "Larsen & Toubro (Sub-contractor)",
        "location": "Chennai",
        "salary_min": 15000,
        "salary_max": 22000,
        "required_skills": ["Team Management", "Safety Compliance", "Basic Masonry", "Supervision"],
        "required_education": "Class 8+",
        "experience_required": 5,
        "description": "Supervise a team of 10–15 construction workers on residential projects.",
        "job_type": "Full-time",
        "sector": "Formal",
    },
    {
        "id": "J002",
        "title": "Delivery Executive",
        "category": "Logistics",
        "employer": "Zomato / Swiggy Partner",
        "location": "Pan India",
        "salary_min": 12000,
        "salary_max": 20000,
        "required_skills": ["Driving (2-wheeler)", "Smartphone Use", "Navigation", "Customer Service"],
        "required_education": "Class 10+",
        "experience_required": 0,
        "description": "Deliver food orders within city limits. Flexible shifts available.",
        "job_type": "Gig/Part-time",
        "sector": "Informal",
    },
    {
        "id": "J003",
        "title": "Domestic Helper (Senior)",
        "category": "Domestic Services",
        "employer": "Urban Company",
        "location": "Major Cities",
        "salary_min": 10000,
        "salary_max": 16000,
        "required_skills": ["Cooking", "Cleaning", "Childcare", "Basic Communication"],
        "required_education": "No minimum",
        "experience_required": 2,
        "description": "Provide comprehensive household support to urban families via platform.",
        "job_type": "Part-time/Full-time",
        "sector": "Platform Economy",
    },
    {
        "id": "J004",
        "title": "Retail Store Associate",
        "category": "Retail",
        "employer": "Reliance Retail",
        "location": "Pan India",
        "salary_min": 11000,
        "salary_max": 16000,
        "required_skills": ["Customer Service", "Sales", "Inventory", "Basic Computer"],
        "required_education": "Class 12+",
        "experience_required": 1,
        "description": "Assist customers, manage shelves, and operate billing counters.",
        "job_type": "Full-time",
        "sector": "Formal",
    },
    {
        "id": "J005",
        "title": "Garment Tailor / Stitcher",
        "category": "Manufacturing",
        "employer": "Tirupur Export Factory",
        "location": "Coimbatore / Tirupur",
        "salary_min": 12000,
        "salary_max": 18000,
        "required_skills": ["Tailoring", "Machine Operation", "Quality Control"],
        "required_education": "ITI or Class 10",
        "experience_required": 2,
        "description": "Operate industrial sewing machines for garment export orders.",
        "job_type": "Full-time",
        "sector": "Formal",
    },
    {
        "id": "J006",
        "title": "Security Guard",
        "category": "Security",
        "employer": "G4S / SIS Security",
        "location": "Pan India",
        "salary_min": 10000,
        "salary_max": 14000,
        "required_skills": ["Physical Fitness", "Discipline", "Basic Communication"],
        "required_education": "Class 8+",
        "experience_required": 0,
        "description": "Guard commercial buildings, malls, and residential complexes.",
        "job_type": "Full-time",
        "sector": "Formal",
    },
    {
        "id": "J007",
        "title": "Home Cook / Tiffin Service Owner",
        "category": "Food & Hospitality",
        "employer": "Self-employed / NoBroker",
        "location": "Urban Areas",
        "salary_min": 8000,
        "salary_max": 25000,
        "required_skills": ["Cooking", "Basic Accounting", "Customer Service", "Smartphone Use"],
        "required_education": "No minimum",
        "experience_required": 3,
        "description": "Start a home-based tiffin service or cook for a small number of households.",
        "job_type": "Self-employed",
        "sector": "Informal",
    },
    {
        "id": "J008",
        "title": "Electrician Helper",
        "category": "Skilled Trade",
        "employer": "Local Contractors",
        "location": "Pan India",
        "salary_min": 11000,
        "salary_max": 17000,
        "required_skills": ["Basic Electrical Knowledge", "Safety Awareness", "Physical Fitness"],
        "required_education": "Class 8+",
        "experience_required": 1,
        "description": "Assist licensed electricians in residential and commercial wiring projects.",
        "job_type": "Contract",
        "sector": "Informal",
    },
]

# ---------------------------------------------------------------------------
# Training programmes
# ---------------------------------------------------------------------------

TRAINING_PROGRAMMES = [
    {
        "id": "T001",
        "name": "PMKVY – Pradhan Mantri Kaushal Vikas Yojana",
        "provider": "NSDC / Government of India",
        "skills_covered": ["Construction", "Automotive", "Retail", "IT", "Healthcare", "Hospitality"],
        "duration": "3–6 months",
        "cost": "Free",
        "certification": "Government-certified NSQF",
        "mode": "Offline / Centre-based",
        "eligibility": "18–45 years, Class 5 pass minimum",
        "link": "https://www.pmkvyofficial.org",
        "languages": ["Hindi", "English", "Regional Languages"],
    },
    {
        "id": "T002",
        "name": "Digital Saksharta Abhiyan (DISHA)",
        "provider": "Government of India / CSC",
        "skills_covered": ["Smartphone Use", "Internet Basics", "Digital Payments", "Online Services"],
        "duration": "20 hours",
        "cost": "Free",
        "certification": "DISHA Certificate",
        "mode": "Online / Offline",
        "eligibility": "Any age, rural/semi-urban households",
        "link": "https://www.pmgdisha.in",
        "languages": ["Hindi", "English", "22 regional languages"],
    },
    {
        "id": "T003",
        "name": "Skill India – Construction Worker Upskilling",
        "provider": "NSDC",
        "skills_covered": ["Safety", "Masonry", "Supervision", "Building Codes"],
        "duration": "45 days",
        "cost": "Free",
        "certification": "Recognition of Prior Learning (RPL)",
        "mode": "Offline",
        "eligibility": "Active construction worker, 18+",
        "link": "https://www.skillindia.gov.in",
        "languages": ["Hindi", "Tamil", "Telugu", "Kannada"],
    },
    {
        "id": "T004",
        "name": "Food Processing & Entrepreneurship",
        "provider": "NIFTEM / State Government",
        "skills_covered": ["Food Safety", "Packaging", "Business Planning", "FSSAI Compliance"],
        "duration": "2 months",
        "cost": "Subsidised (₹500–1000)",
        "certification": "State Board Certificate",
        "mode": "Offline",
        "eligibility": "18+, women preferred",
        "link": "https://mofpi.gov.in",
        "languages": ["Hindi", "English", "Regional"],
    },
    {
        "id": "T005",
        "name": "Garment Technology & Fashion Design (Basic)",
        "provider": "NIFT / State Textile Boards",
        "skills_covered": ["Pattern Making", "Industrial Stitching", "Export Quality Standards"],
        "duration": "3 months",
        "cost": "Free / Subsidised",
        "certification": "NIFT / State Certificate",
        "mode": "Offline",
        "eligibility": "Class 8+, basic stitching knowledge",
        "link": "https://nift.ac.in",
        "languages": ["Tamil", "Hindi", "English"],
    },
    {
        "id": "T006",
        "name": "Two-Wheeler Driving & Logistics Management",
        "provider": "Maruti Driving School / NSDC",
        "skills_covered": ["Traffic Rules", "Vehicle Maintenance", "GPS Use", "Customer Service"],
        "duration": "15 days",
        "cost": "₹1500–2000",
        "certification": "Driving Licence + NSDC Certificate",
        "mode": "Offline",
        "eligibility": "18+, physically fit",
        "link": "https://www.marutisuzukidrivingschool.com",
        "languages": ["Hindi", "English", "Regional"],
    },
    {
        "id": "T007",
        "name": "Tally & Basic Accounting for Small Business",
        "provider": "Tally Education Pvt. Ltd. / CSC",
        "skills_covered": ["Bookkeeping", "GST Basics", "Inventory", "Tally Software"],
        "duration": "2 months",
        "cost": "₹2000–3000",
        "certification": "Tally Certificate",
        "mode": "Online / Offline",
        "eligibility": "Class 10+",
        "link": "https://tallysolutions.com",
        "languages": ["Hindi", "English"],
    },
    {
        "id": "T008",
        "name": "ITI – Industrial Training Institute Courses",
        "provider": "DGET / State ITIs",
        "skills_covered": ["Electrician", "Plumbing", "Welding", "Mechanic", "Turner"],
        "duration": "1–2 years",
        "cost": "Very low / Free for BPL",
        "certification": "NCVT Certificate",
        "mode": "Offline",
        "eligibility": "Class 8–10 pass, 14–40 years",
        "link": "https://dget.nic.in",
        "languages": ["Hindi", "English", "Regional"],
    },
]

# ---------------------------------------------------------------------------
# Government schemes
# ---------------------------------------------------------------------------

GOVERNMENT_SCHEMES = [
    {
        "id": "S001",
        "name": "PM-SYM – Pradhan Mantri Shram Yogi Maan-dhan",
        "category": "Pension",
        "benefit": "₹3000/month pension after age 60",
        "eligibility": "18–40 years, monthly income < ₹15,000, unorganised worker",
        "contribution": "₹55–₹200/month (age-based)",
        "enroll_at": "CSC / Jan Seva Kendra",
        "documents": ["Aadhaar", "Savings Bank Account", "Mobile Number"],
        "link": "https://maandhan.in",
    },
    {
        "id": "S002",
        "name": "ESIC – Employees' State Insurance Scheme",
        "category": "Health Insurance",
        "benefit": "Cashless medical treatment + maternity + disability benefits",
        "eligibility": "Monthly wage < ₹21,000; applicable via registered employer",
        "contribution": "0.75% of wages (employee) + 3.25% (employer)",
        "enroll_at": "Employer registration / ESIC portal",
        "documents": ["Aadhaar", "Employment Proof"],
        "link": "https://www.esic.in",
    },
    {
        "id": "S003",
        "name": "PMJDY – Pradhan Mantri Jan Dhan Yojana",
        "category": "Banking",
        "benefit": "Zero-balance bank account + RuPay Debit Card + ₹2 lakh accident cover",
        "eligibility": "Any Indian above 10 years without a bank account",
        "contribution": "Zero",
        "enroll_at": "Any bank branch / BC Agent",
        "documents": ["Aadhaar", "Any address proof"],
        "link": "https://pmjdy.gov.in",
    },
    {
        "id": "S004",
        "name": "PMJJBY – PM Jeevan Jyoti Bima Yojana",
        "category": "Life Insurance",
        "benefit": "₹2 lakh life cover on death",
        "eligibility": "18–50 years, savings bank account holder",
        "contribution": "₹436/year",
        "enroll_at": "Bank / Insurance company",
        "documents": ["Aadhaar", "Bank Account"],
        "link": "https://financialservices.gov.in",
    },
    {
        "id": "S005",
        "name": "PMSBY – PM Suraksha Bima Yojana",
        "category": "Accident Insurance",
        "benefit": "₹2 lakh on accidental death, ₹1 lakh on partial disability",
        "eligibility": "18–70 years, savings bank account",
        "contribution": "₹20/year",
        "enroll_at": "Bank",
        "documents": ["Bank Account", "Aadhaar"],
        "link": "https://financialservices.gov.in",
    },
    {
        "id": "S006",
        "name": "BOCW – Building & Other Construction Workers Welfare Board",
        "category": "Welfare (Construction)",
        "benefit": "₹2 lakh accident benefit, housing subsidy, scholarship, pension",
        "eligibility": "Construction worker, employed 90+ days in past year",
        "contribution": "₹25–₹50 registration fee",
        "enroll_at": "State Labour Department / BOCW Board",
        "documents": ["Aadhaar", "Employment Certificate", "Photo"],
        "link": "https://bocw.labour.gov.in",
    },
    {
        "id": "S007",
        "name": "Sukanya Samriddhi Yojana",
        "category": "Girl Child Savings",
        "benefit": "8.2% interest, tax benefits, lump sum on maturity",
        "eligibility": "Girl child below 10 years, guardian must have bank account",
        "contribution": "Min ₹250/year",
        "enroll_at": "Post Office / Bank",
        "documents": ["Birth Certificate of girl", "Aadhaar", "Guardian ID"],
        "link": "https://www.india.gov.in",
    },
    {
        "id": "S008",
        "name": "e-Shram Card",
        "category": "Registration / Identity",
        "benefit": "Unique worker ID, priority for scheme benefits, ₹2 lakh accident insurance",
        "eligibility": "Any unorganised/informal worker 16–59 years",
        "contribution": "Free",
        "enroll_at": "eshram.gov.in / CSC",
        "documents": ["Aadhaar", "Mobile linked to Aadhaar"],
        "link": "https://eshram.gov.in",
    },
]

# ---------------------------------------------------------------------------
# Skill taxonomy for gap analysis
# ---------------------------------------------------------------------------

SKILL_TAXONOMY = {
    "Digital": ["Smartphone Use", "Internet Basics", "Digital Payments", "MS Office", "Email", "Social Media"],
    "Communication": ["Spoken Hindi", "Spoken English", "Spoken Tamil", "Written Communication", "Customer Service"],
    "Financial": ["Basic Accounting", "Savings Planning", "Budgeting", "GST Basics", "Loan Management"],
    "Technical": ["Masonry", "Plumbing", "Electrical Work", "Welding", "Machine Operation", "Driving"],
    "Soft Skills": ["Team Management", "Time Management", "Problem Solving", "Leadership", "Discipline"],
    "Business": ["Sales", "Inventory Management", "Entrepreneurship", "Marketing Basics"],
    "Domain Specific": ["Tailoring", "Cooking", "Childcare", "Security", "Construction Supervision"],
}

JOB_SKILL_REQUIREMENTS = {
    "Construction Supervisor": {
        "Technical": ["Masonry", "Safety Compliance"],
        "Soft Skills": ["Team Management", "Leadership"],
        "Communication": ["Spoken Hindi"],
    },
    "Delivery Executive": {
        "Digital": ["Smartphone Use", "Digital Payments"],
        "Communication": ["Customer Service"],
        "Technical": ["Driving"],
    },
    "Retail Store Associate": {
        "Digital": ["MS Office"],
        "Communication": ["Customer Service", "Spoken English"],
        "Business": ["Sales", "Inventory Management"],
    },
    "Garment Tailor": {
        "Technical": ["Machine Operation"],
        "Domain Specific": ["Tailoring"],
        "Soft Skills": ["Time Management"],
    },
    "Home Cook / Tiffin Service": {
        "Domain Specific": ["Cooking"],
        "Business": ["Entrepreneurship", "Marketing Basics"],
        "Digital": ["Smartphone Use"],
        "Financial": ["Basic Accounting"],
    },
}


def get_demo_worker(worker_id: str = "W001") -> dict[str, Any]:
    for w in DEMO_WORKERS:
        if w["id"] == worker_id:
            return w
    return DEMO_WORKERS[0]


def get_all_demo_workers() -> list[dict[str, Any]]:
    return DEMO_WORKERS


def get_all_jobs() -> list[dict[str, Any]]:
    return JOB_LISTINGS


def get_all_training() -> list[dict[str, Any]]:
    return TRAINING_PROGRAMMES


def get_all_schemes() -> list[dict[str, Any]]:
    return GOVERNMENT_SCHEMES
