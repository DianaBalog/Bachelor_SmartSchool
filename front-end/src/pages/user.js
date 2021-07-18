import { React, useContext } from 'react';
import PageNavbar from '../components/PageNavbar';
import User from '../components/User';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

const UserPage= () => {
    const user = useContext(UserContext);

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
        <>
            <PageNavbar/>
            <User/>
        </>
    )
}

export default UserPage;
