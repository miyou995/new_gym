import React,  {useState, Component, useEffect } from "react";

/// Link
import { Link } from "react-router-dom";

/// Scroll
import PerfectScrollbar from "react-perfect-scrollbar";

/// Menu
import MetisMenu from "metismenujs";
import useAxios from "../../components/useAxios";
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
   
   //notice the empty array here
   /// Open menu
   // componentDidMount() {
   //    // sidebar open/close
   //    var btn = document.querySelector(".nav-control");
   //    var aaa = document.querySelector("#main-wrapper");

   //    function toggleFunc() {
   //       return aaa.classList.toggle("menu-toggle");
   //    }

   //    btn.addEventListener("click", toggleFunc);
   // }
   // return() {
   //    /// Path
   //    let path = window.location.pathname;
   //    path = path.split("/");
   //    path = path[path.length - 1];

   //    /// Active menu
   //    let app = ["",],
   //       abon = ["abonnees",'client'],
   //       // tresor = ["tresorie",],
   //       trans = ["transactions",],
   //       plan = ["planning",],
   //       // cren = ["creneaux",],
   //       // salles = ["salles",],
   //       // activit = ["activites",],
   //       presen = ["presences",],
   //       // coachPersonnel = ["coachs-personnels",],
   //       table = ["table-bootstrap-basic", "table-datatable-basic"],
   //       config = ["configuration"];

   const api = useAxios();

   // const [uStatus, setUStatus] = useState(null);

   // api.get(`${process.env.REACT_APP_API_URL}/rest-api/clients-name-drop/`).then(res => {
   //    console.log(res.status);
   //    setUStatus(res.status);
   // }).catch(error => {
   //    if (error.response) {
   //       console.log(error.response.data);
   //       console.log(error.response.status);
   //       console.log(error.response.headers);
   //       setUStatus(error.response.status);
   //    }
   // })

   // const [TransactionsStatus, setTransactionStatus] = useState()
   const [nextpage, setNextpage] = useState(1);
   const baseURL = `${process.env.REACT_APP_API_URL}`
   // const tansactionsURL = `${baseURL}/rest-api/clients-name-drop/`;
   var cURL = `${baseURL}/rest-api/clients-name/?page=${nextpage}`;
   var coachURL = `${baseURL}/rest-api/coachs`

   // const { transactionStatus } = useAaxios(tansactionsURL, 'GET');
   // const { clientStatus } = useAaxios(cURL, 'GET');
   // const { coachStatus } = useAaxios(coachURL, 'GET');
   const { clientStatus } = true;
   const { coachStatus } = true;

  


      return (
         <div className="deznav">
            <PerfectScrollbar className="deznav-scroll">
               <MM className="metismenu" id="menu">
                  {/* <SbNavLinks LinkName="" Icon="flaticon-381-home" Name="Tableau de bord" /> */}
                  {clientStatus == 200 && (
                     <SbNavLinks LinkName="/client" Icon="flaticon-381-user-9" Name="Abonnées" />
                  )}
                  {/* {transactionStatus === 200 && ( */}
                     <SbNavLinks LinkName="/transactions" Icon="flaticon-381-controls" Name="Transactions" />
                  {/* )} */}
                  <SbNavLinks LinkName="/creneaux" Icon="flaticon-381-calendar" Name="Creneaux" />
                  <SbNavLinks LinkName="/presences" Icon="flaticon-381-blueprint" Name="Présences" />
                  {coachStatus == 200 && (
                     <SbNavLinks LinkName="/coach" Icon="flaticon-381-user-1" Name="Coachs" />
                  )}
                  <SbNavLinks LinkName="/personnel" Icon="flaticon-381-user-4" Name="Personnel" />
                  <SbNavLinks LinkName="/configuration" Icon="flaticon-381-settings" Name="configuration" />
                  <SbNavLinks LinkName="/users" Icon="flaticon-381-user-1" Name="Utilisateurs " />
                  <SbNavLinks LinkName="/history-abc" Icon="flaticon-381-bookmark-1" Name="History " />
                  {/* <li className={`${ path ? "mm-active" : ""}`}>
                     <Link className="has-arrow ai-icon" to="#">
                        <i className="flaticon-381-home"></i>
                        <span className="nav-text">Tableau de bord</span>
                     </Link>
                     <ul>
                        <li>
                           <Link className={`${path === "" ? "mm-active" : ""}`} to="/" onClick={() => this.props.onClick()}>
                              Tableau de bord
                           </Link>
                        </li>
                     </ul>
                  </li> */}
                  {/* DASHBOARD */}
                  {/* <li className={`${tresor.includes(path) ? "mm-active" : ""}`}>
                     <Link to="/tresorie">
                        <i className="flaticon-381-television"></i>
                        <span className="nav-text">Trésorie</span>
                     </Link>
                  </li> */}
                  {/* Fin trésorie */}
                  {/* <li>
                     <Link to="/client">
                        <i className="flaticon-381-user-9"></i>
                        <span className="nav-text"> Abonnées </span>
                     </Link>
                  </li> */}
                  {/* Fin ABonnées */}
                  {/* <li>
                     <Link to="/transactions">
                        <i className="flaticon-381-controls"></i>
                        <span className="nav-text">Transactions</span>
                     </Link>
                  </li>
                  <li>
                     <Link to="/creneaux">
                        <i className="flaticon-381-calendar"></i>
                        <span className="nav-text">Créneaux</span>
                     </Link>
                  </li> */}
                  {/* <li
                     className={`${plan.includes(path) ? "mm-active" : ""}`}>
                     <Link className="has-arrow ai-icon" to="/planning">
                        <i className="flaticon-381-networking"></i>
                        <span className="nav-text">Planning</span>
                     </Link>
                     <ul>
                        <li>
                           <Link className={`${cren.includes(path) ? "mm-active" : ""}`} to="/creneaux" onClick={() => this.props.onClick()}>
                              Créneaux
                           </Link>
                        </li>
                        <li>
                           <Link className={`${salles.includes(path) ? "mm-active" : ""}`} to="/salles" onClick={() => this.props.onClick()} >
                              Salles
                           </Link>
                        </li>
                        <li>
                           <Link className={`${activit.includes(path) ? "mm-active" : ""}`} to="/activites" onClick={() => this.props.onClick()} >
                              Activités
                           </Link>
                        </li>
                     </ul>
                  </li> */}
                  {/* Fin planning */}
                  {/* <li>
                     <Link to="/presences">
                        <i className="flaticon-381-blueprint"></i>
                        <span className="nav-text">Présences</span>
                     </Link>
                  </li> */}
                  {/* Fin présences */}
                  {/* Coaches & personnel */}
                  {/* <li>
                     <Link className="has-arrow ai-icon" to="#">
                        <i className="flaticon-381-user-5"></i>
                        <span className="nav-text">Coachs & Personnels</span>
                     </Link>
                     <ul>
                        <li>
                           <Link className={`${path === "table-bootstrap-basic"? "mm-active": ""}`} onClick={() => this.props.onClick()} to="/coach">
                              Coachs
                           </Link>
                        </li>
                        <li>
                           <Link className={`${ path === "table-datatable-basic" ? "mm-active" : ""}`} onClick={() => this.props.onClick()} to="/personnel">
                              Personnel
                           </Link>
                        </li>
                     </ul>
                  </li>
                  <li>
                     <Link to="/configuration">
                        <i className="flaticon-381-settings"></i>
                        <span className="nav-text">configuration</span>
                     </Link>
                  </li>
                  <li>
                     <Link to="/users">
                        <i className="flaticon-381-user-1"></i>
                        <span className="nav-text">Utilisateurs</span>
                     </Link>
                  </li>
                  <li>
                     <Link to="/history-abc">
                        <i className="flaticon-381-bookmark-1"></i>
                        <span className="nav-text">Historique</span>
                     </Link>
                  </li> */}
                     {/* <ul>
                        <li>
                           <Link className={`${path === "table-bootstrap-basic"? "mm-active": ""}`} onClick={() => this.props.onClick()} to="/table-bootstrap-basic">
                              Admins
                           </Link>
                        </li>
                        <li>
                           <Link className={`${ path === "table-datatable-basic" ? "mm-active" : ""}`} onClick={() => this.props.onClick()} to="/table-datatable-basic">
                              Parametres
                           </Link>
                        </li>
                        <li>
                           <Link className={`${ path === "abonnements" ? "mm-active" : ""}`} onClick={() => this.props.onClick()} to="/abonnements">
                              Abonnements
                           </Link>
                        </li>
                     </ul> */}
                  {/* <li className={`${presen.includes(path) ? "mm-active" : ""}`}>
                     <Link to="/presences">
                        <i className="flaticon-381-television"></i>
                        <span className="nav-text">Présences</span>
                     </Link>
                  </li> */}
                  {/* Fin configurations */}
                   {/* <li className={`${table.includes(path) ? "mm-active" : ""}`}>
                     <Link className="has-arrow ai-icon" to="#">
                        <i className="flaticon-381-network"></i>
                        <span className="nav-text">Table</span>
                     </Link>
                     <ul>
                        <li>
                           <Link className={`${path === "table-bootstrap-basic" ? "mm-active" : ""}`} onClick={() => this.props.onClick()} to="/table-bootstrap-basic">
                              Bootstrap
                           </Link>
                        </li>
                        <li>
                           <Link className={`${  path === "table-datatable-basic" ? "mm-active" : "" }`} onClick={() => this.props.onClick()} to="/table-datatable-basic" >
                              Datatable
                           </Link>
                        </li>
                     </ul>
                  </li> */}
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
