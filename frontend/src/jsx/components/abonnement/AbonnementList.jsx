import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown } from "react-bootstrap";
import Search from "../../layouts/Search";
import ShortCuts from "../ShortCuts";
import useAxios from "../useAxios";
import { Link } from "react-router-dom";





const Drop = (props) => {
   return <Dropdown>
            <Dropdown.Toggle variant="" className="table-dropdown i-false">
               <svg width="24px" height="24px" viewBox="0 0 24 24" version="1.1">
                  <g stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
                     <rect x="0" y="0" width="24" height="24"></rect>
                     <circle fill="#000000" cx="5" cy="12" r="2"></circle>
                     <circle fill="#000000" cx="12" cy="12" r="2"></circle>
                     <circle fill="#000000" cx="19" cy="12" r="2"></circle>
                  </g>
               </svg>
            </Dropdown.Toggle>
            <Dropdown.Menu>
               <Dropdown.Item href={`/abonnements/edit/${props.id}`}>Modifier</Dropdown.Item>
               <Dropdown.Item type='button' className="text-danger" onClick={ async () => {
                    await useAxios.delete(`${process.env.REACT_APP_API_URL}/rest-api/abonnements/delete/${props.id}/`)
                    }}>
                   Supprimer
                </Dropdown.Item>
            </Dropdown.Menu>
         </Dropdown>
};



const PresenceList = () => {
   const api = useAxios();
   let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/abonnement/`
  const [savedAbonnements, setSavedAbonnements] = useState([])


   useEffect(() => {
      api.get(endpoint).then((res) => {
         savedAbonnements(res.data)
      })
    }, []);


   console.table('els clieeents', savedAbonnements);
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
            <Search name= 'Abonnée' lien= "/abonnements/create" displayInput="yes" placeholder="Rechercher un Adhérant"/>

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
                                 <th>Prix</th>
                                 <th> Durée (jours) </th>
                                 <th className="pl-5 width200"> Nombre de séances </th>
                                 <th> Activité </th>
                                 <th> Nombre d'inscrits </th>
                                 {/* <th>Adhesion</th>
                                 <th></th> */}
                              </tr>
                           </thead>
                           <tbody id="customers">
                           {savedAbonnements.map(abonnement => (
                              <tr role="row" key={abonnement.id} className="btn-reveal-trigger">
                                 <td className="customer_shop_single"> {abonnement.id} </td>
                                 <td className="py-3">
                                    <Link to={`/abonnement/detail/${abonnement.id}`}>
                                       <div className="media d-flex align-items-center">
                                        
                                          <div className="media-body">
                                             <h5 className="mb-0 fs--1">
                                             {abonnement.name}
                                             </h5>
                                          </div>
                                       </div>
                                    </Link>
                                 </td>
                                 <td className="py-2">{abonnement.price}</td>
                                 <td className="py-2">{abonnement.length}</td>
                                 <td className="py-2 pl-5 wspace-no"> {abonnement.seances_quantity} </td>
                                 <td className="py-2">{abonnement.activity_name}</td>
                                 <td className="py-2">{abonnement.clients_number}</td>
                                 <td className="py-2 text-right">
                                    <Drop id={abonnement.id}/>
                                 </td>
                              </tr>
                              ))}
                              </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </Fragment>
   );
};

export default PresenceList;
