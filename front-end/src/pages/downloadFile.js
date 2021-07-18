import { React, useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import DownloadFile from '../components/DownloadFile';
import { IconContext } from 'react-icons/lib';
import { NavbarContainer, NavLogo, NavTransparentAndNot } from '../components/Navbar/NavbarElements';

const DownloadFilePage = () => {
    // const user = useContext(UserContext);

    let { fileName, id } = useParams();

    const[scrollNav, setScrollNav] = useState(false)
    
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

    // if(!user?.firstName){
    //     return <Redirect to="/"/>;
    // }

    return (
       <>
        <IconContext.Provider value={{ color: '#000'}}>
            <NavTransparentAndNot scrollNav={scrollNav}>
                   <NavbarContainer>
                        <NavLogo to='/'>Smart School</NavLogo>
                    </NavbarContainer>
                </NavTransparentAndNot>
        </IconContext.Provider>
        <DownloadFile fileName = {fileName} id = {id}/>
       </>
    )
}

export default DownloadFilePage;
