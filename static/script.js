// Comprehensive list of diseases for filtering
const diseaseList = [
    "Fever", "Cough", "Cold", "Headache", "Stomach Pain", "Diarrhea", "Vomiting", "Nausea",
    "Chest Pain", "Back Pain", "Joint Pain", "Muscle Pain", "Eye Problems", "Ear Problems",
    "Throat Pain", "Sore Throat", "Difficulty Breathing", "Shortness of Breath", "Wheezing",
    "High Blood Pressure", "Low Blood Pressure", "Diabetes", "Heart Disease", "Asthma",
    "Bronchitis", "Pneumonia", "Tuberculosis", "Malaria", "Dengue", "Chikungunya",
    "Typhoid", "Jaundice", "Hepatitis", "Kidney Stones", "Urinary Tract Infection",
    "Skin Rash", "Allergy", "Food Poisoning", "Migraine", "Dizziness", "Fatigue",
    "Weakness", "Anemia", "Thyroid Problems", "Arthritis", "Osteoporosis", "Cancer",
    "Tumor", "Fracture", "Sprain", "Bruise", "Cut", "Burn", "Infection", "Sepsis",
    "Anxiety", "Depression", "Stress", "Insomnia", "Sleep Disorders", "Memory Loss",
    "Seizures", "Epilepsy", "Stroke", "Paralysis", "Numbness", "Tingling",
    "Vision Problems", "Blurred Vision", "Hearing Loss", "Tinnitus", "Dental Problems",
    "Tooth Pain", "Gum Disease", "Oral Ulcers", "Swelling", "Inflammation",
    "Autoimmune Disease", "Lupus", "Rheumatoid Arthritis", "Multiple Sclerosis",
    "Parkinson's Disease", "Alzheimer's Disease", "Dementia", "Mental Health Issues",
    "Eating Disorders", "Obesity", "Weight Loss", "Weight Gain", "Malnutrition",
    "Vitamin Deficiency", "Iron Deficiency", "Calcium Deficiency", "Dehydration",
    "Heat Stroke", "Hypothermia", "Frostbite", "Sunburn", "Skin Cancer",
    "Melanoma", "Basal Cell Carcinoma", "Squamous Cell Carcinoma", "Leukemia",
    "Lymphoma", "Breast Cancer", "Lung Cancer", "Liver Cancer", "Stomach Cancer",
    "Colon Cancer", "Prostate Cancer", "Cervical Cancer", "Ovarian Cancer",
    "Testicular Cancer", "Bladder Cancer", "Pancreatic Cancer", "Brain Tumor",
    "Spinal Cord Injury", "Head Injury", "Concussion", "Whiplash", "Neck Pain",
    "Shoulder Pain", "Elbow Pain", "Wrist Pain", "Hand Pain", "Finger Pain",
    "Hip Pain", "Knee Pain", "Ankle Pain", "Foot Pain", "Heel Pain", "Toe Pain",
    "Spinal Stenosis", "Herniated Disc", "Sciatica", "Fibromyalgia", "Chronic Fatigue",
    "Irritable Bowel Syndrome", "Crohn's Disease", "Ulcerative Colitis", "Gastritis",
    "Peptic Ulcer", "GERD", "Acid Reflux", "Gallstones", "Appendicitis", "Hernia",
    "Hemorrhoids", "Constipation", "Bloating", "Gas", "Indigestion", "Heartburn",
    "Nausea", "Motion Sickness", "Vertigo", "Balance Problems", "Coordination Issues",
    "Speech Problems", "Swallowing Difficulties", "Voice Problems", "Hoarseness",
    "Laryngitis", "Pharyngitis", "Tonsillitis", "Sinusitis", "Rhinitis", "Hay Fever",
    "Seasonal Allergies", "Drug Allergy", "Contact Dermatitis", "Eczema", "Psoriasis",
    "Acne", "Rosacea", "Vitiligo", "Alopecia", "Hair Loss", "Dandruff", "Lice",
    "Scabies", "Ringworm", "Fungal Infection", "Bacterial Infection", "Viral Infection",
    "Sexually Transmitted Disease", "HIV", "AIDS", "Syphilis", "Gonorrhea", "Chlamydia",
    "Herpes", "HPV", "Hepatitis A", "Hepatitis B", "Hepatitis C", "Hepatitis D",
    "Hepatitis E", "Meningitis", "Encephalitis", "Polio", "Measles", "Mumps",
    "Rubella", "Chickenpox", "Shingles", "Mononucleosis", "Cytomegalovirus",
    "Toxoplasmosis", "Malaria", "Dengue Fever", "Yellow Fever", "Zika Virus",
    "Ebola", "COVID-19", "SARS", "MERS", "Influenza", "Swine Flu", "Bird Flu",
    "Pneumonia", "Bronchitis", "Emphysema", "COPD", "Cystic Fibrosis", "Pulmonary Edema",
    "Pulmonary Embolism", "Pneumothorax", "Pleural Effusion", "Sarcoidosis",
    "Interstitial Lung Disease", "Sleep Apnea", "Snoring", "Restless Leg Syndrome",
    "Periodic Limb Movement Disorder", "Narcolepsy", "Cataplexy", "Sleep Paralysis",
    "Night Terrors", "Nightmares", "Sleepwalking", "Teeth Grinding", "Bruxism",
    "TMJ Disorder", "Temporomandibular Joint Disorder", "Bell's Palsy", "Trigeminal Neuralgia",
    "Carpal Tunnel Syndrome", "Cubital Tunnel Syndrome", "Tarsal Tunnel Syndrome",
    "Plantar Fasciitis", "Achilles Tendinitis", "Rotator Cuff Tear", "Meniscus Tear",
    "ACL Tear", "PCL Tear", "MCL Tear", "LCL Tear", "Torn Ligament", "Torn Tendon",
    "Dislocated Joint", "Subluxation", "Bursitis", "Tendinitis", "Tendinosis",
    "Gout", "Pseudogout", "Osteoarthritis", "Rheumatoid Arthritis", "Psoriatic Arthritis",
    "Ankylosing Spondylitis", "Reactive Arthritis", "Juvenile Arthritis", "Lupus",
    "Scleroderma", "Sjogren's Syndrome", "Mixed Connective Tissue Disease",
    "Polymyositis", "Dermatomyositis", "Vasculitis", "Giant Cell Arteritis",
    "Takayasu's Arteritis", "Behçet's Disease", "Kawasaki Disease", "Henoch-Schönlein Purpura",
    "Wegener's Granulomatosis", "Churg-Strauss Syndrome", "Microscopic Polyangiitis",
    "Goodpasture's Syndrome", "Antiphospholipid Syndrome", "Raynaud's Phenomenon",
    "Ehlers-Danlos Syndrome", "Marfan Syndrome", "Osteogenesis Imperfecta",
    "Achondroplasia", "Dwarfism", "Gigantism", "Acromegaly", "Cushing's Syndrome",
    "Addison's Disease", "Pheochromocytoma", "Hyperthyroidism", "Hypothyroidism",
    "Goiter", "Thyroid Nodules", "Thyroid Cancer", "Graves' Disease", "Hashimoto's Thyroiditis",
    "Diabetes Type 1", "Diabetes Type 2", "Gestational Diabetes", "Prediabetes",
    "Diabetic Ketoacidosis", "Diabetic Neuropathy", "Diabetic Retinopathy", "Diabetic Nephropathy",
    "Hypoglycemia", "Hyperglycemia", "Insulin Resistance", "Metabolic Syndrome",
    "Obesity", "Morbid Obesity", "Anorexia", "Bulimia", "Binge Eating Disorder",
    "Pica", "Rumination Syndrome", "Avoidant/Restrictive Food Intake Disorder",
    "Prader-Willi Syndrome", "Turner Syndrome", "Klinefelter Syndrome", "Down Syndrome",
    "Fragile X Syndrome", "Williams Syndrome", "Angelman Syndrome", "Cri du Chat Syndrome",
    "Patau Syndrome", "Edwards Syndrome", "Trisomy 18", "Trisomy 13", "Trisomy 21",
    "Cystic Fibrosis", "Sickle Cell Disease", "Thalassemia", "Hemophilia", "Von Willebrand Disease",
    "Leukemia", "Lymphoma", "Hodgkin's Disease", "Non-Hodgkin's Lymphoma", "Multiple Myeloma",
    "Myelodysplastic Syndrome", "Aplastic Anemia", "Hemolytic Anemia", "Iron Deficiency Anemia",
    "Vitamin B12 Deficiency", "Folate Deficiency", "Pernicious Anemia", "Sickle Cell Anemia",
    "Thalassemia Major", "Thalassemia Minor", "G6PD Deficiency", "Pyruvate Kinase Deficiency",
    "Hereditary Spherocytosis", "Hereditary Elliptocytosis", "Paroxysmal Nocturnal Hemoglobinuria",
    "Thrombocytopenia", "Thrombocytosis", "Essential Thrombocythemia", "Polycythemia Vera",
    "Myelofibrosis", "Chronic Myeloid Leukemia", "Acute Myeloid Leukemia", "Chronic Lymphocytic Leukemia",
    "Acute Lymphoblastic Leukemia", "Hairy Cell Leukemia", "T-Cell Leukemia", "B-Cell Leukemia",
    "Burkitt's Lymphoma", "Mantle Cell Lymphoma", "Follicular Lymphoma", "Diffuse Large B-Cell Lymphoma",
    "T-Cell Lymphoma", "Cutaneous T-Cell Lymphoma", "Anaplastic Large Cell Lymphoma",
    "Peripheral T-Cell Lymphoma", "Angioimmunoblastic T-Cell Lymphoma", "Enteropathy-Associated T-Cell Lymphoma",
    "Hepatosplenic T-Cell Lymphoma", "Subcutaneous Panniculitis-like T-Cell Lymphoma",
    "Primary Cutaneous Anaplastic Large Cell Lymphoma", "Lymphomatoid Papulosis",
    "Primary Cutaneous CD4+ Small/Medium T-Cell Lymphoproliferative Disorder",
    "Primary Cutaneous CD8+ Aggressive Epidermotropic Cytotoxic T-Cell Lymphoma",
    "Primary Cutaneous Gamma-Delta T-Cell Lymphoma", "Primary Cutaneous CD30+ T-Cell Lymphoproliferative Disorders",
    "Primary Cutaneous CD4+ Small/Medium T-Cell Lymphoproliferative Disorder",
    "Primary Cutaneous CD8+ Aggressive Epidermotropic Cytotoxic T-Cell Lymphoma",
    "Primary Cutaneous Gamma-Delta T-Cell Lymphoma", "Primary Cutaneous CD30+ T-Cell Lymphoproliferative Disorders"
];

