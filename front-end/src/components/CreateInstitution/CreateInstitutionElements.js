import styled from 'styled-components';
import { Link as LinkR } from 'react-router-dom';
import { motion } from "framer-motion";
import Image from '../../images/login.jpg';


export const AppContainer = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-top: 70px;
    padding-bottom: 53px;
    background-image: url(${Image});
    background-color: black;
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    z-index: -10;
`;

export const ButtonLink = styled(LinkR)`
    border-radius: 50px;
    background: #4d96b8;
    white-space: nowrap;
    padding: 10px 22px;
    color: #fff;
    font-size: 16px;
    outline: none;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    text-decoration: none;
    display: flex;
    justify-content: center;
    margin-bottom: 64px;


    &:hover {
        transition: all 0.2s ease-in-out;
        background: #000;
        color: #4d96b8;
    }
`;

export const BackDrop = styled(motion.div)`
    width: 160%;
    height: 550px;
    position: absolute;
    display: flex;
    flex-direction: column;
    border-radius: 50%;
    transform: rotate(60deg);
    top: -350px;
    left: -70px;
    background-color: #4d96b8;
`;

export const TopContainer = styled.div`
    width: 100%;
    height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 0 1.8em;
    padding-bottom: 5em;
`;
