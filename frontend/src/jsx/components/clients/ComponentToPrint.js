import React from "react";
import logo from "../../../images/logo.png";
import atlas from "../../../images/atlas.png";
import "./print.css";
export const ComponentToPrint = React.forwardRef((props, ref) => {
//   const { id, date } = props;
//console.log('PROESSSS', props);
  return (
    <div className="container"  ref={ref}>
    <div className="row px-5">
        {/* <div className="col-12">
            <div className="card">
                <div className="p-0">
                    <div className="row p-5">
                        <div className="col-md-6">
                            <img  src={logo} style={{width: "4rem", height: "4rem"}} />
                        </div>
                        <div className="col-md-6 text-right">
                            <p className="font-weight-bold mb-1">N°: <span className="font-weight-light">#{props.value.id}</span></p>
                            <p className="text-muted">Date: <span className="font-weight-light">{props.value.date_creation}</span></p>
                        </div>
                        <div className="col-md-6">
                            <p className="font-weight-bold mb-4 h4">Adhérant</p>
                            <p className="mb-1 h4">Nom: <span className="font-weight-light">{props.value.client_last_name}</span></p>
                            <p className="mb-1 h4">ID: <span className="font-weight-light">{props.value.client_id}</span></p>
                        </div>
                    </div>   
                    <div className="row p-5">
                        <div className="col-reverse">
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th style={{fontSize: "21px"}} className="border-0 text-uppercase font-weight-bold h1">Abonnement</th>
                                        <th style={{fontSize: "21px"}} className="border-0 text-uppercase font-weight-bold h1">Séances</th>
                                        <th style={{fontSize: "21px"}} className="border-0 text-uppercase font-weight-bold h1">Début</th>
                                        <th style={{fontSize: "21px"}} className="border-0 text-uppercase font-weight-bold h1">Fin</th>
                                        <th style={{fontSize: "21px"}} className="border-0 text-uppercase font-weight-bold h1">Montant</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.abonnement_name}</div></td>
                                        <td><div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.quantity}</div></td>
                                        <td><div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.start_abc}</div></td>
                                        <td><div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.end_abc}</div></td>
                                        <td><div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.amount}</div></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div className="container">
                        <div className="d-flex align-items-center">
                            <h4 className=''>Abonnement</h4>
                            <div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.abonnement_name}</div>
                        </div>
                        <div className="d-flex align-items-center">
                            <h4>Séances</h4>
                            <div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.quantity}</div>
                        </div>
                        <div className="d-flex align-items-center">
                            <h4>Début</h4>
                            <div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.start_abc}</div>
                        </div>
                        <div className="d-flex align-items-center">
                            <h4>Fin</h4>
                            <div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.end_abc}</div>
                        </div>
                        <div className="d-flex">
                            <h4>Montant</h4>
                            <div style={{fontSize: "19px"}} className="font-weight-lighter mt-1 h1" >{props.value.amount}</div>
                        </div>
                    </div>
                    <div className="d-flex flex-row bg-light text-dark p-2">
                        <div className="py-2 px-3 d-flex text-left">
                            <div className="mb-2 h3 mr-4">Total : </div>
                            <div className="h3 font-weight-light">{props.value.amount}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div> */}
        <div className="col-12 pt-5 p-3"  style={{width: "300px"}}>
             {/* <div className="row pt-4 p-5">
                <div className="col-12 mb-2 text-left">
                    <img src={atlas} style={{width: "5rem", height: "5rem"}} />
                </div>
            </div>    */}
            <div className="row mb-5 py-3 ">
                <div className="col-12 text-left font-italic">
                    <p className="mb-1 mr-5 h3 ">N° : <span className="font-weight-light">#{props.value.id}</span></p>
                    <p className="mr-5 h3">Date : <span className="font-weight-bold">{props.value.date_creation}</span></p>
                </div>
                <div className="col-6">
                    <p className="font-weight-bold mb-4 h2">Adhérant</p>
                    <p className="mb-1 h3 mb-3">ID :  <span className="font-weight-bold">{props.value.client_id}</span></p>
                    <p className="mb-1 h3 mb-2">Nom : <span className="font-weight-bold">{props.value.client_last_name}</span></p>
                </div>
            </div>
            <hr className="mb-2"/>
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





                {/* <div className="col-12 justify-content-between align-items-center d-flex mb-3 text-uppercase">
                    <th><h4 className="h2 mr-5">Séances : </h4></th>
                    <td><div className="text-left font-weight-lighter mt-1 h2" >{props.value.quantity}</div></td>
                </div>
                <div className="col-12 justify-content-between align-items-center d-flex mb-3 text-uppercase">
                    <th><h4 className="h2 mr-5">Début : </h4></th>
                    <td><div className="text-left font-weight-lighter mt-1 h2" >{props.value.start_abc}</div></td>
                </div>
                <div className="col-12 justify-content-between align-items-center d-flex mb-3 text-uppercase ">
                    <th><h4 className="h2 mr-5">Fin : </h4></th>
                    <td><div className="text-left font-weight-lighter mt-1 h2" >{props.value.end_abc}</div></td>
                </div>
                <div className="col-12 justify-content-between align-items-center d-flex mb-3 text-uppercase">
                    <th><h4 className="h2 mr-5">Montant : </h4></th>
                    <td><div className="text-left font-weight-lighter mt-1 h2" >{props.value.get_abc_price} DA</div></td>
                </div>
                <div className="col-12 justify-content-between align-items-center d-flex mb-3 text-uppercase">
                    <th><h4 className="h2 mr-5">Reçu : </h4></th>
                    <td><div className="text-left font-weight-lighter mt-1 h2" >{props.value.amount} DA</div></td>
                </div>
                <div className="col-12 justify-content-between align-items-center d-flex mb-3 text-uppercase">
                    <th><h4 className="h2 mr-5">Reste : </h4></th>
                    <td><div className="text-left font-weight-lighter mt-1 h2" >{props.value.get_abc_reste} DA</div></td>
                </div> */}
            </div>
            <div className="d-flex flex-row bg-light text-dark p-2 mt-5">
                <div className="py-2 px-3 d-flex text-left align-items-center">
                    <div className="mb-2 h1 mr-4">Total : </div>
                    <div className="h1 font-weight-light">{props.value.amount}</div>
                </div>
            </div>
        </div>
    </div>
</div>
  );
});


