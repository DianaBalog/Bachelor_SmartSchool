import { React, useState } from 'react';
import HeroSection from '../components/HeroSection';
import InfoSection from '../components/InfoSection';
import { homeAbout, homeRegister, homeContactUs } from '../components/InfoSection/Data';
import Navbar from "../components/Navbar";
import Features from '../components/Features';
import Sidebar from "../components/Sidebar";
import Footer from '../components/Footer';

export const Home = () => {
    const [isOpen, setIsOpen] = useState(false)
    
    const toggle = () => {
        setIsOpen(!isOpen)
    }

    return (
        <div className="Home">
            <Sidebar isOpen={isOpen} toggle={toggle} />
            <Navbar toggle={toggle} />
            <HeroSection />
            <InfoSection {...homeAbout}/>
            <InfoSection {...homeRegister}/>
            <Features />
            <InfoSection {...homeContactUs}/>
            <Footer />
        </div>
    )
}

export default Home;
