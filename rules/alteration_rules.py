# =====================================
# ALTERA ALTERATION DATABASE
# =====================================

ALTERATION_DATABASE = {

"Propylitic":{

    "diagnostic":[
        "Chlorite",
        "Epidote",
        "Calcite"
    ],

    "common":[
        "Quartz",
        "Pyrite",
        "Albite",
        "Actinolite"
    ],

    "possible":[
        "Magnetite"
    ],

    "support":[
        "Moderate CCPI",
        "Low AI",
        "High Mg Number"
    ]

},

"Phyllic":{

    "diagnostic":[
        "Sericite",
        "Pyrite"
    ],

    "common":[
        "Quartz",
        "Illite"
    ],

    "possible":[
        "Chlorite",
        "Rutile"
    ],

    "support":[
        "High AI",
        "High K/Na"
    ]

},

"Argillic":{

    "diagnostic":[
        "Kaolinite",
        "Illite",
        "Smectite"
    ],

    "common":[
        "Quartz"
    ],

    "possible":[
        "Pyrite"
    ],

    "support":[
        "High AI"
    ]

},

"Advanced Argillic":{

    "diagnostic":[
        "Alunite",
        "Dickite",
        "Pyrophyllite"
    ],

    "common":[
        "Quartz",
        "Kaolinite"
    ],

    "possible":[
        "Diaspore",
        "Zunyite"
    ],

    "support":[
        "Very High AI"
    ]

},

"Potassic":{

    "diagnostic":[
        "K-Feldspar",
        "Biotite"
    ],

    "common":[
        "Quartz",
        "Magnetite"
    ],

    "possible":[
        "Actinolite"
    ],

    "support":[
        "High K/Na"
    ]

}

}

# =====================================
# IDENTIFY MINERALS
# =====================================

def identify_minerals(sample, threshold=5):

    minerals = []

    for mineral, value in sample.items():

        if mineral == "Sample":
            continue

        if value >= threshold:

            minerals.append(mineral)

    return minerals

# =====================================
# COUNT MATCHES
# =====================================

def count_matches(minerals, target):

    count = 0

    for mineral in target:

        if mineral in minerals:
            count += 1

    return count

# =====================================
# CALCULATE ALTERATION MATCHES
# =====================================

def calculate_matches(minerals):

    results = {}

    for zone, data in ALTERATION_DATABASE.items():

        diagnostic = count_matches(
            minerals,
            data["diagnostic"]
        )

        common = count_matches(
            minerals,
            data["common"]
        )

        possible = count_matches(
            minerals,
            data["possible"]
        )

        results[zone] = {

            "diagnostic": diagnostic,

            "common": common,

            "possible": possible

        }

    return results

# =====================================
# INTERPRET ALTERATION
# =====================================

def interpret_alteration(matches):

    best_zone = None
    best_score = -1

    for zone, data in matches.items():

        score = (
            data["diagnostic"] * 3 +
            data["common"] * 2 +
            data["possible"] * 1
        )

        if score > best_score:

            best_score = score
            best_zone = zone

    return best_zone, best_score

# =====================================
# GET ALTERATION EVIDENCE
# =====================================

def get_evidence(minerals, zone):

    database = ALTERATION_DATABASE[zone]

    diagnostic = [
        mineral
        for mineral in database["diagnostic"]
        if mineral in minerals
    ]

    common = [
        mineral
        for mineral in database["common"]
        if mineral in minerals
    ]

    possible = [
        mineral
        for mineral in database["possible"]
        if mineral in minerals
    ]

    return {

        "diagnostic": diagnostic,

        "common": common,

        "possible": possible

    }

# =====================================
# CONFIDENCE LEVEL
# =====================================

def confidence_level(score):

    if score >= 8:

        return "Strong Evidence"

    elif score >= 5:

        return "Moderate Evidence"

    elif score >= 3:

        return "Weak Evidence"

    else:

        return "Insufficient Evidence"
    

def generate_interpretation(
    sample_name,
    zone,
    evidence,
    confidence
):

    text = f"Sampel {sample_name} "

    if zone == "Potassic":

        text += (
            "diinterpretasikan termasuk ke dalam zona Potassic "
            "karena mengandung mineral diagnostik "
        )

    elif zone == "Phyllic":

        text += (
            "diinterpretasikan termasuk ke dalam zona Phyllic "
            "karena didominasi mineral serisitisasi "
            "dan sulfida hidrotermal. "
        )

    elif zone == "Propylitic":

        text += (
            "diinterpretasikan sebagai zona Propylitic "
            "karena menunjukkan himpunan mineral alterasi "
            "bertemperatur relatif rendah. "
        )

    elif zone == "Argillic":

        text += (
            "diinterpretasikan sebagai zona Argillic "
            "karena didominasi mineral lempung hasil alterasi. "
        )

    elif zone == "Advanced Argillic":

        text += (
            "diinterpretasikan sebagai zona Advanced Argillic "
            "yang umumnya terbentuk pada sistem hidrotermal "
            "bersifat sangat asam. "
        )

    diagnostic = ", ".join(evidence["diagnostic"])

    common = ", ".join(evidence["common"])

    if diagnostic != "":

        text += (
            f"Mineral diagnostik yang ditemukan yaitu "
            f"{diagnostic}. "
        )

    if common != "":

        text += (
            f"Mineral pendukung yang ikut teridentifikasi "
            f"antara lain {common}. "
        )

    text += (
        f"Tingkat keyakinan interpretasi termasuk "
        f"{confidence}."
    )

    return text