// export class ComponentToPrint extends React.PureComponent {
//     render() {
//       return (
//         <div className="container">
//     <div className="row">
//         <div className="col-12">
//             <div className="card">
//                 <div className="card-body p-0">
//                     <div className="row p-5">
//                         <div className="col-md-6">
//                             <img src="http://via.placeholder.com/400x90?text=logo" />
//                         </div>

//                         <div className="col-md-6 text-right">
//                             <p className="font-weight-bold mb-1">Invoice #550</p>
//                             <p className="text-muted">Due to: 4 Dec, 2019</p>
//                         </div>
//                     </div>
//                     <hr className="my-5" />

//                     <div className="row pb-5 p-5">
//                         <div className="col-md-6">
//                             <p className="font-weight-bold mb-4">Client Information</p>
//                             <p className="mb-1">John Doe, Mrs Emma Downson</p>
//                             <p>Acme Inc</p>
//                             <p className="mb-1">Berlin, Germany</p>
//                             <p className="mb-1">6781 45P</p>
//                         </div>

//                         <div className="col-md-6 text-right">
//                             <p className="font-weight-bold mb-4">Payment Details</p>
//                             <p className="mb-1"><span className="text-muted">VAT: </span> 1425782</p>
//                             <p className="mb-1"><span className="text-muted">VAT ID: </span> 10253642</p>
//                             <p className="mb-1"><span className="text-muted">Payment Type: </span> Root</p>
//                             <p className="mb-1"><span className="text-muted">Name: </span> John Doe</p>
//                         </div>
//                     </div>

//                     <div className="row p-5">
//                         <div className="col-md-12">
//                             <table className="table">
//                                 <thead>
//                                     <tr>
//                                         <th className="border-0 text-uppercase small font-weight-bold">ID</th>
//                                         <th className="border-0 text-uppercase small font-weight-bold">Item</th>
//                                         <th className="border-0 text-uppercase small font-weight-bold">Description</th>
//                                         <th className="border-0 text-uppercase small font-weight-bold">Quantity</th>
//                                         <th className="border-0 text-uppercase small font-weight-bold">Unit Cost</th>
//                                         <th className="border-0 text-uppercase small font-weight-bold">Total</th>
//                                     </tr>
//                                 </thead>
//                                 <tbody>
//                                     <tr>
//                                         <td>1</td>
//                                         <td>Software</td>
//                                         <td>LTS Versions</td>
//                                         <td>21</td>
//                                         <td>$321</td>
//                                         <td>$3452</td>
//                                     </tr>
//                                     <tr>
//                                         <td>1</td>
//                                         <td>Software</td>
//                                         <td>Support</td>
//                                         <td>234</td>
//                                         <td>$6356</td>
//                                         <td>$23423</td>
//                                     </tr>
//                                     <tr>
//                                         <td>1</td>
//                                         <td>Software</td>
//                                         <td>Sofware Collection</td>
//                                         <td>4534</td>
//                                         <td>$354</td>
//                                         <td>$23434</td>
//                                     </tr>
//                                 </tbody>
//                             </table>
//                         </div>
//                     </div>

//                     <div className="d-flex flex-row-reverse bg-dark text-white p-4">
//                         <div className="py-3 px-5 text-right">
//                             <div className="mb-2">Grand Total</div>
//                             <div className="h2 font-weight-light">$234,234</div>
//                         </div>

//                         <div className="py-3 px-5 text-right">
//                             <div className="mb-2">Discount</div>
//                             <div className="h2 font-weight-light">10%</div>
//                         </div>

//                         <div className="py-3 px-5 text-right">
//                             <div className="mb-2">Sub - Total amount</div>
//                             <div className="h2 font-weight-light">$32,432</div>s
//                         </div>
//                     </div>
//                 </div>
//             </div>
//         </div>
//     </div>
    
//     <div className="text-light mt-5 mb-5 text-center small">by : <a className="text-light" target="_blank" href="http://totoprayogo.com">totoprayogo.com</a></div>

// </div>
//       );
//     }
//   }
