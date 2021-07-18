import { React, useContext, useState } from 'react';
import { Marginer } from '../marginer';
import { AccountContext } from './AccountContext';
import { BoxContainer, FormContainer, Input, BoldLink, ButtonLink, ErrorMessage, SuccessMessage, MutedMessage } from './Common';

export const RegisterForm = () => {
    const { switchToLogin } = useContext(AccountContext);

    const [register, setRegister] = useState(); 
    const [success, setSuccess] = useState();

    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [firstName, setFirstName] = useState();
    const [lastName, setLastName] = useState();

    /*
        user register action
        username, password, firstName and lastName are requered
        error if the username already exists
        switch to login if the account was succesfully created
    */
    function RegisterAction() {
        if(username === "" || password === "" || firstName === "" || lastName === "" ||  
        username == null || password == null || firstName == null || lastName == null){
            setRegister("* fields are requerd!");
        }else {
            fetch('/user/register', {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    password: password,
                    firstName: firstName,
                    lastName: lastName
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.register !== 0){
                        setRegister("That username already exists!");
                    } else{
                        setSuccess("Successfully registered!");
                        setTimeout(() => {
                            switchToLogin();
                        }, 500);
                    };                
                });
            };
    };

    return (
        <BoxContainer>
            <FormContainer>
                <Input type="username" placeholder="Username *" onChange={e => {setUsername(e.target.value); setRegister("")}} />
                <Input type="password" placeholder="Password *" onChange={e => {setPassword(e.target.value); setRegister("")}} />
                <Input type="firstName" placeholder="First Name *" onChange={e => {setFirstName(e.target.value); setRegister("")}} />
                <Input type="lastName" placeholder="Last Name *" onChange={e => {setLastName(e.target.value); setRegister("")}} />
            </FormContainer>
            <Marginer direction="vertical" margin={12} />
            <ErrorMessage>{register}</ErrorMessage>
            <SuccessMessage>{success}</SuccessMessage>
            <Marginer direction="vertical" margin={25} />
            <ButtonLink to="#" type="submit" onClick={RegisterAction}>Register</ButtonLink>
            <Marginer direction="vertical" margin={7} />
            <MutedMessage>Already a member yet?
                <BoldLink to="#" onClick={switchToLogin}>Login now</BoldLink>
            </MutedMessage>
        </BoxContainer>       
    )
}

export default RegisterForm;