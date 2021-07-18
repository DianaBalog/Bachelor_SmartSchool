import { React, useContext } from 'react';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';
import CreateFolder from '../components/CreateFolder';

const CreateFolderPage = () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
     }
    return (
       <>
        <PageNavbar/>
        <CreateFolder id ={id}/>
       </>
    )
}

export default CreateFolderPage;
