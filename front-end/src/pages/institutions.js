import { React, useContext } from 'react';
import Institutions from '../components/Institutions';
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

const InstitutionsPage= () => {
    const user = useContext(UserContext);

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <div className="Institutions">
            <PageNavbar/>
            <Institutions/>
        </div>
    )
}

export default InstitutionsPage;
