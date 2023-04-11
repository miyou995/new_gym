import React from "react";
import logo from "../../../images/logo.png";
import atlas from "../../../images/atlas.png";
import "./print.css";
export const ComponentToPrint = React.forwardRef((props, ref) => {
//   const { id, date } = props;
//console.log('PROESSSS', props);
  return (
    <div className="container print-container"  ref={ref}>
    <div className="row px-5">
      
        <div className="col-12 pt-5 p-3"  style={{width: "300px"}}>
             {/* <div className="row pt-4 p-5">
                <div className="col-12 mb-2 text-left">
                    <img src={atlas} style={{width: "5rem", height: "5rem"}} />
                </div>
            </div>    */}
            <div className="row mb-5 py-3 ">
                <div className="col-12 text-left">
                    <p className="mb-1 mr-5 h3 ">N° : <span className="font-weight-light">#{props.value.id}</span></p>
                    <p className="mr-5 h3">Date : <span className="font-weight-bold">{props.value.date_creation}</span></p>
                </div>
                <div className="col-6">
                    <p className="font-weight-bold mb-4 h2">Adhérant</p>
                    <p className="mb-1 h3 mb-3">ID :  <span className="font-weight-bold">{props.value.client_id}</span></p>
                    <p className="mb-1 h3 mb-2">Nom : <span className="font-weight-bold">{props.value.client_last_name}</span></p>
                </div>
            </div>
            {/* <hr className="mb-2"/>
            <div className="row d-flex align-items-center">
                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Abonnement :  {props.value.abonnement_name}</h5></th>
                </div>

                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Séances : {props.value.quantity}</h5></th>
                </div>
                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Début : {props.value.start_abc}</h5></th>
                </div>
                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Fin : {props.value.end_abc}</h5></th>
                </div>
                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Montant : {props.value.get_abc_price} DA</h5></th>
                </div>
                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Reçu : {props.value.amount} DA</h5></th>
                </div>
                <div className="col-12">
                    <th><h5 className='h2 mr-5'>Reste : {props.value.get_abc_reste} DA</h5></th>
                </div>
            </div>
            <div className="d-flex flex-row bg-light text-dark p-2 mt-5">
                <div className="py-2 px-3 d-flex text-left align-items-center">
                    <div className="mb-2 h1 mr-4">Total : </div>
                    <div className="h1 font-weight-light">{props.value.amount}</div>
                </div>
            </div> */}
        </div>
    </div>
</div>
  );
});

