import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import './nv.css'

function SbNavLinks({ LinkName, Icon, Name }) {
  
    return (
        <>
            <li>
                <NavLink to={LinkName} activeClassName='activecn' activeStyle={{ background: "#6418C3", color: "white", borderRadius: '4px', textDecoration: "none" }}>
                    <i className={`${Icon} activei`}></i> 
                    <span className="nav-text">{Name}</span>
                </NavLink>
            </li>
        </>
    )
}

export default SbNavLinks