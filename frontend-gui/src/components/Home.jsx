import React, { useState, useEffect } from 'react';
import './Home.css';
import StickyHeader from './StickyHeader';
import CoolTable from './CoolTable';

const Home = ({ navigate }) => {
    const [tableData, setTableData] = useState([]);
    const [industries, setIndustries] = useState([]);
    const [sectors, setSectors] = useState([]);
    const [selectedIndustries, setSelectedIndustries] = useState([]);
    const [selectedSectors, setSelectedSectors] = useState([]);
    const [minMarketCap, setMinMarketCap] = useState('0.0');
    const [maxMarketCap, setMaxMarketCap] = useState('0.0');
    const [shortRatio, setShortRatio] = useState('0.0');
    const [PERatio, setPERatio] = useState('0.0');
    const [currentRatio, setCurrentRatio] = useState('0.0');

    useEffect(() => {
        // Make an API call when the component loads
        const fetchData = async () => {
            try {
                const response = await fetch('http://localhost:3000/api/launch', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                });
                const data = await response.json();
                console.log(data);
                setTableData(data.sortedStocks);
                setIndustries(data.industries);
                setSectors(data.sectors);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, []);

    const handleCheckboxChange = (event, setSelectedItems) => {
        const { value, checked } = event.target;
        setSelectedItems(prevSelectedItems =>
            checked ? [...prevSelectedItems, value] : prevSelectedItems.filter(item => item !== value)
        );
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        // Validate numeric inputs
        if (isNaN(minMarketCap) || isNaN(maxMarketCap) || isNaN(shortRatio) || isNaN(PERatio) || isNaN(currentRatio) || minMarketCap > maxMarketCap) {
            alert('Please enter valid numbers for Market Cap, Short Ratio, P/E Ratio, and Current Ratio.');
            return;
        }
        const preferences = {
            'industry': selectedIndustries,
            'sector': selectedSectors,
        };

        const displayFields = [minMarketCap, maxMarketCap, shortRatio, PERatio, currentRatio];
        const numericFields = ['minMarketCap', 'maxMarketCap', 'shortRatio', 'forwardPE', 'currentRatio'];
        for (let i = 0; i < displayFields.length; i++) {
            if (parseFloat(displayFields[i]) == 0.0) {
                continue;
            }
            preferences[numericFields[i]] = displayFields[i];
        }
    
        try {
            const response = await fetch('http://localhost:3000/api/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(preferences)
            });
            const data = await response.json();
            setTableData(data.sortedStocks);
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    return (
        <div className="main-comp">
            <StickyHeader navigate={navigate} />
            <div className="content-container">
                <form onSubmit={handleSubmit} className="stock-form">
                <label>Sector:</label>
                    <div className="form-group-prime">
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
                    <label>Industry:</label>
                    <div className="form-group-prime">
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