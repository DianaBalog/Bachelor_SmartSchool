import { React, useContext, useState } from 'react';
import { Redirect } from 'react-router';
import { Marginer } from '../marginer';
import { AccountContext } from './AccountContext';
import { BoxContainer, FormContainer, MutedLink, Input, BoldLink, ButtonLink, ErrorMessage, MutedMessage } from './Common';
import { UserContext } from '../../UserContext';

export const LoginForm = () => {
    const { switchToRegister } = useContext(AccountContext);

    const [login, setLogin] = useState();

    const [username, setUsername] = useState();
    const [password, setPassword] = useState();

    const user = useContext(UserContext);
    

    /*
        user login action
        username and password are requered
        error if the username or password are incorrect
    */
    function LoginAction() {
        if(username === "" || password === "" || username == null || password == null){
            setLogin("* fields are requerd!");
        }else {
            fetch('/user/login', {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.login === 1){
                        setLogin("Incorrect username or password!");
                    } else{
                        user.setCurrentUser({firstName: data.firstName, lastName: data.lastName, image: data.photo});
                    };                
                });
            };
    };

    if(user?.firstName){
        return <Redirect to="/user"/>;
    }

    return (
        <BoxContainer>
            <FormContainer>
                <Input type="username" placeholder="Username *" onChange={e => {setUsername(e.target.value); setLogin("")}} />
                <Input type="password" placeholder="Password *" onChange={e => {setPassword(e.target.value); setLogin("")}} />
            </FormContainer>
            <Marginer direction="vertical" margin={15} />
            <MutedLink to="#">Forget your password?</MutedLink>
            <Marginer direction="vertical" margin={15} />
            {login === "" && <Marginer direction="vertical" margin={12} />}
            <ErrorMessage>{login}</ErrorMessage>
            <Marginer direction="vertical" margin={29} />
            <ButtonLink to="#" type="submit" onClick={LoginAction} >Login</ButtonLink>
            <Marginer direction="vertical" margin={15} />
            <MutedMessage>Not a member yet?
                <BoldLink to="#" onClick={switchToRegister}>Register now</BoldLink>
            </MutedMessage>
        </BoxContainer>       
    )
}

export default LoginForm;