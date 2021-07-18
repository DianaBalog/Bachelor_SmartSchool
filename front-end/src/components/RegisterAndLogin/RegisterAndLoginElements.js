import styled from "styled-components";
import { motion } from "framer-motion";
import Image from '../../images/login.jpg';

export const AppContainer = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 130px;
    padding-bottom: 53px;
    background-image: url(${Image});
    background-color: black;
    background-size: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    z-index: -10;
`;

export const BoxContainer = styled.div`
    width: 280px;
    min-height: 570px;
    display: flex;
    flex-direction: column;
    border-radius: 19px;
    background-color: #fff;
    box-shadow: 0 0 2px rgba(15, 15, 15, 0.50);
    position: relative;
    overflow: hidden;
`;

export const TopContainer = styled.div`
    width: 100%;
    height: 250px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 0 1.8em;
    padding-bottom: 5em;
`;

export const BackDrop = styled(motion.div)`
    width: 160%;
    height: 550px;
    position: absolute;
    display: flex;
    flex-direction: column;
    border-radius: 50%;
    transform: rotate(60deg);
    top: -290px;
    left: -70px;
    background-color: #4d96b8;
`;

export const BackDropVariants = {
    expanded: {
        width: "233%",
        height: "1050px",
        borderRadius: "20%",
        transform: "rotate(60deg)"
    },
    collapsed: {
        width: "160%",
        height: "550px",
        borderRadius: "50%",
        transform: "rotate(60deg)"
    }
};

export const ExpandingTransition = {
    type: "spring",
    duration: 2.3,
    stiffness: 30
};

export const HeaderContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
`;

export const HeaderText = styled.h2`
    font-size: 30px;
    font-weight: 600;
    line-height: 1.24;
    color: #fff;
    z-index: 10;
    margin: 0;
`;

export const SmallText = styled.h5`
    color: #fff;
    font-weight: 500;
    font-size: 11px;
    z-index: 10;
    margin: 0;
    margin-top: 15px;
`;

export const InnerContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 0 1.8em;
`;