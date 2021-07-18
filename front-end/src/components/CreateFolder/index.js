import { React, useState, useEffect } from 'react';
import { InstitutionsTitle, InstitutionsContainerNoCenter } from '../Institutions/InstitutionsElements';
import Cookies from 'universal-cookie';
import 'react-circular-progressbar/dist/styles.css';
import { BoxContainer, ButtonBlue } from '../User/UserElements';
import { FormContainer, Input } from '../RegisterAndLogin/Common';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import { Tooltip } from '@material-ui/core';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import IconButton from '@material-ui/core/IconButton';
import { Redirect } from 'react-router';


function Alert(props) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const CreateFolder = ({id}) => {
    const cookies = new Cookies();

    const [folderName, setFolderName] = useState("");
    const [openError, setOpenError] = useState(false);
    const [openSuccess, setOpenSuccess] = useState(false);
    const [canCreate, setCanCreate] = useState(true)

    const handleCloseError = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }

        setOpenError(false);
    };

    const handleCloseSuccess = (event, reason) => {
        if (reason === 'clickaway') {
        return;
        }
        setOpenSuccess(false);
    };

    useEffect(() => {  
        fetch('/institution/userInSubject', {
            method: 'POST',
            body: JSON.stringify({
                id: id, subject: true
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

    function CreateFolder() {
        if(folderName === "" || folderName == null){
            setOpenError(true);
        }else {
            fetch('/institution/createSubjectFolder', {
                method: 'POST',
                body: JSON.stringify({
                    id: id, name: folderName
                }),
                credentials: 'same-origin',
                headers: {
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token'),
                    'Content-Type': 'application/json'
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.ok === '0'){
                        setOpenSuccess(true);
                        setFolderName("");
                    }                
                });
            };
    }

    if(!canCreate){
        return <Redirect to="/"/>;
    }
    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/subjectFiles/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title="Files">
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>

            <InstitutionsTitle style={{alignSelf: "center", marginTop: "10px"}}>Create folder</InstitutionsTitle>
           

            <BoxContainer style={{alignSelf: "center"}}>

                <br/><br/>
                <FormContainer style={{width: "50%"}}>
                    <Input type="text" placeholder="Folder Name" value={folderName} onChange={e => {setFolderName(e.target.value)}}/>
                </FormContainer>
                <br/>
                
               <ButtonBlue to="#" onClick={CreateFolder}>Create</ButtonBlue>
            </BoxContainer>
            <Snackbar open={openError} autoHideDuration={6000} onClose={handleCloseError}>
                <Alert onClose={handleCloseError} severity="error">
                    Folder name can't be empty!
                </Alert>
            </Snackbar>
            <Snackbar open={openSuccess} autoHideDuration={6000} onClose={handleCloseSuccess}>
                <Alert onClose={handleCloseSuccess} severity="success">
                    Successfully created!
                </Alert>
            </Snackbar>
        </InstitutionsContainerNoCenter>
    )
}

export default CreateFolder;
