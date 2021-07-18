import styled from "styled-components";
import { Link as LinkR } from 'react-router-dom';

export const BoxContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 10px;
`;

export const FormContainer = styled.form`
    width: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: 0px 0px 2.5px rgba(15, 15, 15, 0.19);
`;

export const MutedLink = styled.a`
    font-size: 11px;
    color: rgba(200, 200, 200, 0.8);
    font-weight: 500;
    text-decoration: none;
`;

export const MutedMessage = styled.div`
    font-size: 11px;
    color: rgba(200, 200, 200, 0.8);
    font-weight: 500;
    text-decoration: none;
`;

export const ErrorMessage = styled.h5`
    color: red;
    font-weight: 500;
    font-size: 11px;
`;

export const SuccessMessage = styled.h5`
    color: green;
    font-weight: 500;
    font-size: 11px;
`;

export const BoldLink = styled.a`
    font-size: 12px;
    color: #4d96b8;
    font-weight: 500;
    text-decoration: none;
    margin: 0 4px;
    cursor: pointer;
`;

export const Input = styled.input`
    width: 100%;
    height: 42px;
    outline: none;
    border: 1px solid rgba(200, 200, 200, 0.3);
    padding: 0px 10px;
    border-bottom: 1.4px solid transparent;
    transition: all 200ms ease-in-out;
    font-size: 12px;

    &::placeholder {
        color: rgba(200, 200, 200, 1)
    } 

    &:not(:last-of-type) {
        border-bottom: 1.5px solid rgba(200, 200, 200, 0.4);
    }

    &:focus {
        outline: none;
        border-bottom: 2px solid #4d96b8;
    }
`;

export const SubmitButton = styled.button`
    width: 100%;
    padding: 11px 40%;
    color: #fff;
    font-size: 15px;
    font-weight: 600;
    border: none;
    border-radius: 100px 100px 100px 100px;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    background: #4d96b8;

    &:hover {
        filter: brightness(1.03);
        background: #000;
        transition: all 0.2s ease-in-out;
    }
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

    &:hover {
        transition: all 0.2s ease-in-out;
        background: #010606;
        color: #4d96b8;
    }
`