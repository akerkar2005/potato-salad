import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import './App.css';
import AboutUs from './components/AboutUs';
import Home from './components/Home';

function App() {
    document.title = "Stock Screener";
    return (
        <Router>
            <AppWithBackground />
        </Router>
    );
}

function AppWithBackground() {
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.key === '1') {
                navigate('/');
            } else if (event.key === '2') {
                navigate('/aboutus');
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [navigate]);

    return (
        <div className="App">
            {/* Main content */}
            <Routes>
                <Route path="/" element={<Home navigate={navigate} />} />
                <Route path="/aboutus" element={<AboutUs navigate={navigate} />} />
            </Routes>
        </div>
    );
}

function StickyHeader({ navigate }) {
    return (
        <div className="sticky-header">
            <button onClick={() => navigate('/')}>Home</button>
            <button onClick={() => navigate('/aboutus')}>About Us</button>
        </div>
    );
}

export default App;