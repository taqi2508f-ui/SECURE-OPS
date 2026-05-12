import streamlit as st
import subprocess
import json
import datetime
import random
import requests
import os

st.set_page_config(
    page_title="SecureOps Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

:root {
    --bg:       #0a0e17;
    --surface:  #111827;
    --card:     #161f30;
    --border:   #1e3a5f;
    --accent:   #00d4ff;
    --accent2:  #00ff88;
    --warn:     #ffaa00;
    --danger:   #ff4455;
    --text:     #c8d8e8;
    --muted:    #5a7a9a;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Cards */
.sec-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.sec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent);
}
.sec-card.warn::before { background: var(--warn); }
.sec-card.danger::before { background: var(--danger); }
.sec-card.success::before { background: var(--accent2); }

/* Metric boxes */
.metric-row { display: flex; gap: 12px; margin-bottom: 20px; }
.metric-box {
    flex: 1;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}
.metric-val {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2rem;
    color: var(--accent);
    display: block;
}
.metric-val.warn  { color: var(--warn); }
.metric-val.danger { color: var(--danger); }
.metric-val.ok    { color: var(--accent2); }
.metric-label { font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

/* Mono text */
.mono { font-family: 'Share Tech Mono', monospace; font-size: 0.85rem; color: var(--accent); }
.mono-sm { font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; color: var(--muted); }

/* Header */
.site-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 24px;
}
.site-header h1 {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    color: var(--accent);
    letter-spacing: 3px;
    margin: 0;
}
.site-header .tagline { color: var(--muted); font-size: 0.85rem; letter-spacing: 2px; }

/* Tables */
.data-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.data-table th { color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-size: 0.7rem; border-bottom: 1px solid var(--border); padding: 8px; text-align: left; }
.data-table td { padding: 10px 8px; border-bottom: 1px solid #1a2a3a; }
.data-table tr:last-child td { border-bottom: none; }

/* Badges */
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-family: 'Share Tech Mono', monospace; font-weight: 600; letter-spacing: 1px; }
.badge-crit  { background: rgba(255,68,85,0.15);  color: var(--danger); border: 1px solid rgba(255,68,85,0.3); }
.badge-high  { background: rgba(255,170,0,0.15);  color: var(--warn);   border: 1px solid rgba(255,170,0,0.3); }
.badge-med   { background: rgba(0,212,255,0.1);   color: var(--accent); border: 1px solid rgba(0,212,255,0.2); }
.badge-low   { background: rgba(0,255,136,0.1);   color: var(--accent2);border: 1px solid rgba(0,255,136,0.2); }
.badge-info  { background: rgba(90,122,154,0.2);  color: var(--muted);  border: 1px solid rgba(90,122,154,0.3); }

/* Buttons */
.stButton button {
    background: transparent !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    border-radius: 4px !important;
}
.stButton button:hover {
    background: rgba(0,212,255,0.1) !important;
}

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Log viewer */
.log-viewer {
    background: #050a10;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent2);
    max-height: 280px;
    overflow-y: auto;
    line-height: 1.7;
}
.log-viewer .log-err  { color: var(--danger); }
.log-viewer .log-warn { color: var(--warn); }
.log-viewer .log-info { color: var(--muted); }

