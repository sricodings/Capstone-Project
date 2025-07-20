# Adaptive Multilingual Programming Language

## 🌍 Overview

An innovative programming language with WORA (Write Once, Run Anywhere) capabilities that adapts to multiple human languages while maintaining consistent syntax. This project demonstrates cutting-edge approaches to programming language accessibility and localization.

## ✨ Key Features

### Core Programming Language
- **Simple Syntax**: Designed for ease of learning and use
- **WORA Capability**: Bytecode compilation for platform independence
- **Custom Compiler**: Built with PLY (Python Lex-Yacc)
- **Virtual Machine**: Stack-based execution environment
- **Consistent Structure**: Identical syntax across all language variants

### Multilingual Support
- **6+ Languages**: Tamil, English, Malayalam, Telugu, Hindi, Sanskrit
- **Adaptive Keywords**: Keywords change based on selected language
- **Transliteration**: English transliteration for native language concepts
- **Seamless Switching**: Change languages without altering program structure

### User Interface
- **Streamlit Web App**: Modern, responsive web interface
- **Real-time Compilation**: Instant feedback on code changes
- **Syntax Highlighting**: Language-aware code highlighting
- **Interactive Help**: Contextual guidance and examples

### Code Analysis System
- **Intelligent Descriptions**: AI-powered code explanation
- **Native Language Output**: Explanations in user's selected language
- **Complexity Analysis**: Automated code complexity scoring
- **Error Detection**: Smart identification of potential issues

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multilingual-programming-language.git
   cd multilingual-programming-language
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run src/streamlit_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 💻 Usage Examples

### English
```
var x = 10
if x > 5:
    print "Greater than 5"

function greet(name):
    print "Hello " + name
    return true
```

### Tamil (தமிழ்)
```
maari x = 10
yenil x > 5:
    veliyidu "5 vida periyathu"

seyalpaadu vanakkam(peyar):
    veliyidu "Vanakkam " + peyar
    thiruppu unmai
```

### Hindi (हिन्दी)
```
badal x = 10
agar x > 5:
    dikhaao "5 se zyada"

kaam namaste(naam):
    dikhaao "Namaste " + naam
    wapas sach
```

## 🏗️ Architecture

### Components

1. **Language Definitions** (`language_definitions.py`)
   - Keyword mappings for all supported languages
   - Description templates for code explanation
   - Language metadata and configuration

2. **Lexical Analyzer** (`lexer.py`)
   - PLY-based tokenization
   - Language-aware keyword recognition
   - Syntax highlighting rule generation

3. **Parser** (`parser.py`)
   - Recursive descent parsing with PLY yacc
   - Abstract Syntax Tree (AST) generation
   - Error recovery and reporting

4. **AST Nodes** (`ast_nodes.py`)
   - Complete AST node definitions
   - Visitor pattern implementation
   - Type-safe node representations

5. **Bytecode Generator** (`bytecode_generator.py`)
   - AST to bytecode compilation
   - Instruction set definition
   - Constant pool management

6. **Virtual Machine** (`virtual_machine.py`)
   - Stack-based execution engine
   - Instruction dispatch and execution
   - Memory and state management

7. **Code Analyzer** (`code_analyzer.py`)
   - Intelligent code analysis
   - Multilingual description generation
   - Complexity metrics and insights

8. **Compiler** (`compiler.py`)
   - Main integration layer
   - Language switching coordination
   - End-to-end compilation pipeline

9. **Streamlit App** (`streamlit_app.py`)
   - Web-based user interface
   - Real-time compilation and execution
   - Interactive development environment

### Execution Flow

1. **Code Input**: User writes code in selected language
2. **Tokenization**: Lexer breaks code into language-aware tokens
3. **Parsing**: Parser generates Abstract Syntax Tree
4. **Analysis**: Code analyzer provides insights and descriptions
5. **Compilation**: Bytecode generator creates executable instructions
6. **Execution**: Virtual machine runs bytecode and produces output

## 🔧 Technical Specifications

### Supported Constructs
- Variables and assignments
- Conditional statements (if/else)
- Loops (while, for)
- Functions with parameters and return values
- Arithmetic and logical operations
- Built-in functions (print, input, type conversion)

### Bytecode Instructions
- `LOAD_CONST`: Load constant value
- `LOAD_VAR`: Load variable value
- `STORE_VAR`: Store value in variable
- `BINARY_OP`: Binary operations (+, -, *, /, etc.)
- `UNARY_OP`: Unary operations (-, not)
- `JUMP`: Unconditional jump
- `JUMP_IF_FALSE`: Conditional jump
- `CALL`: Function call
- `RETURN`: Function return
- `PRINT`: Output instruction
- `HALT`: Program termination

### Language Keywords Mapping

| English | Tamil | Malayalam | Telugu | Hindi | Sanskrit |
|---------|--------|-----------|--------|-------|----------|
| if | yenil | yendaa | ayite | agar | yadi |
| else | illaiyal | allenkil | leda | warna | anya |
| while | varaikum | vare | varaku | jabtak | yavat |
| function | seyalpaadu | pani | pani | kaam | kriya |
| print | veliyidu | parakuu | cheppu | dikhaao | darshaya |

## 🧪 Testing

### Running Tests
```bash
python -m pytest tests/
```

### Test Coverage
- Unit tests for all major components
- Integration tests for end-to-end functionality
- Language-specific test cases
- Performance and stress testing

## 📚 Documentation

### API Reference
- Complete API documentation for all modules
- Usage examples and best practices
- Extension and customization guides

### User Manual
- Step-by-step tutorials for each supported language
- Programming concepts and syntax explanations
- Troubleshooting and FAQ

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Add tests for new functionality
6. Submit a pull request

### Adding New Languages
1. Add language definition in `language_definitions.py`
2. Update keyword mappings
3. Add description templates
4. Create test cases
5. Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PLY (Python Lex-Yacc) for parsing infrastructure
- Streamlit for the web interface framework
- The open-source community for inspiration and tools

## 🔮 Future Roadmap

- [ ] Additional language support (Arabic, Chinese, Japanese)
- [ ] Advanced IDE features (debugging, intellisense)
- [ ] Package management system
- [ ] Object-oriented programming constructs
- [ ] Standard library development
- [ ] Mobile app development
- [ ] Cloud-based execution environment

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Join our community discussions
- Check the documentation and FAQ

---

**Made with ❤️ for global programming accessibility**