module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      backgroundImage: {
        experimental: "url('../public/img/foto34.jpeg')",
        experimental2: "url('../public/img/foto38.jpeg')",
        experimental3: "url('../public/img/foto39.jpeg')",
        experimental4: "url('../public/img/foto40.jpeg')",
        experimental5: "url('../public/img/foto30.jpeg')",
        experimental6: "url('../public/img/foto28.jpeg')",
        experimental7: "url('../public/img/foto35.jpeg')",
        experimental8: "url('../public/img/foto24.jpeg')",
        home: "url('../public/img/foto8.jpeg')",
      },
    },
  },
  backgroundcolor:(theme) => ({
    ...theme("colors"),
    primary: "#f28005",
    secundary:"#07fade",
    terciary:"#f28005",
  }),
  textColor: {
    primary: "",
    secundary:"",
    terciary:"",
  },
  plugins: [],
};
