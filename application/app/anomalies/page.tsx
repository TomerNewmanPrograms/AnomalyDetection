import React from "react";
import styles from './AnomaliesPage.module.css';

interface Anomaly {
    cpu: string;
    memory: string;
    id: number;
    time: string;
    _uid: string;
}

const AnomaliesPage: React.FC = async () => {
    const res = await fetch('https://jsonplaceholder.typicode.com/users');
    let anomalies: Anomaly[] = await res.json();

    anomalies = anomalies.map((anomaly, index) => ({
        ...anomaly,
        _uid: `${anomaly.id}-${Date.now()}-${index}`
    }));

    return (
        <div className={styles.container}>
            <h1>AnomaliesPage</h1>
            <ul>
                {anomalies.map(anomaly => (
                    <li key={anomaly._uid} className={styles.detail}>
                        <strong>ID:</strong> {anomaly.id}, <strong>CPU:</strong> {anomaly.cpu}, <strong>Memory:</strong> {anomaly.memory}, <strong>Time:</strong> {anomaly.time}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AnomaliesPage;
