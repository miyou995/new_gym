import React from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

// Images
import transactionImg from "../../images/profile/transaction.png";
import creneauImg from "../../images/profile/creneau.png";
import abonnementImg from "../../images/profile/abonnement.png";
import clientsImg from "../../images/profile/clients.png";
import cochsImg from "../../images/profile/coach.png";
import presencesImg from "../../images/profile/presences.png";
import tresorieImg from "../../images/profile/tresorie.png";
import dashboardImg from "../../images/profile/dashboard.png";
import confImg from "../../images/profile/gear.png";
import stafImg from "../../images/profile/waiter.png";
import { Link } from "react-router-dom";

function SampleNextArrow(props) {
  const { onClick } = props;
  return (
    <div className="conteact-next c-pointer" onClick={onClick}>
      <i className="las la-long-arrow-alt-right" />
    </div>
  );
}

const ShortCuts = () => {
  const settings = {
    slidesToShow: 9,
    slidesToScroll: 1,
    dots: false,
    autoplay: false,
    // autoplaySpeed: 2000,
    centerMode: true,
    // infinite: true,
    // touchMove: true,
    className: "contacts-card",
    centerPadding: "60px",
    speed: 100,
    accessibility: false,
    nextArrow: <SampleNextArrow />,
    responsive: [
      {
        breakpoint: 1200,
        settings: {
          slidesToShow: 7,
          slidesToScroll: 1,
        },
      },
      {
        breakpoint: 991,
        settings: {
          slidesToShow: 5,
          slidesToScroll: 1,
          centerPadding: 0,
          centerMode: false,
        },
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 1,
        },
      },
      {
        breakpoint: 360,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 1,
        },
      },
    ],
  };
  return (
    <Slider {...settings}>
      <Link to="/">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={dashboardImg}  />
            <h6 className=" mb-0 text-center">Tableau de board</h6>
            {/* <span className="fs-12">Gestion des transaction</span> */}
          </div>
        </div>
      </Link>
      <Link to="/transactions">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={transactionImg}  />
            <h6 className=" mb-0 text-center">Transactions</h6>
            {/* <span className="fs-12">Gestion des transaction</span> */}
          </div>
        </div>
      </Link>
      {/* <Link to="/Abonnements">
         <div className="items">
            <div>
               <img className="mb-3 ml-auto mr-auto" src={abonnementImg} alt />
               <h6 className=" mb-0 text-center">Abonnements</h6>
            </div>
         </div>
         </Link> */}
      <Link to="/client">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={clientsImg}  />
            <h6 className=" mb-0 text-center">Clients</h6>
            {/* <span className="fs-12">Gestion des clients</span> */}
          </div>
        </div>
      </Link>
      <Link to="/coach">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={cochsImg}  />
            <h6 className=" mb-0 text-center">Coachs </h6>
            {/* <span className="fs-12">Gestion des coachs</span> */}
          </div>
        </div>
      </Link>
      <Link to="/personnel">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={stafImg}  />
            <h6 className=" mb-0 text-center">Personnels </h6>
            {/* <span className="fs-12">Gestion des coachs</span> */}
          </div>
        </div>
      </Link>
      <Link to="/presences">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={presencesImg}  />
            <h6 className=" mb-0 text-center">Présences </h6>
            {/* <span className="fs-12">Gestion des présences</span> */}
          </div>
        </div>
      </Link>
      <Link to="/tresorie">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={tresorieImg}  />
            <h6 className=" mb-0 text-center">Chiffre d'affiare</h6>
          </div>
        </div>
      </Link>
      <Link to="/creneaux">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={creneauImg}  />
            <h6 className=" mb-0 text-center">Créneaux</h6>
            {/* <span className="fs-12">Gestion des Créneaux</span> */}
          </div>
        </div>
      </Link>
      <Link to="/configuration">
        <div className="items">
          <div>
            <img className="mb-3 ml-auto mr-auto" src={confImg}  />
            <h6 className=" mb-0 text-center">Configuration</h6>
            {/* <span className="fs-12">Créer/Supprimer</span> */}
          </div>
        </div>
      </Link>
    </Slider>
  );
};

export default ShortCuts;
