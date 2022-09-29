import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown } from "react-bootstrap";
import useAxios from "../useAxios";
import Search from "../../layouts/Search";

/// images
import avartar5 from "../../../images/avatar/5.png";
import avartar1 from "../../../images/avatar/1.png";
import { Link } from "react-router-dom";

import ShortCuts from "../ShortCuts";
import useAuth from "../useAuth";
import Error403 from "../../pages/Error403";




function refreshPage() {
   window.location.reload(false);
 }

 const CoachList = () => {
    const api = useAxios();
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
                   <Dropdown.Item href={`/coach/edit/${props.id}`}>Modifier</Dropdown.Item>
                   <Dropdown.Item type='button' className="text-danger" onClick={ () => {
                         api.delete(`${process.env.REACT_APP_API_URL}/rest-api/coachs/delete/${props.id}`).then(res=> {
                            refreshPage()
                         })
                        }}>
                       Supprimer
                    </Dropdown.Item>
                </Dropdown.Menu>
             </Dropdown>
    };

   const coachAuthorizationEnd = `${process.env.REACT_APP_API_URL}/rest-api/get_coach_authorization/`
   let endpoint = `${process.env.REACT_APP_API_URL}/rest-api/coachs/`

   
   const [coachData, setCoachData] = useState([]);
   const [coachStatus, setCoachStatus] = useState(null);
   // const savedCoachs = api.get(endpoint)
   
   useEffect(() => {
      api.get(endpoint).then( res=> {
         setCoachData(res.data)
         setCoachStatus(res.status);

      }).catch(err => {
         if (err.response) {
            console.log(err.response.data);
            console.log(err.response.status);
            console.log(err.response.headers);
            setCoachStatus(err.response.status);
      }})
      // const coachs = savedCoachs
   }, [endpoint]);
   // //console.log('els clieeents', savedClients);

   const [coachAuth, loading] = useAuth(coachAuthorizationEnd, 'GET')


   return (
      <Fragment>
         {loading &&
         <>
         {coachAuth ? (
            <>
         {/* <PageTitle activeMenu="Liste" motherMenu="Abonnées" /> */}
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div>

         <Search name= 'Ajouter Coach' lien= "/coach/create" placeHolder="Rechercher un coach"/>

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
                                 <th></th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                           {coachData.map(coach => (
                              <tr role="row" key={coach.id} className="btn-reveal-trigger">
                                 <td className="customer_shop_single"> {coach.id} </td>
                                 <td className="py-3">
                                    <Link to={`/coach/${coach.id}`}>
                                       <div className="media d-flex align-items-center">
                                          <div className="avatar avatar-xl mr-2">
                                             <div className="">
                                                <img className="rounded-circle img-fluid" src={avartar5} width="30" alt="" />
                                             </div>
                                          </div>
                                          <div className="media-body">
                                             <h5 className="mb-0 fs--1">
                                             {coach.last_name}
                                             </h5>
                                          </div>
                                       </div>
                                    </Link>
                                 </td>
                                 <td className="py-2">
                                    {coach.first_name}
                                 </td>
                                 <td className="py-2">
                                    <a href="tel:{coach.phone}">{coach.phone}</a>
                                 </td>
                                 <td className="py-2 pl-5 wspace-no"> {coach.adress} </td>
                                 <td className="py-2">30/03/2018</td>
                                 <td className="py-2 text-right">
                                    <Drop id={coach.id}/>
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
      </>
      ) : <Error403 />}
         </>
      }
      </Fragment>
   );
};

export default CoachList;
