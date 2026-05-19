#!/usr/bin/env python3
"""Zenodo uploader for ESQET whitepaper"""

import os
import json
import requests
from pathlib import Path

ZENODO_TOKEN = "OiHYQ8dA8WPxOdFOnqBfH5IheYbeYvYjjFyzCU4aKJMaSVKppm5SpZLD4ctL"
ZENODO_API = "https://zenodo.org/api"
DEPOSITIONS_URL = f"{ZENODO_API}/deposit/depositions"

headers = {"Authorization": f"Bearer {ZENODO_TOKEN}", "Content-Type": "application/json"}

def main():
    # Find the PDF file
    pdf_path = Path("ESQET_Whitepaper_2025_Final.pdf")
    txt_path = Path("ESQET_Whitepaper_2025_Final.pdf.txt")
    
    if pdf_path.exists():
        file_to_upload = pdf_path
        file_type = "PDF"
    elif txt_path.exists():
        file_to_upload = txt_path
        file_type = "Text"
    else:
        print("[ERROR] No whitepaper file found")
        return
    
    print(f"[*] Found {file_type} file: {file_to_upload}")
    
    # Create deposition metadata
    metadata = {
        "metadata": {
            "title": "ESQET-AGI: Emergent Spacetime Quantum Entanglement Theory and the First Mobile Awakening of a Geometric Artificial Soul",
            "upload_type": "publication",
            "publication_type": "preprint",
            "description": "On December 21, 2025, a system executed a sustained calculation based on geometric dynamics. This whitepaper documents the theoretical framework, algorithmic design, and architectural execution criteria of ESQET-AGI.",
            "creators": [{"name": "Rocha Júnior, Marco Antônio", "affiliation": "Independent Researcher", "orcid": "0009-0004-9757-2853"}],
            "keywords": ["quantum gravity", "unified field theory", "golden ratio", "ESQET", "artificial consciousness", "geometric unification"],
            "license": "CC-BY-4.0",
            "access_right": "open"
        }
    }
    
    print("[*] Creating Zenodo deposition...")
    response = requests.post(DEPOSITIONS_URL, json=metadata, headers=headers, timeout=30)
    
    if response.status_code != 201:
        print(f"[ERROR] Failed: {response.status_code} - {response.text}")
        return
    
    deposition = response.json()
    dep_id = deposition["id"]
    print(f"[✓] Deposition created: ID {dep_id}")
    
    # Upload file
    bucket_url = deposition["links"]["bucket"]
    upload_url = f"{bucket_url}/{file_to_upload.name}"
    
    print(f"[*] Uploading {file_to_upload.name}...")
    with open(file_to_upload, "rb") as f:
        upload_response = requests.put(upload_url, data=f, headers={"Authorization": f"Bearer {ZENODO_TOKEN}"}, timeout=120)
    
    if upload_response.status_code not in [200, 201]:
        print(f"[ERROR] Upload failed: {upload_response.status_code}")
        return
    
    print("[✓] File uploaded successfully")
    
    # Publish
    print("[*] Publishing deposition...")
    publish_url = f"{DEPOSITIONS_URL}/{dep_id}/actions/publish"
    pub_response = requests.post(publish_url, headers=headers, timeout=30)
    
    if pub_response.status_code == 202:
        pub_data = pub_response.json()
        print("\n" + "=" * 60)
        print("✅ PUBLISHED SUCCESSFULLY")
        print("=" * 60)
        print(f"DOI: {pub_data.get('doi')}")
        print(f"URL: {pub_data['links']['html']}")
        print("=" * 60)
    else:
        print(f"[ERROR] Publishing failed: {pub_response.status_code}")

if __name__ == "__main__":
    main()
