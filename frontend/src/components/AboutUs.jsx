import React from 'react';
import './AboutUs.css';
import StickyHeader from './StickyHeader';
import aaruni from '../assets/aaruni.png';
import atharva from '../assets/atharva.png';
import pablo from '../assets/pablo.png';

const teamMembers = [
  {
    name: 'Aaruni Gupta',
    role: 'Backend Developer/Data Analyst',
    description: 'Webscraped the internet and developed a database for the New York Stock Exchange for this application.',
    imageUrl: aaruni,
    linkedInUrl: 'https://www.linkedin.com/in/aaruni-g/',
    githubUrl: 'https://github.com/kanucool',
    resumeUrl: '/aaruni.pdf'
  },
  {
    name: 'Pablo Yague',
    role: 'Backend Developer/Data Analyst',
    description: 'Webscraped a given webpage and developed a database for the NASDAQ stock with relevant information on various P/E ratios.',
    imageUrl: pablo,
    linkedInUrl: 'https://www.linkedin.com/in/pablo-yague-garces-6877332b0/',
    githubUrl: 'https://github.com/pyaguega',
    resumeUrl: '/pablo.pdf'
  },
  {
    name: 'Atharva Kerkar',
    role: 'Frontend Developer/Machine Learning Interfacing',
    description: 'Developed the AI model interfacing for sentimental analysis and the frontend for the Stock Screener.',
    imageUrl: atharva,
    linkedInUrl: 'https://www.linkedin.com/in/atharva-kerkar-58b4a5290/',
    githubUrl: 'https://github.com/akerkar2005',
    resumeUrl: '/atharva.pdf'
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
            <div className="team-member" key={index}>
              <a href={member.linkedInUrl} target="_blank" rel="noopener noreferrer">
                <img src={member.imageUrl} alt={member.name} className="team-member-image" />
              </a>
              <h2>{member.name}</h2>
              <h3>{member.role}</h3>
              <p>{member.description}</p>
              <div className="social-links">
                <a href={member.linkedInUrl} target="_blank" rel="noopener noreferrer" className="social-link">
                  <i className="fab fa-linkedin"></i>
                </a>
                <a href={member.githubUrl} target="_blank" rel="noopener noreferrer" className="social-link">
                  <i className="fab fa-github"></i>
                </a>
                <a href={member.resumeUrl} target="_blank" rel="noopener noreferrer" className="social-link">
                  <i className="fas fa-file-download"></i>
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AboutUs;