import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages';
import LoginPage from './pages/login';
import UserPage from './pages/user';
import InstitutionsPage from './pages/institutions';
import { UserContext } from './UserContext';
import { useState, useEffect } from 'react';
import CreateInstitutionPage from './pages/createInstitution';
import CurrentInstitutionPage from './pages/currentInstitution';
import { CircularProgress } from '@material-ui/core';
import SubjectPage from './pages/subject';
import CreateSubjectPage from './pages/createSubject';
import SearchSubjectPage from './pages/searchSubjects';
import EditInstitutionPage from './pages/editInstitution';
import EditSubjectPage from './pages/editSubject';
import ParticipantsInstitutionPage from './pages/participantsInstitution';
import ParticipantsSubjectPage from './pages/participantsSubject';
import UploadFilesPage from './pages/uploadFiles';
import PostPage from './pages/post';
import FilesSubjectPage from './pages/filesSubject';
import CreateFolderPage from './pages/createFolder';
import FolderPage from './pages/folder';
import UploadFolderFilesPage from './pages/uploadFolderFiles'
import DownloadFilePage from './pages/downloadFile';

function App() {

  const [currentUser, setCurrentUser] = useState(null);

  useEffect(() => {
    fetch('/user/info').then(response => 
      response.json().then(data => {
          if(data.ok === "0") {
              setCurrentUser({firstName: data.firstName, lastName: data.lastName, image: data.photo});
          }
          else{
            setCurrentUser({});
          }
      }
    ));
    
    return( <div style={{display: 'flex', justifyContent: 'center', alignItems: "center", height: "100%"}}>
              <CircularProgress />
            </div>)
    
  }, [])
  
  return (
    <UserContext.Provider value={{...currentUser, setCurrentUser: setCurrentUser}}>
      <Router>
        <Switch>
          <Route path="/" component={Home} exact />
          <Route path="/login" component={LoginPage} exact />
          <Route path="/user" component={UserPage} exact />
          <Route path="/institutions" component={InstitutionsPage} exact />
          <Route path="/createInstitution" component={CreateInstitutionPage} exact />
          <Route path="/institution/:id" component={CurrentInstitutionPage} exact />
          <Route path="/createSubject/:id" component={CreateSubjectPage} exact />
          <Route path="/subject/:id" component={SubjectPage} exact />
          <Route path="/searchSubjects" component={SearchSubjectPage} exact />
          <Route path="/editInstitution/:id" component={EditInstitutionPage} exact />
          <Route path="/editSubject/:id" component={EditSubjectPage} exact />
          <Route path="/participantsInstitution/:id" component={ParticipantsInstitutionPage} exact />
          <Route path="/participantsSubject/:id" component={ParticipantsSubjectPage} exact /> 
          <Route path="/post/:id" component={PostPage} exact /> 
          <Route path="/subjectFiles/:id" component={FilesSubjectPage} exact />
          <Route path="/uploadFiles/:id" component={UploadFilesPage} exact />
          <Route path="/createFolder/:id" component={CreateFolderPage} exact />
          <Route path="/folder/:id" component={FolderPage} exact />
          <Route path="/uploadFolderFiles/:id" component={UploadFolderFilesPage} exact />
          <Route path="/download/:fileName&:id" component={DownloadFilePage} exact />
        </Switch>
      </Router>
    </UserContext.Provider>
  );
}

export default App;
