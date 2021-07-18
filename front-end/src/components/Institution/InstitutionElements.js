import styled from 'styled-components';
import { Link as LinkR } from 'react-router-dom';

export const ButtonMenu = styled(LinkR)`
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
    justify-content: center;


    &:hover {
        transition: all 0.2s ease-in-out;
        background: #4d96b8;
        color: #000;
    }
`

export const ButtonWrapper = styled(LinkR)`
    display: flex;
    justify-content: center;
    float: left;
`