const stateDistricts = {
    "Andhra Pradesh": { code: "AP", district: {"Anantapur":"01", "Chittoor":"02", "East Godavari":"03", "Guntur":"04", "Krishna":"05", "Kurnool":"06", "Nellore":"07", "Prakasam":"08", "Srikakulam":"09", "Visakhapatnam":"10", "Vizianagaram":"11", "West Godavari":"12"} },
    "Arunachal Pradesh": { code: "AR", district: {"Tawang":"01", "West Kameng":"02", "East Kameng":"03", "Papum Pare":"04", "Kurung Kumey":"05", "Kra Daadi":"06", "Lower Subansiri":"07", "Upper Subansiri":"08", "West Siang":"09", "East Siang":"10", "Siang":"11", "Upper Siang":"12", "Lower Siang":"13", "Lower Dibang Valley":"14", "Dibang Valley":"15", "Anjaw":"16", "Lohit":"17", "Namsai":"18", "Changlang":"19", "Tirap":"20", "Longding":"21"} },
    "Assam": { code: "AS", district: {"Baksa":"01", "Barpeta":"02", "Biswanath":"03", "Bongaigaon":"04", "Cachar":"05", "Charaideo":"06", "Chirang":"07", "Darrang":"08", "Dhemaji":"09", "Dhubri":"10", "Dibrugarh":"11", "Goalpara":"12", "Golaghat":"13", "Hailakandi":"14", "Hojai":"15", "Jorhat":"16", "Kamrup":"17", "Kamrup Metropolitan":"18", "Karbi Anglong":"19", "Karimganj":"20", "Kokrajhar":"21", "Lakhimpur":"22", "Majuli":"23", "Morigaon":"24", "Nagaon":"25", "Nalbari":"26", "Dima Hasao":"27", "Sivasagar":"28", "Sonitpur":"29", "South Salmara-Mankachar":"30", "Tinsukia":"31", "Udalguri":"32", "West Karbi Anglong":"33"} },
    "Bihar": { code: "BR", district: {"Araria":"01", "Arwal":"02", "Aurangabad":"03", "Banka":"04", "Begusarai":"05", "Bhagalpur":"06", "Bhojpur":"07", "Buxar":"08", "Darbhanga":"09", "East Champaran":"10", "Gaya":"11", "Gopalganj":"12", "Jamui":"13", "Jehanabad":"14", "Kaimur":"15", "Katihar":"16", "Khagaria":"17", "Kishanganj":"18", "Lakhisarai":"19", "Madhepura":"20", "Madhubani":"21", "Munger":"22", "Muzaffarpur":"23", "Nalanda":"24", "Nawada":"25", "Patna":"26", "Purnia":"27", "Rohtas":"28", "Saharsa":"29", "Samastipur":"30", "Saran":"31", "Sheikhpura":"32", "Sheohar":"33", "Sitamarhi":"34", "Siwan":"35", "Supaul":"36", "Vaishali":"37", "West Champaran":"38"} },
    "Chhattisgarh": { code: "CG", district: {"Balod":"01", "Baloda Bazar":"02", "Balrampur":"03", "Bastar":"04", "Bemetara":"05", "Bijapur":"06", "Bilaspur":"07", "Dantewada":"08", "Dhamtari":"09", "Durg":"10", "Gariaband":"11", "Gaurela-Pendra-Marwahi":"12", "Janjgir-Champa":"13", "Jashpur":"14", "Kabirdham":"15", "Kanker":"16", "Kondagaon":"17", "Korba":"18", "Koriya":"19", "Mahasamund":"20", "Mungeli":"21", "Narayanpur":"22", "Raigarh":"23", "Raipur":"24", "Rajnandgaon":"25", "Sukma":"26", "Surajpur":"27", "Surguja":"28"} },
    "Goa": { code: "GA", district: {"North Goa":"01", "South Goa":"02"} },
    "Gujarat": { code: "GJ", district: {"Ahmedabad":"01", "Amreli":"02", "Anand":"03", "Aravalli":"04", "Banaskantha":"05", "Bharuch":"06", "Bhavnagar":"07", "Botad":"08", "Chhota Udaipur":"09", "Dahod":"10", "Dang":"11", "Devbhoomi Dwarka":"12", "Gandhinagar":"13", "Gir Somnath":"14", "Jamnagar":"15", "Junagadh":"16", "Kheda":"17", "Kutch":"18", "Mahisagar":"19", "Mehsana":"20", "Morbi":"21", "Narmada":"22", "Navsari":"23", "Panchmahal":"24", "Patan":"25", "Porbandar":"26", "Rajkot":"27", "Sabarkantha":"28", "Surat":"29", "Surendranagar":"30", "Tapi":"31", "Vadodara":"32", "Valsad":"33"} },
    "Haryana": { code: "HR", district: {"Ambala":"01", "Bhiwani":"02", "Charkhi Dadri":"03", "Faridabad":"04", "Fatehabad":"05", "Gurugram":"06", "Hisar":"07", "Jhajjar":"08", "Jind":"09", "Kaithal":"10", "Karnal":"11", "Kurukshetra":"12", "Mahendragarh":"13", "Nuh":"14", "Palwal":"15", "Panchkula":"16", "Panipat":"17", "Rewari":"18", "Rohtak":"19", "Sirsa":"20", "Sonipat":"21", "Yamunanagar":"22"} },
    "Himachal Pradesh": { code: "HP", district: {"Bilaspur":"01", "Chamba":"02", "Hamirpur":"03", "Kangra":"04", "Kinnaur":"05", "Kullu":"06", "Lahaul and Spiti":"07", "Mandi":"08", "Shimla":"09", "Sirmaur":"10", "Solan":"11", "Una":"12"} },
    "Jharkhand": { code: "JH", district: {"Bokaro":"01", "Chatra":"02", "Deoghar":"03", "Dhanbad":"04", "Dumka":"05", "East Singhbhum":"06", "Garhwa":"07", "Giridih":"08", "Godda":"09", "Gumla":"10", "Hazaribagh":"11", "Jamtara":"12", "Khunti":"13", "Koderma":"14", "Latehar":"15", "Lohardaga":"16", "Pakur":"17", "Palamu":"18", "Ramgarh":"19", "Ranchi":"20", "Sahebganj":"21", "Seraikela Kharsawan":"22", "Simdega":"23", "West Singhbhum":"24"} },
    "Karnataka": { code: "KA", district: {"Bagalkot":"01", "Ballari":"02", "Belagavi":"03", "Bengaluru Rural":"04", "Bengaluru Urban":"05", "Bidar":"06", "Chamarajanagar":"07", "Chikballapur":"08", "Chikkamagaluru":"09", "Chitradurga":"10", "Dakshina Kannada":"11", "Davanagere":"12", "Dharwad":"13", "Gadag":"14", "Hassan":"15", "Haveri":"16", "Kalaburagi":"17", "Kodagu":"18", "Kolar":"19", "Koppal":"20", "Mandya":"21", "Mysuru":"22", "Raichur":"23", "Ramanagara":"24", "Shivamogga":"25", "Tumakuru":"26", "Udupi":"27", "Uttara Kannada":"28", "Vijayapura":"29", "Yadgir":"30"} },
    "Kerala": { code: "KL", district: {"Alappuzha":"01", "Ernakulam":"02", "Idukki":"03", "Kannur":"04", "Kasaragod":"05", "Kollam":"06", "Kottayam":"07", "Kozhikode":"08", "Malappuram":"09", "Palakkad":"10", "Pathanamthitta":"11", "Thiruvananthapuram":"12", "Thrissur":"13", "Wayanad":"14"} },
    "Madhya Pradesh": { code: "MP", district: {"Agar Malwa":"01", "Alirajpur":"02", "Anuppur":"03", "Ashoknagar":"04", "Balaghat":"05", "Barwani":"06", "Betul":"07", "Bhind":"08", "Bhopal":"09", "Burhanpur":"10", "Chhatarpur":"11", "Chhindwara":"12", "Damoh":"13", "Datia":"14", "Dewas":"15", "Dhar":"16", "Dindori":"17", "Guna":"18", "Gwalior":"19", "Harda":"20", "Hoshangabad":"21", "Indore":"22", "Jabalpur":"23", "Jhabua":"24", "Katni":"25", "Khandwa":"26", "Khargone":"27", "Mandla":"28", "Mandsaur":"29", "Morena":"30", "Narsinghpur":"31", "Neemuch":"32", "Panna":"33", "Raisen":"34", "Rajgarh":"35", "Ratlam":"36", "Rewa":"37", "Sagar":"38", "Satna":"39", "Sehore":"40", "Seoni":"41", "Shahdol":"42", "Shajapur":"43", "Sheopur":"44", "Shivpuri":"45", "Sidhi":"46", "Singrauli":"47", "Tikamgarh":"48", "Ujjain":"49", "Umaria":"50", "Vidisha":"51"} },
    "Maharashtra": { code: "MH", district: {"Ahmednagar":"01", "Akola":"02", "Amravati":"03", "Aurangabad":"04", "Beed":"05", "Bhandara":"06", "Buldhana":"07", "Chandrapur":"08", "Dhule":"09", "Gadchiroli":"10", "Gondia":"11", "Hingoli":"12", "Jalgaon":"13", "Jalna":"14", "Kolhapur":"15", "Latur":"16", "Mumbai City":"17", "Mumbai Suburban":"18", "Nagpur":"19", "Nanded":"20", "Nandurbar":"21", "Nashik":"22", "Osmanabad":"23", "Palghar":"24", "Parbhani":"25", "Pune":"26", "Raigad":"27", "Ratnagiri":"28", "Sangli":"29", "Satara":"30", "Sindhudurg":"31", "Solapur":"32", "Thane":"33", "Wardha":"34", "Washim":"35", "Yavatmal":"36"} },
    "Manipur": { code: "MN", district: {"Bishnupur":"01", "Chandel":"02", "Churachandpur":"03", "Imphal East":"04", "Imphal West":"05", "Jiribam":"06", "Kakching":"07", "Kamjong":"08", "Kangpokpi":"09", "Noney":"10", "Pherzawl":"11", "Senapati":"12", "Tamenglong":"13", "Tengnoupal":"14", "Thoubal":"15", "Ukhrul":"16"} },
    "Meghalaya": { code: "ML", district: {"East Garo Hills":"01", "East Jaintia Hills":"02", "East Khasi Hills":"03", "North Garo Hills":"04", "Ri-Bhoi":"05", "South Garo Hills":"06", "South West Garo Hills":"07", "South West Khasi Hills":"08", "West Garo Hills":"09", "West Jaintia Hills":"10", "West Khasi Hills":"11"} },
    "Mizoram": { code: "MZ", district: {"Aizawl":"01", "Champhai":"02", "Kolasib":"03", "Lawngtlai":"04", "Lunglei":"05", "Mamit":"06", "Saiha":"07", "Serchhip":"08"} },
    "Nagaland": { code: "NL", district: {"Dimapur":"01", "Kiphire":"02", "Kohima":"03", "Longleng":"04", "Mokokchung":"05", "Mon":"06", "Peren":"07", "Phek":"08", "Tuensang":"09", "Wokha":"10", "Zunheboto":"11"} },
    "Odisha": { code: "OR", district: {"Angul":"01", "Balangir":"02", "Balasore":"03", "Bargarh":"04", "Bhadrak":"05", "Boudh":"06", "Cuttack":"07", "Deogarh":"08", "Dhenkanal":"09", "Gajapati":"10", "Ganjam":"11", "Jagatsinghpur":"12", "Jajpur":"13", "Jharsuguda":"14", "Kalahandi":"15", "Kandhamal":"16", "Kendrapara":"17", "Kendujhar":"18", "Khordha":"19", "Koraput":"20", "Malkangiri":"21", "Mayurbhanj":"22", "Nabarangpur":"23", "Nayagarh":"24", "Nuapada":"25", "Puri":"26", "Rayagada":"27", "Sambalpur":"28", "Subarnapur":"29", "Sundargarh":"30"} },
    "Punjab": { code: "PB", district: {"Amritsar":"01", "Barnala":"02", "Bathinda":"03", "Faridkot":"04", "Fatehgarh Sahib":"05", "Fazilka":"06", "Ferozepur":"07", "Gurdaspur":"08", "Hoshiarpur":"09", "Jalandhar":"10", "Kapurthala":"11", "Ludhiana":"12", "Malerkotla":"13", "Mansa":"14", "Moga":"15", "Mohali":"16", "Muktsar":"17", "Nawanshahr":"18", "Pathankot":"19", "Patiala":"20", "Rupnagar":"21", "Sangrur":"22", "Tarn Taran":"23"} },
    "Rajasthan": { code: "RJ", district: {"Ajmer":"01", "Alwar":"02", "Banswara":"03", "Baran":"04", "Barmer":"05", "Bharatpur":"06", "Bhilwara":"07", "Bikaner":"08", "Bundi":"09", "Chittorgarh":"10", "Churu":"11", "Dausa":"12", "Dholpur":"13", "Dungarpur":"14", "Hanumangarh":"15", "Jaipur":"16", "Jaisalmer":"17", "Jalore":"18", "Jhalawar":"19", "Jhunjhunu":"20", "Jodhpur":"21", "Karauli":"22", "Kota":"23", "Nagaur":"24", "Pali":"25", "Pratapgarh":"26", "Rajsamand":"27", "Sawai Madhopur":"28", "Sikar":"29", "Sirohi":"30", "Sri Ganganagar":"31", "Tonk":"32", "Udaipur":"33"} },
    "Sikkim": { code: "SK", district: {"East Sikkim":"01", "North Sikkim":"02", "South Sikkim":"03", "West Sikkim":"04"} },
    "Tamil Nadu": { code: "TN", district: {"Ariyalur":"01", "Chengalpattu":"02", "Chennai":"03", "Coimbatore":"04", "Cuddalore":"05", "Dharmapuri":"06", "Dindigul":"07", "Erode":"08", "Kallakurichi":"09", "Kanchipuram":"10", "Kanyakumari":"11", "Karur":"12", "Krishnagiri":"13", "Madurai":"14", "Nagapattinam":"15", "Namakkal":"16", "Nilgiris":"17", "Perambalur":"18", "Pudukkottai":"19", "Ramanathapuram":"20", "Ranipet":"21", "Salem":"22", "Sivaganga":"23", "Tenkasi":"24", "Thanjavur":"25", "Theni":"26", "Thoothukudi":"27", "Tiruchirappalli":"28", "Tirunelveli":"29", "Tirupathur":"30", "Tiruppur":"31", "Tiruvallur":"32", "Tiruvannamalai":"33", "Tiruvarur":"34", "Vellore":"35", "Viluppuram":"36", "Virudhunagar":"37"} },
    "Telangana": { code: "TG", district: {"Adilabad":"01", "Bhadradri Kothagudem":"02", "Hyderabad":"03", "Jagtial":"04", "Jangaon":"05", "Jayashankar Bhupalpally":"06", "Jogulamba Gadwal":"07", "Kamareddy":"08", "Karimnagar":"09", "Khammam":"10", "Komaram Bheem":"11", "Mahabubabad":"12", "Mahabubnagar":"13", "Mancherial":"14", "Medak":"15", "Medchal–Malkajgiri":"16", "Mulugu":"17", "Nagarkurnool":"18", "Nalgonda":"19", "Narayanpet":"20", "Nirmal":"21", "Nizamabad":"22", "Peddapalli":"23", "Rajanna Sircilla":"24", "Ranga Reddy":"25", "Sangareddy":"26", "Siddipet":"27", "Suryapet":"28", "Vikarabad":"29", "Wanaparthy":"30", "Warangal Rural":"31", "Warangal Urban":"32", "Yadadri Bhuvanagiri":"33"} },
    "Tripura": { code: "TR", district: {"Dhalai":"01", "Gomati":"02", "Khowai":"03", "North Tripura":"04", "Sepahijala":"05", "South Tripura":"06", "Unakoti":"07", "West Tripura":"08"} },
    "Uttar Pradesh": { code: "UP", district: {"Agra":"01", "Aligarh":"02", "Allahabad":"03", "Ambedkar Nagar":"04", "Amethi":"05", "Amroha":"06", "Auraiya":"07", "Azamgarh":"08", "Baghpat":"09", "Bahraich":"10", "Ballia":"11", "Balrampur":"12", "Banda":"13", "Barabanki":"14", "Bareilly":"15", "Basti":"16", "Bijnor":"17", "Budaun":"18", "Bulandshahr":"19", "Chandauli":"20", "Chitrakoot":"21", "Deoria":"22", "Etah":"23", "Etawah":"24", "Faizabad":"25", "Farrukhabad":"26", "Fatehpur":"27", "Firozabad":"28", "Gautam Buddh Nagar":"29", "Ghaziabad":"30", "Ghazipur":"31", "Gonda":"32", "Gorakhpur":"33", "Hamirpur":"34", "Hapur":"35", "Hardoi":"36", "Hathras":"37", " Jalaun":"38", "Jaunpur":"39", "Jhansi":"40", "Kannauj":"41", "Kanpur Dehat":"42", "Kanpur Nagar":"43", "Kasganj":"44", "Kaushambi":"45", "Kheri":"46", "Kushinagar":"47", "Lalitpur":"48", "Lucknow":"49", "Maharajganj":"50", "Mahoba":"51", "Mainpuri":"52", "Mathura":"53", "Mau":"54", "Meerut":"55", "Mirzapur":"56", "Moradabad":"57", "Muzaffarnagar":"58", "Pilibhit":"59", "Pratapgarh":"60", "Rae Bareli":"61", "Rampur":"62", "Saharanpur":"63", "Sambhal":"64", "Sant Kabir Nagar":"65", "Sant Ravidas Nagar":"66", "Shahjahanpur":"67", "Shamli":"68", "Shravasti":"69", "Siddharthnagar":"70", "Sitapur":"71", "Sonbhadra":"72", "Sultanpur":"73", "Unnao":"74", "Varanasi":"75"} },
    "Uttarakhand": { code: "UK", district: {"Almora":"01", "Bageshwar":"02", "Chamoli":"03", "Champawat":"04", "Dehradun":"05", "Haridwar":"06", "Nainital":"07", "Pauri Garhwal":"08", "Pithoragarh":"09", "Rudraprayag":"10", "Tehri Garhwal":"11", "Udham Singh Nagar":"12", "Uttarkashi":"13"} },
    "West Bengal": { code: "WB", district: {"Alipurduar":"01", "Bankura":"02", "Birbhum":"03", "Cooch Behar":"04", "Dakshin Dinajpur":"05", "Darjeeling":"06", "Hooghly":"07", "Howrah":"08", "Jalpaiguri":"09", "Jhargram":"10", "Kalimpong":"11", "Kolkata":"12", "Malda":"13", "Murshidabad":"14", "Nadia":"15", "North 24 Parganas":"16", "Paschim Bardhaman":"17", "Paschim Medinipur":"18", "Purba Bardhaman":"19", "Purba Medinipur":"20", "Purulia":"21", "South 24 Parganas":"22", "Uttar Dinajpur":"23"} },
    "Delhi": { code: "DL", district: {"Central Delhi":"01", "East Delhi":"02", "New Delhi":"03", "North Delhi":"04", "North East Delhi":"05", "North West Delhi":"06", "Shahdara":"07", "South Delhi":"08", "South East Delhi":"09", "South West Delhi":"10", "West Delhi":"11"} },
    "Ladakh": { code: "LA", district: {"Kargil":"01", "Leh":"02"} }
};

