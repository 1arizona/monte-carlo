import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { type PercentileResult, runClientSimulation } from '../math/monteCarlo';

export const Simulator: React.FC = () => {
  const [initialCapital, setInitialCapital] = useState<number>(50000);
  const [annualReturn, setAnnualReturn] = useState<number>(0.08);
  const [annualVolatility, setAnnualVolatility] = useState<number>(0.15);
  const [years, setYears] = useState<number>(10);
  const [data, setData] = useState<PercentileResult[]>([]);

  useEffect(() => {
    const res = runClientSimulation(initialCapital, annualReturn, annualVolatility, years);
    setData(res);
  }, [initialCapital, annualReturn, annualVolatility, years]);

  return (
    <div style={{ padding: '24px', maxWidth: '1000px', margin: '0 auto', fontFamily: 'sans-serif' }}>
      <h2 style={{ color: '#0f172a', marginBottom: '16px', fontSize: '24px', fontWeight: 'bold' }}>Monte Carlo Portfolio Simulator</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', background: '#f5f5f5', padding: '16px', borderRadius: '8px', marginBottom: '24px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold' }}>Initial Capital ($)</label>
          <input 
            type="number" 
            value={initialCapital} 
            onChange={(e) => setInitialCapital(Number(e.target.value))}
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        <div>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold' }}>Expected Return (%)</label>
          <input 
            type="number" 
            step="0.5"
            value={annualReturn * 100} 
            onChange={(e) => setAnnualReturn(Number(e.target.value) / 100)}
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        <div>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold' }}>Volatility (%)</label>
          <input 
            type="number" 
            step="0.5"
            value={annualVolatility * 100} 
            onChange={(e) => setAnnualVolatility(Number(e.target.value) / 100)}
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
        <div>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold' }}>Time Horizon (Years)</label>
          <input 
            type="number" 
            value={years} 
            onChange={(e) => setYears(Number(e.target.value))}
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
        </div>
      </div>

      <div style={{ height: '400px', width: '100%', background: '#fff', padding: '16px', borderRadius: '8px', border: '1px solid #ddd' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="year" unit=" yrs" />
            <YAxis tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
            <Tooltip formatter={(val: number) => [`$${val.toLocaleString()}`]} />
            <Legend />
            <Line type="monotone" dataKey="p90" name="Optimistic (p90)" stroke="#10B981" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="p50" name="Median (p50)" stroke="#3B82F6" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="p10" name="Pessimistic (p10)" stroke="#EF4444" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};