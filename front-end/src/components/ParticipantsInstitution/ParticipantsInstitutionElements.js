import styled from 'styled-components';

export const DetailsContainer = styled.div`
    width: 100%;
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

export const DetailsContainerStart = styled.div`
    width: 100%;
    justify-content: flex-start;
    grid-template-columns: 1fr 1fr;
    display: grid;
    align-items: flex-start;
    grid-gap: 16px;
    padding: 0 50px;

    @media screen and (max-width: 780px) {
        grid-template-columns: 1fr;
        padding: 0 20px;
    }
`;