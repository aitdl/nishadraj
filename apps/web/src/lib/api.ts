/**
 * Project: NishadRaj OS
 * Organization: AITDL | NISHADRAJ
 * Organization: AITDL
 * License: AGPL-3.0 + Governance Protection Terms
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export async function fetchGovernanceStatus() {
    const res = await fetch(`${API_BASE_URL}/governance/status`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch governance status");
    return res.json();
}

export async function fetchGovernanceVersion() {
    const res = await fetch(`${API_BASE_URL}/governance/version`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch governance version");
    return res.json();
}

export async function fetchGovernanceHashes() {
    const res = await fetch(`${API_BASE_URL}/governance/hash`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch governance hashes");
    return res.json();
}

export async function fetchGovernanceSignature() {
    const res = await fetch(`${API_BASE_URL}/governance/signature`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch governance signature");
    return res.json();
}

export async function fetchGovernanceTasks() {
    const res = await fetch(`${API_BASE_URL}/governance/tasks`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch governance tasks");
    return res.json();
}

export async function fetchGovernanceConfig() {
    const res = await fetch(`${API_BASE_URL}/governance/config`, { cache: 'no-store' });
    if (!res.ok) throw new Error("Failed to fetch governance config");
    return res.json();
}
