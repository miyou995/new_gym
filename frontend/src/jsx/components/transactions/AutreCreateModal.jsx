import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import { Dropdown, Tab, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
 
function refreshPage() {
  window.location.reload(false);
}
const AutreCreateModal = ({show, onShowShange, transactionData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])

    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/transactions/autre/create`

   const [people, setPeople] = useState([])
  //  const [client, setClient] = useState("")
   const [nom, setNom] = useState("")
  const [amount, setAmount] = useState("");

   const [note, setNote] = useState("")

  const handleSubmit = async e => {
      e.preventDefault();
      const newTransaction = {
        amount: amount,
        name :nom,
        notes : note
      }
     await axios.post(endpoint, newTransaction)
      // refreshPage()
      handleShow()
    }
  console.log('creneaux detail');

return ( 

    <Modal className="fade bd-example-modal-lg" size="lg"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title>Autre Transaction</Modal.Title>
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
                                 <div className="form-row">
                                    
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
                                    <div className="form-group col-md-6">
                                      <TextField
                                        type="text"
                                        onChange={e=> setNom(e.currentTarget.value)}

                                      //   defaultValue={endHour}
                                        // value={creneauDetail.hour_finish}
                                        // className={classes.textField}
                                        variant="outlined"
                                        label="Libellé"

                                        fullWidth
                                        // defaultValue={coachs[coach]}
                                      //   onChange={e => setNewEndHour(e.currentTarget.value)}
                                      />
                                    </div>
                                    <div className="form-group col-md-6">
                                      <TextField
                                        type="text"
                                        onChange={e=> setNote(e.currentTarget.value)}

                                      //   defaultValue={endHour}
                                        // value={creneauDetail.hour_finish}
                                        // className={classes.textField}
                                        variant="outlined"
                                        label="Note"

                                        fullWidth
                                        // defaultValue={coachs[coach]}
                                      //   onChange={e => setNewEndHour(e.currentTarget.value)}
                                      />
                                    </div>
                                  </div>
                                 <Button
                                      onClick={handleShow}
                                      variant="danger light"
                                      className='m-2'
                                      >
                                      Annulé
                                  </Button>
                                  <Button variant="primary" type="submit">Confirmer</Button>
                                  </form>
     </Modal.Body>




     


    </Modal>
)

}
export default AutreCreateModal;