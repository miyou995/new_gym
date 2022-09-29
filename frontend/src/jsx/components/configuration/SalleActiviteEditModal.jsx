import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";

import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
import createPalette from "@material-ui/core/styles/createPalette";
function refreshPage() {
  window.location.reload(false);
}
const SalleActiviteEditModal = ({show, onShowShange, salleData}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const salleActiviteUpdateEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/${salleData['salleId']}/`
    const doors = salleData['doors']
    const selectedDoor  = salleData['doorId']
    const [name, setName] = useState('')

    const [is_default, setDefault] = useState(false)
    const [door, setDoor] = useState([])


    //console.log('doors doors', doors);
    //console.log('selected DOOR', salleData['doorId']);

    useEffect(() => {
    if (show == true) {
        setName(salleData['salleName'])
        setDefault(salleData['isDefaultSalle'])
    }
    }, [salleData['salleId']]);
    const HandleSubmit = e => {
        e.preventDefault();
        const salleFormData = {
            name : name,
            door : Number(door),
            is_default : is_default
        }
        console.log(" =================> salleFormData ", salleFormData);
        api.put(salleActiviteUpdateEnd, salleFormData).then( res => {
            notifySuccess('Salle modifier avec succés')
                handleShow()
            }).catch(err => {
                notifyError("Erreur lors de la modification de la salle")
            })
      } 
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer un nouvel abonnement </Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={HandleSubmit}>
            <div className="form-group row">
                <label className="col-sm-3 col-form-label">Nom  </label>
                <div className="col-sm-9">
                    <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
                </div>
            </div>
            <div className="form-group row">
              <label className="col-sm-3 col-form-label">Salle </label>
              <div className="col-sm-9">
                  <Autocomplete
                      onChange={((event, value) =>  {
                        setDoor(value.id)
                    }
                        )} 
                    //   value={salles}
                      options={salleData['doors']}
                      defaultValue={doors[selectedDoor]}
                      getOptionSelected={(option) =>  option['id']}

                      id="size-small-standard-multi"
                      getOptionLabel={(option) =>  ( option['ip_adress'])}
                      renderInput={(params) =>
                  (<TextField {...params} name="door" label="Porte" variant="outlined" fullWidth />)}
                />
              </div>
            </div>
            <div className="form-group row">
                <FormControlLabel
                    control={
                        <Checkbox 
                            checked={is_default}
                            onChange={e=> {
                            setDefault(!is_default)
                                //console.log('target value', e.target.value);
                            }}
                            name="checkedB"
                            color="primary"
                        />
                    }
                    label="Salle par défaut"
                />
            </div>
          
          <div className="form-group row d-flex justify-content-between">
            <div className="m-3">
                <button type="submit" className="btn btn-primary">
                    Valider
                </button>
            </div>
            <div className="m-3">
                <button type="button" className="btn btn-danger" onClick={ async () => {
                await api.delete(`${process.env.REACT_APP_API_URL}/rest-api/salle-activite/delete/${salleData['salleId']}/`)
                notifySuccess(`La salle ${salleData['salleName']} a été supprimer avec succés`)
                handleShow()
                }}>
                    Supprimer
                </button>
            </div>
          </div>
      </form>
     </Modal.Body>
    </Modal>
)}

export default SalleActiviteEditModal;