import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
 
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
// import { Dropdown, Tab, Nav } from "react-bootstrap";
// import { Link } from "react-router-dom";
import useForm from 'react-hook-form';
import {notifySuccess, notifyError} from '../Alert'
import useAxios from "../useAxios";

const PaiementCreateModal = ({show, onShowShange}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    const api = useAxios();

    // const {register, handleSubmit, errors } = useForm();

    let paiementCreateEnd = `${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/create`
    // let abonnementTypeEnd = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    let clientsEnd = `${process.env.REACT_APP_API_URL}/rest-api/clients-name-drop/`

   const [abc, setAbc] = useState([])
   const [abcId, setAbcId] = useState([])
   const [client, setClient] = useState("")
   const [clients, setClients] = useState("")
   const [dettes, showDettes] = useState(false)
   const [erreur, seterreur] = useState(false)
   const [amount, setAmount] = useState("");
   const [clientId, setClientId] = useState("");
   
  //  const [abonnement, setAbonnement] = useState("")
   const [note, setNote] = useState("")
  //  const clients = useGetAPI(clientsEnd)

    useEffect(() => {
       const fetchData = async () => {
          try {
             const res = await api.get(clientsEnd);
             setClients(res.data)
            //  console.log('les clizents ???', res.data.results);
          } catch (error) {
             console.log(error);
          }
       }
       fetchData();
    }, [] );
    useEffect(() => {
      if (show == true) {
        
        const fetchData = async () => {
           try {
              const res = await api.get(`${process.env.REACT_APP_API_URL}/rest-api/abonnement-by-client/?cl=${clientId}`);
              setAbc(res.data)
              console.log('ceci est le resultat de labonnement client ', res.data);
           } catch (error) {
              console.log(error);
           }
        }
        fetchData();
      }
    }, [clientId] );
    const handleSubmit =async e => {
      e.preventDefault();
      const newTransaction = {
        amount : amount ,
        abonnement_client: Number(abcId),
        // type : Number(abonnement),
        note : note
      }
      await api.post(paiementCreateEnd, newTransaction).then( res => {
        notifySuccess('Paiement creer avec succés')
              handleShow()
        }).catch(err => {
          notifyError("Erreur lors de la creation de la Paiement")
        })
      }

return ( 

  <Modal className="fade bd-example-modal-lg" size="lg"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title>Paiement</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} > <span>&times;</span></Button>
    </Modal.Header>
    <Modal.Body>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group col-md-6">
            <Autocomplete
              onChange={((event, value) =>  {
                try {
                  setClientId(value.id)
                  seterreur(false)
                  showDettes(true)
                } catch (error) {
                  setClientId('')
                  seterreur(true)
                }
              })}
              options={clients}
              getOptionSelected={(option) =>  option['id']}
              getOptionLabel={(option) =>  (  option['id'] +' - '+ option['last_name'])}
              renderInput={(params) => 
                <TextField {...params}  label="Clients" variant="outlined" fullWidth required />}
            />
            {erreur && <p style={{color:'red'}}>veuillez choisir un client pour le paiement</p>}
              
          </div>
          <div className="form-group col-md-6">
            <Autocomplete
              onChange={((event, value) =>  {
                try {
                  setAbcId(value.id)
                  seterreur(false)
                  showDettes(true)
                } catch (error) {
                  setAbcId('')
                  seterreur(true)
                }
              })}
              options={abc}
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
            label="Montant"
            variant="outlined"
            onChange={e=> setAmount(e.currentTarget.value)}
            fullWidth
          />
          </div>
          <div className="form-group col-md-6">
          <TextField
            type="text"
            onChange={e=> setNote(e.currentTarget.value)}
            variant="outlined"
            label="Note"
            fullWidth
          />
          </div>
        </div>
        <Button onClick={handleShow} variant="danger light" className='m-2' > Annulé </Button>
        <Button variant="primary" type="submit">Confirmer</Button>
        </form>
    </Modal.Body>
  </Modal>
)
}
export default PaiementCreateModal;