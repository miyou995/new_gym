import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
// import productData from "../productData";
import useAxios from "../useAxios";
import { Tab, Button } from "react-bootstrap";

import PerfectScrollbar from "react-perfect-scrollbar";

import { ToastContainer, toast } from 'react-toastify'
import {notifySuccess, notifyError} from '../Alert'
import ShortCuts from "../ShortCuts";
import PaiementModal from './PaiementModal'



const PersonnelDetail = (props) => {
  const api = useAxios();
  const [paiementModal, setPaiementModal] = useState(false);
  const [employe, setEmploye] = useState({});
  const [transactionsEmploye, setTransactionsEmploye] = useState([]);

  const employeId = props.match.params.id;

  let PersonnelDetailEndpoint = `${process.env.REACT_APP_API_URL}/rest-api/personnel/${employeId}`;
  const transactionsEmployeEnd = `${process.env.REACT_APP_API_URL}/rest-api/transactions/remunerationProf-by-id?em=${employeId}`;
  const [personnelData, setPersonnelData] = useState([])
  //FK 
  useEffect(() => {
    api.get(PersonnelDetailEndpoint).then((res) => {
      setPersonnelData(res.data)
    })
  }, []);
  useEffect(() => {
    const personnelSelected = personnelData;
    setEmploye(personnelSelected);
  }, [personnelData]);

  const capitalizeFirstLetter = (word) => {
    if (word) return word.charAt(0).toUpperCase() + word.slice(1);
    return "";
  };
  useEffect(() => {
    //  const clientId = props.match.params.id;
     api.get(transactionsEmployeEnd).then( res => {
      setTransactionsEmploye(res.data)
           })
  }, [props.match.params.id] );
  return (
    <>
<div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
<ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
        <ShortCuts />
      </div>
      {/* <div className="page-titles">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to="/coach">Coachs</Link>
          </li>
          <li className="breadcrumb-item active">
            <Link to="#">ID: {employe.id} - {employe.last_name}</Link>
          </li>
        </ol>
      </div> */}
      {/* <div className="row">
        

        <div className="col-lg-4  col-sm-6">
            <button type='button' className="btn btn-success" onClick= { e => setPaiementModal(true)}>
              <h2 style={{color:'#ffffff',  marginTop:'5px'}} >Ajouter Virement</h2>
            </button>
        </div>
        <div className="col-lg-4  col-sm-6">
            <button type='button' className="btn btn-danger" >
              <h2 style={{color:'#ffffff',  marginTop:'5px'}} > Reste du salaire : {employe.salaire}</h2>
            </button>
        </div>
      </div> */}
      <div className="row">
        <div className="col-12">
          <div className="card">
            <div className="card-body">
              <div className="row">
              <div className="card-body bg-white ">
                <div className="media profile-bx">
                      <img src={employe.picture} alt="" />
                      <div className="media-body align-items-center">
                        <h2 className="text-black font-w600">
                          {capitalizeFirstLetter(employe.last_name)} {capitalizeFirstLetter(employe.first_name)} { employeId.function && (employe.function)}
                        </h2>
                        <h4 className="mb-2 text-black">ID: <span className='text-danger'>{employe.id}</span></h4>
                        <h6 className="text-black">
                            inscrit le : <span className="text-primary">{employe.date_added}</span>
                        </h6>
                        <div className="social-icons">
                            <Link to={`/personnel/edit/${employeId}`} className="btn btn-outline-dark" > Modifier Profile </Link>
                        </div>
                      </div>
                      <div className="social-icons m-3">
                        <h6 className='text-primary'>Civilité:                   <a className="item text-dark">{employe.civility_display}</a> </h6>
                        <h6 className='text-primary'>Téléphone:                  <span className="item text-dark"><a href={`tel:${employe.phone}`}> {employe.phone}</a></span></h6>
                        <h6 className='text-primary'>email:                      <span className="item text-dark"><a href={`mailto:${employe.email}`}> {employe.email}</a></span></h6>
                        <h6 className='text-primary'>Groupe sanguin:&nbsp;&nbsp; <span className="badge badge-danger light">{employe.blood}</span> </h6>
                      </div>
                      <div className="social-icons m-3">
                        <h6 className='text-primary'>Nationalité:                 <span className="item text-dark">{employe.nationality}</span> </h6>
                        <h6 className='text-primary'>Date de naissance:           <span className="item text-dark">{employe.birth_date}</span> </h6>
                        <h6 className='text-primary'>Salaire par heure:           <a className="item text-dark"> {employe.pay_per_hour}</a> </h6>
                      </div>
                  </div>
                </div>
                {/*Tab slider End*/}
                <div className="col-xl-9 col-lg-6  col-md-6 col-xxl-7 col-sm-12">
                  <div className="product-detail-content">
                    {/*Product details*/}
                    <div className="new-arrival-content pr">
                      <ul>
                        {/* 
                          { client.maladie_name.map(maladie =>
                            <div className="custom-control custom-checkbox mb-3">
                              <li className="custom-control-label" key={maladie.id} htmlFor={maladie.id}> {maladie.name}</li>
                            </div>
                          )}
                        */}
                      </ul>
                      <div className='row d-flex'>
                        <div className="shopping-cart mt-3 col- col-md-6">
                          <h4>Note :</h4>
                          <p>{employe.note}</p>
                        </div>
                        <div className="shopping-cart mt-3 col- col-md-6">
                          <h4>Adresse :</h4>
                          <p>{employe.adress}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        

        <div className="col-xl-3 col-xxl-4 col-lg-6 col-sm-6">
          <div className="card">
            <div className="card-header border-0">
              <h4 className="mb-0  fs-20">Virements</h4>
              
            </div>
            <div className="card-body p-0">
            <PerfectScrollbar
                style={{ height: "370px" }}
                id="DZ_W_TimeLine"
                className="widget-timeline dz-scroll height370 ps ps--active-y"
              >
              <div className="table-responsive card-table">
                <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr>
                      <th className="text-left">Montant</th>
                      <th>Date</th>
                      {/* <th className="text-right">Total</th> */}
                    </tr>
                  </thead>
                  <tbody>
                    
                    {transactionsEmploye.map(trans => (
                      <tr key={trans.id}>
                      <td className="text-left">{trans.amount}</td>
                      {/* <td>0.18</td> */}
                      <td className="text-right">{trans.date_creation}</td>
                    </tr>
                    ))
                    }
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>
            </div>
            <div className="card-footer border-0 pt-0 text-center">
            </div>
          </div>
        </div>
        <PaiementModal show={paiementModal} onShowShange={setPaiementModal} coachData={{employeId: employeId, emplyeName:employe.first_name}} />
      </div>
    </>
  );
};

export default PersonnelDetail;
