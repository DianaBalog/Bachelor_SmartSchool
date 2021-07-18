import styled from 'styled-components';
import Image from '../../images/login.jpg';
import { Link as LinkR } from 'react-router-dom';

export const InstitutionsContainer = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-top: 130px;
    padding-bottom: 53px;
    background-image: url(${Image});
    background-color: black;
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    z-index: -10;
`;

export const InstitutionsContainerWithBack = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-top: 5px;
    padding-bottom: 53px;
    background-image: url(${Image});
    background-color: black;
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    z-index: -10;
`;

export const InstitutionsContainerNoCenter = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding-top: 70px;
    padding-bottom: 53px;
    background-image: url(${Image});
    background-color: black;
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    z-index: -10;
`;

export const InstitutionsWrapper = styled.div`
    max-width: 1000px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    align-items: center;
    grid-gap: 16px;

    @media screen and (max-width: 1000px) {
        grid-template-columns: 1fr 1fr 1fr;
    }

    @media screen and (max-width: 885px) {
        grid-template-columns: 1fr 1fr;
    }

    @media screen and (max-width: 650px) {
        grid-template-columns: 1fr;
        padding: 0 20px;
    }
`;

export const InstitutionsCard = styled.div`
    background: #fff;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    border-radius: 10px;
    height: 340px;
    width: 240px;
    padding: 30px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    transition: all 0.2s ease-in-out;

    &:hover {
        transform: scale(1.02);
        transition: all 0.2s ease-in-out;
        cursor: pointer;
    }
`;

export const InstitutionsIcon = styled.img`
    height: 160px;
    width: 160px;
    margin-bottom: 10px;
`;

export const InstitutionsTitleWrapper= styled.div`
    align-items: center;
    background-color: #4d96b8;
    justify-content: center;
    width: 80%;
    display: flex;   
    box-shadow: 0px 3px 2px rgba(0, 0, 0, 0.8);
    border: 10px solid transparent;
    border-right-color: black;
    border-left-color: black;
    border-right-width: 20px;
    border-radius: 14px;
    
`;

export const InstitutionsTitle = styled.h1`
    font-size: 2.5rem;
    color: #fff;
    margin-bottom: 15px;

    @media screen and (max-width: 480px) {
        font-size: 2rem;
    }
`;

export const InstitutionsSubtitle = styled.h2`
    font-size: 1rem;
    margin-bottom: 10px;
`;

export const InstitutionsDescription = styled.p`
    font-size: 1rem;
    text-align: center;
`;

export const StyledLink = styled(LinkR)`
  color: black;
  text-decoration: none;
`;

export const ButtonLink = styled(LinkR)`
    border-radius: 50px;
    background: #fff;
    white-space: nowrap;
    padding: 10px 22px;
    color: #000;
    font-size: 16px;
    outline: none;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    text-decoration: none;
    display: flex;
    justify-content: flex-end;
    margin-bottom: 64px;


    &:hover {
        transition: all 0.2s ease-in-out;
        background: #4d96b8;
        color: #000;
    }
`