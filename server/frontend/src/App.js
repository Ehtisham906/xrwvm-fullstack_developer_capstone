import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Register from './components/Register/Register.jsx';
import Dealers from './components/Dealers/Dealers.jsx';

function App() {
    return (
        <Routes>
            <Route path="/login" element={<LoginPanel />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dealers" element={<Dealers />} />
        </Routes>
    );
}
export default App;
