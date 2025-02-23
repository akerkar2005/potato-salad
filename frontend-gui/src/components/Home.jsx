import React, { useState } from 'react';
import './Home.css';
import StickyHeader from './StickyHeader';
import CoolTable from './CoolTable';

const tableData = [
    ['Symbol', 'Short Name', 'forward P/E', 'current ratio', 'short ratio'],
    ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3', 'Row 1, Col 4', 'Row 1, Col 5'],
    ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3', 'Row 2, Col 4', 'Row 2, Col 5'],
    ['Row 3, Col 1', 'Row 3, Col 2', 'Row 3, Col 3', 'Row 3, Col 4', 'Row 3, Col 5'],
    ['Row 4, Col 1', 'Row 4, Col 2', 'Row 4, Col 3', 'Row 4, Col 4', 'Row 4, Col 5'],
    ['Row 5, Col 1', 'Row 5, Col 2', 'Row 5, Col 3', 'Row 5, Col 4', 'Row 5, Col 5']
];

const industries = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer Goods'];
const sectors = ['Software', 'Biotech', 'Banking', 'Oil & Gas', 'Retail'];

const Home = ({ navigate }) => {
    const [selectedIndustries, setSelectedIndustries] = useState(industries);
    const [selectedSectors, setSelectedSectors] = useState(sectors);
    const [minMarketCap, setMinMarketCap] = useState('0.0');
    const [maxMarketCap, setMaxMarketCap] = useState('0.0');
    const [shortRatio, setShortRatio] = useState('0.0');
    const [PERatio, setPERatio] = useState('0.0');
    const [currentRatio, setCurrentRatio] = useState('0.0');

    const handleCheckboxChange = (event, setSelectedItems) => {
        const { value, checked } = event.target;
        setSelectedItems(prevSelectedItems =>
            checked ? [...prevSelectedItems, value] : prevSelectedItems.filter(item => item !== value)
        );
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Validate numeric inputs
        if (isNaN(minMarketCap) || isNaN(maxMarketCap) || isNaN(shortRatio) || isNaN(PERatio) || isNaN(currentRatio) || selectedIndustries.length === 0 || selectedSectors.length === 0) {
            alert('Please enter valid numbers for Market Cap, Short Ratio, P/E Ratio, and Current Ratio.');
            return;
        }

        // Perform API call here
        console.log({
            selectedIndustries,
            selectedSectors,
            minMarketCap,
            maxMarketCap,
            shortRatio,
            PERatio,
            currentRatio
        });
    };

    return (
        <div className="main-comp">
            <StickyHeader navigate={navigate} />
            <h1>Welcome to the Stock Screener</h1>
            <div className="content-container">
                <form onSubmit={handleSubmit} className="stock-form">
                    <div className="form-group">
                        <label>Industry:</label>
                        {industries.map(industry => (
                            <div key={industry}>
                                <input
                                    type="checkbox"
                                    value={industry}
                                    checked={selectedIndustries.includes(industry)}
                                    onChange={(e) => handleCheckboxChange(e, setSelectedIndustries)}
                                />
                                {industry}
                            </div>
                        ))}
                    </div>
                    <div className="form-group">
                        <label>Sector:</label>
                        {sectors.map(sector => (
                            <div key={sector}>
                                <input
                                    type="checkbox"
                                    value={sector}
                                    checked={selectedSectors.includes(sector)}
                                    onChange={(e) => handleCheckboxChange(e, setSelectedSectors)}
                                />
                                {sector}
                            </div>
                        ))}
                    </div>
                    <div className="form-group">
                        <label>Min Market Cap:</label>
                        <input type="text" value={minMarketCap} onChange={(e) => setMinMarketCap(e.target.value)} placeholder="Enter minimum market cap" />
                    </div>
                    <div className="form-group">
                        <label>Max Market Cap:</label>
                        <input type="text" value={maxMarketCap} onChange={(e) => setMaxMarketCap(e.target.value)} placeholder="Enter maximum market cap" />
                    </div>
                    <div className="form-group">
                        <label>Short Ratio:</label>
                        <input type="text" value={shortRatio} onChange={(e) => setShortRatio(e.target.value)} placeholder="Enter short ratio" />
                    </div>
                    <div className="form-group">
                        <label>P/E Ratio:</label>
                        <input type="text" value={PERatio} onChange={(e) => setPERatio(e.target.value)} placeholder="Enter P/E ratio" />
                    </div>
                    <div className="form-group">
                        <label>Current Ratio:</label>
                        <input type="text" value={currentRatio} onChange={(e) => setCurrentRatio(e.target.value)} placeholder="Enter current ratio" />
                    </div>
                    <button type="submit" className="submit-button">Submit</button>
                </form>
                <CoolTable data={tableData} />
            </div>
        </div>
    );
};

export default Home;