"""
Blockchain Forensics module.
Connects to Etherscan V2 to trace funds across multiple chains.
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
        self.base_url = "https://api.etherscan.io/v2/api"
        
        # Guardrails
        self.MAX_TRANSACTIONS = 20 
        self.API_RETRY_LIMIT = 3   

    def get_transactions(self, address: str, chain_id: int = 1) -> list:
        """Obtiene las transacciones de una billetera en la red seleccionada."""
        if not self.api_key:
            print("⚠️ Warning: No Etherscan API Key found.")
            return []

        params = {
            "chainid": chain_id, # <--- AQUÍ ESTÁ LA MAGIA PARA MULTI-CHAIN
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
                    print(f"🛡️ [Guardrail] Rate Limit. Retrying... ({attempt+1}/{self.API_RETRY_LIMIT})")
                    time.sleep(2)
                else:
                    print(f"❌ API Error: {data.get('message')} - {data.get('result')}")
                    break
            except Exception as e:
                print(f"Connection error: {e}")
                time.sleep(1)
                
        return []

    def build_fund_flow_graph(self, transactions: list) -> nx.DiGraph:
        """Crea un grafo dirigido con Guardrail de tamaño."""
        G = nx.DiGraph()
        
        for tx in transactions:
            sender = tx["from"]
            receiver = tx["to"]
            eth_value = int(tx["value"]) / 10**18 
            
            if eth_value > 0:
                G.add_edge(sender, receiver, weight=eth_value)
                
                if G.number_of_nodes() > 100:
                    print("🛡️ [Guardrail] Graph node limit reached. Stopping.")
                    break
                
        return G