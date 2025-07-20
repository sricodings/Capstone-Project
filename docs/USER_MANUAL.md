# User Manual - Adaptive Multilingual Programming Language

## 🎯 Table of Contents
1. [Getting Started](#getting-started)
2. [Language Selection](#language-selection)
3. [Basic Syntax](#basic-syntax)
4. [Programming Concepts](#programming-concepts)
5. [Code Examples](#code-examples)
6. [Features Guide](#features-guide)
7. [Troubleshooting](#troubleshooting)

## 🚀 Getting Started

### First Steps
1. **Launch the Application**: Run `streamlit run src/streamlit_app.py`
2. **Select Your Language**: Choose from 6 supported languages in the sidebar
3. **Start Coding**: Write your first program in the code editor
4. **Run Your Code**: Click "▶️ Run Code" to see results

### Interface Overview
- **Code Editor**: Main area for writing programs
- **Language Selector**: Sidebar dropdown for language selection
- **Keywords Reference**: Real-time keyword mapping display
- **Output Tabs**: Results, analysis, bytecode, and debug information
- **Action Buttons**: Run, compile, analyze, and clear functions

## 🌐 Language Selection

### Supported Languages

#### English
- **Display Name**: English
- **Code**: `en`
- **Sample**: `if x > 5: print "Hello"`

#### Tamil (தமிழ்)
- **Display Name**: தமிழ்
- **Code**: `ta`
- **Sample**: `yenil x > 5: veliyidu "Vanakkam"`

#### Malayalam (മലയാളം)
- **Display Name**: മലയാളം  
- **Code**: `ml`
- **Sample**: `yendaa x > 5: parakuu "Namaskaram"`

#### Telugu (తెలుగు)
- **Display Name**: తెలుగు
- **Code**: `te`  
- **Sample**: `ayite x > 5: cheppu "Namaste"`

#### Hindi (हिन्दी)
- **Display Name**: हिन्दी
- **Code**: `hi`
- **Sample**: `agar x > 5: dikhaao "Namaste"`

#### Sanskrit (संस्कृत)
- **Display Name**: संस्कृत
- **Code**: `sa`
- **Sample**: `yadi x > 5: darshaya "Namah"`

### Switching Languages
1. Select desired language from sidebar dropdown
2. Keywords automatically update in the reference panel
3. Existing code remains unchanged
4. Use "Translate Code" feature for conversion

## 📝 Basic Syntax

### Universal Syntax Rules
All languages follow identical syntax structure:

#### Variables
```
var variable_name = value
```

#### Conditional Statements
```
if condition:
    statements
else:
    statements
```

#### Loops
```
while condition:
    statements

for variable = start: end:
    statements
```

#### Functions
```
function name(parameters):
    statements
    return value
```

#### Print Statements
```
print expression
```

### Language-Specific Keywords

| Concept | English | Tamil | Malayalam | Telugu | Hindi | Sanskrit |
|---------|---------|--------|-----------|--------|-------|----------|
| Variable | var | maari | madhu | chaala | badal | parimaan |
| If | if | yenil | yendaa | ayite | agar | yadi |
| Else | else | illaiyal | allenkil | leda | warna | anya |
| While | while | varaikum | vare | varaku | jabtak | yavat |
| For | for | ondrumuttal | vendii | kosam | keliye | artham |
| Function | function | seyalpaadu | pani | pani | kaam | kriya |
| Print | print | veliyidu | parakuu | cheppu | dikhaao | darshaya |
| Return | return | thiruppu | thiriche | tirigi | wapas | nivrit |

## 🎓 Programming Concepts

### 1. Variables and Data Types

#### Numbers
```english
var age = 25
var price = 99.99
```

```tamil
maari vayas = 25
maari vilai = 99.99
```

#### Strings
```english
var name = "John"
var message = "Hello World"
```

```hindi
badal naam = "Ram"
badal sandesh = "Namaste Duniya"
```

#### Booleans
```english
var isActive = true
var isComplete = false
```

```malayalam
madhu sakriyam = sathyam
madhu poorna = jhooth
```

### 2. Conditional Logic

#### Simple If Statement
```english
if age >= 18:
    print "Adult"
```

```tamil
yenil vayas >= 18:
    veliyidu "Muthal"
```

#### If-Else Statement
```english
if score >= 60:
    print "Pass"
else:
    print "Fail"
```

```telugu
ayite marks >= 60:
    cheppu "Pass"
leda:
    cheppu "Fail"
```

### 3. Loops

#### While Loop
```english
var i = 1
while i <= 5:
    print i
    var i = i + 1
```

```hindi
badal i = 1
jabtak i <= 5:
    dikhaao i
    badal i = i + 1
```

#### For Loop
```english
for i = 1: 10:
    print "Number: " + i
```

```sanskrit
artham i = 1: 10:
    darshaya "Sankhya: " + i
```

### 4. Functions

#### Function Definition
```english
function greet(name):
    print "Hello " + name
    return true
```

```tamil
seyalpaadu vanakkam(peyar):
    veliyidu "Vanakkam " + peyar
    thiruppu unmai
```

#### Function Call
```english
var result = greet("World")
```

```malayalam
madhu parinaamam = namaskaram("Lokam")
```

## 💡 Code Examples

### Example 1: Hello World
```english
print "Hello, World!"
```

```tamil
veliyidu "Vanakkam, Ulagam!"
```

### Example 2: Number Guessing Game
```english
var secret = 7
var guess = 5

if guess == secret:
    print "Correct!"
else:
    if guess < secret:
        print "Too low"
    else:
        print "Too high"
```

```hindi
badal gupti = 7
badal anumaan = 5

agar anumaan == gupti:
    dikhaao "Sahi!"
warna:
    agar anumaan < gupti:
        dikhaao "Kam hai"
    warna:
        dikhaao "Zyada hai"
```

### Example 3: Factorial Calculator
```english
function factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

var result = factorial(5)
print "Factorial: " + result
```

```telugu
pani factorial(n):
    ayite n <= 1:
        tirigi 1
    leda:
        tirigi n * factorial(n - 1)

chaala parinaamam = factorial(5)
cheppu "Factorial: " + parinaamam
```

### Example 4: Sum of Numbers
```english
function sum_range(start, end):
    var total = 0
    for i = start: end:
        var total = total + i
    return total

var result = sum_range(1, 10)
print "Sum: " + result
```

```sanskrit
kriya sankhya_yoga(aarambha, samaapta):
    parimaan sampurna = 0
    artham i = aarambha: samaapta:
        parimaan sampurna = sampurna + i
    nivrit sampurna

parimaan parinaamam = sankhya_yoga(1, 10)
darshaya "Yoga: " + parinaamam
```

## 🔧 Features Guide

### Code Analysis
1. **Click "📊 Analyze Code"** to get detailed insights
2. **View Metrics**: See statement count, variables, functions
3. **Complexity Score**: Understand code complexity level
4. **Native Descriptions**: Get explanations in your selected language

### Bytecode Viewer
1. **Compile Your Code** using "🔧 Compile Only"
2. **View Bytecode Tab** to see generated instructions
3. **Understand Execution**: See how your code translates to bytecode

### Debug Information
1. **Check Tokens**: See how your code is tokenized
2. **Validate Syntax**: Verify code correctness
3. **Error Messages**: Get helpful error information

### Execution History
1. **Track Runs**: See history of executed programs
2. **Compare Results**: Review previous outputs
3. **Learn Patterns**: Understand execution behavior

## 🛠️ Troubleshooting

### Common Issues

#### 1. Syntax Errors
**Problem**: Code won't compile
**Solution**: 
- Check keyword spelling in selected language
- Verify proper indentation (use spaces, not tabs)
- Ensure colons after if/while/function statements

#### 2. Runtime Errors
**Problem**: Code compiles but fails during execution
**Solution**:
- Check variable names are defined before use
- Verify function names are correct
- Ensure proper data types for operations

#### 3. Language Keywords Not Recognized
**Problem**: Keywords appear as unknown tokens
**Solution**:
- Verify correct language is selected
- Check keyword reference in sidebar
- Use English transliteration for native language keywords

#### 4. Infinite Loops
**Problem**: Program seems to hang
**Solution**:
- Add proper loop termination conditions
- Use break statements where appropriate
- Check loop variable modifications

### Error Messages

#### Compilation Errors
- **"Variable 'x' not defined"**: Declare variable before use
- **"Syntax error at token"**: Check syntax around indicated position
- **"Unknown keyword"**: Verify keyword spelling and language selection

#### Runtime Errors
- **"Division by zero"**: Check divisor values
- **"Stack underflow"**: Internal error - check complex expressions
- **"Execution limit exceeded"**: Possible infinite loop detected

### Getting Help

#### Built-in Help
1. Click **"📖 Show Help"** in sidebar
2. View keyword reference panel
3. Try example programs

#### Documentation
1. Check README.md for setup issues
2. Review API documentation for advanced usage
3. Consult troubleshooting section

#### Community Support
1. Create GitHub issues for bugs
2. Join community discussions
3. Contribute to documentation improvements

### Performance Tips

#### Writing Efficient Code
1. **Minimize Loop Complexity**: Use simple loop conditions
2. **Avoid Deep Recursion**: Limit recursive function calls
3. **Use Appropriate Data Types**: Choose correct types for operations

#### Best Practices
1. **Clear Variable Names**: Use descriptive identifiers
2. **Consistent Indentation**: Maintain proper code structure
3. **Comment Complex Logic**: Add explanatory comments
4. **Test Incrementally**: Build and test code step by step

---

## 📞 Need More Help?

For additional support:
- 📧 **Email**: support@multilingual-lang.org
- 💬 **Discord**: Join our community server
- 📖 **Documentation**: Visit our online docs
- 🐛 **Bug Reports**: Create GitHub issues

**Happy Coding in Your Native Language! 🌍**