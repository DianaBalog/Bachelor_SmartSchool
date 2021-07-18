import styled from 'styled-components';

export const BoxContainer = styled.div`
    width: 50%;
    display: flex;
    flex-direction: column;
    background-color: white;
    border-radius: 19px;

    @media screen and (max-width: 780px) {
        width: 90%;
    }
`;

export const MessageContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
    border-style: solid;
    border-width: 1px;
    border-color: black;

    @media screen and (max-width: 780px) {
        width: 80%;
    }
`;

export const MessagesBox = styled.div`
    width: 50%;
    display: flex;
    flex-direction: column;

    @media screen and (max-width: 780px) {
        width: 90%;
    }
`;
