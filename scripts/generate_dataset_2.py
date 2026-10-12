"""Generator script to produce Sample Dataset 2 (Operation Cyber-Phantom).
Rigorous multi-modal dataset:
- 140+ financial wires with closed layering loops, structuring, nocturnal spikes, and legitimate background noise.
- 18 high-profile crime records (FIRs, NBWs, LOCs, CBI Special Offenses, Proclaimed Offender notices).
- 60+ telecom CDR phone intercepts synchronized with laundering transactions.
- Raw police FIR narrative for free-text ingestion testing.
"""
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "data" / "sample_datasets_2"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# 1. GENERATE FINANCIAL WIRES (140+ rows)
# ---------------------------------------------------------
IBM_HEADER = [
    'Timestamp', 'From Bank', 'Account', 'To Bank', 'Account',
    'Amount Received', 'Receiving Currency', 'Amount Paid', 'Payment Currency',
    'Payment Format', 'Is Laundering'
]

wires = []

# --- A. Laundering Cycles & Wires (35 records) ---
# Cycle 1: 3-Hop Loop (Oberoi -> Kulkarni -> Vertex -> Oberoi)
wires.append(["2026/03/18 01:10", "010", "ACC-OBEROI-901", "010", "ACC-KULKARNI-902", "450000.00", "US Dollar", "450000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/18 01:45", "010", "ACC-KULKARNI-902", "010", "ACC-VERTEX-903", "446000.00", "US Dollar", "446000.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/18 02:30", "010", "ACC-VERTEX-903", "010", "ACC-OBEROI-901", "440000.00", "US Dollar", "440000.00", "US Dollar", "Reinvestment", "1"])

# Kickback 1 to Bank Operations Manager Kavita Roy
wires.append(["2026/03/18 03:00", "010", "ACC-OBEROI-901", "010", "ACC-KAVITA-907", "50000.00", "US Dollar", "50000.00", "US Dollar", "Wire", "1"])

# Cycle 2: 4-Hop Loop (Oberoi -> Farhan -> Joshi -> Vertex -> Oberoi)
wires.append(["2026/03/19 01:15", "010", "ACC-OBEROI-901", "010", "ACC-FARHAN-904", "280000.00", "US Dollar", "280000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/19 01:50", "010", "ACC-FARHAN-904", "010", "ACC-JOSHI-906", "276500.00", "US Dollar", "276500.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/19 02:40", "010", "ACC-JOSHI-906", "010", "ACC-VERTEX-903", "272000.00", "US Dollar", "272000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/19 03:15", "010", "ACC-VERTEX-903", "010", "ACC-OBEROI-901", "268000.00", "US Dollar", "268000.00", "US Dollar", "Reinvestment", "1"])

# Kickback 2 to Bank Operations Manager Kavita Roy
wires.append(["2026/03/19 03:45", "010", "ACC-VERTEX-903", "010", "ACC-KAVITA-907", "35000.00", "US Dollar", "35000.00", "US Dollar", "Wire", "1"])

# Cycle 3: 4-Hop Crypto Liquidity Loop (Kulkarni -> Tanya -> Farhan -> Joshi -> Kulkarni)
wires.append(["2026/03/20 01:30", "010", "ACC-KULKARNI-902", "010", "ACC-TANYA-905", "185000.00", "US Dollar", "185000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/20 02:15", "010", "ACC-TANYA-905", "010", "ACC-FARHAN-904", "181500.00", "US Dollar", "181500.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/20 02:50", "010", "ACC-FARHAN-904", "010", "ACC-JOSHI-906", "178000.00", "US Dollar", "178000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/20 03:30", "010", "ACC-JOSHI-906", "010", "ACC-KULKARNI-902", "174000.00", "US Dollar", "174000.00", "US Dollar", "Reinvestment", "1"])

# Kickback 3 to Bank Operations Manager Kavita Roy
wires.append(["2026/03/20 04:00", "010", "ACC-FARHAN-904", "010", "ACC-KAVITA-907", "25000.00", "US Dollar", "25000.00", "US Dollar", "Wire", "1"])

