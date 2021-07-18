import { React, useContext } from 'react';
import Institution from '../components/Institution';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

const CurrentInstitutionPage= () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <div className="CurrentInstitution">
            <PageNavbar/>
            <Institution id ={id}/>
        </div>
    )
}

export default CurrentInstitutionPage;
