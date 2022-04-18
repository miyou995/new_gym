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
import useForm from 'react-hook-form';
import createPalette from "@material-ui/core/styles/createPalette";

const SalleActiviteCreateModal = ({show, onShowShange}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    const salleActiviteCreateEnd = `${process.env.REACT_APP_API_URL}/rest-api/salle-activite/create`

const [name, setName] = useState('')
const [price, setPrice] = useState('')
const [numberOfDays, setNumberOfDays] = useState('')
const [seancesQuantity, setSeancesQuantity] = useState('')
const [activity, setActivity] = useState([])
const [selectedActivities, setSelectedActivities] = useState([])
const [is_default, setDefault] = useState(false)

    const HandleSubmit = async e => {
        e.preventDefault();
        const ebonnementFormData = {
            name : name,
            is_default : is_default,
        }
        await axios.post(salleActiviteCreateEnd, ebonnementFormData).then( res => {
            notifySuccess('Salle creer avec succés')
                  handleShow()
            }).catch(err => {
              notifyError("Erreur lors de la creation de la salle")
            })
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>Creer un nouvel abonnement </Modal.Title>
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
                label="Salle par défaut"
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
export default SalleActiviteCreateModal;