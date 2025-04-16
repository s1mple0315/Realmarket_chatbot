import { BrowserRouter as Router, Route, NavLink } from "react-router-dom";
import HomePage from "../../pages/HomePage/HomePage";

const Router = () => {
  return (
    <Router>
      <Route path="/" exact component={<HomePage />} />
    </Router>
  );
};

export default Router;
