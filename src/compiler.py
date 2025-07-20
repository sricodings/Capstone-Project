"""
Main Compiler Class
Integrates lexer, parser, and bytecode generator
"""

from typing import Optional, List, Dict, Any
from .lexer import MultilingualLexer
from .parser import MultilingualParser
from .bytecode_generator import BytecodeGenerator
from .virtual_machine import VirtualMachine
from .code_analyzer import CodeAnalyzer
from .language_definitions import LanguageDefinitions

class CompilerError(Exception):
    """Compiler-specific error"""
    pass

class MultilingualCompiler:
    """Main compiler class integrating all components"""
    
    def __init__(self, language: str = 'english'):
        self.current_language = language
        self.language_defs = LanguageDefinitions()
        self.lexer = MultilingualLexer(language)
        self.parser = MultilingualParser(language)
        self.bytecode_gen = BytecodeGenerator()
        self.vm = VirtualMachine()
        self.analyzer = CodeAnalyzer()
        self.analyzer.set_language(language)
        
        self.last_ast = None
        self.last_bytecode = None
        self.last_constants = None
    
    def change_language(self, new_language: str):
        """Change compiler language"""
        if new_language not in self.language_defs.get_language_list():
            raise CompilerError(f"Unsupported language: {new_language}")
        
        self.current_language = new_language
        self.lexer.change_language(new_language)
        self.parser.change_language(new_language)
        self.analyzer.set_language(new_language)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.language_defs.get_language_list()
    
    def get_language_display_name(self, language_code: str) -> str:
        """Get display name for language"""
        return self.language_defs.get_language_name(language_code)
    
    def get_keywords_for_current_language(self) -> Dict[str, str]:
        """Get keywords for current language"""
        return self.language_defs.get_keywords_for_language(self.current_language)
    
    def get_syntax_highlighting_rules(self) -> Dict[str, List[str]]:
        """Get syntax highlighting rules for current language"""
        return self.lexer.get_syntax_highlighting_rules()
    
    def tokenize(self, code: str) -> List[Dict[str, Any]]:
        """Tokenize code"""
        try:
            return self.lexer.tokenize(code)
        except Exception as e:
            raise CompilerError(f"Tokenization error: {e}")
    
    def parse(self, code: str):
        """Parse code and return AST"""
        try:
            ast = self.parser.parse(code)
            if ast is None:
                raise CompilerError("Failed to parse code")
            self.last_ast = ast
            return ast
        except Exception as e:
            raise CompilerError(f"Parse error: {e}")
    
    def compile_to_bytecode(self, code: str) -> List:
        """Compile code to bytecode"""
        try:
            # Parse code
            ast = self.parse(code)
            
            # Generate bytecode
            instructions = self.bytecode_gen.generate(ast)
            constants = self.bytecode_gen.constants
            
            self.last_bytecode = instructions
            self.last_constants = constants
            
            return instructions
        except Exception as e:
            raise CompilerError(f"Compilation error: {e}")
    
    def execute(self, code: str, input_data: List[str] = None) -> Dict[str, Any]:
        """Compile and execute code"""
        try:
            # Compile to bytecode
            instructions = self.compile_to_bytecode(code)
            
            # Load into VM
            self.vm.load_bytecode(instructions, self.last_constants)
            
            # Set input if provided
            if input_data:
                self.vm.set_input(input_data)
            
            # Execute
            self.vm.execute()
            
            # Return results
            return {
                'success': True,
                'output': self.vm.get_output(),
                'error': None,
                'bytecode': instructions,
                'constants': self.last_constants
            }
        
        except Exception as e:
            return {
                'success': False,
                'output': [],
                'error': str(e),
                'bytecode': None,
                'constants': None
            }
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code and generate description"""
        try:
            # Try to parse for detailed analysis
            ast = self.parse(code)
            if ast:
                return self.analyzer.analyze_ast(ast)
            else:
                # Fallback to string analysis
                return self.analyzer.analyze_code_string(code)
        except:
            # Fallback to string analysis
            return self.analyzer.analyze_code_string(code)
    
    def get_bytecode_listing(self) -> str:
        """Get human-readable bytecode listing"""
        if self.last_bytecode is None:
            return "No bytecode generated yet"
        return self.bytecode_gen.get_bytecode_listing()
    
    def translate_code(self, code: str, target_language: str) -> str:
        """Translate code from current language to target language"""
        try:
            # Tokenize in current language
            tokens = self.tokenize(code)
            
            # Translate keywords
            translated_code = code
            current_keywords = self.language_defs.get_keywords_for_language(self.current_language)
            target_keywords = self.language_defs.get_keywords_for_language(target_language)
            
            # Reverse mapping for current language
            current_reverse = {v: k for k, v in current_keywords.items()}
            
            # Replace keywords
            for token in tokens:
                if token['type'] != 'IDENTIFIER':
                    continue
                
                token_value = token['value']
                if token_value in current_reverse:
                    english_keyword = current_reverse[token_value]
                    target_keyword = target_keywords.get(english_keyword, token_value)
                    translated_code = translated_code.replace(token_value, target_keyword)
            
            return translated_code
        
        except Exception as e:
            raise CompilerError(f"Translation error: {e}")
    
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate code syntax"""
        try:
            ast = self.parse(code)
            return {
                'valid': True,
                'errors': [],
                'warnings': []
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [str(e)],
                'warnings': []
            }
    
    def get_help_text(self) -> str:
        """Get help text in current language"""
        keywords = self.get_keywords_for_current_language()
        lang_name = self.get_language_display_name(self.current_language)
        
        help_sections = []
        help_sections.append(f"=== {lang_name} Programming Language Help ===\n")
        
        help_sections.append("Keywords:")
        for eng, local in keywords.items():
            help_sections.append(f"  {eng} -> {local}")
        
        help_sections.append("\nBasic Syntax Examples:")
        if self.current_language == 'english':
            help_sections.append("  var x = 10")
            help_sections.append("  if x > 5:")
            help_sections.append("    print \"Greater than 5\"")
            help_sections.append("  function greet(name):")
            help_sections.append("    print \"Hello \" + name")
        elif self.current_language == 'tamil':
            help_sections.append("  maari x = 10")
            help_sections.append("  yenil x > 5:")
            help_sections.append("    veliyidu \"5 vida periyathu\"")
            help_sections.append("  seyalpaadu vanakkam(peyar):")
            help_sections.append("    veliyidu \"Vanakkam \" + peyar")
        
        return "\n".join(help_sections)