# 🥷 TraderTraitor-Trace: Binance Heist Forensics

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-red.svg)]()
[![Blockchain](https://img.shields.io/badge/Tech-Blockchain-orange.svg)]()
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)]()

An advanced **Blockchain Forensic & Threat Intelligence** tool designed to trace the flow of stolen cryptocurrency.

This project serves as a real-world case study of the **2026 Binance Hack** (a $6.3 billion heist attributed to the North Korean state-sponsored group *TraderTraitor*). The tool analyzes public blockchain data to map the hacker's money laundering network and identifies high-risk addresses.

## 🚨 The Case Study (Context)
- **The Attack:** Hackers used a sophisticated social engineering campaign (fake job interview) to compromise a Binance engineer, ultimately exploiting the EIP-7702 vulnerability to drain hot wallets.
- **The Laundering:** The stolen funds were rapidly dispersed across thousands of wallets and multiple blockchains to obfuscate the trail.
- **The Goal:** This tool aims to demystify the attack by providing visual intelligence on the movement of the stolen assets.

## 🧠 Features

1. **OSINT Phishing Analyzer:** Detects social engineering vectors used against the Binance engineer (urgency, malicious domains, executable files) by analyzing text input.
2. **Blockchain Forensics:** Connects to the Etherscan V2 API to trace the flow of funds, map wallet connections, and build a transaction graph using `NetworkX`.
3. **Guardrail Architecture:** Implements API retry logic and graph size limits to prevent crashes and memory exhaustion (OOM) during large-scale forensic analysis.

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- Etherscan API Key (Free tier)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/TraderTraitor-Trace-Binance-Heist-Forensics.git
   cd TraderTraitor-Trace-Binance-Heist-Forensics
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
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

## 🖥️ Demo

*(You can add screenshots of your Streamlit Dashboard here later)*
- **Tab 1:** Paste a malicious recruiter message and watch the risk score hit 100/100.
- **Tab 2:** Enter a wallet address to see the transaction graph and fund movements.

## 📁 Project Structure

```text
TraderTraitor-Trace/
├── src/
│   ├── phishing_analyzer.py   # OSINT detection logic
│   └── blockchain_tracker.py  # Etherscan API & NetworkX graph builder
├── app.py                     # Streamlit Dashboard UI
├── requirements.txt           # Dependencies
├── .env                       # API Keys (Ignored in git)
└── README.md
```

## 🔒 Ethical Disclaimer
This tool is built for educational and defensive cybersecurity purposes only. It utilizes public blockchain data and should not be used to target or harass individuals. 

---
*Built as a Cybersecurity & InfoSec Portfolio Project.*
```

