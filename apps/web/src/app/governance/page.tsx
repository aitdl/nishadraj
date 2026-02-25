/**
 * Project: NishadRaj OS
 * Organization: AITDL | NISHADRAJ
 * Organization: AITDL
 * License: AGPL-3.0 + Governance Protection Terms
 */

import {
    fetchGovernanceStatus,
    fetchGovernanceVersion,
    fetchGovernanceHashes,
    fetchGovernanceSignature,
    fetchGovernanceTasks,
    fetchGovernanceConfig
} from "../../../lib/api";
import { Card, Badge } from "../../../components/GovernanceUI";

export const dynamic = 'force-dynamic';

export default async function GovernanceDashboard() {
    let status, version, hashes, signature, tasks, config;
    let error = null;

    try {
        [status, version, hashes, signature, tasks, config] = await Promise.all([
            fetchGovernanceStatus(),
            fetchGovernanceVersion(),
            fetchGovernanceHashes(),
            fetchGovernanceSignature(),
            fetchGovernanceTasks(),
            fetchGovernanceConfig()
        ]).catch(e => {
            console.error(e);
            throw e;
        });
    } catch (e) {
        error = "Governance Integrity Compromised — System in Protected Mode";
    }

    if (error || (status && status.integrity_compromised)) {
        return (
            <div className="min-h-screen bg-[#000d1a] text-white p-8">
                <header className="mb-12 border-b border-red-500 pb-4">
                    <h1 className="text-4xl font-extrabold text-white tracking-tighter">NISHADRAJ OS <span className="text-red-500">GOVERNANCE</span></h1>
                    <p className="text-red-400 mt-2 font-mono">INTEGRITY FAILURE DETECTED</p>
                </header>
                <div className="bg-red-900/50 border border-red-500 p-8 rounded-lg mb-8">
                    <h2 className="text-2xl font-bold mb-4">{error || "CRITICAL SECURITY ALERT"}</h2>
                    <p>The system has entered protected mode. Interactive UI is disabled.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#000d1a] text-white p-8 font-sans">
            <header className="mb-12 border-b border-gold pb-4 flex justify-between items-center">
                <div>
                    <h1 className="text-4xl font-extrabold text-white tracking-tighter uppercase">NishadRaj OS <span className="text-gold">Governance</span></h1>
                    <p className="text-gray-400 mt-2 font-mono uppercase text-xs tracking-[0.3em]">Deterministic Transparency Layer</p>
                </div>
                <div className="text-right">
                    <p className="text-gold text-xs font-bold uppercase">Authorized Access Only</p>
                    <p className="text-gray-500 text-[10px] mt-1 italic">Copyright © AITDL | NISHADRAJ All Rights Reserved</p>
                </div>
            </header>

            <main className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* System Status */}
                <Card title="System Status" status="ok">
                    <div className="flex justify-between items-center">
                        <span>Status</span>
                        <Badge status={status?.system_status || "UNKNOWN"} />
                    </div>
                    <div className="flex justify-between items-center">
                        <span>Mode</span>
                        <span>{status?.governance_mode || "Deterministic"}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span>Legal</span>
                        <Badge status={status?.legal_status || "UNKNOWN"} />
                    </div>
                </Card>

                {/* Integrity Monitor */}
                <Card title="Integrity Monitor" status="ok">
                    <div className="flex justify-between">
                        <span className="text-gray-400">Version</span>
                        <span className="font-mono text-gold">{version?.schema_version}</span>
                    </div>
                    <div className="mt-4">
                        <p className="text-[10px] text-gray-500 uppercase font-bold mb-1">Schema Hash</p>
                        <p className="font-mono text-[9px] break-all text-blue-300">{hashes?.schema_hash}</p>
                    </div>
                    <div className="mt-2 text-xs">
                        <p className="text-[10px] text-gray-500 uppercase font-bold mb-1">Instance Hash</p>
                        <p className="font-mono text-[9px] break-all text-blue-300">{hashes?.instance_hash}</p>
                    </div>
                </Card>

                {/* Signature Status */}
                <Card title="Digital Signature" status={signature?.verified ? "ok" : "error"}>
                    <div className="flex justify-between items-center">
                        <span>Verified</span>
                        <span className={signature?.verified ? "text-green-400" : "text-red-400"}>
                            {signature?.verified ? "CRYPTOGRAPHIC_PASS" : "FAILED"}
                        </span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span>Algorithm</span>
                        <span className="font-mono">{signature?.algorithm}</span>
                    </div>
                    <div className="flex justify-between items-center">
                        <span>Enforced</span>
                        <span>{signature?.enforced ? "YES" : "NO"}</span>
                    </div>
                </Card>

                {/* Operational Model */}
                <Card title="Execution Model">
                    <div className="flex justify-between items-center">
                        <span>Model</span>
                        <span className="font-mono text-gold underline">{config?.execution_model}</span>
                    </div>
                    <div className="mt-4 border-t border-gray-800 pt-4">
                        <p className="text-[10px] text-gray-500 uppercase font-bold mb-2">Expansion Layer</p>
                        {config?.hybrid_expansion_layer && Object.entries(config.hybrid_expansion_layer).map(([key, val]) => (
                            <div key={key} className="flex justify-between text-[11px] mb-1 capitalize">
                                <span className="text-gray-300">{key.replace(/_/g, ' ')}</span>
                                <span className={val ? "text-green-400" : "text-red-400"}>{val ? "ENABLED" : "DISABLED"}</span>
                            </div>
                        ))}
                    </div>
                </Card>

                {/* Task Ledger */}
                <Card title="Task Ledger">
                    <div className="grid grid-cols-2 gap-4 text-center">
                        <div className="bg-black/30 p-2 rounded">
                            <p className="text-2xl font-bold text-gold">{tasks?.total || 0}</p>
                            <p className="text-[10px] text-gray-500 uppercase">Total</p>
                        </div>
                        <div className="bg-black/30 p-2 rounded">
                            <p className="text-2xl font-bold text-green-500">{tasks?.completed || 0}</p>
                            <p className="text-[10px] text-gray-500 uppercase">Success</p>
                        </div>
                    </div>
                    <div className="mt-4">
                        <p className="text-[10px] text-gray-500 uppercase font-bold mb-2">Audit Trace</p>
                        <div className="space-y-1">
                            {tasks?.recent_tasks?.map((task: any) => (
                                <div key={task.id} className="flex justify-between text-[10px] border-l border-gold pl-2">
                                    <span>{task.id}</span>
                                    <Badge status={task.status} />
                                </div>
                            ))}
                        </div>
                    </div>
                </Card>

                {/* Enforcement Monitor */}
                <Card title="Enforcement Flags" status="ok">
                    <div className="space-y-3">
                        <div className="flex items-center justify-between text-xs">
                            <span>Hard Determinism</span>
                            <span className="text-green-400">✓</span>
                        </div>
                        <div className="flex items-center justify-between text-xs">
                            <span>additionalProperties: false</span>
                            <span className="text-green-400">✓</span>
                        </div>
                        <div className="flex items-center justify-between text-xs">
                            <span>Schema Mismatch Blocking</span>
                            <span className="text-green-400">✓</span>
                        </div>
                        <div className="flex items-center justify-between text-xs">
                            <span>Autonomous Control</span>
                            <span className={config?.lifecycle_control?.autonomous_control ? "text-green-400" : "text-gray-400"}>
                                {config?.lifecycle_control?.autonomous_control ? "ACTIVE" : "STUB"}
                            </span>
                        </div>
                    </div>
                </Card>
            </main>

            <footer className="mt-12 pt-8 border-t border-gray-900 text-center">
                <p className="text-[10px] text-gray-600 uppercase tracking-widest">
                    Authorized Transparency Layer — NishadRaj OS — V{version?.schema_version}
                </p>
            </footer>
        </div>
    );
}
