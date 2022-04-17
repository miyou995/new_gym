import React, { useState , useEffect, useContext} from "react";
import axios from 'axios';

import { ClientsContext } from './Clients';

import {useGetAPI} from '../useAPI'
 
// import { Tab, Nav,Row, Card, Col, Button, Modal, Container } from "react-bootstrap";
// import { Link } from "react-router-dom";

const HandleClient = () => {
  // const { state, dispatch } = useContext(SalleContext);
  
  const [creneaux, setCreneaux] = useState([]);

  useEffect(() => {
      const fetchCreneaux =  async () => {
         try {
            const result = await axios.get(`${process.env.REACT_APP_API_URL}/rest-api/creneau/`)

            setCreneaux(result.data)
          //   console.log('cest le resultat data',result.data);
         } catch (error) {
            alert(error);
            console.log(error);
         }
      }
      fetchCreneaux();
   }, []);


  const {clientState, dispatcher } = useContext(ClientsContext);

  const [civility, setCivility] = useState();
  const [lastName, setLastName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [adress, setAdress] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [nationality, setNationality] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [blood, setBlood] = useState("");
  const [note, setNote] = useState("");
  const [etat, setEtat] = useState("");
  const [dette, setDette] = useState("");
  //FK 
const [creneau, setCreneau] = useState("");
   
   
  
  let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/clients/` //ENDPOINT TO GET THE MODEL INSTANCE LIKE HERE CLIENTS 
  const savedClients = useGetAPI(endpoint)
  // const savedSalles = useAPI(endpoint)



  useEffect(()=>{
      dispatcher({type: "get", payload: savedClients})
      console.log('savedClients:', savedClients);
    },[savedClients]) 

  const handleSubmit = async e => {
    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/clients/create`
      e.preventDefault();

      const newClient = {
        // name:lastName, 
        // creneau: Number(creneau),
        civility :civility,
        last_name :lastName,
        first_name :firstName,
        adress :adress,
        phone :phone,
        email :email,
        nationality :nationality,
        birth_date :birthDate,
        state: etat,
        blood :blood,
        note :note,
        dette :Number(dette),
        creneau :Number(creneau),
      }
      console.log('the new planning',newClient );
      await axios.post(endpoint, newClient)

      dispatcher({type:'add', payload:newClient})

      console.log('le ID dCreneau est ', creneau);
      console.log('le format json envoyé ==========>',newClient);
      setLastName("")
      setCreneau("")
  }
  return (
<div className="">
          <div className="card">
            <div className="card-header">
              <h4 className="card-title">Profile Abonnus</h4>
            </div>
            <div className="card-body">
              <div className="basic-form">
                <form onSubmit={handleSubmit}>
                  <div className="form-row">
                    <div className="form-group col-md-6">
                      <label>Nom</label>
                      <input type="text" name="last_name" className="form-control" placeholder="Nom du client" onChange={e => setLastName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Prénom</label>
                      <input  type="text" name="first_name"  className="form-control"  placeholder="Prénom du client"onChange={e => setFirstName(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Email</label>
                      <input  type="email" name="email"  className="form-control"  placeholder="Email"onChange={e => setEmail(e.target.value)}/>
                    </div>

                    <div className="form-group col-md-6">
                      <label>Adresse</label>
                      <input type="text"name="adress" className="form-control" onChange={e => setAdress(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Date de naissance</label>
                      <input type="date" name="birth_date" max="2099-01-01"  className="form-control" onChange={e => setBirthDate(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Nationalité</label>
                      <input type="text" name="nationality" className="form-control" onChange={e => setNationality(e.target.value)} />
                    </div>
                    <div className="form-group col-md-6">
                      <label>Téléphone</label>
                      <input type="text" name="phone" className="form-control" onChange={e => setPhone(e.target.value)} />
                    </div>
                  </div>
                
                  <div className="form-row">
                    <div className="form-group col-md-4">
                      <label>Civilité</label>
                      <select  defaultValue={"option"} name="civility"  className="form-control" onChange={e => setCivility(e.target.value)}>
                      <option value="option" disabled>Cliquez pour choisir</option>
                        <option value="MLL" >Mlle</option>
                        <option value="MME" >Mme</option>
                        <option value="MR" >Mr</option>
                      </select>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Groupe sanguin</label>
                      <select defaultValue={"option"} name="blood" className="form-control" onChange={e => setBlood(e.target.value)}>
                      <option value="option" disabled>Cliquez pour choisir</option>
                        <option value='A-'  >A-</option>
                        <option value='A+'  >A+</option>
                        <option value='B-'  >B-</option>
                        <option value='B+'  >B+</option>
                        <option value='O-'  >O-</option>
                        <option value='O+'  >O+</option>
                        <option value='AB-' >AB-</option>
                        <option value='AB+' >AB+</option>
                      </select>
                      
                    </div>
                    <div className="form-group col-md-4">
                      <label>état</label>
                      <select  defaultValue={"option"} name="state" className="form-control" onChange={e => setEtat(e.target.value)}>
                        <option value="option" disabled>Cliquez pour choisir</option>
                        <option value="A" >Active</option>
                        <option value="N" >Non active</option>
                        <option value="S" >Suspendue</option>
                      </select>
                    </div>
                  </div>
                  <div className="form-row">
                    <div className="form-group col-md-4">
                    <label>Dettes</label>
                      <input type="number" name="dette" className="form-control" onChange={e => setDette(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Creneau</label>
                      <select defaultValue={"option"} name="creneau" className="form-control" onChange={e => setCreneau(e.target.value)}>
                        <option value="option" disabled>Cliquez pour choisir</option>
                        { creneaux.map(creneau =>
                          <option key={creneau.id} value={creneau.id}>{creneau.hour_start}</option>
                      )}
                      </select>
                    </div>
                </div>
                  <div className="form-row">
                      <label>Note</label>
                      <textarea name="note" className="form-control" onChange={e => setNote(e.target.value)}/>
                </div>

                  <button type="submit" className="btn btn-primary">
                    Creer
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      
  )
}
export default HandleClient;




