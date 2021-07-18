import { React, useState, useEffect} from 'react';
import { BoxContainer, HeaderContainer, HeaderText, InnerContainer } from '../RegisterAndLogin/RegisterAndLoginElements';
import { FormContainer, Input, ErrorMessage, SuccessMessage } from '../RegisterAndLogin/Common';
import { ButtonLink, BackDrop, AppContainer, TopContainer } from '../CreateInstitution/CreateInstitutionElements';
import { Marginer } from '../marginer';
import Cookies from 'universal-cookie';
import { Redirect } from 'react-router';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { withStyles } from '@material-ui/core/styles';
import Switch from '@material-ui/core/Switch';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import { ButtonWrapper } from '../Institution/InstitutionElements';


const CreateSubject = ({id}) => {
    const cookies = new Cookies();
    const [create, setCreate] = useState(); 
    const [success, setSuccess] = useState();
    const [subject, setSubject] = useState(false)
    const [canCreate, setCanCreate] = useState(true)

    const [name, setName] = useState();

    const [state, setState] = useState({publicSubject: false, message: false});
    
    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };

    useEffect(() => {  
        fetch('/institution/canCreateSubject', {
            method: 'POST',
            body: JSON.stringify({
                id: id
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                setCanCreate(data.ok)            
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps    
    }, []); 

    function CreateAction() {
        if(name === "" || name == null){
            setCreate("* fields are required!");
        }else {
            fetch('/institution/createSubject', {
                method: 'POST',
                body: JSON.stringify({
                    institution: id, name: name, public: state.publicSubject, message: state.message
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token'),
                    'Content-Type': 'application/json'
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.createSubject !== '0'){
                        setCreate("An unexpected error occurred!");
                    } else{
                        setSuccess("Successfully created!");
                        setTimeout(() => {
                            setSubject(true);
                        }, 500);
                    };                
                });
            };
    };

    const CustomSwitch = withStyles({
        switchBase: {
          color: '#79a2b5',
          '&$checked': {
            color: '#4d96b8',
          },
          '&$checked + $track': {
            backgroundColor: '#4d96b8',
          },
        },
        checked: {},
        track: {},
      })(Switch);

    if(subject){
        return <Redirect to={"/institution/" + id}/>;
    }
    if(!canCreate){
        return <Redirect to="/"/>;
    }
    return (
        <AppContainer>
            <ButtonWrapper to={"/institution/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title="Institution">
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <BoxContainer style={{alignSelf: "center"}}>
                <TopContainer>
                    <BackDrop/>
                    <HeaderContainer>
                        <HeaderText>Create</HeaderText>
                        <HeaderText>Subject</HeaderText>
                    </HeaderContainer>
                </TopContainer>
                <Marginer direction="vertical" margin={50} />
                <InnerContainer>
                    <FormContainer>
                    <Input type="name" placeholder="Name *" onChange={e => {setName(e.target.value); setCreate("")}}/>
                    </FormContainer>
                    <Marginer direction="vertical" margin={20} />
                    <FormControlLabel
                        control={<CustomSwitch checked={state.publicSubject} onChange={handleChange} name="publicSubject" />}
                        label="Public"
                    />
                    <Marginer direction="vertical" margin={15} />
                    <FormControlLabel
                        control={<CustomSwitch checked={state.message} onChange={handleChange} name="message" />}
                        label="Message"
                    />
                    <Marginer direction="vertical" margin={15} />
                    <ErrorMessage>{create}</ErrorMessage>
                    <SuccessMessage>{success}</SuccessMessage>
                    <Marginer direction="vertical" margin={50} />
                    <ButtonLink to="#" type="submit" onClick={CreateAction} >Create</ButtonLink>
                </InnerContainer>
            </BoxContainer>
        </AppContainer>
    )
}

export default CreateSubject;
