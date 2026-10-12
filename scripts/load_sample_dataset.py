"""Load and test multi-modal synthetic datasets into a MAHA investigation case.
Ingests:
1. Court case proceedings & judicial orders (JSON)
2. Financial wire transactions with layering loops (IBM HI-Small CSV)
3. Police crime records, FIRs & Look-Out Circulars (CSV)
4. Telecom Call Detail Records / CDR (CSV)
5. Trains ML models and displays ranked suspects.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from maha.store import Store
from maha.ingestion import ibm_records, narrative_records, cdr_records, history_records
from maha.graph import snapshot
from maha.analytics import analyze
from maha.suspects import compute_suspect_dossiers


def find_file(directory: Path, prefixes: list):
    for prefix in prefixes:
        candidate = directory / prefix
        if candidate.exists():
            return candidate
    return None


def load_dataset(case_id="CASE-2026-TEST", root_dir="data/private/runtime", dataset_num="1", custom_dir=None):
    store = Store(Path(root_dir))
    
    if custom_dir:
        samples = Path(custom_dir)
    elif str(dataset_num) == "2":
        samples = Path("data/sample_datasets_2")
    else:
        samples = Path("data/sample_datasets")

    print(f"\n========================================================")
    print(f"[*] INGESTING SYNTHETIC DATASET {dataset_num} INTO CASE: {case_id}")
    print(f"[*] Source directory: {samples}")
    print(f"========================================================")

    # Ensure case exists in store and user has access
    access_file = Path(root_dir) / 'access.json'
    token = None
    if access_file.exists():
        tokens = json.loads(access_file.read_text())
        token = tokens.get('investigator')
        store.add_case_to_user('investigator', case_id)
    else:
        token = store.create_user('investigator', [case_id])

    # 1. Court Case Proceedings (JSON)
    court_path = find_file(samples, ['court_proceedings_sample_2.json', 'court_proceedings_sample.json', 'court_proceedings.json'])
    if court_path:
        docs = json.loads(court_path.read_text(encoding='utf-8'))
        # Adjust case_id in docs to target case_id
        for d in docs:
            d['case_id'] = case_id
        content = json.dumps(docs, indent=2).encode('utf-8')
        res = store.import_records(court_path.name, content, 'team-authored', True, case_id, narrative_records(content), 'investigator')
        print(f"[+] 1. Court Case Proceedings Ingested: {res.get('accepted_new')} new records ({len(docs)} judicial docs)")
    else:
        print(f"[!] Warning: No court proceedings JSON found in {samples}")

    # 2. Financial Wire Transactions (CSV)
    fin_path = find_file(samples, ['financial_wires_sample_2.csv', 'financial_wires_sample.csv', 'financial_wires.csv'])
    if fin_path:
        content = fin_path.read_bytes()
        res = store.import_records(fin_path.name, content, 'ibm-hi-small', True, case_id, ibm_records(content), 'investigator')
        print(f"[+] 2. Financial Wires Ingested: {res.get('accepted_new')} new records with multi-hop layering cycles")
    else:
        print(f"[!] Warning: No financial wires CSV found in {samples}")

    # 3. Police Crime Records & FIRs (CSV)
    crime_path = find_file(samples, ['crime_records_sample_2.csv', 'crime_records_sample.csv', 'crime_records.csv'])
    if crime_path:
        # Update case_id in rows
        rows = list(csv.reader(io.StringIO(crime_path.read_text(encoding='utf-8'))))
        header = rows[0]
        updated_rows = [header]
        for r in rows[1:]:
            if r:
                r[2] = case_id
                updated_rows.append(r)
        buf = io.StringIO()
        csv.writer(buf).writerows(updated_rows)
        content = buf.getvalue().encode('utf-8')
        res = store.import_records(crime_path.name, content, 'team-authored', True, case_id, history_records(content, case_id), 'investigator')
        print(f"[+] 3. Police Crime Records Ingested: {res.get('accepted_new')} new records (FIRs, Warrants, LOCs)")
    else:
        print(f"[!] Warning: No crime records CSV found in {samples}")

    # 4. Telecom Call Detail Records / CDR (CSV)
    cdr_path = find_file(samples, ['telecom_cdr_sample_2.csv', 'telecom_cdr_sample.csv', 'telecom_cdr.csv'])
    if cdr_path:
        content = cdr_path.read_bytes()
        res = store.import_records(cdr_path.name, content, 'team-authored', True, case_id, cdr_records(content), 'investigator')
        print(f"[+] 4. Telecom CDR Records Ingested: {res.get('accepted_new')} new records (Phone Intercepts)")
    else:
        print(f"[!] Warning: No telecom CDR CSV found in {samples}")

    # 5. Run ML Model Training & Suspect Dossier Ranking
    print(f"\n[*] RUNNING ML TRAINING PIPELINE (Isolation Forest + Graph Cycles + NLP + Centrality)...")
    g = snapshot(store, [case_id])
    analysis = analyze(g)
    suspects = compute_suspect_dossiers(g, analysis.get('leads', []), analysis.get('metrics', {}))

    train_meta = {
        'case_id': case_id,
        'nodes_count': len(g['nodes']),
        'edges_count': len(g['edges']),
        'leads_count': len(analysis.get('leads', [])),
        'suspects_count': len(suspects),
        'status': 'TRAINED'
    }
    store.record_training_run(case_id, train_meta)

    print(f"\n========================================================")
    print(f"[OK] ML TRAINING COMPLETE: {len(suspects)} RANKED SUSPECTS EXTRACTED")
    print(f"========================================================")
    for s in suspects:
        print(f"\n>>> {s['title']}: {s['name']} (ID: {s['authoritative_id']})")
        print(f"    Risk Score: {s['risk_score']} / 100 [{s['risk_level']}] | Role: {s['role']}")
        print(f"    Syndicate Tier: {s['syndicate_tier']}")
        print(f"    M.O.: {s['modus_operandi']}")
        print(f"    Fund Trail Hops: {len(s.get('fund_trail', []))} hops")
        print(f"    Why Flagged:")
        for wf in s['why_flagged'][:3]:
            print(f"      - {wf}")
        if s.get('fund_trail'):
            print(f"    Money Flow Hop #1: {s['fund_trail'][0]['from_account']} -> {s['fund_trail'][0]['to_account']} ({s['fund_trail'][0]['amount']})")

    print(f"\n[i] Access Token: {token}")
    print(f"[i] Open in Web Workspace: http://localhost:5173 (Select Case: {case_id})\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load and test multi-modal synthetic datasets into MAHA")
    parser.add_argument('--case', default='CASE-RIGOROUS-02', help="Case Identifier to create/populate")
    parser.add_argument('--dataset', default='2', choices=['1', '2'], help="Dataset version (1 or 2)")
    parser.add_argument('--dir', default=None, help="Custom samples directory path")
    parser.add_argument('--store', default='data/private/runtime', help="Store directory")
    args = parser.parse_args()
    load_dataset(case_id=args.case, root_dir=args.store, dataset_num=args.dataset, custom_dir=args.dir)