const hospitalSuggestions = {
    "Karur": [
        "Apollo Hospital",
        "Amaravathi Hospital",
        "Vasan Eye Care Hospital",
        "Aarthy Eye Hospital",
        "ABS Hospital",
        "Velan Eye Hospital",
        "Deepa Kannan Hospital",
        "Somasundaram Eye Hospital",
        "Ammaiyappa Hospital",
        "Kumaran Hospital",
        "Kabila Hospital",
        "Karur Government Hospital",
        "K B Kavita Skin Care Hospital",
        "Dr. Selvam Cardiology Hospital",
        "Sushila Periyaswamy Hospital",
        "Sri Balaji Physio Clinic",
        "Akhila Children's Hospital",
        "Kasturibai Municipal Maternity Hospital",
        "ERS Hospital",
        "S and V Loga Hospital Private Limited",
        "Nirmala Nursing Home",
        "Abirami Hospitals",
        "Abishek Ortho Center",
        "Government Head Quarters Hospital, Kulithalai",
        "Government Hospital, Aravakurichi",
        "Government Hospital, Krishnarayapuram",
        "Government Hospital, Manmangalam",
        "Government Hospital, Mylampatti",
        "Government Hospital, Pallapatti",
        "Government Hospital, Velayuthampalayam",
        "Government Medical College Hospital, Karur",
        "Primary Health Centre, Ayyampalayam",
        "Primary Health Centre, Ayyarmalai",
        "Primary Health Centre, Chinnadharapuram",
        "Primary Health Centre, Esanatham",
        "Primary Health Centre, Govindampalayam",
        "Primary Health Centre, Inungur",
        "Primary Health Centre, K. Paramathy",
        "Primary Health Centre, Kadavur",
        "Primary Health Centre, Kallapalli",
        "Primary Health Centre, Kaniyalampatti",
        "Primary Health Centre, Karuppampalayam",
        "Primary Health Centre, Karvazhi",
        "Primary Health Centre, Olapalayam",
        "Primary Health Centre, Panjapatti",
        "Primary Health Centre, Punnam"
    ]
};
        
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("patientForm");

	// Populate state/district selects on register page
	initializeStateDistrictSelects();

    form.addEventListener("submit", function (event) {
        // Prevent form submission if validation fails
        if (!validateForm()) {
            event.preventDefault();
        } else {
            showSuccessMessage();
        }
    });
});

