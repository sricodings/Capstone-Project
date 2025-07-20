"""
Test cases for the Multilingual Compiler
Comprehensive testing for all language features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from compiler import MultilingualCompiler, CompilerError

class TestMultilingualCompiler(unittest.TestCase):
    """Test cases for multilingual compiler functionality"""
    
    def setUp(self):
        """Set up test compiler instance"""
        self.compiler = MultilingualCompiler()
    
    def test_language_switching(self):
        """Test switching between languages"""
        # Test initial language
        self.assertEqual(self.compiler.current_language, 'english')
        
        # Test language switching
        self.compiler.change_language('tamil')
        self.assertEqual(self.compiler.current_language, 'tamil')
        
        # Test invalid language
        with self.assertRaises(CompilerError):
            self.compiler.change_language('invalid_language')
    
    def test_english_compilation(self):
        """Test compilation in English"""
        self.compiler.change_language('english')
        
        code = '''
var x = 10
if x > 5:
    print "Greater than 5"
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['Greater than 5'])
    
    def test_tamil_compilation(self):
        """Test compilation in Tamil"""
        self.compiler.change_language('tamil')
        
        code = '''
maari x = 10
yenil x > 5:
    veliyidu "5 vida periyathu"
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['5 vida periyathu'])
    
    def test_hindi_compilation(self):
        """Test compilation in Hindi"""
        self.compiler.change_language('hindi')
        
        code = '''
badal x = 10
agar x > 5:
    dikhaao "5 se zyada"
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['5 se zyada'])
    
    def test_function_definition_and_call(self):
        """Test function definition and calling"""
        self.compiler.change_language('english')
        
        code = '''
function greet(name):
    print "Hello " + name
    return true

var result = greet("World")
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['Hello World'])
    
    def test_loop_execution(self):
        """Test loop execution"""
        self.compiler.change_language('english')
        
        code = '''
var i = 1
while i <= 3:
    print i
    var i = i + 1
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['1', '2', '3'])
    
    def test_for_loop(self):
        """Test for loop execution"""
        self.compiler.change_language('english')
        
        code = '''
for i = 1: 3:
    print i
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['1', '2', '3'])
    
    def test_arithmetic_operations(self):
        """Test arithmetic operations"""
        self.compiler.change_language('english')
        
        code = '''
var a = 10
var b = 5
print a + b
print a - b
print a * b
print a / b
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['15', '5', '50', '2.0'])
    
    def test_comparison_operations(self):
        """Test comparison operations"""
        self.compiler.change_language('english')
        
        code = '''
var x = 10
print x == 10
print x != 5
print x > 5
print x < 15
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['True', 'True', 'True', 'True'])
    
    def test_logical_operations(self):
        """Test logical operations"""
        self.compiler.change_language('english')
        
        code = '''
var a = true
var b = false
print a and b
print a or b
print not b
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['False', 'True', 'True'])
    
    def test_nested_conditions(self):
        """Test nested if conditions"""
        self.compiler.change_language('english')
        
        code = '''
var x = 15
if x > 10:
    if x > 20:
        print "Very large"
    else:
        print "Medium"
else:
    print "Small"
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['Medium'])
    
    def test_error_handling(self):
        """Test error handling"""
        # Test undefined variable
        code = '''
print unknown_variable
'''
        
        result = self.compiler.execute(code)
        self.assertFalse(result['success'])
        self.assertIn('not defined', result['error'])
    
    def test_division_by_zero(self):
        """Test division by zero error"""
        self.compiler.change_language('english')
        
        code = '''
var x = 10
var y = 0
print x / y
'''
        
        result = self.compiler.execute(code)
        self.assertFalse(result['success'])
        self.assertIn('Division by zero', result['error'])
    
    def test_code_analysis(self):
        """Test code analysis functionality"""
        self.compiler.change_language('english')
        
        code = '''
var x = 10
if x > 5:
    print "Hello"
function test():
    return true
'''
        
        analysis = self.compiler.analyze_code(code)
        
        self.assertGreater(analysis['total_statements'], 0)
        self.assertIn('x', analysis['variables'])
        self.assertIn('test', analysis['functions'])
        self.assertIn('if', analysis['control_structures'])
        self.assertIsInstance(analysis['description'], str)
        self.assertGreater(len(analysis['description']), 0)
    
    def test_bytecode_generation(self):
        """Test bytecode generation"""
        self.compiler.change_language('english')
        
        code = '''
var x = 10
print x
'''
        
        instructions = self.compiler.compile_to_bytecode(code)
        self.assertIsInstance(instructions, list)
        self.assertGreater(len(instructions), 0)
        
        # Check for expected instructions
        opcodes = [instr.opcode for instr in instructions]
        self.assertIn('LOAD_CONST', opcodes)
        self.assertIn('STORE_VAR', opcodes)
        self.assertIn('PRINT', opcodes)
        self.assertIn('HALT', opcodes)
    
    def test_syntax_validation(self):
        """Test syntax validation"""
        # Valid syntax
        valid_code = '''
var x = 10
print x
'''
        
        validation = self.compiler.validate_syntax(valid_code)
        self.assertTrue(validation['valid'])
        self.assertEqual(len(validation['errors']), 0)
        
        # Invalid syntax
        invalid_code = '''
var x = 
print x
'''
        
        validation = self.compiler.validate_syntax(invalid_code)
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['errors']), 0)
    
    def test_multilingual_equivalence(self):
        """Test that equivalent programs in different languages produce same results"""
        # English version
        self.compiler.change_language('english')
        english_code = '''
var x = 5
if x > 3:
    print "Success"
'''
        english_result = self.compiler.execute(english_code)
        
        # Tamil version
        self.compiler.change_language('tamil')
        tamil_code = '''
maari x = 5
yenil x > 3:
    veliyidu "Success"
'''
        tamil_result = self.compiler.execute(tamil_code)
        
        # Should produce same output
        self.assertTrue(english_result['success'])
        self.assertTrue(tamil_result['success'])
        self.assertEqual(english_result['output'], tamil_result['output'])
    
    def test_function_with_parameters(self):
        """Test function with multiple parameters"""
        self.compiler.change_language('english')
        
        code = '''
function add(a, b):
    return a + b

var result = add(5, 3)
print result
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['8'])
    
    def test_recursive_function(self):
        """Test recursive function"""
        self.compiler.change_language('english')
        
        code = '''
function factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

var result = factorial(4)
print result
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        self.assertEqual(result['output'], ['24'])
    
    def test_complex_program(self):
        """Test complex program with multiple features"""
        self.compiler.change_language('english')
        
        code = '''
function fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

var i = 0
while i < 5:
    var fib_num = fibonacci(i)
    print "Fib(" + i + ") = " + fib_num
    var i = i + 1
'''
        
        result = self.compiler.execute(code)
        self.assertTrue(result['success'])
        expected_output = [
            'Fib(0) = 0',
            'Fib(1) = 1', 
            'Fib(2) = 1',
            'Fib(3) = 2',
            'Fib(4) = 3'
        ]
        self.assertEqual(result['output'], expected_output)


class TestLanguageSpecificFeatures(unittest.TestCase):
    """Test language-specific features and edge cases"""
    
    def setUp(self):
        self.compiler = MultilingualCompiler()
    
    def test_all_supported_languages(self):
        """Test basic functionality in all supported languages"""
        test_cases = {
            'english': ('var x = 42\nprint x', ['42']),
            'tamil': ('maari x = 42\nveliyidu x', ['42']),
            'malayalam': ('madhu x = 42\nparakuu x', ['42']),
            'telugu': ('chaala x = 42\ncheppu x', ['42']),
            'hindi': ('badal x = 42\ndikhaao x', ['42']),
            'sanskrit': ('parimaan x = 42\ndarshaya x', ['42'])
        }
        
        for language, (code, expected_output) in test_cases.items():
            with self.subTest(language=language):
                self.compiler.change_language(language)
                result = self.compiler.execute(code)
                self.assertTrue(result['success'], f"Failed for {language}")
                self.assertEqual(result['output'], expected_output)
    
    def test_keyword_consistency(self):
        """Test that all languages have consistent keyword mappings"""
        languages = self.compiler.get_supported_languages()
        
        for language in languages:
            keywords = self.compiler.language_defs.get_keywords_for_language(language)
            
            # Check that all essential keywords are present
            essential_keywords = ['if', 'else', 'while', 'function', 'var', 'print', 'return']
            for keyword in essential_keywords:
                self.assertIn(keyword, keywords, f"Missing {keyword} in {language}")
    
    def test_error_messages(self):
        """Test error messages in different languages"""
        # Test with undefined variable in different languages
        test_cases = [
            ('english', 'print undefined_var'),
            ('tamil', 'veliyidu undefined_var'),
            ('hindi', 'dikhaao undefined_var')
        ]
        
        for language, code in test_cases:
            with self.subTest(language=language):
                self.compiler.change_language(language)
                result = self.compiler.execute(code)
                self.assertFalse(result['success'])
                self.assertIsNotNone(result['error'])


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)