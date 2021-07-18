import { React, useContext } from 'react';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';
import UploadFiles from '../components/UploadFiles';

const UploadFilesPage= () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
     }
    return (
       <>
        <PageNavbar/>
        <UploadFiles id ={id}/>
       </>
    )
}

export default UploadFilesPage;
