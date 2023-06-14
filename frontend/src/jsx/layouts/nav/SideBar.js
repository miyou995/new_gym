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
import agendaIcon from "../../../images/icons/agenda.png";
import presenceIcon from "../../../images/icons/attendance.png";
import planningIcon from "../../../images/icons/calendar.png";
import coachIcon from "../../../images/icons/coach.png";
import clientIcon from "../../../images/icons/people.png";
import transactionIcon from "../../../images/icons/transaction.png";
import userIcon from "../../../images/icons/user.png";
import configIcon from "../../../images/icons/setting.png";

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
                     <SbNavLinks LinkName="/client" Icon={clientIcon} Name="Abonnées" />
                  )}
                  {transactionAuth  && (
                     <SbNavLinks LinkName="/transactions" Icon={transactionIcon} Name="Transactions" />
                  )}
                  <SbNavLinks LinkName="/creneaux" Icon={planningIcon} Name="Creneaux" />
                  {presenceAuth &&
                     <SbNavLinks LinkName="/presences" Icon={presenceIcon} Name="Présences" />
                  }
                  {coachAuth && (
                     <SbNavLinks LinkName="/coach" Icon={coachIcon} Name="Coachs" />
                  )}
                  {persoAuth && 
                     <SbNavLinks LinkName="/personnel" Icon={userIcon} Name="Personnel" />
                  }
                  <SbNavLinks LinkName="/configuration" Icon={configIcon} Name="configuration" />
                  <SbNavLinks LinkName="/users" Icon={userIcon} Name="Utilisateurs " />
                  {/* <SbNavLinks LinkName="/history-abc" Icon={agendaIcon} Name="History " /> */}
                 </MM>
       
               <div className="copyright">
                  <p>
                     <strong>COPYRIGHT - OctoGym Dashboard</strong> © 2022 All
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
