import React from "react";

const Footer = () => {
  var d = new Date();
  return (
    <div className="footer">
      <div className="copyright">
        <p>
          Copyright 2021 © Designed &amp; Developed by{" "}
          <a href="https://octopus-consulting.com/" target="_blank">
            Octopus Consulting
          </a>{" "}
          {d.getFullYear()}
        </p>
      </div>
    </div>
  );
};

export default Footer;
