import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/logister.css";

const Logister = () => {
  const [active, setActive] = useState(false);
  const [passwords, setPasswords] = useState({
    signIn: "",
    signUp: ""
  });
  const [showPassword, setShowPassword] = useState({
    signIn: false,
    signUp: false
  });

  // Alternar visibilidad de contraseña
  const togglePasswordVisibility = (formType) => {
    setShowPassword(prev => ({
      ...prev,
      [formType]: !prev[formType]
    }));
  };

  // Handlers para cambiar entre formularios
  const handleSignUpClick = () => setActive(true);
  const handleSignInClick = () => setActive(false);

  // Manejar cambios en contraseñas
  const handlePasswordChange = (formType, value) => {
    setPasswords(prev => ({
      ...prev,
      [formType]: value
    }));
  };

  // Manejar envío de formularios
  const handleSignInSubmit = (e) => {
    e.preventDefault();
    console.log("Intento de inicio de sesión");
  };

  const handleSignUpSubmit = (e) => {
    e.preventDefault();
    console.log("Intento de registro");
  };

  return (
    <div className={`container ${active ? "active" : ""}`}>
      {/* Área blanca con formulario */}
      <div className="box">
        {/* Formulario de Sign In */}
        <div className="form sign_in">
          <h3>Sign In</h3>
          <span>or use your account</span>
          <form onSubmit={handleSignInSubmit}>
            <div className="type">
              <input
                type="email"
                placeholder="Email"
                id="emailSignIn"
                required
              />
            </div>
            <div className="type password-container">
              <input
                type={showPassword.signIn ? "text" : "password"}
                placeholder="Password"
                id="passwordSignIn"
                required
                value={passwords.signIn}
                onChange={(e) => handlePasswordChange("signIn", e.target.value)}
              />
              {passwords.signIn.length > 0 && (
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility("signIn")}
                  className="password-toggle"
                >
                  {showPassword.signIn ? "🙈" : "👁️"}
                </button>
              )}
            </div>
            <div className="forgot">
              <span>Forgot your password?</span>
            </div>
            <button className="btn" type="submit">
              SIGN IN
            </button>
          </form>
        </div>

        {/* Formulario de Sign Up */}
        <div className="form sign_up">
          <h3>Sign Up</h3>
          <span>or use your email for registration</span>
          <form onSubmit={handleSignUpSubmit}>
            <div className="type">
              <input
                type="text"
                placeholder="Username"
                id="name"
                required
              />
            </div>
            <div className="type">
              <input
                type="email"
                placeholder="Email"
                id="emailSignUp"
                required
              />
            </div>
            <div className="type password-container">
              <input
                type={showPassword.signUp ? "text" : "password"}
                placeholder="Password"
                id="passwordSignUp"
                pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&]{8,}$"
                title="La contraseña debe tener al menos 8 caracteres, incluyendo una letra minúscula, una mayúscula, un número y un carácter especial"
                required
                value={passwords.signUp}
                onChange={(e) => handlePasswordChange("signUp", e.target.value)}
              />
              {passwords.signUp.length > 0 && (
                <button
                  type="button"
                  onClick={() => togglePasswordVisibility("signUp")}
                  className="password-toggle"
                >
                  {showPassword.signUp ? "🙈" : "👁️"}
                </button>
              )}
            </div>
            <button className="btn" type="submit">
              SIGN UP
            </button>
          </form>
        </div>
      </div>

      <div className="overlay">
        <div className="page page_signIn">
          <h3>Welcome Back!</h3>
          <p>To keep connected with us please login with your personal info</p>
          <button className="btn" onClick={handleSignUpClick}>
            SIGN UP
          </button>
        </div>

        <div className="page page_signUp">
          <h3>Hello Friend!</h3>
          <p>Enter your personal details and start journey with us</p>
          <button className="btn" onClick={handleSignInClick}>
            SIGN IN
          </button>
        </div>
      </div>
    </div>
  );
};

export default Logister;