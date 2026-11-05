"""
TraderTraitor-Trace: Ultimate Dashboard.
Includes Multi-Chain support, Interactive Graphs, and Evidence Export.
"""

import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import time

from src.phishing_analyzer import RecruiterAnalyzer
from src.blockchain_tracker import BlockchainTracker

# Configuración de la página
st.set_page_config(page_title="TraderTraitor Trace", page_icon="🥷", layout="wide")

# Título principal
st.title("🥷 TraderTraitor-Trace: Binance Heist Forensics")
st.markdown("""
**Threat Intelligence & Blockchain Forensics Dashboard.**
This tool analyzes social engineering vectors and traces on-chain movements across multiple blockchains.
""")

st.divider()

# Pestañas
tab_osint, tab_blockchain = st.tabs(["🕵️‍♂️ OSINT Phishing Analyzer", "⛓️ Blockchain Forensics"])

# ==========================================
# PESTAÑA 1: Analizador de Phishing (OSINT)
# ==========================================
with tab_osint:
    st.header("Social Engineering Detector")
    st.write("Paste a suspicious recruiter message to check for TraderTraitor attack patterns.")
    
    message_input = st.text_area(
        "Suspicious Message:", 
        height=150,
        placeholder="Hello, please download this file http://career-apply.net/technical_test.exe and run it urgently..."
    )
    
    if st.button("Analyze Message", type="primary"):
        if not message_input.strip():
            st.warning("Please enter a message to analyze.")
        else:
            analyzer = RecruiterAnalyzer()
            result = analyzer.analyze_text(message_input)
            
            st.divider()
            st.subheader("Analysis Results")
            
            col1, col2 = st.columns(2)
            col1.metric("Risk Score", f"{result['risk_score']}/100")
            
            if result['risk_score'] >= 70:
                col2.error(f"Risk Level: {result['risk_level']}")
            elif result['risk_score'] >= 40:
                col2.warning(f"Risk Level: {result['risk_level']}")
            else:
                col2.success(f"Risk Level: {result['risk_level']}")
                
            st.subheader("Red Flags Detected:")
            for finding in result['findings']:
                st.write(finding)


# ==========================================
# PESTAÑA 2: Rastreador Blockchain
# ==========================================
with tab_blockchain:
    st.header("On-Chain Fund Tracker")
    
    col_net, col_addr = st.columns([1, 3])
    
    with col_net:
        # Selector de Red
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
        
    with col_addr:
        address_input = st.text_input(
            "Wallet Address:", 
            value="0x28C6c06298d514Db089934071355E5743bf21d60"
        )
    
    if st.button("Trace Funds", type="primary"):
        tracker = BlockchainTracker()
        
        try:
            with st.spinner(f"Connecting to {network[0]} API..."):
                txs = tracker.get_transactions(address_input, chain_id=chain_id)
            
            if not txs:
                st.error(f"❌ Failed to fetch transactions on {network[0]}. Check the address.")
                st.stop()
                
            graph = tracker.build_fund_flow_graph(txs)
            
            st.divider()
            st.subheader(f"Forensic Analysis ({network[0]})")
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Transactions", len(txs))
            col2.metric("Wallets Involved", graph.number_of_nodes())
            col3.metric("Connections", graph.number_of_edges())
            
            # Threat Intel Scoring (NUEVO)
            if len(txs) > 15 or graph.number_of_nodes() > 10:
                col4.error("Threat Level: HIGH")
            else:
                col4.warning("Threat Level: MEDIUM")
            
            # --- GRÁFICO INTERACTIVO ---
            st.subheader("🕸️ Interactive Transaction Graph")
            
            if graph.number_of_nodes() > 0:
                net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", directed=True)
                net.from_nx(graph)
                
                for node in net.nodes:
                    if node['id'].lower() == address_input.lower():
                        node['color'] = 'red' 
                        node['size'] = 30
                    else:
                        node['color'] = 'lightblue'
                        node['size'] = 15
                        
                html_content = net.generate_html()
                st.components.v1.html(html_content, height=500)
                
            else:
                st.info("No graph data to display.")
            
            # --- TABLA Y EXPORTACIÓN ---
            st.subheader("Recent Fund Movements")
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
                st.dataframe(df, use_container_width=True)
                
                # Botón de descarga de evidencia
                json_report = df.to_json(orient="records", indent=4)
                st.download_button(
                    label="⬇️ Download Forensic Evidence (JSON)",
                    data=json_report,
                    file_name=f"forensic_report_{address_input[:8]}.json",
                    mime="application/json"
                )
            else:
                st.info("No direct native token transfers found in the recent history.")
                
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")