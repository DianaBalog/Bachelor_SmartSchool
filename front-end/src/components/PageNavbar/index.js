import { React, useState, useEffect, useContext } from 'react';
import { IconContext } from 'react-icons/lib';
import { NavbarContainer, NavLogo, NavTransparentAndNot } from '../Navbar/NavbarElements';
import Menu from '@material-ui/core/Menu';
import { ButtonMenu } from '../Institution/InstitutionElements';
import { UserContext } from '../../UserContext';
import Tooltip from '@material-ui/core/Tooltip';
import Avatar from '@material-ui/core/Avatar';
import { NavbarBtn } from './PageNavbarElements';


const PageNavbar = () => {
    const[scrollNav, setScrollNav] = useState(false)
    const user = useContext(UserContext);
    
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
            user.setCurrentUser({});            
        }));
    };
    
    return(
        <IconContext.Provider value={{ color: '#000'}}>
            <NavTransparentAndNot scrollNav={scrollNav}>
                   <NavbarContainer>
                        <NavLogo to='/'>Smart School</NavLogo>
                        <NavbarBtn>
                            <Tooltip title={user.firstName + " " + user.lastName} onClick={handleClick}>
                                <Avatar alt={user.firstName} src={user.image}/>
                            </Tooltip>
                       </NavbarBtn>
                    </NavbarContainer>
                </NavTransparentAndNot>
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
    )
}

export default PageNavbar;