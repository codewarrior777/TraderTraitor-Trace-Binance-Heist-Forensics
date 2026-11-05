"""
Blockchain Forensics module.
Connects to Etherscan V2 to trace the flow of funds from known hacker wallets.
Includes API and Graph Guardrails.
"""

import os
import time
import requests
import networkx as nx
from dotenv import load_dotenv

load_dotenv()

class BlockchainTracker:
    def __init__(self):
        self.api_key = os.getenv("ETHERSCAN_API_KEY")
        # ACTUALIZADO: Ahora usamos la API V2
        self.base_url = "https://api.etherscan.io/v2/api"
        # Dirección de ejemplo (Fondo de reserva de Binance)
        self.target_address = "0x28C6c06298d514Db089934071355E5743bf21d60" 
        
        # --- GUARDRAILS ---
        self.MAX_TRANSACTIONS = 20 
        self.API_RETRY_LIMIT = 3   

    def get_transactions(self, address: str) -> list:
        """Obtiene las transacciones de una billetera con Guardrail de reintentos."""
        if not self.api_key:
            print("⚠️ Warning: No Etherscan API Key found in .env")
            return []

        params = {
            "chainid": 1, # ACTUALIZADO: Requerido por la V2 (1 = Ethereum Mainnet)
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": self.api_key
        }
        
        for attempt in range(self.API_RETRY_LIMIT):
            try:
                response = requests.get(self.base_url, params=params, timeout=10)
                data = response.json()
                
                if data["status"] == "1":
                    return data["result"][:self.MAX_TRANSACTIONS]
                
                elif "Max rate limit reached" in data.get("result", ""):
                    print(f"🛡️ [Guardrail] Rate Limit detectado. Reintentando en 2s... (Intento {attempt+1}/{self.API_RETRY_LIMIT})")
                    time.sleep(2)
                else:
                    print(f"❌ Error de API: {data.get('message')} - Detalle: {data.get('result')}")
                    break
            except Exception as e:
                print(f"Error de conexión: {e}")
                time.sleep(1)
                
        return []

    def build_fund_flow_graph(self, transactions: list) -> nx.DiGraph:
        """Crea un grafo dirigido con un Guardrail para limitar el tamaño."""
        G = nx.DiGraph()
        
        for tx in transactions:
            sender = tx["from"]
            receiver = tx["to"]
            eth_value = int(tx["value"]) / 10**18 
            
            if eth_value > 0:
                G.add_edge(sender, receiver, weight=eth_value)
                
                if G.number_of_nodes() > 100:
                    print("🛡️ [Guardrail] Límite de nodos alcanzado. Deteniendo construcción del grafo para proteger la memoria.")
                    break
                
        return G

# --- Bloque de prueba ---
if __name__ == "__main__":
    print("🕵️‍♂️ Iniciando Rastreo Forense...")
    tracker = BlockchainTracker()
    
    print(f"Buscando transacciones para: {tracker.target_address[:10]}...")
    txs = tracker.get_transactions(tracker.target_address)
    
    if txs:
        print(f"✅ Se encontraron {len(txs)} transacciones recientes.")
        graph = tracker.build_fund_flow_graph(txs)
        
        print(f"📊 Grafo creado con {graph.number_of_nodes()} billeteras y {graph.number_of_edges()} conexiones.")
        print("\nÚltimos movimientos de fondos:")
        
        for tx in txs[:5]:
            eth_value = int(tx["value"]) / 10**18
            if eth_value > 0:
                print(f"  -> {eth_value:.4f} ETH enviados de {tx['from'][:8]}... a {tx['to'][:8]}...")
    else:
        print("No se pudieron obtener transacciones. Verifica tu API Key o intenta más tarde.")