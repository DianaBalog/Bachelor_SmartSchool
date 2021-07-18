import { React, useState, useRef, useEffect } from 'react';
import { InstitutionsTitle, InstitutionsContainerNoCenter } from '../Institutions/InstitutionsElements';
import Cookies from 'universal-cookie';
import 'react-circular-progressbar/dist/styles.css';
import { BoxContainer, ButtonBlue } from '../User/UserElements';
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

const UploadFolderFiles = ({id}) => {
    const cookies = new Cookies();
    const fileInput = useRef(null)
    const [fileName, SetFileName] = useState("No file selected")
    const [singleFile, setSingleFile] = useState(false);
    const [openSuccess, setOpenSuccess] = useState(false);
    const [canCreate, setCanCreate] = useState(true)

    function HandleSingleFileClick() {
        if(singleFile){
            setSingleFile(false)
        } else{
            fileInput.current.click()
            setSingleFile(true)
        }
    }

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
                id: id, subject: false
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

    function SaveFolderFile() {
            if(fileInput.current.files.length !== 0){   
                let formData = new FormData()
                formData.append('id', id) 
                formData.append('files', fileInput.current.files[0])         
                fetch('/institution/saveFolderFile', {
                    method: 'POST',
                    body: formData,
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                    }
                }).then(response =>
                    response.json()).then((data) => {
                        if(data.ok === '0'){
                            HandleSingleFileClick();
                            SetFileName("No file selected");
                            setOpenSuccess(true);
                        };               
                    });
            } else{
                HandleSingleFileClick();
            }
    }

    if(!canCreate){
        return <Redirect to="/"/>;
    }
    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/folder/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title="Folder">
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>

            <InstitutionsTitle style={{alignSelf: "center", marginTop: "10px"}}>Upload Files</InstitutionsTitle>
           
            <BoxContainer style={{alignSelf: "center"}}>
                <br/>
                <h2 style={{color: "#4d96b8"}}>Add file in folder</h2>
                <br/>
                <h4>{fileName}</h4>
                {singleFile === false && <ButtonBlue to="#" onClick={HandleSingleFileClick}>Select File</ButtonBlue>}
                {singleFile === true && <ButtonBlue to="#" onClick={SaveFolderFile}>Upload File</ButtonBlue>}
                
                    <input onChange={e => {SetFileName(e.target.value)}}
                        accept="image/* audio/* video/* .png .xml .ppt"
                        id="file"
                        type="file"
                        ref={fileInput}
                        style={{display: "none"}}
                    />
            </BoxContainer>
            <Snackbar open={openSuccess} autoHideDuration={6000} onClose={handleCloseSuccess}>
                <Alert onClose={handleCloseSuccess} severity="success">
                    Successfully added!
                </Alert>
            </Snackbar>
        </InstitutionsContainerNoCenter>
    )
}

export default UploadFolderFiles;
