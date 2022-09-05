// import React, { useCallback, useEffect, useState } from 'react';
// import { useHistory } from 'react-router-dom';
// import { notifyError, notifySuccess } from '../Alert';
// import useAxios from '../useAxios';
// import Autocomplete from '@material-ui/lab/Autocomplete';
// import TextField from '@material-ui/core/TextField';
// import { Link } from "react-router-dom";
// import { Dropdown, Button, Modal } from "react-bootstrap";

// function UpdateModal(props, show, onShowShange, userData) {

// const handleShow = useCallback(() => { onShowShange(false) }, [onShowShange])

//   const history = useHistory();


// const api = useAxios();

// const [data, setData] = useState();

// console.warn("props", props.match.params.id)


// const usersId = props.match.params.id;

// let usersURI = `${process.env.REACT_APP_API_URL}/rest-api/auth/users/${usersId}/`;

//     const initialFormData = Object.freeze({
//         email: userData["user"],
//         first_name: userData["user"],
//         last_name: userData["user"],
//         password: userData["user"],
//         re_password: userData["user"],
//     });

//     const [formData, setFormData] = useState(initialFormData);
//     const [userGroup, setUserGroup] = useState(userData['userGroup']);
//     const [group, setGroup] = useState('');

//     //   useEffect( () =>  {
//     //     api.get(groupsEnd).then( res => {
//     //        console.log('result ', res);
//     //        setUserGroup(res.data)
//     //     }).catch( err => {
//     //        console.log('IRRROR', err);
//     //     })
//     //  }, [userData['userGroup']]);
//     //  const groupIndex = () => {
//     //   const groupList = userGroup
//     //  }
//     const { first_name, last_name, email, password, re_password } = formData;

//     const handleChange = (e) => {
//         setFormData({
//             ...formData,
//             [e.target.name]: e.target.value.trim(),
//         });
//     };

// // useEffect(() => {
// //     api.get(usersURI), {
// //             email: formData.email,
// //             first_name: formData.first_name,
// //             last_name: formData.last_name,
// //             password: formData.password,
// //             re_password: formData.re_password,
// //             group: userGroup,
// //         }.then((res) => {
// //             // window.location = '/login';
// //             console.log(res);
// //             console.log(res.data);
// //             setData(res)

// //     });

// //     // result = res.json();
// // }, []);


//     useEffect(() => {
//         api.get(`${process.env.REACT_APP_API_URL}/rest-api/auth/users/`).then(res => {
//             console.log('result ', res);
//             setData(res.data)
//         }).catch(err => {
//             console.log('IRRROR', err);
//         })
//             // setDette(res.data.dette)
//             // setCreneau(res.data.creneau)
//     }, []);

//     const HandleSubmit = async (e) => {
//         e.preventDefault();
//         const EditedUser = {
//             email: email,
//             first_name: first_name,
//             last_name: last_name,
//             password: password,
//             re_password: re_password,
//             group: userGroup,
//             // dette :Number(dette),
//             // creneau :Number(creneau),
//         };
//         api.put(usersURI, EditedUser).then(res => {
//             notifySuccess('Personnel modifier avec succés')
//             history.push("/personnel");
//         }).catch(err => {
//             notifyError("Erreur lors de la modification du personnel")
//         })
//     };


