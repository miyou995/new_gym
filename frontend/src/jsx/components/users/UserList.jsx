import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
import { Link } from "react-router-dom";
import useAxios from "../useAxios";
import useAuth from "../useAuth";
import UserModal from "./UserModal"
const UserList = () => {
const api = useAxios();
const [usersData, setUsersData] = useState([]);
const [userModal, setUserModal] = useState(false);
const [userId, setUserId] = useState("");
const [selectedUser, setSelectedUser] = useState("");

const [nextpage, setNextpage] = useState(1);
   
const [requestedUrl, setRequestedUrl] = useState(null);
const [nextUrl, setNextUrl] = useState("");
const [previusUrl, setPreviusUrl] = useState("");
const [userGroup, setUserGroup] = useState([]);
const [groups, setGroups] = useState([]);
// const [usersStatus, setUsersStatus] = useState(null);
const usersEnd= `${process.env.REACT_APP_API_URL}/rest-api/auth/users`
const groupsEnd = `${process.env.REACT_APP_API_URL}/rest-api/auth/groups/`
      // eslint-disable-next-line react-hooks/exhaustive-deps
      useEffect(  () =>  {
          api.get(usersEnd).then( res => {
            //console.log('result ', res);
            setUsersData(res.data.results)
            setNextUrl(res.data.next)
            setPreviusUrl(res.data.previous)
            // setUsersStatus(res.status)
         }).catch( err => {
            //console.log('IRRROR', err);
            // setUsersStatus(err.response.status)
         })
         api.get(groupsEnd).then( res => {
            setGroups(res.data)
            console.log("MY GROUSP ", res.data);
      })
      }, [usersEnd, groupsEnd]);
      useEffect(() =>  {
         if (requestedUrl) {
            api.get(requestedUrl).then(res => {
               //console.log('le resultat des clients est ', res);
               setUsersData(res.data.results)
               setNextUrl(res.data.next)
               setPreviusUrl(res.data.previous)
               console.log('le setNextUrl des ', nextUrl);     
               console.log('le setPreviusUrl des ', previusUrl);
            })
         }
      }, [requestedUrl]);
      
   const setSelectedGroup = (groups, groupId ) => {
      for (let i = 0; i < groups.length; i++) {
          if (groupId == groups[i].id){
             return i
          }            
      }
  }
   const userAuthorization = `${process.env.REACT_APP_API_URL}/rest-api/auth/users/`

   const userAuth = useAuth(userAuthorization, 'GET')

   console.log("userAuth=========================>", useAuth(userAuthorization, 'GET'));


   return (
      <Fragment>
         <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div>
         {userAuth && (
         <>
         <div className="form-head d-flex mb-4 mb-md-5 align-items-start">
            <div className="input-group search-area d-inline-flex">
            </div>
               <Button onClick={e => { setUserModal(true)}}>Ajouter</Button>
         </div>
            <div className="row">
            <div className="col-lg-12">
               <div className="card">
                  <div className="card-body" style={{padding: '5px'}}>
                     <div className="table-responsive">
                        <table className="table mb-0 table-striped">
                           <thead>
                              <tr>
                                 <th className="customer_shop">ID Utilisateur </th>
                                 <th> Email</th>
                                 <th> Nom </th>
                                 <th> Prénom </th>
                                 <th className="pl-5 width200">Role </th>
                                 <th className='text-right'>Actif </th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                              {usersData.map(user => (
                                 <tr role="row presences" key={user.id} className="btn-reveal-trigger cursor-abonnement presences p-0">
                                    <td className="customer_shop_single"> {user.id} </td>
                                    <td className="customer_shop_single"> 
                                       <Link to={`/users/${user.id}`}>{user.email}</Link>
                                    </td>
                                    <td >{user.first_name}</td>
                                    <td >{user.last_name }</td>
                                    <td className=" text-left" onClick={e => {
                                    console.log("THE USER", user);

                                    }}>{user.get_first_group}</td>
                                    <td className=" text-right text-danger">{user.is_active}</td>
                                 </tr>
                              ))}
                              </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>

         </div>
         <div className='d-flex text-center justify-content-end'>
                     <div className='dataTables_info text-black' id='example5_info '>

                     </div>
                     <div className='dataTables_paginate paging_simple_numbers' id='example5_paginate' >
                        {
                           previusUrl && 
                           <Button
                              onClick={() => {
                                 if( nextpage > 1 ) {
                                    setRequestedUrl(previusUrl)
                                    nextpage > 0 && setNextpage(nextpage - 1)
                                 }
                              }}
                              style={{ width: '100px', border: 'none', height: '48px', color: '#ffffff', textAlign: 'left', fontSize: '15px', paddingLeft: '8px' }}>
                              Précédent
                           </Button>
                        }
                        {
                         previusUrl ? <span className="m-3" >{nextpage}</span> : nextUrl ?  <span className="m-3" >{nextpage}</span> : ""
                        }
                        {
                           nextUrl && 
                           <Button
                              style={{ width: '100px', border: 'none', height: '48px', color: '#ffffff', textAlign: 'center', fontSize: '15px', padding: '2px' }}
                              onClick={() => {
                                 setRequestedUrl(nextUrl)
                                 nextpage > 0 && setNextpage(nextpage + 1)
                              }}
                           >
                              Suivant
                           </Button>
                        }
                     </div>

                  </div>
               <UserModal show={userModal} onShowShange={setUserModal}  userData={{
                  userId : userId,
                  selectedUser : setSelectedUser,
                  userGroup: userGroup,
                  groups : groups
                  // userGroop : userGroop,
               }} /> 
         </>
         )}
      </Fragment>
   );
};

export default UserList;
