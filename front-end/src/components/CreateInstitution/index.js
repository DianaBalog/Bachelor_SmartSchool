import { React, useState } from 'react';
import { BoxContainer, HeaderContainer, HeaderText, InnerContainer } from '../RegisterAndLogin/RegisterAndLoginElements';
import { FormContainer, Input, ErrorMessage, SuccessMessage } from '../RegisterAndLogin/Common';
import { ButtonLink, BackDrop, AppContainer, TopContainer } from './CreateInstitutionElements';
import { Marginer } from '../marginer';
import Cookies from 'universal-cookie';
import { Redirect } from 'react-router';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';


const CreateInstitution = () => {
    const cookies = new Cookies();
    const [create, setCreate] = useState(); 
    const [success, setSuccess] = useState();
    const [institution, setInstitution] = useState(false)

    const [name, setName] = useState();
    const [country, setCountry] = useState();
    const [region, setRegion] = useState();
    const [city, setCity] = useState();
    const [street, setStreet] = useState();
    const [number, setNumber] = useState();

    function CreateAction() {
        if(name === "" || name == null || country === "" || country == null || region === "" || region == null || city === "" || city == null || street === "" || street == null || number === "" || number == null){
            setCreate("* fields are required!");
        }else {
            fetch('/institution/create', {
                method: 'POST',
                body: JSON.stringify({
                    name: name, country: country, region: region, city: city, street: street, number: number
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token'),
                    'Content-Type': 'application/json'
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.create !== '0'){
                        setCreate("An unexpected error occurred!");
                    } else{
                        setSuccess("Successfully created!");
                        setTimeout(() => {
                            setInstitution(true);
                        }, 500);
                    };                
                });
            };
    };


    if(institution){
        return <Redirect to="/institutions"/>;
    }
    return (
        <AppContainer>
            <ButtonWrapper to="/institutions" style={{justifyContent: "flex-start", paddingLeft: "20px"}} >
                    <Tooltip title="Institutions">
                        <IconButton edge="end" aria-label="user" >
                            <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                        </IconButton>
                    </Tooltip>
            </ButtonWrapper>
            <BoxContainer style={{alignSelf: "center"}}>
                <TopContainer>
                    <BackDrop/>
                    <HeaderContainer>
                        <HeaderText>Create Institution</HeaderText>
                    </HeaderContainer>
                </TopContainer>
                <InnerContainer>
                    <FormContainer>
                    <Input type="name" placeholder="Name *" onChange={e => {setName(e.target.value); setCreate("")}}/>
                    <Input type="country" placeholder="Country *" onChange={e => {setCountry(e.target.value); setCreate("")}}/>
                    <Input type="region" placeholder="Region *" onChange={e => {setRegion(e.target.value); setCreate("")}}/>
                    <Input type="city" placeholder="City *" onChange={e => {setCity(e.target.value); setCreate("")}}/>
                    <Input type="street" placeholder="Street *" onChange={e => {setStreet(e.target.value); setCreate("")}}/>
                    <Input type="addressnumber" placeholder="Number *" onChange={e => {setNumber(e.target.value); setCreate("")}}/>
                    </FormContainer>
                    <Marginer direction="vertical" margin={10} />
                    <ErrorMessage>{create}</ErrorMessage>
                    <SuccessMessage>{success}</SuccessMessage>
                    <Marginer direction="vertical" margin={15} />
                    <ButtonLink to="#" type="submit" onClick={CreateAction} >Create</ButtonLink>
                </InnerContainer>
            </BoxContainer>
        </AppContainer>
    )
}

export default CreateInstitution;
