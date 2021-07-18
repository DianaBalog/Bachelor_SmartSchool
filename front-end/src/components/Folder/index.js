import { React, useState, useEffect } from 'react';
import { InstitutionsTitle, ButtonLink, InstitutionsContainerNoCenter } from '../Institutions/InstitutionsElements';
import Menu from '@material-ui/core/Menu';
import { ButtonMenu } from '../Institution/InstitutionElements';
import SettingsIcon from '@material-ui/icons/Settings';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import Cookies from 'universal-cookie';
import IconButton from '@material-ui/core/IconButton';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import { BoxContainer } from '../User/UserElements';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import InsertDriveFileIcon from '@material-ui/icons/InsertDriveFile';
import AccessTimeIcon from '@material-ui/icons/AccessTime';
import { Link } from "react-router-dom";
import LinkIcon from '@material-ui/icons/Link';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { Redirect } from 'react-router';
import { ButtonBlue } from '../User/UserElements';
import { makeStyles } from "@material-ui/core";
import Modal from "@material-ui/core/Modal";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";
import HighlightOffIcon from '@material-ui/icons/HighlightOff';

function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const Folder = ({id}) => {
    const cookies = new Cookies();
    const[folder, setFolder] = useState({name: "", subjectName: "", subjectId:"", role: "", filesList: [], isIn: true})
    const [anchorEl, setAnchorEl] = useState(null);
    const [fileIdDelete, setFileIdDelete] = useState("");

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };
    
    useEffect(() => {
        fetch('/institution/folderPageInfo', {
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
                    setFolder({...folder, name: data.name, role: data.role, filesList: data.filesList, subjectName: data.subjectName, 
                        subjectId: data.subjectId, isIn: data.isIn})
                };               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const [openSuccess, setOpenSuccess] = useState(false);
    const handleCloseSuccess = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpenSuccess(false);
    };

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
    const [openDeleteFile, setOpenDeleteFile] = useState(false);

    const handleOpenDeleteFile = () => {
        setOpenDeleteFile(true);
    };

    const handleCloseDeleteFile = () => {
        setOpenDeleteFile(false);
    };

    function DeleteFile(id){
        fetch('/institution/deleteFolderFile', {
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
                    setFolder({...folder, filesList: data.filesList});
                    handleCloseDeleteFile();
                }   
            });
    }
    
    if(!folder.isIn){
        return <Redirect to="/"/>;
    }

    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/subjectFiles/" + folder.subjectId} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={folder.subjectName + " Files"}>
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <InstitutionsTitle style={{alignSelf: "center"}}>{folder.name} Files</InstitutionsTitle>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <ButtonMenu to={"/uploadFolderFiles/" + id}>Upload File</ButtonMenu>
            </Menu>
            <ButtonLink to="#" aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} style={{alignSelf: "center"}}><SettingsIcon/></ButtonLink>  
            
            <BoxContainer style={{alignSelf: "center", minHeight: "60%"}}>
                <br/>
                <List style={{ overflow: 'auto', maxHeight: 350,  width: '80%' }}>
                    {folder.filesList.map(item => {
                        return (
                        <ListItem button component={Link} to={{ pathname: process.env.REACT_APP_BACK + "institution/downloadFile/" + item.file }} target="_blank" key={item.file}>
                            <ListItemAvatar>
                                <Tooltip title={"Uploaded by: " + item.username}>
                                    <InsertDriveFileIcon style={{fill: "#4d96b8"}} fontSize="large"/>
                                </Tooltip>
                            </ListItemAvatar>
                            <ListItemText
                                primary={item.name}
                            />
                            <ListItemSecondaryAction>
                                <Tooltip title="Copy download link">
                                    <LinkIcon style={{fill: "#4d96b8", cursor: "pointer"}} fontSize="large" onClick={() => {navigator.clipboard.writeText(process.env.REACT_APP_FRONT + "download/" + item.name + "&" + item.file); setOpenSuccess(true)}}/>
                                </Tooltip>
                                <Tooltip title={item.date}>
                                    <AccessTimeIcon style={{fill: "#4d96b8", marginLeft:"10px", marginRight:"10px"}} fontSize="large"/>
                                </Tooltip>
                                <Tooltip title="Delete">
                                    <HighlightOffIcon fontSize="large" style={{fill: "#4d96b8", cursor: "pointer"}} onClick={() => {setFileIdDelete(item.idFile); handleOpenDeleteFile()}}/>
                                </Tooltip>
                            </ListItemSecondaryAction>
                        </ListItem>)})}
                </List>
                <br/>
            </BoxContainer>
            <Snackbar open={openSuccess} autoHideDuration={6000} onClose={handleCloseSuccess}>
                <Alert onClose={handleCloseSuccess} severity="success">
                    Copied to clipboard!
                </Alert>
            </Snackbar>
            <Modal  
                className={classesModal.modal}
                open={openDeleteFile}
                onClose={handleCloseDeleteFile}
                closeAfterTransition
                BackdropComponent={Backdrop}
                BackdropProps={{
                timeout: 500
                }}
            >
                <Fade in={openDeleteFile}>
                    <div className={classesModal.paper}>
                    <br/><br/>
                    <h2>Are you sure you want to delete this file?</h2>
                    <br/><br/>
                    <p>This action can't be undone!</p>
                    <br/><br/>
                    <ButtonBlue to="#" onClick={() => DeleteFile(fileIdDelete)} style={{justifyContent:"center"}}>Delete</ButtonBlue>
                    </div>
                </Fade>
            </Modal>            
        </InstitutionsContainerNoCenter>
    )
}

export default Folder;