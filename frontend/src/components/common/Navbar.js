import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">SmarTest AI</div>
      <ul className="navbar-links">
        <li>
          <NavLink 
            to="/minmax" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            MinMax (Alpha-Beta)
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/nash" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            Nash Equilibrium
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/strategy" 
            className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
          >
            Strategy Selection
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;