/* Status dot */
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.dot-green  { background: var(--accent2); box-shadow: 0 0 6px var(--accent2); }
.dot-yellow { background: var(--warn);    box-shadow: 0 0 6px var(--warn); }
.dot-red    { background: var(--danger);  box-shadow: 0 0 6px var(--danger); }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────
if "scan_results" not in st.session_state:
    st.session_state.scan_results = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "alerts" not in st.session_state:
    st.session_state.alerts = [
        {"time": "08:14", "host": "192.168.1.10", "msg": "SSH brute-force detected (24 attempts)", "level": "danger"},
        {"time": "09:02", "host": "192.168.1.22", "msg": "Outdated OpenSSL 1.0.2 detected", "level": "warn"},
        {"time": "09:45", "host": "192.168.1.5",  "msg": "Port 23 (Telnet) open — unencrypted", "level": "warn"},
        {"time": "10:30", "host": "192.168.1.1",  "msg": "All ports nominal", "level": "ok"},
    ]

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px'>
      <div style='font-family:Share Tech Mono,monospace;font-size:1.1rem;color:#00d4ff;letter-spacing:3px'>SECUREOPS</div>
      <div style='font-size:0.7rem;color:#5a7a9a;letter-spacing:2px'>DEFENSIVE LAB v1.0</div>
    </div>
    <hr style='border-color:#1e3a5f;margin:0 0 16px'>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🏠  Dashboard",
        "🔍  Network Scanner",
        "🛡️  Vulnerability Tracker",
        "🎓  Awareness Trainer",
        "📊  Threat Analyzer",
        "📄  Report Generator",
        "🤖  AI Assistant",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#1e3a5f;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:#5a7a9a;letter-spacing:1px;padding:0 4px'>
      <div style='margin-bottom:6px'><span class='dot dot-green'></span>All systems nominal</div>
      <div style='margin-bottom:6px'><span class='dot dot-yellow'></span>2 open findings</div>
      <div style='color:#2a4a6a;margin-top:12px'>⚠ AUTHORIZED USE ONLY<br>Scan only hosts you own<br>or have written consent for.</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════
