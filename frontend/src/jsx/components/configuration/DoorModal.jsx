import React, { useState, useCallback, useEffect } from "react";
import { Button, Modal } from "react-bootstrap";

import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";

const DoorModal = ({show, onShowShange, doorData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
  const api = useAxios();
  // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const postDoorEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/door/`
    const putDoorEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/door/${doorData['doorId']}/`
    const [doorId, setDoorId] = useState('')
    const [doorIp, setDoorIp] = useState('')
    const [doorUsername, setDoorUsername] = useState('')
    const [doorPassword, setDoorPassword] = useState('')

    useEffect(() => {
      if (show == true) {
        setDoorId(doorData['doorId'])
        setDoorIp(doorData['doorIp'])
        setDoorUsername(doorData['doorUsername'])
        setDoorPassword(doorData['doorPassword'])
        console.log('id de la porte ',doorId , 'new one ',doorData['doorId']  );
      }
    }, [doorData['doorId'], show]);
    const HandleSubmit = e => {
        e.preventDefault();
        const doorData = {
            ip_adress :doorIp,
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
      <form onSubmit={HandleSubmit}>
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
                <button type="button" className="btn btn-danger" onClick={ async () => {
                await api.delete(putDoorEnd)
                notifySuccess(`La porte ${doorData['doorIp']} a été supprimer avec succés`)
                handleShow()
                }}>Supprimer</button>
            </div>
          </div>
      </form>
     </Modal.Body>
    </Modal>
)}

export default DoorModal;