# Structuring / Smurfing Campaign: Rapid Sub-$50,000 Wires (Night of March 21)
wires.append(["2026/03/21 01:05", "010", "ACC-OBEROI-901", "010", "ACC-FARHAN-904", "49500.00", "US Dollar", "49500.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/21 01:25", "010", "ACC-OBEROI-901", "010", "ACC-FARHAN-904", "48900.00", "US Dollar", "48900.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/21 01:45", "010", "ACC-OBEROI-901", "010", "ACC-FARHAN-904", "49200.00", "US Dollar", "49200.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/21 02:10", "010", "ACC-FARHAN-904", "010", "ACC-TANYA-905", "48000.00", "US Dollar", "48000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/21 02:30", "010", "ACC-FARHAN-904", "010", "ACC-TANYA-905", "47500.00", "US Dollar", "47500.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/21 02:55", "010", "ACC-FARHAN-904", "010", "ACC-TANYA-905", "48300.00", "US Dollar", "48300.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/21 03:20", "010", "ACC-TANYA-905", "010", "ACC-VERTEX-903", "95000.00", "US Dollar", "95000.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/21 03:50", "010", "ACC-VERTEX-903", "010", "ACC-OBEROI-901", "93500.00", "US Dollar", "93500.00", "US Dollar", "Reinvestment", "1"])

# Multi-Tier Deep Layering Loop 4 (5-Hop Loop: Oberoi -> Kulkarni -> Tanya -> Joshi -> Vertex -> Oberoi)
wires.append(["2026/03/22 01:00", "010", "ACC-OBEROI-901", "010", "ACC-KULKARNI-902", "320000.00", "US Dollar", "320000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/22 01:40", "010", "ACC-KULKARNI-902", "010", "ACC-TANYA-905", "315000.00", "US Dollar", "315000.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/22 02:20", "010", "ACC-TANYA-905", "010", "ACC-JOSHI-906", "310000.00", "US Dollar", "310000.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/22 03:00", "010", "ACC-JOSHI-906", "010", "ACC-VERTEX-903", "305000.00", "US Dollar", "305000.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/22 03:45", "010", "ACC-VERTEX-903", "010", "ACC-OBEROI-901", "300000.00", "US Dollar", "300000.00", "US Dollar", "Reinvestment", "1"])

# Second Smurfing Wave (Night of March 22)
wires.append(["2026/03/22 04:05", "010", "ACC-OBEROI-901", "010", "ACC-JOSHI-906", "49800.00", "US Dollar", "49800.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/22 04:20", "010", "ACC-OBEROI-901", "010", "ACC-JOSHI-906", "49100.00", "US Dollar", "49100.00", "US Dollar", "Wire", "1"])
wires.append(["2026/03/22 04:35", "010", "ACC-JOSHI-906", "010", "ACC-FARHAN-904", "97500.00", "US Dollar", "97500.00", "US Dollar", "ACH", "1"])
wires.append(["2026/03/22 04:50", "010", "ACC-FARHAN-904", "010", "ACC-OBEROI-901", "96000.00", "US Dollar", "96000.00", "US Dollar", "Reinvestment", "1"])

# Additional Kickback 4 to Kavita Roy
wires.append(["2026/03/22 05:00", "010", "ACC-KULKARNI-902", "010", "ACC-KAVITA-907", "40000.00", "US Dollar", "40000.00", "US Dollar", "Wire", "1"])

# --- B. Routine Commercial Background Noise (110 records) ---
legit_nodes = [
    "ACC-CORP-OFFICE-01", "ACC-PAYROLL-CORP", "ACC-LOGISTICS-HUB", "ACC-OFFICE-SUPPLIES",
    "ACC-UTILITIES-POWER", "ACC-SERVER-HOSTING", "ACC-RETAIL-STORE-1", "ACC-RETAIL-STORE-2",
    "ACC-EMPLOYEE-BENEFITS", "ACC-LEGAL-RETAINER", "ACC-SOFTWARE-LIC", "ACC-EQUIP-MAINT",
    "ACC-SHIPPING-CARGO", "ACC-TAX-ESCROW", "ACC-CATERING-SVC", "ACC-FACILITY-MGMT",
    "ACC-STATIONERY-MART", "ACC-TELECOM-CORP", "ACC-SECURITY-AGENCY", "ACC-TRAVEL-DESK"
]

formats = ["ACH", "Cheque", "Wire", "CreditCard"]
import random
random.seed(42)

