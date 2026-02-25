/**
 * Project: NishadRaj OS
 * Organization: AITDL | NISHADRAJ
 * Organization: AITDL
 * License: AGPL-3.0 + Governance Protection Terms
 */

import React from 'react';

interface CardProps {
    title: string;
    children: React.ReactNode;
    status?: 'ok' | 'error' | 'warning';
}

export const Card: React.FC<CardProps> = ({ title, children, status }) => {
    const borderColor = status === 'ok' ? 'border-green-500' : status === 'error' ? 'border-red-500' : status === 'warning' ? 'border-yellow-500' : 'border-gray-800';

    return (
        <div className={`bg-[#001f3f] border ${borderColor} p-6 rounded-lg shadow-lg hover:shadow-gold transition-shadow duration-300`}>
            <h2 className="text-gold font-bold text-lg mb-4 uppercase tracking-wider">{title}</h2>
            <div className="text-white space-y-2">
                {children}
            </div>
        </div>
    );
};

export const Badge: React.FC<{ status: string }> = ({ status }) => {
    const colors = {
        ACTIVE: 'bg-green-600 text-white',
        PROTECTED: 'bg-yellow-600 text-white',
        COMPLETED: 'bg-green-600 text-white',
        IN_PROGRESS: 'bg-blue-600 text-white',
        FAILED: 'bg-red-600 text-white',
        SUCCESS: 'bg-green-600 text-white',
    };

    return (
        <span className={`px-2 py-1 rounded text-xs font-bold ${colors[status as keyof typeof colors] || 'bg-gray-600 text-white'}`}>
            {status}
        </span>
    );
};
