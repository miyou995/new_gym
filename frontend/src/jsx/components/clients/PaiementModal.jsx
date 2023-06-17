import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import PageTitle from "../../layouts/PageTitle";

import {notifySuccess, notifyError} from '../Alert'
import useAxios from "../useAxios";

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";

function refreshPage() {
  window.location.reload(false);
}
const formatDate = (date) => {
  return new Date(date).toISOString().slice(0, 10)
}
const PaiementModal = ({show, onShowChange, clientData}) => {
    const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])
  const api = useAxios();
  const clientId = clientData['clientId']
    const abonnements = clientData['abcs']
    const paiementCreateEND =`${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/create` 
    const [amount, setAmount] = useState("")
    const [erreur, seterreur] = useState(false)
    const [abcId, setAbcId] = useState([])
    const [dateCreation, setDateCreation] = useState(formatDate(new Date()))
    const [note, setNote] = useState("")
    // const [error, setError] = useState(false)
    // const [success, setSuccess] = useState(false)
    
    // useEffect(() => {
    //   if (show == true) {
        
    //     const fetchData = async () => {
    //        try {
    //           const res = await api.get(`${process.env.REACT_APP_API_URL}/rest-api/abonnement-by-client/?cl=${clientId}`);
    //           setAbc(res.data)
    //           //console.log('ceci est le resultat de labonnement client ', res.data);
    //        } catch (error) {
    //           console.log(error);
    //        }
    //     }
    //     fetchData();
    //   }
    // }, [clientId] );
  //   const notifySuccess = () => {
  //     toast.success('Paiement  effectuer Avec Succée', {
  //       position: 'top-right',
  //       autoClose: 5000,
  //       closeOnClick: true,
  //       pauseOnHover: true,
  //       draggable: true,
  //     })
  //   }
  // const notifyError = () => {
  //     toast.error('Echec de paiement', {
  //       position: 'top-right',
  //       autoClose: 5000,
  //       hideProgressBar: false,
  //       closeOnClick: true,
  //       pauseOnHover: true,
  //       draggable: true,
  //     })
  //   }
  //   useEffect(() => {
  //     if (error == true) {
  //       notifyError()
  //     }
  //   }, [error]);
  //   useEffect(() => {
  //     if (success == true) {
  //       notifySuccess()
  //     }
  //   }, [success]);

    const handleSubmit = async e => {
      e.preventDefault();
        const paiementDetails = {
          abonnement_client :Number(abcId),
          amount : amount,
          notes : note,
          date_creation : dateCreation
        }
        console.log(" =================> new Creneau ", paiementDetails);
        try {
          await api.post(paiementCreateEND, paiementDetails)
          notifySuccess('Paiement effectuer avec succés')
          handleShow()
        } catch (error) {
           notifyError("Echec de paiement")
            //console.log('je suis la ', error);
        }

      }
return ( 

    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black font-weight-bold'>Creer un nouveau paiement pour : {clientId}</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
    <form onSubmit={handleSubmit}>
        <div className="row">
          <div className="form-group col-md-6">
            <Autocomplete
              // id={(option) =>  option['id']}
              onChange={((event, value) =>  {
                try {
                  setAbcId(value.id)
                  seterreur(false)
                } catch (error) {
                  setAbcId('')
                  seterreur(true)
                }
              })}
              // onChange={handleSubmit}
              options={abonnements}
              //  value={activities[creneauActivite]}
              getOptionSelected={(option) =>  option['id']}
              getOptionLabel={(option) =>  option['type_abonnement_name']}
              renderInput={(params) => 
                <TextField {...params}  label="Abonnements" variant="outlined" fullWidth required />}
            />
            {erreur && <p style={{color:'red'}}>veuillez choisir un abonnement du client</p>}
          </div>

          <div className="form-group col-md-6">
            <TextField
                type="number"
              //   defaultValue={}
                label="Montant"
                variant="outlined"
                onChange={e=> setAmount(e.currentTarget.value)}
                // onChange={(event, value) => setNewStartHour(value)}
                fullWidth
              />
          </div>
          <div className="form-group col- col-md-6">
              <TextField type="date" value={dateCreation} onChange={e=> setDateCreation(e.currentTarget.value)} variant="outlined" label="Date"fullWidth  />
              </div>
            <div className="form-group col- col-md-6">
              <TextField type="text" onChange={e=> setNote(e.currentTarget.value)} variant="outlined" label="Note"fullWidth  />
              </div>
        </div>
        <Button onClick={handleShow} variant="danger light" className='m-2' > Fermer </Button>
        <Button variant="primary" type="submit">Valider</Button>
      </form>
     </Modal.Body>
    </Modal>
)}
export default PaiementModal;