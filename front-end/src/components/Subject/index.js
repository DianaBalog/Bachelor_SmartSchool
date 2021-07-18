import { React, useState, useEffect } from 'react';
import { InstitutionsTitle, ButtonLink, InstitutionsContainerNoCenter, InstitutionsWrapper, InstitutionsCard, InstitutionsDescription, InstitutionsSubtitle, StyledLink } from '../Institutions/InstitutionsElements';
import Menu from '@material-ui/core/Menu';
import { ButtonMenu } from '../Institution/InstitutionElements';
import SettingsIcon from '@material-ui/icons/Settings';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import Cookies from 'universal-cookie';
import IconButton from '@material-ui/core/IconButton';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import TextField from "@material-ui/core/TextField";
import { BoxContainer } from './SubjectElements';
import SendIcon from '@material-ui/icons/Send';
import { ButtonBlue } from '../User/UserElements';
import Avatar from '@material-ui/core/Avatar';
import { Pagination } from '@material-ui/lab';
import { makeStyles } from "@material-ui/core";
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { Redirect } from 'react-router-dom';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}


const Subject = ({id}) => {
    const cookies = new Cookies();
    const[subject, setSubject] = useState({pages: null, currentPage: 1, name: "", institution: "", institutionId:"", role: "", postList: [], isIn: true})
    const [anchorEl, setAnchorEl] = useState(null);
    const [description, setDescription] = useState("");
    const [title, setTitle] = useState("");
    const [open, setOpen] = useState(false);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleCloseError = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpen(false);
    };

    const handleChange = (event, value) => {
        getData(value)
    };

    const useStyles = makeStyles(() => ({
        ul: {
          "& .MuiPaginationItem-root": {
            color: "#fff"
          }
        }
      }));

    const classes = useStyles();

    useEffect(() => {
        fetch('/institution/subjectPageInfo', {
            method: 'POST',
            body: JSON.stringify({
                id: id, pageNumber: subject.currentPage
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setSubject({...subject, name: data.subject, institution: data.institution, 
                        institutionId: data.institutionId, role: data.role, postList: data.postList, pages: data.pages, isIn: data.isIn})
                };               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    function CreatePost() {
        if(description !== "" && description != null && title !== "" && title != null){
            fetch('/institution/createPost', {
                method: 'POST',
                body: JSON.stringify({
                    id: id, title: title, description: description, pageNumber: 1
                }),
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.ok === '0'){
                        setSubject({...subject, postList: data.postList, pages: data.pages})
                    };   
                    setDescription("")
                    setTitle("")            
                });
        }
        else{
            setOpen(true);
            setDescription("");
            setTitle("");
        }
    }

    function RefreshPosts() {
        fetch('/institution/refreshPosts', {
            method: 'POST',
            body: JSON.stringify({
                id: id, pageNumber: 1
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setSubject({...subject, postList: data.postList, pages: data.pages})
                };               
            });
    }

    function getData(value){
        fetch('/institution/subjectPageInfo', {
            method: 'POST',
            body: JSON.stringify({
                id: id, pageNumber: value
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setSubject({...subject, name: data.subject, institution: data.institution, institutionId: data.institutionId, 
                        role: data.role, postList: data.postList, pages: data.pages, isIn: data.isIn, currentPage: value})
                };               
            });
    }

    if(!subject.isIn){
        return <Redirect to="/"/>;
    }

    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/institution/" + subject.institutionId} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={subject.institution} >
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <InstitutionsTitle style={{alignSelf: "center"}}>{subject.name}</InstitutionsTitle>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <ButtonMenu to={"/editSubject/" + id}>Subject Info</ButtonMenu>
                <ButtonMenu to={"/participantsSubject/" + id}>Participants</ButtonMenu>
                <ButtonMenu to={"/subjectFiles/" + id}>Files</ButtonMenu>
            </Menu>
            <ButtonLink to="#" aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} style={{alignSelf: "center"}}><SettingsIcon/></ButtonLink>  
            
            {subject.role === "user" && <ButtonBlue to="#" style={{ alignSelf: "center"}} onClick={RefreshPosts}>Refresh for new posts</ButtonBlue>}
            
            {subject.role === "teacher" && 
            <BoxContainer style={{ alignSelf: "center"}}>
            <ButtonBlue to="#" style={{ alignSelf: "center", marginTop: "15px"}} onClick={RefreshPosts}>Refresh for new posts</ButtonBlue>
            <TextField
                    id="outlined-multiline-static1"
                    label="Title"
                    variant="outlined"
                    style={{width: "70%", justifyContent: "flex-start", marginLeft: "80px", marginBottom: "15px"}}
                    value={title} onChange={e => {setTitle(e.target.value)}}
                />  
            <div style={{flexDirection:'row'}}>
                <TextField
                    id="outlined-multiline-static"
                    label="Short Description"
                    multiline
                    rows={2}
                    variant="outlined"
                    style={{width: "70%", justifyContent: "flex-start", marginLeft: "80px", marginBottom: "15px"}}
                    value={description} onChange={e => {setDescription(e.target.value)}}
                />  
                <Tooltip title="Post">
                    <IconButton type="submit" aria-label="search" style={{ marginLeft: "50px", marginTop: "20px"}} onClick={CreatePost}>
                        <SendIcon style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </div>
            </BoxContainer>}
            <br/><br/>
            <InstitutionsWrapper style={{alignSelf: "center"}}>
            {subject.postList.map(item => {
                return (
                       <StyledLink to={"/post/" + item.idPost} key={item.idPost}>
                            <InstitutionsCard id={item.idPost}>
                                <InstitutionsSubtitle style={{ color:"#4d96b8"}}>{item.title}</InstitutionsSubtitle>
                                <InstitutionsDescription>{item.description}</InstitutionsDescription>
                                <br/><br/>
                                <h4 style={{ marginTop: "15px", color:"grey"}}>{item.name}</h4>
                                <Tooltip title={item.username}>
                                    <Avatar style={{ flex: "flex-end"}} src={item.icon}/>
                                </Tooltip>
                                <br/>
                                <InstitutionsDescription style={{ color:"grey"}}>{item.date}</InstitutionsDescription>
                            </InstitutionsCard>
                       </StyledLink>)
            })}
            </InstitutionsWrapper>
            <br/>
            <Pagination style={{alignSelf: "center"}} count={subject.pages} defaultPage={subject.currentPage} page={subject.currentPage} color="primary" classes={{ ul: classes.ul }} onChange={handleChange}/>
            <br/>
            <Snackbar open={open} autoHideDuration={6000} onClose={handleCloseError}>
                <Alert onClose={handleCloseError} severity="error">
                    A post needs a title and a short description!
                </Alert>
            </Snackbar>
        </InstitutionsContainerNoCenter>
    )
}

export default Subject;