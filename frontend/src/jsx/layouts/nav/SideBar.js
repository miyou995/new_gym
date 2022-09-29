import React,  {useState, Component, useEffect } from "react";

/// Link
import { Link } from "react-router-dom";

/// Scroll
import PerfectScrollbar from "react-perfect-scrollbar";

/// Menu
import MetisMenu from "metismenujs";
import useAxios from "../../components/useAxios";
import useAuth from "../../components/useAuth"
import SbNavLinks from "./SbNavLinks";
// import useAaxios from "../../components/useAaxios";
///
// import drump from "../../../images/card/drump.png";

class MM extends Component {
   componentDidMount() {
      this.$el = this.el;
      this.mm = new MetisMenu(this.$el);
   }
   componentWillUnmount() {
      //  this.mm("dispose");
      // console.log(this.mm);
   }
   render() {
      return (
         <div className="mm-wrapper">
            <ul className="metismenu" ref={(el) => (this.el = el)}>
               {this.props.children}
            </ul>
         </div>
      );
   }
}

const SideBar =  () => {
//       this.mm = new MetisMenu(this.$el);
const [path,setPath] = useState("");
   useEffect(()=>{
      var btn = document.querySelector(".nav-control");
      var aaa = document.querySelector("#main-wrapper");

      function toggleFunc() {
         return aaa.classList.toggle("menu-toggle");
      }

      btn.addEventListener("click", toggleFunc);
   },[]) 
   

   const api = useAxios();
   const baseURL = `${process.env.REACT_APP_API_URL}`


   const clientAuthorizationEnd = `${baseURL}/rest-api/get_client_authorization/`
   const transactionAuthorization = `${baseURL}/rest-api/transactions/get_transaction_authorization/`;
   const coachAuthorizationEnd = `${baseURL}/rest-api/get_coach_authorization/`
   let personnelAuthorization = `${baseURL}/rest-api/get_personnel_authorization/`
   let presenceAuthorization = `${baseURL}/rest-api/presence/get_presence_authorization/`

   const [clientAuth] = useAuth(clientAuthorizationEnd, 'GET')
   const [coachAuth] = useAuth(coachAuthorizationEnd, 'GET')
   const [transactionAuth] = useAuth(transactionAuthorization, 'GET')
   const [persoAuth] = useAuth(personnelAuthorization, 'GET')
   const [presenceAuth] = useAuth(presenceAuthorization, 'GET')


      return (
         <div className="deznav">
            <PerfectScrollbar className="deznav-scroll">
               <MM className="metismenu" id="menu">
                  {/* <SbNavLinks LinkName="" Icon="flaticon-381-home" Name="Tableau de bord" /> */}
                  {clientAuth && (
                     <SbNavLinks LinkName="/client" Icon="flaticon-381-user-9" Name="Abonnées" />
                  )}
                  {transactionAuth  && (
                     <SbNavLinks LinkName="/transactions" Icon="flaticon-381-controls" Name="Transactions" />
                  )}
                  <SbNavLinks LinkName="/creneaux" Icon="flaticon-381-calendar" Name="Creneaux" />
                  {presenceAuth &&
                     <SbNavLinks LinkName="/presences" Icon="flaticon-381-blueprint" Name="Présences" />
                  }
                  {coachAuth && (
                     <SbNavLinks LinkName="/coach" Icon="flaticon-381-user-1" Name="Coachs" />
                  )}
                  {persoAuth && 
                     <SbNavLinks LinkName="/personnel" Icon="flaticon-381-user-4" Name="Personnel" />
                  }
                  <SbNavLinks LinkName="/configuration" Icon="flaticon-381-settings" Name="configuration" />
                  <SbNavLinks LinkName="/users" Icon="flaticon-381-user-1" Name="Utilisateurs " />
                  <SbNavLinks LinkName="/history-abc" Icon="flaticon-381-bookmark-1" Name="History " />
                 </MM>
       
               <div className="copyright">
                  <p>
                     <strong>COPYRIGHT - OctoGym Dashboard</strong> © 2021 All
                     Rights Reserved
                  </p>
                  {/* <p>
                     Made with <i className="fa fa-heart" /> by DexignZone
                  </p> */}
               </div>
            </PerfectScrollbar>
         </div>
      );
   }
// }

export default SideBar;
