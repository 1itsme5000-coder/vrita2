import pytest
from maha.store import Store
from maha.graph import snapshot
from maha.analytics import analyze
from maha.court_data import seed_court_and_crime_data
from maha.suspects import compute_suspect_dossiers


def test_suspect_intelligence_ranking_and_evidence(tmp_path, monkeypatch):
    monkeypatch.delenv('NEO4J_URI', raising=False)
    store = Store(tmp_path / 'private')

    # Seed court and crime data
    results = seed_court_and_crime_data(store)
    assert len(results) >= 5

    # Snapshot authorized case scope
    g = snapshot(store, ['DEMO-C01', 'DEMO-C02', 'DEMO-C03'])
    analysis = analyze(g)

    suspects = analysis.get('suspects', [])
    assert len(suspects) >= 3

    # Verify ranking structure
    s1 = suspects[0]
    assert s1['rank'] == 1
    assert s1['title'] == 'Suspect #1'
    assert s1['risk_score'] > 50.0
    assert s1['risk_level'] in ['HIGH', 'CRITICAL', 'MEDIUM']
    assert len(s1['why_flagged']) >= 2
    assert len(s1['recommended_actions']) >= 1
    assert len(s1['evidence_ids']) > 0

    # Ensure evidence IDs resolve strictly to stored evidence
    for eid in s1['evidence_ids'][:5]:
        ev = store.evidence(eid, ['DEMO-C01', 'DEMO-C02', 'DEMO-C03'])
        assert 'passage' in ev
        assert ev['case_ids']

    # Verify Suspect #2 and #3
    s2 = suspects[1]
    assert s2['rank'] == 2
    assert s2['title'] == 'Suspect #2'

    s3 = suspects[2]
    assert s3['rank'] == 3
    assert s3['title'] == 'Suspect #3'


def test_case_training_and_intake_workflow(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from maha.api import create_app
    monkeypatch.delenv('NEO4J_URI', raising=False)
    store = Store(tmp_path / 'private')
    token = store.create_user('investigator', ['TEST-C01'])
    app = create_app(store)
    client = TestClient(app)
    headers = {'Authorization': f'Bearer {token}'}

    # 1. Untrained case returns empty suspects and is_trained = False
    res = client.get('/api/analysis?case=TEST-C01', headers=headers).json()
    assert res['is_trained'] is False
    assert res['suspects'] == []

    # 2. Cannot train empty case
    train_fail = client.post('/api/cases/TEST-C01/train', headers=headers)
    assert train_fail.status_code == 400

    # 3. Seed case evidence
    seed_res = client.post('/api/cases/TEST-C01/load-sample', headers=headers)
    assert seed_res.status_code == 200

    # 4. Before training, suspects are still not shown
    res2 = client.get('/api/analysis?case=TEST-C01', headers=headers).json()
    assert res2['is_trained'] is False
    assert res2['suspects'] == []

    # 5. Run ML Model training & Suspect Extraction
    train_res = client.post('/api/cases/TEST-C01/train', headers=headers)
    assert train_res.status_code == 200
    trained_data = train_res.json()
    assert trained_data['status'] == 'success'
    assert len(trained_data['suspects']) >= 3
    assert trained_data['training_metadata']['status'] == 'TRAINED'

    # 6. Now /api/analysis and /api/suspects return the ranked suspects
    res3 = client.get('/api/analysis?case=TEST-C01', headers=headers).json()
    assert res3['is_trained'] is True
    assert len(res3['suspects']) >= 3
    assert res3['suspects'][0]['title'] == 'Suspect #1'

    # 7. Reset case clears data and training state
    reset_res = client.post('/api/cases/TEST-C01/reset', headers=headers)
    assert reset_res.status_code == 200
    res4 = client.get('/api/analysis?case=TEST-C01', headers=headers).json()
    assert res4['is_trained'] is False
    assert res4['suspects'] == []
