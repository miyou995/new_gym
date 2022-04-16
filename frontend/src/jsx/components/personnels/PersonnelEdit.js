import React, { useState, useEffect } from "react";
import axios from "axios";
import ShortCuts from "../ShortCuts";

import { useGetAPI, usePutAPI } from "../useAPI";
import { useHistory } from "react-router-dom";
//  useNavigate in V6
import {notifySuccess, notifyError} from '../Alert'


const PersonnelEdit = (props) => {
  // let creneauxEnd = `${process.env.REACT_APP_API_URL}/rest-api/creneau/`
  const currentPersonnelId = props.match.params.id;

  let personnelURI = `${process.env.REACT_APP_API_URL}/rest-api/personnel/${currentPersonnelId}/`;

  const creneaux = useGetAPI(personnelURI);
  const history = useHistory();

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
  const [fonction, setFonction] = useState("");
  // const [dette, setDette] = useState("");
  //FK
  // const [creneau, setCreneau] = useState("");
  useEffect(() => {
    axios.get(personnelURI).then((res) => {
      setCivility(res.data.civility);
      setLastName(res.data.last_name);
      setFirstName(res.data.first_name);
      setAdress(res.data.adress);
      setPhone(res.data.phone);
      setEmail(res.data.email);
      setNationality(res.data.nationality);
      setBirthDate(res.data.birth_date);
      setBlood(res.data.blood);
      setNote(res.data.note);
      setEtat(res.data.etat);
      setFonction(res.data.function)
      // setDette(res.data.dette)
      // setCreneau(res.data.creneau)
    });
  }, []);
  const HandleSubmit = async (e) => {
    e.preventDefault();
    const EditedPersonnel = {
      civility: civility,
      last_name: lastName,
      first_name: firstName,
      adress: adress,
      phone: phone,
      email: email,
      nationality: nationality,
      function: fonction,
      birth_date: birthDate,
      state: etat,
      blood: blood,
      note: note,
      // dette :Number(dette),
      // creneau :Number(creneau),
    };
    usePutAPI(personnelURI, EditedPersonnel).then( res => {
      notifySuccess('Personnel modifier avec succés')
        history.push("/personnel");
      }).catch(err => {
        notifyError("Erreur lors de la modification du personnel")
      })
  };
  return (
    <div className="">
      <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
        <ShortCuts />
      </div>
      <div className="card">
        <div className="card-header">
          <h4 className="card-title">Profile Abonné</h4>
        </div>
        <div className="card-body">
          <div className="basic-form">
            <form onSubmit={HandleSubmit}>
              <div className="form-row">
                <div className="form-group col-md-6">
                  <label>Nom </label>
                  <input
                    type="text"
                    name="last_name"
                    className="form-control"
                    value={lastName}
                    placeholder="Nom du client"
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </div>
                <div className="form-group col-md-6">
                  <label>Prénom</label>
                  <input
                    type="text"
                    name="first_name"
                    className="form-control"
                    value={firstName}
                    placeholder="Prénom du client"
                    onChange={(e) => setFirstName(e.target.value)}
                  />
                </div>
                <div className="form-group col-md-6">
                      <label>Fonction</label>
                      <input type="text" name="functiopn"  className="form-control"value={fonction}  onChange={e => setFonction(e.target.value)}/>
                    </div>
                <div className="form-group col-md-6">
                  <label>Email </label>
                  <input
                    type="email"
                    name="email"
                    className="form-control"
                    value={email}
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </div>

                <div className="form-group col-md-6">
                  <label>Adresse</label>
                  <input
                    type="text"
                    name="adress"
                    className="form-control"
                    value={adress}
                    onChange={(e) => setAdress(e.target.value)}
                  />
                </div>
                <div className="form-group col-md-6">
                  <label>Date de naissance </label>
                  <input
                    type="date"
                    name="birth_date"
                    className="form-control"
                    value={birthDate}
                    onChange={(e) => setBirthDate(e.target.value)}
                  />
                </div>
                <div className="form-group col-md-6">
                  <label>Nationalité</label>
                  <input
                    type="text"
                    name="nationality"
                    className="form-control"
                    value={nationality}
                    onChange={(e) => setNationality(e.target.value)}
                  />
                </div>
                <div className="form-group col-md-6">
                  <label>Téléphone</label>
                  <input
                    type="text"
                    name="phone"
                    className="form-control"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group col-md-4">
                  <label>Civilité</label>
                  <select
                    defaultValue={"option"}
                    name="civility"
                    className="form-control"
                    value={civility}
                    onChange={(e) => setCivility(e.target.value)}
                  >
                    <option value="option" disabled>
                      Cliquez pour choisir
                    </option>
                    <option value="MLL">Mlle</option>
                    <option value="MME">Mme</option>
                    <option value="MR">Mr</option>
                  </select>
                </div>
                <div className="form-group col-md-4">
                  <label>Groupe sanguin</label>
                  <select
                    defaultValue={"option"}
                    name="blood"
                    className="form-control"
                    value={blood}
                    onChange={(e) => setBlood(e.target.value)}
                  >
                    <option value="option" disabled>
                      Cliquez pour choisir
                    </option>
                    <option value="A-">A-</option>
                    <option value="A+">A+</option>
                    <option value="B-">B-</option>
                    <option value="B+">B+</option>
                    <option value="O-">O-</option>
                    <option value="O+">O+</option>
                    <option value="AB-">AB-</option>
                    <option value="AB+">AB+</option>
                  </select>
                </div>
                <div className="form-group col-md-4">
                  <label>état</label>
                  <select
                    defaultValue={"option"}
                    name="state"
                    className="form-control"
                    value={etat}
                    onChange={(e) => setEtat(e.target.value)}
                  >
                    <option value="option" disabled>
                      Cliquez pour choisir
                    </option>
                    <option value="A">Active</option>
                    <option value="N">Non active</option>
                    <option value="S">Suspendue</option>
                  </select>
                </div>
              </div>

              <div className="form-row">
                <label>Note</label>
                <textarea
                  name="note"
                  className="form-control"
                  value={note}
                  onChange={(e) => setNote(e.target.value)}
                />
              </div>

              <button type="submit" className="btn btn-primary">
                Confirmer la modification
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
export default PersonnelEdit;
