# 🛡️ ZeroTrust Shield

**Zero-Trust Network Access: Implementing Cloudflare Tunnels and Multi-Factor Authentication (MFA) to Secure Internal Admin Consoles**

A simulated cybersecurity analytics dashboard built with **Python**, **Streamlit**, and **Pandas**. ZeroTrust Shield demonstrates how Zero-Trust Network Access (ZTNA) principles — specifically Cloudflare Tunnels and MFA — can be applied to monitor and secure internal admin consoles, using rule-based detection logic and sample data.

> ⚠️ **Disclaimer:** This project is an educational simulation. No real Cloudflare Tunnel infrastructure or live MFA system is deployed. All log and alert data is sample data for demonstration purposes only.

---

## 📋 Table of Contents

- [Features](#features)
- [Dashboard Sections](#dashboard-sections)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [How the Detection Logic Works](#how-the-detection-logic-works)
- [Risk Level Assignment](#risk-level-assignment)
- [Sample Data](#sample-data)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [References](#references)
- [License](#license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Live Metrics Dashboard** | Four KPI cards showing total requests, successful auths, blocked attempts, and suspicious activities |
| 📋 **Security Logs Table** | 14-row sample log with a dropdown filter (All / Successful / Failed) |
| 📈 **Visual Analytics** | Two bar charts — authentication outcomes and failed attempts per IP |
| 🔎 **Rule-Based IP Detection** | Flags any IP with ≥ 5 failed authentication attempts as suspicious |
| 🚨 **Security Alerts** | High / Medium / Low risk cards with tailored security recommendations |
| 🔽 **Dropdown Filters** | Filter login records by result and alerts by risk level — updates data dynamically |
| 🌑 **Dark Cybersecurity Theme** | Custom CSS dark theme (`#0d1117` background, `#58a6ff` accent) |

---

## 🖥️ Dashboard Sections

```
┌─────────────────────────────────────────────────────┐
│  🛡️  ZeroTrust Shield                               │
│  Zero-Trust Network Access simulation dashboard      │
├────────────┬────────────┬────────────┬──────────────┤
│  1,284     │  1,103     │  142       │  39          │
│  Requests  │  Allowed   │  Blocked   │  Suspicious  │
├─────────────────────────────────────────────────────┤
│  ⚠️  Active Alert Banner                            │
├──────────┬────────────┬──────────────┬─────────────┤
│ ☁️ Tunnel│ 🔑 MFA    │ 📋 Policies  │ 👁️ Monitor  │
├─────────────────────────────────────────────────────┤
│  📋 Security Logs  [Filter ▾]                       │
│  14-row sample access log table                     │
├──────────────────────┬──────────────────────────────┤
│  📈 Auth Outcomes    │  📈 Failed / IP (red)        │
│  (blue bar chart)    │  (bar chart)                 │
├─────────────────────────────────────────────────────┤
│  🔎 Rule-Based Suspicious IP Detection              │
│  Warning panel for IPs with ≥ 5 failures            │
├─────────────────────────────────────────────────────┤
│  🚨 Security Alerts  [Risk Level Filter ▾]          │
│  High / Medium / Low risk cards + suggestions       │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Version | Role |
|---|---|---|
| Python | 3.10+ | Core language |
| Streamlit | 1.30+ | Dashboard framework |
| Pandas | 2.0+ | Data manipulation and aggregation |

No machine learning, no database, no external APIs — runs entirely on sample in-memory data.

---

## 📁 Project Structure

```
IBM PROJECT/
│
├── app.py                              # Main dashboard (single file, ~700 lines)
├── README.md                           # This file
└── ZeroTrust_Shield_Project_Report.docx  # Full college project report
```

---

## ⚙️ Installation

**Step 1 — Install Python 3.10+**

Download from [https://www.python.org/downloads/](https://www.python.org/downloads/).  
On Windows, check **"Add Python to PATH"** during installation.

**Step 2 — Install required libraries**

Open a terminal (PowerShell, Command Prompt, or macOS/Linux Terminal) and run:

```bash
pip install streamlit pandas
```

---

## 🚀 Running the App

Navigate to the folder containing `app.py` and run:

```bash
streamlit run app.py
```

Streamlit will print a local URL — open it in your browser:

```
  Local URL:  http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Press `Ctrl + C` in the terminal to stop the server.

---

## 🔎 How the Detection Logic Works

The rule-based suspicious IP detection uses **plain Python `if/else` statements** — no machine learning required.

```python
# Step 1: Define what counts as a failure
FAILED_KEYWORD = "Blocked"

# Step 2: Filter failed rows
failed_logs = logs[logs["Auth Status"].str.contains(FAILED_KEYWORD)]

# Step 3: Count failures per IP
failed_counts = failed_logs.groupby("IP Address").size()

# Step 4: Set the threshold
THRESHOLD = 5

# Step 5: Flag IPs that cross the threshold
suspicious_ips = []

for ip_address, attempt_count in failed_counts.items():
    if attempt_count >= THRESHOLD:
        suspicious_ips.append({"ip": ip_address, "count": attempt_count})
    # else: below threshold — not flagged

# Step 6: Render warning panel or green success message
```

With the sample data provided, **IP `185.220.101.9`** has **6 blocked entries** and is correctly flagged.

---

## 🚨 Risk Level Assignment

Security alerts are classified using `if/else` logic based on the number of failed login attempts:

| Condition | Risk Level | Colour | Action |
|---|---|---|---|
| `failed_attempts >= 5` | 🔴 **High** | Red | Block IP at Cloudflare WAF, lock account, escalate |
| `failed_attempts >= 2` | 🟠 **Medium** | Orange | Review logs, verify identity, check MFA activity |
| `failed_attempts == 1` | 🟢 **Low** | Green | Monitor account, verify MFA completion |

---

## 📊 Sample Data

The dashboard uses **14 sample log rows** and **5 sample alert entries** (all fictional, for demonstration only).

**Sample Security Logs (excerpt):**

| Timestamp | Username | Requested Resource | IP Address | Auth Status |
|---|---|---|---|---|
| 2025-07-15 09:12 | alice@corp.com | Admin Console | 10.0.1.22 | ✅ Allowed |
| 2025-07-15 09:23 | eve@unknown.net | Admin Console | 185.220.101.9 | 🚫 Blocked |
| 2025-07-15 10:20 | heidi@corp.com | CI/CD Pipeline | 10.0.2.34 | ⚠️ Pending MFA |
| 2025-07-15 11:02 | eve@unknown.net | Admin Console | 185.220.101.9 | 🚫 Blocked |

IP `185.220.101.9` appears **6 times** with `Blocked` status — deliberately triggering the detection rule.

**Sample Security Alerts:**

| IP Address | Username | Failed Attempts | Risk Level |
|---|---|---|---|
| 185.220.101.9 | eve@unknown.net | 6 | 🔴 High |
| 91.108.4.15 | ivan@unknown.net | 3 | 🟠 Medium |
| 198.51.100.77 | unknown@external.io | 7 | 🔴 High |
| 203.0.113.42 | temp@vendor.org | 2 | 🟠 Medium |
| 10.0.5.88 | newuser@corp.com | 1 | 🟢 Low |

---

## 📸 Screenshots

> Screenshots can be added here after running the dashboard. Use `streamlit run app.py`, take screenshots of each section, and add them to a `screenshots/` folder.

```
screenshots/
├── 01_metrics_cards.png
├── 02_security_logs.png
├── 03_visual_analytics.png
├── 04_suspicious_ip_detection.png
└── 05_security_alerts.png
```

---

## 🔮 Future Enhancements

1. **Real Cloudflare API Integration** — ingest live access logs via the Cloudflare Zero Trust API
2. **Live MFA via `pyotp`** — generate real TOTP codes for functional MFA simulation
3. **Database Backend** — replace in-memory data with SQLite or PostgreSQL for persistence
4. **ML Anomaly Detection** — add scikit-learn Isolation Forest to detect behavioural anomalies
5. **Email / SMS Alerting** — send real-time notifications when High risk events are detected
6. **Role-Based Access Control** — protect the dashboard itself with login and analyst/admin roles

---

## 📚 References

1. Rose et al. *Zero Trust Architecture.* NIST SP 800-207. NIST, 2020. https://doi.org/10.6028/NIST.SP.800-207
2. Cloudflare Inc. *Cloudflare Tunnel Documentation.* 2024. https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
3. Cloudflare Inc. *Cloudflare Zero Trust Documentation.* 2024. https://developers.cloudflare.com/cloudflare-one/
4. M'Raihi et al. *TOTP: Time-Based One-Time Password Algorithm.* RFC 6238. IETF, 2011. https://www.rfc-editor.org/rfc/rfc6238
5. Kindervag, J. *No More Chewy Centers: Introducing The Zero Trust Model.* Forrester Research, 2010.
6. OWASP Foundation. *Authentication Cheat Sheet.* 2024. https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
7. Streamlit Inc. *Streamlit Documentation.* 2024. https://docs.streamlit.io/
8. The pandas development team. *Pandas Documentation.* 2024. https://pandas.pydata.org/docs/
9. Grassi et al. *Digital Identity Guidelines.* NIST SP 800-63B. NIST, 2017. https://doi.org/10.6028/NIST.SP.800-63b
10. Python Software Foundation. *Python 3 Documentation.* 2024. https://docs.python.org/3/

---

## 📄 License

This project is submitted as an academic project for the **Master of Computer Applications (MCA) – Cyber Security** programme. It is intended for educational purposes only.

---

<p align="center">Built with ❤️ using Python & Streamlit &nbsp;|&nbsp; Zero-Trust Network Access · Cloudflare Tunnels · MFA</p>
