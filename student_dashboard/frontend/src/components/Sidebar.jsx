import React from 'react';
import { Search, RotateCcw } from 'lucide-react';

const FilterGroup = ({ label, options, selected, onChange }) => {
    return (
        <div className="filter-group">
            <label className="filter-label">{label}</label>
            <select
                multiple
                value={selected || []}
                onChange={(e) => {
                    const values = Array.from(e.target.selectedOptions, option => option.value);
                    onChange(values);
                }}
                style={{ height: '100px' }}
            >
                {options && options.map(opt => (
                    <option key={opt} value={opt}>{opt}</option>
                ))}
            </select>
        </div>
    );
};

const Sidebar = ({ options, filters, onFilterChange, onReset, recordCount }) => {
    return (
        <div className="sidebar">
            <div className="section-title" style={{ marginTop: 0, borderBottom: '2px solid #29ABE2', paddingBottom: '8px' }}>
                <Search size={16} /> FILTERS
            </div>

            <FilterGroup
                label="Gender"
                options={options.gender}
                selected={filters.gender}
                onChange={(val) => onFilterChange('gender', val)}
            />

            <FilterGroup
                label="Academic Stage"
                options={options.stage}
                selected={filters.stage}
                onChange={(val) => onFilterChange('stage', val)}
            />

            <FilterGroup
                label="Grade"
                options={options.grade}
                selected={filters.grade}
                onChange={(val) => onFilterChange('grade', val)}
            />

            <FilterGroup
                label="Subject / Topic"
                options={options.topic}
                selected={filters.topic}
                onChange={(val) => onFilterChange('topic', val)}
            />

            <FilterGroup
                label="Semester"
                options={options.semester}
                selected={filters.semester}
                onChange={(val) => onFilterChange('semester', val)}
            />

            <FilterGroup
                label="Parent Satisfaction"
                options={options.parent_sat}
                selected={filters.parent_sat}
                onChange={(val) => onFilterChange('parent_sat', val)}
            />

            <FilterGroup
                label="Absence Category"
                options={options.absence}
                selected={filters.absence}
                onChange={(val) => onFilterChange('absence', val)}
            />

            <button className="reset-btn" onClick={onReset}>
                <RotateCcw size={16} /> Reset Filters
            </button>

            <div style={{ marginTop: '16px', fontSize: '11px', color: '#718096', textAlign: 'center' }}>
                {recordCount}
            </div>
        </div>
    );
};

export default Sidebar;
