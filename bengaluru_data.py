# Bengaluru Public Places and Infrastructure Database (Hospitals, Metro, Bus Stops, Airport, Schools, Tech Parks)

BENGALURU_INFRA_DATA = {
    "whitefield": {
        "hospitals": [
            {"name": "Manipal Hospital Whitefield", "distance": "1.2 km", "rating": "4.8", "contact": "+91 80 4966 6666", "type": "Multi-Speciality & Emergency", "address": "ITPL Main Rd, EPIP Zone, Whitefield"},
            {"name": "Columbia Asia Hospital (Aster Whitefield)", "distance": "2.4 km", "rating": "4.7", "contact": "+91 80 6165 6666", "type": "Super Speciality", "address": "Varthur Rd, Ramagondanahalli"},
            {"name": "Vydehi Institute of Medical Sciences", "distance": "3.1 km", "rating": "4.5", "contact": "+91 80 2841 3381", "type": "Medical College & Trauma Center", "address": "EPIP Zone, Whitefield"},
            {"name": "Sathya Sai Super Speciality Hospital", "distance": "2.0 km", "rating": "4.9", "contact": "+91 80 2841 1500", "type": "Cardiac & Neuro Super Speciality", "address": "EPIP Zone, Whitefield"}
        ],
        "metro": [
            {"station": "Whitefield (Kadugodi) Metro Station", "line": "Purple Line", "distance": "0.8 km", "gate": "Gate 1 & Gate 2", "status": "Operational"},
            {"station": "Hope Farm Channasandra Metro Station", "line": "Purple Line", "distance": "1.5 km", "gate": "Gate A & B", "status": "Operational"},
            {"station": "Pattandur Agrahara (ITPL) Metro Station", "line": "Purple Line", "distance": "1.9 km", "gate": "Direct Skywalk to ITPL", "status": "Operational"}
        ],
        "bus_stops": [
            {"name": "Whitefield TTMC Bus Terminal", "distance": "0.5 km", "routes": "335E, 500D, V-500A, 333P", "location": "Whitefield Main Rd"},
            {"name": "Hope Farm Junction Bus Stop", "distance": "1.2 km", "routes": "333P, 500E, V-335E, 335F", "location": "SH-35 Junction"},
            {"name": "ITPL Main Gate Bus Stop", "distance": "1.8 km", "routes": "KIAS-6, 500D, 335E", "location": "ITPL Main Rd"}
        ],
        "airport": {
            "distance": "38 km",
            "travel_time": "55-65 mins (via SH-104 / Devanahalli Highway)",
            "kias_bus": "Vaju Veer (KIAS-6) direct airport shuttle every 30 mins"
        },
        "schools": [
            {"name": "The International School Bangalore (TISB)", "distance": "4.5 km", "board": "IB / IGCSE"},
            {"name": "Deens Academy Whitefield", "distance": "2.0 km", "board": "CBSE"},
            {"name": "Delhi Public School Whitefield", "distance": "3.5 km", "board": "CBSE"}
        ],
        "tech_parks": [
            {"name": "International Tech Park Bangalore (ITPL)", "distance": "1.8 km", "companies": "TCS, Oracle, SAP, Applied Materials, Mercedes-Benz"},
            {"name": "EPIP Zone & Sigma Soft Tech Park", "distance": "2.5 km", "companies": "Capgemini, Dell, ABB, General Electric"},
            {"name": "Prestige Shantiniketan Tech Park", "distance": "2.1 km", "companies": "ExxonMobil, Synchrony, Alstom"}
        ]
    },
    "kengeri": {
        "hospitals": [
            {"name": "BGS Gleneagles Global Hospital", "distance": "1.8 km", "rating": "4.8", "contact": "+91 80 2625 5555", "type": "Multi-Organ Transplant & Super Speciality", "address": "Uttarahalli Main Rd, Kengeri"},
            {"name": "Rajarajeswari Medical College & Hospital", "distance": "3.2 km", "rating": "4.6", "contact": "+91 80 2843 7444", "type": "Trauma & Teaching Hospital", "address": "Mysore Rd, Kengeri"},
            {"name": "HK Hospital Kengeri", "distance": "0.9 km", "rating": "4.3", "contact": "+91 80 2848 4400", "type": "General Hospital", "address": "Kengeri Satellite Town"}
        ],
        "metro": [
            {"station": "Kengeri Bus Terminal Metro Station", "line": "Purple Line Terminal", "distance": "0.4 km", "gate": "Gate 1 & Gate 2", "status": "Operational"},
            {"station": "Challaghatta Metro Station", "line": "Purple Line Extension", "distance": "1.6 km", "gate": "Gate A (Mysore Rd)", "status": "Operational"},
            {"station": "Kengeri TTMC Station", "line": "Purple Line", "distance": "0.5 km", "gate": "Skywalk Connection", "status": "Operational"}
        ],
        "bus_stops": [
            {"name": "Kengeri TTMC Bus Station", "distance": "0.3 km", "routes": "222A, 226N, 227B, 401B, V-226", "location": "Mysore Rd Junction"},
            {"name": "Kengeri Satellite Town Bus Stop", "distance": "0.8 km", "routes": "222B, 223A, 401M", "location": "Kengeri 1st Stage"},
            {"name": "Rajarajeswari Medical College Gate Stop", "distance": "3.0 km", "routes": "226, 227, 228", "location": "Mysore National Highway"}
        ],
        "airport": {
            "distance": "48 km",
            "travel_time": "65-75 mins (via NICE Expressway & Airport Toll Highway)",
            "kias_bus": "KIAS-10 Direct Airport Express from Kengeri TTMC"
        },
        "schools": [
            {"name": "Gurukula International School", "distance": "1.5 km", "board": "ICSE"},
            {"name": "National Public School Kengeri", "distance": "2.2 km", "board": "CBSE"}
        ],
        "tech_parks": [
            {"name": "Kumbalgodu Industrial Area & Tech Zone", "distance": "4.5 km", "companies": "Bosch, Toyota Kirloskar, Mitsubishi"},
            {"name": "Global Village Tech Park (Rajarajeshwari Nagar)", "distance": "5.2 km", "companies": "Mindtree, Accenture, NTT Data"}
        ]
    },
    "electronic city": {
        "hospitals": [
            {"name": "Narayana Institute of Cardiac Sciences", "distance": "3.5 km", "rating": "4.9", "contact": "+91 80 7122 2222", "type": "Cardiac & Multi-Speciality", "address": "Bommasandra Industrial Area"},
            {"name": "Springleaf Hospital Electronic City", "distance": "1.1 km", "rating": "4.4", "contact": "+91 80 4115 2200", "type": "Multi-Speciality", "address": "Phase 1, Hosur Rd"},
            {"name": "Kauvery Hospital Electronic City", "distance": "2.0 km", "rating": "4.7", "contact": "+91 80 6825 5000", "type": "Super Speciality", "address": "Phase 1, Electronic City"}
        ],
        "metro": [
            {"station": "Electronic City Metro Station", "line": "Yellow Line", "distance": "0.6 km", "gate": "Gate A (Wipro Gate)", "status": "Operational / Testing"},
            {"station": "Infosys Foundation Konappana Agrahara", "line": "Yellow Line", "distance": "1.2 km", "gate": "Infosys Skywalk Gate", "status": "Operational / Testing"}
        ],
        "bus_stops": [
            {"name": "Electronic City Wipro Gate Bus Stop", "distance": "0.4 km", "routes": "356C, 600F, V-356C", "location": "Phase 1 Wipro Circle"},
            {"name": "Konappana Agrahara Bus Station", "distance": "0.9 km", "routes": "360B, 356N, 356E", "location": "Hosur Highway"}
        ],
        "airport": {
            "distance": "52 km",
            "travel_time": "70-85 mins (via E-City Flyover & Airport Expressway)",
            "kias_bus": "KIAS-8 Express Shuttle every 45 mins"
        },
        "schools": [
            {"name": "DPS Electronic City", "distance": "3.0 km", "board": "CBSE"},
            {"name": "Sbrr Mahajana Public School", "distance": "2.2 km", "board": "ICSE"}
        ],
        "tech_parks": [
            {"name": "Infosys & Wipro Campus (Phase 1)", "distance": "0.5 km", "companies": "Infosys, Wipro, HCL, Siemens, Hewlett Packard"},
            {"name": "Velankani Tech Park (Phase 2)", "distance": "1.8 km", "companies": "TCS, Tech Mahindra, Continental"}
        ]
    },
    "indira nagar": {
        "hospitals": [
            {"name": "Chinmaya Mission Hospital (CMH)", "distance": "0.6 km", "rating": "4.7", "contact": "+91 80 2528 0461", "type": "Multi-Speciality", "address": "CMH Rd, Indiranagar"},
            {"name": "Manipal Hospital Old Airport Road", "distance": "2.1 km", "rating": "4.8", "contact": "+91 80 2502 4444", "type": "Super Speciality & Tertiary Care", "address": "98 HAL Old Airport Rd"}
        ],
        "metro": [
            {"station": "Indiranagar Metro Station", "line": "Purple Line", "distance": "0.3 km", "gate": "Gate A (100ft Rd) & Gate B (CMH Rd)", "status": "Operational"},
            {"station": "Swami Vivekananda Road Metro Station", "line": "Purple Line", "distance": "1.1 km", "gate": "Gate 1 (Old Madras Rd)", "status": "Operational"}
        ],
        "bus_stops": [
            {"name": "Indiranagar 100ft Road Bus Stop", "distance": "0.2 km", "routes": "138, 201, 314, V-201", "location": "100ft Rd Junction"},
            {"name": "CMH Hospital Bus Terminal", "distance": "0.5 km", "routes": "138, 314E, 314F", "location": "CMH Road"}
        ],
        "airport": {
            "distance": "37 km",
            "travel_time": "50-60 mins (via Inner Ring Road & Bellary Road)",
            "kias_bus": "KIAS-4 Direct Airport Express from CMH Road"
        },
        "schools": [
            {"name": "National Public School (NPS Indiranagar)", "distance": "1.2 km", "board": "CBSE"},
            {"name": "Frank Anthony Public School", "distance": "2.5 km", "board": "ICSE"}
        ],
        "tech_parks": [
            {"name": "Embassy GolfLinks Business Park (EGL)", "distance": "2.8 km", "companies": "IBM, Goldman Sachs, Microsoft, Target"},
            {"name": "Bagmane Tech Park", "distance": "3.2 km", "companies": "Cognizant, Motorola, Texas Instruments, Oracle"}
        ]
    },
    "koramangala": {
        "hospitals": [
            {"name": "St. John's Medical College Hospital", "distance": "1.0 km", "rating": "4.8", "contact": "+91 80 2206 5000", "type": "Multi-Speciality Medical Research", "address": "Sarjapur Rd, John Nagar, Koramangala"},
            {"name": "Apollo Spectra Hospital Koramangala", "distance": "0.8 km", "rating": "4.6", "contact": "+91 80 4333 4444", "type": "Speciality Surgery Center", "address": "5th Block, Koramangala"}
        ],
        "metro": [
            {"station": "Rashtriya Vidyalaya Road Metro Station", "line": "Green Line", "distance": "2.8 km", "gate": "Gate 1 & Gate 2", "status": "Operational"},
            {"station": "Tavarekere Metro Station", "line": "Yellow Line", "distance": "1.5 km", "gate": "Gate A (BTM Link Rd)", "status": "Operational / Testing"}
        ],
        "bus_stops": [
            {"name": "Koramangala TTMC Bus Terminal", "distance": "0.4 km", "routes": "171, 201, 356C, V-500A", "location": "80ft Rd, 6th Block"},
            {"name": "Forum Mall / Checkpost Bus Stop", "distance": "0.7 km", "routes": "171A, 365, 356E", "location": "Hosur Rd Junction"}
        ],
        "airport": {
            "distance": "40 km",
            "travel_time": "60-75 mins (via Agara & Airport Expressway)",
            "kias_bus": "KIAS-7 Direct Airport Bus from Koramangala TTMC"
        },
        "schools": [
            {"name": "Bethany High School", "distance": "0.9 km", "board": "ICSE"},
            {"name": "National Public School (NPS Koramangala)", "distance": "1.4 km", "board": "CBSE"}
        ],
        "tech_parks": [
            {"name": "Koramangala Startup Hub & Sony World Zone", "distance": "0.3 km", "companies": "Flipkart HQ, Swiggy HQ, Razorpay, PhonePe"},
            {"name": "Prestige Blue Chip & Forum Business Park", "distance": "0.8 km", "companies": "InMobi, Siemens, Cisco, Titan"}
        ]
    }
}

