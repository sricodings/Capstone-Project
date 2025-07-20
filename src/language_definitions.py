"""
Language Definitions for Multilingual Programming Language
Defines keywords, operators, and syntax elements for each supported language
"""

from typing import Dict, List, Any

class LanguageDefinitions:
    """Centralized language definitions and keyword mappings"""
    
    def __init__(self):
        self.languages = {
            'english': {
                'name': 'English',
                'code': 'en',
                'keywords': {
                    'if': 'if',
                    'else': 'else',
                    'while': 'while',
                    'for': 'for',
                    'function': 'function',
                    'return': 'return',
                    'var': 'var',
                    'print': 'print',
                    'input': 'input',
                    'true': 'true',
                    'false': 'false',
                    'and': 'and',
                    'or': 'or',
                    'not': 'not',
                    'break': 'break',
                    'continue': 'continue',
                    'class': 'class',
                    'import': 'import'
                },
                'description_templates': {
                    'if_statement': 'This is a conditional statement that executes code if the condition is true.',
                    'loop': 'This is a loop that repeats code multiple times.',
                    'function': 'This defines a reusable function that can be called with parameters.',
                    'variable': 'This declares a variable to store data.',
                    'print': 'This outputs text or values to the console.'
                }
            },
            'tamil': {
                'name': 'தமிழ்',
                'code': 'ta',
                'keywords': {
                    'if': 'yenil',
                    'else': 'illaiyal',
                    'while': 'varaikum',
                    'for': 'ondrumuttal',
                    'function': 'seyalpaadu',
                    'return': 'thiruppu',
                    'var': 'maari',
                    'print': 'veliyidu',
                    'input': 'ulle',
                    'true': 'unmai',
                    'false': 'poi',
                    'and': 'mattrum',
                    'or': 'allathu',
                    'not': 'alla',
                    'break': 'neekku',
                    'continue': 'thodaru',
                    'class': 'vagai',
                    'import': 'konduvaa'
                },
                'description_templates': {
                    'if_statement': 'இது ஒரு நிபந்தனை கூற்று, நிபந்தனை உண்மையாக இருந்தால் குறியீட்டை செயல்படுத்துகிறது.',
                    'loop': 'இது குறியீட்டை பல முறை மீண்டும் செய்யும் ஒரு சுழற்சி.',
                    'function': 'இது அளவுருக்களுடன் அழைக்கக்கூடிய மீண்டும் பயன்படுத்தக்கூடிய செயல்பாட்டை வரையறுக்கிறது.',
                    'variable': 'இது தரவை சேமிக்க ஒரு மாறியை அறிவிக்கிறது.',
                    'print': 'இது உரை அல்லது மதிப்புகளை கன்சோலுக்கு வெளியிடுகிறது.'
                }
            },
            'malayalam': {
                'name': 'മലയാളം',
                'code': 'ml',
                'keywords': {
                    'if': 'yendaa',
                    'else': 'allenkil',
                    'while': 'vare',
                    'for': 'vendii',
                    'function': 'pani',
                    'return': 'thiriche',
                    'var': 'madhu',
                    'print': 'parakuu',
                    'input': 'keraluu',
                    'true': 'sathyam',
                    'false': 'jhooth',
                    'and': 'koode',
                    'or': 'allenguil',
                    'not': 'alla',
                    'break': 'niruthuu',
                    'continue': 'thidaruu',
                    'class': 'jathi',
                    'import': 'konduvaru'
                },
                'description_templates': {
                    'if_statement': 'ഇത് ഒരു വ്യവസ്ഥാപിത പ്രസ്താവനയാണ്, വ്യവസ്ഥ സത്യമാണെങ്കിൽ കോഡ് നടപ്പിലാക്കുന്നു.',
                    'loop': 'ഇത് കോഡ് ഒന്നിലധികം തവണ ആവർത്തിക്കുന്ന ഒരു ലൂപ്പാണ്.',
                    'function': 'ഇത് പാരാമീറ്ററുകളുമായി വിളിക്കാവുന്ന പുനരുപയോഗിക്കാവുന്ന ഫംഗ്ഷൻ നിർവചിക്കുന്നു.',
                    'variable': 'ഇത് ഡാറ്റ സംഭരിക്കാൻ ഒരു വേരിയബിൾ പ്രഖ്യാപിക്കുന്നു.',
                    'print': 'ഇത് ടെക്സ്റ്റോ മൂല്യങ്ങളോ കൺസോളിലേക്ക് ഔട്ട്പുട്ട് ചെയ്യുന്നു.'
                }
            },
            'telugu': {
                'name': 'తెలుగు',
                'code': 'te',
                'keywords': {
                    'if': 'ayite',
                    'else': 'leda',
                    'while': 'varaku',
                    'for': 'kosam',
                    'function': 'pani',
                    'return': 'tirigi',
                    'var': 'chaala',
                    'print': 'cheppu',
                    'input': 'teesuko',
                    'true': 'nijam',
                    'false': 'abaddham',
                    'and': 'mariyu',
                    'or': 'leda',
                    'not': 'kadu',
                    'break': 'aagu',
                    'continue': 'koniyu',
                    'class': 'taram',
                    'import': 'techchuko'
                },
                'description_templates': {
                    'if_statement': 'ఇది ఒక షరతు ప్రకటన, షరతు నిజమైతే కోడ్‌ను అమలు చేస్తుంది.',
                    'loop': 'ఇది కోడ్‌ను అనేకసార్లు పునరావృతం చేసే లూప్.',
                    'function': 'ఇది పరామితులతో పిలవబడే పునర్వినియోగ ఫంక్షన్‌ను నిర్వచిస్తుంది.',
                    'variable': 'ఇది డేటాను నిల్వ చేయడానికి వేరియబల్‌ను ప్రకటిస్తుంది.',
                    'print': 'ఇది టెక్స్ట్ లేదా విలువలను కన్సోల్‌కు అవుట్‌పుట్ చేస్తుంది.'
                }
            },
            'hindi': {
                'name': 'हिन्दी',
                'code': 'hi',
                'keywords': {
                    'if': 'agar',
                    'else': 'warna',
                    'while': 'jabtak',
                    'for': 'keliye',
                    'function': 'kaam',
                    'return': 'wapas',
                    'var': 'badal',
                    'print': 'dikhaao',
                    'input': 'input',
                    'true': 'sach',
                    'false': 'jhooth',
                    'and': 'aur',
                    'or': 'ya',
                    'not': 'nahin',
                    'break': 'roko',
                    'continue': 'aage',
                    'class': 'varg',
                    'import': 'laao'
                },
                'description_templates': {
                    'if_statement': 'यह एक शर्त वाला कथन है जो शर्त सच होने पर कोड चलाता है।',
                    'loop': 'यह एक लूप है जो कोड को कई बार दोहराता है।',
                    'function': 'यह एक पुन: उपयोग योग्य फ़ंक्शन को परिभाषित करता है जिसे पैरामीटर के साथ बुलाया जा सकता है।',
                    'variable': 'यह डेटा स्टोर करने के लिए एक वेरिएबल घोषित करता है।',
                    'print': 'यह टेक्स्ट या वैल्यू को कंसोल पर आउटपुट करता है।'
                }
            },
            'sanskrit': {
                'name': 'संस्कृत',
                'code': 'sa',
                'keywords': {
                    'if': 'yadi',
                    'else': 'anya',
                    'while': 'yavat',
                    'for': 'artham',
                    'function': 'kriya',
                    'return': 'nivrit',
                    'var': 'parimaan',
                    'print': 'darshaya',
                    'input': 'grah',
                    'true': 'satyam',
                    'false': 'asatyam',
                    'and': 'cha',
                    'or': 'va',
                    'not': 'na',
                    'break': 'stambha',
                    'continue': 'chala',
                    'class': 'varga',
                    'import': 'aaharya'
                },
                'description_templates': {
                    'if_statement': 'एषा एका शर्ता वाक्या अस्ति या शर्ता सत्या भवति चेत् कोडम् चालयति।',
                    'loop': 'एषा एका आवर्तना अस्ति या कोडम् बहुवारं पुनरावृत्ति करोति।',
                    'function': 'एषा एका पुनः उपयोग योग्या क्रिया परिभाषयति या पैरामीटर सह आह्वायितुम् शक्यते।',
                    'variable': 'एषा डेटा संचयार्थं एकं परिमाणं घोषयति।',
                    'print': 'एषा पाठं वा मूल्यानि वा कन्सोले निर्गच्छति।'
                }
            }
        }
        
        # Reverse mapping for keyword lookup
        self.keyword_to_lang = {}
        for lang_code, lang_data in self.languages.items():
            for eng_keyword, local_keyword in lang_data['keywords'].items():
                if local_keyword not in self.keyword_to_lang:
                    self.keyword_to_lang[local_keyword] = {}
                self.keyword_to_lang[local_keyword][lang_code] = eng_keyword
    
    def get_language_list(self) -> List[str]:
        """Get list of supported languages"""
        return list(self.languages.keys())
    
    def get_keywords_for_language(self, language: str) -> Dict[str, str]:
        """Get keyword mapping for specific language"""
        return self.languages.get(language, {}).get('keywords', {})
    
    def get_reverse_keywords(self, language: str) -> Dict[str, str]:
        """Get reverse keyword mapping (local to English)"""
        keywords = self.get_keywords_for_language(language)
        return {v: k for k, v in keywords.items()}
    
    def translate_keyword(self, keyword: str, from_lang: str, to_lang: str) -> str:
        """Translate keyword between languages"""
        from_keywords = self.get_reverse_keywords(from_lang)
        to_keywords = self.get_keywords_for_language(to_lang)
        
        # Get English equivalent
        eng_keyword = from_keywords.get(keyword, keyword)
        
        # Get target language keyword
        return to_keywords.get(eng_keyword, keyword)
    
    def get_description_template(self, language: str, template_key: str) -> str:
        """Get description template for specific language and concept"""
        return self.languages.get(language, {}).get('description_templates', {}).get(template_key, '')
    
    def is_keyword(self, word: str, language: str) -> bool:
        """Check if word is a keyword in specified language"""
        keywords = self.get_keywords_for_language(language)
        return word in keywords.values()
    
    def get_language_name(self, language_code: str) -> str:
        """Get display name for language"""
        return self.languages.get(language_code, {}).get('name', language_code.title())