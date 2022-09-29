import React, { Fragment , useCallback, useEffect, useState} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button, Modal } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
// import DetteCreateModal from './DetteCreateModal';
/// images 
import { Link } from "react-router-dom";
import { useHistory } from 'react-router-dom';
import useAxios from "../useAxios";

import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import { notifyError, notifySuccess } from "../Alert";


const UserModal = ({show, onShowShange, userData}) => {

  // const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
  // const api = useAxios();
  // const [selectedUser, setSelectedUser] = useState();
  // const [groups, setGroups] = useState();

  //   const initialFormData = Object.freeze({
  //     email: userData["user"],
  //     first_name: userData["user"],
  //     last_name: userData["user"],
  //     password: userData["user"],
  //     re_password: userData["user"],
  //     });

  //   const [formData, setFormData] = useState(initialFormData);
  //   const [userGroup, setUserGroup] = useState(userData['userGroup']);
  //   const [group, setGroup] = useState('');

  //   useEffect( () =>  {
  //     api.get(groupsEnd).then( res => {
  //        //console.log('result ', res);
  //        setUserGroup(res.data)
  //     }).catch( err => {
  //        //console.log('IRRROR', err);
  //     })
  //  }, [userData['userGroup']]);
  //  const groupIndex = () => {
  //   const groupList = userGroup
  //  }
    // const { first_name, last_name, email, password, re_password} = formData;
    
    //   const handleChange = (e) => {
    //       setFormData({
    //           ...formData,
    //           [e.target.name]: e.target.value.trim(),
    //       });
    //   };

    //   const handleSubmit = (e) => {
    //       e.preventDefault();
    //       // console.log("FORM DATA =>", formData);
    //       api.post(`${process.env.REACT_APP_API_URL}/rest-api/auth/register`, {
    //         email: email,
    //         first_name: first_name,
    //         last_name: last_name,
    //         password: password,
    //         re_password: re_password,
    //         group: userGroup,
    //       }).then((res) => {
    //           // window.location = '/login';
    //           console.log(res);
    //           console.log(res.data);
    //       });
    //   };

  const api = useAxios();

  // const creneaux = useGetAPI(creneauxEnd)
  const history = useHistory();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])

  const [userGroup, setUserGroup] = useState(userData['userGroup']);
  const [group, setGroup] = useState('');

  //   useEffect( () =>  {
  //     api.get(groupsEnd).then( res => {
  //        //console.log('result ', res);
  //        setUserGroup(res.data)
  //     }).catch( err => {
  //        //console.log('IRRROR', err);
  //     })
  //  }, [userData['userGroup']]);
   
  //  const groupIndex = () => {
  //   const groupList = userGroup
  //  }

  const [last_name, setLastName] = useState("");
  const [first_name, setFirstName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [re_password, setRePassword] = useState("");

  //FK 

  // const HandleSubmit = async e => {
  //   let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/auth/register`
  //   e.preventDefault();
  //   const newUser = {
  //     last_name: last_name,
  //     first_name: first_name,
  //     email: email,
  //     password: password,
  //     re_password: re_password,
  //     group: userGroup,
  //   }
  //   if (email !== '') {
  //     newUser.email = email
  //   }

  const HandleSubmit = (e) => {
    e.preventDefault();
    // console.log("FORM DATA =>", formData);
    api.post(`${process.env.REACT_APP_API_URL}/rest-api/auth/register`, {
      email: email,
      first_name: first_name,
      last_name:  last_name,
      password:  password,
      re_password:  re_password,
      group: userGroup,
    }).then((res) => {
        // window.location = '/login';
        console.log(res);
        console.log(res.data);
        notifySuccess(" Le Client a été ajouter avec succés");
        onShowShange(false)
    }).catch(err => {
      notifyError("Erreur lors de la creation de l'abonnement")
    });
};


    // api.post(endpoint, newUser).then(res => {
    //   notifySuccess('User creer avec succés')
    //   history.push("/users")
    // }).catch(err => {
    //   notifyError("Erreur lors de la creation du User")
    // })

  // }
   return (
    <Modal  className="fade bd-example-modal-md" size="md" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer Admin</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
        <h4 className="text-center mb-4">Creer un nouveau compte</h4>
        <form onSubmit={(e) => HandleSubmit(e)}>
          <div className="form-group">
            <label className="mb-1">
              <strong>Email</strong>
            </label>
            <input type="email" className="form-control" placeholder="hello@example.com" name="email" onChange={(e) => setEmail(e.target.value)} value={email} />
          </div>
          <div className="form-group">
            <label className="mb-1">
              <strong>Nom</strong>
            </label>
            <input type="nom" className="form-control" placeholder="votre nom..." name="first_name" onChange={(e) => setFirstName(e.target.value)} value={first_name} />
          </div>
          <div className="form-group">
            <label className="mb-1">
              <strong>Prénom</strong>
            </label>
            <input type="nom" className="form-control" placeholder="votre Prénom..." name="last_name" onChange={(e) => setLastName(e.target.value)} value={last_name} />
          </div>
          <div className="form-group">
            <label>Role(s)</label>
            <Autocomplete
              style={{backgroundColor:'#ffffff'}}
              onChange={(event, value) => {
                setUserGroup(value.id);
              }}
              defaultValue={userData[userGroup]}
              options={userData['groups']}
              getOptionLabel={(option) => (option['name'])}
              renderInput={(params) => (<TextField {...params} className="form-control" name="group" label="Role" variant="outlined" fullWidth />)} />
        </div>
          <div className="form-group">
            <label className="mb-1">
              <strong>Password</strong>
            </label>
            <input type="password" className="form-control" name="password" onChange={(e) => setPassword(e.target.value)} value={password} />
          </div>
          <div className="form-group">
            <label className="mb-1">
              <strong>Password</strong>
            </label>
            <input type="password" className="form-control" name="re_password" onChange={(e) => setRePassword(e.target.value)} value={re_password} />
          </div>
          <div className="text-center mt-4">
            <button type="submit" className="btn btn-primary btn-block" > Confirmer </button>
          </div>
        </form>
        <div className="new-account mt-3">
          <p>
            Vous avez déja un compte ?{" "}
            <Link className="text-primary" to="/login">Se connecter</Link>
          </p>
        </div>
    </Modal.Body>
    </Modal>
   );
};

export default UserModal;
