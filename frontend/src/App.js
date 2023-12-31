import React from 'react';
import './App.css';
import StatusDisplay from './StatusDisplay';
import StatusUpdater from './StatusUpdater';

function App() {
  return (
    <div className="App">
      <h1>EDS 217 Status Stoplight</h1>
      <StatusDisplay />
      <h2>How's the pace?</h2>
      <StatusUpdater />
    </div>
  );
}

export default App;