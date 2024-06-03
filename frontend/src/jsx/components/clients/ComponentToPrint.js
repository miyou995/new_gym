import React from "react";
import logo from "../../../images/logo.png";
import atlas from "../../../images/atlas.png";
export const ComponentToPrint = React.forwardRef((props, ref) => {
//   const { id, date } = props;
//console.log('PROESSSS', props);
  return (
    <div className="container"  ref={ref}>
    <div className="row">
      
        <div className="col-12" >
             {/* <div className="row pt-4 p-5">
                <div className="col-12 mb-2 text-left">
                    <img src={atlas} style={{width: "5rem", height: "5rem"}} />
                </div>
            </div>    */}
            <div >
                <div className="col-12 text-left font-italic">
                    <p style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>N° : <span style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>#{props.value.id}</span></p>
                    <p style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Date : {props.value.date_creation}</p>
                </div>
                <div className="col-6">
                    <p style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Adhérant</p>
                    <p style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>ID :  <span style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>{props.value.client_id}</span></p>
                    <p style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Nom : <span style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>{props.value.client_last_name}</span></p>
                </div>
            </div>
           <hr className="mb-2"/>
            <div className="row d-flex align-items-center">
                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Abonnement :  {props.value.abonnement_name}</h5>
                </div>

                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Séances : {props.value.quantity}</h5>
                </div>
                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Début : {props.value.start_abc}</h5>
                </div>
                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Fin : {props.value.end_abc}</h5>
                </div>
                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Montant : {props.value.get_abc_price} DA</h5>
                </div>
                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Reçu : {props.value.amount} DA</h5>
                </div>
                <div className="col-12">
                    <h5 style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Reste : {props.value.get_abc_reste} DA</h5>
                </div>
            </div>
            <div className="d-flex flex-row bg-light text-dark p-2 mt-5">
                <div className="py-2 px-3 d-flex text-left align-items-center">
                    <div style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>Total : </div>
                    <div style={{color: "#000", "font-weight": "500", fontSize: "14pt"}}>{props.value.amount}</div>
                </div>
            </div> 
        </div>
    </div>
</div>
  );
});

