import streamlit as st
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ZeroTrust Shield",
    page_icon="🛡️",
    layout="wide",
)

# ── Custom CSS – dark cybersecurity theme ─────────────────────────────────────
st.markdown("""
<style>
    /* Background & base text */
    .stApp { background-color: #0d1117; color: #c9d1d9; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #161b22; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 16px 20px;
    }
    div[data-testid="metric-container"] label {
        color: #8b949e !important;
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #58a6ff !important;
        font-size: 2rem !important;
        font-weight: 700;
    }

    /* Feature cards */
    .feature-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #58a6ff;
        border-radius: 10px;
        padding: 18px 20px;
        height: 100%;
    }
    .feature-card h4 { color: #58a6ff; margin: 0 0 8px 0; font-size: 1rem; }
    .feature-card p  { color: #8b949e; font-size: 0.88rem; margin: 0; line-height: 1.6; }
    .feature-icon { font-size: 1.6rem; margin-bottom: 8px; }

    /* Section headers */
    .section-header {
        color: #f0f6fc;
        font-size: 1.15rem;
        font-weight: 600;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }

    /* Status badges */
    .badge-success  { background:#1a3a2a; color:#3fb950; padding:3px 10px;
                      border-radius:20px; font-size:0.78rem; font-weight:600; }
    .badge-blocked  { background:#3a1a1a; color:#f85149; padding:3px 10px;
                      border-radius:20px; font-size:0.78rem; font-weight:600; }
    .badge-pending  { background:#3a2e1a; color:#d29922; padding:3px 10px;
                      border-radius:20px; font-size:0.78rem; font-weight:600; }

    /* Dataframe overrides */
    div[data-testid="stDataFrame"] { border: 1px solid #30363d; border-radius: 8px; }

    /* Divider */
    hr { border-color: #30363d; }

    /* Hero description */
    .hero-desc { color: #8b949e; font-size: 0.95rem; line-height: 1.7; margin-top: 4px; }

    /* Alert box */
    .alert-box {
        background-color: #1c2128;
        border: 1px solid #f85149;
        border-radius: 8px;
        padding: 12px 16px;
        color: #f85149;
        font-size: 0.88rem;
    }

    /* ── Rule-based suspicious IP panel ── */
    .susp-panel {
        background-color: #1c1206;
        border: 1px solid #d29922;
        border-left: 5px solid #d29922;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 14px;
    }
    .susp-panel .susp-title {
        color: #d29922;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .susp-panel .susp-body {
        color: #c9d1d9;
        font-size: 0.88rem;
        line-height: 1.7;
    }
    .susp-panel .susp-body strong { color: #f0f6fc; }
    .susp-panel .susp-body code {
        background: #21262d;
        color: #d29922;
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.84rem;
    }
    .susp-rule-note {
        background-color: #161b22;
        border: 1px dashed #30363d;
        border-radius: 8px;
        padding: 12px 16px;
        color: #8b949e;
        font-size: 0.82rem;
        margin-bottom: 16px;
        line-height: 1.6;
    }
    .susp-rule-note strong { color: #c9d1d9; }
    .sample-tag {
        display: inline-block;
        background: #21262d;
        color: #8b949e;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #30363d;
        margin-left: 8px;
        vertical-align: middle;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── Security Alerts – risk-level cards ── */
    .alert-card {
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    /* High risk — red */
    .alert-card.high {
        background-color: #1e0a0a;
        border: 1px solid #f85149;
        border-left: 5px solid #f85149;
    }
    .alert-card.high .alert-risk  { color: #f85149; font-weight: 700; font-size: 0.85rem; }
    .alert-card.high .alert-title { color: #ff7b72; font-size: 1rem; font-weight: 700; margin: 4px 0 8px 0; }
    /* Medium risk — orange */
    .alert-card.medium {
        background-color: #1c1206;
        border: 1px solid #d29922;
        border-left: 5px solid #d29922;
    }
    .alert-card.medium .alert-risk  { color: #d29922; font-weight: 700; font-size: 0.85rem; }
    .alert-card.medium .alert-title { color: #e3b341; font-size: 1rem; font-weight: 700; margin: 4px 0 8px 0; }
    /* Low risk — green */
    .alert-card.low {
        background-color: #071a10;
        border: 1px solid #3fb950;
        border-left: 5px solid #3fb950;
    }
    .alert-card.low .alert-risk  { color: #3fb950; font-weight: 700; font-size: 0.85rem; }
    .alert-card.low .alert-title { color: #56d364; font-size: 1rem; font-weight: 700; margin: 4px 0 8px 0; }
    /* Shared card body */
    .alert-card .alert-body {
        color: #c9d1d9;
        font-size: 0.87rem;
        line-height: 1.75;
    }
    .alert-card .alert-body strong { color: #f0f6fc; }
    .alert-card .alert-body code {
        background: #21262d;
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.82rem;
    }
    .alert-card.high   .alert-body code { color: #f85149; }
    .alert-card.medium .alert-body code { color: #d29922; }
    .alert-card.low    .alert-body code { color: #3fb950; }
    /* Suggestion list inside a card */
    .alert-card ul.suggestions {
        margin: 6px 0 0 0;
        padding-left: 18px;
        color: #8b949e;
        font-size: 0.84rem;
        line-height: 1.8;
    }
    .alert-card ul.suggestions li strong { color: #c9d1d9; }
    /* Disclaimer box */
    .disclaimer-box {
        background-color: #161b22;
        border: 1px dashed #30363d;
        border-radius: 8px;
        padding: 14px 18px;
        color: #8b949e;
        font-size: 0.82rem;
        line-height: 1.7;
        margin-top: 18px;
    }
    .disclaimer-box strong { color: #c9d1d9; }

    /* ── Chart explanation box ── */
    .chart-explain {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-top: 3px solid #58a6ff;
        border-radius: 8px;
        padding: 12px 16px;
        color: #8b949e;
        font-size: 0.82rem;
        line-height: 1.65;
        margin-top: 10px;
    }
    .chart-explain strong { color: #c9d1d9; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🛡️ ZeroTrust Shield")
st.markdown(
    '<p class="hero-desc">'
    "A Zero-Trust Network Access (ZTNA) platform that secures internal admin consoles "
    "using <strong style='color:#58a6ff'>Cloudflare Tunnels</strong> and "
    "<strong style='color:#58a6ff'>Multi-Factor Authentication (MFA)</strong>. "
    "Every access request is verified, logged, and acted upon — trust no one by default."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown('<hr style="margin:18px 0">', unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📊 Live Access Dashboard</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("🔢 Total Access Requests",      "1,284",  "+38 today")
col2.metric("✅ Successful Authentications", "1,103",  "+29 today")
col3.metric("🚫 Blocked Access Attempts",    "142",    "+7 today")
col4.metric("⚠️ Suspicious Activities",      "39",     "+2 today")

st.markdown("<br>", unsafe_allow_html=True)

# ── Alert banner ──────────────────────────────────────────────────────────────
st.markdown(
    '<div class="alert-box">⚠️  <strong>Active Alert:</strong>  '
    '2 new suspicious login attempts detected from unrecognised IP addresses in the last hour. '
    'Review the logs below.</div>',
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

# ── Feature highlights ────────────────────────────────────────────────────────
st.markdown('<p class="section-header">🔐 Security Features</p>', unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">☁️</div>
        <h4>Cloudflare Tunnel</h4>
        <p>Exposes internal services through encrypted Cloudflare Tunnels without opening
        firewall ports, eliminating direct attack surfaces.</p>
    </div>""", unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔑</div>
        <h4>Multi-Factor Authentication</h4>
        <p>Every login requires a second factor (TOTP / hardware key), so stolen credentials
        alone are never enough to gain access.</p>
    </div>""", unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h4>Zero-Trust Access Policies</h4>
        <p>Least-privilege rules evaluate identity, device posture, and context on every
        request — there is no implicit trust for anyone on the network.</p>
    </div>""", unsafe_allow_html=True)

