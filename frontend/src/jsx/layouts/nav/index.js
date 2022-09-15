import React, { Fragment, useState } from "react";
import SideBar from "./SideBar";
import NavHader from "./NavHader";
import Header from "./Header";
import { Link, useHistory, useRouteMatch } from "react-router-dom";

const JobieNav = ({ title, onClick: ClickToAddEvent, onClick2, onClick3 }) => {
   const [toggle, setToggle] = useState("");
   const onClick = (name) => setToggle(toggle === name ? "" : name);

   // const [NamesTab, setNamesTab] = useState(title);

   const [textTab, setTextTab] = useState(null);

   let match = window.location.pathname === "/";
   let match0 = window.location.pathname === "/client" ;
   let match1 = useRouteMatch("/transactions");
   let match2 = useRouteMatch("/creneaux");
   let match3 = useRouteMatch("/presences");
   let match4 = useRouteMatch("/coach");
   let match5 = useRouteMatch("/personnel");
   let match6 = useRouteMatch("/configuration");
   let match7 = useRouteMatch("/users");
   let match8 = useRouteMatch("/history-abc");
   let match9 = useRouteMatch("/tresorie");







   React.useEffect(() => {
      
      if (match) {
         setTextTab("Tableau de Board")
      }if (match0) {
         setTextTab("Client")
      }if(match1){
         setTextTab("Transactions")
      }if (match2) {
         setTextTab("Créneaux")
      }if (match3) {
         setTextTab("Présences")
      }if (match4) {
         setTextTab("Coachs")
      }if (match5) {
         setTextTab("Personnels")
      }if(match6){
         setTextTab("Configuration")
      }if (match7) {
         setTextTab("Users")
      }if (match8) {
         setTextTab("History")
      }if (match9) {
         setTextTab("Trésorie")
      }
   }, [match,match0,match1,match2,match3,match4,match5,match6,match7,match8,match9]);
  

   return (
      <Fragment>
         <NavHader />
         <SideBar onClick={() => onClick2()} onClick3={() => onClick3()}  />
         <Header
            textTab={textTab}
            onNote={() => onClick("chatbox")}
            onNotification={() => onClick("notification")}
            onProfile={() => onClick("profile")}
            toggle={toggle}
            title={title}
            onBox={() => onClick("box")}
            onClick={() => ClickToAddEvent()}
         />
      </Fragment>
   );
};

export default JobieNav;
