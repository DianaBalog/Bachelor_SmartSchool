import { React, useState, useEffect } from 'react';
import { InstitutionsContainerNoCenter, InstitutionsTitle } from '../Institutions/InstitutionsElements';
import Cookies from 'universal-cookie';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';
import { BoxContainer, ButtonBlue, ElementsContainer } from '../User/UserElements';
import { ErrorMessage, FormContainer, Input } from '../RegisterAndLogin/Common';
import { DetailsContainer } from './ParticipantsInstitutionElements';
import { Tooltip } from '@material-ui/core';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import { Redirect } from 'react-router-dom';

const ParticipantsInstitution = ({id}) => {
    const cookies = new Cookies();
    const [error, setError] = useState("")
    const [username, setUsername] = useState("");
    const[info, setInfo] = useState({institution: "", usersList: [], owner: "", role: "", isIn: true })


    useEffect(() => {
        fetch('/institution/participantsInfo', {
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
                if(data.ok === '0'){
                    setInfo({...info, institution: data.institution, usersList: data.users, owner: data.owner, role: data.role, isIn: data.isIn})
                };               
            });
            // eslint-disable-next-line react-hooks/exhaustive-deps  
        }, []);

    function AddUser() {
        if(username === "" || username == null){
            setError("Username can't be empty!");
        } else {
            fetch('/institution/addUserToInstitution', {
                method: 'POST',
                body: JSON.stringify({
                    id: id , username: username
                }),
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.ok === '0'){
                        setInfo({...info, usersList: data.users});
                        setUsername("");
                    }
                    else{
                        setError(data.ok);
                    }
                });
        }
    }

    function RemoveUser(selectedUsername) {
        fetch('/institution/removeUserFromInstitution', {
            method: 'POST',
            body: JSON.stringify({
                id: id , username: selectedUsername
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setInfo({...info, usersList: data.users});
                }
            });
    }

    if(!info.isIn){
        return <Redirect to="/"/>;
    }

    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/institution/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={info.institution}>
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <InstitutionsTitle style={{alignSelf: "center"}}>{info.institution} - Participants</InstitutionsTitle>
            <br/>
            <BoxContainer style={{width: '50%', minHeight: 500, alignSelf: "center"}}>
                <br/>
                <h4 style={{color:"#4d96b8"}}>Owner: <b>{info.owner.name}</b></h4>
                {info.role === "owner" && <DetailsContainer>
                    <ElementsContainer>
                        <FormContainer style={{width: '60%'}}>
                            <Input type="username" placeholder="Username" value={username} onChange={e => {setUsername(e.target.value); setError("")}}/>
                        </FormContainer>
                        <br/>
                        <ErrorMessage>{error}</ErrorMessage>
                    </ElementsContainer>
                    <ElementsContainer>
                        <br/><br/>
                        <ButtonBlue to="#" onClick={AddUser}>Add new user</ButtonBlue>
                    </ElementsContainer>
                </DetailsContainer> }

                <List style={{ overflow: 'auto', maxHeight: 300,  width: '100%', maxWidth: 360 }}>
                    <ListItem>
                        <ListItemAvatar>
                            <Avatar src={info.owner.image}/>
                        </ListItemAvatar>
                        <ListItemText
                            primary={info.owner.name}
                        />
                    </ListItem>
                    {info.usersList.map(item => {
                        return (
                            <ListItem key={item.name}>
                                <ListItemAvatar>
                                    <Avatar src={item.image}/>
                                </ListItemAvatar>
                                <ListItemText
                                    primary={item.name}
                                />
                                {info.role === "owner" && <ListItemSecondaryAction>
                                    <Tooltip title="Delete">
                                        <IconButton edge="end" aria-label="delete" onClick={() => RemoveUser(item.name)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </Tooltip>
                                </ListItemSecondaryAction>}
                            </ListItem>
                        )
                    })}
                 </List>
            </BoxContainer>    
        </InstitutionsContainerNoCenter>
    )
}

export default ParticipantsInstitution;