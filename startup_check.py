import os
import sys

# Suppress Streamlit warnings during startup
os.environ["STREAMLIT_SERVER_HEADLESS"] = "false"

try:
    import streamlit as st
    print("✅ Streamlit loaded successfully")
except ImportError as e:
    print(f"❌ Streamlit import error: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

print("""
═══════════════════════════════════════════════════════════════
  🧠 Argument Structure Analyzer
═══════════════════════════════════════════════════════════════

✅ App starting...

   🌐 Open in browser: http://localhost:8501
   
   💡 First load may take 10-20 seconds
   
   ⏸️  Press Ctrl+C to stop
   
═══════════════════════════════════════════════════════════════
""")
