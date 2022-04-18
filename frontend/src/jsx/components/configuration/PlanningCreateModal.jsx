import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI, usePostAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import PageTitle from "../../layouts/PageTitle";
import {notifySuccess, notifyError} from '../Alert'
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
// import useForm from 'react-hook-form';
// import createPalette from "@material-ui/core/styles/createPalette";

const PlanningCreateModal = ({show, onShowShange}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const planningCreateEnd = `${process.env.REACT_APP_API_URL}/rest-api/planning/create`

const [name, setName] = useState('')
const [is_default, setDefault] = useState(false)
    const HandleSubmit = async e => {
        e.preventDefault();
        const ebonnementFormData = {
            name : name,
            is_default : is_default
            // salle_sport : 1
        }
        await axios.post(planningCreateEnd, ebonnementFormData).then( res => {
                notifySuccess('Planning creer avec succés')
                handleShow()
            }).catch(err => {
                notifyError("Erreur lors de la modification du planning")
            })
        // refreshPage()
        handleShow()
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer un nouveau Planning </Modal.Title>
      <Button
          variant=""
          className="close"
          onClick={handleShow}
          >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={HandleSubmit}>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Nom </label>
              <div className="col-sm-9">
                  <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
              </div>
          </div>
          <div className="form-group row">
              <FormControlLabel
                control={
                    <Checkbox 
                        checked={is_default}
                        onChange={e=> {
                        setDefault(!is_default)
                            console.log('target value', e.target.value);
                        }}

                        name="checkedB"
                        color="primary"
                    />
                }
                label="Planning par défaut"
            />
          </div>
          

          <div className="form-group row">
              <div className="col-sm-10">
                  <button type="submit" className="btn btn-primary">
                      Valider
                  </button>
              </div>
          </div>
      </form>
     </Modal.Body>

    </Modal>
)

}
export default PlanningCreateModal;