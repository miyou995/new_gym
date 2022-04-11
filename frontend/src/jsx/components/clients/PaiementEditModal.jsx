import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Table } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import PageTitle from "../../layouts/PageTitle";
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";

function refreshPage() {
  window.location.reload(false);
}

const PaiementEditModal = ({show, onShowShange, paiementData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    const clientId = paiementData['clientId']
    const abonnements = paiementData['abcs']

    const amountInfo = paiementData['paiementAmountInfo']
    const aBC = paiementData['paiementABCInfo']
    const date = paiementData['paiementDateInfo']

    const [amount, setAmount] = useState("")
    const [erreur, seterreur] = useState(false)
    const [abcId, setAbcId] = useState([])
    
    // const [abc, setAbc] = useState([])
    const [note, setNote] = useState("")
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)
    const [paiementIdReceived, setPaiementIdReceived] = useState("");
    const [paiementAmountReceived, setPaiementAmountReceived] = useState("");
    const [paiementABCReceived, setPaiementABCReceived] = useState("");
    const [paiementDateReceived, setPaiementDateReceived] = useState("");
   const [paiementABCNameReceived, setPaiementABCNameReceived] = useState("");
   const [selectedAbc, setSelectedAbc] = useState("");
    
    console.log('Paimeent selectedAbc',selectedAbc)
    console.log('Paimeent paiementDatpaiementABCInfo]',paiementData['paiementABCInfo'])
    const paiementCreateEND =`${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/${paiementIdReceived}/` 
    const paiementDeleteEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/delete/${paiementIdReceived}/`

    useEffect(() => {
      if (show == true) {
            setPaiementIdReceived(paiementData['paiementIdInfo'])
            setAmount(paiementData['paiementAmountInfo'])
            setPaiementABCReceived(paiementData['paiementABCInfo'])
            setPaiementDateReceived(paiementData['paiementDateInfo'])
            setNote(paiementData['paiementNotesInfo'])
            setPaiementABCNameReceived(paiementData['paiementABCName'])
            setSelectedAbc(abonnements[abonnements.findIndex(x => x.id == paiementData['paiementABCInfo'])])
          }

    }, [show, paiementData['paiementIdInfo']])
    
    const notifySuccess = () => {
      toast.success('Paiement  Modifier Avec Succée', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      })
    }
  const notifyError = () => {
      toast.error('Echec de Modification paiement', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      })
    }
    useEffect(() => {
      if (error == true) {
        notifyError()
      }
    }, [error]);
    useEffect(() => {
      if (success == true) {
        notifySuccess()
      }
    }, [success]);

    const handleDelete = e => {
      axios.delete().then(
          // refreshPage(),
          handleShow()
      )
  }
  
    const handleSubmit = async e => {
      e.preventDefault();
        const paiementDetails = {
          // abonnement_client :Number(abcId),
          note : note,
          date : paiementDateReceived
        }
        console.log(" =================> new Creneau ", paiementDetails);
        try {
         await axios.patch(paiementCreateEND, paiementDetails).then(res => {
           if (res.status === 200) {
             setSuccess(true)
             handleShow()
           }
         })
        } catch (error) {
          setError(true)
        }
        // refreshPage()
        // setCreneaux([])
        // handleShow()
      }
return ( 
    <Modal  className="fade bd-example-modal-lg" size="xl" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title> paiement de : {clientId}</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
    <form onSubmit={handleSubmit}>
        <div className="row">
          <div className="form-group col-md-6">
            <TextField type="text" value={paiementABCNameReceived} fullWidth  disabled/>
          </div>
          <div className="form-group col-md-6">
            <TextField type="number" value={amount} fullWidth  disabled/>
          </div>
          <div className="form-group col-12 col-md-6">
              <TextField
                type="date"
                onChange={e=> setPaiementDateReceived(e.currentTarget.value)}
                defaultValue={date}
                variant="outlined"
                label="Date"
                fullWidth
              />
          </div>
          <div className="form-group col-12 col-md-6">
              <TextField
                type="text"
                onChange={e=> setNote(e.currentTarget.value)}
                value={note}
                variant="outlined"
                label="Notes"
                fullWidth
              />
          </div>
        </div>
        <div className="row justify-content-between">
          <div className='col-9'>

            <Button onClick={handleShow} variant="danger light" > Fermer </Button>
            <Button variant="primary" type="submit">Valider</Button>
          </div>
        <div className='col-3'>
                {/* <Button variant="primary" type="submit">Supprimer</Button> */}
                <Button type="button" className="btn btn-danger" onClick={ async () => {
                await axios.delete(paiementDeleteEND)
                handleShow()
                }}>
                    Supprimer
                </Button>
            </div>
        </div>
      </form>
     </Modal.Body>
    </Modal>
)}
export default PaiementEditModal;