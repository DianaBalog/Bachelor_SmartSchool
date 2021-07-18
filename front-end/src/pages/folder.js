import { React, useContext } from 'react';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';
import Folder from '../components/Folder';

const FolderPage = () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
     }
    return (
       <>
        <PageNavbar/>
        <Folder id ={id}/>
       </>
    )
}

export default FolderPage;