function validateForm() {
    let name = document.getElementById("name").value.trim();
    let age = document.getElementById("age").value.trim();
	// Support both select-based and legacy input-based fields
	let stateEl = document.getElementById("stateSelect") || document.getElementById("state");
	let districtEl = document.getElementById("districtSelect") || document.getElementById("district");
	let state = stateEl ? stateEl.value.trim() : "";
	let district = districtEl ? districtEl.value.trim() : "";
    let patientId = document.getElementById("patientId").value.trim();
    let userInput = document.getElementById("user-input").value;

    if (!name || !state || !district || !userInput) {
        alert("All fields must be filled.");
        return false;
    }

    if (isNaN(age) || age <= 0) {
        alert("Age must be a positive number.");
        return false;
    }

    if (userInput.length !== 6 || !/^\d{6}$/.test(userInput)) {
        alert("Last 6 digits must be exactly 6 numbers.");
        return false;
    }

    if (!patientId.startsWith("IND") || patientId.length !== 13) {
        alert("Patient ID must start with 'IND' and be 13 characters long.");
        return false;
    }

    return true;
}

function showSuccessMessage() {
    let successMessage = document.getElementById("successMessage");
    successMessage.classList.remove("hidden");

    setTimeout(() => {
        successMessage.classList.add("hidden");
    }, 3000);
}

