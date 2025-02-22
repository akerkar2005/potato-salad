import React from 'react';
import './AboutUs.css';
import StickyHeader from './StickyHeader';
import aaruni from '../assets/aaruni.png'
import atharva from '../assets/atharva.png';

const teamMembers = [
  {
    name: 'Aaruni Gupta',
    role: 'Backend Developer/Data Analyst',
    image: aaruni,
    description: 'Webscraped the internet and developed a database for the New York Stock Exchange for this application.'
  },
  {
    name: 'Pablo Yague',
    role: 'Backend Developer/Data Analyst',
    image: 'path/to/jane.jpg',
    description: 'Webscraped a given webpage and developed a database for the NASDAQ stock with relevant information on various P/E ratios.'
  },
  {
    name: 'Atharva Kerkar',
    role: 'Frontend Developer/Machine Learning Interfacing',
    image: atharva,
    description: 'Developed the AI model interfacing for sentimental analysis and the frontend for the Stock Screener.'
  }
];

const AboutUs = ({ navigate }) => {
  return (
    <div className="main-comp">
        <StickyHeader navigate={navigate} />
        <div className="about-us">
            <h1>About Us</h1>
            <div className="team">
                {teamMembers.map((member, index) => (
                <div key={index} className="team-member">
                    <img src={member.image} alt={member.name} className="team-member-image" />
                    <h2>{member.name}</h2>
                    <h3>{member.role}</h3>
                    <p>{member.description}</p>
                </div>
                ))}
            </div>
        </div>
    </div>
  );
};

export default AboutUs;