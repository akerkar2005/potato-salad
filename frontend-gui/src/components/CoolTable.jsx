import React from 'react';
import './CoolTable.css';

const CoolTable = ({ data }) => {
  if (data.length === 0) {
    return <div>No data available</div>;
  }

  // Extract headers from the keys of the first dictionary
  const headers = Object.keys(data[0]);

  // Remove the 8th and 9th headers (assuming they are at index 7 and 8)
  const modifiedHeaders = [...headers.slice(0, 8), 'Sentiment'];

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
              {headers.slice(0, 8).map((header, cellIndex) => (
                <td key={cellIndex}>{row[header]}</td>
              ))}
              <td key="sentiment">
              <a target = '_blank'
              href = {`https://finance.yahoo.com/quote/${row[headers[0]]}/news`}>
              <div
                    style={{
                      width: '100%',
                      height: '100%',
                      backgroundColor: getColor(row[headers[8]], row[headers[9]]),
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#000', // Text color for better readability
                    }}>
                    {row[headers[8]]}
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