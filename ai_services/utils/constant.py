import os

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

# Constants for each file type category
PDF_TYPES = ['pdf']
WORD_TYPES = ['docx', 'doc']
OOTM_TYPES = ['odt', 'ott', 'txt', 'md']
IMAGE_TYPES = ['jpg', 'jpeg', 'tiff', 'tif', 'gif', 'png']
VOICE_TYPES = ['mp3', 'ogg', 'wma', 'mp4', 'aac', 'm4a', 'wav', 'aiff', 'flac']

# Combining all categories into one main list
ALLOWED_FILE_TYPES_LIST = PDF_TYPES + WORD_TYPES + OOTM_TYPES + IMAGE_TYPES + VOICE_TYPES


LANG_MAPPING_LANGID = {
    'en': 'eng',
    'ar': 'ara', }

GENERAL_ERROR = "General Error"

EXPERIENCE_LEVELS = {
    "مبتدئ": "Entry",
    "متوسط": "Intermediate",
    "خبير": "Senior",
    "إداري": "Managerial",
    "مدير": "Director",
    "تنفيذي": "Executive"
}

MARITAL_STATUS ={ "اعزب": "Single", "متزوج": "Married"}


GENDERS = {"ذكر": "Male", "انثى": "Female", "غير محدد":"Unspecified"}

EDUCATIONAL_LEVEL = {
    "الثانوية": "High School",
    "الدبلوم": "Diploma",
    "البكالوريوس": "Bachelor",
    "الماجستير": "Master",
    "الدكتوراه": "Doctorate"
}

EN_EDUCATIONAL_LEVEL_KEYWORDS = {
    "Doctorate Of": [
        "Doctorate of",
        "Doctorate in",
        "Doctor of",
        "Doctor in",
        "Doctorate",
        "Doctor",
        "Phd of",
        "Phd in",
        "Phd"
    ],
    "Master Of": [
        "Master's of",
        "Master's in",
        "Master of",
        "Master in",
        "MSc of",
        "MSc in",
        "Master's",
        "Master",
        "MSc"
    ],
    "Bachelor Of": [
        "Bachelor's Of",
        "Bachelor's in",
        "Bachelor of",
        "Bachelor in",
        "Bachelor's",
        "Bachelor"
    ],
    "Diploma of": [
        "Diploma of",
        "Diploma in",
        "Diploma"
    ]
}

AR_EDUCATIONAL_LEVEL_KEYWORDS = {
    "الدكتوراه في": [
        "دكتورا",
    ],
    "ماجستير في": [
        "ماجستير",
        "ماستر"
    ],
    "بكالوريوس في": [
        "بكالوريوس"
    ],
    "دبلوم في": [
        "دبلوم"
    ]
}

LANGUAGES = {'الأفريكانية': 'Afrikaans',
             'الألبانية': 'Albanian',
             'الأمهرية': 'Amharic', 'اللغة العربية': 'Arabic', 'الآرامية': 'Aramaic', 'أرميني': 'Armenian',
             'أذربيجاني': 'Azerbaijani', 'البنغالية': 'Bengali', 'البوسنية': 'Bosnian', 'البلغارية': 'Bulgarian',
             'الكانتونية': 'Cantonese', 'صينى': 'Chinese', 'الكرواتية': 'Croatian', 'التشيكية': 'Czech', 'دانماركي': 'Danish',
             'هولندي': 'Dutch', 'اللغة الإنجليزية': 'English', 'الإستونية': 'Estonian', 'الفلبينية': 'Filipino',
             'الفنلندية': 'Finnish', 'الفرنسية': 'French', 'الجورجية': 'Georgian', 'الألمانية': 'German',
             'اليونانية': 'Greek', 'الغوجاراتية': 'Gujarati', 'الكريولية الهايتية': 'Haitian Creole', 'الهوسا': 'Hausa',
             'عبرى': 'Hebrew', 'الهندية': 'Hindi', 'المجرية': 'Hungarian', 'الأيسلندية': 'Icelandic', 'الإيجبو': 'Igbo',
             'الأندونيسية': 'Indonesian', 'الإيطالية': 'Italian', 'اليابانية': 'Japanese', 'الكانادا': 'Kannada',
             'الكازاخية': 'Kazakh', 'الخمير': 'Khmer', 'الكورية': 'Korean', 'كردى': 'Kurdish', 'القيرغيزية': 'Kyrgyz',
             'لاو': 'Lao', 'اللاتينية': 'Latin', 'اللاتفية': 'Latvian', 'اللتوانية': 'Lithuanian', 'اللوكسمبورجية': 'Luxembourgish',
             'المقدونية': 'Macedonian', 'المالاغاسية': 'Malagasy', 'لغة الملايو': 'Malay', 'المالايالامية': 'Malayalam',
             'المالطية': 'Maltese', 'ماورى': 'Maori', 'الماراثى': 'Marathi', 'المنغولية': 'Mongolian',
             'بورما (البورمية)': 'Myanmar (Burmese)', 'النيبالية': 'Nepali', 'النرويجية': 'Norwegian',
             'نيانجا (تشيتشيوا)': 'Nyanja (Chichewa)', 'الباشتو': 'Pashto', 'الفارسية': 'Persian', 'البولندية': 'Polish',
             'البرتغالية': 'Portuguese', 'البنجابية': 'Punjabi', 'الرومانية': 'Romanian', 'الروسية': 'Russian', 'ساموا': 'Samoan',
             'غيليس الإسكتلنديين': 'Scots Gaelic', 'الصربية': 'Serbian', 'السوتو': 'Sesotho', 'شونا': 'Shona', 'السندية': 'Sindhi',
             'سينهالا': 'Sinhala', 'السلوفاكية': 'Slovak', 'السلوفينية': 'Slovenian', 'الصومالية': 'Somali', 'الإسبانية': 'Spanish',
             'السودانية': 'Sundanese', 'السواحلية': 'Swahili', 'السويدية': 'Swedish', 'طاجيكى': 'Tajik', 'التاميل': 'Tamil',
             'التتارية': 'Tatar', 'التيلجو': 'Telugu', 'التايلاندية': 'Thai', 'اللغة التركية': 'Turkish', 'التركمانية': 'Turkmen',
             'الأوكرانية': 'Ukrainian', 'الأردية': 'Urdu', 'الأويغورية': 'Uyghur', 'أوزبكي': 'Uzbek', 'فيتنامي': 'Vietnamese',
             'الولزية': 'Welsh', 'الكوسا': 'Xhosa', 'اليديشية': 'Yiddish', 'اليوروبا': 'Yoruba', 'الزولو': 'Zulu'}




