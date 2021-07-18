import { React, useState, useEffect } from 'react';
import { InstitutionsContainerNoCenter, InstitutionsTitle} from '../Institutions/InstitutionsElements';
import { BoxContainer, DetailsContainer, Img, ImgWrap, ElementsContainer, ButtonBlue } from '../User/UserElements';
import Image from '../../images/institution.svg';
import { ErrorMessage, FormContainer, Input } from '../RegisterAndLogin/Common';
import Cookies from 'universal-cookie';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import { makeStyles } from "@material-ui/core/styles";
import Modal from "@material-ui/core/Modal";
import Backdrop from "@material-ui/core/Backdrop";
import Fade from "@material-ui/core/Fade";
import { Redirect } from 'react-router';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import { ButtonWrapper } from '../Institution/InstitutionElements';


const EditInstitution = ({id}) => {
    const cookies = new Cookies();
    const[institution, setInstitution] = useState({name: "", country: "", region: "", city: "", street: "", number: "", isIn: true})
    const [edit, setEdit] = useState(false);
    const [name, setName] = useState();
    const [country, setCountry] = useState();
    const [region, setRegion] = useState();
    const [city, setCity] = useState();
    const [street, setStreet] = useState();
    const [number, setNumber] = useState();
    const [error, setError] = useState("");
    const [deleted, setDeleted] = useState(false);

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

    useEffect(() => {  
        fetch('/institution/getInstitutionInfo', {
            method: 'POST',
            body: JSON.stringify({
                institution: id
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setInstitution({...institution, name: data.name, country: data.country, region: data.region, city: data.city, street: data.street, number: data.number, role: data.role, isIn: data.isIn});
                    setName(data.name);
                    setCountry(data.country);
                    setRegion(data.region);
                    setCity(data.city);
                    setStreet(data.street);
                    setNumber(data.number);
                };
                setError("");               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps    
    }, []); 

    function EditInstitution() {
        if(name === "" || name == null || country === "" || country == null || region === "" || region == null || city === "" || city == null || street === "" || street == null || number === "" || number == null){
            setError("Fields can't be empty!");
        } else{
            fetch('/institution/editInstitutionInfo', {
                method: 'POST',
                body: JSON.stringify({
                    id: id , name: name, country: country, region: region, city: city, street: street, number: number
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
                        setInstitution({...institution, name: name, country: country, region: region, city: city, street: street, number: number})
                    };               
                });
        }
    }

    function DeleteInstitution(){
        fetch('/institution/delete', {
            method: 'DELETE',
            body: JSON.stringify({
                institution: id
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

    if(!institution.isIn){
        return <Redirect to="/"/>;
    }

    return (
        <InstitutionsContainerNoCenter>
            <ButtonWrapper to={"/institution/" + id} style={{justifyContent: "flex-start", paddingLeft: "20px"}}>
                <Tooltip title={institution.name}>
                    <IconButton edge="end" aria-label="user" >
                        <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                    </IconButton>
                </Tooltip>
            </ButtonWrapper>            
            <InstitutionsTitle style={{alignSelf: "center"}}>Institution Info</InstitutionsTitle>    
            <BoxContainer style={{alignSelf: "center"}}>
                <br/>
                {institution.role === "owner" && <DeleteForeverIcon fontSize="large" style={{fill: "#4d96b8", cursor: "pointer"}} onClick={handleOpen} />}
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
                            <h2>Are you sure you want to delete this institution?</h2>
                            <br/>
                            <h2 style={{color:"#4d96b8"}}>{institution.name}</h2>
                            <br/><br/>
                            <p>This action can't be undone!</p>
                            <br/><br/>
                            <ButtonBlue to="#" onClick={DeleteInstitution} style={{justifyContent:"center"}}>Delete</ButtonBlue>
                        </div>
                    </Fade>
                </Modal>
                <DetailsContainer>
                    <ElementsContainer>
                        <ImgWrap>
                            <Img src={Image}/>
                        </ImgWrap>
                    </ElementsContainer>
                    <ElementsContainer>
                        {edit === false && <> 
                        <h5 style={{color:"#4d96b8"}}>Current institution info</h5><br/>
                        <FormContainer>
                            <Input type="name" placeholder="Name" value={"Name: " + institution.name} disabled/>
                            <Input type="country" placeholder="Country" value={"Country: " + institution.country} disabled/>
                            <Input type="region" placeholder="Region" value={"Region: " + institution.region} disabled/>
                            <Input type="city" placeholder="City" value={"City: " + institution.city} disabled/>
                            <Input type="street" placeholder="Street" value={"Street: " + institution.street} disabled/>
                            <Input type="addressnumber" placeholder="Number" value={"Number: " + institution.number} disabled/>
                        </FormContainer>
                        <br/>
                        {institution.role === "owner" && <ButtonBlue to="#" onClick={HandleEditClick}>Edit</ButtonBlue>}
                        </>}
                        {edit === true &&<> 
                        <h5 style={{color:"#4d96b8"}}>Edit fields you want to change</h5><br/>
                        <FormContainer>
                            <Input type="name" placeholder="Name" defaultValue={institution.name} onChange={e => {setName(e.target.value); setError("")}}/>
                            <Input type="country" placeholder="Country" defaultValue={institution.country} onChange={e => {setCountry(e.target.value); setError("")}}/>
                            <Input type="region" placeholder="Region" defaultValue={institution.region} onChange={e => {setRegion(e.target.value); setError("")}}/>
                            <Input type="city" placeholder="City" defaultValue={institution.city} onChange={e => {setCity(e.target.value); setError("")}}/>
                            <Input type="street" placeholder="Street" defaultValue={institution.street} onChange={e => {setStreet(e.target.value); setError("")}}/>
                            <Input type="addressnumber" placeholder="Number" defaultValue={institution.number} onChange={e => {setNumber(e.target.value); setError("")}}/>
                        </FormContainer>
                        <br/>
                        <ErrorMessage>{error}</ErrorMessage>
                        <br/>
                        <ButtonBlue to="#" onClick={EditInstitution}>Save</ButtonBlue>
                        </>}
                    </ElementsContainer>
                </DetailsContainer>
            </BoxContainer>   
        </InstitutionsContainerNoCenter>
    )
}

export default EditInstitution;