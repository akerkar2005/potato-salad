import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import './StickyHeader.css';
import aaruni from "../assets/aaruni.png";

function StickyHeader({ navigate }) {
    return (
        <div className="sticky-header">
            <button class="logo-button" onClick={() => navigate('/')}>
                <img src={aaruni} alt="Logo" />
            </button> 
            <div class="button-container">
            <button onClick={() => navigate('/')}>Home</button>
            <button onClick={() => navigate('/aboutus')}>About Us</button>
            </div>          

        </div>
    );
}

export default StickyHeader;