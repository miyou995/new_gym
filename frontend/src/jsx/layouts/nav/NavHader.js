import React, { useState } from "react";

/// React router dom
import { Link } from "react-router-dom";

/// images
import logo from "../../../images/logo.png";

const NavHader = () => {
   const [toggle, setToggle] = useState(true);
   return (
      <div className="nav-header">
         <Link to="/" className="brand-logo">
            <img className="logo-abbr" src={logo} alt="" />
            <h2 className="brand-title font-weight-bold"> Gym </h2>
         </Link>

         <div className="nav-control" onClick={() => setToggle(!toggle)}>
            <div className={`hamburger ${toggle ? "is-active" : ""}`}>
               <span className="line"></span>
               <span className="line"></span>
               <span className="line"></span>
            </div>
         </div>
      </div>
   );
};

export default NavHader;
