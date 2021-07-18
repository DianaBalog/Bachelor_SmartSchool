import { React, useContext } from 'react';
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';
import { useParams } from "react-router-dom";
import ParticipantsSubject from '../components/ParticipantsSubject';

const ParticipantsSubjectPage = () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <>
            <PageNavbar/>
            <ParticipantsSubject id={id}/>
        </>
    )
}

export default ParticipantsSubjectPage;
