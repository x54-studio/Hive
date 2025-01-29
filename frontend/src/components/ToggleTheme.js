const [theme, setTheme] = useState("light");

const toggleTheme = () => {
  setTheme(theme === "light" ? "dark" : "light");
};

return (
  <div className={theme === "light" ? "bg-white text-black" : "bg-black text-white"}>
    <button onClick={toggleTheme}>Toggle Theme</button>
  </div>
);
