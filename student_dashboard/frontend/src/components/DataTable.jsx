import React from 'react';

const DataTable = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <div className="card" style={{ padding: '20px', textAlign: 'center', color: '#718096' }}>
                No records found.
            </div>
        );
    }

    const columns = Object.keys(data[0]);

    return (
        <div className="table-container card">
            <table>
                <thead>
                    <tr>
                        {columns.map(col => (
                            <th key={col}>{col}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, idx) => (
                        <tr key={idx}>
                            {columns.map(col => {
                                let cellClass = "";
                                if (col === 'Class') {
                                    if (row[col] === 'High') cellClass = 'perf-high';
                                    else if (row[col] === 'Medium') cellClass = 'perf-med';
                                    else if (row[col] === 'Low') cellClass = 'perf-low';
                                }
                                return (
                                    <td key={col} className={cellClass}>
                                        {row[col]}
                                    </td>
                                );
                            })}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default DataTable;
