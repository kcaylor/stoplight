import React from 'react';
import './StatusUpdater.css'; // Import the CSS file

function StatusUpdater() {
    const handleClick = (status) => {
        fetch('/api/status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status }),
        });
    };

    return (
        <div className="status-updater">
            <button onClick={() => handleClick('red')} style={{ backgroundColor: 'red' }}>
                🚫
            </button>
            <button onClick={() => handleClick('yellow')} style={{ backgroundColor: 'yellow' }}>
                ⚠️
            </button>
            <button onClick={() => handleClick('green')} style={{ backgroundColor: 'green' }}>
                ✅
            </button>
        </div>
    );
}

export default StatusUpdater;