import React from 'react'
import UpdateIcon from '@material-ui/icons/Update';
import DeleteIcon from '@material-ui/icons/Delete';


function Users({usersData,setUserId, setSelectedUser, setUserGroup, userGroup, loading}) {

    if (loading) {
        return <h2>Loading...</h2>;
    }

  return (
    <>
          {usersData.map(user => (
              <>
                  <tr role="row" key={user.id} className="btn-reveal-trigger presences cursor-abonnement" onClick={e => {
                      setUserId(user.id)
                      setSelectedUser(user)
                      setUserGroup(user.groups)
                      // setUserModal(true)
                      console.log('user data-> ', user);
                      console.log("user group", userGroup);
                  }}>
                      <td className=" pl-5"> {user.id} </td>
                      <td className="customer_shop_single">
                          <div className="media d-flex align-items-center">
                              <div className="media-body">
                                  <h5 className="mb-0 fs--1">
                                      {user.email}
                                      {/* <Link to={"users/edit"}> */}
                                      {/* <span>Update</span> */}
                                      {/* </Link> */}
                                  </h5>
                              </div>
                          </div>
                      </td>
                      <td className="text-center">
                          <a href={`/user/edit/${user.id}`}>
                              <UpdateIcon fontSize="1rem" className='' />
                              <span className="text-center">Modifier</span>

                          </a>
                      </td>
                      {/* <td className="text-center">
                                    <a className="text-danger" onClick={async () => {
                                       await useAxios.delete(`${process.env.REACT_APP_API_URL}/rest-api/users/delete/${user.id}`)
                                    }}>
                                       <DeleteIcon fontSize="1rem" />
                                       <span className="text-center">Supprimer</span>

                                    </a>
                                 </td> */}

                  </tr>

              </>
          ))}
    </>
  )
}

export default Users