function showStateSuggestions() {
    const input = document.getElementById('state').value.toLowerCase();
    const suggestions = document.getElementById('stateSuggestions');
    suggestions.innerHTML = '';

    if (input.length > 0) {
        Object.keys(stateDistricts).forEach(state => {
            if (state.toLowerCase().includes(input)) {
                const div = document.createElement('div');
                div.className = 'autocomplete-item';
                div.textContent = state;
                div.onclick = () => {
                    document.getElementById('state').value = state;
                    suggestions.innerHTML = '';
                    generatePatientID();
                };
                suggestions.appendChild(div);
            }
        });
    }
}

function showDistrictSuggestions() {
    const state = document.getElementById('state').value;
    const input = document.getElementById('district').value.toLowerCase();
    const suggestions = document.getElementById('districtSuggestions');
    suggestions.innerHTML = '';

    if (stateDistricts[state] && input.length > 0) {
        Object.keys(stateDistricts[state].district).forEach(district => {
            if (district.toLowerCase().includes(input)) {
                const div = document.createElement('div');
                div.className = 'autocomplete-item';
                div.textContent = district;
                div.onclick = () => {
                    document.getElementById('district').value = district;
                    suggestions.innerHTML = '';
                    generatePatientID();
                };
                suggestions.appendChild(div);
            }
        });
    }
}

