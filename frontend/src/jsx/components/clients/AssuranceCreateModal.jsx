import React, { useState, useCallback, useEffect } from "react";
import { Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import useAxios from "../useAxios";
import { Dropdown, Tab, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
 
function refreshPage() {
  window.location.reload(false);
}
const AssuranceCreateModal = ({show, onShowChange, clientData}) => {
  const api = useAxios();
    const handleShow = useCallback( () => {onShowChange(false)}, [onShowChange])

    // let clientEnd = `${process.env.REACT_APP_API_URL}/rest-api/clients-name/`
    // let assuranceEnd = `${process.env.REACT_APP_API_URL}/rest-api/assurance/`
    
    // const clients = useGetAPI(clientEnd)
    // const assurance = useGetAPI(assuranceEnd)
    // //console.log('les clients ', clients);
    // const history = useHistory();
    const [amount, setAmount] = useState("");
    const [notes, setNotes] = useState("");
    // const [type, setType] = useState("");
    // const [client, setClient] = useState("");
   //  useEffect(() => {
         // setPeople(clients)
      //   //console.log('THE NEW CLIENT ONEEE ', res.data);

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
    const HandleSubmit = async e => {
      e.preventDefault();
    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/transactions/assurance/create`

      const newTransaction = {
        amount : amount ,
        notes : notes ,
        // type : type ,
        client : clientData['clientId']
        }
        await api.post(endpoint, newTransaction)
        // history.push("/client")
        refreshPage()
        // handleShow()
        // //console.log('THE NEW CLIENT ', newTransaction);
    }
return ( 
    <Modal className="fade bd-example-modal-lg" size="lg" onHide={handleShow} show={show}>
    <Modal.Header>
      <Modal.Title className='text-black' >Creneau</Modal.Title>
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
          <div className="form-row">
            {/* <div className="form-group col-md-6">
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
            </div> */}
            {/* <div className="form-group col-md-6">
              <Autocomplete
                // id={(option) =>  option['id']}
                onChange={(event, value) => setType(value.id)}
                // onChange={handleSubmit}
                options={assurance}
                //  value={activities[creneauActivite]}
                getOptionSelected={(option) =>  option['id']}
                getOptionLabel={(option) =>  (
                    option['price'])}
                renderInput={(params) => <TextField {...params}  label="Type d'assurance" variant="outlined" fullWidth />}
              />
            </div> */}
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
              onChange={e=> setNotes(e.currentTarget.value)}

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
export default AssuranceCreateModal;