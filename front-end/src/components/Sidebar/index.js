import { React, useContext} from 'react';
import { SidebarContainer, Icon, CloseIcon, SidebarWrapper, SidebarMenu, SidebarLink, SideBtnWrap, SidebarRoute } from './SidebarElements';
import { UserContext } from '../../UserContext';
import Avatar from '@material-ui/core/Avatar';

/**
 * @param  {} {isOpen  when the sidebar is available (on smaller screen)
 * @param  {} toggle}  scroll to coresponding part of the homepage
 */
export const Sidebar = ({isOpen, toggle}) => {
    const user = useContext(UserContext);


    // user logout
    function Logout() {
        fetch('/user/logout').then(response => 
        response.json().then(data => {
            user.setCurrentUser({});
        }));
    };

    return (
        <SidebarContainer isOpen={isOpen} onClick={toggle}>
            <Icon onClick={toggle}>
                <CloseIcon />
            </Icon>
            <SidebarWrapper>
                <SidebarMenu>
                    <SidebarLink to="about" onClick={toggle}>About</SidebarLink>
                    <SidebarLink to="register" onClick={toggle}>Register</SidebarLink>
                    <SidebarLink to="features" onClick={toggle}>Features</SidebarLink>
                    <SidebarLink to="contactus" onClick={toggle}>Contact Us</SidebarLink>
                    {user?.firstName && <>
                        <SideBtnWrap>
                            <SidebarRoute style={{background: 'transparent'}} to="/user"><Avatar alt={user.firstName} src={user.image}/></SidebarRoute>
                        </SideBtnWrap>
                        </>} 
                </SidebarMenu>
                <SideBtnWrap>
                    {!user?.firstName && <SidebarRoute to="/login">Login</SidebarRoute> }
                    {user?.firstName &&<>
                        <SidebarRoute to="#" type="submit" onClick = {Logout}><span>Logout <b>{user.firstName}</b></span></SidebarRoute></> } 
                </SideBtnWrap>
            </SidebarWrapper>
        </SidebarContainer>
    )
}

export default Sidebar;