with f4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👁️</div>
        <h4>Access Monitoring</h4>
        <p>Real-time logging of every access event with instant alerts on anomalies,
        unusual locations, or repeated failed attempts.</p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Security logs table ───────────────────────────────────────────────────────
st.markdown('<p class="section-header">📋 Security Logs</p>', unsafe_allow_html=True)

# ── Sample security log data ─────────────────────────────────────────────────
# NOTE: This is sample/demo data used to illustrate the rule-based detection.
# 185.220.101.9 deliberately has 6 failed/blocked attempts so the rule fires.
logs = pd.DataFrame({
    "Timestamp":          [
        "2025-07-15 09:12:04", "2025-07-15 09:18:47", "2025-07-15 09:23:11",
        "2025-07-15 09:31:55", "2025-07-15 09:45:30", "2025-07-15 09:52:08",
        "2025-07-15 10:03:19", "2025-07-15 10:11:42", "2025-07-15 10:20:57",
        "2025-07-15 10:35:14", "2025-07-15 10:41:03", "2025-07-15 10:48:27",
        "2025-07-15 10:55:50", "2025-07-15 11:02:19",
    ],
    "Username":           [
        "alice@corp.com",   "bob@corp.com",     "eve@unknown.net",
        "charlie@corp.com", "diana@corp.com",   "eve@unknown.net",
        "frank@corp.com",   "grace@corp.com",   "heidi@corp.com",
        "ivan@unknown.net", "eve@unknown.net",  "eve@unknown.net",
        "eve@unknown.net",  "eve@unknown.net",
    ],
    "Requested Resource": [
        "Admin Console",  "DB Dashboard",    "Admin Console",
        "CI/CD Pipeline", "Billing Portal",  "DB Dashboard",
        "Admin Console",  "Log Viewer",      "CI/CD Pipeline",
        "Billing Portal", "Admin Console",   "Admin Console",
        "Admin Console",  "Admin Console",
    ],
    "IP Address":         [
        "10.0.1.22",     "10.0.1.45",     "185.220.101.9",
        "10.0.2.11",     "10.0.1.78",     "185.220.101.9",
        "10.0.3.55",     "10.0.1.99",     "10.0.2.34",
        "91.108.4.15",   "185.220.101.9", "185.220.101.9",
        "185.220.101.9", "185.220.101.9",
    ],
    "Auth Status":        [
        "✅ Allowed",    "✅ Allowed",    "🚫 Blocked",
        "✅ Allowed",    "✅ Allowed",    "🚫 Blocked",
        "✅ Allowed",    "✅ Allowed",    "⚠️ Pending MFA",
        "🚫 Blocked",   "🚫 Blocked",   "🚫 Blocked",
        "🚫 Blocked",   "🚫 Blocked",
    ],
    "Action Taken":       [
        "Access Granted",  "Access Granted",  "IP Blacklisted",
        "Access Granted",  "Access Granted",  "Alert Triggered",
        "Access Granted",  "Access Granted",  "MFA Challenge Sent",
        "Account Locked",  "IP Blacklisted",  "Alert Triggered",
        "Alert Triggered", "Account Locked",
    ],
})

