import React, { useState, useEffect } from 'react';
import './StickyHeader.css';
import potato from "../assets/potato.png";

function StickyHeader({ navigate }) {
    const [flippedButton, setFlippedButton] = useState(null);

    useEffect(() => {
        // On mount, show text (back) by adding .flipped to all flip buttons
        const buttons = document.querySelectorAll('.flip-button');
        buttons.forEach(button => button.classList.add('flipped'));
        // After a short delay, remove .flipped to flip to icon (front)
        setTimeout(() => {
            buttons.forEach(button => button.classList.remove('flipped'));
        }, 600); // Adjust delay for desired effect
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
            <div className="logo-title-container">
                <button className="logo-button" onClick={(e) => handleClick(e, '/')}>
                    <img src={potato} alt="Logo" />
                </button>
                <h1 onClick={(e) => handleClick(e, '/')}>Potato Salad</h1>
            </div>
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