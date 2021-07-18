import { React, useState, useEffect } from 'react';
import { InstitutionsContainerWithBack, InstitutionsTitle, InstitutionsWrapper, InstitutionsCard, InstitutionsIcon, InstitutionsDescription, InstitutionsSubtitle, ButtonLink, StyledLink } from '../Institutions/InstitutionsElements';
import { Pagination } from '@material-ui/lab';
import { makeStyles } from "@material-ui/core";
import { Marginer } from '../marginer';
import Cookies from 'universal-cookie';
import Menu from '@material-ui/core/Menu';
import { ButtonMenu, ButtonWrapper } from './InstitutionElements';
import SettingsIcon from '@material-ui/icons/Settings';
import ArrowBackIosIcon from '@material-ui/icons/ArrowBackIos';
import { Tooltip } from '@material-ui/core';
import IconButton from '@material-ui/core/IconButton';
import { Redirect } from 'react-router-dom';

const Institution = ({id}) => {
    const cookies = new Cookies();
    const[subjects, setSubjects] = useState({pages: null, currentPage: 1, subjectsList: [], role: "", isIn: true})
    const[name, setName] = useState();

    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };
    
    useEffect(() => {
        fetch('/institution/allInstitutionSubjects', {
            method: 'POST',
            body: JSON.stringify({
                pageNumber: subjects.currentPage,
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
                    setSubjects({...subjects, pages: data.pages, subjectsList: data.subjects, role: data.role, isIn: data.isIn})
                    setName(data.institutionName)
                };               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    function getData(value){
        fetch('/institution/allInstitutionSubjects', {
            method: 'POST',
            body: JSON.stringify({
                pageNumber: value,
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
                    setSubjects({...subjects, pages: data.pages, currentPage:value, subjectsList: data.subjects, role: data.role, isIn: data.isIn})
                };               
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

    if(!subjects.isIn){
        return <Redirect to="/"/>;
    }

    return (
        <>
        <ButtonWrapper to="/institutions"  style={{justifyContent: "flex-start", paddingTop: "70px", paddingLeft: "20px"}}>
            <Tooltip title="Institutions">
                <IconButton edge="end" aria-label="user" >
                    <ArrowBackIosIcon  style={{fill: "#4d96b8"}} fontSize="large"/>
                </IconButton>
            </Tooltip>
        </ButtonWrapper>
        <InstitutionsContainerWithBack>
            <InstitutionsTitle>{name}</InstitutionsTitle>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                {subjects.role === "owner" && <ButtonMenu to={"/createSubject/" + id}>Create Subject</ButtonMenu>}
                <ButtonMenu to={"/editInstitution/" + id}>Institution Info</ButtonMenu>
                <ButtonMenu to={"/participantsInstitution/" + id}>Participants</ButtonMenu>
            </Menu>
            <ButtonLink to="#" aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}><SettingsIcon/></ButtonLink>
            <InstitutionsWrapper>
            {subjects.subjectsList.map(item => {
                return (
                        <StyledLink to={"/subject/" + item.id} key={item.id}> 
                            <InstitutionsCard id={item.id}>
                                <InstitutionsIcon src={item.image}/>
                                <InstitutionsSubtitle>{item.name}</InstitutionsSubtitle>
                                <InstitutionsDescription>{item.institution}</InstitutionsDescription>
                            </InstitutionsCard>
                        </StyledLink>)
            })}
            </InstitutionsWrapper>
            <Marginer direction="vertical" margin={25} />
            <Pagination count={subjects.pages} defaultPage={subjects.currentPage} page={subjects.currentPage} color="primary" classes={{ ul: classes.ul }} onChange={handleChange}/>
        </InstitutionsContainerWithBack>
        </>
    )
}

export default Institution;
