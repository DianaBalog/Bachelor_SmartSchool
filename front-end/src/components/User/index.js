import { React,  useContext, useState, useRef } from 'react';
import { UserContext } from '../../UserContext';
import { InstitutionsContainer, InstitutionsTitle} from '../Institutions/InstitutionsElements';
import { BoxContainer, DetailsContainer, Img, ImgWrap, ElementsContainer, ButtonBlue } from './UserElements';
import { ErrorMessage, FormContainer, Input } from '../RegisterAndLogin/Common';
import Cookies from 'universal-cookie';


const User = () => {
    const user = useContext(UserContext);
    const cookies = new Cookies();
    const [edit, setEdit] = useState(false);
    const [change, setChange] = useState(false);
    const [changeImg, setChangeImg] = useState(false);
    const [firstName, setFirstName] = useState(user.firstName);
    const [lastName, setLastName] = useState(user.lastName);
    const [currentPassword, setCurrentPassword] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [error, setError] = useState("");
    const [error2, setError2] = useState("");
    const fileInput = useRef(null)


    function HandleEditClick() {
        if(edit){
            setEdit(false)
        } else{
            setEdit(true)
        }
    }


    function HandleChangeClick() {
        if(change){
            setChange(false)
        } else{
            setChange(true)
        }
    }


    function HandleImgClick() {
        if(changeImg){
            setChangeImg(false)
        } else{
            fileInput.current.click()
            setChangeImg(true)
        }
    }


    function EditUser() {
        if(firstName === "" || firstName == null || lastName === "" || lastName == null){
            setError("Fields can't be empty!");
        } else{
            if(user.firstName !== firstName || user.lastName !== lastName){
                fetch('/user/editUserInfo', {
                    method: 'POST',
                    body: JSON.stringify({
                        firstName: firstName, lastName: lastName
                    }),
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                    }
                }).then(response =>
                    response.json()).then((data) => {
                        if(data.ok === '0'){
                            HandleEditClick();
                            user.setCurrentUser({...user, firstName: firstName, lastName: lastName});
                            setError("");
                        };               
                    });
            }
            else{
                HandleEditClick();
                setError("");
            }
        }
    }

    function ChangePassword() {
        if(password === "" || password == null || password2 === "" || password2 == null || currentPassword === "" || currentPassword === null){
            setError2("Fields can't be empty!");
        } else{
            if(password !== password2){
                setError2("Password doesn't match!");
            } else{
                fetch('/user/changeUserPassword', {
                    method: 'POST',
                    body: JSON.stringify({
                        currentPassword: currentPassword, password: password
                    }),
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                    }
                }).then(response =>
                    response.json()).then((data) => {
                        if(data.ok === '0'){
                            HandleChangeClick();
                            setError2("");
                        }
                        else{
                            setError2(data.ok);
                        };             
                    });
                }
        }
    }

    function GetBase64(file){

        return new Promise(resolve => {
          let baseURL = "";
          // Make new FileReader
          let reader = new FileReader();
          
          // on reader load somthing...
          reader.onload = () => {
            // Make a fileInfo Object
            baseURL = reader.result;
            resolve(baseURL);
          };

          // Convert the file to base64 text
          reader.readAsDataURL(file);
        });
      };

    function SaveChangeImage() {
        if(fileInput.current.files.length !== 0){
            var newImg;
            GetBase64(fileInput.current.files[0])
                .then(result => {
                    newImg = result

                    fetch('/user/editUserImage', {
                        method: 'POST',
                        body: JSON.stringify({
                            image: newImg
                        }),
                        credentials: 'same-origin',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': cookies.get('csrf_access_token')
                        }
                    }).then(response =>
                        response.json()).then((data) => {
                            if(data.ok === '0'){
                                HandleImgClick();
                                user.setCurrentUser({...user, image: newImg});
                            };               
                        });
                })
        } else{
            HandleImgClick();
        }
    }

    return (
        <InstitutionsContainer>
            <InstitutionsTitle>User {user.firstName} {user.lastName}</InstitutionsTitle>    
            <BoxContainer>
                <DetailsContainer>
                    <ElementsContainer>
                        <ImgWrap>
                            <Img src={user.image}/>
                        </ImgWrap>
                        {changeImg === false && <ButtonBlue to="#" onClick={HandleImgClick}>Change Image</ButtonBlue>}
                        {changeImg === true && <ButtonBlue to="#" onClick={SaveChangeImage}>Save Image</ButtonBlue>}
                        <input
                            accept="image/*"
                            id="image-file"
                            type="file"
                            ref={fileInput}
                            style={{display: "none"}}
                            />
                    </ElementsContainer>
                    <ElementsContainer>
                        {edit === false && <> <ButtonBlue to="#" onClick={HandleEditClick}>Edit</ButtonBlue>
                        <FormContainer>
                            <Input type="firstName" placeholder="First Name" value={"First Name: " + user.firstName} onChange={e => {setFirstName(e.target.value)}} disabled/>
                            <Input type="lastName" placeholder="Last Name" value={"Last Name: " + user.lastName} onChange={e => {setLastName(e.target.value)}} disabled/>
                        </FormContainer></>}
                        {edit === true &&<> <ButtonBlue to="#" onClick={EditUser}>Save</ButtonBlue>
                        <FormContainer>
                            <Input type="firstName" placeholder="First Name" defaultValue={user.firstName} onChange={e => {setFirstName(e.target.value)}} />
                            <Input type="lastName" placeholder="Last Name" defaultValue={user.lastName} onChange={e => {setLastName(e.target.value)}} />
                        </FormContainer></>}
                        <br/>
                        <ErrorMessage>{error}</ErrorMessage><br/>
                        {change === false && <> <ButtonBlue to="#" onClick={HandleChangeClick}>Change Password</ButtonBlue></>}
                        {change === true && <> <ButtonBlue to="#" onClick={ChangePassword}>Save new password</ButtonBlue>
                        <FormContainer>
                            <Input type="password" placeholder="Current Password" onChange={e => {setCurrentPassword(e.target.value); setError2("")}} />
                            <Input type="password" placeholder="New Password" onChange={e => {setPassword(e.target.value); setError2("")}} />
                            <Input type="password" placeholder="Re-enter new Password" onChange={e => {setPassword2(e.target.value); setError2("")}} />
                        </FormContainer>
                        <br/>
                        <ErrorMessage>{error2}</ErrorMessage>
                        </>}
                    </ElementsContainer>
                </DetailsContainer>
            </BoxContainer>   
        </InstitutionsContainer>
    )
}

export default User;