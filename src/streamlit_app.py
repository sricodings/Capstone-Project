"""
Streamlit Web Application for Multilingual Programming Language
Main user interface with code editor, compilation, and execution
"""

import streamlit as st
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from compiler import MultilingualCompiler, CompilerError
from language_definitions import LanguageDefinitions

# Page configuration
st.set_page_config(
    page_title="Adaptive Multilingual Programming Language",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2563EB 0%, #059669 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .language-card {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    .language-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    .code-output {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        border: 1px solid #334155;
    }
    .error-output {
        background: #fef2f2;
        color: #dc2626;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #fecaca;
    }
    .success-output {
        background: #f0fdf4;
        color: #059669;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bbf7d0;
    }
    .keyword-badge {
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;
        margin: 0.125rem;
        display: inline-block;
    }
    .sidebar-section {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'compiler' not in st.session_state:
    st.session_state.compiler = MultilingualCompiler()
    st.session_state.current_language = 'english'
    st.session_state.code = ""
    st.session_state.execution_history = []

def main():
    # Header
    st.markdown('<div class="main-header"><h1>🌍 Adaptive Multilingual Programming Language</h1><p>Write Once, Run Anywhere - in your native language!</p></div>', unsafe_allow_html=True)
    
    # Sidebar for language selection and help
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("🔧 Language Settings")
        
        # Language selection
        lang_defs = LanguageDefinitions()
        languages = lang_defs.get_language_list()
        language_names = [lang_defs.get_language_name(lang) for lang in languages]
        
        selected_index = st.selectbox(
            "Select Programming Language",
            range(len(languages)),
            format_func=lambda x: f"{language_names[x]} ({languages[x]})",
            index=languages.index(st.session_state.current_language)
        )
        
        selected_language = languages[selected_index]
        
        # Update compiler if language changed
        if selected_language != st.session_state.current_language:
            st.session_state.current_language = selected_language
            st.session_state.compiler.change_language(selected_language)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Keywords reference
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📚 Keywords Reference")
        keywords = st.session_state.compiler.get_keywords_for_current_language()
        
        for eng_keyword, local_keyword in keywords.items():
            st.markdown(f'<span class="keyword-badge">{eng_keyword} → {local_keyword}</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Help section
        if st.button("📖 Show Help", use_container_width=True):
            st.session_state.show_help = True
        
        # Example programs
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("💡 Example Programs")
        
        if st.button("Hello World", use_container_width=True):
            if selected_language == 'english':
                st.session_state.code = 'print "Hello, World!"'
            elif selected_language == 'tamil':
                st.session_state.code = 'veliyidu "Vanakkam, Ulagam!"'
            elif selected_language == 'hindi':
                st.session_state.code = 'dikhaao "Namaste, Duniya!"'
        
        if st.button("Simple Loop", use_container_width=True):
            if selected_language == 'english':
                st.session_state.code = """var i = 1
while i <= 5:
    print i
    var i = i + 1"""
            elif selected_language == 'tamil':
                st.session_state.code = """maari i = 1
varaikum i <= 5:
    veliyidu i
    maari i = i + 1"""
        
        if st.button("Function Example", use_container_width=True):
            if selected_language == 'english':
                st.session_state.code = """function greet(name):
    print "Hello " + name
    return true

var result = greet("World")"""
            elif selected_language == 'tamil':
                st.session_state.code = """seyalpaadu vanakkam(peyar):
    veliyidu "Vanakkam " + peyar
    thiruppu unmai

maari mudivU = vanakkam("Ulagam")"""
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("✏️ Code Editor")
        
        # Code editor
        current_lang_display = lang_defs.get_language_name(selected_language)
        code = st.text_area(
            f"Write your code in {current_lang_display}:",
            value=st.session_state.code,
            height=400,
            key="code_editor",
            help=f"Use {current_lang_display} keywords. See the sidebar for reference."
        )
        
        st.session_state.code = code
        
        # Action buttons
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        
        with col_btn1:
            run_button = st.button("▶️ Run Code", type="primary", use_container_width=True)
        
        with col_btn2:
            compile_button = st.button("🔧 Compile Only", use_container_width=True)
        
        with col_btn3:
            analyze_button = st.button("📊 Analyze Code", use_container_width=True)
        
        with col_btn4:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.session_state.code = ""
            st.rerun()
    
    with col2:
        st.header("📤 Output & Results")
        
        # Tabs for different outputs
        tab1, tab2, tab3, tab4 = st.tabs(["🖥️ Output", "📋 Analysis", "⚙️ Bytecode", "🔍 Debug"])
        
        with tab1:
            if run_button and code.strip():
                with st.spinner("Executing code..."):
                    try:
                        # Get input if needed
                        input_data = []
                        if 'input(' in code or 'grah(' in code or 'ulle(' in code:
                            input_text = st.text_input("Enter input (comma-separated for multiple values):")
                            if input_text:
                                input_data = [x.strip() for x in input_text.split(',')]
                        
                        result = st.session_state.compiler.execute(code, input_data)
                        
                        if result['success']:
                            if result['output']:
                                st.markdown('<div class="success-output">', unsafe_allow_html=True)
                                st.text("Program Output:")
                                for line in result['output']:
                                    st.text(line)
                                st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.success("Program executed successfully (no output)")
                            
                            # Add to history
                            st.session_state.execution_history.append({
                                'code': code,
                                'language': selected_language,
                                'output': result['output'],
                                'success': True
                            })
                        else:
                            st.markdown(f'<div class="error-output">Error: {result["error"]}</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.markdown(f'<div class="error-output">Execution Error: {str(e)}</div>', unsafe_allow_html=True)
            
            elif compile_button and code.strip():
                with st.spinner("Compiling code..."):
                    try:
                        instructions = st.session_state.compiler.compile_to_bytecode(code)
                        st.success(f"✅ Compilation successful! Generated {len(instructions)} instructions.")
                    except CompilerError as e:
                        st.markdown(f'<div class="error-output">Compilation Error: {str(e)}</div>', unsafe_allow_html=True)
        
        with tab2:
            if analyze_button and code.strip():
                with st.spinner("Analyzing code..."):
                    try:
                        analysis = st.session_state.compiler.analyze_code(code)
                        
                        st.subheader("📊 Code Analysis")
                        
                        # Basic metrics
                        col_a1, col_a2, col_a3 = st.columns(3)
                        with col_a1:
                            st.metric("Statements", analysis.get('total_statements', 0))
                        with col_a2:
                            st.metric("Variables", len(analysis.get('variables', [])))
                        with col_a3:
                            st.metric("Functions", len(analysis.get('functions', [])))
                        
                        # Complexity
                        complexity = analysis.get('complexity_score', 0)
                        if complexity < 5:
                            st.success(f"🟢 Low Complexity (Score: {complexity})")
                        elif complexity < 15:
                            st.warning(f"🟡 Medium Complexity (Score: {complexity})")
                        else:
                            st.error(f"🔴 High Complexity (Score: {complexity})")
                        
                        # Description
                        if 'description' in analysis:
                            st.subheader("📝 Code Description")
                            st.info(analysis['description'])
                        
                        # Variables and functions
                        if analysis.get('variables'):
                            st.subheader("📋 Variables Used")
                            for var in analysis['variables']:
                                st.markdown(f"• `{var}`")
                        
                        if analysis.get('functions'):
                            st.subheader("🔧 Functions Defined")
                            for func in analysis['functions']:
                                st.markdown(f"• `{func}()`")
                        
                        # Control structures
                        if analysis.get('control_structures'):
                            st.subheader("🔄 Control Structures")
                            structure_counts = {}
                            for structure in analysis['control_structures']:
                                structure_counts[structure] = structure_counts.get(structure, 0) + 1
                            
                            for structure, count in structure_counts.items():
                                st.markdown(f"• `{structure}`: {count} times")
                    
                    except Exception as e:
                        st.error(f"Analysis Error: {str(e)}")
        
        with tab3:
            if code.strip():
                try:
                    # Try to compile and show bytecode
                    st.session_state.compiler.compile_to_bytecode(code)
                    bytecode_listing = st.session_state.compiler.get_bytecode_listing()
                    
                    st.markdown('<div class="code-output">', unsafe_allow_html=True)
                    st.text(bytecode_listing)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Cannot generate bytecode: {str(e)}")
        
        with tab4:
            st.subheader("🔍 Debug Information")
            
            # Tokenization
            if code.strip():
                try:
                    tokens = st.session_state.compiler.tokenize(code)
                    
                    st.write("**Tokens:**")
                    token_display = []
                    for token in tokens[:20]:  # Limit display
                        token_display.append(f"{token['type']}: {token['value']}")
                    
                    st.text("\n".join(token_display))
                    if len(tokens) > 20:
                        st.text(f"... and {len(tokens) - 20} more tokens")
                
                except Exception as e:
                    st.error(f"Tokenization Error: {str(e)}")
            
            # Syntax validation
            if st.button("Validate Syntax"):
                if code.strip():
                    validation = st.session_state.compiler.validate_syntax(code)
                    if validation['valid']:
                        st.success("✅ Syntax is valid!")
                    else:
                        st.error("❌ Syntax errors found:")
                        for error in validation['errors']:
                            st.text(f"• {error}")
    
    # Help dialog
    if st.session_state.get('show_help', False):
        with st.expander("📖 Programming Language Help", expanded=True):
            help_text = st.session_state.compiler.get_help_text()
            st.text(help_text)
            
            if st.button("Close Help"):
                st.session_state.show_help = False
                st.rerun()
    
    # Execution history
    if st.session_state.execution_history:
        with st.expander("📚 Execution History"):
            for i, entry in enumerate(reversed(st.session_state.execution_history[-5:])):
                st.text(f"--- Execution {len(st.session_state.execution_history) - i} ({entry['language']}) ---")
                st.code(entry['code'])
                if entry['success'] and entry['output']:
                    st.text("Output: " + ', '.join(entry['output']))
                st.text("")

if __name__ == "__main__":
    main()