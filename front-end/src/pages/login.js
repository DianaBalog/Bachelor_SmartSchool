import { React, useState, useEffect } from 'react';
import RegisterAndLogin from '../components/RegisterAndLogin/index';
import { AppContainer } from '../components/RegisterAndLogin/RegisterAndLoginElements';
import { IconContext } from 'react-icons/lib';
import { NavbarContainer, NavLogo, NavTransparentAndNot } from '../components/Navbar/NavbarElements';

export const LoginPage = () => {
    const[scrollNav, setScrollNav] = useState(false)
    /**
     * To delimit sections of the homepage in order to scroll when the navigation bar links are pressed
     */
    const changeNav = () => {
        if(window.scrollY >=80) {
            setScrollNav(true)
        } else {
            setScrollNav(false)
        }
    }

    useEffect(() => {
        window.addEventListener('scroll', changeNav)
    }, []); 

    return (
        <>
        <IconContext.Provider value={{ color: '#000'}}>
            <NavTransparentAndNot scrollNav={scrollNav}>
                <NavbarContainer>
                    <NavLogo to='/'>Smart School</NavLogo>
                </NavbarContainer>
            </NavTransparentAndNot>
        </IconContext.Provider>
        <AppContainer>
            <RegisterAndLogin />
        </AppContainer>
        </>
    )
}

export default LoginPage;