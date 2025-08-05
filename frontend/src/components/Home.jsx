import React, { useState, useEffect } from 'react';
import './Home.css';
import StickyHeader from './StickyHeader';
import CoolTable from './CoolTable';

const Home = ({ navigate }) => {
    // Submit form on Enter key anywhere on the page
    React.useEffect(() => {
        const handleEnter = (e) => {
            if (e.key === 'Enter') {
                // Prevent default only if not focused on textarea or text input
                if (
                    document.activeElement.tagName !== 'TEXTAREA' &&
                    !(document.activeElement.tagName === 'INPUT' && document.activeElement.type === 'text')
                ) {
                    const form = document.querySelector('.stock-form');
                    if (form) form.requestSubmit();
                }
            }
        };
        window.addEventListener('keydown', handleEnter);
        return () => window.removeEventListener('keydown', handleEnter);
    }, []);
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
    const server = "https://potato-salad-backend-d5b51d0a4e6b.herokuapp.com/api"

    useEffect(() => {
        // Make an API call when the component loads
        const fetchData = async () => {
            try {
                const response = await fetch(`${server}/launch`, {
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
            'industry': selectedIndustries.join(','),
            'sector': selectedSectors.join(','),
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
            const response = await fetch(`${server}/update`, {
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
                <label className="title">Options</label>
                <label className="subtitle-label">Sector</label>
                    <div className="form-group-prime">
                        {sectors.map(sector => (
                            <div key={sector}>
                                <input
                                    type="checkbox"
                                    value={sector}
                                    checked={selectedSectors.includes(sector)}
                                    onChange={(e) => handleCheckboxChange(e, setSelectedSectors)}
                                    style={{ display: 'none' }}
                                    id={`sector-${sector}`}
                                />
                                <span
                                    className={`checkbox-label${selectedSectors.includes(sector) ? ' selected' : ''}`}
                                    role="button"
                                    tabIndex={0}
                                    onClick={e => {
                                        e.preventDefault();
                                        if (selectedSectors.includes(sector)) {
                                            setSelectedSectors(selectedSectors.filter(item => item !== sector));
                                        } else {
                                            setSelectedSectors([...selectedSectors, sector]);
                                        }
                                    }}
                                    onKeyDown={e => {
                                        if (e.key === 'Enter' || e.key === ' ') {
                                            e.preventDefault();
                                            if (selectedSectors.includes(sector)) {
                                                setSelectedSectors(selectedSectors.filter(item => item !== sector));
                                            } else {
                                                setSelectedSectors([...selectedSectors, sector]);
                                            }
                                        }
                                    }}
                                >
                                    {sector}
                                </span>
                            </div>
                        ))}
                    </div>
                    <label className="subtitle-label">Industry</label>
                    <div className="form-group-prime">
                        {industries.map(industry => (
                            <div key={industry}>
                                <input
                                    type="checkbox"
                                    value={industry}
                                    checked={selectedIndustries.includes(industry)}
                                    onChange={(e) => handleCheckboxChange(e, setSelectedIndustries)}
                                    style={{ display: 'none' }}
                                    id={`industry-${industry}`}
                                />
                                <span
                                    className={`checkbox-label${selectedIndustries.includes(industry) ? ' selected' : ''}`}
                                    role="button"
                                    tabIndex={0}
                                    onClick={e => {
                                        e.preventDefault();
                                        if (selectedIndustries.includes(industry)) {
                                            setSelectedIndustries(selectedIndustries.filter(item => item !== industry));
                                        } else {
                                            setSelectedIndustries([...selectedIndustries, industry]);
                                        }
                                    }}
                                    onKeyDown={e => {
                                        if (e.key === 'Enter' || e.key === ' ') {
                                            e.preventDefault();
                                            if (selectedIndustries.includes(industry)) {
                                                setSelectedIndustries(selectedIndustries.filter(item => item !== industry));
                                            } else {
                                                setSelectedIndustries([...selectedIndustries, industry]);
                                            }
                                        }
                                    }}
                                >
                                    {industry}
                                </span>
                            </div>
                        ))}
                    </div>
                    <div className="form-fields">
                        <div className="form-group">
                            <label className="small-subtitle-label">Min Market Cap</label>
                            <input type="text" value={minMarketCap} onChange={(e) => setMinMarketCap(e.target.value)} placeholder="Enter minimum market cap" />
                        </div>
                        <div className="form-group">
                            <label className="small-subtitle-label">Max Market Cap</label>
                            <input type="text" value={maxMarketCap} onChange={(e) => setMaxMarketCap(e.target.value)} placeholder="Enter maximum market cap" />
                        </div>
                        <div className="form-group">
                            <label className="small-subtitle-label">Short Ratio</label>
                            <input type="text" value={shortRatio} onChange={(e) => setShortRatio(e.target.value)} placeholder="Enter short ratio" />
                        </div>
                        <div className="form-group">
                            <label className="small-subtitle-label">P/E Ratio</label>
                            <input type="text" value={PERatio} onChange={(e) => setPERatio(e.target.value)} placeholder="Enter P/E ratio" />
                        </div>
                        <div className="form-group">
                            <label className="small-subtitle-label">Current Ratio</label>
                            <input type="text" value={currentRatio} onChange={(e) => setCurrentRatio(e.target.value)} placeholder="Enter current ratio" />
                        </div>
                    </div>
                    <button type="submit" className="submit-button">Submit</button>
                </form>
                <CoolTable data={tableData} />
            </div>
        </div>
    );
};

export default Home;