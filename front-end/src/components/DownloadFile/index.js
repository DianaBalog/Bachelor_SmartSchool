import { React } from 'react';
import { InstitutionsContainerNoCenter, InstitutionsTitle} from '../Institutions/InstitutionsElements';
import { ButtonBlue } from '../User/UserElements';


const DownloadFile = ({fileName, id}) => {

    return (
        <InstitutionsContainerNoCenter>
            <InstitutionsTitle style={{alignSelf: "center", marginTop: "50px"}}>Download {fileName}</InstitutionsTitle>
            <br/>
            <ButtonBlue style={{alignSelf: "center"}} to={{ pathname: process.env.REACT_APP_BACK + "institution/downloadFile/" + id }} target="_blank" >Download</ButtonBlue>
        </InstitutionsContainerNoCenter>
    )
}

export default DownloadFile;