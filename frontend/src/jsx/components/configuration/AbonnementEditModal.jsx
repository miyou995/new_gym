import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import PageTitle from "../../layouts/PageTitle";
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
import createPalette from "@material-ui/core/styles/createPalette";
import {notifySuccess, notifyError} from '../Alert'

function refreshPage() {
  window.location.reload(false);
}

const AbonnementEditModal = ({show, onShowShange, abonnementData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    // const abonnementEditEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    // const creneauPerAbonnementEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`

const [name, setName] = useState('')
const [price, setPrice] = useState('')
const [numberOfDays, setNumberOfDays] = useState('')
const [seancesQuantity, setSeancesQuantity] = useState('')
const [activity, setActivity] = useState([])
const [systemeCochage, setSystemeCochage] = useState(false)

const [numOfWeek, setNumOfWeek] = useState("")
const [AlertSuccess, setAlertSuccess] = useState(false);
const [AlertError, setAlertError] = useState(false);
const [abonnementId, setAbonnementId] = useState();
const [abonnementDetail, setAbonnementDetail] = useState();
const [selectedActivities, setSelectedActivities] = useState([])
const [abnIndex, setAbnIndex] = useState([])
const [showModal, setShowModal]  = useState(false)
const [duree, setDuree] = useState('')

const abonnementEditEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/${abonnementData['abonnementId']}/`
const abonnementDeleteEND = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/delete/${abonnementData['abonnementId']}/`
// setSelectedActivities(abonnementData['selectedActivities'])
// const provArray = []

const DureeAb = [
  {mois :'1 Jour', jours : 1},
  {mois :'15 Jour', jours : 15},
  {mois :'45 Jour', jours : 45},
  {mois :'1 mois', jours : 30},
  {mois :'2 mois', jours : 60},
  {mois :'3 mois', jours : 90},
  {mois :'4 mois', jours : 120},
  {mois :'6 mois', jours : 180},
  {mois :'12 mois', jours : 360},
]

useEffect(() => {
    if (selectedActivities !== [] ) {
     setShowModal(true)   
    }
  if (show == true) {
    axios.get(abonnementEditEND).then(  res => {
      setName(res.data.name)
      setPrice(res.data.price)
      setNumberOfDays(res.data.number_of_days)
      setSeancesQuantity(res.data.seances_quantity)
      setSystemeCochage(res.data.systeme_cochage)
      setAbnIndex(abonnementData['dureeInd'])
      setActivity(abonnementData['selectedActivities'])
    })
  }
}, [abonnementData['abonnementId']]);
    const handleDelete = e => {
        axios.delete(abonnementDeleteEND).then(
            // refreshPage(),
            notifySuccess('Abonnement supprimé'),
            handleShow()
        )
    }
    const handleSubmit = async e => {
      e.preventDefault();
        for (let i = 0; i < activity.length; i++) {
            selectedActivities.push(activity[i]['id'])
        }
        const abonnementFormData = {
          name              : name,
          price             : price,
          seances_quantity  : Number(seancesQuantity),
          salles          : selectedActivities,
          systeme_cochage : systemeCochage,
          number_of_days    : Number(duree)
      }
      const response = await axios.put(abonnementEditEND, abonnementFormData).then(res => {
            setSelectedActivities([])
            notifySuccess('Modifictation de labonnement effectué')
            handleShow()
          } ).catch( err => {
            notifyError('erreur de modification')
         })
    }


return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black'>{name}</Modal.Title>
      <Button
          variant=""
          className="close"
          onClick={handleShow}
          >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={handleSubmit}>
          <div className="form-group row">
          <label className="col-sm-3 col-form-label">Systeme d'abonnement : </label>
              <div className="col-sm-9">
                <FormControlLabel
                    control={<Switch checked={systemeCochage}   color="primary" />}
                    label={systemeCochage ? 'Prépayé ': 'Normal'}
                    labelPlacement={systemeCochage ? 'end': 'start'}
                    />
              </div>
              <label className="col-sm-3 col-form-label">Nom </label>
              <div className="col-sm-9">
                  <input type="text" value={name} className="form-control" placeholder="..." onChange={e => setName(e.target.value)}/>
              </div>
          </div>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Prix </label>
              <div className="col-sm-9">
                  <input type="number"value={price} className="form-control" placeholder="..." onChange={e => setPrice(e.target.value)}/>
              </div>
          </div>
       
            <div className="form-group row">
                    <label className="col-sm-3 col-form-label">Durée </label>
                <div className="form-group col-sm-9">
                    <Autocomplete
                        onChange={(event, value) => 
                        {
                            try {
                            setDuree(value.jours)
                        } catch (error) {
                            setDuree('')
                        }}
                        }
                        defaultValue={DureeAb[abonnementData['dureeInd']]}
                        options={DureeAb}
                        getOptionLabel={(option) =>  option['mois']}
                        renderInput={(params) => <TextField {...params} label="Mois" variant="outlined" />}
                        />
                </div>
            </div>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Nombre de Séances </label>
              <div className="col-sm-9">
                  <input type="number"value={seancesQuantity} className="form-control" placeholder="..." onChange={e => setSeancesQuantity(e.target.value)}/>
              </div>
          </div>
          <div className="form-group row">
              <label className="col-sm-3 col-form-label">Salles </label>
              <div className="col-sm-9">
                  <Autocomplete
                      multiple
                      onChange={((event, value) =>  
                        {
                        setActivity(value)
                        console.log('the valueee', value);
                    }
                        )} 
                      value={activity}
                      options={abonnementData['salles']}
                      id="size-small-standard-multi"
                      getOptionLabel={(option) =>  ( option['name'])}
                      renderInput={(params) =>
                  (<TextField {...params} name="salles" label="Salles" variant="outlined" fullWidth />)}
                />
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
                    await axios.get(`${process.env.REACT_APP_API_URL}/rest-api/abonnement/deativate/${abonnementData['abonnementId']}/`)
                    handleShow()
                    }}>Supprimer</button>
                </div>
          </div>
      </form>
     </Modal.Body>

    </Modal>
)

}
export default AbonnementEditModal;