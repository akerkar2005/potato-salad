import React, { useState, useEffect } from 'react';
import './StickyHeader.css';
import aaruni from "../assets/aaruni.png";

function StickyHeader({ navigate }) {
    const [flippedButton, setFlippedButton] = useState(null);

    useEffect(() => {
        // Add the 'flipped' class to all buttons on startup
        const buttons = document.querySelectorAll('.flip-button');
        buttons.forEach(button => button.classList.add('flipped'));

        // Remove the 'flipped' class after a short delay to flip them back up
        setTimeout(() => {
            buttons.forEach(button => button.classList.remove('flipped'));
        }, 300); // Adjust the delay as needed
    }, []);

    const handleClick = (event, path) => {
        setFlippedButton(event.currentTarget);
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => {
            navigate(path);
        }, 100); // Adjust the timeout duration as needed
    };

    return (
        <div className="sticky-header">
            <button className="logo-button" onClick={() => navigate('/')}>
                <img src={aaruni} alt="Logo" />
            </button> 
            <div className="button-container">
                <button
                    className="flip-button"
                    onClick={(e) => handleClick(e, '/')}
                >
                    <div className="flip-content">
                        <div className="flip-front">
                            <i className="fas fa-home"></i>
                        </div>
                        <div className="flip-back">
                            Home
                        </div>
                    </div>
                </button>
                <button
                    className="flip-button"
                    onClick={(e) => handleClick(e, '/aboutus')}
                >
                    <div className="flip-content">
                        <div className="flip-front">
                            <i className="fas fa-question"></i>
                        </div>
                        <div className="flip-back">
                            About
                        </div>
                    </div>
                </button>
            </div>          
        </div>
    );
}

export default StickyHeader;