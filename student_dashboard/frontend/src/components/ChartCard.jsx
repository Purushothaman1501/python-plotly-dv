import React from 'react';
import Plot from 'react-plotly.js';

const ChartCard = ({ figure, title, height = 340 }) => {
    if (!figure || !figure.data) {
        return (
            <div className="card chart-card" style={{ height: `${height}px`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <p style={{ color: '#718096' }}>Loading {title}...</p>
            </div>
        );
    }

    // Ensure layout is merged with any specific chart config
    const layout = {
        ...figure.layout,
        height: height - 40, // Adjust for padding
        autosize: true,
    };

    return (
        <div className="card chart-card">
            <Plot
                data={figure.data}
                layout={layout}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: '100%', height: `${height - 20}px` }}
            />
        </div>
    );
};

export default ChartCard;
