// Language definitions for the multilingual programming language
export interface LanguageDefinition {
  name: string;
  code: string;
  keywords: Record<string, string>;
  operators: Record<string, string>;
  builtins: Record<string, string>;
  messages: Record<string, string>;
}

export const LANGUAGES: Record<string, LanguageDefinition> = {
  english: {
    name: "English",
    code: "en",
    keywords: {
      if: "if",
      else: "else",
      while: "while",
      for: "for",
      function: "function",
      return: "return",
      var: "var",
      true: "true",
      false: "false",
      null: "null",
      print: "print",
      input: "input"
    },
    operators: {
      "=": "=",
      "==": "==",
      "!=": "!=",
      "<": "<",
      ">": ">",
      "<=": "<=",
      ">=": ">=",
      "+": "+",
      "-": "-",
      "*": "*",
      "/": "/",
      "%": "%",
      "&&": "&&",
      "||": "||",
      "!": "!"
    },
    builtins: {
      print: "print",
      input: "input",
      length: "length",
      type: "type"
    },
    messages: {
      welcome: "Welcome to the Multilingual Programming Environment",
      selectLanguage: "Select Programming Language",
      compile: "Compile",
      run: "Run",
      describe: "Describe Code",
      clear: "Clear",
      help: "Help",
      syntaxError: "Syntax Error",
      runtimeError: "Runtime Error",
      compilationSuccess: "Compilation Successful",
      executionComplete: "Execution Complete"
    }
  },
  tamil: {
    name: "தமிழ்",
    code: "ta",
    keywords: {
      if: "yenil",
      else: "illai",
      while: "varai",
      for: "ulla",
      function: "seyal",
      return: "thirumbu",
      var: "maari",
      true: "unmai",
      false: "poi",
      null: "ondrum_illai",
      print: "achchidu",
      input: "ulle"
    },
    operators: {
      "=": "=",
      "==": "==",
      "!=": "!=",
      "<": "<",
      ">": ">",
      "<=": "<=",
      ">=": ">=",
      "+": "+",
      "-": "-",
      "*": "*",
      "/": "/",
      "%": "%",
      "&&": "&&",
      "||": "||",
      "!": "!"
    },
    builtins: {
      print: "achchidu",
      input: "ulle",
      length: "neelam",
      type: "vaghai"
    },
    messages: {
      welcome: "பல்மொழி நிரலாக்க சூழலுக்கு வரவேற்கிறோம்",
      selectLanguage: "நிரலாக்க மொழியைத் தேர்ந்தெடுக்கவும்",
      compile: "தொகுக்கவும்",
      run: "இயக்கவும்",
      describe: "குறியீட்டை விளக்கவும்",
      clear: "அழிக்கவும்",
      help: "உதவி",
      syntaxError: "தொடரியல் பிழை",
      runtimeError: "இயக்க நேர பிழை",
      compilationSuccess: "தொகுத்தல் வெற்றிகரமாக",
      executionComplete: "செயல்பாடு முடிந்தது"
    }
  },
  malayalam: {
    name: "മലയാളം",
    code: "ml",
    keywords: {
      if: "engil",
      else: "allengil",
      while: "vare",
      for: "ulla",
      function: "pani",
      return: "thirike",
      var: "maatti",
      true: "sathyam",
      false: "asathyam",
      null: "onnum_illa",
      print: "print",
      input: "input"
    },
    operators: {
      "=": "=",
      "==": "==",
      "!=": "!=",
      "<": "<",
      ">": ">",
      "<=": "<=",
      ">=": ">=",
      "+": "+",
      "-": "-",
      "*": "*",
      "/": "/",
      "%": "%",
      "&&": "&&",
      "||": "||",
      "!": "!"
    },
    builtins: {
      print: "print",
      input: "input",
      length: "neelam",
      type: "prakaram"
    },
    messages: {
      welcome: "ബഹുഭാഷാ പ്രോഗ്രാമിംഗ് പരിതസ്ഥിതിയിലേക്ക് സ്വാഗതം",
      selectLanguage: "പ്രോഗ്രാമിംഗ് ഭാഷ തിരഞ്ഞെടുക്കുക",
      compile: "കംപൈൽ ചെയ്യുക",
      run: "പ്രവർത്തിപ്പിക്കുക",
      describe: "കോഡ് വിവരിക്കുക",
      clear: "മായ്ക്കുക",
      help: "സഹായം",
      syntaxError: "വാക്യഘടന പിശക്",
      runtimeError: "റൺടൈം പിശക്",
      compilationSuccess: "കംപൈലേഷൻ വിജയകരം",
      executionComplete: "നിർവ്വഹണം പൂർത്തിയായി"
    }
  },
  telugu: {
    name: "తెలుగు",
    code: "te",
    keywords: {
      if: "ayite",
      else: "lekapothe",
      while: "varaku",
      for: "kosam",
      function: "pani",
      return: "thirigi",
      var: "maaru",
      true: "nijam",
      false: "abaddham",
      null: "emiledu",
      print: "print",
      input: "input"
    },
    operators: {
      "=": "=",
      "==": "==",
      "!=": "!=",
      "<": "<",
      ">": ">",
      "<=": "<=",
      ">=": ">=",
      "+": "+",
      "-": "-",
      "*": "*",
      "/": "/",
      "%": "%",
      "&&": "&&",
      "||": "||",
      "!": "!"
    },
    builtins: {
      print: "print",
      input: "input",
      length: "neelam",
      type: "rakam"
    },
    messages: {
      welcome: "బహుభాషా ప్రోగ్రామింగ్ వాతావరణానికి స్వాగతం",
      selectLanguage: "ప్రోగ్రామింగ్ భాషను ఎంచుకోండి",
      compile: "కంపైల్ చేయండి",
      run: "అమలు చేయండి",
      describe: "కోడ్‌ను వివరించండి",
      clear: "క్లియర్ చేయండి",
      help: "సహాయం",
      syntaxError: "వాక్య నిర్మాణ లోపం",
      runtimeError: "రన్‌టైమ్ లోపం",
      compilationSuccess: "కంపైలేషన్ విజయవంతం",
      executionComplete: "అమలు పూర్తయింది"
    }
  },
  hindi: {
    name: "हिन्दी",
    code: "hi",
    keywords: {
      if: "agar",
      else: "nahi_to",
      while: "jab_tak",
      for: "ke_liye",
      function: "kaam",
      return: "wapas",
      var: "badal",
      true: "sach",
      false: "jhooth",
      null: "kuch_nahi",
      print: "print",
      input: "input"
    },
    operators: {
      "=": "=",
      "==": "==",
      "!=": "!=",
      "<": "<",
      ">": ">",
      "<=": "<=",
      ">=": ">=",
      "+": "+",
      "-": "-",
      "*": "*",
      "/": "/",
      "%": "%",
      "&&": "&&",
      "||": "||",
      "!": "!"
    },
    builtins: {
      print: "print",
      input: "input",
      length: "lambai",
      type: "prakar"
    },
    messages: {
      welcome: "बहुभाषी प्रोग्रामिंग वातावरण में आपका स्वागत है",
      selectLanguage: "प्रोग्रामिंग भाषा चुनें",
      compile: "कंपाइल करें",
      run: "चलाएं",
      describe: "कोड का वर्णन करें",
      clear: "साफ़ करें",
      help: "सहायता",
      syntaxError: "वाक्य रचना त्रुटि",
      runtimeError: "रनटाइम त्रुटि",
      compilationSuccess: "संकलन सफल",
      executionComplete: "निष्पादन पूर्ण"
    }
  },
  sanskrit: {
    name: "संस्कृतम्",
    code: "sa",
    keywords: {
      if: "yadi",
      else: "anya",
      while: "yavat",
      for: "artham",
      function: "karma",
      return: "nivartate",
      var: "parivartan",
      true: "satyam",
      false: "asatyam",
      null: "shunya",
      print: "print",
      input: "input"
    },
    operators: {
      "=": "=",
      "==": "==",
      "!=": "!=",
      "<": "<",
      ">": ">",
      "<=": "<=",
      ">=": ">=",
      "+": "+",
      "-": "-",
      "*": "*",
      "/": "/",
      "%": "%",
      "&&": "&&",
      "||": "||",
      "!": "!"
    },
    builtins: {
      print: "print",
      input: "input",
      length: "dirgha",
      type: "prakara"
    },
    messages: {
      welcome: "बहुभाषी प्रोग्रामन वातावरणे स्वागतम्",
      selectLanguage: "प्रोग्रामन भाषां चिनुत",
      compile: "संकलयतु",
      run: "चालयतु",
      describe: "कोडस्य वर्णनं करोतु",
      clear: "स्वच्छं करोतु",
      help: "सहायता",
      syntaxError: "वाक्य रचना दोषः",
      runtimeError: "चालन काल दोषः",
      compilationSuccess: "संकलनं सफलम्",
      executionComplete: "निष्पादनं समाप्तम्"
    }
  }
};

export const getLanguageByCode = (code: string): LanguageDefinition | undefined => {
  return LANGUAGES[code];
};

export const getAllLanguages = (): LanguageDefinition[] => {
  return Object.values(LANGUAGES);
};

export const getKeywordTranslation = (keyword: string, fromLang: string, toLang: string): string => {
  const fromLanguage = LANGUAGES[fromLang];
  const toLanguage = LANGUAGES[toLang];
  
  if (!fromLanguage || !toLanguage) return keyword;
  
  // Find the English equivalent first
  let englishKeyword = keyword;
  for (const [eng, translated] of Object.entries(fromLanguage.keywords)) {
    if (translated === keyword) {
      englishKeyword = eng;
      break;
    }
  }
  
  // Return the translation in target language
  return toLanguage.keywords[englishKeyword] || keyword;
};