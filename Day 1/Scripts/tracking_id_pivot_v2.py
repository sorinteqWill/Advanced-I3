import sys
import subprocess

# --- DEPENDENCY BOOTSTRAPPER ---
def ensure_deps():
    deps = {
        "termcolor": "termcolor",
        "requests": "requests"
    }
    for pkg, module in deps.items():
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Missing '{pkg}'. Auto-installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

ensure_deps()
# -------------------------------

import re
import requests
from urllib.parse import urlparse
from termcolor import colored


def is_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def load_content(source: str) -> str | None:
    if is_url(source):
        print(colored(f"[*] Fetching URL: {source}", "cyan"))
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(source, headers=headers, timeout=20)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(colored(f"[-] Failed to fetch URL: {source}", "red"))
            print(colored(f"    Error: {e}", "red"))
            return None
    else:
        print(colored(f"[*] Reading local file: {source}", "cyan"))
        try:
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(colored(f"[-] Failed to read file: {source}", "red"))
            print(colored(f"    Error: {e}", "red"))
            return None


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_window(content: str, start: int, end: int, radius: int = 120) -> str:
    left = max(0, start - radius)
    right = min(len(content), end + radius)
    return clean_text(content[left:right])


def near_analytics_context(content: str, start: int, end: int, radius: int = 180) -> bool:
    left = max(0, start - radius)
    right = min(len(content), end + radius)
    window = content[left:right].lower()

    analytics_terms = [
        "gtag",
        "googletagmanager",
        "google-analytics",
        "analytics.js",
        "gtm.js",
        "measurement_id",
        "datalayer",
        "fbq(",
        "connect.facebook.net",
        "ttq.",
        "_linkedin_partner_id",
        "hotjar",
        "_hjsettings",
        "_paq",
        "matomo",
        "piwik",
        "bat.bing.com"
    ]
    return any(term in window for term in analytics_terms)


def add_result(results: dict, platform: str, value: str, context: str):
    results.setdefault(platform, {})
    if value not in results[platform]:
        results[platform][value] = context


def scan_tracking(source: str):
    print(colored("--- SCANNING FOR PUBLIC TRACKER IDS / TELEMETRY INDICATORS ---", "blue"))

    content = load_content(source)
    if content is None:
        return

    results = {}

    strong_patterns = {
        "Universal Analytics": [
            r"\b(UA-\d{4,10}-\d{1,4})\b"
        ],
        "GA4 Measurement ID": [
            r"""gtag\s*\(\s*['"]config['"]\s*,\s*['"](G-[A-Z0-9]{8,16})['"]""",
            r"""['"]measurement_id['"]\s*[:=]\s*['"](G-[A-Z0-9]{8,16})['"]""",
            r"""googletagmanager\.com/gtag/js\?id=(G-[A-Z0-9]{8,16})"""
        ],
        "Google Tag Manager": [
            r"\b(GTM-[A-Z0-9]{4,10})\b"
        ],
        "Google Ads Conversion ID": [
            r"\b(AW-\d{6,20})\b"
        ],
        "Meta Pixel ID": [
            r"""fbq\s*\(\s*['"]init['"]\s*,\s*['"](\d{5,20})['"]"""
        ],
        "Hotjar Site ID": [
            r"""hjid\s*[:=]\s*(\d{4,12})""",
            r"""_hjSettings\s*=\s*\{[^}]*hjid\s*:\s*(\d{4,12})"""
        ],
        "Segment Write Key": [
            r"""analytics\.load\s*\(\s*['"]([A-Za-z0-9]{10,64})['"]\s*\)"""
        ],
        "Matomo Site ID": [
            r"""_paq\.push\(\s*\[\s*['"]setSiteId['"]\s*,\s*['"]?(\d{1,10})['"]?\s*\]\s*\)"""
        ],
        "TikTok Pixel ID": [
            r"""ttq\.load\s*\(\s*['"]([A-Za-z0-9]{6,32})['"]\s*\)"""
        ],
        "LinkedIn Insight Tag Partner ID": [
            r"""_linkedin_partner_id\s*=\s*['"]?(\d{5,20})['"]?"""
        ],
        "Twitter / X Pixel ID": [
            r"""twq\s*\(\s*['"]init['"]\s*,\s*['"]([A-Za-z0-9]{5,25})['"]"""
        ]
    }

    for platform, regex_list in strong_patterns.items():
        for pattern in regex_list:
            for match in re.finditer(pattern, content, flags=re.DOTALL):
                groups = [g for g in match.groups() if g]
                if not groups:
                    continue
                value = groups[0].strip()
                context = extract_window(content, match.start(), match.end())
                add_result(results, platform, value, context)

    # Balanced GA4 fallback
    for match in re.finditer(r"\b(G-[A-Z0-9]{8,16})\b", content, flags=re.DOTALL):
        value = match.group(1)
        if near_analytics_context(content, match.start(), match.end()):
            context = extract_window(content, match.start(), match.end())
            add_result(results, "GA4 Measurement ID", value, context)

    presence_patterns = {
        "Google tag library present": r"googletagmanager\.com/gtag/js|googletagmanager\.com/gtm\.js",
        "Google Analytics style code present": r"\bgtag\s*\(|\bdatalayer\b|google-analytics\.com",
        "Meta Pixel style code present": r"\bfbq\s*\(|connect\.facebook\.net",
        "TikTok tracking code present": r"\bttq\s*\(",
        "LinkedIn Insight code present": r"\b_linkedin_partner_id\b|insight\.min\.js",
        "Hotjar code present": r"\bhotjar\b|\bhj\(",
        "Bing UET code present": r"bat\.bing\.com/bat\.js|\bUET\b",
        "Matomo / Piwik code present": r"\b_paq\b|\bmatomo\b|\bpiwik\b"
    }

    indicator_hits = []
    for label, pattern in presence_patterns.items():
        if re.search(pattern, content, flags=re.DOTALL | re.IGNORECASE):
            indicator_hits.append(label)

    found_ids = False
    for platform, values in results.items():
        found_ids = True
        for value, context in sorted(values.items()):
            print(colored(f"[+] Confirmed public ID: {platform} -> {value}", "green", attrs=["bold"]))
            print(f"    [*] Context: ...{context}...")

    if indicator_hits:
        print(colored("\n--- TELEMETRY / TRACKER INDICATORS ---", "blue"))
        for hit in indicator_hits:
            print(colored(f"[~] {hit}", "yellow"))

    if not found_ids and not indicator_hits:
        print(colored("\n[-] No common public tracker IDs or obvious telemetry indicators were found in the raw HTML.", "yellow"))
        print(colored("[*] Interpretation: this script did not find extractable client-side artefacts in the returned source.", "cyan"))
        print(colored("[*] This does NOT prove the site has no tracking, telemetry, or measurement.", "cyan"))
    elif not found_ids and indicator_hits:
        print(colored("\n[*] Summary: tracker/telemetry code appears to be present, but no public ID was extracted from the raw HTML.", "cyan"))
        print(colored("[*] This often means IDs are injected later by JavaScript, consent flows, tag managers, or other runtime logic.", "cyan"))


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "target_archive.html"
    scan_tracking(source)