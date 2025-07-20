import React, { useState, useCallback, useMemo } from 'react';
import { Play, Code, FileText, HelpCircle, Trash2, Globe, ChevronDown } from 'lucide-react';
import { LANGUAGES, LanguageDefinition, getAllLanguages } from './language/definitions';
import { Lexer } from './compiler/lexer';
import { Parser, ParseError } from './compiler/parser';
import { BytecodeGenerator, VirtualMachine } from './compiler/bytecode';

interface CompilationResult {
  success: boolean;
  output?: string[];
  error?: string;
  bytecode?: any;
}

interface CodeDescription {
  summary: string;
  details: string[];
  complexity: 'Simple' | 'Moderate' | 'Complex';
}

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState<string>('english');
  const [code, setCode] = useState<string>('');
  const [output, setOutput] = useState<string[]>([]);
  const [error, setError] = useState<string>('');
  const [isCompiling, setIsCompiling] = useState<boolean>(false);
  const [showHelp, setShowHelp] = useState<boolean>(false);
  const [codeDescription, setCodeDescription] = useState<CodeDescription | null>(null);
  const [showLanguageDropdown, setShowLanguageDropdown] = useState<boolean>(false);

  const currentLanguage = useMemo(() => {
    const allLangs = Object.values(LANGUAGES);
    return allLangs.find(lang => lang.code === selectedLanguage) || LANGUAGES['english'];
  }, [selectedLanguage]);
  

  const availableLanguages = useMemo(() => getAllLanguages(), []);

  const generateCodeDescription = useCallback((code: string, language: LanguageDefinition): CodeDescription => {
    const lines = code.trim().split('\n').filter(line => line.trim());
    const details: string[] = [];
    let complexity: 'Simple' | 'Moderate' | 'Complex' = 'Simple';

    if (lines.length === 0) {
      return {
        summary: language.messages.welcome || "Empty program",
        details: ["No code to analyze"],
        complexity: 'Simple'
      };
    }

    const hasLoops = code.includes(language.keywords.while) || code.includes(language.keywords.for);
    const hasConditions = code.includes(language.keywords.if);
    const hasFunctions = code.includes(language.keywords.function);
    const hasVariables = code.includes(language.keywords.var);

    if (hasFunctions || (hasLoops && hasConditions)) {
      complexity = 'Complex';
    } else if (hasLoops || hasConditions || hasVariables) {
      complexity = 'Moderate';
    }

    let summary = '';
    switch (language.code) {
      case 'ta':
        summary = `இந்த நிரல் ${lines.length} வரிகளைக் கொண்டுள்ளது`;
        if (hasVariables) details.push('மாறிகளை பயன்படுத்துகிறது');
        if (hasConditions) details.push('நிபந்தனை சோதனைகளை செய்கிறது');
        if (hasLoops) details.push('மீண்டும் மீண்டும் செயல்களை செய்கிறது');
        if (hasFunctions) details.push('செயல்பாடுகளை வரையறுக்கிறது');
        break;
      case 'ml':
        summary = `ഈ പ്രോഗ്രാമിൽ ${lines.length} വരികൾ ഉണ്ട്`;
        if (hasVariables) details.push('വേരിയബിളുകൾ ഉപയോഗിക്കുന്നു');
        if (hasConditions) details.push('വ്യവസ്ഥകൾ പരിശോധിക്കുന്നു');
        if (hasLoops) details.push('ആവർത്തന പ്രവർത്തനങ്ങൾ നടത്തുന്നു');
        if (hasFunctions) details.push('ഫംഗ്ഷനുകൾ നിർവചിക്കുന്നു');
        break;
      case 'te':
        summary = `ఈ ప్రోగ్రామ్‌లో ${lines.length} లైన్లు ఉన్నాయి`;
        if (hasVariables) details.push('వేరియబుల్స్ ఉపయోగిస్తుంది');
        if (hasConditions) details.push('షరతులను తనిఖీ చేస్తుంది');
        if (hasLoops) details.push('పునరావృత కార్యకలాపాలు చేస్తుంది');
        if (hasFunctions) details.push('ఫంక్షన్లను నిర్వచిస్తుంది');
        break;
      case 'hi':
        summary = `इस प्रोग्राम में ${lines.length} लाइनें हैं`;
        if (hasVariables) details.push('वेरिएबल्स का उपयोग करता है');
        if (hasConditions) details.push('शर्तों की जांच करता है');
        if (hasLoops) details.push('दोहराव के कार्य करता है');
        if (hasFunctions) details.push('फंक्शन्स को परिभाषित करता है');
        break;
      case 'sa':
        summary = `अस्मिन् प्रोग्रामे ${lines.length} पंक्तयः सन्ति`;
        if (hasVariables) details.push('चरांकानां प्रयोगं करोति');
        if (hasConditions) details.push('शर्तानां परीक्षां करोति');
        if (hasLoops) details.push('पुनरावृत्ति कार्याणि करोति');
        if (hasFunctions) details.push('कार्याणि परिभाषयति');
        break;
      default:
        summary = `This program contains ${lines.length} lines`;
        if (hasVariables) details.push('Uses variables for data storage');
        if (hasConditions) details.push('Performs conditional logic');
        if (hasLoops) details.push('Executes repetitive operations');
        if (hasFunctions) details.push('Defines reusable functions');
    }

    return { summary, details, complexity };
  }, []);

  const compileAndRun = useCallback(async (): Promise<CompilationResult> => {
    if (!code.trim()) {
      return { success: false, error: currentLanguage.messages.syntaxError || 'No code to compile' };
    }

    try {
      const lexer = new Lexer(code, currentLanguage);
      const tokens = lexer.tokenize();

      const parser = new Parser(tokens);
      const ast = parser.parse();

      const generator = new BytecodeGenerator();
      const bytecode = generator.generate(ast);

      const vm = new VirtualMachine();
      const result = vm.execute(bytecode);

      if (result.error) {
        return { success: false, error: result.error };
      }

      return { 
        success: true, 
        output: result.output,
        bytecode 
      };
    } catch (error) {
      if (error instanceof ParseError) {
        return { 
          success: false, 
          error: `${currentLanguage.messages.syntaxError || 'Syntax Error'}: ${error.message} at line ${error.token.line}` 
        };
      }
      return { 
        success: false, 
        error: error instanceof Error ? error.message : String(error) 
      };
    }
  }, [code, currentLanguage]);

  const handleCompile = useCallback(async () => {
    setIsCompiling(true);
    setError('');
    setOutput([]);

    const result = await compileAndRun();

    if (result.success) {
      setOutput(result.output || []);
    } else {
      setError(result.error || 'Unknown error');
    }

    setIsCompiling(false);
  }, [compileAndRun]);

  const handleDescribeCode = useCallback(() => {
    if (!code.trim()) {
      setCodeDescription({
        summary: currentLanguage.messages.welcome || "No code to analyze",
        details: ["Please write some code first"],
        complexity: 'Simple'
      });
      return;
    }

    const description = generateCodeDescription(code, currentLanguage);
    setCodeDescription(description);
  }, [code, currentLanguage, generateCodeDescription]);

  const handleClear = useCallback(() => {
    setCode('');
    setOutput([]);
    setError('');
    setCodeDescription(null);
  }, []);

  const getExampleCode = useCallback((language: LanguageDefinition): string => {
    const { keywords } = language;
    return `${keywords.var} x = 10;\n${keywords.var} y = 20;\n${keywords.var} sum = x + y;\n${keywords.print}(sum);\n\n${keywords.if} (sum > 25) {\n    ${keywords.print}(\"Sum is greater than 25\");\n} ${keywords.else} {\n    ${keywords.print}(\"Sum is 25 or less\");\n}`;
  }, []);

  const handleLanguageChange = useCallback((langCode: string) => {
    const newLanguage = LANGUAGES[langCode] || LANGUAGES['english'];
    setSelectedLanguage(langCode);
    setShowLanguageDropdown(false);
    setError('');
    setOutput([]);
    setCodeDescription(null);
    // Always set example code when changing languages
    setCode(getExampleCode(newLanguage));
  }, [getExampleCode]);
  


  return (
    
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <Globe className="w-8 h-8 text-blue-600" />
              <h1 className="text-3xl font-bold text-gray-800">
                {currentLanguage.messages.welcome}
              </h1>
            </div>
            <button
              onClick={() => setShowHelp(!showHelp)}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors"
            >
              <HelpCircle className="w-5 h-5" />
              <span>{currentLanguage.messages.help}</span>
            </button>
          </div>

          {/* Language Selector */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {currentLanguage.messages.selectLanguage}
            </label>
            <button
              onClick={() => setShowLanguageDropdown(!showLanguageDropdown)}
              className="w-full md:w-64 flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg hover:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
              <span className="font-medium">{currentLanguage.name}</span>
              <ChevronDown className="w-5 h-5 text-gray-400" />
            </button>
     
          {showLanguageDropdown && (
            <div className="absolute top-full left-0 right-0 md:right-auto md:w-64 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
              {availableLanguages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code)}
                className={`w-full text-left px-4 py-3 hover:bg-blue-50 first:rounded-t-lg last:rounded-b-lg transition-colors ${
                selectedLanguage === lang.code ? 'bg-blue-100 text-blue-700' : 'text-gray-700'
              }`}
              >
             {lang.name}
              </button>
            ))}
          </div>
          )}
        </div>
        </div>
        {/* Help Panel */}
        {showHelp && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">
              {currentLanguage.messages.help}
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Keywords:</h4>
                <div className="space-y-1 text-sm">
                  {Object.entries(currentLanguage.keywords).map(([eng, translated]) => (
                    <div key={eng} className="flex justify-between">
                      <code className="bg-gray-100 px-2 py-1 rounded">{translated}</code>
                      <span className="text-gray-500">({eng})</span>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Example:</h4>
                <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                  <code>{getExampleCode(currentLanguage)}</code>
                </pre>
              </div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Code Editor */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-800 flex items-center space-x-2">
                <Code className="w-5 h-5" />
                <span>Code Editor</span>
              </h2>
              <div className="flex space-x-2">
                <button
                  onClick={handleDescribeCode}
                  className="flex items-center space-x-2 px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors"
                >
                  <FileText className="w-4 h-4" />
                  <span>{currentLanguage.messages.describe}</span>
                </button>
                <button
                  onClick={handleClear}
                  className="flex items-center space-x-2 px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                  <span>{currentLanguage.messages.clear}</span>
                </button>
              </div>
            </div>
            
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-80 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              placeholder={`Write your code in ${currentLanguage.name}...`}
              spellCheck={false}
            />
            
            <div className="mt-4 flex justify-between items-center">
              <div className="text-sm text-gray-500">
                Lines: {code.split('\n').length} | Characters: {code.length}
              </div>
              <button
                onClick={handleCompile}
                disabled={isCompiling || !code.trim()}
                className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Play className="w-5 h-5" />
                <span>{isCompiling ? 'Compiling...' : currentLanguage.messages.run}</span>
              </button>
            </div>
          </div>

          {/* Output and Description */}
          <div className="space-y-6">
            {/* Output Panel */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Output</h2>
              <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm min-h-32 max-h-64 overflow-y-auto">
                {error ? (
                  <div className="text-red-400">{error}</div>
                ) : output.length > 0 ? (
                  output.map((line, index) => (
                    <div key={index}>{line}</div>
                  ))
                ) : (
                  <div className="text-gray-500">
                    {currentLanguage.messages.executionComplete || 'Ready to run...'}
                  </div>
                )}
              </div>
            </div>

            {/* Code Description */}
            {codeDescription && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-800 mb-4">
                  {currentLanguage.messages.describe}
                </h2>
                <div className="space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-gray-700">Summary</h3>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        codeDescription.complexity === 'Simple' ? 'bg-green-100 text-green-700' :
                        codeDescription.complexity === 'Moderate' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {codeDescription.complexity}
                      </span>
                    </div>
                    <p className="text-gray-600">{codeDescription.summary}</p>
                  </div>
                  
                  {codeDescription.details.length > 0 && (
                    <div>
                      <h3 className="font-medium text-gray-700 mb-2">Details</h3>
                      <ul className="space-y-1">
                        {codeDescription.details.map((detail, index) => (
                          <li key={index} className="text-gray-600 flex items-start space-x-2">
                            <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></span>
                            <span>{detail}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Adaptive Multilingual Programming Language</p>
        </div>
      </div>
    </div>
  );
}

export default App;
