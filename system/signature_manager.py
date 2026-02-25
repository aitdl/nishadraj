"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Role: Software Architect
Organization: AITDL
Websites: https://aitdl.com | https://nishadraj.com
Governance Version: 1.1.0
"""

import os
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

# Paths
BASE_DIR = "d:/IMP/GitHub/nishadraj"
SECURITY_DIR = os.path.join(BASE_DIR, "security")
PRIVATE_KEY_PATH = os.path.join(SECURITY_DIR, "system_private_key.pem")
PUBLIC_KEY_PATH = os.path.join(SECURITY_DIR, "system_public_key.pem")
REGISTRY_PATH = os.path.join(SECURITY_DIR, "signature_registry.json")

GOVERNANCE_FILES = [
    os.path.join(BASE_DIR, "governance/ai-governance.schema.json"),
    os.path.join(BASE_DIR, "governance/governance.lock.json"),
    os.path.join(BASE_DIR, "system/task_registry.json"),
    os.path.join(BASE_DIR, "docs/DOCUMENTATION_MANIFEST.md"),
    os.path.join(BASE_DIR, "public/github/ORG_PROFILE_README.md"),
    os.path.join(BASE_DIR, "public/website/LANDING_PAGE_COPY.md"),
    os.path.join(BASE_DIR, "public/whitepaper/NISHADRAJ_OS_WHITEPAPER.md")
]

def ensure_security_dir():
    if not os.path.exists(SECURITY_DIR):
        os.makedirs(SECURITY_DIR)
        print(f"Created directory: {SECURITY_DIR}")

def generate_keypair():
    ensure_security_dir()
    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        print("Keypair already exists.")
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )

    # Save Private Key
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save Public Key
    public_key = private_key.public_key()
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    # Restrict permissions (Wait: Windows might not support chmod 600 easily via Python)
    print("Generated 4096-bit RSA keypair.")

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

def generate_signature(file_path):
    private_key = load_private_key()
    with open(file_path, "rb") as f:
        data = f.read()
    
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

def verify_signature(file_path, signature_b64):
    try:
        public_key = load_public_key()
        signature = base64.b64decode(signature_b64)
        with open(file_path, "rb") as f:
            data = f.read()
        
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Signature verification failed for {file_path}: {e}")
        return False

def sign_governance_files():
    generate_keypair()
    registry = {"signed_files": {}, "last_signed_at": datetime.now().isoformat()}
    
    for file_path in GOVERNANCE_FILES:
        if os.path.exists(file_path):
            sig = generate_signature(file_path)
            # Store relative path for portability if needed, but here absolute is fine
            registry["signed_files"][file_path] = sig
            print(f"Signed: {file_path}")
        else:
            print(f"WARNING: File not found for signing: {file_path}")
    
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)
    print(f"Signature registry updated: {REGISTRY_PATH}")

def verify_all_governance_files():
    if not os.path.exists(REGISTRY_PATH):
        print("ERROR: Signature registry missing.")
        return False
    
    with open(REGISTRY_PATH, "r") as f:
        registry = json.load(f)
    
    for file_path, sig in registry.get("signed_files", {}).items():
        if not verify_signature(file_path, sig):
            return False
    
    print("All governance signatures verified successfully.")
    return True

if __name__ == "__main__":
    ensure_security_dir()
    sign_governance_files()
