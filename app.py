"""
TraderTraitor-Trace: Main Dashboard.
A unified UI for OSINT and Blockchain Forensics.
"""

import streamlit as st
import pandas as pd
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
    
    # Área de texto para el mensaje
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
            
            # Métricas visuales
            col1, col2 = st.columns(2)
            col1.metric("Risk Score", f"{result['risk_score']}/100")
            
            if result['risk_score'] >= 70:
                col2.error(f"Risk Level: {result['risk_level']}")
            elif result['risk_score'] >= 40:
                col2.warning(f"Risk Level: {result['risk_level']}")
            else:
                col2.success(f"Risk Level: {result['risk_level']}")
                
            # Mostrar los hallazgos (Red Flags)
            st.subheader("Red Flags Detected:")
            for finding in result['findings']:
                st.write(finding)


# ==========================================
# PESTAÑA 2: Rastreador Blockchain
# ==========================================
with tab_blockchain:
    st.header("On-Chain Fund Tracker")
    st.write("Trace the flow of funds from known hacker wallets.")
    
    # Input de la dirección
    address_input = st.text_input(
        "Wallet Address (Ethereum):", 
        value="0x28C6c06298d514Db089934071355E5743bf21d60"
    )
    
    if st.button("Trace Funds", type="primary"):
        tracker = BlockchainTracker()
        tracker.target_address = address_input
        
        with st.spinner("Connecting to Etherscan V2 API..."):
            txs = tracker.get_transactions(address_input)
            
            if txs:
                graph = tracker.build_fund_flow_graph(txs)
                
                st.divider()
                st.subheader("Forensic Analysis")
                
                # Métricas del grafo
                col1, col2, col3 = st.columns(3)
                col1.metric("Transactions Found", len(txs))
                col2.metric("Wallets Involved", graph.number_of_nodes())
                col3.metric("Connections", graph.number_of_edges())
                
                st.subheader("Recent Fund Movements")
                
                # Crear un DataFrame para mostrar una tabla bonita
                table_data = []
                for tx in txs:
                    eth_value = int(tx["value"]) / 10**18
                    # Solo mostramos transacciones que muevan ETH
                    if eth_value > 0:
                        table_data.append({
                            "Sender": tx['from'][:10] + "...",
                            "Receiver": tx['to'][:10] + "...",
                            "Value (ETH)": f"{eth_value:.4f}",
                            "Hash": tx['hash'][:10] + "..."
                        })
                
                if table_data:
                    df = pd.DataFrame(table_data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No direct ETH transfers found in the last transactions (only token transfers).")
            else:
                st.error("Failed to fetch transactions. Check the address or your API Key.")