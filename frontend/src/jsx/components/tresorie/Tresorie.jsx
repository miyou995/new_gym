import React, { Fragment, useState, useEffect } from "react";
import { Dropdown } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useGetAPI, usePutAPI } from '../useAPI'

import { ToastContainer } from 'react-toastify'
import ShortCuts from "../ShortCuts";
import PerfectScrollbar from "react-perfect-scrollbar";
import axios from "axios";



const CoinDetails = () => {
    const formatDate = (date) => {
        return new Date(date).toISOString().slice(0, 10)
     }
     
    const [caBySalle, setCaBySalle] = useState([])
    const [caByAB, setCaByAB] = useState([])
    const [chiffre, setChiffre] = useState([])
    const [startDate, setStartDate] = useState(new Date())
    const [endDate, setEndDate] = useState(new Date())
    const caBySalleEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/ca-by-salle?st=${formatDate(startDate)}&nd=${formatDate(endDate)}`
    const caByABEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/paiement/ca-by-abonnement?st=${formatDate(startDate)}&nd=${formatDate(endDate)}`
    const caEND = `${process.env.REACT_APP_API_URL}/rest-api/transactions/ca_by_date?st=${formatDate(startDate)}&nd=${formatDate(endDate)}`
useEffect(() => {
    axios.get(caBySalleEND).then((res) => {
        setCaBySalle(res.data)
     })
     axios.get(caByABEND).then((res) => {
        setCaByAB(res.data)
     })
     axios.get(caEND).then((res) => {
      setChiffre(res.data)
      console.log('resulta ca', res.data);
   })
     
}, [startDate, endDate]);
  return (
    <Fragment>
        <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
        </div>
<div className="row">
        <div className="form-group col-md-2">
            <label >Date Début</label>
            <input type="date" name="start_date" className="form-control" value={formatDate(startDate)} onChange={e => setStartDate(e.target.value)}/>
        </div>
         <div className="form-group col-md-2">
             <label >Date Fin</label>
            <input type="date" name="end_date" className="form-control" value={formatDate(endDate)} onChange={e => setEndDate(e.target.value)}/>
         </div>
        <div className="form-group float-right ">
          <h2 className="text-danger ml-5">Résultat: {chiffre.chiffre_affaire ? chiffre.chiffre_affaire : 0} DA</h2>
        </div>
</div>
         <div className="row">
         <div className="col-lg-4 col-xxl-4  col-sm-6">
          <div className="card"  >
            <div className="card-header border-0">
              <h4 className="mb-0 text-black fs-20">Chiffre d'affaire par salle</h4>
            </div>
            <div className="card-body p-0">
            <PerfectScrollbar style={{ height: "370px" }} id="DZ_W_TimeLine" className="widget-timeline dz-scroll height370 ps ps--active-y" >
              <div className="table-responsive card-table">
                <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr>
                      <th className="text-left"><h5>nom</h5></th>
                      <th className="text-center"><h5>Mantant</h5></th>
                    </tr>
                  </thead>
                  <tbody>
                    {caBySalle.map(tran => (
                      <tr key={tran.name }>
                      <td className="py-2 text-left">
                        {tran.name} 
                      </td>
                        <td className="py-2 pl-5 wspace-no text-center">
                            {tran.abonnements__type_abonnement_client__transactions__amount__sum}
                        </td>
                    </tr>
                    ))
                    }
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>

            </div>
            <div className="card-footer border-0 pt-0 text-center">
              <Link to="/transactions" className="btn-link">
                Afficher tout <i className="fa fa-caret-right ml-2 scale-2" />
              </Link>
            </div>
          </div>
        </div>


        <div className="col-lg-4 col-xxl-4  col-sm-6" >
          <div className="card">
            <div className="card-header border-0">
              <h4 className="mb-0 text-black fs-20">Chiffre d'affaire par Abonnement</h4>
            </div>
            <div className="card-body p-0">
            <PerfectScrollbar style={{ height: "370px" }} id="DZ_W_TimeLine" className="widget-timeline dz-scroll height370 ps ps--active-y" >
              <div className="table-responsive card-table">
                <table className="table text-center bg-warning-hover">
                  <thead>
                    <tr>
                      <th className="text-left"><h5>nom</h5></th>
                      <th className="text-center"><h5>Mantant</h5></th>
                    </tr>
                  </thead>
                  <tbody>
                    {caByAB.map(tran => (
                      <tr key={tran.name}>
                      <td className="py-2 text-left">
                        {tran.name} 
                      </td>
                    <td className="py-2 pl-5 wspace-no text-center">
                        {tran.type_abonnement_client__transactions__amount__sum}
                    </td>
                    </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </PerfectScrollbar>

            </div>
            <div className="card-footer border-0 pt-0 text-center">
              <Link to="/transactions" className="btn-link">
                Transactions <i className="fa fa-caret-right ml-2 scale-2" />
              </Link>
            </div>
          </div>
        </div>


    </div>








    </Fragment>
  );
};

export default CoinDetails;