DEFAULT_LOCATION_INFRA = {
    "hospitals": [
        {"name": "Apollo Hospital Bengaluru Branch", "distance": "2.5 km", "rating": "4.8", "contact": "+91 80 2630 4050", "type": "Multi-Speciality Hospital", "address": "BG Road / City Center"},
        {"name": "Fortis Hospital Super Speciality", "distance": "3.0 km", "rating": "4.7", "contact": "+91 80 6621 4444", "type": "Super Speciality & Emergency", "address": "Bannerghatta Rd / Main Corridor"},
        {"name": "Manipal Hospital Central", "distance": "3.8 km", "rating": "4.8", "contact": "+91 80 2502 4444", "type": "Multi-Speciality Medical Center", "address": "Bengaluru Metropolitan Region"}
    ],
    "metro": [
        {"station": "Nearest Namma Metro Station", "line": "Purple / Green Line", "distance": "1.8 km", "gate": "Main Entrance Gate A & B", "status": "Operational"},
        {"station": "Bengaluru Central Interchange Station", "line": "Purple / Green Interchange", "distance": "3.5 km", "gate": "Interchange Skywalk Gate", "status": "Operational"}
    ],
    "bus_stops": [
        {"name": "Local BMTC Junction Bus Stop", "distance": "0.4 km", "routes": "BMTC Route 201, 335E, 500D, V-500", "location": "Main Road Junction"},
        {"name": "BMTC Feeder & Express Bus Stop", "distance": "0.9 km", "routes": "BMTC Metro Feeder MF-1, MF-2, 356C", "location": "Cross Road Junction"}
    ],
    "airport": {
        "distance": "36-45 km",
        "travel_time": "55-70 mins (via Airport Expressway / Bellary Highway)",
        "kias_bus": "Vaju Veer (KIAS) Airport Shuttle stop within 1.5 km radius"
    },
    "schools": [
        {"name": "National Public School (NPS Branch)", "distance": "1.5 km", "board": "CBSE"},
        {"name": "St. Joseph's Boys / Sacred Heart School", "distance": "2.8 km", "board": "ICSE / State Board"}
    ],
    "tech_parks": [
        {"name": "Manyata Tech Park / Tech Corridor", "distance": "5.0 km", "companies": "IBM, Cognizant, Target, Concentrix"}
    ]
}

def get_location_infra(location_name):
    key = location_name.lower().strip()
    if key in BENGALURU_INFRA_DATA:
        return BENGALURU_INFRA_DATA[key]
    
    for loc_key in BENGALURU_INFRA_DATA:
        if loc_key in key or key in loc_key:
            return BENGALURU_INFRA_DATA[loc_key]
            
    return DEFAULT_LOCATION_INFRA