function showHospitalSuggestions() {
    const district = document.getElementById('district').value;
    const input = document.getElementById('hospital').value.toLowerCase();
    const suggestions = document.getElementById('hospitalSuggestions');
    suggestions.innerHTML = '';

    if (hospitalSuggestions[district] && input.length > 0) {
        hospitalSuggestions[district].forEach(hospital => {
            if (hospital.toLowerCase().includes(input)) {
                const div = document.createElement('div');
                div.className = 'autocomplete-item';
                div.textContent = hospital;
                div.onclick = () => {
                    document.getElementById('hospital').value = hospital;
                    suggestions.innerHTML = '';
                };
                suggestions.appendChild(div);
            }
        });
    }
}

function generatePatientID() {
    // Support both select-based and legacy input-based fields
    let stateEl = document.getElementById("stateSelect") || document.getElementById("state");
    let districtEl = document.getElementById("districtSelect") || document.getElementById("district");
    let state = stateEl ? stateEl.value : "";
    let district = districtEl ? districtEl.value : "";
    let userInput = document.getElementById("user-input").value.toUpperCase().padEnd(6, "-");

    let stateCode = (state && stateDistricts[state] && stateDistricts[state].code) ? stateDistricts[state].code : "--";
    let districtCode = (state && district && stateDistricts[state] && stateDistricts[state].district && stateDistricts[state].district[district]) ? stateDistricts[state].district[district] : "--";

    let patientID = `IND${stateCode}${districtCode}${userInput}`;

    document.getElementById("patientId").value = patientID;
    const display = document.getElementById("patientIdDisplay");
    if (display) display.textContent = patientID;
}