//   return (
//     <div>
//           <Modal className="fade bd-example-modal-md" size="md" onHide={handleShow} show={show}>
//               <Modal.Header>
//                   <Modal.Title className='text-black'>Modifier / Creer Admin</Modal.Title>
//                   <Button variant="" className="close" onClick={handleShow} >
//                       <span>&times;</span>
//                   </Button>
//               </Modal.Header>
//               <Modal.Body>
//                   <h4 className="text-center mb-4">Creer un nouveau compte</h4>
//                   <form onSubmit={(e) => HandleSubmit(e)}>
//                       <div className="form-group">
//                           <label className="mb-1">
//                               <strong>Email</strong>
//                           </label>
//                           <input type="email" className="form-control" placeholder="hello@example.com" name="email" onChange={(e) => handleChange(e)} value={formData.email} />
//                       </div>
//                       <div className="form-group">
//                           <label className="mb-1">
//                               <strong>Nom</strong>
//                           </label>
//                           <input type="nom" className="form-control" placeholder="votre nom..." name="first_name" onChange={(e) => handleChange(e)} value={formData.first_name} />
//                       </div>
//                       <div className="form-group">
//                           <label className="mb-1">
//                               <strong>Prénom</strong>
//                           </label>
//                           <input type="nom" className="form-control" placeholder="votre Prénom..." name="last_name" onChange={(e) => handleChange(e)} value={formData.last_name} />
//                       </div>
//                       <div className="form-group">
//                           <label>Role(s)</label>
//                           <Autocomplete
//                               style={{ backgroundColor: '#ffffff' }}
//                               onChange={(event, value) => {
//                                   setUserGroup(value.id);
//                               }}
//                               defaultValue={userData[userGroup]}
//                               options={userData['groups']}
//                               getOptionLabel={(option) => (option['name'])}
//                               renderInput={(params) => (<TextField {...params} className="form-control" name="group" label="Role" variant="outlined" fullWidth />)} />
//                       </div>
//                       <div className="form-group">
//                           <label className="mb-1">
//                               <strong>Password</strong>
//                           </label>
//                           <input type="password" className="form-control" name="password" onChange={(e) => handleChange(e)} value={password} />
//                       </div>
//                       <div className="form-group">
//                           <label className="mb-1">
//                               <strong>Password</strong>
//                           </label>
//                           <input type="password" className="form-control" name="re_password" onChange={(e) => handleChange(e)} value={re_password} />
//                       </div>
//                       <div className="text-center mt-4">
//                           <button type="submit" className="btn btn-primary btn-block" > Confirmer </button>
//                       </div>
//                   </form>
//                   <div className="new-account mt-3">
//                       <p>
//                           Vous avez déja un compte ?{" "}
//                           <Link className="text-primary" to="/login">Se connecter</Link>
//                       </p>
//                   </div>
//               </Modal.Body>
//           </Modal> 
//     </div>
//   )
// }

// export default UpdateModal



import React, { useState, useEffect } from "react";
import useAxios from "../useAxios";


import { useHistory } from "react-router-dom";
import ShortCuts from "../ShortCuts";



const UpdateModal = (props) => {
    const api = useAxios();
    const currentUserId = props.match.params.id;

    let userURI = `${process.env.REACT_APP_API_URL}/rest-api/auth/users/${currentUserId}/`

    const history = useHistory();

    const [lastName, setLastName] = useState("");
    const [firstName, setFirstName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [re_password, setRePassword] = useState("");



    useEffect(() => {
        api.get(userURI).then((res) => {
            setLastName(res.data.last_name)
            setFirstName(res.data.first_name)
            setEmail(res.data.email)
            setPassword(res.data.password)
            setRePassword(res.data.re_password)
        })
    }, []);

    const HandleSubmit = async e => {
        e.preventDefault();
        const EditedUser = {
            last_name: lastName,
            first_name: firstName,
            email: email,
            password: password,
            repassword: re_password,
        }
        api.put(userURI, EditedUser).then(() => {
            history.push("/users")
        })

    }

    const [u, setU] = useState(404);

    const aa = api.get(`${process.env.REACT_APP_API_URL}/rest-api/auth/users/${currentUserId}/`)
        .then(res => {
            setU(res.status);
            console.log(res.status);
        }).catch(err => {
            const { status, data, config } = err.response;
            if (status === 404) {
                history.push("/users")
            }
            if (status === 400 && config.method === 'get' && data.error.hasOwnProperty('id')) {
                history.push('/users')
            }
            console.log(err)
            // history.push('/users')
        })


        // if (status === 200)



    return (
        <div className="">
            <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
                <ShortCuts />
            </div>
            <div className="card">
                <div className="card-header">
                    <h4 className="card-title">Modifier Utilisateur</h4>
                </div>
                <div className="card-body">
                    <div className="basic-form">
                        <form onSubmit={HandleSubmit}>
                            <div className="form-row">
                                <div className="form-group col-md-6">
                                    <label>Nom </label>
                                    <input type="text" name="last_name" className="form-control" value={lastName} placeholder="Nom du client" onChange={e => setLastName(e.target.value)} />
                                </div>
                                <div className="form-group col-md-6">
                                    <label>Prénom</label>
                                    <input type="text" name="first_name" className="form-control" value={firstName} placeholder="Prénom du client" onChange={e => setFirstName(e.target.value)} />
                                </div>
                                <div className="form-group col-md-6">
                                    <label>Email </label>
                                    <input type="email" name="email" className="form-control" value={email} placeholder="Email" onChange={e => setEmail(e.target.value)} />
                                </div>
                                {/* <div className="form-group col-md-4">
                      <label>état</label>
                      <select  defaultValue={"option"} name="state" className="form-control"value={etat} onChange={e => setEtat(e.target.value)}>
                        <option value="option" disabled>Cliquez pour choisir</option>
                        <option value="A" >Active</option>
                        <option value="N" >Non active</option>
                        <option value="S" >Suspendue</option>
                      </select>
                    </div> */}
                            </div>
                            <button type="submit" className="btn btn-primary">
                                Confirmer la modification
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

    )
}
export default UpdateModal;




