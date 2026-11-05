"""
TraderTraitor-Trace: Main Dashboard.
A unified UI for OSINT and Blockchain Forensics with Interactive Graphs.
"""

import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

from src.phishing_analyzer import RecruiterAnalyzer
from src.blockchain_tracker import BlockchainTracker

# Configuración de la página
st.set_page_config(page_title="TraderTraitor Trace", page_icon="🥷", layout="wide")

# Título principal
st.title("🥷 TraderTraitor-Trace: Binance Heist Forensics")
st.markdown("""
**Threat Intelligence & Blockchain Forensics Dashboard.**
This tool analyzes the social engineering vectors and traces the on-chain movement of stolen funds related to the historic Binance hack.
""")

st.divider()

# Creamos dos pestañas para separar las herramientas
tab_osint, tab_blockchain = st.tabs(["🕵️‍♂️ OSINT Phishing Analyzer", "⛓️ Blockchain Forensics"])

# ==========================================
# PESTAÑA 1: Analizador de Phishing (OSINT)
# ==========================================
with tab_osint:
    st.header("Social Engineering Detector")
    st.write("Paste a suspicious recruiter message to check for TraderTraitor attack patterns (urgency, malicious domains, executable files).")
    
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
    st.write("Trace the flow of funds from known hacker wallets.")
    
    address_input = st.text_input(
        "Wallet Address (Ethereum):", 
        value="0x28C6c06298d514Db089934071355E5743bf21d60"
    )
    
    if st.button("Trace Funds", type="primary"):
        tracker = BlockchainTracker()
        tracker.target_address = address_input
        
        try:
            with st.spinner("Connecting to Etherscan V2 API..."):
                txs = tracker.get_transactions(address_input)
            
            if not txs:
                st.error("❌ Failed to fetch transactions. Please verify your Etherscan API Key in the `.env` file or try a different address.")
                st.stop()
                
            graph = tracker.build_fund_flow_graph(txs)
            
            st.divider()
            st.subheader("Forensic Analysis")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Transactions Found", len(txs))
            col2.metric("Wallets Involved", graph.number_of_nodes())
            col3.metric("Connections", graph.number_of_edges())
            
            # --- GRÁFICO INTERACTIVO ---
            st.subheader("🕸️ Interactive Transaction Graph")
            st.write("Drag nodes to explore the network. The red node is the target address.")
            
            if graph.number_of_nodes() > 0:
                net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=True)
                net.from_nx(graph)
                
                # Personalizar los nodos
                for node in net.nodes:
                    if node['id'].lower() == address_input.lower():
                        node['color'] = 'red' 
                        node['size'] = 30
                    else:
                        node['color'] = 'lightblue'
                        node['size'] = 15
                        
                # Renderizar HTML. (Usamos components.v1.html porque PyVis requiere un iframe con JS)
                html_content = net.generate_html()
                st.components.v1.html(html_content, height=600)
                
            else:
                st.info("No graph data to display.")
            
            # 4. Mostrar Tabla
            st.subheader("Recent Fund Movements (ETH Only)")
            table_data = []
            for tx in txs:
                eth_value = int(tx["value"]) / 10**18
                if eth_value > 0:
                    table_data.append({
                        "Sender": tx['from'][:10] + "...",
                        "Receiver": tx['to'][:10] + "...",
                        "Value (ETH)": f"{eth_value:.4f}",
                        "Hash": tx['hash'][:10] + "..."
                    })
            
            if table_data:
                df = pd.DataFrame(table_data)
                # ACTUALIZACIÓN: Se cambió use_container_width por width="stretch"
                st.dataframe(df, width="stretch")
            else:
                st.info("No direct ETH transfers found (the target wallet might only be receiving tokens).")
                
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")