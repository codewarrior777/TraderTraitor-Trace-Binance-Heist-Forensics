# 🥷 TraderTraitor-Trace: Binance Heist Forensics

[![Live Demo](https://img.shields.io/badge/demo-LIVE-brightgreen?style=for-the-badge&logo=streamlit)](https://tradertraitor-trace-binance-heist-forensics-c55d8ematrrgxukdmw.streamlit.app/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tradertraitor-trace-binance-heist-forensics-c55d8ematrrgxukdmw.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-red.svg)]()
[![Blockchain](https://img.shields.io/badge/Tech-Blockchain-orange.svg)]()

An advanced **Blockchain Forensic & Threat Intelligence** tool designed to trace the flow of stolen cryptocurrency.

This project serves as a real-world case study of the **2026 Binance Hack** (a $6.3 billion heist attributed to the North Korean state-sponsored group *TraderTraitor*). The tool analyzes public blockchain data to map the hacker's money laundering network and identifies high-risk addresses.

## 🌐 Try It Live

🔴 **[Open the Interactive Dashboard Here](https://tradertraitor-trace-binance-heist-forensics-c55d8ematrrgxukdmw.streamlit.app/)**

No installation needed — just click and explore the OSINT analyzer and the interactive blockchain graph in your browser.

## 🚨 The Case Study (Context)
- **The Attack:** Hackers used a sophisticated social engineering campaign (a fake job interview) to compromise a Binance engineer, ultimately exploiting the EIP-7702 vulnerability to drain hot wallets.
- **The Laundering:** The stolen funds were rapidly dispersed across thousands of wallets and multiple blockchains to obfuscate the trail.
- **The Goal:** This tool aims to demystify the attack by providing visual intelligence on the movement of stolen assets.

## 🧠 Features

1. **OSINT Phishing Analyzer:** Detects social engineering vectors used against the Binance engineer (urgency, malicious domains, executable files) by analyzing text input using heuristic rules.
2. **Blockchain Forensics:** Connects to the Etherscan V2 API to trace the flow of funds, map wallet connections, and build a transaction graph using `NetworkX`.
3. **Interactive Visualization:** Uses `PyVis` to generate a dynamic, draggable network graph of the transactions directly in the browser.
4. **Guardrail Architecture:** Implements API retry logic and graph size limits to prevent crashes and memory exhaustion (OOM) during large-scale forensic analysis.

## 🖥️ Dashboard Preview

*(When viewing the live app, you will see two main tabs)*:
- **🕵️‍♂️ OSINT Phishing Analyzer:** Paste a malicious recruiter message and watch the risk score hit 100/100 with detailed red flags.
- **⛓️ Blockchain Forensics:** Enter a wallet address to see the interactive transaction graph and the latest ETH fund movements.

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10+
- Etherscan API Key (Free tier at [etherscan.io](https://etherscan.io/apis))

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/codewarrior777/TraderTraitor-Trace-Binance-Heist-Forensics.git
   cd TraderTraitor-Trace-Binance-Heist-Forensics
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   # source .venv/bin/activate     # macOS/Linux
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add your Etherscan API key:
   ```env
   ETHERSCAN_API_KEY="your_api_key_here"
   ```

4. Run the Threat Intelligence Dashboard:
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```text
TraderTraitor-Trace/
├── src/
│   ├── phishing_analyzer.py   # OSINT detection logic (Regex-based)
│   └── blockchain_tracker.py  # Etherscan API V2 & NetworkX graph builder
├── app.py                     # Streamlit Dashboard UI (OSINT + PyVis)
├── requirements.txt           # Dependencies
├── .gitignore                 # Excludes .env and lib/
└── README.md
```

## 🔒 Ethical Disclaimer
This tool is built strictly for **educational and defensive cybersecurity purposes**. It utilizes public blockchain data and should not be used to target or harass individuals. 

---
*Built as a Cybersecurity & InfoSec Portfolio Project by Gustavo Ramos.*
```

