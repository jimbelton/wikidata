# -*- coding: utf-8 -*-
# All language names have had the words characters, languages and language removed and all remaining words capitalized
# 1. The list of languages in ISO 639-1 is from the standard: http://www.loc.gov/standards/iso639-2/
# 2. The list of languages in wikidata was taken from the 'original language of work' properties of all books in the dump from
#    20160215, and may not be complete.

# These are the primary language names and their codes from ISO 639-1, or in rare cases, from ISO 639-2
#
nameToIso639Id = {
    "Abkhazian":            "ab",
    "Afar":                 "aa",
    "Afrikaans":            "af",    # Found in wikidata
    "Akan":                 "ak",
    "Albanian":             "sq",
    "Algonquian":           "alg",   # No similar language in ISO 639-1
    "Amharic":              "am",    # Found in wikidata
    "Ancient Greek":        "grc",   # Found in wikidata
    "Arabic":               "ar",    # Found in wikidata
    "Aragonese":            "an",    # Found in wikidata
    "Aramaic":              "arc",   # Found in wikidata
    "Armenian":             "hy",    # Found in wikidata
    "Assamese":             "as",    # Found in wikidata
    "Avaric":               "av",
    "Avestan":              "ae",
    "Awadhi":               "awa",   # Found in wikidata
    "Aymara":               "ay",
    "Azerbaijani":          "az",    # Found in wikidata
    "Bambara":              "bm",
    "Bantu":                "bnt",   # No similar language in ISO 639-1
    "Bashkir":              "ba",
    "Basque":               "eu",    # Found in wikidata
    "Belarusian":           "be",    # Found in wikidata
    "Bengali":              "bn",    # Found in wikidata
    "Berber":               "ber",   # No similar language in ISO 639-1
    "Bihari":               "bh",
    "Bislama":              "bi",
    "Bosnian":              "bs",    # Found in wikidata
    "Breton":               "br",    # Found in wikidata
    "Bulgarian":            "bg",    # Found in wikidata
    "Burmese":              "my",    # Found in wikidata
    "Catalan":              "ca",    # Found in wikidata
    "Central Khmer":        "km",
    "Chamorro":             "ch",
    "Chechen":              "ce",
    "Chichewa":             "ny",
    "Chinese":              "zh",    # Found in wikidata
    "Chuvash":              "cv",
    "Cornish":              "kw",
    "Corsican":             "co",
    "Cree":                 "cr",
    "Croatian":             "hr",    # Found in wikidata
    "Czech":                "cs",    # Found in wikidata
    "Danish":               "da",    # Found in wikidata
    "Divehi":               "dv",
    "Dutch":                "nl",    # Found in wikidata
    "Dzongkha":             "dz",
    "English":              "en",
    "Esperanto":            "eo",    # Found in wikidata
    "Estonian":             "et",    # Found in wikidata
    "Ewe":                  "ee",
    "Faroese":              "fo",    # Found in wikidata
    "Fijian":               "fj",
    "Filipino":             "fil",   # Found in wikidata
    "Finnish":              "fi",    # Found in wikidata
    "French":               "fr",    # Found in wikidata
    "Fulah":                "ff",
    "Galician":             "gl",    # Found in wikidata
    "Ganda":                "lg",
    "Georgian":             "ka",    # Found in wikidata
    "German":               "de",    # Found in wikidata
    "Greek":                "el",    # Found in wikidata
    "Guaraní":              "gn",
    "Gujarati":             "gu",    # Found in wikidata
    "Haitian":              "ht",
    "Hausa":                "ha",
    "Hawaiian":             "haw",   # No similar language in ISO 639-1
    "Hebrew":               "he",    # Found in wikidata
    "Herero":               "hz",
    "Hindi":                "hi",    # Found in wikidata
    "Hiri Motu":            "ho",
    "Hmong":                "hmn",   # Found in wikidata
    "Hungarian":            "hu",    # Found in wikidata
    "Icelandic":            "is",    # Found in wikidata
    "Ido":                  "io",
    "Igbo":                 "ig",
    "Indonesian":           "id",    # Found in wikidata
    "Interlingua":          "ia",
    "Interlingue":          "ie",
    "Inupiaq":              "ik",
    "Irish":                "ga",    # Found in wikidata
    "Italian":              "it",    # Found in wikidata
    "Inuktitut":            "iu",
    "Japanese":             "ja",    # Found in wikidata
    "Javanese":             "jv",
    "Judeo-Arabic":         "jrb",   # Found in wikidata
    "Kalaallisut":          "kl",
    "Kannada":              "kn",    # Found in wikidata
    "Kanuri":               "kr",
    "Karelian":             "krl",   # Found in wikidata
    "Kashubian":            "csb",   # Found in wikidata
    "Kashmiri":             "ks",
    "Kazakh":               "kk",
    "Kikuyu":               "ki",
    "Kinyarwanda":          "rw",
    "Kirundi":              "rn",
    "Komi":                 "kv",
    "Kongo":                "kg",
    "Konkani":              "kok",   # Found in wikidata
    "Korean":               "ko",    # Found in wikidata
    "Kurdish":              "ku",
    "Kwanyama":             "kj",
    "Kyrgyz":               "ky",
    "Ladino":               "lad",   # Found in wikidata
    "Latin":                "la",    # Found in wikidata
    "Latvian":              "lv",
    "Luxembourgish":        "lb",
    "Limburgish":           "li",
    "Lingala":              "ln",
    "Lao":                  "lo",
    "Lithuanian":           "lt",    # Found in wikidata
    "Luba-Katanga":         "lu",
    "Manx":                 "gv",
    "Macedonian":           "mk",    # Found in wikidata
    "Malagasy":             "mg",
    "Malay":                "ms",    # Found in wikidata
    "Malayalam":            "ml",    # Found in wikidata
    "Maltese":              "mt",
    "Manx":                 "gv",
    "Maori":                "mi",
    "Marathi":              "mr",    # Found in wikidata
    "Marshallese":          "mh",
    "Mayan":                "myn",   # No similar language in ISO 639-1
    "Mongolian":            "mn",
    "Nahuatl":              "nah",   # Found in wikidata. No similar language in ISO 639-1
    "Nauru":                "na",
    "Navajo":               "nv",
    "Ndonga":               "ng",
    "Neapolitan":           "nap",   # Found in wikidata
    "Nepali":               "ne",    # Found in wikidata
    "North Ndebele":        "nd",
    "Northern Sami":        "se",
    "Norwegian":            "no",    # Found in wikidata
    "Norwegian Bokmål":     "nb",
    "Norwegian Nynorsk":    "nn",
    "Nuosu":                "ii",
    "Southern Ndebele":     "nr",
    "Occitan":              "oc",    # Found in wikidata
    "Ojibwe":               "oj",
    "Old Church Slavonic":  "cu",    # Found in wikidata
    "Old Norse":            "non",   # Found in wikidata
    "Oriya":                "or",
    "Oromo":                "om",
    "Ossetian":             "os",
    "Pali":                 "pi",    # Found in wikidata
    "Pashto":               "ps",
    "Persian":              "fa",    # Found in wikidata
    "Polish":               "pl",    # Found in wikidata
    "Portuguese":           "pt",    # Found in wikidata
    "Prakrit":              "pra",   # Found in wikidata
    "Punjabi":              "pa",    # Found in wikidata
    "Quechua":              "qu",
    "Romansh":              "rm",    # Found in wikidata
    "Romanian":             "ro",    # Found in wikidata
    "Rundi":                "rn",
    "Russian":              "ru",    # Found in wikidata
    "Samoan":               "sm",
    "Sango":                "sg",
    "Sanskrit":             "sa",    # Found in wikidata
    "Sardinian":            "sc",
    "Scottish Gaelic":      "gd",    # Found in wikidata
    "Serbian":              "sr",    # Found in wikidata
    "Shona":                "sn",
    "Sicilian":             "scn",   # Found in wikidata
    "Sindhi":               "sd",    # Found in wikidata
    "Sinhala":              "si",    # Found in wikidata
    "Slovak":               "sk",    # Found in wikidata
    "Slovenian":            "sl",    # Found in wikidata
    "Somali":               "so",
    "South Ndebele":        "nr",
    "Southern Sotho":       "st",
    "Spanish":              "es",    # Found in wikidata
    "Sundanese":            "su",
    "Swahili":              "sw",
    "Swati":                "ss",
    "Swedish":              "sv",    # Found in wikidata
    "Tagalog":              "tl",    # Found in wikidata
    "Tahitian":             "ty",
    "Tajik":                "tg",
    "Tamil":                "ta",    # Found in wikidata
    "Tatar":                "tt",
    "Telugu":               "te",    # Found in wikidata
    "Tajik":                "tg",
    "Thai":                 "th",    # Found in wikidata
    "Tigrinya":             "ti",
    "Tibetan":              "bo",
    "Tswana":               "tn",
    "Tonga":                "to",
    "Tsonga":               "ts",
    "Tswana":               "tn",
    "Turkish":              "tr",    # Found in wikidata
    "Turkmen":              "tk",
    "Tsonga":               "ts",
    "Tatar":                "tt",
    "Twi":                  "tw",
    "Tahitian":             "ty",
    "Uyghur":               "ug",
    "Ukrainian":            "uk",    # Found in wikidata
    "Urdu":                 "ur",    # Found in wikidata
    "Uzbek":                "uz",
    "Venda":                "ve",
    "Vietnamese":           "vi",    # Found in wikidata
    "Volapük":              "vo",
    "Walloon":              "wa",
    "Welsh":                "cy",    # Found in wikidata
    "Wolof":                "wo",
    "Western Frisian":      "fy",
    "Xhosa":                "xh",
    "Yiddish":              "yi",    # Found in wikidata
    "Yoruba":               "yo",
    "Zhuang":               "za",
    "Zulu":                 "zu"
}

