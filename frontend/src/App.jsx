import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import './App.css';
import AboutUs from './components/AboutUs';
import Home from './components/Home';

function App() {
    return (
        <Router basename="/potato-salad/">
            <AppWithBackground />
        </Router>
    );
}

function AppWithBackground() {
    const location = useLocation();
    const navigate = useNavigate();

    return (
        <div className="App">
            {/* Main content */}
            <Routes>
                <Route path="/" element={<Home navigate={navigate} />} />
                <Route path="/aboutus" element={<AboutUs navigate={navigate} />} />
            </Routes>
        </div>
    );
}

function StickyHeader({ navigate }) {
    return (
        <div className="sticky-header">
            <button onClick={() => navigate('/')}>Home</button>
            <button onClick={() => navigate('/aboutus')}>About Us</button>
        </div>
    );
}

export default App;