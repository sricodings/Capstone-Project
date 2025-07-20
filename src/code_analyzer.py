"""
Code Analyzer and Description Generator
Provides intelligent code analysis and explanation in multiple languages
"""

from typing import List, Dict, Any, Optional
import re
from .ast_nodes import *
from .language_definitions import LanguageDefinitions

class CodeAnalyzer:
    """Analyzes code and generates descriptions in native languages"""
    
    def __init__(self):
        self.language_defs = LanguageDefinitions()
        self.current_language = 'english'
    
    def set_language(self, language: str):
        """Set the description language"""
        self.current_language = language
    
    def analyze_ast(self, ast: ProgramNode) -> Dict[str, Any]:
        """Analyze AST and return structured analysis"""
        analysis = {
            'total_statements': 0,
            'variables': set(),
            'functions': set(),
            'control_structures': [],
            'complexity_score': 0,
            'description': ''
        }
        
        self._analyze_node(ast, analysis)
        analysis['variables'] = list(analysis['variables'])
        analysis['functions'] = list(analysis['functions'])
        analysis['description'] = self._generate_description(analysis)
        
        return analysis
    
    def _analyze_node(self, node: ASTNode, analysis: Dict[str, Any]):
        """Recursively analyze AST node"""
        if isinstance(node, ProgramNode):
            analysis['total_statements'] = len(node.statements)
            for statement in node.statements:
                if statement:
                    self._analyze_node(statement, analysis)
        
        elif isinstance(node, AssignmentNode):
            analysis['variables'].add(node.identifier)
            self._analyze_node(node.expression, analysis)
        
        elif isinstance(node, IfNode):
            analysis['control_structures'].append('if')
            analysis['complexity_score'] += 2
            self._analyze_node(node.condition, analysis)
            for stmt in node.then_statements:
                if stmt:
                    self._analyze_node(stmt, analysis)
            for stmt in node.else_statements:
                if stmt:
                    self._analyze_node(stmt, analysis)
        
        elif isinstance(node, WhileNode):
            analysis['control_structures'].append('while')
            analysis['complexity_score'] += 3
            self._analyze_node(node.condition, analysis)
            for stmt in node.statements:
                if stmt:
                    self._analyze_node(stmt, analysis)
        
        elif isinstance(node, ForNode):
            analysis['control_structures'].append('for')
            analysis['complexity_score'] += 3
            analysis['variables'].add(node.variable)
            self._analyze_node(node.start, analysis)
            self._analyze_node(node.end, analysis)
            for stmt in node.statements:
                if stmt:
                    self._analyze_node(stmt, analysis)
        
        elif isinstance(node, FunctionNode):
            analysis['functions'].add(node.name)
            analysis['complexity_score'] += 5
            for param in node.parameters:
                analysis['variables'].add(param)
            for stmt in node.statements:
                if stmt:
                    self._analyze_node(stmt, analysis)
        
        elif isinstance(node, BinaryOpNode):
            analysis['complexity_score'] += 1
            self._analyze_node(node.left, analysis)
            self._analyze_node(node.right, analysis)
        
        elif isinstance(node, UnaryOpNode):
            analysis['complexity_score'] += 1
            self._analyze_node(node.operand, analysis)
        
        elif isinstance(node, FunctionCallNode):
            analysis['complexity_score'] += 2
            for arg in node.arguments:
                self._analyze_node(arg, analysis)
        
        elif isinstance(node, (PrintNode, ReturnNode, ExpressionStatementNode)):
            if hasattr(node, 'expression') and node.expression:
                self._analyze_node(node.expression, analysis)
        
        elif isinstance(node, IdentifierNode):
            analysis['variables'].add(node.name)
    
    def _generate_description(self, analysis: Dict[str, Any]) -> str:
        """Generate human-readable description in selected language"""
        lang_data = self.language_defs.languages.get(self.current_language, {})
        
        if self.current_language == 'english':
            return self._generate_english_description(analysis)
        elif self.current_language == 'tamil':
            return self._generate_tamil_description(analysis)
        elif self.current_language == 'malayalam':
            return self._generate_malayalam_description(analysis)
        elif self.current_language == 'telugu':
            return self._generate_telugu_description(analysis)
        elif self.current_language == 'hindi':
            return self._generate_hindi_description(analysis)
        elif self.current_language == 'sanskrit':
            return self._generate_sanskrit_description(analysis)
        else:
            return self._generate_english_description(analysis)
    
    def _generate_english_description(self, analysis: Dict[str, Any]) -> str:
        """Generate description in English"""
        parts = []
        
        # Basic structure
        parts.append(f"This program contains {analysis['total_statements']} statements.")
        
        # Variables
        if analysis['variables']:
            var_count = len(analysis['variables'])
            if var_count == 1:
                parts.append(f"It uses 1 variable: {', '.join(analysis['variables'])}.")
            else:
                parts.append(f"It uses {var_count} variables: {', '.join(analysis['variables'])}.")
        
        # Functions
        if analysis['functions']:
            func_count = len(analysis['functions'])
            if func_count == 1:
                parts.append(f"It defines 1 function: {', '.join(analysis['functions'])}.")
            else:
                parts.append(f"It defines {func_count} functions: {', '.join(analysis['functions'])}.")
        
        # Control structures
        if analysis['control_structures']:
            control_types = set(analysis['control_structures'])
            parts.append(f"The program uses control structures: {', '.join(control_types)}.")
        
        # Complexity
        complexity = analysis['complexity_score']
        if complexity < 5:
            parts.append("This is a simple program with low complexity.")
        elif complexity < 15:
            parts.append("This is a moderately complex program.")
        else:
            parts.append("This is a complex program with advanced logic.")
        
        return " ".join(parts)
    
    def _generate_tamil_description(self, analysis: Dict[str, Any]) -> str:
        """Generate description in Tamil"""
        parts = []
        
        parts.append(f"இந்த நிரல் {analysis['total_statements']} அறிக்கைகளை கொண்டுள்ளது.")
        
        if analysis['variables']:
            var_count = len(analysis['variables'])
            if var_count == 1:
                parts.append(f"இது 1 மாறியை பயன்படுத்துகிறது: {', '.join(analysis['variables'])}.")
            else:
                parts.append(f"இது {var_count} மாறிகளை பயன்படுத்துகிறது: {', '.join(analysis['variables'])}.")
        
        if analysis['functions']:
            func_count = len(analysis['functions'])
            if func_count == 1:
                parts.append(f"இது 1 செயல்பாட்டை வரையறுக்கிறது: {', '.join(analysis['functions'])}.")
            else:
                parts.append(f"இது {func_count} செயல்பாடுகளை வரையறுக்கிறது: {', '.join(analysis['functions'])}.")
        
        if analysis['control_structures']:
            control_types = set(analysis['control_structures'])
            parts.append(f"நிரல் கட்டுப்பாட்டு கட்டமைப்புகளை பயன்படுத்துகிறது: {', '.join(control_types)}.")
        
        complexity = analysis['complexity_score']
        if complexity < 5:
            parts.append("இது குறைந்த சிக்கலான எளிய நிரல்.")
        elif complexity < 15:
            parts.append("இது மிதமான சிக்கலான நிரல்.")
        else:
            parts.append("இது மேம்பட்ட தர்க்கத்துடன் கூடிய சிக்கலான நிரல்.")
        
        return " ".join(parts)
    
    def _generate_malayalam_description(self, analysis: Dict[str, Any]) -> str:
        """Generate description in Malayalam"""
        parts = []
        
        parts.append(f"ഈ പ്രോഗ്രാമിൽ {analysis['total_statements']} പ്രസ്താവനകൾ അടങ്ങിയിരിക്കുന്നു.")
        
        if analysis['variables']:
            var_count = len(analysis['variables'])
            if var_count == 1:
                parts.append(f"ഇത് 1 വേരിയബിൾ ഉപയോഗിക്കുന്നു: {', '.join(analysis['variables'])}.")
            else:
                parts.append(f"ഇത് {var_count} വേരിയബിളുകൾ ഉപയോഗിക്കുന്നു: {', '.join(analysis['variables'])}.")
        
        if analysis['functions']:
            func_count = len(analysis['functions'])
            if func_count == 1:
                parts.append(f"ഇത് 1 ഫംഗ്ഷൻ നിർവചിക്കുന്നു: {', '.join(analysis['functions'])}.")
            else:
                parts.append(f"ഇത് {func_count} ഫംഗ്ഷനുകൾ നിർവചിക്കുന്നു: {', '.join(analysis['functions'])}.")
        
        if analysis['control_structures']:
            control_types = set(analysis['control_structures'])
            parts.append(f"പ്രോഗ്രാം നിയന്ത്രണ ഘടനകൾ ഉപയോഗിക്കുന്നു: {', '.join(control_types)}.")
        
        complexity = analysis['complexity_score']
        if complexity < 5:
            parts.append("ഇത് കുറഞ്ഞ സങ്കീർണ്ണതയുള്ള ലളിതമായ പ്രോഗ്രാമാണ്.")
        elif complexity < 15:
            parts.append("ഇത് മിതമായ സങ്കീർണ്ണതയുള്ള പ്രോഗ്രാമാണ്.")
        else:
            parts.append("ഇത് വിപുലമായ ലോജിക്കുള്ള സങ്കീർണ്ണമായ പ്രോഗ്രാമാണ്.")
        
        return " ".join(parts)
    
    def _generate_telugu_description(self, analysis: Dict[str, Any]) -> str:
        """Generate description in Telugu"""
        parts = []
        
        parts.append(f"ఈ ప్రోగ్రామ్‌లో {analysis['total_statements']} ప్రకటనలు ఉన్నాయి.")
        
        if analysis['variables']:
            var_count = len(analysis['variables'])
            if var_count == 1:
                parts.append(f"ఇది 1 వేరియబల్‌ను ఉపయోగిస్తుంది: {', '.join(analysis['variables'])}.")
            else:
                parts.append(f"ఇది {var_count} వేరియబల్స్‌ను ఉపయోగిస్తుంది: {', '.join(analysis['variables'])}.")
        
        if analysis['functions']:
            func_count = len(analysis['functions'])
            if func_count == 1:
                parts.append(f"ఇది 1 ఫంక్షన్‌ను నిర్వచిస్తుంది: {', '.join(analysis['functions'])}.")
            else:
                parts.append(f"ఇది {func_count} ఫంక్షన్లను నిర్వచిస్తుంది: {', '.join(analysis['functions'])}.")
        
        if analysis['control_structures']:
            control_types = set(analysis['control_structures'])
            parts.append(f"ప్రోగ్రామ్ నియంత్రణ నిర్మాణాలను ఉపయోగిస్తుంది: {', '.join(control_types)}.")
        
        complexity = analysis['complexity_score']
        if complexity < 5:
            parts.append("ఇది తక్కువ సంక్లిష్టతతో కూడిన సరళమైన ప్రోగ్రామ్.")
        elif complexity < 15:
            parts.append("ఇది మధ్యస్థ సంక్లిష్టతతో కూడిన ప్రోగ్రామ్.")
        else:
            parts.append("ఇది అధునాతన లాజిక్‌తో కూడిన సంక్లిష్టమైన ప్రోగ్రామ్.")
        
        return " ".join(parts)
    
    def _generate_hindi_description(self, analysis: Dict[str, Any]) -> str:
        """Generate description in Hindi"""
        parts = []
        
        parts.append(f"इस प्रोग्राम में {analysis['total_statements']} कथन हैं।")
        
        if analysis['variables']:
            var_count = len(analysis['variables'])
            if var_count == 1:
                parts.append(f"यह 1 वेरिएबल का उपयोग करता है: {', '.join(analysis['variables'])}।")
            else:
                parts.append(f"यह {var_count} वेरिएबल्स का उपयोग करता है: {', '.join(analysis['variables'])}।")
        
        if analysis['functions']:
            func_count = len(analysis['functions'])
            if func_count == 1:
                parts.append(f"यह 1 फ़ंक्शन को परिभाषित करता है: {', '.join(analysis['functions'])}।")
            else:
                parts.append(f"यह {func_count} फ़ंक्शन्स को परिभाषित करता है: {', '.join(analysis['functions'])}।")
        
        if analysis['control_structures']:
            control_types = set(analysis['control_structures'])
            parts.append(f"प्रोग्राम नियंत्रण संरचनाओं का उपयोग करता है: {', '.join(control_types)}।")
        
        complexity = analysis['complexity_score']
        if complexity < 5:
            parts.append("यह कम जटिलता वाला सरल प्रोग्राम है।")
        elif complexity < 15:
            parts.append("यह मध्यम जटिलता वाला प्रोग्राम है।")
        else:
            parts.append("यह उन्नत तर्क के साथ जटिल प्रोग्राम है।")
        
        return " ".join(parts)
    
    def _generate_sanskrit_description(self, analysis: Dict[str, Any]) -> str:
        """Generate description in Sanskrit"""
        parts = []
        
        parts.append(f"अस्मिन् कार्यक्रमे {analysis['total_statements']} वाक्यानि सन्ति।")
        
        if analysis['variables']:
            var_count = len(analysis['variables'])
            if var_count == 1:
                parts.append(f"एतत् 1 परिमाणस्य उपयोगं करोति: {', '.join(analysis['variables'])}।")
            else:
                parts.append(f"एतत् {var_count} परिमाणानाम् उपयोगं करोति: {', '.join(analysis['variables'])}।")
        
        if analysis['functions']:
            func_count = len(analysis['functions'])
            if func_count == 1:
                parts.append(f"एतत् 1 क्रियाम् परिभाषयति: {', '.join(analysis['functions'])}।")
            else:
                parts.append(f"एतत् {func_count} क्रियाः परिभाषयति: {', '.join(analysis['functions'])}।")
        
        if analysis['control_structures']:
            control_types = set(analysis['control_structures'])
            parts.append(f"कार्यक्रमः नियन्त्रण संरचनानाम् उपयोगं करोति: {', '.join(control_types)}।")
        
        complexity = analysis['complexity_score']
        if complexity < 5:
            parts.append("एतत् न्यून जटिलतायाः सरलं कार्यक्रमम् अस्ति।")
        elif complexity < 15:
            parts.append("एतत् मध्यम जटिलतायाः कार्यक्रमम् अस्ति।")
        else:
            parts.append("एतत् उन्नत तर्कयुक्तं जटिलं कार्यक्रमम् अस्ति।")
        
        return " ".join(parts)
    
    def analyze_code_string(self, code: str) -> Dict[str, Any]:
        """Analyze raw code string and provide insights"""
        analysis = {
            'lines': len(code.split('\n')),
            'characters': len(code),
            'keywords_used': [],
            'estimated_complexity': 'Low',
            'potential_issues': [],
            'suggestions': []
        }
        
        # Find keywords
        keywords = self.language_defs.get_keywords_for_language(self.current_language)
        for keyword in keywords.values():
            if keyword in code:
                analysis['keywords_used'].append(keyword)
        
        # Estimate complexity
        keyword_count = len(analysis['keywords_used'])
        if keyword_count > 10:
            analysis['estimated_complexity'] = 'High'
        elif keyword_count > 5:
            analysis['estimated_complexity'] = 'Medium'
        
        # Basic issue detection
        if 'while' in analysis['keywords_used'] and 'break' not in analysis['keywords_used']:
            analysis['potential_issues'].append('Potential infinite loop detected')
        
        if analysis['lines'] > 50:
            analysis['suggestions'].append('Consider breaking large programs into functions')
        
        return analysis