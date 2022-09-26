import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
import { Link } from "react-router-dom";
import useAxios from "../useAxios";
import useAuth from "../useAuth";

const UserList = () => {
const api = useAxios();
const [usersData, setUsersData] = useState([]);
const [userModal, setUserModal] = useState(false);
const [userId, setUserId] = useState("");
const [selectedUser, setSelectedUser] = useState("");


const [userGroup, setUserGroup] = useState([]);
const [groups, setGroups] = useState([]);
// const [usersStatus, setUsersStatus] = useState(null);
const usersEnd= `${process.env.REACT_APP_API_URL}/rest-api/auth/users`
const groupsEnd = `${process.env.REACT_APP_API_URL}/rest-api/auth/groups/`
      // eslint-disable-next-line react-hooks/exhaustive-deps
      useEffect(  () =>  {
          api.get(usersEnd).then( res => {
            console.log('result ', res);
            setUsersData(res.data.results)
            // setUsersStatus(res.status)
         }).catch( err => {
            console.log('IRRROR', err);
            // setUsersStatus(err.response.status)
         })
         api.get(groupsEnd).then( res => {
            setGroups(res.data)
            console.log("MY GROUSP ", res.data);
      })
      }, [usersEnd, groupsEnd]);

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
                                       <Link to={`/user/${user.id}`}>{user.email}</Link>
                                    </td>
                                    <td >{user.first_name}</td>
                                    <td >{user.last_name }</td>
                                    <td className=" text-left">{user.get_first_group}</td>
                                    <td className=" text-right text-danger">{user.is_active}</td>
                                 </tr>
                              ))}
                              </tbody>
                        </table>
                     </div>
                  </div>
               </div>
            </div>
            {/* <PresenceEditModal show={editModal} onShowShange={setEditModal} presenceData={{presenceId:presenceId, client:client, hourIn:hourIn, hourOut: hourOut, creneau:creneau, note:note, clientId:clientId, date:date, activity:activity}}/>
            <PresenceCreateModal show={presneceCreateModal} onShowShange={setPresneceCreateModal} /> */}
         </div>
        
         </>
         )}
      </Fragment>
   );
};

export default UserList;
