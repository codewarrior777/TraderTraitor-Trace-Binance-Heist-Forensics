"""
OSINT & Phishing Analyzer module for the TraderTraitor case.
Simulates the detection of the social engineering vector used against the Binance engineer.
"""

import re
from urllib.parse import urlparse

class RecruiterAnalyzer:
    def __init__(self):
        # Indicadores de Compromiso (IOCs) comunes en ataques de TraderTraitor
        self.suspicious_domains = ["linkedin-jobs.com", "career-apply.net", "github-recruiter.io"]
        self.suspicious_keywords = ["urgent", "technical test", "download this file", "run this script", "update your browser"]
        self.malicious_extensions = [".exe", ".bat", ".vbs", ".scr", ".ps1"]

    def extract_urls(self, text: str) -> list:
        """Extracts URLs from the given text."""
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        return re.findall(url_pattern, text)

    def analyze_text(self, text: str) -> dict:
        """Analyzes the recruiter message for red flags."""
        text_lower = text.lower()
        urls = self.extract_urls(text)
        
        findings = []
        risk_score = 0
        
        # 1. Check for suspicious keywords (Urgency and action requests)
        for keyword in self.suspicious_keywords:
            if keyword in text_lower:
                findings.append(f"🚩 Suspicious keyword found: '{keyword}'")
                risk_score += 20

        # 2. Check URLs
        for url in urls:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            if domain in self.suspicious_domains:
                findings.append(f"🔴 Known malicious domain detected: {domain}")
                risk_score += 50
            
            # Check for file downloads in URL
            if any(url.endswith(ext) for ext in self.malicious_extensions):
                findings.append(f"⚠️ Direct download link to executable file: {url}")
                risk_score += 40

        # 3. Check for attachment mentions
        if any(ext in text_lower for ext in self.malicious_extensions):
            findings.append("📎 Mentions an executable file extension (e.g., .exe, .ps1)")
            risk_score += 30

        # Determine risk level
        if risk_score >= 70:
            level = "CRITICAL (High probability of TraderTraitor / Lazarus attack)"
        elif risk_score >= 40:
            level = "HIGH (Proceed with extreme caution)"
        elif risk_score > 0:
            level = "MEDIUM (Suspicious, verify sender)"
        else:
            level = "LOW (Looks clean, but always verify)"

        return {
            "risk_level": level,
            "risk_score": min(risk_score, 100), # Cap at 100
            "findings": findings if findings else ["No obvious red flags found. Stay vigilant."]
        }

# --- Block for quick local testing ---
if __name__ == "__main__":
    print("Testing Phishing Analyzer...")
    # Simulating the message a hacker might send during a fake interview
    fake_message = """
    Hello, we are very interested in your profile. Please check our career-apply.net portal.
    The test is urgent! Please download this file http://career-apply.net/technical_test.exe 
    and run it to update your browser.
    """
    
    analyzer = RecruiterAnalyzer()
    result = analyzer.analyze_text(fake_message)
    
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_level']}")
    for finding in result['findings']:
        print(finding)