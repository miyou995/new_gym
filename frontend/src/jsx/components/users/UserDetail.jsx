import React, { useState, useEffect } from "react";
import useAxios from "../useAxios";

import { useHistory } from "react-router-dom";
import ShortCuts from "../ShortCuts";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { TextField } from "@material-ui/core";
import { notifyError, notifySuccess } from "../Alert";
import { ToastContainer } from "react-toastify";

const UserDetail = (props) => {
    const api = useAxios();
    
    const currentUserId = props.match.params.id;

    let userURI = `${process.env.REACT_APP_API_URL}/rest-api/auth/users/${currentUserId}/`
    let groupsEnd = `${process.env.REACT_APP_API_URL}/rest-api/auth/groups/`

    const history = useHistory();

    const [lastName, setLastName] = useState("");
    const [firstName, setFirstName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [rePassword, setRePassword] = useState("");
    const [userGroups, setUserGroups] = useState([]);
    const [userFirstGroup, setUserFirstGroup] = useState({});
    const [groups, setGroups] = useState([]);
    

    useEffect( () => {
        api.get(groupsEnd).then( (res) => {
             setGroups(res.data)
            // console.log("fetch groups repsponse", res);
        })
        api.get(userURI).then((res) => {
            setLastName(res.data.last_name !== null ? res.data.last_name : "" )
            setFirstName(res.data.first_name !== null ? res.data.first_name : "")
            setEmail(res.data.email !== null ? res.data.email : "")
            setUserGroups(res.data.groups)
        })

    }, [userURI, groupsEnd]);





    useEffect(() => {
        const groupId = userGroups[0]
        const result = groups.find(({ id }) => id === groupId);
        setUserFirstGroup(result)
        console.log("setUserGroupgroups", groups);
        console.log("ITEM °°°°°°°°°> ", result);
        console.log("userFirstGroup °°°°°°°°°> ", userFirstGroup);
    }, [userGroups]);

    const HandleSubmit = async (e) => {
        e.preventDefault();
        const EditedUser = {
            email: email,
            first_name: firstName,
            last_name: lastName,
            groups: [Number(userFirstGroup.id)],
        };
        if (password !== rePassword) {
            notifyError("Vérifier que les mots de pass sont identique")
        }else {
            if (password !== ""){
                console.log("ADDED");
                EditedUser["password"] = password
                EditedUser["repassword"] = rePassword
            }
            api.patch(userURI, EditedUser).then(res => {
                history.push("/users");
                notifySuccess('utilisateur modifier avec succés')
            }).catch(err => {
                notifyError("Erreur lors de la modification de l'utilisateur")
            })
        }
    };

    const [userEditStatus, setUserEditStatus] = useState(null);

    return (
        <div className="">
            <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
                <ShortCuts />
            </div>
            <>
                <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
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
                                        <input type="text" name="last_name" className="form-control" value={lastName} onChange={e => setLastName(e.target.value)} />
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label>Prénom</label>
                                        <input type="text" name="first_name" className="form-control" value={firstName} onChange={e => setFirstName(e.target.value)} />
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label>Email </label>
                                        <input type="email" name="email" className="form-control" value={email}  onChange={e => setEmail(e.target.value)} />
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label> Role(s) </label>
                                        <Autocomplete
                                            style={{backgroundColor: '#fff'}}
                                            options={groups}
                                            getOptionLabel={(option) => (option['name']?option['name']:'')}
                                            value={userFirstGroup || null}
                                            onChange={(event, value) => {
                                            if (value) {
                                                setUserFirstGroup(value);
                                            }}}
                                            className="autocomplete"
                                            //   defaultValue={}
                                            renderInput={(params) => (<TextField {...params} className="p-0 m-0 h-0" name="group" label="" variant="outlined" fullWidth />)}
                                        />
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label>Password </label>
                                        <input type="password" name="password" className="form-control" value={password}  onChange={e => setPassword(e.target.value)} />
                                    </div>
                                    <div className="form-group col-md-6">
                                        <label>Re-Password </label>
                                        <input type="password" name="repassword" className="form-control" value={rePassword}  onChange={e => setRePassword(e.target.value)} />
                                    </div>
                              
                                </div>
                                <button type="submit" className="float-right btn btn-primary">
                                    Confirmer la modification
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </>
        </div>

    )
}
export default UserDetail;




