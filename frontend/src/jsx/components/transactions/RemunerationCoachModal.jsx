import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import { useGetAPI, usePutAPI } from '../useAPI'
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import axios from 'axios';
import { Dropdown, Tab, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
import {notifySuccess, notifyError} from '../Alert'
 
function refreshPage() {
  window.location.reload(false);
}
const RemunerationCoachModal = ({show, onShowShange, transactionData}) => {
    const handleShow = useCallback( () => {onShowShange(false)}, [onShowShange])


    let paiementCreateEnd = `${process.env.REACT_APP_API_URL}/rest-api/transactions/remunerationProf/create`
    // let abonnementTypeEnd = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
    let coachsEnd = `${process.env.REACT_APP_API_URL}/rest-api/coachs/`

   const [coach, setCoach] = useState("")
   const [note, setNote] = useState("")
   const [amount, setAmount] = useState("")
   const coachs = useGetAPI(coachsEnd)
  //  const abonnements = useGetAPI(abonnementTypeEnd)
   //  useEffect(() => {
         // setPeople(clients)
      //   console.log('THE NEW CLIENT ONEEE ', res.data);

      //   setCreneauDetail(res.data)
      //   console.log(res.data);
      //   setNewActivity(activities[creneauActivite].id)
      //   setNewCoach(coachs[creneauCoach].id)
      //   setNewStartHour(startHour)
      //   setNewEndHour(endHour)
      //   setNewDay(days[day].day)
      //   setNewPlanning(plannings[creneauPlanning].id)
       
   //  }, [])

    // }, [transactionData['creneauId']]);
    const handleSubmit =async e => {
      e.preventDefault();
      const newTransaction = {
         coach: Number(coach),
         amount:amount,
         notes : note
      }
      await axios.post(paiementCreateEnd, newTransaction).then( res => {
        notifySuccess('Transaction creer avec succés')
              handleShow()
        }).catch(err => {
          notifyError("Erreur lors de la creation de la transaction")
        })
  }

return ( 

    <Modal className="fade bd-example-modal-lg" size="lg"onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title>Remunération Coach</Modal.Title>
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
                                      <Autocomplete
                                        // id={(option) =>  option['id']}
                                        onChange={(event, value) => setCoach(value.id)}
                                        // onChange={handleSubmit}
                                        options={coachs}
                                       //  value={activities[creneauActivite]}
                                        getOptionSelected={(option) =>  option['id']}
                                        getOptionLabel={(option) =>  option['last_name']}
                                        renderInput={(params) => <TextField {...params}  label="Coach" variant="outlined" fullWidth />}
                                      />
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
export default RemunerationCoachModal;