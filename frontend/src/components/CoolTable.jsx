import React from 'react';
import './CoolTable.css';

const CoolTable = ({ data }) => {
  if (data.length === 0) {
    return <div style={{ textAlign: 'center', padding: '20px', color: '#fff' }}>No data available</div>;
  }

  // Extract headers from the keys of the first dictionary
  const headers = Object.keys(data[0]);

  // Use explicit keys for sentiment and confidence
  const sentimentKey = headers.find(h => h.toLowerCase().includes('sentiment')) || 'sentiment';
  const confidenceKey = headers.find(h => h.toLowerCase().includes('confidence')) || 'confidence';
  const marketCapKey = headers.find(h => h.toLowerCase().includes('market cap')) || 'Market Cap';

  // Remove sentiment and confidence from headers for display
  const displayHeaders = headers.filter(h => h !== sentimentKey && h !== confidenceKey);
  const modifiedHeaders = [...displayHeaders, 'Sentiment'];

  // Function to get the color based on sentiment and confidence
  const getColor = (sentiment, confidence) => {
    let color;
    switch (sentiment) {
      case 'positive':
        color = `rgba(0, 255, 0, ${confidence})`; // Green with varying saturation
        break;
      case 'negative':
        color = `rgba(255, 0, 0, ${confidence})`; // Red with varying saturation
        break;
      case 'neutral':
        color = `rgba(255, 255, 255, ${confidence})`; // White with varying saturation
        break;
      default:
        color = `rgba(255, 255, 255, 1)`; // Default to white
    }
    return color;
  };

  return (
    <div className="cool-table-container">
      <table className="cool-table">
        <thead>
          <tr>
            {modifiedHeaders.map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {displayHeaders.map((header, cellIndex) => (
                <td key={cellIndex}>
                  {/* Fix Market Cap tuple bug */}
                  {header === marketCapKey && Array.isArray(row[header]) ? row[header][0] : row[header]}
                </td>
              ))}
              <td key="sentiment">
                <a target='_blank'
                  href={`https://finance.yahoo.com/quote/${row[headers[0]]}/news`}>
                  <div
                    style={{
                      width: '100%',
                      height: '100%',
                      backgroundColor: getColor(row[sentimentKey], row[confidenceKey]),
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#000', // Text color for better readability
                    }}>
                    {row[sentimentKey]}
                  </div>
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CoolTable;