JOB_TYPES = {
                "دوام كامل": "Full Time",
                "دوام جزئي": "Part Time",
                "تعاقدية": "Contractual",
                "تدريب": "Internship",
                "فريلانسر": "Freelancer"
            }


#TODO: fill other values
SECTORS = {
    "الزراعة": "Agriculture",
    "الموارد الطبيعية": "Natural Resources",
    "الفنون": "Arts",
    "الإعلام": "Media",
    "الترفيه": "Entertainment",
    "البناء": "Building",
    "التشييد": "Construction",
    "الأعمال": "Business",
    "التمويل": "Finance",
    "التعليم": "Education",
    "تطوير الطفل": "Child Development",
    "الخدمات الأسرية": "Family Services",
    "الطاقة": "Energy",
    "البيئة": "Environment",
    "المرافق": "Utilities",
    "الهندسة": "Engineering",
    "العمارة": "Architecture",
    "تصميم الأزياء": "Fashion",
    "الديكور الداخلي": "Interior Design",
    "العلوم الصحية": "Health Science",
    "التكنولوجيا الطبية": "Medical Technology",
    "الضيافة": "Hospitality",
    "السياحة": "Tourism",
    "تكنولوجيا المعلومات": "Information Technology",
    "الاتصالات": "Communication",
    "التصنيع": "Manufacturing",
    "تطوير المنتجات": "Product Development",
    "التسويق": "Marketing",
    "المبيعات": "Sales",
    "الخدمات": "Services",
    "الخدمات العامة": "Public Services",
    "النقل": "Transportation"
}

FUNCTIONAL_AREAS = {
    "عمل حر": "Freelancing",
    "تسويق": "Marketing",
    "إنتاج": "Production",
    "التخطيط الاستراتيجي": "Strategy And Planning",
    "تكنولوجيا المعلومات": "Information Technology",
    "الموارد البشرية": "Human Resources",
    "خدمات الدعم": "Support Services",
    "الادارة": "Administration",
    "عمليات": "Operations",
    "التمويل والتحليل": "Finance And Analysis",
    "البحث و التطوير": "Research And Development",
    "المبيعات": "Sales",
    "تطوير الأعمال": "Business Development",
    "اعمال صيانة": "Maintenance",
    "إدارة المخاطر": "Risk Management",
    "التدقيق المحاسبي": "Accounting And Auditing"
}

PAYMENT_RATES = {
    "شهري": "Monthly",
    "سنوي": "Yearly",
    "أسبوعي": "Weekly",
    "يومي": "Daily",
    "بالساعة": "Hourly"
}


EXPERIENCE_LEVEL_YEARS_OF_EXPERIENCE_MAPPING = {
    "Entry": {"from": 0, "to": 2},
    "Intermediate": {"from": 2, "to": 5},
    "Senior": {"from": 5, "to": 10},
    "Managerial": {"from": 7, "to": 15},
    "Director": {"from": 10, "to": 20},
    "Executive": {"from": 15, "to": 20}
}
