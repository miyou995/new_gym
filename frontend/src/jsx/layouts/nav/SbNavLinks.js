import React from 'react'
import { Link, NavLink } from 'react-router-dom'

function SbNavLinks({LinkName,Icon, Name}) {
  return (
    <>
        <li>
            <NavLink  to={LinkName} activeStyle={{background: "#6418C3" , color: "white",textDecoration:"none"}}>
                <i className={`${Icon}  "active" ? "bg-gray" : "bg-light" `}></i>
                <span className="nav-text">{Name}</span>
            </NavLink>
        </li>
    </>
  )
}

export default SbNavLinks