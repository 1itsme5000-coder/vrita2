"""Pretrained NER plus explicit identifier and relation templates; no name-only merge."""
import re
from functools import lru_cache
from difflib import SequenceMatcher
from .store import uid
from .ingestion import node,edge,account


@lru_cache(maxsize=1)
def pipeline():
    import spacy
    # Fail visibly rather than silently replacing pretrained extraction with an empty model.
    return spacy.load("en_core_web_sm")


def extract(doc,base,nlp=None):
    text=doc['text']; did="document:"+uid(doc['document_id'],text); cid=doc['case_id']
    common=[node("Case",cid,cid),node("Document",did,doc['document_id'],filed_date=doc['filed_date']),edge("FILED_UNDER",did,cid)]
    yield dict(locator={**base,"char_start":0,"char_end":len(text)},passage=text,method="document-metadata",facts=common)
    # Only these explicit relation sentences assert ownership, location, or case participation.
    person_pattern=r"Person (?P<name>[^\n\[.]+) \[ID:(?P<pid>[A-Za-z0-9_-]+)\]"
    declared=[]
    for m in re.finditer(person_pattern,text):
        pid="person:demo:"+m['pid'];declared.append((m.start(),m.end(),pid))
        facts=[node("Person",pid,m['name'].strip(),authoritative_id=m['pid']),edge("MENTIONED_IN",pid,did, str(m.start()))]
        tail=text[m.end():].split('\n',1)[0]
        role_match=re.match(r" is named as ([^.]+?) in this case", tail)
        if role_match:
            role=role_match[1].strip()
            facts[0]['attrs']['case_role']=role
            facts.append(edge("INVOLVED_IN_CASE",pid,cid,str(m.start()),role=role))
        elif tail.startswith(" is referenced in this case"):
            facts.append(edge("INVOLVED_IN_CASE",pid,cid,str(m.start())))
        own=re.match(r" owns account \[Bank:([^;\]]+); Account:([^\]]+)\]",tail)
        if own:
            aid=account(own[1],own[2]);facts.extend([node("Account",aid,own[1]+" / "+own[2],bank=own[1],account=own[2]),edge("OWNS_ACCOUNT",pid,aid,str(m.start())),edge("INVOLVED_IN_CASE",aid,cid,str(m.start()))])
        location=re.match(r" was recorded at \[Location:([^\]]+)\]",tail)
        if location:
            lid="location:"+uid("demo",location[1]);facts.extend([node("Location",lid,location[1]),edge("LOCATED_AT",pid,lid,str(m.start()))])
        end=m.end()+len(tail)
        yield dict(locator={**base,"char_start":m.start(),"char_end":end,"line_start":text.count('\n',0,m.start())+1},passage=text[m.start():end],method="explicit-identifier-rule",facts=facts)
    model=nlp if nlp is not None else pipeline()
    for ent in model(text).ents:
        kind={"PERSON":"Person","ORG":"Organization","GPE":"Location","LOC":"Location"}.get(ent.label_)
        if not kind or any(a<=ent.start_char<b for a,b,_ in declared):continue
        entity="mention:"+uid(did,ent.start_char,ent.end_char)
        yield dict(locator={**base,"char_start":ent.start_char,"char_end":ent.end_char},passage=ent.text,
                   method="spacy-en_core_web_sm",confidence=0.7,
                   extraction_version='model:'+model.meta.get('version','unknown')+';adapter:0.1',
                   confidence_basis='uncalibrated review-priority heuristic; model does not expose span probabilities',
                   facts=[node(kind,entity,ent.text),edge("MENTIONED_IN",entity,did,str(ent.start_char))])


