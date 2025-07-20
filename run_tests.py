#!/usr/bin/env python3
"""
Test runner for the Multilingual Programming Language
Runs comprehensive tests and generates coverage reports
"""

import sys
import os
import unittest
import time

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_all_tests():
    """Run all test suites"""
    print("🧪 Running Multilingual Programming Language Tests")
    print("=" * 60)
    
    # Start timing
    start_time = time.time()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    test_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    # Calculate timing
    end_time = time.time()
    duration = end_time - start_time
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"Duration: {duration:.2f} seconds")
    
    # Print failure details if any
    if result.failures:
        print("\n❌ FAILURES:")
        for test, trace in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n🚨 ERRORS:")
        for test, trace in result.errors:
            print(f"  - {test}")
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0

def test_basic_functionality():
    """Quick smoke test for basic functionality"""
    print("\n🔥 Running Smoke Tests")
    print("-" * 30)
    
    try:
        from compiler import MultilingualCompiler
        
        # Test compiler initialization
        compiler = MultilingualCompiler()
        print("✅ Compiler initialization")
        
        # Test language switching
        compiler.change_language('tamil')
        compiler.change_language('english')
        print("✅ Language switching")
        
        # Test basic compilation
        code = 'var x = 10\nprint x'
        result = compiler.execute(code)
        assert result['success'], "Basic compilation failed"
        assert result['output'] == ['10'], "Incorrect output"
        print("✅ Basic code execution")
        
        # Test analysis
        analysis = compiler.analyze_code(code)
        assert 'description' in analysis, "Analysis failed"
        print("✅ Code analysis")
        
        print("🎉 All smoke tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False

def test_all_languages():
    """Test basic functionality in all supported languages"""
    print("\n🌍 Testing All Languages")
    print("-" * 30)
    
    try:
        from compiler import MultilingualCompiler
        
        compiler = MultilingualCompiler()
        languages = compiler.get_supported_languages()
        
        test_programs = {
            'english': 'var x = 5\nif x > 3:\n    print "Pass"',
            'tamil': 'maari x = 5\nyenil x > 3:\n    veliyidu "Pass"',
            'malayalam': 'madhu x = 5\nyendaa x > 3:\n    parakuu "Pass"',
            'telugu': 'chaala x = 5\nayite x > 3:\n    cheppu "Pass"',
            'hindi': 'badal x = 5\nagar x > 3:\n    dikhaao "Pass"',
            'sanskrit': 'parimaan x = 5\nyadi x > 3:\n    darshaya "Pass"'
        }
        
        for language in languages:
            compiler.change_language(language)
            
            if language in test_programs:
                code = test_programs[language]
                result = compiler.execute(code)
                
                if result['success'] and result['output'] == ['Pass']:
                    print(f"✅ {compiler.get_language_display_name(language)}")
                else:
                    print(f"❌ {compiler.get_language_display_name(language)}: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"⚠️  {language}: No test program defined")
        
        print("🎉 All language tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Language test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Multilingual Programming Language - Test Suite")
    print("=" * 60)
    
    # Run smoke tests first
    if not test_basic_functionality():
        print("💥 Smoke tests failed - aborting full test suite")
        return False
    
    # Test all languages
    if not test_all_languages():
        print("💥 Language tests failed - aborting full test suite")
        return False
    
    # Run full test suite
    success = run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("Your multilingual programming language is working perfectly!")
    else:
        print("\n💥 SOME TESTS FAILED")
        print("Please review the failures above and fix the issues.")
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)