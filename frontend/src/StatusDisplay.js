import React, { useState, useEffect } from 'react';
import './StatusDisplay.css';

function StatusDisplay() {
    const [statusSummary, setStatusSummary] = useState({ red: 0, yellow: 0, green: 0 });
    const [totalUpdates, setTotalUpdates] = useState(0);

    useEffect(() => {
        const fetchData = async () => {
            const response = await fetch('/api/status_summary');
            const data = await response.json();
            setStatusSummary(data);
            console.log('Data:', data); // Log the fetched data

            const newTotalUpdates = data.total;
            setTotalUpdates(newTotalUpdates);
            console.log('Total updates:', newTotalUpdates);
        };

        const intervalId = setInterval(fetchData, 1000); // Fetch data every 1 seconds
        fetchData(); // Fetch initial data

        return () => clearInterval(intervalId); // Cleanup on unmount
    }, []);

    const total = statusSummary.red + statusSummary.yellow + statusSummary.green;
    const redWidth = total === 0 ? 0 : (statusSummary.red / total) * 100;
    const yellowWidth = total === 0 ? 0 : (statusSummary.yellow / total) * 100;
    const greenWidth = total === 0 ? 0 : (statusSummary.green / total) * 100;

    return (
        <div className="status-display">
            <div className="bar">
                <div className="red" style={{ width: `${redWidth}%` }}></div>
                <div className="yellow" style={{ width: `${yellowWidth}%` }}></div>
                <div className="green" style={{ width: `${greenWidth}%` }}></div>
            </div>
            <p>Total updates in the past 10 minutes: {totalUpdates}</p>
        </div>
    );
}

export default StatusDisplay;