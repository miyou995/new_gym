import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";

import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import { Dropdown, Tab, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
import {notifySuccess, notifyError} from '../Alert'
 

const AssuranceCreateModal = ({show, onShowShange}) => {
  const api = useAxios();
  const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])
    let clientEnd = `${process.env.REACT_APP_API_URL}/rest-api/clients-name/`
    let assuranceEnd = `${process.env.REACT_APP_API_URL}/rest-api/assurance/`
  const [clients, setClients] = useState([])
  const [assurance, setAssurance] = useState([])
  useEffect(() => {
    api.get(clientEnd).then((res) => {
      setClients(res.data)
    })
    api.get(assuranceEnd).then((res) => {
      setAssurance(res.data)
    })
  }, []);
    // const history = useHistory();
    const [amount, setAmount] = useState("");
    const [notes, setNotes] = useState("");
    const [type, setType] = useState("");
    const [client, setClient] = useState("");

    const HandleSubmit = async e => {
      e.preventDefault();
    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/transactions/assurance/create`

      const newTransaction = {
        amount : amount ,
        notes : notes ,
        // type : type ,
        client : client
        }
        await api.post(endpoint, newTransaction).then( res => {
          notifySuccess('Transaction creer avec succés')
                handleShow()
          }).catch(err => {
            notifyError("Erreur lors de la creation de la transaction")
          })
    }
return ( 

    <Modal className="fade bd-example-modal-lg" size="lg"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title>Creneau</Modal.Title>
      <Button variant="" className="close" onClick={handleShow} >
          <span>&times;</span>
      </Button>
    </Modal.Header>
    <Modal.Body>
      
    <form onSubmit={HandleSubmit}>
                                 <div className="form-row">
                                    <div className="form-group col-md-6">
                                      <Autocomplete
                                        // id={(option) =>  option['id']}
                                        onChange={(event, value) => setClient(value.id)}
                                        // onChange={handleSubmit}
                                        options={clients.results}
                                       //  value={activities[creneauActivite]}
                                        getOptionSelected={(option) =>  option['id']}
                                        getOptionLabel={(option) =>  option['last_name']}
                                        renderInput={(params) => <TextField {...params}  label="Client" variant="outlined" fullWidth />}
                                      />
                                    </div>

                                    <div className="form-group col-md-6">
                                    <TextField type="number" label="Montant" variant="outlined" onChange={e=> setAmount(e.currentTarget.value)} fullWidth />
                                    </div>
                                    <div className="form-group col-md-6">
                                    <TextField type="text" onChange={e=> setNotes(e.currentTarget.value)} variant="outlined" label="Note" fullWidth />
                                    </div>
                                  </div>
                                 <Button onClick={handleShow}variant="danger light"className='m-2'>Annulé</Button>
                                  <Button variant="primary" type="submit">Confirmer</Button>
                                  </form>
     </Modal.Body>




     


    </Modal>
)

}
export default AssuranceCreateModal;