for day in range(15, 23):
    date_str = f"2026/03/{day:02d}"
    # Generate 14 legitimate daylight business transactions per day (09:00 - 18:00)
    for i in range(14):
        hour = 9 + (i % 9)
        minute = (i * 17) % 60
        ts = f"{date_str} {hour:02d}:{minute:02d}"
        src = legit_nodes[(i * 3 + day) % len(legit_nodes)]
        dst = legit_nodes[(i * 7 + day + 1) % len(legit_nodes)]
        if src == dst:
            dst = legit_nodes[(i + 2) % len(legit_nodes)]
        # Normal commercial amounts: $250.00 to $18,500.00
        amt_val = round(random.uniform(250.0, 18500.0), 2)
        amt_str = f"{amt_val:.2f}"
        fmt = formats[(i + day) % len(formats)]
        wires.append([ts, "010", src, "010", dst, amt_str, "US Dollar", amt_str, "US Dollar", fmt, "0"])

wires_csv_path = BASE_DIR / "financial_wires_sample_2.csv"
with open(wires_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(IBM_HEADER)
    writer.writerows(wires)

print(f"[OK] Generated {len(wires)} financial wires -> {wires_csv_path}")

# ---------------------------------------------------------
# 2. GENERATE POLICE CRIME RECORDS (18 rows)
# ---------------------------------------------------------
CRIME_HEADER = ['record_id', 'person_id', 'case_id', 'record_date', 'record_status', 'text', 'synthetic']
crime_rows = [
    # P201: Aditya Vardhan Oberoi (Mastermind)
    ["CR-FIR-2021-901", "P201", "DEMO-C01", "2021-09-12", "Active Charge-Sheet",
     "EOW FIR No. 340/2021 registered under IPC Sections 420, 409, 120B. Misappropriation of ₹45 Crores in State Infrastructure Tenders via fabricated vendor bank accounts.", "true"],
    ["CR-LOC-2022-902", "P201", "DEMO-C01", "2022-03-15", "Look Out Circular",
     "Look Out Circular (LOC No. B-9912) opened by Bureau of Immigration at all international airports and seaports to prevent evasion from ongoing financial investigation.", "true"],
    ["CR-ECIR-2023-903", "P201", "DEMO-C01", "2023-01-10", "PMLA Indictment",
     "Directorate of Enforcement ECIR No. DL-08/2023 registered under Section 3 & 4 PMLA for generation and laundering of proceeds of crime totaling ₹85 Crores.", "true"],
    ["CR-NBW-2024-904", "P201", "DEMO-C01", "2024-06-20", "Non-Bailable Warrant",
     "Special Court for PMLA issued Non-Bailable Arrest Warrant following deliberate non-appearance across 8 consecutive statutory summons.", "true"],
    ["CR-PROC-2025-905", "P201", "DEMO-C01", "2025-02-14", "Proclaimed Offender",
     "Proclamation under Section 82 CrPC published in National Dailies declaring Aditya Vardhan Oberoi a Proclaimed Offender.", "true"],

    # P202: Sameer Kulkarni (Hawala Mule Coordinator)
    ["CR-FIR-2022-906", "P202", "DEMO-C01", "2022-08-04", "Active Charge-Sheet",
     "Mumbai Crime Branch EOW FIR 112/2022 under IPC 420/120B and FEMA violations for operating unauthorized foreign exchange and cash mule layering conduits.", "true"],
    ["CR-NBW-2023-907", "P202", "DEMO-C01", "2023-05-19", "Non-Bailable Warrant",
     "Metropolitan Magistrate Court issued Non-Bailable Warrant for absconding during trial in hawala smurfing proceedings.", "true"],
    ["CR-CBI-2024-908", "P202", "DEMO-C01", "2024-11-02", "CBI Special Offense",
     "CBI Banking Fraud Security Cell (BS&FC) RC-04/2024 for diversion of consortium credit lines into structured beneficiary accounts.", "true"],

    # P203: Radhika Singhania (Dummy Shell Director)
    ["CR-ROC-2023-909", "P203", "DEMO-C01", "2023-04-18", "Disqualified Director",
     "Ministry of Corporate Affairs disqualification order under Section 164(2) Companies Act for directorship in bogus shell entities including Vertex Exim Corp.", "true"],
    ["CR-SFIO-2024-910", "P203", "DEMO-C01", "2024-03-30", "SFIO Investigation",
     "Serious Fraud Investigation Office (SFIO) inspection report identifying round-tripping of capital and fictitious loan amortization back to Aditya Oberoi.", "true"],

    # P204: Farhan Akhtar Siddiqui (Angadia Courier Cash Mule)
    ["CR-FIR-2023-911", "P204", "DEMO-C01", "2023-07-22", "Active Charge-Sheet",
     "Gujarat Police Crime Branch FIR 88/2023 under IPC 420/467/468. Seizure of ₹2.4 Crores unaccounted cash transit linked to Angadia courier syndicates.", "true"],
    ["CR-LOC-2024-912", "P204", "DEMO-C01", "2024-05-10", "Look Out Circular",
     "Look Out Circular issued by Ministry of Home Affairs to monitor transit between Ahmedabad, Mumbai, and Delhi.", "true"],

    # P205: Tanya Deshmukh (Darknet Crypto Liquidity Operator)
    ["CR-CYB-2024-913", "P205", "DEMO-C01", "2024-08-14", "Cyber Crime Notice",
     "Notice under Section 91 CrPC by Delhi Police Cyber Cell regarding unhosted cryptocurrency wallets and P2P USDT liquidation conduits.", "true"],
    ["CR-INTER-2025-914", "P205", "DEMO-C01", "2025-01-20", "INTERPOL Red Notice Alert",
     "INTERPOL Purple Notice intelligence sharing on crypto tumbler / mixing protocols used to obscure criminal ransomware and fraud proceeds.", "true"],

    # P206: Deepak Joshi (Syndicate Chartered Accountant)
    ["CR-ICAI-2024-915", "P206", "DEMO-C01", "2024-02-11", "ICAI Disciplinary Bar",
     "Institute of Chartered Accountants of India Disciplinary Directorate prima facie finding of professional misconduct for certifying fabricated balance sheets.", "true"],
    ["CR-FIR-2024-916", "P206", "DEMO-C01", "2024-09-08", "Active Charge-Sheet",
     "Central GST Intelligence (DGGI) FIR under Section 132 CGST Act and IPC 468/471 for generating ₹120 Crores in bogus Input Tax Credit (ITC) e-way bills.", "true"],

    # P207: Kavita Roy (Corrupt Bank Operations Manager)
    ["CR-CBI-2025-917", "P207", "DEMO-C01", "2025-04-12", "CBI Corruption Indictment",
     "CBI Anti-Corruption Branch RC-22/2025 registered under Section 7 & 13(1)(d) Prevention of Corruption Act for accepting pecuniary gratification to suppress AML alerts.", "true"],
    ["CR-VIG-2025-918", "P207", "DEMO-C01", "2025-07-01", "Bank Vigilance Suspension",
     "Central Vigilance Commission (CVC) inquiry order and immediate departmental suspension from Senior Branch Operations Manager post at Bank 010.", "true"]
]

crime_csv_path = BASE_DIR / "crime_records_sample_2.csv"
with open(crime_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(CRIME_HEADER)
    writer.writerows(crime_rows)

print(f"[OK] Generated {len(crime_rows)} crime records -> {crime_csv_path}")

# ---------------------------------------------------------
# 3. GENERATE TELECOM CALL DETAIL RECORDS / CDR (65 calls)
# ---------------------------------------------------------
CDR_HEADER = ['record_id', 'caller_person_id', 'callee_person_id', 'start_time', 'duration_seconds', 'synthetic']
cdr_rows = []

# Synchronized calls tightly coupled to wire transfer times:
# 18 March: Oberoi (P201) coordinates Loop 1 with Kulkarni (P202) and Vertex (P203)
cdr_rows.append(["CDR-2026-201", "P201", "P202", "2026-03-18T00:55:00+00:00", 380, "true"])
cdr_rows.append(["CDR-2026-202", "P202", "P203", "2026-03-18T01:35:00+00:00", 290, "true"])
cdr_rows.append(["CDR-2026-203", "P203", "P201", "2026-03-18T02:20:00+00:00", 410, "true"])
cdr_rows.append(["CDR-2026-204", "P201", "P207", "2026-03-18T02:50:00+00:00", 185, "true"]) # Bank manager alert suppression

# 19 March: Oberoi (P201) coordinates Loop 2 with Farhan (P204), Joshi (P206), and Vertex (P203)
cdr_rows.append(["CDR-2026-205", "P201", "P204", "2026-03-19T01:00:00+00:00", 420, "true"])
cdr_rows.append(["CDR-2026-206", "P204", "P206", "2026-03-19T01:38:00+00:00", 250, "true"])
cdr_rows.append(["CDR-2026-207", "P206", "P203", "2026-03-19T02:25:00+00:00", 310, "true"])
cdr_rows.append(["CDR-2026-208", "P203", "P201", "2026-03-19T03:05:00+00:00", 340, "true"])
cdr_rows.append(["CDR-2026-209", "P203", "P207", "2026-03-19T03:35:00+00:00", 215, "true"]) # Bank manager kickback confirmation

# 20 March: Crypto loop coordination Kulkarni (P202) -> Tanya (P205) -> Farhan (P204) -> Joshi (P206)
cdr_rows.append(["CDR-2026-210", "P202", "P205", "2026-03-20T01:15:00+00:00", 480, "true"])
cdr_rows.append(["CDR-2026-211", "P205", "P204", "2026-03-20T02:00:00+00:00", 330, "true"])
cdr_rows.append(["CDR-2026-212", "P204", "P206", "2026-03-20T02:35:00+00:00", 295, "true"])
cdr_rows.append(["CDR-2026-213", "P206", "P202", "2026-03-20T03:15:00+00:00", 360, "true"])
cdr_rows.append(["CDR-2026-214", "P204", "P207", "2026-03-20T03:50:00+00:00", 170, "true"])

# 21 March: Smurfing campaign coordination (Rapid calls between Oberoi, Farhan, Tanya, Vertex)
cdr_rows.append(["CDR-2026-215", "P201", "P204", "2026-03-21T00:50:00+00:00", 510, "true"])
cdr_rows.append(["CDR-2026-216", "P201", "P204", "2026-03-21T01:15:00+00:00", 180, "true"])
cdr_rows.append(["CDR-2026-217", "P204", "P205", "2026-03-21T01:55:00+00:00", 420, "true"])
cdr_rows.append(["CDR-2026-218", "P205", "P203", "2026-03-21T03:05:00+00:00", 275, "true"])
cdr_rows.append(["CDR-2026-219", "P203", "P201", "2026-03-21T03:40:00+00:00", 390, "true"])

# 22 March: 5-Hop loop coordination calls
cdr_rows.append(["CDR-2026-220", "P201", "P202", "2026-03-22T00:45:00+00:00", 440, "true"])
cdr_rows.append(["CDR-2026-221", "P202", "P205", "2026-03-22T01:25:00+00:00", 380, "true"])
cdr_rows.append(["CDR-2026-222", "P205", "P206", "2026-03-22T02:05:00+00:00", 310, "true"])
cdr_rows.append(["CDR-2026-223", "P206", "P203", "2026-03-22T02:45:00+00:00", 290, "true"])
cdr_rows.append(["CDR-2026-224", "P203", "P201", "2026-03-22T03:30:00+00:00", 415, "true"])
cdr_rows.append(["CDR-2026-225", "P202", "P207", "2026-03-22T04:45:00+00:00", 195, "true"])

# Syndicate Intra-Network Background Chatter (40 additional intercept records across the syndicate)
syndicate_members = ["P201", "P202", "P203", "P204", "P205", "P206", "P207"]
for idx in range(40):
    caller = syndicate_members[idx % len(syndicate_members)]
    callee = syndicate_members[(idx * 3 + 2) % len(syndicate_members)]
    if caller == callee:
        callee = syndicate_members[(idx + 1) % len(syndicate_members)]
    day = 15 + (idx % 8)
    hour = (idx * 5) % 24
    minute = (idx * 13) % 60
    dur = 90 + ((idx * 29) % 500)
    rec_id = f"CDR-2026-{226 + idx}"
    ts = f"2026-03-{day:02d}T{hour:02d}:{minute:02d}:00+00:00"
    cdr_rows.append([rec_id, caller, callee, ts, dur, "true"])

cdr_csv_path = BASE_DIR / "telecom_cdr_sample_2.csv"
with open(cdr_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(CDR_HEADER)
    writer.writerows(cdr_rows)

print(f"[OK] Generated {len(cdr_rows)} telecom CDR intercepts -> {cdr_csv_path}")

# ---------------------------------------------------------
# 4. GENERATE RAW POLICE FIR NARRATIVE (Free-text testing)
# ---------------------------------------------------------
raw_fir_text = """FIRST INFORMATION REPORT (Under Section 154 Cr.P.C.)
POLICE STATION: Special Investigation Bureau & Economic Offenses Wing (EOW), New Delhi
FIR No: 588/2026 | Date: 28-03-2026 | Time: 16:45 HRS
Acts & Sections: Section 420 IPC (Cheating), Section 120B IPC (Criminal Conspiracy), Section 409 IPC (Criminal Breach of Trust), Section 468 & 471 IPC (Forgery), Section 66D Information Technology Act, Section 7 & 13(1)(d) Prevention of Corruption Act, read with Section 3 & 4 of Prevention of Money Laundering Act, 2002 (PMLA).

1. COMPLAINANT PARTICULARS:
Director of Forensic Audits, National Financial Intelligence Authority (NFIA), New Delhi.

2. SUSPECTS & ACCUSED PARTICULARS:
(i) Accused Aditya Vardhan Oberoi [ID:P201], Managing Director of Oberoi Global Conglomerate (Alias: Singhania). Beneficial owner of primary conduit account ACC-OBEROI-901 at Bank 010.
(ii) Accused Sameer Kulkarni [ID:P202], Chief Cash Smurfing & Hawala Controller. Operates mule layering account ACC-KULKARNI-902 at Bank 010.
(iii) Accused Radhika Singhania [ID:P203], Dummy Managing Director of Vertex Exim Corp. Operates corporate transit account ACC-VERTEX-903 at Bank 010.
(iv) Accused Farhan Akhtar Siddiqui [ID:P204], Angadia Cash Courier Coordinator. Operates rapid liquidation account ACC-FARHAN-904 at Bank 010.
(v) Accused Tanya Deshmukh [ID:P205], Unhosted Darknet Crypto Liquidity Operator. Operates digital off-ramp account ACC-TANYA-905 at Bank 010.
(vi) Accused Deepak Joshi [ID:P206], Syndicate Chartered Accountant and Bogus Invoice Architect. Operates pass-through account ACC-JOSHI-906 at Bank 010.
(vii) Accused Kavita Roy [ID:P207], Senior Branch Operations Manager at Bank 010. Operates kickback repository account ACC-KAVITA-907 at Bank 010.
(viii) Witness Arvind Swaminathan [ID:P208], Principal Core Banking Systems Auditor. Deposed under Section 164 CrPC providing cryptographic log trails.

3. DETAILS OF OFFENSE & MODUS OPERANDI:
A rigorous forensic audit of core banking transaction ledgers revealed that between January and March 2026, the aforementioned syndicate hatched a sophisticated multi-hop money laundering conspiracy totaling ₹85,000,000 INR (approximately $1,020,000 USD).
Accused Aditya Vardhan Oberoi [ID:P201] systematically transferred large tranches from account 010 / ACC-OBEROI-901 during nocturnal hours (01:00 AM to 04:30 AM) to circumvent internal compliance monitoring.
The funds were layered across multiple concurrent pathways:
- Primary 3-Hop Closed Loop: From ACC-OBEROI-901 into mule account ACC-KULKARNI-902, layered into shell entity ACC-VERTEX-903, and repatriated back to ACC-OBEROI-901 under the deceptive notation of 'Reinvestment'.
- Secondary 4-Hop Loop: Diverted from ACC-OBEROI-901 into cash courier ACC-FARHAN-904, routed through fake billing account ACC-JOSHI-906, channeled through ACC-VERTEX-903, and reintegrated into ACC-OBEROI-901.
- Darknet Crypto Tumbling: Funds channeled through ACC-TANYA-905 for unhosted P2P cryptocurrency off-ramping.
- Bank Collusion: Accused Kavita Roy [ID:P207] systematically overrode automated AML Anti-Structuring alerts and accepted kickback wires directly into ACC-KAVITA-907.

4. INVESTIGATIVE DIRECTIVES & ACTIONS REQUESTED:
(a) Immediate freezing of all 7 syndicate bank accounts under Section 102 CrPC.
(b) Transmittal of forensic dossiers to Directorate of Enforcement (ED) and Central Bureau of Investigation (CBI).
(c) Execution of Non-Bailable Arrest Warrants (NBW) against P201, P202, and P204, and renewal of Look Out Circulars (LOC) at all international ports.
"""

raw_fir_path = BASE_DIR / "raw_police_fir_sample_2.txt"
with open(raw_fir_path, "w", encoding="utf-8") as f:
    f.write(raw_fir_text)

print(f"[OK] Generated Raw Police FIR Narrative -> {raw_fir_path}")
print("\n[SUCCESS] Dataset 2 Generation Complete!")
