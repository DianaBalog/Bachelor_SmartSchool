import { React, useContext } from 'react';
import Subject from '../components/Subject';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

const SubjectPage= () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
       <>
        <PageNavbar/>
        <Subject id ={id}/>
       </>
    )
}

export default SubjectPage;
