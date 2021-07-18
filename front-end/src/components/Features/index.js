import { React } from 'react';
import { FeaturesContainer, FeaturesTitle, FeaturesWrapper, FeaturesCard, FeaturesIcon, FeaturesDescription, FeaturesSubtitle } from './FeaturesElements'
import Icon1 from '../../images/home-3_1.svg';
import Icon2 from '../../images/home-3_3.svg';
import Icon3 from '../../images/home-3_2.svg';

const Features = () => {
    return (
        <FeaturesContainer id="features">
            <FeaturesTitle>Features</FeaturesTitle>
            <FeaturesWrapper>
                <FeaturesCard>
                    <FeaturesIcon src={Icon2}/>
                    <FeaturesSubtitle>Schedule</FeaturesSubtitle>
                    <FeaturesDescription>Possibility to create a schedule and maintain all events from the user's subjects.</FeaturesDescription>
                </FeaturesCard>
                <FeaturesCard>
                    <FeaturesIcon src={Icon1}/>
                    <FeaturesSubtitle>Automatic notation</FeaturesSubtitle>
                    <FeaturesDescription>Automatic correction of tests and quizzes according to user preferences.</FeaturesDescription>
                </FeaturesCard>
                <FeaturesCard>
                    <FeaturesIcon src={Icon3}/>
                    <FeaturesSubtitle>Video</FeaturesSubtitle>
                    <FeaturesDescription>Videoconferencing for subjects and related courses for better communication.</FeaturesDescription>
                </FeaturesCard>
            </FeaturesWrapper>
        </FeaturesContainer>
    )
}

export default Features;
