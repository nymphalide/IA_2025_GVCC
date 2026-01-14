import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <h2 className="navbar-brand">SmarTest</h2>
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
            to="/strategy"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            Strategy
          </NavLink>
        </li>

        {/* Added RL Link */}
        <li>
          <NavLink
            to="/rl"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            RL
          </NavLink>
        </li>

        {/* Added CSP Link */}
        <li>
          <NavLink
            to="/csp"
            className={({ isActive }) =>
              isActive ? "nav-link active" : "nav-link"
            }
          >
            CSP
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;