import { React, useState, useEffect } from 'react';
import { InstitutionsContainer, InstitutionsTitle, InstitutionsWrapper, InstitutionsCard, InstitutionsIcon, InstitutionsDescription, InstitutionsSubtitle, ButtonLink, StyledLink } from './InstitutionsElements';
import Icon from '../../images/institution.svg';
import { Pagination } from '@material-ui/lab';
import { makeStyles } from "@material-ui/core";
import { Marginer } from '../marginer';
import Cookies from 'universal-cookie';
import Menu from '@material-ui/core/Menu';
import { ButtonMenu } from '../Institution/InstitutionElements'
import SettingsIcon from '@material-ui/icons/Settings';

const Institutions = () => {
    const cookies = new Cookies();
    const[institutions, setInstitutions] = useState({pages: null, currentPage: 1, institutionsList: []})

    useEffect(() => {
        fetch('/institution/allInstitutions', {
            method: 'POST',
            body: JSON.stringify({
                pageNumber: institutions.currentPage
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setInstitutions({...institutions, pages: data.pages, institutionsList: data.institutions})
                };               
            });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])


    function getData(value){
        fetch('/institution/allInstitutions', {
            method: 'POST',
            body: JSON.stringify({
                pageNumber: value
            }),
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': cookies.get('csrf_access_token')
            }
        }).then(response =>
            response.json()).then((data) => {
                if(data.ok === '0'){
                    setInstitutions({...institutions, pages: data.pages, currentPage:value, institutionsList: data.institutions})
                };               
            });
    }
    
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
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

    return (
        <InstitutionsContainer>
            <InstitutionsTitle>Institutions</InstitutionsTitle>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <ButtonMenu to={"/createInstitution"}>Create</ButtonMenu>
            </Menu>
            <ButtonLink to="#" aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}><SettingsIcon/></ButtonLink>
            <InstitutionsWrapper>
            {institutions.institutionsList.map(item => {
                return ( 
                       <StyledLink to={"/institution/" + item.id} key={item.id}>
                            <InstitutionsCard id={item.id}>
                                <InstitutionsIcon src={Icon}/>
                                <InstitutionsSubtitle>{item.name}</InstitutionsSubtitle>
                                <InstitutionsDescription>{item.city}</InstitutionsDescription>
                            </InstitutionsCard>
                       </StyledLink>)
            })}
            </InstitutionsWrapper>
            <Marginer direction="vertical" margin={25} />
            <Pagination count={institutions.pages} defaultPage={institutions.currentPage} page={institutions.currentPage} color="primary" classes={{ ul: classes.ul }} onChange={handleChange}/>
        </InstitutionsContainer>
    )
}

export default Institutions;
