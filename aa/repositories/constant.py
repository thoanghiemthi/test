PATTERN_DATETIME = "%Y-%m-%d"

PATERN_MONTH = "%Y-%-m"

STATUS_DONE = "Done"

SUPPORT_RATE = 0.1

# Ops: 0.3
# Task create: 0.2
# Task manage, review, create: 0.25
MEMBERS = {
    "dungphanquang": 3000,
    "loinguyenduc": 3000,
    "vuonglevan": 3000,
    "tung491": 3000,
    "thangbq": 3000,
    "tungnguyentu": 3000,
    "vinhvungoc": 3000,
    "triduongvan": 3000,
    "thanhnguyencong": 3000,
    "khangletruc": 3000,
    "duynguyenngoc": 3000
}

RANKS = {
    "late1 - Không đạt": "E",
    "late2- Đạt": "D",
    "late3- Rất tốt": "C",
    "pass1 - Không đạt": "E",
    "pass2- Đạt": "C",
    "pass3- Rất tốt": "B",
    "early1 - Không đạt": "E",
    "early2- Đạt": "B",
    "early3- Rất tốt": "A",
    "fail1 - Không đạt": "E",
    "fail2- Đạt": "E",
    "fail3- Rất tốt": "E",
    "failNone": "E",
    "passNone": "E",
    "earlyNone": "E",
    "lateNone": "E",
    "late": "E",
}

POINTS = {
    "Development1 - LowA":200,
    "Development1 - LowB":100,
    "Development1 - LowC":50,
    "Development1 - LowD":20,
    "Development1 - LowE":-50,
    "Development2 - MediumA":600,
    "Development2 - MediumB":300,
    "Development2 - MediumC":150,
    "Development2 - MediumD":60,
    "Development2 - MediumE":-150,
    "Development3 - HighA":1200,
    "Development3 - HighB":600,
    "Development3 - HighC":300,
    "Development3 - HighD":120,
    "Development3 - HighE":-300,
    "RnD1 - LowA":600,
    "RnD1 - LowB":300,
    "RnD1 - LowC":150,
    "RnD1 - LowD":60,
    "RnD1 - LowE":-150,
    "RnD2 - MediumA":1000,
    "RnD2 - MediumB":500,
    "RnD2 - MediumC":250,
    "RnD2 - MediumD":100,
    "RnD2 - MediumE":-250,
    "RnD3 - HighA":1400,
    "RnD3 - HighB":700,
    "RnD3 - HighC":350,
    "RnD3 - HighD":140,
    "RnD3 - HighE":-350,
    "Support1 - LowA":100,
    "Support1 - LowB":50,
    "Support1 - LowC":25,
    "Support1 - LowD":10,
    "Support1 - LowE":-25,
    "Support2 - MediumA":200,
    "Support2 - MediumB":100,
    "Support2 - MediumC":50,
    "Support2 - MediumD":20,
    "Support2 - MediumE":-50,
    "Support3 - HighA":400,
    "Support3 - HighB":200,
    "Support3 - HighC":100,
    "Support3 - HighD":40,
    "Support3 - HighE":-100,
    "None1 - LowE": 0,
    "None2 - MediumE": 0,
    "None3 - HighE": 0,
    "None1 - LowA": 0,
    "None2 - MediumA": 0,
    "None3 - HighA": 0,
    "None1 - LowB": 0,
    "None2 - MediumB": 0,
    "None3 - HighB": 0,
    "None1 - LowC": 0,
    "None2 - MediumC": 0,
    "None3 - HighC": 0,
    "None1 - LowD": 0,
    "None2 - MediumD": 0,
    "None3 - HighD": 0,
    "DevelopmentNoneE": 0,
    "RnDNoneE": 0
}

SALARY_BONUS = {
    'L1': 0,
    'L2': 0,
    'L3': 0,
    'L4': 0,
    'L5': 0,
    'L6': 0,
    'L0': 0
}

TRAINING_BONUS = {
    '2022-8': {
        'vuonglevan': {
            'description': 'Backend meeting',
            'point': 8
        },
        'duynn': {
            'description': 'Intern training',
            'point': 8
        },
    }
}

RELEASE_BONUS = {
    '2022-8': {
        'anhhoangtung': { 
            'description': 'Webmail release',
            'point': 2.5
        },
        'loinguyenduc': {
            'description': 'Webmail release',
            'point': 5
        },
        'tung491': { 
            'description': 'CS release',
            'point': 2.5
        },
    }
}

IMPROVEMENT_BONUS = {
    '2021-12': {
        '': {
            'description': '',
            'point': 0
        },
    }
}
