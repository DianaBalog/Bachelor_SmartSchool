import { React, useContext } from 'react';
import { useParams } from "react-router-dom";
import PageNavbar from '../components/PageNavbar';
import { UserContext } from '../UserContext';
import { Redirect } from 'react-router-dom';
import Post from '../components/Post';

const PostPage= () => {
    const user = useContext(UserContext);

    let { id } = useParams();

    if(!user?.firstName){
        return <Redirect to="/"/>;
    }
    return (
       <>
        <PageNavbar/>
        <Post id ={id}/>
       </>
    )
}

export default PostPage;
