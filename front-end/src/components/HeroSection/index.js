import { React, useState } from 'react';
import Video from '../../videos/home-video.mp4';
import { HeroContainer, HeroBg, VideoBg, HeroContent, HeroH1, HeroP, HeroBtnWrapper, ArrowForward, ArrowRight } from './HeroElements';
import { Button } from '../ButtonElements';

/**
 * When the mouse pointer hovers over the register button, we change setHover state in order to change the button color and animation of the arrow
 * After the mouse pointer is no longer on the button, we change setHover again
 */
const HeroSection = () => {
    const [hover, setHover] = useState(false)

    const onHover = () => {
        setHover(!hover)
    }

    return (
        <HeroContainer id='home'>
            <HeroBg>
                <VideoBg autoPlay loop muted src={Video} type='video/mp4' />
            </HeroBg>
            <HeroContent>
                <HeroH1>Welcome to Smart School</HeroH1>
                <HeroP>Not a member yet? Join our comunity today!</HeroP>
                <HeroBtnWrapper>
                    <Button to="register" onMouseEnter={onHover} onMouseLeave={onHover}
                    primary='true' dark='true' smooth='true' duration={500} spy={true} exact='true' offset={-80}>
                    Register now {hover ? <ArrowForward /> : <ArrowRight />}
                    </Button>
                </HeroBtnWrapper>           
            </HeroContent>
        </HeroContainer>
    )
}

export default HeroSection;