// Initialize cascading state and district selects on register page
function initializeStateDistrictSelects() {
    const stateSelect = document.getElementById('stateSelect');
    const districtSelect = document.getElementById('districtSelect');
    if (!stateSelect || !districtSelect) return;

    // Fill states
    const states = Object.keys(stateDistricts).sort((a, b) => a.localeCompare(b));
    states.forEach(st => {
        const opt = document.createElement('option');
        opt.value = st;
        opt.textContent = st;
        stateSelect.appendChild(opt);
    });

    function populateDistrictsForState(st) {
        districtSelect.innerHTML = '';
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = 'Select district';
        districtSelect.appendChild(placeholder);

        if (!st || !stateDistricts[st]) {
            districtSelect.disabled = true;
            return;
        }

        const districts = Object.keys(stateDistricts[st].district).sort((a, b) => a.localeCompare(b));
        districts.forEach(d => {
            const opt = document.createElement('option');
            opt.value = d;
            opt.textContent = d;
            districtSelect.appendChild(opt);
        });
        districtSelect.disabled = false;
    }

    stateSelect.addEventListener('change', () => {
        populateDistrictsForState(stateSelect.value);
        districtSelect.value = '';
        generatePatientID();
    });

    districtSelect.addEventListener('change', () => {
        generatePatientID();
    });

    // Initialize with current value (if any)
    populateDistrictsForState(stateSelect.value);
}

