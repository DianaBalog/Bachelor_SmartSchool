import { React, useState, useEffect } from 'react';
import { InstitutionsTitle, InstitutionsContainerNoCenter } from '../Institutions/InstitutionsElements';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import Cookies from 'universal-cookie';
import IconButton from '@material-ui/core/IconButton';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import TextField from "@material-ui/core/TextField";
import { BoxContainer, MessageContainer, MessagesBox } from '../Subject/SubjectElements';
import SendIcon from '@material-ui/icons/Send';
import { ButtonBlue } from '../User/UserElements';
import Avatar from '@material-ui/core/Avatar';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import HighlightOffIcon from '@material-ui/icons/HighlightOff';
import { Pagination } from '@material-ui/lab';
import { makeStyles } from "@material-ui/core";
import Modal from "@material-ui/core/Modal";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";
import { Redirect } from 'react-router-dom';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';

const Post = ({id}) => {
    const cookies = new Cookies();
    const [post, setPost] = useState({pages: null, currentPage: 1, title: "", idSubject: "", subject: "", role: "", message: "", messagesList: [], isIn: true})
    const [message, setMessage] = useState("");
    const [deleted, setDeleted] = useState(false)
    const [idDeleteMessage, setIdDeleteMessage] = useState("")


    useEffect(() => {
        fetch('/institution/getPostInfo', {
            method: 'POST',
            body: JSON.stringify({
                id: id, pageNumber: post.currentPage
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setPost({...post, title: data.title, idSubject: data.idSubject, subject: data.subject, role: data.role, 
                        message: data.hasMessages, messagesList: data.messagesList, pages: data.pages, isIn: data.isIn})
                };               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    function getData(value){
        fetch('/institution/getPostInfo', {
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
                    setPost({...post, title: data.title, idSubject: data.idSubject, subject: data.subject, role: data.role, 
                        message: data.hasMessages, messagesList: data.messagesList, pages: data.pages, currentPage: value, isIn: data.isIn})
                };               
            });
    }

    function SendMessage() {
        if(message !== "" && message != null){
            fetch('/institution/sendMessage', {
                method: 'POST',
                body: JSON.stringify({
                    id: id, message: message, pageNumber: post.currentPage
                }),
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.ok === '0'){
                        setPost({...post, messagesList: data.messagesList, pages: data.pages, currentPage: data.pages})
                    };   
                    setMessage("")            
                });
        }
    }

    function RefreshMessages() {
        fetch('/institution/refreshMessages', {
            method: 'POST',
            body: JSON.stringify({
                id: id, pageNumber: post.currentPage
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setPost({...post, messagesList: data.messagesList, pages: data.pages})
                };               
            });
    }

    function DeleteMessage(idMessage) {
        fetch('/institution/deleteMessage', {
            method: 'DELETE',
            body: JSON.stringify({
                id: id, idMessage: idMessage, pageNumber: post.currentPage
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.delete === '0'){
                    setPost({...post, messagesList: data.messagesList, pages: data.pages})
                    setOpen(false);
                }else{
                    setOpen(false);
                }               
            });
    }

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

    const useStylesModal = makeStyles((theme) => ({
        modal: {
          display: "flex",
          alignItems: "center",
          justifyContent: "center"
        },
        paper: {
          backgroundColor: theme.palette.background.paper,
          border: "0.5px solid #000",
          boxShadow: theme.shadows[5],
          padding: theme.spacing(2, 4, 3)
        }
    }));

    const classesModal = useStylesModal();
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const [openPost, setOpenPost] = useState(false);

    const handleOpenPost = () => {
        setOpenPost(true);
    };

    const handleClosePost = () => {
        setOpenPost(false);
    };

    function DeletePost(){
        fetch('/institution/deletePost', {
            method: 'DELETE',
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
                    setDeleted(true);
                }   
            });
    }

    if(!post.isIn){
        return <Redirect to="/"/>;
    }

    if(deleted){
        return <Redirect to={"/subject/" + post.idSubject}/>;
    }

    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/subject/" + post.idSubject} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={post.subject} >
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <InstitutionsTitle style={{alignSelf: "center"}}>{post.title}</InstitutionsTitle>  
            
            {!post.message && post.role === "user" && <ButtonBlue style={{ alignSelf: "center"}} onClick={RefreshMessages}>Refresh for new messages</ButtonBlue>}
            
            {((post.role === "teacher" && !post.message) || post.message) && 
            <BoxContainer style={{ alignSelf: "center"}}>
                {post.role === "teacher" && <><br/><DeleteForeverIcon fontSize="large" style={{fill: "#4d96b8", cursor: "pointer", alignSelf: "center"}} onClick={handleOpenPost} /></>}
                <Modal  
                    className={classesModal.modal}
                    open={openPost}
                    onClose={handleClosePost}
                    closeAfterTransition
                    BackdropComponent={Backdrop}
                    BackdropProps={{
                    timeout: 500
                    }}
                >
                    <Fade in={openPost}>
                        <div className={classesModal.paper}>
                            <br/><br/>
                            <h2>Are you sure you want to delete this post?</h2>
                            <br/>
                            <h2 style={{color:"#4d96b8"}}>{post.title}</h2>
                            <br/><br/>
                            <p>This action can't be undone!</p>
                            <br/><br/>
                            <ButtonBlue to="#" onClick={DeletePost} style={{justifyContent:"center"}}>Delete</ButtonBlue>
                        </div>
                    </Fade>
                </Modal>
            <ButtonBlue to="#" style={{ alignSelf: "center", marginTop: "15px"}} onClick={RefreshMessages}>Refresh for new messages</ButtonBlue>
            <div style={{flexDirection:'row'}}>
                <TextField
                    id="outlined-multiline-static"
                    label="Send Message"
                    multiline
                    rows={3}
                    variant="outlined"
                    style={{width: "70%", justifyContent: "flex-start", marginLeft: "80px", marginBottom: "15px"}}
                    value={message} onChange={e => {setMessage(e.target.value)}}
                />  
                <Tooltip title="Send">
                    <IconButton type="submit" aria-label="search" style={{ marginLeft: "50px", marginTop: "20px"}} onClick={SendMessage}>
                        <SendIcon style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </div>
            </BoxContainer>}
            <br/><br/>
            <MessagesBox style={{alignSelf: "center"}}>
                {post.messagesList.map(item => {
                    if(item.currentUser){
                        return (
                            <MessageContainer style={{alignSelf: "center", backgroundColor: "#4d96b8"}} key={item.idMessage}>
                                <div style={{ display: "grid",  gridTemplateColumns: "1fr 1fr", alignSelf: "flex-start"}}>        
                                    <Tooltip title={item.username}>
                                        <Avatar style={{ marginLeft: "15px", marginTop: "5px", marginRight: "10px"}} src={item.icon}/>
                                    </Tooltip>
                                    <h4 style={{ marginTop: "15px"}}>{item.name}</h4>
                                </div>
                                <p style={{ marginLeft: "20px", marginRight: "20px", alignSelf: "center", marginTop: "5px" }}>{item.text}</p>
                                <div style={{ display: "grid",  gridTemplateColumns: "1fr 1fr", alignSelf: "flex-end", marginBottom: "5px"}}>
                                    <Tooltip title="Delete">
                                        <HighlightOffIcon fontSize="small" style={{ marginRight: "10px"}} onClick={() => {setIdDeleteMessage(item.idMessage); handleOpen();}}/>
                                    </Tooltip>
                                    <Tooltip title={item.date}>
                                        <AccessTimeIcon fontSize="small" style={{ marginRight: "10px"}}/>
                                    </Tooltip>
                                </div>
                            </MessageContainer> 
                            ) 
                    } else {
                        return (
                            <MessageContainer style={{alignSelf: "center", backgroundColor: "white"}} key={item.idMessage}>
                                <div style={{ display: "grid",  gridTemplateColumns: "1fr 1fr", alignSelf: "flex-start"}}>
                                    <Tooltip title={item.username}> 
                                        <Avatar style={{ marginRight: "15px", marginTop: "5px", marginLeft: "10px"}} src={item.icon}/>
                                    </Tooltip>
                                    <h4 style={{ marginTop: "15px"}}>{item.name}</h4>
                                </div>
                                <p style={{ marginLeft: "20px", marginRight: "20px", marginTop: "3px", alignSelf: "center" }}>{item.text}</p>
                                <Tooltip title={item.date}>
                                    <AccessTimeIcon fontSize="small" style={{alignSelf: "flex-end", marginRight: "10px", marginBottom: "5px"}}/>
                                </Tooltip>
                            </MessageContainer>
                            ) 
                    }
                })}
            </MessagesBox>
            <Modal  
                className={classesModal.modal}
                open={open}
                onClose={handleClose}
                closeAfterTransition
                BackdropComponent={Backdrop}
                BackdropProps={{
                timeout: 500
                }}
            >
                <Fade in={open}>
                    <div className={classesModal.paper}>
                    <br/><br/>
                    <h2>Are you sure you want to delete this message?</h2>
                    <br/><br/>
                    <p>This action can't be undone!</p>
                    <br/><br/>
                    <ButtonBlue to="#" onClick={() => DeleteMessage(idDeleteMessage)} style={{justifyContent:"center"}}>Delete</ButtonBlue>
                    </div>
                </Fade>
            </Modal>
            <br/>
            <Pagination style={{alignSelf: "center"}} count={post.pages} defaultPage={post.currentPage} page={post.currentPage} color="primary" classes={{ ul: classes.ul }} onChange={handleChange}/>
            <br/>
        </InstitutionsContainerNoCenter>
    )
}

export default Post;