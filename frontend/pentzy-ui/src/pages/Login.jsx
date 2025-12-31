import API from "../api/api";

export default function Login() {
  const handleLogin = async (e) => {
    e.preventDefault();

    const form = e.target;
    const data = new URLSearchParams();
    data.append("username", form.username.value);
    data.append("password", form.password.value);

    try {
      const res = await API.post("/auth/login", data, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      alert("Invalid credentials");
      console.error(err.response?.data || err.message);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Pentzy Login</h2>

      <input
        name="username"
        placeholder="Username"
        required
      />

      <input
        name="password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit">Login</button>
    </form>
  );
}
