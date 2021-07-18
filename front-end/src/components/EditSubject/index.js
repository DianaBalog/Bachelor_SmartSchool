import { React, useState, useRef, useEffect } from 'react';
import { InstitutionsContainerNoCenter, InstitutionsTitle} from '../Institutions/InstitutionsElements';
import { BoxContainer, DetailsContainer, Img, ImgWrap, ElementsContainer, ButtonBlue } from '../User/UserElements';
import { ErrorMessage, FormContainer, Input } from '../RegisterAndLogin/Common';
import Cookies from 'universal-cookie';
import { Marginer } from '../marginer';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { withStyles } from '@material-ui/core/styles';
import Switch from '@material-ui/core/Switch';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import { makeStyles } from "@material-ui/core/styles";
import Modal from "@material-ui/core/Modal";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";
import { Redirect } from 'react-router';
import { ButtonWrapper } from '../Institution/InstitutionElements';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';


const EditSubject = ({id}) => {
    const [edit, setEdit] = useState(false);
    const cookies = new Cookies();
    const[subject, setSubject] = useState({name: "", publicSubject: false, message: false, image: "", role: "", isIn: true})
    const [name, setName] = useState();
    const [state, setState] = useState({publicSubject: subject.publicSubject, message: subject.message});
    const [changeImg, setChangeImg] = useState(false);
    const fileInput = useRef(null)
    const [error, setError] = useState("")
    const [deleted, setDeleted] = useState(false);

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

    const useStyles = makeStyles((theme) => ({
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
    
    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };

    function HandleImgClick() {
        if(changeImg){
            setChangeImg(false)
        } else{
            fileInput.current.click()
            setChangeImg(true)
        }
    }

    useEffect(() => {  
        fetch('/institution/getSubjectInfo', {
            method: 'POST',
            body: JSON.stringify({
                subject: id
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setSubject({...subject, name: data.name, publicSubject: data.public, message: data.message, image: data.image, role: data.role, isIn: data.isIn});
                    setState({...state, publicSubject: data.public, message: data.message});
                    setName(data.name);
                };               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps  
    }, []); 

    function EditSubject() {
        if(name === "" || name == null){
            setError("Name can't be empty!");
        } else {
            fetch('/institution/editSubjectInfo', {
                method: 'POST',
                body: JSON.stringify({
                    id: id , name: name, public: state.publicSubject, message: state.message
                }),
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                }
            }).then(response =>
                response.json()).then((data) => {
                    if(data.ok === '0'){
                        HandleEditClick();
                        setSubject({...subject, name: name, public: state.publicSubject, message: state.message});
                    }; 
                    setError("");              
                });
        }
    }


    function GetBase64(file){

        return new Promise(resolve => {
          let baseURL = "";
          // Make new FileReader
          let reader = new FileReader();
          
          // on reader load somthing...
          reader.onload = () => {
            // Make a fileInfo Object
            baseURL = reader.result;
            resolve(baseURL);
          };

          // Convert the file to base64 text
          reader.readAsDataURL(file);
        });
      };

    function SaveChangeImage() {
        if(fileInput.current.files.length !== 0){
            var newImg;
            GetBase64(fileInput.current.files[0])
                .then(result => {
                    newImg = result

                    fetch('/institution/editSubjectImage', {
                        method: 'POST',
                        body: JSON.stringify({
                            id: id , image: newImg
                        }),
                        credentials: 'same-origin',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                        }
                    }).then(response =>
                        response.json()).then((data) => {
                            if(data.ok === '0'){
                                HandleImgClick();
                                setSubject({...subject, image: newImg});
                            };               
                        });
                })
        } else{
            HandleImgClick();
        }
    }

    function DeleteSubject(){
        fetch('/institution/deleteSubject', {
            method: 'DELETE',
            body: JSON.stringify({
                subject: id
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.delete === '0'){
                    setDeleted(true);
                };             
            });
    }

    function HandleEditClick() {
        if(edit){
            setEdit(false)
        } else{
            setEdit(true)
        }
    }

    const classes = useStyles();
    const [open, setOpen] = useState(false);

    const handleOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    if(deleted){
        return <Redirect to="/institutions"/>;
    }

    if(!subject.isIn){
        return <Redirect to="/"/>;
    }
    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/subject/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={subject.name}>
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>
            <InstitutionsTitle style={{alignSelf: "center"}}>Subject Info</InstitutionsTitle>    
            <BoxContainer style={{alignSelf: "center"}}>
                <br/>
                {subject.role === "teacher" && <DeleteForeverIcon fontSize="large" style={{fill: "#4d96b8", cursor: "pointer"}} onClick={handleOpen} />}
                <Modal  
                    className={classes.modal}
                    open={open}
                    onClose={handleClose}
                    closeAfterTransition
                    BackdropComponent={Backdrop}
                    BackdropProps={{
                    timeout: 500
                    }}
                >
                    <Fade in={open}>
                        <div className={classes.paper}>
                            <br/><br/>
                            <h2>Are you sure you want to delete this subject?</h2>
                            <br/>
                            <h2 style={{color:"#4d96b8"}}>{subject.name}</h2>
                            <br/><br/>
                            <p>This action can't be undone!</p>
                            <br/><br/>
                            <ButtonBlue to="#" onClick={DeleteSubject} style={{justifyContent:"center"}}>Delete</ButtonBlue>
                        </div>
                    </Fade>
                </Modal>
                <DetailsContainer>
                    <ElementsContainer>
                        <ImgWrap>
                            <Img src={subject.image}/>
                        </ImgWrap>
                        {changeImg === false && subject.role === "teacher" && <ButtonBlue to="#" onClick={HandleImgClick}>Change Image</ButtonBlue>}
                        {changeImg === true && <ButtonBlue to="#" onClick={SaveChangeImage}>Save Image</ButtonBlue>}
                        <input
                            accept="image/*"
                            id="image-file"
                            type="file"
                            ref={fileInput}
                            style={{display: "none"}}
                        />
                         
                    </ElementsContainer>
                    <ElementsContainer>
                        {edit === false &&<> 
                        <h5 style={{color:"#4d96b8"}}>Current subject info</h5><br/>
                        <FormContainer>
                            <Input type="name" placeholder="Name" value={"Name: " + subject.name} disabled/>
                        </FormContainer>
                        <Marginer direction="vertical" margin={20} />
                        <FormControlLabel
                            control={<CustomSwitch checked={state.publicSubject} disabled name="publicSubject" />}
                            label="Public"
                        />
                        <Marginer direction="vertical" margin={15} />
                        <FormControlLabel
                            control={<CustomSwitch checked={state.message} disabled name="message" />}
                            label="Message"
                        />
                        <Marginer direction="vertical" margin={15} />
                        <br/>
                        {subject.role === "teacher" && <ButtonBlue to="#" onClick={HandleEditClick}>Edit</ButtonBlue>}
                        </>}

                        {edit === true &&<> 
                        <h5 style={{color:"#4d96b8"}}>Edit fields you want to change</h5><br/>
                        <FormContainer>
                            <Input type="name" placeholder="Name" defaultValue={subject.name} onChange={e => {setName(e.target.value); setError("")}}/>
                        </FormContainer>
                        <br/>
                        <ErrorMessage>{error}</ErrorMessage>
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
                        <br/>
                        <ButtonBlue to="#" onClick={EditSubject}>Save</ButtonBlue>
                        </>}
                    </ElementsContainer>
                </DetailsContainer>
            </BoxContainer>   
        </InstitutionsContainerNoCenter>
    )
}

export default EditSubject;