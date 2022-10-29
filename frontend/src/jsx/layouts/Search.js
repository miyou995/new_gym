import React, {useContext}  from "react";
import { Link } from "react-router-dom";
import searchIcon from "../../images/icons/loupe.png";



const Search = (props) => {
   // const context = useContext({ClientContext,SerchPlanContext})

  return (
      <div className="form-head d-flex mb-4 mb-md-5 align-items-start">
         {
            props.displayInput
            &&
         <div className="input-group search-area d-inline-flex">
            <div className="input-group-append">
               <span className="input-group-text">
               <img src={searchIcon} width="22" />

                  {/* <i className="flaticon-381-search-2" /> */}
               </span>
            </div>
            <input type="text" className="form-control" placeholder={props.placeHolder} />
         </div>
         }
         <Link to={props.lien} className="btn btn-primary ml-auto">
               {props.name} 
         </Link>
      </div>
  );
};

export default Search;