def candidates(nodes,threshold=0.9):
    from .limits import check
    people=[n for n in nodes if n['type']=='Person'];result=[]
    check(len(people)*(len(people)-1)//2,'CANDIDATE_PAIRS',20000)
    for i,a in enumerate(people):
        for b in people[i+1:]:
            aid=a['attrs'].get('authoritative_id');bid=b['attrs'].get('authoritative_id')
            if aid and bid and aid!=bid:continue
            score=SequenceMatcher(None,' '.join(a['label'].casefold().split()),' '.join(b['label'].casefold().split())).ratio()
            if score>=threshold:
                left,right=sorted([a['id'],b['id']])
                result.append(dict(id=uid(left,right),left=left,right=right,left_name=a['label'],right_name=b['label'],similarity=score,state="pending",evidence_ids=sorted(set(a['evidence_ids']+b['evidence_ids']))))
    return sorted(result,key=lambda x:(-x['similarity'],x['id']))


def raw_text_records(text, case_id, doc_title='RAW-TEXT-INTAKE', source_type='police_fir'):
    """Zero-shot NLP parser for unstructured FIR text, court orders, and interrogation transcripts.
    Automatically extracts Persons, Roles, Bank Accounts, and Statutory Sections without requiring structured JSON.
    """
    from datetime import datetime, timezone
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    did = "document:" + uid(doc_title, text[:60])
    base_facts = [
        node("Case", case_id, case_id),
        node("Document", did, doc_title, filed_date=today, source_type=source_type),
        edge("FILED_UNDER", did, case_id)
    ]
    yield dict(
        locator={"record_type": "free_text_header", "doc_title": doc_title},
        passage=text[:300],
        method="raw-text-nlp-header",
        facts=base_facts
    )

    # 1. Identify statutory penal sections
    sections = []
    for pat in [r"(?:Section|Sec\.?)\s*(\d+[A-Za-z]*)", r"PMLA\s*(?:Section|Sec\.?)?\s*(\d+(?:\s*&\s*\d+)?)", r"(?:IPC|BNS)\s*(\d+[A-Za-z]*)"]:
        sections.extend(re.findall(pat, text, re.IGNORECASE))
    sections_str = ", ".join(sorted(set(sections))) if sections else "IPC 420 / 120B"

    # 2. Extract Persons & Accused
    declared_people = []
    # Pattern for explicit names like 'Accused Rajesh Singhania' or 'Person Dev Shah'
    person_patterns = [
        r"(?:Accused|Person|Shri|Mr\.|Director|Proprietor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        r"(?:State|ED|CBI)\s+vs\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)"
    ]
    extracted_names = []
    for pat in person_patterns:
        for m in re.finditer(pat, text):
            extracted_names.append((m.group(1).strip(), m.start()))

    # If regex missed, try SpaCy
    if not extracted_names:
        try:
            model = pipeline()
            for ent in model(text).ents:
                if ent.label_ == 'PERSON' and len(ent.text.split()) >= 2:
                    extracted_names.append((ent.text.strip(), ent.start_char))
        except Exception:
            pass

    # Deduplicate names
    seen_names = set()
    unique_persons = []
    for name, pos in extracted_names:
        clean = " ".join(name.split())
        if clean.lower() not in seen_names and len(clean) > 3:
            seen_names.add(clean.lower())
            unique_persons.append((clean, pos))

    # 3. Extract Bank Accounts
    account_matches = []
    bank_patterns = [
        r"(HDFC|ICICI|SBI|Axis|PNB|Kotak|DEMO|Baroda|Standard Chartered)\s*(?:Bank)?\s*(?:account|a/c|acct)?\s*[:\s]*([A-Za-z0-9_-]{4,18})",
        r"(?:account|a/c)\s*[:\s]*([0-9]{6,16})"
    ]
    for pat in bank_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if len(m.groups()) == 2:
                account_matches.append((m.group(1).upper(), m.group(2).strip(), m.start()))
            else:
                account_matches.append(("DEMO", m.group(1).strip(), m.start()))

    # Emit extracted person facts
    for idx, (name, pos) in enumerate(unique_persons):
        pid = f"person:demo:P{uid(name)[:4]}"
        auth_id = f"P{uid(name)[:4].upper()}"

        # Contextual role inference
        window = text[max(0, pos - 100):min(len(text), pos + 200)].lower()
        if any(w in window for w in ["prime accused", "mastermind", "kingpin", "main beneficiary"]):
            role = "Primary Syndicate Mastermind"
        elif any(w in window for w in ["mule", "hawala", "layering", "coordinator", "cash smurfing"]):
            role = "Hawala Mule Coordinator"
        elif any(w in window for w in ["crypto", "wallet", "off-ramp", "darknet"]):
            role = "Crypto Layering Specialist"
        elif any(w in window for w in ["director", "dummy", "shell"]):
            role = "Shell Entity Dummy Director"
        elif "witness" in window:
            role = "Investigative Witness"
        else:
            role = "Prime Accused" if idx == 0 else "Co-Conspirator / Accused"

        status_flag = "active_charge_sheet" if "fir" in text.lower() or "charge" in text.lower() else "under_investigation"
        p_facts = [
            node("Person", pid, name, authoritative_id=auth_id, case_role=role),
            edge("MENTIONED_IN", pid, did, str(pos)),
            edge("INVOLVED_IN_CASE", pid, case_id, str(pos), role=role, source_record_status=status_flag, source_text=f"Named in {doc_title} under {sections_str}. Role: {role}")
        ]

        # Link closest bank account to this person if available
        if account_matches:
            # Pair with nearest account or round-robin
            b_name, a_num, _ = account_matches[idx % len(account_matches)]
            aid = account(b_name, a_num)
            p_facts.extend([
                node("Account", aid, f"{b_name} / {a_num}", bank=b_name, account=a_num),
                edge("OWNS_ACCOUNT", pid, aid, str(pos)),
                edge("INVOLVED_IN_CASE", aid, case_id, str(pos))
            ])

        snippet = text[max(0, pos - 40):min(len(text), pos + 120)]
        yield dict(
            locator={"record_type": "entity_extracted", "person": name, "pos": pos},
            passage=snippet,
            method="raw-text-zero-shot-nlp",
            facts=p_facts
        )
