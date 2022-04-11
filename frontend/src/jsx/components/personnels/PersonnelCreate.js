import React, { useState } from "react";
import axios from 'axios';
import ShortCuts from "../ShortCuts";

import { useGetAPI, usePostAPI } from '../useAPI'
import {  useHistory } from "react-router-dom";

 

const PersonnelCreate = () => {
  
  const history = useHistory();

  const [civility, setCivility] = useState();
  const [lastName, setLastName] = useState("");
  const [firstName, setFirstName] = useState("");
  const [adress, setAdress] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [nationality, setNationality] = useState("Algérienne");
  const [birthDate, setBirthDate] = useState("");
  const [blood, setBlood] = useState("");
  const [note, setNote] = useState("");
  const [etat, setEtat] = useState("");
  //FK 
   
  const HandleSubmit = async e => {
    let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/personnel/create`
      e.preventDefault();
      const newPersonnel = {
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
      }
      usePostAPI(endpoint, newPersonnel)
      history.push("/personnel")

  }
  return (
        <div className="">
                <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
        <ShortCuts />
      </div>
          <div className="card">
            <div className="card-header">
              <h4 className="card-title">Profile Personnel</h4>
            </div>
            <div className="card-body">
              <div className="basic-form">
                <form onSubmit={HandleSubmit}>
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
                      <input type="date" name="birth_date" className="form-control" onChange={e => setBirthDate(e.target.value)}/>
                    </div>
                    <div className="form-group col-md-6">
                      <label>Nationalité</label>
                      <input type="text" name="nationality" value={nationality} className="form-control" onChange={e => setNationality(e.target.value)} />
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
                        <option value="MLL">Mlle</option>
                        <option value="MME" >Mme</option>
                        <option value="MR" >Mr</option>
                      </select>
                    </div>
                    <div className="form-group col-md-4">
                      <label>Groupe sanguin</label>
                      <select defaultValue={"option"} name="blood" className="form-control" onChange={e => setBlood(e.target.value)}>
                      <option value="option" disabled>Cliquez pour choisir</option>
                        <option value='A-' >A-</option>
                        <option value='A+' >A+</option>
                        <option value='B-' >B-</option>
                        <option value='B+' >B+</option>
                        <option value='O-' >O-</option>
                        <option value='O+' >O+</option>
                        <option value='AB-'>AB-</option>
                        <option value='AB+'>AB+</option>
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
export default PersonnelCreate;




