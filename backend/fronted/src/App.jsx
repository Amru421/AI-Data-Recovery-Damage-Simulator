import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Recovery from "./pages/Recovery";
import Artifact from "./pages/Artifact";

function App() {

  return (
    <BrowserRouter>

      <div className="app">

        <nav className="navbar">
          <Link className="brand" to="/">
            <span className="brand-mark">RX</span>
            <span>
              <strong>RecoverX</strong>
              <small>evidence intelligence</small>
            </span>
          </Link>

          <div className="nav-links">

            <Link to="/">Overview</Link>
            <Link to="/recovery">Recovery lab</Link>

          </div>

          <div className="nav-status"><span /> Engine online</div>

        </nav>

        <Routes>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/recovery"
            element={<Recovery />}
          />

          <Route
            path="/artifact/:id"
            element={<Artifact />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  );
}

export default App;