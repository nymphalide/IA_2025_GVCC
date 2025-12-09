import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">SmarTest</div>

      <ul className="navbar-links">
        <li>
          <NavLink
            to="/minmax"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            MinMax
          </NavLink>
        </li>

        <li>
          <NavLink
            to="/nash"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Nash
          </NavLink>
        </li>

        <li>
          <NavLink
            to="/nqueens"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            N-Queens
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
