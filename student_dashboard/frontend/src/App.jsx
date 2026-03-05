import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import KPICard from './components/KPICard';
import ChartCard from './components/ChartCard';
import DataTable from './components/DataTable';
import { fetchDashboardData } from './api';
import { Users, Trophy, TrendingUp, AlertTriangle, Hand, BookOpen, MessageCircle } from 'lucide-react';
import './index.css';

const App = () => {
  const [filters, setFilters] = useState({
    gender: [],
    stage: [],
    grade: [],
    topic: [],
    semester: [],
    parent_sat: [],
    absence: []
  });

  const [options, setOptions] = useState({
    gender: [],
    stage: [],
    grade: [],
    topic: [],
    semester: [],
    parent_sat: [],
    absence: []
  });

  const [data, setData] = useState({
    kpis: {},
    charts: {},
    tableData: [],
    countLabel: "Loading..."
  });

  const [loading, setLoading] = useState(true);

  const loadData = async (currentFilters) => {
    setLoading(true);
    try {
      const result = await fetchDashboardData(currentFilters);
      setData(result);
      if (result.options) {
        setOptions(result.options);
      }
    } catch (error) {
      console.error("Dashboard failed to load:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(filters);
  }, [filters]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const resetFilters = () => {
    setFilters({
      gender: [],
      stage: [],
      grade: [],
      topic: [],
      semester: [],
      parent_sat: [],
      absence: []
    });
  };

  const { kpis, charts, tableData, countLabel } = data;

  return (
    <div className="app">
      <header className="dashboard-header">
        <div style={{ fontSize: '32px' }}>📊</div>
        <div>
          <h1 style={{ margin: 0, fontSize: '20px', fontWeight: 800 }}>Student Engagement & Performance Dashboard</h1>
          <p style={{ margin: '2px 0 0', fontSize: '12px', opacity: 0.8 }}>React + Python Analytics</p>
        </div>
      </header>

      <div className="dashboard-container">
        <Sidebar
          options={options}
          filters={filters}
          onFilterChange={handleFilterChange}
          onReset={resetFilters}
          recordCount={countLabel}
        />

        <main className="main-content">
          {/* KPI Row */}
          <div className="section-title">📊 Key Performance Indicators</div>
          <div className="kpi-row">
            <KPICard label="Total Students" value={kpis.total || 0} color="#29ABE2" icon={Users} />
            <KPICard label="% High Performers" value={kpis.pct_high || '0%'} color="#8DC63F" icon={Trophy} />
            <KPICard label="% Medium Performers" value={kpis.pct_med || '0%'} color="#29ABE2" icon={TrendingUp} />
            <KPICard label="% Low Performers" value={kpis.pct_low || '0%'} color="#E05C5C" icon={AlertTriangle} />
            <KPICard label="Avg Raised Hands" value={kpis.avg_hands || 0} color="#4472C4" icon={Hand} />
            <KPICard label="Avg Resources Visited" value={kpis.avg_res || 0} color="#8DC63F" icon={BookOpen} />
            <KPICard label="Avg Discussion" value={kpis.avg_disc || 0} color="#29ABE2" icon={MessageCircle} />
          </div>

          {/* Performance Overview */}
          <div className="section-title">🎯 Performance Overview</div>
          <div className="chart-grid grid-3">
            <ChartCard title="Distribution" figure={charts.perf_pie} height={360} />
            <ChartCard title="By Gender" figure={charts.perf_gender} height={360} />
            <ChartCard title="By Stage" figure={charts.perf_stage} height={360} />
          </div>

          {/* Engagement Analytics */}
          <div className="section-title">📡 Engagement Analytics</div>
          <div className="chart-grid grid-2">
            <ChartCard title="Raised Hands" figure={charts.hands_perf} height={340} />
            <ChartCard title="Resources Visited" figure={charts.res_perf} height={340} />
          </div>
          <div className="chart-grid grid-mix">
            <ChartCard title="Scatter" figure={charts.scatter} height={380} />
            <ChartCard title="Box Discussion" figure={charts.box_disc} height={380} />
          </div>

          {/* Attendance & Parent Insights */}
          <div className="section-title">🏫 Attendance & Parent Insights</div>
          <div className="chart-grid grid-3">
            <ChartCard title="Absence" figure={charts.absence_perf} height={340} />
            <ChartCard title="Satisfaction" figure={charts.sat_perf} height={340} />
            <ChartCard title="Survey" figure={charts.survey_perf} height={340} />
          </div>

          {/* Data Table */}
          <div className="section-title">📋 Filtered Student Records</div>
          <DataTable data={tableData} />
        </main>
      </div>
    </div>
  );
};

export default App;
