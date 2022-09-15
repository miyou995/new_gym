import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button } from "react-bootstrap";
import useAxios from "../useAxios";

/// images
import avartar5 from "../../../images/avatar/5.png";
import { Link } from "react-router-dom";

import ShortCuts from "../ShortCuts";



export const ClientContext = React.createContext()
// function refreshPage() {
//    window.location.reload(false);
//  }
function refreshPage() {
   window.location.reload(false);
 }


const ClientList = () => {
   const api = useAxios();

   const formatDate = (date) => {
      try {
         const returned = new Date(date).toISOString().slice(0, 10)
         return returned
      } catch (error) {
         const returned = new Date().toISOString().slice(0, 10)
         return returned
      }
   }

   const [nextpage, setNextpage] = useState(1);
   const [clientData, setclientData] = useState([]);
   const [searchValue, setSearchValue] = useState('')
   const [startDate, setStartDate] = useState(formatDate(new Date('2021-01-05')));
   const [endDate, setEndDate] = useState(formatDate(new Date()));

   const [searchBarActivated, setSearchBarActivated] = useState(false)
   var endpoint = `${process.env.REACT_APP_API_URL}/rest-api/clients-name/?page=${nextpage}`
   var searchEndpoint = `${process.env.REACT_APP_API_URL}/rest-api/clients-name/?search=${searchValue}`
   
useEffect(() =>  {
   if (searchValue !== '') {
      api.get(searchEndpoint).then(res => {
         setclientData(res.data.results)
         console.log('le resultat des clients est ', res.data);
      })
   }else {
      api.get(endpoint).then(res => {
         setclientData(res.data.results)
         console.log('le resultat des clients est ', res.data);
      })}
}, [nextpage, searchValue]);

const [clientStatus, setClientStatus] = useState(null);


api.get(endpoint).then(res => {
  console.log(res.status);
  setClientStatus(res.status);
}).catch(error => {
  if (error.response) {
     console.log(error.response.data);
     console.log(error.response.status);
     console.log(error.response.headers);
     setClientStatus(error.response.status);
  }
})



console.log('le searchValue des searchValue est ', searchValue);

   const capitalizeFirstLetter = (word) => {
      if (word)
          return word.charAt(0).toUpperCase() + word.slice(1);
      return '';
   };

 return (
      <Fragment>
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div>
         {clientStatus == 200 && (
         <>
         {/* <PageTitle activeMenu="Liste" motherMenu="Abonnées" /> */}
         <div className="form-head d-flex mb-4 mb-md-5 align-items-start">
            <div className="input-group search-area d-inline-flex">
               <div className="input-group-append">
                  <span className="input-group-text">
                     <i className="flaticon-381-search-2"/>
                  </span>
               </div>
               <input id="searchClient" type="text" className="form-control" placeholder="rechercher un client" value={searchValue} onChange={e => setSearchValue(e.target.value)}/>
            </div>
               {/* <div className="input-group search-area d-inline-flex ml-3">
                  <input type="date" name="birth_date" value={startDate} className="form-control"  onChange={e => setStartDate(e.target.value)}/>
               </div>
               <div className="input-group search-area d-inline-flex ml-3">
                  <input type="date" name="birth_date" value={endDate} className="form-control"  onChange={e => setEndDate(e.target.value)}/>
               </div> */}
            <Link to="/client/create" className="btn btn-primary ml-auto">Ajouter un abonné</Link>
         </div>

         <div className="row">
            <div className="col-lg-12">
               <div className="card">
                  <div className="card-body">
                     <div className="table-responsive">
                        <table className="table mb-0 table-striped">
                           <thead>
                              <tr>
                                 <th className="customer_shop"> ID </th>
                                 <th>Nom</th>
                                 <th>Prénom</th>
                                 <th>Téléphone</th>
                                 <th className="pl-5 width200"> Addresse </th>
                                 <th>Adhesion</th>
                                 <th>Dettes</th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                           {clientData.map(client => (
                              <tr role="row" key={client.id} className="btn-reveal-trigger">
                                 <td className="customer_shop_single"> {client.id} </td>
                                 <td className="py-3">
                                    <Link to={`/client/${client.id}`}>
                                       <div className="media d-flex align-items-center">
                                          <div className="avatar avatar-xl mr-2">
                                             <div className="">
                                                <img className="rounded-circle img-fluid" src={avartar5} width="30" alt="" />
                                             </div>
                                          </div>
                                          <div className="media-body">
                                             <h5 className="mb-0 fs--1">
                                             {capitalizeFirstLetter(client.last_name)}
                                             </h5>
                                          </div>
                                       </div>
                                    </Link>
                                 </td>
                                 <td className="py-2">
                                    {capitalizeFirstLetter(client.first_name)}
                                 </td>
                                 <td className="py-2">
                                    <a href="tel:{client.phone}">{client.phone}</a>
                                 </td>
                                 <td className="py-2 pl-5 wspace-no"> {client.adress} </td>
                                 <td className="py-2">{client.date_added}</td>
                                 <td className="py-2  text-danger">{client.dettes.reste__sum}</td>
                              </tr>
                              ))}
                              </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>
         </div>
         {
            !searchBarActivated &&

            <div className='d-flex text-center justify-content-end'>

                <div className='dataTables_info text-black' id='example5_info '>
                  {/* Showing {activePag.current * sort + 1} to{' '}
                  {data.length > (activePag.current + 1) * sort
                    ? (activePag.current + 1) * sort
                    : data.length}{' '}
                  of {data.length} entries{' '} */}
                </div>
                <div
                  className='dataTables_paginate paging_simple_numbers'
                  id='example5_paginate'
                >
                  <Button
                    onClick={() =>
                     nextpage > 0 && setNextpage(nextpage - 1)

                  }
                  style={{width: '100px', border: 'none', height:'48px', color:'#ffffff',textAlign: 'left', fontSize:'15px', paddingLeft:'8px'}}>
                    Précédent
                  </Button>
                  <span>
                      <input
                        to='/transactions'
                        type='number'
                        className='paginate_button_client  '
                        onChange={e => setNextpage(e.target.value)}
                      value={nextpage}
                      style={{width: '100px', border: 'none', height:'99%', textAlign: 'center', fontSize:'15px'}}
                      />
                  </span>
                  <Button
                  style={{width: '100px', border: 'none', height:'48px', color:'#ffffff',textAlign: 'center', fontSize:'15px', padding:'2px'}}

                    onClick={() =>
                     nextpage > 0 && setNextpage(nextpage + 1)
                    }
                  >
                    Suivant
                  </Button>
                </div>

              </div>
         }
         </>
         )}
      </Fragment>
   );
};

export default ClientList;
