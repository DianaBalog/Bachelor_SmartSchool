import { React, useState } from 'react';
import { AccountContext } from './AccountContext';
import { LoginForm } from './LoginForm';
import { BackDrop, BoxContainer, HeaderContainer, HeaderText, TopContainer, SmallText, InnerContainer, BackDropVariants, ExpandingTransition } from './RegisterAndLoginElements';
import { RegisterForm } from './RegisterForm';


const RegisterAndLogin = () => {
    const[isExpanded, setExpanded] = useState(false);
    const[active, setActive] = useState("login");

    // animation between register and login
    const playTransitionAnimation = () => {
        setExpanded(true);
        setTimeout(() => {
            setExpanded(false);
        }, ExpandingTransition.duration * 1000 - 1500);
    };

    // change to register
    const switchToRegister = () => {
        playTransitionAnimation();
        setTimeout(() => {
            setActive("register");
        }, 400);
    };

    // change to login
    const switchToLogin = () => {
        playTransitionAnimation();
        setTimeout(() => {
            setActive("login");
        }, 400);
    };

    // change between register and login
    const contextValue = { switchToRegister, switchToLogin };

    return (
        <AccountContext.Provider value={contextValue}>
            <BoxContainer>
                <TopContainer>
                    <BackDrop initial={false} 
                        animate={isExpanded ? "expanded" : "collapsed"} 
                        variants={BackDropVariants} 
                        transition={ExpandingTransition}/>
                    {active === "login" &&
                    <HeaderContainer>
                        <HeaderText>Welcome</HeaderText>
                        <HeaderText>Back</HeaderText>
                        <SmallText>Please login to continue!</SmallText>
                    </HeaderContainer>}
                    {active === "register" &&
                    <HeaderContainer>
                        <HeaderText>Welcome</HeaderText>
                        <HeaderText>New user</HeaderText>
                        <SmallText>Join our comunity today!</SmallText>
                    </HeaderContainer>}
                </TopContainer>
                <InnerContainer>
                    {active === "login" && <LoginForm />}
                    {active === "register" && <RegisterForm />} 
                </InnerContainer>
            </BoxContainer>
        </AccountContext.Provider>
    )
}

export default RegisterAndLogin;