if "Dashboard" in page:
    st.markdown("""
    <div class='site-header'>
      <h1>🛡 SECUREOPS LAB</h1>
      <div class='tagline'>DEFENSIVE SECURITY OPERATIONS PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.markdown("""
    <div class='metric-row'>
      <div class='metric-box'>
        <span class='metric-val'>12</span>
        <span class='metric-label'>Hosts Scanned</span>
      </div>
      <div class='metric-box'>
        <span class='metric-val warn'>3</span>
        <span class='metric-label'>Open Findings</span>
      </div>
      <div class='metric-box'>
        <span class='metric-val danger'>1</span>
        <span class='metric-label'>Critical CVEs</span>
      </div>
      <div class='metric-box'>
        <span class='metric-val ok'>94%</span>
        <span class='metric-label'>Awareness Score</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("<div class='sec-card'>", unsafe_allow_html=True)
        st.markdown("**Recent Alerts**")
        rows = ""
        for a in st.session_state.alerts:
            badge = {"danger": "badge-crit", "warn": "badge-high", "ok": "badge-low"}.get(a["level"], "badge-info")
            label = {"danger": "HIGH", "warn": "MED", "ok": "OK"}.get(a["level"], "INFO")
            rows += f"""<tr>
              <td class='mono-sm'>{a['time']}</td>
              <td class='mono-sm'>{a['host']}</td>
              <td>{a['msg']}</td>
              <td><span class='badge {badge}'>{label}</span></td>
            </tr>"""
        st.markdown(f"""
        <table class='data-table'>
          <thead><tr><th>Time</th><th>Host</th><th>Event</th><th>Sev.</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sec-card success'>", unsafe_allow_html=True)
        st.markdown("**System Status**")
        services = [
            ("Network Scanner", "dot-green", "Ready"),
            ("CVE Database", "dot-green", "NVD synced 2h ago"),
            ("AI Assistant", "dot-yellow", "API key needed"),
            ("Log Analyzer", "dot-green", "Monitoring"),
            ("Report Engine", "dot-green", "Ready"),
        ]
        for name, dot, status in services:
            st.markdown(f"<div style='margin:8px 0;font-size:0.85rem'><span class='dot {dot}'></span><b>{name}</b> <span style='color:var(--muted);font-size:0.75rem'>— {status}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='sec-card warn' style='margin-top:0'>", unsafe_allow_html=True)
        st.markdown("**Quick Actions**")
        if st.button("▶ Run Quick Scan"):
            st.info("Navigate to Network Scanner to configure targets.")
        if st.button("📥 Pull Latest CVEs"):
            st.info("Navigate to Vulnerability Tracker.")
        if st.button("📄 Generate Report"):
            st.info("Navigate to Report Generator.")
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: NETWORK SCANNER
# ══════════════════════════════════════════════════════════════
elif "Network Scanner" in page:
    st.markdown("<h2 style='color:var(--accent);letter-spacing:2px'>🔍 NETWORK SCANNER</h2>", unsafe_allow_html=True)
    st.markdown("<div class='sec-card warn'><b>⚠ Authorization Gate</b> — Only scan hosts you own or have explicit written permission to test. Unauthorized scanning is illegal.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        target = st.text_input("Target IP / Range", placeholder="192.168.1.0/24 or 192.168.1.10")
        scan_type = st.selectbox("Scan Profile", [
            "Quick scan (-T4 -F)",
            "Service detection (-sV)",
            "OS detection (-O)",
            "Full port scan (-p-)",
        ])
    with col2:
        authorized = st.checkbox("✅ I confirm I am authorized to scan this target")
        notes = st.text_area("Authorization notes / scope reference", height=80, placeholder="e.g. Lab network — home router + test VMs")

    if st.button("▶ Start Scan") and authorized and target:
        flag_map = {
            "Quick scan (-T4 -F)":      ["-T4", "-F"],
            "Service detection (-sV)":  ["-sV", "-T4"],
            "OS detection (-O)":        ["-O", "-T4"],
            "Full port scan (-p-)":     ["-p-", "-T4"],
        }
        flags = flag_map[scan_type]
        with st.spinner("Scanning…"):
            try:
                result = subprocess.run(
                    ["nmap"] + flags + [target],
                    capture_output=True, text=True, timeout=120
                )
                output = result.stdout or result.stderr
            except FileNotFoundError:
                output = "[ERROR] nmap not found. Install with: sudo apt install nmap"
            except subprocess.TimeoutExpired:
                output = "[ERROR] Scan timed out after 120s"

        st.session_state.scan_results.append({
            "time": datetime.datetime.now().strftime("%H:%M:%S"),
            "target": target,
            "type": scan_type,
            "output": output
        })
        st.markdown(f"<div class='log-viewer'>{output.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    elif st.button("▶ Start Scan") and not authorized:
        st.error("You must confirm authorization before scanning.")

    if st.session_state.scan_results:
        st.markdown("### Scan History")
        for r in reversed(st.session_state.scan_results[-5:]):
            with st.expander(f"[{r['time']}] {r['target']} — {r['type']}"):
                st.code(r["output"], language="text")


# ══════════════════════════════════════════════════════════════
# PAGE: VULNERABILITY TRACKER
# ══════════════════════════════════════════════════════════════
elif "Vulnerability" in page:
    st.markdown("<h2 style='color:var(--accent);letter-spacing:2px'>🛡️ VULNERABILITY TRACKER</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        cve_id = st.text_input("Search CVE ID", placeholder="CVE-2024-1234")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search = st.button("🔍 Lookup CVE")

    if search and cve_id:
        cve_clean = cve_id.strip().upper()
        with st.spinner(f"Querying NVD for {cve_clean}…"):
            try:
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_clean}"
                r = requests.get(url, timeout=10)
                data = r.json()
                vulns = data.get("vulnerabilities", [])
                if vulns:
                    cve_data = vulns[0]["cve"]
                    desc = cve_data.get("descriptions", [{}])[0].get("value", "No description")
                    metrics = cve_data.get("metrics", {})
                    score = "N/A"
                    severity = "UNKNOWN"
                    if "cvssMetricV31" in metrics:
                        m = metrics["cvssMetricV31"][0]["cvssData"]
                        score = m.get("baseScore", "N/A")
                        severity = m.get("baseSeverity", "UNKNOWN")
                    elif "cvssMetricV2" in metrics:
                        m = metrics["cvssMetricV2"][0]["cvssData"]
                        score = m.get("baseScore", "N/A")
                        severity = metrics["cvssMetricV2"][0].get("baseSeverity", "UNKNOWN")

                    badge_map = {"CRITICAL": "badge-crit", "HIGH": "badge-high", "MEDIUM": "badge-med", "LOW": "badge-low"}
                    badge = badge_map.get(severity, "badge-info")

                    st.markdown(f"""
                    <div class='sec-card'>
                      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'>
                        <span class='mono'>{cve_clean}</span>
                        <span><span class='badge {badge}'>{severity}</span> &nbsp; <span class='mono' style='font-size:1.2rem'>{score}</span></span>
                      </div>
                      <p style='color:var(--text);font-size:0.9rem;line-height:1.6'>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(f"No data found for {cve_clean}")
            except Exception as e:
                st.error(f"NVD API error: {e}")

    # Static sample findings table
    st.markdown("### Current Findings")
    sample = [
        ("CVE-2024-3094", "192.168.1.10", "XZ Utils backdoor", "CRITICAL", "9.8", "Patch immediately"),
        ("CVE-2023-44487", "192.168.1.22", "HTTP/2 Rapid Reset", "HIGH",     "7.5", "Update nginx/Apache"),
        ("CVE-2023-23397", "192.168.1.5",  "Outlook NTLM leak",  "HIGH",     "9.8", "Apply MS patch"),
        ("CVE-2022-0778",  "192.168.1.1",  "OpenSSL inf loop",   "MEDIUM",   "5.3", "Upgrade OpenSSL"),
    ]
    rows = ""
    for cve, host, name, sev, score, action in sample:
        badge_map = {"CRITICAL": "badge-crit", "HIGH": "badge-high", "MEDIUM": "badge-med"}
        badge = badge_map.get(sev, "badge-info")
        rows += f"<tr><td class='mono-sm'>{cve}</td><td class='mono-sm'>{host}</td><td>{name}</td><td><span class='badge {badge}'>{sev}</span></td><td class='mono'>{score}</td><td style='color:var(--muted);font-size:0.8rem'>{action}</td></tr>"

    st.markdown(f"""
    <div class='sec-card'>
    <table class='data-table'>
      <thead><tr><th>CVE</th><th>Host</th><th>Vulnerability</th><th>Severity</th><th>Score</th><th>Action</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: AWARENESS TRAINER
# ══════════════════════════════════════════════════════════════
elif "Awareness" in page:
    st.markdown("<h2 style='color:var(--accent);letter-spacing:2px'>🎓 PHISHING AWARENESS TRAINER</h2>", unsafe_allow_html=True)
    st.markdown("<div class='sec-card'>This module trains your team to recognize phishing attempts. No real emails are sent externally — all scenarios run inside your browser.</div>", unsafe_allow_html=True)

    scenarios = [
        {
            "from": "IT-Support <it-supp0rt@company-secure.net>",
            "subject": "URGENT: Your account will be suspended in 24h",
            "body": "Dear Employee,\n\nWe detected unusual activity on your account. You must verify your credentials immediately to avoid suspension.\n\nClick here to verify: http://company-secure.net.malicious.io/login\n\nIT Security Team",
            "red_flags": ["Spoofed domain (company-secure.net.malicious.io)", "Urgency/pressure tactic", "Generic greeting", "Suspicious link domain"],
            "answer": "Phishing"
        },
        {
            "from": "newsletter@github.com",
            "subject": "Your monthly GitHub digest — May 2026",
            "body": "Hi there,\n\nHere's what happened on GitHub this month across your repositories and the projects you follow...\n\nView your digest on GitHub →\n\nYou're receiving this because you subscribed to GitHub newsletters.",
            "red_flags": [],
            "answer": "Legitimate"
        },
        {
            "from": "paypa1-security@paypai.com",
            "subject": "Action required: Confirm your payment method",
            "body": "Your PayPal account has been limited. To restore full access, please confirm your payment details.\n\nLog in at: http://paypal.confirm-details.ru/secure\n\nFailure to act within 48 hours will result in permanent suspension.",
            "red_flags": ["Typosquatted sender (paypa1, paypai)", "Foreign TLD (.ru)", "Urgency threat", "Not addressed to you by name"],
            "answer": "Phishing"
        },
    ]

    if "scenario_idx" not in st.session_state:
        st.session_state.scenario_idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.last_correct = None

    idx = st.session_state.scenario_idx % len(scenarios)
    sc = scenarios[idx]

    st.markdown(f"""
    <div class='sec-card'>
      <div style='margin-bottom:12px'>
        <span class='mono-sm'>FROM: </span><span style='color:var(--text)'>{sc['from']}</span><br>
        <span class='mono-sm'>SUBJ: </span><b style='color:var(--text)'>{sc['subject']}</b>
      </div>
      <div style='background:#050a10;border-radius:6px;padding:14px;font-size:0.85rem;line-height:1.8;white-space:pre-wrap;color:var(--text)'>{sc['body']}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answered:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚨 Mark as Phishing"):
                st.session_state.answered = True
                st.session_state.last_correct = ("Phishing" == sc["answer"])
                if st.session_state.last_correct:
                    st.session_state.score += 1
        with c2:
            if st.button("✅ Mark as Legitimate"):
                st.session_state.answered = True
                st.session_state.last_correct = ("Legitimate" == sc["answer"])
                if st.session_state.last_correct:
                    st.session_state.score += 1
    else:
        correct = st.session_state.last_correct
        if correct:
            st.success(f"✅ Correct! This was **{sc['answer']}**.")
        else:
            st.error(f"❌ Incorrect. This was **{sc['answer']}**.")

        if sc["red_flags"]:
            st.markdown("**Red flags in this email:**")
            for flag in sc["red_flags"]:
                st.markdown(f"<div style='color:var(--warn);font-size:0.85rem;margin:4px 0'>⚠ {flag}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:var(--accent2);font-size:0.85rem'>✔ No red flags — this email is from a legitimate sender.</div>", unsafe_allow_html=True)

        if st.button("Next Scenario →"):
            st.session_state.scenario_idx += 1
            st.session_state.answered = False
            st.rerun()

    st.markdown(f"<br><div class='mono' style='text-align:right'>Score: {st.session_state.score} / {st.session_state.scenario_idx}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: THREAT ANALYZER
# ══════════════════════════════════════════════════════════════
elif "Threat" in page:
    st.markdown("<h2 style='color:var(--accent);letter-spacing:2px'>📊 THREAT ANALYZER</h2>", unsafe_allow_html=True)

    log_input = st.text_area("Paste auth/syslog entries here", height=180, placeholder="/var/log/auth.log or Windows Event Log entries...")

    if st.button("🔍 Analyze Logs"):
        if log_input.strip():
            lines = log_input.strip().split("\n")
            findings = []
            for line in lines:
                l = line.lower()
                if "failed password" in l or "authentication failure" in l:
                    findings.append(("HIGH", "Brute-force indicator", line[:80]))
                elif "invalid user" in l:
                    findings.append(("MEDIUM", "Unknown user login attempt", line[:80]))
                elif "accepted password" in l or "session opened" in l:
                    findings.append(("INFO", "Successful login", line[:80]))
                elif "sudo" in l and "command" in l:
                    findings.append(("MEDIUM", "Privilege escalation (sudo)", line[:80]))
                elif "port scan" in l or "nmap" in l:
                    findings.append(("HIGH", "Scan activity detected", line[:80]))
                else:
                    findings.append(("INFO", "Nominal event", line[:80]))

            rows = ""
            for sev, label, raw in findings:
                badge_map = {"HIGH": "badge-high", "MEDIUM": "badge-med", "INFO": "badge-info"}
                badge = badge_map.get(sev, "badge-info")
                rows += f"<tr><td><span class='badge {badge}'>{sev}</span></td><td>{label}</td><td class='mono-sm'>{raw}</td></tr>"

            st.markdown(f"""
            <div class='sec-card'>
            <table class='data-table'>
              <thead><tr><th>Severity</th><th>Finding</th><th>Raw</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
            </div>
            """, unsafe_allow_html=True)

            high_count = sum(1 for s, _, _ in findings if s == "HIGH")
            if high_count:
                st.error(f"⚠ {high_count} high-severity event(s) detected. Review immediately.")
        else:
            st.warning("Paste some log data to analyze.")


# ══════════════════════════════════════════════════════════════
# PAGE: REPORT GENERATOR
# ══════════════════════════════════════════════════════════════
elif "Report" in page:
    st.markdown("<h2 style='color:var(--accent);letter-spacing:2px'>📄 REPORT GENERATOR</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        org = st.text_input("Organization", placeholder="Acme Corp")
        assessor = st.text_input("Assessor Name", placeholder="Your name")
        scope = st.text_area("Scope", placeholder="192.168.1.0/24 — internal lab network", height=80)
    with col2:
        date = st.date_input("Assessment Date", datetime.date.today())
        include_scans = st.checkbox("Include scan results", value=True)
        include_vulns = st.checkbox("Include vulnerability findings", value=True)
        include_recs = st.checkbox("Include remediation recommendations", value=True)

    if st.button("📄 Generate Report"):
        report = f"""
SECUREOPS LAB — SECURITY ASSESSMENT REPORT
==========================================
Organization : {org or 'N/A'}
Assessor     : {assessor or 'N/A'}
Date         : {date}
Scope        : {scope or 'N/A'}

EXECUTIVE SUMMARY
-----------------
This report summarizes the findings from a defensive security assessment
conducted on the above-mentioned scope. All scanning and testing was
performed on authorized systems only.

"""
        if include_scans and st.session_state.scan_results:
            report += "SCAN RESULTS\n" + "-"*40 + "\n"
            for r in st.session_state.scan_results:
                report += f"\n[{r['time']}] {r['target']} ({r['type']})\n{r['output']}\n"

        if include_vulns:
            report += """
VULNERABILITY FINDINGS
----------------------
ID              Severity   Score   Host              Description
CVE-2024-3094   CRITICAL   9.8     192.168.1.10      XZ Utils backdoor
CVE-2023-44487  HIGH       7.5     192.168.1.22      HTTP/2 Rapid Reset
CVE-2023-23397  HIGH       9.8     192.168.1.5       Outlook NTLM leak
CVE-2022-0778   MEDIUM     5.3     192.168.1.1       OpenSSL infinite loop
"""

        if include_recs:
            report += """
RECOMMENDATIONS
---------------
1. [CRITICAL] Patch XZ Utils immediately on 192.168.1.10
2. [HIGH]     Update web server to patch HTTP/2 Rapid Reset on 192.168.1.22
3. [HIGH]     Apply Microsoft security patch for CVE-2023-23397 on 192.168.1.5
4. [MEDIUM]   Upgrade OpenSSL to latest stable on all hosts
5. [GENERAL]  Disable Telnet (port 23) — replace with SSH
6. [GENERAL]  Implement SSH key auth and disable password auth
7. [GENERAL]  Enable automatic security updates on all managed hosts

DISCLAIMER
----------
This report was generated by SecureOps Lab. All assessments were conducted
on authorized systems only. Findings should be remediated in order of severity.
"""
        st.code(report, language="text")
        st.download_button("⬇ Download Report (.txt)", report, file_name=f"secureops_report_{date}.txt", mime="text/plain")


# ══════════════════════════════════════════════════════════════
# PAGE: AI ASSISTANT
# ══════════════════════════════════════════════════════════════
elif "AI" in page:
    st.markdown("<h2 style='color:var(--accent);letter-spacing:2px'>🤖 AI SECURITY ASSISTANT</h2>", unsafe_allow_html=True)
    st.markdown("<div class='sec-card'>Ask the AI for defensive security advice, CVE explanations, remediation steps, and threat intelligence. Powered by Claude via Anthropic API.</div>", unsafe_allow_html=True)

    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")

    for msg in st.session_state.chat_history:
        role_color = "var(--accent)" if msg["role"] == "assistant" else "var(--text)"
        role_label = "🤖 Assistant" if msg["role"] == "assistant" else "👤 You"
        st.markdown(f"""
        <div class='sec-card' style='margin-bottom:8px'>
          <div class='mono-sm' style='margin-bottom:6px'>{role_label}</div>
          <div style='font-size:0.9rem;line-height:1.6'>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

    user_input = st.text_area("Ask a security question…", height=80,
        placeholder="e.g. What does CVE-2024-3094 mean and how do I patch it?")

    if st.button("Send") and user_input and api_key:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking…"):
            try:
                resp = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1024,
                        "system": "You are a defensive security expert assistant inside SecureOps Lab. Help users understand vulnerabilities, remediation steps, log analysis, and security best practices. Never assist with offensive or unauthorized activity.",
                        "messages": st.session_state.chat_history
                    },
                    timeout=30
                )
                answer = resp.json()["content"][0]["text"]
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"API error: {e}")
    elif st.button("Send") and not api_key:
        st.warning("Enter your Anthropic API key above.")
