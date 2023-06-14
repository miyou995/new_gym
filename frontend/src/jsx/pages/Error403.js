import React from "react";
import { Link } from "react-router-dom";

const Error403 = () => {
   return (
      <div className="authincation">
         <div className="container mt-0">
            <div className="row justify-content-center align-items-center ">
               <div className="col-md-5">
                  <div className="form-input-content text-center error-page">
                     <h1 className="error-text  font-weight-bold">403</h1>
                     <h4>
                        <i className="fa fa-times-circle text-danger" />{" "}
                        Forbidden Error!
                     </h4>
                     <p>Vous n'avez pas le droit de visiter cette page.</p>
                     <div>
                        <Link className="btn btn-primary" to="/">
                           Retourner A l'accueil
                        </Link>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </div>
   );
};

export default Error403;
