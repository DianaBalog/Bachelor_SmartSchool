import { React, useContext } from 'react';
import CreateInstitution from '../components/CreateInstitution';
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

export const CreateInstitutionPage = () => {
    const user = useContext(UserContext);

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <>
        <PageNavbar/>
        <CreateInstitution/>
        </>
    )
}

export default CreateInstitutionPage;