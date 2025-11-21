/**
 * Main Entry Point for React App
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import BouncingBallsApp from './components/BouncingBallsApp.jsx';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <BouncingBallsApp />
    </React.StrictMode>
);
