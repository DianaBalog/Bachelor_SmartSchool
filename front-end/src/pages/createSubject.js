import { React, useContext } from 'react';
import CreateSubject from '../components/CreateSubject';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

export const CreateSubjectPage = () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <>
        <PageNavbar/>
        <CreateSubject id={id}/>
        </>
    )
}

export default CreateSubjectPage;