# ── Login Records filter dropdown ────────────────────────────────────────────
# The user can pick "All", "Successful", or "Failed" to narrow the table.
log_filter = st.selectbox(
    "🔽 Filter login records by result:",
    options=["All Records", "Successful Only", "Failed / Blocked Only"],
    key="log_filter",
)

# Apply the filter using simple if/else — no machine learning needed
if log_filter == "Successful Only":
    # Keep only rows where Auth Status contains "Allowed"
    filtered_logs = logs[logs["Auth Status"].str.contains("Allowed")]
elif log_filter == "Failed / Blocked Only":
    # Keep only rows where Auth Status contains "Blocked"
    filtered_logs = logs[logs["Auth Status"].str.contains("Blocked")]
else:
    # No filter — show every row
    filtered_logs = logs

st.dataframe(filtered_logs.reset_index(drop=True), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ── Visual Analytics: Authentication Charts ───────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="section-header">📈 Visual Analytics</p>', unsafe_allow_html=True)

# ── Chart data preparation ────────────────────────────────────────────────────
# Count how many rows have each auth outcome from the FULL (unfiltered) logs.
# We classify "Allowed" as Successful, "Blocked" as Failed, anything else as Other.

total_successful = 0   # counter for allowed logins
total_failed     = 0   # counter for blocked logins
total_other      = 0   # counter for pending MFA etc.

for status in logs["Auth Status"]:
    if "Allowed" in status:
        total_successful += 1
    elif "Blocked" in status:
        total_failed += 1
    else:
        total_other += 1   # e.g. "Pending MFA"

# Build a small DataFrame for Chart 1 — two bars: Successful vs Failed
auth_summary_df = pd.DataFrame({
    "Outcome":  ["Successful", "Failed / Blocked", "Pending / Other"],
    "Count":    [total_successful, total_failed, total_other],
})

# Build a DataFrame for Chart 2 — one bar per IP, showing its failure count
failed_only = logs[logs["Auth Status"].str.contains("Blocked")]
failures_per_ip_df = (
    failed_only
    .groupby("IP Address")
    .size()
    .reset_index(name="Failed Attempts")
    .sort_values("Failed Attempts", ascending=False)
)

# ── Side-by-side charts ───────────────────────────────────────────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Chart 1 — Authentication Outcomes**")
    # st.bar_chart needs the value column; set the index to the label column
    st.bar_chart(
        auth_summary_df.set_index("Outcome"),
        y="Count",
        color="#58a6ff",        # blue bars matching the dashboard accent
        use_container_width=True,
    )
    # Short explanation below the chart
    st.markdown(
        '<div class="chart-explain">'
        "<strong>What this chart shows:</strong> "
        "It compares the number of <em>successful</em> logins against "
        "<em>failed/blocked</em> ones recorded in the security log. "
        "In a Zero-Trust environment protected by Cloudflare Tunnels and MFA, "
        "a high failed-to-successful ratio is a strong early warning sign — "
        "it may indicate a brute-force or credential-stuffing attack. "
        "A healthy system should show the vast majority of attempts as successful."
        "</div>",
        unsafe_allow_html=True,
    )

with chart_col2:
    st.markdown("**Chart 2 — Failed Attempts per IP Address**")
    st.bar_chart(
        failures_per_ip_df.set_index("IP Address"),
        y="Failed Attempts",
        color="#f85149",        # red bars to signal danger
        use_container_width=True,
    )
    # Short explanation below the chart
    st.markdown(
        '<div class="chart-explain">'
        "<strong>What this chart shows:</strong> "
        "Each bar represents one IP address and its total number of blocked login "
        "attempts. A single IP with many failures stands out visually and is a "
        "classic indicator of a targeted attack. "
        "In a Zero-Trust system, Cloudflare Tunnels expose no direct ports, so "
        "repeated failures reaching the authentication layer suggest the attacker "
        "is probing the Cloudflare Access endpoint. "
        "Any IP with 5 or more failures is flagged as suspicious by the rule below."
        "</div>",
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# ── Rule-Based Suspicious IP Detection ────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<p class="section-header">'
    '🔎 Rule-Based Suspicious IP Detection'
    '<span class="sample-tag">Sample Data</span>'
    '</p>',
    unsafe_allow_html=True,
)

# ── Always show: how the rule works ──────────────────────────────────────────
st.markdown(
    '<div class="susp-rule-note">'
    "<strong>🧠 Detection Rule (no machine learning used):</strong><br>"
    "The system scans every row in the security logs and counts how many times each "
    "IP address appears with a <em>failed</em> authentication status "
    "(<code>🚫 Blocked</code>). "
    "If the same IP address has <strong>5 or more failed attempts</strong>, "
    "it is automatically flagged as suspicious. "
    "This logic is implemented with plain Python <code>if/else</code> statements — "
    "no machine learning or external libraries required. "
    "In a real Zero-Trust system using Cloudflare Tunnels and MFA, this rule would "
    "trigger an automated policy response such as IP blacklisting or account lockout."
    "</div>",
    unsafe_allow_html=True,
)

# ── Step 1: Define which auth status counts as a failure ─────────────────────
FAILED_KEYWORD = "Blocked"   # any row whose Auth Status contains this word is a failure

# ── Step 2: Filter only the failed rows from the log ─────────────────────────
failed_logs = logs[logs["Auth Status"].str.contains(FAILED_KEYWORD)]

# ── Step 3: Count failures per IP address ────────────────────────────────────
# .groupby() groups rows by IP; .size() counts how many rows are in each group.
failed_counts = failed_logs.groupby("IP Address").size()  # result: IP -> int

# ── Step 4: Set the suspicion threshold ──────────────────────────────────────
THRESHOLD = 5   # an IP with 5 or more failures is flagged as suspicious

# ── Step 5: Check each IP with if/else and collect suspicious ones ────────────
suspicious_ips = []   # list to store flagged IPs and their failure counts

for ip_address, attempt_count in failed_counts.items():
    # Rule: if an IP has 5 or more blocked attempts, flag it
    if attempt_count >= THRESHOLD:
        suspicious_ips.append({"ip": ip_address, "count": attempt_count})
    # else: below threshold — not flagged, nothing to do

# ── Step 6: Display results ───────────────────────────────────────────────────
if suspicious_ips:
    # One or more IPs crossed the threshold — render a warning for each
    for entry in suspicious_ips:
        flagged_ip   = entry["ip"]
        failed_count = entry["count"]

        # Pull every log row (blocked and others) tied to this IP
        related_rows = logs[logs["IP Address"] == flagged_ip][
            ["Timestamp", "Username", "Requested Resource",
             "IP Address", "Auth Status", "Action Taken"]
        ].reset_index(drop=True)

        # Summarise distinct usernames and resources for the warning panel
        usernames_seen      = ", ".join(related_rows["Username"].unique())
        resources_targeted  = ", ".join(related_rows["Requested Resource"].unique())

        # ── Warning panel ────────────────────────────────────────────────────
        st.markdown(
            f'<div class="susp-panel">'
            f'<div class="susp-title">🚨 Suspicious IP Flagged: {flagged_ip}</div>'
            f'<div class="susp-body">'
            f"<strong>Why it was flagged:</strong> This IP address recorded "
            f"<strong>{failed_count} failed (Blocked) authentication "
            f"attempts</strong>, which meets or exceeds the threshold of "
            f"<strong>{THRESHOLD} failures</strong>. "
            f"In a Zero-Trust Network Access environment secured by Cloudflare "
            f"Tunnels and MFA, repeated failures from the same IP strongly indicate "
            f"a brute-force or credential-stuffing attack targeting internal admin "
            f"consoles.<br><br>"
            f"<strong>Associated Username(s):</strong> "
            f"<code>{usernames_seen}</code><br>"
            f"<strong>Targeted Resource(s):</strong> "
            f"<code>{resources_targeted}</code><br>"
            f"<strong>Failed Attempts from this IP:</strong> "
            f"<code>{failed_count}</code><br>"
            f"<strong>Detection Rule Applied:</strong> "
            f"<code>failed_attempts &gt;= {THRESHOLD} → Flag as Suspicious</code><br>"
            f"<strong>Recommended Action:</strong> Block IP at Cloudflare WAF, "
            f"lock associated accounts, and escalate to the security team."
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── Related log records table ─────────────────────────────────────────
        st.markdown(
            "**📄 Related Log Records** "
            "*(sample data — all rows in the security log linked to this IP)*"
        )
        st.dataframe(related_rows, use_container_width=True, hide_index=True)

else:
    # No IP reached the threshold — show a clean all-clear message
    st.success(
        f"✅ No suspicious IPs detected. "
        f"No IP address has reached {THRESHOLD} or more failed authentication attempts."
    )

# ═══════════════════════════════════════════════════════════════════════════════
# ── Security Alerts ───────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    '<p class="section-header">'
    '🚨 Security Alerts'
    '<span class="sample-tag">Sample Data</span>'
    '</p>',
    unsafe_allow_html=True,
)

# ── Sample alert data ─────────────────────────────────────────────────────────
# Each entry represents a suspicious login event observed in the system.
# "failed_attempts" is the number of blocked/failed logins from that IP.
# This sample data covers all three risk levels so every card style is shown.
alert_data = [
    {
        "ip":              "185.220.101.9",
        "username":        "eve@unknown.net",
        "failed_attempts": 6,
        "reason":          "Repeated failed logins targeting the Admin Console via Cloudflare Tunnel",
    },
    {
        "ip":              "91.108.4.15",
        "username":        "ivan@unknown.net",
        "failed_attempts": 3,
        "reason":          "Multiple failed MFA challenges from an unrecognised external IP",
    },
    {
        "ip":              "198.51.100.77",
        "username":        "unknown@external.io",
        "failed_attempts": 7,
        "reason":          "High-frequency login attempts against the Billing Portal",
    },
    {
        "ip":              "203.0.113.42",
        "username":        "temp@vendor.org",
        "failed_attempts": 2,
        "reason":          "Login attempt from an IP not on the approved Cloudflare Access list",
    },
    {
        "ip":              "10.0.5.88",
        "username":        "newuser@corp.com",
        "failed_attempts": 1,
        "reason":          "First-time login from an unregistered internal device; MFA pending",
    },
]

# ── Security Alerts filter dropdown ──────────────────────────────────────────
# Assign a risk label to every alert entry first, then filter by the chosen level.

# Step 1: Assign risk labels to all alerts using if/else (same rule as below)
for alert in alert_data:
    if alert["failed_attempts"] >= 5:
        alert["risk_level"] = "High"
    elif alert["failed_attempts"] >= 2:
        alert["risk_level"] = "Medium"
    else:
        alert["risk_level"] = "Low"

# Step 2: Show the dropdown — "All Alerts" means no filter is applied
alert_filter = st.selectbox(
    "🔽 Filter security alerts by risk level:",
    options=["All Alerts", "High Risk Only", "Medium Risk Only", "Low Risk Only"],
    key="alert_filter",
)

# Step 3: Build the filtered list with if/else
if alert_filter == "High Risk Only":
    filtered_alert_data = [a for a in alert_data if a["risk_level"] == "High"]
elif alert_filter == "Medium Risk Only":
    filtered_alert_data = [a for a in alert_data if a["risk_level"] == "Medium"]
elif alert_filter == "Low Risk Only":
    filtered_alert_data = [a for a in alert_data if a["risk_level"] == "Low"]
else:
    filtered_alert_data = alert_data   # show everything

# Show a message if the filter returns no results
if not filtered_alert_data:
    st.info(f"ℹ️ No alerts match the selected filter: **{alert_filter}**.")

# ── Risk-labelling rules (plain if/else — no machine learning) ────────────────
# Rule:
#   High   → 5 or more failed attempts  (serious threat, immediate action needed)
#   Medium → 2 to 4 failed attempts     (suspicious, needs investigation)
#   Low    → exactly 1 failed attempt   (low concern, monitor the account)

for alert in filtered_alert_data:
    ip       = alert["ip"]
    username = alert["username"]
    attempts = alert["failed_attempts"]
    reason   = alert["reason"]

    # ── Step 1: Assign risk level with if/else ─────────────────────────────────
    if attempts >= 5:
        # High risk: 5 or more failures — strong indicator of brute force
        risk_level  = "High"
        css_class   = "high"
        risk_icon   = "🔴"
        # Suggestions specifically for high-risk events
        suggestions = [
            "<strong>Block the IP immediately</strong> at the Cloudflare WAF to stop further attempts.",
            "<strong>Review the full access logs</strong> for this IP across all protected resources.",
            "<strong>Lock the associated account</strong> and notify the user through a verified channel.",
            "<strong>Verify the user's identity</strong> via a secondary out-of-band method (phone/email).",
            "<strong>Audit MFA activity</strong> — check whether TOTP codes or hardware keys were used.",
            "<strong>Escalate to the security team</strong> for a formal incident response investigation.",
        ]

    elif attempts >= 2:
        # Medium risk: 2–4 failures — suspicious but may be a forgotten password
        risk_level  = "Medium"
        css_class   = "medium"
        risk_icon   = "🟠"
        suggestions = [
            "<strong>Review access logs</strong> for this IP over the past 24 hours.",
            "<strong>Verify the user's identity</strong> — confirm they are aware of the failed attempts.",
            "<strong>Check MFA activity</strong> to see if the second factor was challenged and passed.",
            "<strong>Monitor the account closely</strong> for further unusual behaviour.",
        ]

    else:
        # Low risk: 1 failure — could be a simple mistyped password
        risk_level  = "Low"
        css_class   = "low"
        risk_icon   = "🟢"
        suggestions = [
            "<strong>Monitor the account</strong> — a single failure is often a typo.",
            "<strong>Verify MFA was prompted</strong> and completed successfully on the next login.",
            "<strong>No immediate action required</strong>, but keep the event in the audit log.",
        ]

    # ── Step 2: Build the suggestion list HTML ────────────────────────────────
    suggestion_items_html = "\n".join(
        f"<li>{s}</li>" for s in suggestions
    )

    # ── Step 3: Render the alert card ─────────────────────────────────────────
    st.markdown(
        f'<div class="alert-card {css_class}">'
        f'  <div class="alert-risk">{risk_icon} {risk_level.upper()} RISK</div>'
        f'  <div class="alert-title">Suspicious Login Activity — {ip}</div>'
        f'  <div class="alert-body">'
        f'    <strong>IP Address:</strong> <code>{ip}</code>&nbsp;&nbsp;'
        f'    <strong>Username:</strong> <code>{username}</code>&nbsp;&nbsp;'
        f'    <strong>Failed Attempts:</strong> <code>{attempts}</code><br>'
        f'    <strong>Reason for Alert:</strong> {reason}<br><br>'
        f'    <strong>Suggested Actions:</strong>'
        f'    <ul class="suggestions">{suggestion_items_html}</ul>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="disclaimer-box">'
    "<strong>⚠️ Important Disclaimer:</strong> "
    "A suspicious login pattern identified by these rule-based alerts "
    "<strong>does not automatically prove a cyberattack</strong>. "
    "Multiple failed attempts can result from a forgotten password, a misconfigured "
    "application, or a legitimate user working from an unfamiliar device or location. "
    "Every alert should be treated as a starting point for investigation — not a "
    "definitive verdict. Always <strong>review the full access logs</strong>, "
    "<strong>verify the user's identity</strong>, and "
    "<strong>check MFA activity</strong> before taking disruptive action such as "
    "permanently blocking an IP or locking an account. "
    "These alerts are generated from <em>sample data</em> for demonstration purposes."
    "</div>",
    unsafe_allow_html=True,
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#484f58;font-size:0.8rem;">'
    "ZeroTrust Shield — Built with Streamlit &nbsp;|&nbsp; "
    "Zero-Trust Network Access via Cloudflare Tunnels &amp; MFA"
    "</p>",
    unsafe_allow_html=True,
)