# These are aliases from ISO 639-1 and wikidata, and the closest ISO 639-1 codes (or, in a few cases, 639-2 codes). The wikidata
# language aliases have been forced to the nearest 639-1 code whereever possible, with comments indicating that there is a better
# fit in 639-2 if that is the case. This was done to keep the number of lanaguage codes to a minimum, but it means (for example)
# that all Aryan languages map to "hi" (Hindi)
#
aliasToIso639Id = {
    "American English":                 "en",    # From wikidata
    "Australian English":               "en",    # From wikidata
    "Austrian German":                  "de",    # From wikidata
    "Bangla":                           "bn",
    "Bhojpuri":                         "bh",
    "Bokm\u00e5l":                      "nb",    # From wikidata
    "Brazil":                           "pt",    # From wikidata
    "Brazil Portuguese":                "pt",    # From wikidata
    "Brazilian Portuguese":             "pt",    # From wikidata
    "British English":                  "en",    # From wikidata
    "Burgundian":                       "de",    # From wikidata: Similar to Gothic, which has its own code in ISO 639-2, "got"
    "Canadian English":                 "en",    # From wikidata
    "Castilian":                        "es",
    "Catal\u00e1n":                     "ca",    # From wikidata
    "Central":                          "bo",
    "Chewa":                            "ny",
    "Chuang":                           "za",
    "Church Slavic":                    "cu",
    "Church Slavonic":                  "cu",    # From ISO 639-1, found in wikidata
    "Classical Armenian":               "hy",    # From wikidata
    "Classical Chinese":                "zh",    # From wikidata
    "Classical Nahuatl":                "nah",   # From wikidata
    "Common Brittonic":                 "br",    # From wikidata
    "Dhivehi":                          "dv",
    "Early Modern English":             "en",    # From wikidata
    "Early Modern Spanish":             "es",    # From wikidata
    "Early New High German":            "de",    # From wikidata
    "Egyptian Arabic":                  "ar",    # From wikidata
    "Farsi":                            "fa",
    "Flemish":                          "nl",    # From ISO 639-2, found in wikidata
    "France":                           "fr",    # From wikidata
    "Fulah":                            "ff",
    "Gaelic":                           "gd",
    "Geordie Dialect":                  "en",    # From wikidata
    "Gikuyu":                           "ki",
    "Greenlandic":                      "kl",
    "Haitian Creole":                   "ht",
    "Hawaiian Pidgin":                  "haw",   # From wikidata
    "Hiberno-English":                  "en",    # From wikidata
    "Indian English":                   "en",    # From wikidata
    "Italiano Moderno":                 "it",    # From wikidata
    "Kalaallisut":                      "kl",
    "Kanbun":                           "ja",    # From wikidata. Annotated Classical Chinese that can be read in Japanese
    "Katharevousa":                     "el",    # From wikidata
    "Kerewe":                           "bnt",   # From wikidata. No similar in ISO 639-1. A Bantu language: "bnt" from ISO 639-2
    "Khmer":                            "km",    # From in wikidata
    "Kirghiz":                          "ky",
    "Koine Greek":                      "el",    # From wikidata
    "Kuanyama":                         "kj",
    "Late Old Japanese":                "ja",    # From wikidata
    "Letzeburgesch":                    "lb",
    "Limburgan":                        "li",
    "Limburger":                        "li",
    "Luganda":                          "lg",
    "Magahi":                           "bh",
    "Maghrebi Arabic":                  "ar",    # From wikidata
    "Maithili":                         "bh",    # From ISO 639-1. Found in wikidata
    "Malaysian":                        "ms",    # From wikidata
    "Malay Trade And Creole":           "ms",    # From wikidata
    "Maldivian":                        "dv",
    "Mandarin Chinese":                 "zh",    # From wikidata
    "Manglish":                         "en",    # From wikidata
    "Massachusett":                     "alg",   # From wikidata. No similar in ISO 639-1. An Algonquian language: "alg" ISO 639-2
    "Medieval Latin":                   "la",    # From wikidata
    "Middle English":                   "en",    # From wikidata. Middle English has its own code in ISO 639-2, "enm"
    "Middle French":                    "fr",    # From wikidata. Middle French has its own code in ISO 639-2, "frm"
    "Mittelalterliches Aragonesisch":   "an",    # From wikidata
    "Modern Greek":                     "el",    # From wikidata
    "Moldavian":                        "ro",
    "Moldovan":                         "ro",
    "Mon":                              "km",    # From wikidata. Mon-Khnmer languages have there own code in ISO 639-2, "mkh"
    "Navaho":                           "nv",
    "Netherlands":                      "nl",    # From wikidata
    "Nyanja":                           "ny",
    "Nynorsk":                          "nn",    # From wikidata
    "Occidental":                       "ie",
    "Odia":                             "hi",    # From wikidata
    "Ojibwa":                           "oj",
    "Old Bulgarian":                    "cu",
    "Old Chinese":                      "zh",    # From wikidata
    "Old East Slavic":                  "cu",    # From wikidata
    "Old French":                       "fr",    # From wikidata. Old French has its own code in ISO 639-2, "fro"
    "Old Slavonic":                     "cu",
    "Old Spanish":                      "es",    # From wikidata.
    "Ossetic":                          "os",
    "Ossetic":                          "os",
    "Panjabi":                          "pa",
    "Pulaar":                           "ff",
    "Pular":                            "ff",
    "Pushto":                           "ps",
    "Quebec French":                    "fr",    # From wikidata
    "Radical Bokm\u00e5l":              "nb",    # From wikidata
    "Ruthenian":                        "cu",    # From wikidata
    "Scots":                            "gd",    # From wikidata
    "Scottish English":                 "en",    # From wikidata
    "Serbo-Croatian":                   "sr",    # From wikidata
    "Shan":                             "th",    # From wikidata. Tai languages have there own code in ISO 639-2, "tai"
    "Sichuan Yi":                       "ii",
    "Sinhalese":                        "si",
    "Slovene":                          "sl",    # From in wikidata
    "Spanish In The Philippines":       "es",    # From wikidata
    "Standard Chinese":                 "zh",    # From wikidata
    "Taglish":                          "en",    # From wikidata. English words with Tagalog syntax
    "Tuareg":                           "ber",   # From wikidata. No similar in ISO 639-1. A Berber language: "ber" from ISO 639-2
    "Tibetan Standard":                 "bo",
    "Traditional Chinese":              "zh",    # From wikidata
    "Uighur":                           "ug",
    "Valencian":                        "ca",    # From wikidata
    "Western Armenian":                 "hy",    # From wikidata
    "Written Vernacular Chinese":       "zh",    # From wikidata
    "Yucatec Maya":                     "myn"    # From wikidata; no similar language in ISO 639-1. "myn" is from ISO 639-2
}

iso639IdToName = None    # Constructed on the first call to isoIdToName

def nameToIsoId(name):
    words = name.split(" ")

    for i in reversed(range(len(words))):
        if words[i] == "characters" or words[i] == "language" or words[i] == "languages":
            del words[i]
            continue

        words[i] = words[i][0].upper() + words[i][1:]

    name = " ".join(words)

    if name in nameToIso639Id:
        return nameToIso639Id[name]

    if name in aliasToIso639Id:
        return aliasToIso639Id[name]

    raise KeyError(name)

def isoIdToName(isoId):
    global iso639IdToName

    if not iso639IdToName:
        iso639IdToName = {}

        for name in nameToIso639Id:
            iso639IdToName[nameToIso639Id[name]] = name

    if isoId in iso639IdToName:
        return iso639IdToName[isoId]

    raise KeyError(isoId)
