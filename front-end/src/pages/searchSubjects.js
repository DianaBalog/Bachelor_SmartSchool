import { React, useContext } from 'react';
import PageNavbar from '../components/PageNavbar';
import SearchSubjects from '../components/SearchSubjects';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';

const SearchSubjectPage = () => {
    const user = useContext(UserContext);

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
       <>
        <PageNavbar/>
        <SearchSubjects/>
       </>
    )
}

export default SearchSubjectPage;