// ========== Generic Table Utilities: Search + Sort ==========
// Automatically adds a search input and enables click-to-sort on all tables with class 'table'
(function () {
    function normalizeText(txt) {
        return (txt || "").toString().toLowerCase().trim();
    }

    function createSearchBox(table) {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-controls';
        wrapper.style.display = 'flex';
        wrapper.style.justifyContent = 'space-between';
        wrapper.style.alignItems = 'center';
        wrapper.style.margin = '8px 0';

        const label = document.createElement('label');
        label.textContent = 'Search:';
        label.style.marginRight = '8px';
        label.setAttribute('for', 'table-search-' + Math.random().toString(36).slice(2));

        const input = document.createElement('input');
        input.type = 'search';
        input.placeholder = 'Type to filter rows';
        input.id = label.getAttribute('for');
        input.style.maxWidth = '260px';
        input.style.padding = '6px 10px';

        const left = document.createElement('div');
        left.style.display = 'flex';
        left.style.alignItems = 'center';
        left.appendChild(label);
        left.appendChild(input);

        wrapper.appendChild(left);

        // Insert controls just before the table
        table.parentNode.insertBefore(wrapper, table);

        input.addEventListener('input', () => applyFilter(table, input.value));
    }

    function applyFilter(table, query) {
        const q = normalizeText(query);
        const tbody = table.tBodies[0];
        if (!tbody) return;
        Array.from(tbody.rows).forEach(tr => {
            const rowText = normalizeText(Array.from(tr.cells).map(td => td.textContent).join(' '));
            tr.style.display = rowText.includes(q) ? '' : 'none';
        });
    }

    function makeSortable(table) {
        const thead = table.tHead;
        const tbody = table.tBodies[0];
        if (!thead || !tbody) return;

        Array.from(thead.rows[0].cells).forEach((th, colIndex) => {
            th.style.cursor = 'pointer';
            th.setAttribute('aria-sort', 'none');

            th.addEventListener('click', () => {
                const current = th.getAttribute('data-sort') || 'none';
                const next = current === 'asc' ? 'desc' : 'asc';

                // reset others
                Array.from(thead.rows[0].cells).forEach(h => {
                    h.removeAttribute('data-sort');
                    h.setAttribute('aria-sort', 'none');
                });

                th.setAttribute('data-sort', next);
                th.setAttribute('aria-sort', next === 'asc' ? 'ascending' : 'descending');

                const rows = Array.from(tbody.rows).filter(r => r.style.display !== 'none'); // respect active filter
                const cmp = (a, b) => {
                    const ta = normalizeText(a.cells[colIndex]?.textContent);
                    const tb = normalizeText(b.cells[colIndex]?.textContent);
                    const na = parseFloat(ta.replace(/[^0-9.\-]/g, ''));
                    const nb = parseFloat(tb.replace(/[^0-9.\-]/g, ''));
                    const bothNumbers = !isNaN(na) && !isNaN(nb);
                    if (bothNumbers) {
                        return na === nb ? 0 : na < nb ? -1 : 1;
                    }
                    return ta.localeCompare(tb);
                };

                rows.sort((r1, r2) => (next === 'asc' ? cmp(r1, r2) : cmp(r2, r1)));
                rows.forEach(r => tbody.appendChild(r));
            });
        });
    }

    function enhanceAllTables() {
        const tables = document.querySelectorAll('table.table');
        tables.forEach(table => {
            // Avoid double-init
            if (table.__enhanced) return;
            table.__enhanced = true;
            createSearchBox(table);
            makeSortable(table);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enhanceAllTables);
    } else {
        enhanceAllTables();
    }
})();

// ========== Advanced Filtering Utilities ==========
(function() {
    // Auto-complete functionality for filter inputs
    function createAutocomplete(input, options, onSelect) {
        let suggestionsDiv = null;
        
        function createSuggestions() {
            if (suggestionsDiv) {
                suggestionsDiv.remove();
            }
            
            suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'autocomplete-suggestions';
            suggestionsDiv.style.cssText = 'position: absolute; z-index: 1000; background: white; border: 1px solid var(--border); border-radius: 8px; box-shadow: var(--shadow); max-height: 200px; overflow-y: auto; width: 100%;';
            
            input.parentNode.style.position = 'relative';
            input.parentNode.appendChild(suggestionsDiv);
        }
        
        function filterOptions(query) {
            if (!query || query.length < 2) return [];
            return options.filter(option => 
                option.toLowerCase().includes(query.toLowerCase())
            ).slice(0, 10); // Limit to 10 suggestions
        }
        
        function showSuggestions(query) {
            const filtered = filterOptions(query);
            if (filtered.length === 0) {
                suggestionsDiv.style.display = 'none';
                return;
            }
            
            suggestionsDiv.innerHTML = '';
            suggestionsDiv.style.display = 'block';
            
            filtered.forEach(option => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.style.cssText = 'padding: 8px 12px; cursor: pointer; border-bottom: 1px solid #f0f0f0;';
                item.textContent = option;
                
                item.addEventListener('click', () => {
                    input.value = option;
                    suggestionsDiv.style.display = 'none';
                    if (onSelect) onSelect(option);
                });
                
                item.addEventListener('mouseenter', () => {
                    item.style.backgroundColor = '#f8fafc';
                });
                
                item.addEventListener('mouseleave', () => {
                    item.style.backgroundColor = 'white';
                });
                
                suggestionsDiv.appendChild(item);
            });
        }
        
        function hideSuggestions() {
            setTimeout(() => {
                if (suggestionsDiv) {
                    suggestionsDiv.style.display = 'none';
                }
            }, 150);
        }
        
        input.addEventListener('input', (e) => {
            const query = e.target.value;
            if (query.length >= 2) {
                showSuggestions(query);
            } else {
                suggestionsDiv.style.display = 'none';
            }
        });
        
        input.addEventListener('blur', hideSuggestions);
        input.addEventListener('focus', (e) => {
            if (e.target.value.length >= 2) {
                showSuggestions(e.target.value);
            }
        });
        
        // Close suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!input.parentNode.contains(e.target)) {
                hideSuggestions();
            }
        });
        
        createSuggestions();
    }
    
    // Initialize autocomplete for filter inputs
    function initializeFilterAutocomplete() {
        // Hospital filter autocomplete
        const hospitalInput = document.getElementById('hospital');
        if (hospitalInput) {
            // Fetch hospital options dynamically
            fetch('/api/filter_options?type=hospitals')
                .then(response => response.json())
                .then(data => {
                    createAutocomplete(hospitalInput, data.options, (selected) => {
                        // Auto-submit form when hospital is selected
                        const form = document.getElementById('filterForm');
                        if (form) form.submit();
                    });
                })
                .catch(error => console.error('Error fetching hospitals:', error));
        }
        
        // Doctor filter autocomplete (if needed)
        const doctorInput = document.getElementById('doctor');
        if (doctorInput) {
            // For doctor names, we could implement a more sophisticated search
            // For now, just add basic functionality
            doctorInput.addEventListener('input', (e) => {
                if (e.target.value.length >= 3) {
                    // Could implement real-time search here
                }
            });
        }
    }
    
    // Enhanced date range validation
    function initializeDateValidation() {
        const dateFrom = document.getElementById('date_from');
        const dateTo = document.getElementById('date_to');
        
        if (dateFrom && dateTo) {
            function validateDateRange() {
                if (dateFrom.value && dateTo.value) {
                    if (new Date(dateFrom.value) > new Date(dateTo.value)) {
                        dateTo.setCustomValidity('End date must be after start date');
                        dateTo.reportValidity();
                    } else {
                        dateTo.setCustomValidity('');
                    }
                }
            }
            
            dateFrom.addEventListener('change', validateDateRange);
            dateTo.addEventListener('change', validateDateRange);
        }
    }
    
    // Real-time filter count updates
    function initializeFilterCounts() {
        const filterForm = document.getElementById('filterForm');
        if (!filterForm) return;
        
        const inputs = filterForm.querySelectorAll('input, select');
        const countDisplay = document.querySelector('[data-filter-count]');
        
        function updateFilterCount() {
            let activeFilters = 0;
            inputs.forEach(input => {
                if (input.value && input.value.trim() !== '') {
                    activeFilters++;
                }
            });
            
            if (countDisplay) {
                countDisplay.textContent = `${activeFilters} filter(s) active`;
            }
        }
        
        inputs.forEach(input => {
            input.addEventListener('change', updateFilterCount);
            input.addEventListener('input', updateFilterCount);
        });
        
        updateFilterCount();
    }
    
    // Initialize all filter enhancements
    function initializeFilterEnhancements() {
        initializeFilterAutocomplete();
        initializeDateValidation();
        initializeFilterCounts();
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeFilterEnhancements);
    } else {
        initializeFilterEnhancements();
    }
})();
