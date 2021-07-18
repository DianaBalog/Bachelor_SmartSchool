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
import ArrowForwardIcon from '@material-ui/icons/ArrowForward';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import IconButton from '@material-ui/core/IconButton';
import { BoxContainer, ButtonBlue, ElementsContainer } from '../User/UserElements';
import { ErrorMessage, FormContainer, Input } from '../RegisterAndLogin/Common';
import { DetailsContainer, DetailsContainerStart } from '../ParticipantsInstitution/ParticipantsInstitutionElements';
import { Tooltip } from '@material-ui/core';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import { Redirect } from 'react-router-dom';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const ParticipantsSubject = ({id}) => {
    const cookies = new Cookies();
    const [error, setError] = useState("")
    const [username, setUsername] = useState("");
    const[info, setInfo] = useState({subject: "", usersList: [], teachersList: [], role: "", isIn: true})
    const [open, setOpen] = useState(false);

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpen(false);
    };


    useEffect(() => {
        fetch('/institution/participantsSubjectInfo', {
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
                    setInfo({...info, subject: data.subject, usersList: data.users, teachersList: data.teachers, role: data.role, isIn: data.isIn})
                };               
            });
            // eslint-disable-next-line react-hooks/exhaustive-deps
        }, []);

    function AddUser() {
        if(username === "" || username == null){
            setError("Username can't be empty!");
        } else {
            fetch('/institution/addUserToSubject', {
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
                        setInfo({...info, usersList: data.users, teachersList: data.teachers});
                        setUsername("");
                    }
                    else{
                        setError(data.ok);
                    }
                });
        }
    }

    function AddTeacher() {
        if(username === "" || username == null){
            setError("Username can't be empty!");
        } else {
            fetch('/institution/addTeacherToSubject', {
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
                        setInfo({...info, usersList: data.users, teachersList: data.teachers});
                        setUsername("");
                    }
                    else{
                        setError(data.ok);
                    }
                });
        }
    }

    function RemoveUser(selectedUsername) {
        fetch('/institution/removeUserFromSubject', {
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
                    setInfo({...info, usersList: data.users, teachersList: data.teachers});
                }
                else{
                    setOpen(true);
                }
            });
    }

    function MakeTeacher(selectedUsername){
        fetch('/institution/makeTeacherSubject', {
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
                    setInfo({...info, usersList: data.users, teachersList: data.teachers});
                }
                else{
                    setOpen(true);
                }
            });
    }

    function MakeUser(selectedUsername){
        fetch('/institution/makeUserSubject', {
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
                    setInfo({...info, usersList: data.users, teachersList: data.teachers});
                }
                else{
                    setOpen(true);
                }
            });
    }

    if(!info.isIn){
        return <Redirect to="/"/>;
    }

    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/subject/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={info.subject}>
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <InstitutionsTitle style={{alignSelf: "center"}}>{info.subject} - Participants</InstitutionsTitle>
            <br/>
            <BoxContainer style={{width: '50%', minHeight: 500, alignSelf: "center"}}>
                {info.role === "teacher" && <DetailsContainer>
                    <ElementsContainer>
                        <FormContainer style={{width: '60%'}}>
                            <Input type="username" placeholder="Username" value={username} onChange={e => {setUsername(e.target.value); setError("")}}/>
                        </FormContainer>
                        <br/>
                        <ErrorMessage>{error}</ErrorMessage>
                    </ElementsContainer>
                    <ElementsContainer>
                        <br/><br/>
                        <DetailsContainer>
                        <ElementsContainer><ButtonBlue to="#" onClick={AddUser}>Add new user</ButtonBlue></ElementsContainer>
                        <ElementsContainer><ButtonBlue to="#" onClick={AddTeacher}>Add new teacher</ButtonBlue></ElementsContainer>
                        </DetailsContainer>
                    </ElementsContainer>
                </DetailsContainer>}
                <br/>
                <DetailsContainerStart>
                    <ElementsContainer>
                        <h4 style={{color:"#4d96b8"}}>Users</h4>
                        <List style={{ overflow: 'auto', maxHeight: 300,  width: '100%', maxWidth: 360 }}>
                            {info.usersList.map(item => {
                                return (
                                    <ListItem key={item.name}>
                                        <ListItemAvatar>
                                            <Avatar src={item.image}/>
                                        </ListItemAvatar>
                                        <ListItemText
                                            primary={item.name}
                                        />
                                        {info.role === "teacher" && <ListItemSecondaryAction>
                                            <Tooltip title="Delete">
                                                <IconButton edge="end" aria-label="delete" onClick={() => RemoveUser(item.name)}>
                                                    <DeleteIcon />
                                                </IconButton>
                                            </Tooltip>
                                            <Tooltip title="Make Teacher">
                                                <IconButton edge="end" aria-label="teacher" onClick={() => MakeTeacher(item.name)}>
                                                    <ArrowForwardIcon />
                                                </IconButton>
                                            </Tooltip>
                                        </ListItemSecondaryAction>}
                                    </ListItem>
                                )
                            })}
                        </List>
                    </ElementsContainer>
                    <ElementsContainer>
                        <h4 style={{color:"#4d96b8"}}>Teachers</h4>
                        <List style={{ overflow: 'auto', maxHeight: 300,  width: '100%', maxWidth: 360 }}>
                            {info.teachersList.map(item => {
                                return (
                                    <ListItem key={item.name}>
                                        <ListItemAvatar>
                                            <Avatar src={item.image}/>
                                        </ListItemAvatar>
                                        <ListItemText
                                            primary={item.name}
                                        />
                                        {info.role === "teacher" && <ListItemSecondaryAction>
                                            <Tooltip title="Delete">
                                                <IconButton edge="end" aria-label="delete" onClick={() => RemoveUser(item.name)}>
                                                    <DeleteIcon />
                                                </IconButton>
                                            </Tooltip>
                                            <Tooltip title="Make user">
                                                <IconButton edge="end" aria-label="user" onClick={() => MakeUser(item.name)}>
                                                    <ArrowBackIcon />
                                                </IconButton>
                                            </Tooltip>
                                        </ListItemSecondaryAction>}
                                    </ListItem>
                                )
                            })}
                        </List>
                    </ElementsContainer>
                </DetailsContainerStart>
            </BoxContainer>    
            <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
                <Alert onClose={handleClose} severity="error">
                    You can't change yourself!
                </Alert>
            </Snackbar>
        </InstitutionsContainerNoCenter>
    )
}

export default ParticipantsSubject;