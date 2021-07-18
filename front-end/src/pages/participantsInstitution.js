import { React, useContext } from 'react';
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';
import { useParams } from "react-router-dom";
import ParticipantsInstitution from '../components/ParticipantsInstitution';

const ParticipantsInstitutionPage = () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <>
            <PageNavbar/>
            <ParticipantsInstitution id={id}/>
        </>
    )
}

export default ParticipantsInstitutionPage;
