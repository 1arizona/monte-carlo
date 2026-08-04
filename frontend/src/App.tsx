import React from 'react';
import { Simulator } from './components/Simulator';

export const App: React.FC = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', paddingTop: '40px' }}>
      <Simulator />
    </div>
  );
};

export default App;