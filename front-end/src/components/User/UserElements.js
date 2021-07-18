import styled from 'styled-components';
import { Link as LinkR } from 'react-router-dom';

export const BoxContainer = styled.div`
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
    border-radius: 19px;

    @media screen and (max-width: 780px) {
        width: 90%;
    }
`;


export const DetailsContainer = styled.div`
    width: 100%;
    min-height: 500px;
    justify-content: flex-start;
    grid-template-columns: 1fr 1fr;
    display: grid;
    align-items: center;
    grid-gap: 16px;
    padding: 0 50px;

    @media screen and (max-width: 780px) {
        grid-template-columns: 1fr;
        padding: 0 20px;
    }
`;

export const ElementsContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
`;

export const ImgWrap = styled.div`
    width: 300px;
    height: 100%;
    padding-top: 50px;
`;

export const Img = styled.img`
    width: 100%;
    margin: 0 0 10px 0;
    padding-right: 0;
`;

export const ButtonBlue = styled(LinkR)`
    border-radius: 50px;
    background: #4d96b8;
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
        background: #000;
        color: #fff;
    }
`