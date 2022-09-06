import React, { Fragment , useState, useEffect} from "react";
import PageTitle from "../../layouts/PageTitle";
import { Dropdown, Button } from "react-bootstrap";
import ShortCuts from "../ShortCuts";
import { ToastContainer, toast } from 'react-toastify'
// import DetteCreateModal from './DetteCreateModal';
/// images 
import { Link } from "react-router-dom";
import useAxios from "../useAxios";
import UserModal from "./UserModal"
// import EditForm from "./EditForm";
// import UpdateIcon from '@material-ui/icons/Update';
// import DeleteIcon from '@material-ui/icons/Delete';

import Pagination from "./Pagination.js";
import Users from "./Users";
const UserList = () => {

const api = useAxios();
const [usersData, setUsersData] = useState([]);
const [userModal, setUserModal] = useState(false);
const [userId, setUserId] = useState("");
const [selectedUser, setSelectedUser] = useState("");


const [userGroup, setUserGroup] = useState([]);
const [groups, setGroups] = useState([]);

const groupsEnd = `${process.env.REACT_APP_API_URL}/rest-api/auth/groups/`

   useEffect( () =>  {
      api.get(`${process.env.REACT_APP_API_URL}/rest-api/auth/users`).then( res => {
         console.log('result ', res);
         setUsersData(res.data)
      }).catch( err => {
         console.log('IRRROR', err);
      })
      api.get(groupsEnd).then( res => {
         setGroups(res.data)
         console.log("MY GROUSP ", res.data);
     })
   }, [userModal]);

   const setSelectedGroup = (groups, groupId ) => {
      for (let i = 0; i < groups.length; i++) {
          if (groupId == groups[i].id){
             return i
          }            
      }
  }
   // const [users, setUsers] = useState([]);
   const [loading, setLoading] = useState(false);
   const [currentPage, setCurrentPage] = useState(1);
   const [UserPerPage] = useState(2);

  const indexOfLastUser = currentPage * UserPerPage;
  const indexOfFirstUser = indexOfLastUser - UserPerPage;
  const currentUsers = usersData.slice(indexOfFirstUser, indexOfLastUser);

   const paginate = pageNumber => setCurrentPage(pageNumber);
  
   return (
      <Fragment>
         <ToastContainer position='top-right' autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
         <div className="testimonial-one owl-right-nav owl-carousel owl-loaded owl-drag mb-4">
            <ShortCuts />
         </div>
         <div className="form-head d-flex mb-4 mb-md-5 align-items-start">
            <div className="input-group search-area d-inline-flex">
            </div>
               <Button onClick={e => { setUserModal(true)}}>Ajouter</Button>
            {/* <Link to="/users/create" className="btn btn-primary ml-auto">Ajouter un utilisateur</Link> */}
         </div>
            {/* <Search name= 'Abonnée' lien= "/client/create"/> */}
            {/* <div className="row d-flex justify-content-arround mb-3">
                  <div className="btn btn-success ml-auto" onClick={e => setPaiementModal(true) }>
                     + Paiement 
                  </div>
                  <div className="btn btn-danger ml-auto" onClick={e => setRemunerationPersonnelModal(true) }>
                  + Remunération Personnel 
                  </div>
                  <div className="btn btn-info ml-auto" onClick={e => setRemunerationCoachModal(true) }>
                  + Remunération Coach
                  </div>
                  <div className="btn btn-primary ml-auto" onClick={e => setAutreModal(true) }>
                  + Autre Transaction
                  </div>
                <div className="col-md-2">
                      <input type="date" name="birth_date" value={startDate} className="form-control"  onChange={e => setStartDate(e.target.value)}/>
               </div>
               <div className=" col-md-2">
                     <input type="date" name="birth_date" value={endDate} className="form-control"  onChange={e => setEndDate(e.target.value)}/>
               </div>
            </div> */}

         <div className="row">
            <div className="col-lg-12">
               <div className="card">
                  <div className="card-body" style={{padding: '5px'}}>
                     <div className="table-responsive">
                        <table className="table mb-0 table-striped">
                           <thead>
                              <tr>
                                 <th>ID</th>
                                 <th>Email</th>
                              </tr>
                           </thead>
                           <tbody id="customers">
                              <Users usersData={currentUsers} setUserId={setUserId} setSelectedUser={setSelectedUser}
                              setUserGroup={setUserGroup} userGroup={userGroup} loading={loading}/>
                           </tbody>
                        </table>
                        <Pagination
                           UserPerPage={UserPerPage}
                           totalUsers={usersData.length}
                           paginate={paginate}
                        />
 
                        
                     </div>
                  </div>
               </div>
            </div>
         </div>
         { userModal == true && 
         <UserModal show={userModal} onShowShange={setUserModal}  userData={{
            userId : userId,
            selectedUser : setSelectedUser,
            userGroup: userGroup,
            groups : groups
            // userGroop : userGroop,
            }}
           />
         }

            {/* <EditForm show={userModal} onShowShange={setUserModal} userData={{
               userId: userId,
            }} /> */}
      </Fragment>
   );
};

export default UserList;
