"""
TraderTraitor-Trace: Professional Threat Intelligence Dashboard.
Symmetric Layout: Input (Left) + Output (Right) for both tabs.
Includes Input Validation Security.
"""

import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import re # <-- Importamos Regex para validación

from src.phishing_analyzer import RecruiterAnalyzer
from src.blockchain_tracker import BlockchainTracker
from src.ai_analyst import generate_threat_report

st.set_page_config(page_title="TraderTraitor Trace", page_icon="🥷", layout="wide")

# ==========================================
# 🎨 CLEAN CYBERPUNK THEME (CSS)
# ==========================================
cyberpunk_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Fondo general */
.stApp {
    background-color: #0a0a0f;
    color: #e0e0e0;
    font-family: 'Share Tech Mono', monospace;
}

/* Título Principal Verde Neón */
h1 {
    color: #00ff41 !important;
    text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    font-family: 'Share Tech Mono', monospace;
}

/* Subtítulos en Cian */
h2, h3 {
    color: #00ffff !important;
    font-family: 'Share Tech Mono', monospace;
}

/* Cajas de entrada */
.stTextArea textarea, .stTextInput input {
    background-color: #111111 !important;
    color: #00ff41 !important;
    border: 1px solid #333 !important;
    border-left: 4px solid #00ffff !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Botones */
.stButton > button {
    background-color: #111111 !important;
    color: #00ffff !important;
    border: 1px solid #00ffff !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace;
    transition: all 0.2s ease !important;
    width: 100%;
}

.stButton > button:hover {
    background-color: #00ffff !important;
    color: #000000 !important;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.4) !important;
}

/* Tarjetas de métricas */
div[data-testid="stMetric"] {
    background-color: #111111;
    border: 1px solid #333;
    padding: 10px;
    border-radius: 5px;
}

div[data-testid="stMetricValue"] {
    color: #00ff41 !important;
    font-family: 'Share Tech Mono', monospace;
}

/* Footer Custom */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #111111;
    color: #888;
    text-align: center;
    padding: 10px;
    font-size: 12px;
    border-top: 1px solid #333;
    font-family: 'Share Tech Mono', monospace;
    z-index: 1000;
}
</style>
"""
st.markdown(cyberpunk_css, unsafe_allow_html=True)

# ==========================================
# ⚠️ SIDEBAR DISCLAIMER
# ==========================================
st.sidebar.warning(
    "⚠️ **Ethical Disclaimer**\n\n"
    "This tool is built for **educational and defensive cybersecurity purposes only**. "
    "It utilizes public blockchain data and should not be used to target or harass individuals. "
    "Always ensure you have explicit permission before conducting security assessments."
)

# ==========================================
# HEADER
# ==========================================
st.title("🥷 TraderTraitor-Trace")
st.markdown("**Threat Intelligence & Blockchain Forensics Dashboard**")
st.divider()

# Pestañas
tab_osint, tab_blockchain = st.tabs(["🕵️‍♂️ OSINT Analyzer", "⛓️ Blockchain Forensics"])

# ==========================================
# PESTAÑA 1: OSINT
# ==========================================
with tab_osint:
    st.header("Social Engineering Detector")
    
    col_input, col_output = st.columns([1, 1.5])
    
    with col_input:
        st.markdown("### Input")
        message_input = st.text_area(
            "Paste the suspicious message:", 
            height=250,
            placeholder="Hello, please download this file..."
        )
        analyze_btn = st.button("🚀 RUN ANALYSIS", type="primary")
        
    with col_output:
        st.markdown("### Analysis Results")
        
        if analyze_btn and message_input.strip():
            with st.spinner("Analyzing threat vector..."):
                analyzer = RecruiterAnalyzer()
                result = analyzer.analyze_text(message_input)
                
                c1, c2 = st.columns(2)
                c1.metric("Risk Score", f"{result['risk_score']}/100")
                
                if result['risk_score'] >= 70:
                    c2.error("Level: CRITICAL")
                elif result['risk_score'] >= 40:
                    c2.warning("Level: HIGH")
                else:
                    c2.success("Level: LOW")
                
                with st.expander("🚩 View Red Flags Detected", expanded=True):
                    for finding in result['findings']:
                        st.write(finding)
                
                st.markdown("#### 🧠 AI Threat Report")
                with st.spinner("Generating AI report..."):
                    ai_report = generate_threat_report(message_input, result['findings'])
                    st.info(ai_report)
                    
        elif analyze_btn and not message_input.strip():
            st.warning("Please enter a message to analyze.")
        else:
            st.info("Waiting for input... Paste a message on the left to begin.")


# ==========================================
# PESTAÑA 2: BLOCKCHAIN
# ==========================================
with tab_blockchain:
    st.header("On-Chain Fund Tracker")
    
    col_input, col_output = st.columns([1, 1.5])
    
    with col_input:
        st.markdown("### Search Parameters")
        
        network = st.selectbox(
            "Select Network:",
            options=[
                ("Ethereum Mainnet", 1),
                ("Binance Smart Chain (BSC)", 56),
                ("Polygon POS", 137),
                ("Arbitrum One", 42161)
            ],
            format_func=lambda x: x[0]
        )
        chain_id = network[1]
        
        address_input = st.text_input(
            "Wallet Address:", 
            value="0x28C6c06298d514Db089934071355E5743bf21d60"
        )
        
        trace_btn = st.button("🛰️ TRACE FUNDS", type="primary")
        
        if trace_btn:
            # 🛡️ SECURITY GUARDRAIL: Validación de Dirección
            # Expresión regular que exige empezar con 0x y tener 40 caracteres hexadecimales
            if not re.match(r"^0x[a-fA-F0-9]{40}$", address_input.strip()):
                st.error("❌ SECURITY ERROR: Invalid Wallet Address format. Must start with '0x' and be exactly 42 characters long.")
                st.stop() # Detiene la ejecución para no llamar a la API
                
            tracker = BlockchainTracker()
            try:
                with st.spinner("Fetching data from blockchain..."):
                    txs = tracker.get_transactions(address_input, chain_id=chain_id)
                    
                if not txs:
                    st.error("Failed to fetch transactions.")
                    st.session_state['txs'] = None
                    st.session_state['graph'] = None
                else:
                    graph = tracker.build_fund_flow_graph(txs)
                    st.session_state['txs'] = txs
                    st.session_state['graph'] = graph
                    st.session_state['address'] = address_input
                    st.session_state['chain'] = network[0]
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col_output:
        st.markdown("### Forensic Results")
        
        if 'graph' in st.session_state and st.session_state['graph'] is not None:
            graph = st.session_state['graph']
            txs = st.session_state['txs']
            address = st.session_state['address']
            chain = st.session_state['chain']
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Transactions", len(txs))
            c2.metric("Wallets Involved", graph.number_of_nodes())
            
            if len(txs) > 15 or graph.number_of_nodes() > 10:
                c3.error("Level: HIGH")
            else:
                c3.warning("Level: MEDIUM")
            
            st.markdown(f"#### 🕸️ Transaction Graph ({chain})")
            if graph.number_of_nodes() > 0:
                net = Network(height="400px", width="100%", bgcolor="#111111", font_color="#00ff41", directed=True)
                net.from_nx(graph)
                
                for node in net.nodes:
                    if node['id'].lower() == address.lower():
                        node['color'] = '#ff00ff' 
                        node['size'] = 30
                    else:
                        node['color'] = '#00ffff' 
                        node['size'] = 15
                        
                net.set_options("""
                var options = {"physics": {"forceAtlas2Based": {"gravitationalConstant": -50, "centralGravity": 0.01, "springLength": 100}, "solver": "forceAtlas2Based"}}
                """)
                
                html_content = net.generate_html()
                st.components.v1.html(html_content, height=400)
            else:
                st.info("No graph data to display.")
            
            st.markdown("#### Recent Fund Movements")
            table_data = []
            for tx in txs:
                val = int(tx["value"]) / 10**18
                if val > 0:
                    table_data.append({
                        "Sender": tx['from'][:10] + "...",
                        "Receiver": tx['to'][:10] + "...",
                        "Value": f"{val:.4f}",
                        "Hash": tx['hash'][:10] + "..."
                    })
            
            if table_data:
                df = pd.DataFrame(table_data)
                st.dataframe(df, width="stretch")
                
                json_report = df.to_json(orient="records", indent=4)
                st.download_button(
                    label="⬇️ Download Evidence (JSON)",
                    data=json_report,
                    file_name=f"report_{address[:8]}.json",
                    mime="application/json"
                )
            else:
                st.info("No direct native token transfers found.")
                
        else:
            st.info("Waiting for input... Enter a wallet address on the left to begin.")

# ==========================================
# FOOTER DISCLAIMER
# ==========================================
st.markdown(
    '<div class="footer">Built for Defensive Cybersecurity & Threat Intelligence. Public Blockchain Data Only. © 2026 Gustavo Ramos.</div>', 
    unsafe_allow_html=True
)