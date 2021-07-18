import { React, useState, useEffect, useContext } from 'react';
import { FaBars } from 'react-icons/fa';
import { IconContext } from 'react-icons/lib';
import { animateScroll as scroll } from 'react-scroll';
import { Nav, NavbarContainer, NavLogo, MobileIcon, NavMenu, NavItem, NavLinks, NavBtn, NavBtnLink } from './NavbarElements';
import { UserContext } from '../../UserContext';
import Avatar from '@material-ui/core/Avatar';
import Menu from '@material-ui/core/Menu';
import { ButtonMenu } from '../Institution/InstitutionElements';
import Tooltip from '@material-ui/core/Tooltip';


const Navbar = ({toggle}) => {
    const[scrollNav, setScrollNav] = useState(false)
    const user = useContext(UserContext);

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
    
    const toggleHome = () => {
        scroll.scrollToTop();
    }

    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };


    // user logout
    function Logout() {
        fetch('/user/logout').then(response => 
        response.json().then(data => {
            handleClose();
            user.setCurrentUser({});            
        }));
    };


    return (
        <>
        <IconContext.Provider value={{ color: '#fff'}}>
            <Nav scrollNav={scrollNav}>
                <NavbarContainer>
                    <NavLogo to='/' onClick={toggleHome}>Smart School</NavLogo>
                    <MobileIcon onClick={toggle}>
                        <FaBars />
                    </MobileIcon>
                    <NavMenu>
                        <NavItem>
                            <NavLinks to="about" smooth='true' duration={500} spy={true} exact='true' offset={-80}>About</NavLinks>
                        </NavItem>
                        <NavItem>
                            <NavLinks to="register" smooth='true' duration={500} spy={true} exact='true' offset={-80}>Register</NavLinks>
                        </NavItem>
                        <NavItem>
                            <NavLinks to="features" smooth='true' duration={500} spy={true} exact='true' offset={-80}>Features</NavLinks>
                        </NavItem>
                        <NavItem>
                            <NavLinks to="contactus" smooth='true' duration={500} spy={true} exact='true' offset={-80}>Contact Us</NavLinks>
                        </NavItem>
                    </NavMenu>
                    <NavBtn>
                        {!user?.firstName && <NavBtnLink to="/login">Login</NavBtnLink> }
                        {user?.firstName && <>
                        <Tooltip title={user.firstName + " " + user.lastName} onClick={handleClick}>
                            <Avatar alt={user.firstName} src={user.image}/>
                        </Tooltip> </>} 
                    </NavBtn>
                </NavbarContainer>
            </Nav>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <ButtonMenu to="/user">My Page</ButtonMenu>
                <ButtonMenu to="/institutions">My Institutions</ButtonMenu>
                <ButtonMenu to="#" type="submit" onClick = {Logout}><span>Logout <b>{user.firstName}</b></span></ButtonMenu>
            </Menu>
        </IconContext.Provider>
        </>
    )
}

export default Navbar;
