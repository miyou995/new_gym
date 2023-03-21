import React, { useState, useCallback, useEffect } from "react";
import { Button, Modal } from "react-bootstrap";

import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";

const DoorModal = ({show, onShowChange, doorData}) => {
    const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])
  const api = useAxios();
  // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const postDoorEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/door/`
    const putDoorEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/door/${doorData['doorId']}/`
    // const salleActivitiesEND = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/`

    const [doorId, setDoorId] = useState('')
    const [doorIp, setDoorIp] = useState('')
    
    const [salle, setSalle] = useState('')
    const [showForm, setShowForm] = useState(false)

    const [doorUsername, setDoorUsername] = useState('')
    const [doorPassword, setDoorPassword] = useState('')
    const [salles, setSalles] = useState([])
    // const [salllesActivities, setSalllesActivities] = useState([]);

    // useEffect(() => {
    //     api.get(salleActivitiesEND).then(res =>{
    //         setSalllesActivities(res.data)
    //     })
    // }, [salleActivitiesEND]);
    const openTheDoor = () => {
        // e.preventDefault();
        api.get(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/openthedoor/${doorData['doorId']}/`).then(res => {
            if (res.status === 200) {
                notifySuccess(`La porte de la salle ${doorData['salleName']} a été ouverte avec succés`)
                handleShow()
            }else {
                notifyError(`La porte de la salle ${doorData['salleName']} n'a pas été ouverte `)
            }
        }).catch(err => {
            notifyError(`La porte de la salle ${doorData['salleName']} n'a pas été ouverte `)
        })
    }
    useEffect(() => {
        setDoorId(doorData['doorId'])
        setDoorIp(doorData['doorIp'])
        setSalle(doorData['doorSalle'])
        setDoorUsername(doorData['doorUsername'])
        setDoorPassword(doorData['doorPassword'])
        setSalles(doorData['salllesActivities'])
        setShowForm(true)
        console.log("LES SALLES DACTIVITE SUR LE DOOR MODAL ", doorData['salllesActivities']);
        console.log('id de la porte ',doorData['doorId'] , 'new one ',salle  );
        console.log("REAL SALLES", salles);

    }, [doorData, show]);
    const selectValue = evt => {
        const { value } = evt.target;
        console.log("VALUE SELECTED", value);
        console.log("VALUE SELECTED TYPE", typeof(value));
        const item = salles.find(item => item.id === Number(value));
        console.log("THE ITEM%", item);
        setSalle(item.id);
        console.log(item.id);
        // setSelectedValue(value);
      };
    const HandleSubmit = e => {
        e.preventDefault();
        const doorData = {
            ip_adress :doorIp,
            salle     :Number(salle),
            username  :doorUsername,
            password  :doorPassword,
        }
        if( doorId ){
            doorData.id = doorId
            api.put(putDoorEnd, doorData).then( res => {
                notifySuccess('Porte modifier avec succés')
                    handleShow()
                }).catch(err => {
                    notifyError("Erreur lors de la modification de la porte")
                })
                console.log(' door data', doorData);
        }else {
            api.post(postDoorEnd, doorData).then( res => {
                notifySuccess('Porte Créer avec succés')
                    handleShow()
                }).catch(err => {
                    notifyError("Erreur lors de la modification de la porte")
                })
                console.log('post door data', doorData);
        }
    }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Modifier / Creer Porte {doorData['maladieName']}</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
        {
            showForm &&
            <form onSubmit={HandleSubmit}>
                    <div className="form-group row">
                    <label className="col-sm-3 col-form-label">Salle </label>
                    <div className="col-sm-9">
                            <select
                            defaultValue={doorData['doorSalle']}
                            className="form-control"
                            id="selectSalle"
                            onChange={selectValue}>
                                <option hidden value="">Sélectionner une salle</option>
                                {/* <option selected disabled hidden>Salle</option> */}
                            {
                                salles.map(salle =>(
                                    <option key={salle.id} value={salle.id}>{salle.name}</option>
                                ))
                            }
                            </select>
                        {/* <Autocomplete
                            onChange={((event, value) =>  {
                                setDoor(value.id)
                            }
                                )} 
                            //   value={salles}
                            options={doorData['doors']}
                            getOptionSelected={(option) =>  option['id']}

                            id="size-small-standard-multi"
                            getOptionLabel={(option) =>  ( option['ip_adress'])}
                            renderInput={(params) =>
                        (<TextField {...params} name="door" label="Porte" variant="outlined" fullWidth />)}
                        /> */}
                    </div>
                </div>
                <div className="form-group row">
                    <label className="col-sm-3 col-form-label">Adresse IP  </label>
                    <div className="col-sm-9">
                        <input type="text" value={doorIp} className="form-control" placeholder="..." onChange={e => setDoorIp(e.target.value)}/>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="col-sm-3 col-form-label">Username  </label>
                    <div className="col-sm-9">
                        <input type="text" value={doorUsername} className="form-control" placeholder="..." onChange={e => setDoorUsername(e.target.value)}/>
                    </div>
                </div>
                <div className="form-group row">
                    <label className="col-sm-3 col-form-label">Password</label>
                    <div className="col-sm-9">
                        <input type="text" value={doorPassword} className="form-control" placeholder="..." onChange={e => setDoorPassword(e.target.value)}/>
                    </div>
                </div>

                <div className="form-group row d-flex justify-content-between">
                    <div className="m-3">
                        <button type="submit" className="btn btn-primary">
                            Valider
                        </button>
                    </div>
                    <div className="m-3">
                        <button type="button" className="btn btn-success" onClick={e => openTheDoor()}>
                            Ouvrir
                        </button>
                    </div>
                    <div className="m-3">
                        <button type="button" className="btn btn-danger" onClick={ async () => {
                        await api.delete(putDoorEnd)
                        notifySuccess(`La porte ${doorData['doorIp']} a été supprimer avec succés`)
                        handleShow()
                        }}>Supprimer</button>
                    </div>
                </div>
            </form>

        }
     </Modal.Body>
    </Modal>
)}

export default DoorModal;