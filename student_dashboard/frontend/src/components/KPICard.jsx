import React from 'react';

const KPICard = ({ label, value, color, icon: Icon, emoji }) => {
    return (
        <div className="card kpi-card" style={{ borderTop: `3px solid ${color}` }}>
            <div style={{ fontSize: '20px', marginBottom: '4px' }}>
                {Icon ? <Icon size={20} color={color} /> : emoji}
            </div>
            <div id={`kpi-${label.toLowerCase().replace(/ /g, '-')}`}
                style={{ fontSize: '26px', fontWeight: '800', color: color, lineHeight: '1' }}>
                {value}
            </div>
            <div style={{ fontSize: '10px', color: '#718096', marginTop: '6px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '0.8px' }}>
                {label}
            </div>
        </div>
    );
};

export default KPICard;
