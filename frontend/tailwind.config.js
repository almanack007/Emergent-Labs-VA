/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        warmgreen: {
          DEFAULT: "#4CAF50",
          100: "#E8F5E9",
          200: "#C8E6C9",
          300: "#A5D6A7",
          400: "#81C784",
          500: "#66BB6A",
          600: "#4CAF50",
          700: "#43A047",
        },
        textblack: "#212121",
      },
      boxShadow: {
        soft: "0 6px 20px rgba(0,0,0,0.08)",
        card: "0 10px 30px rgba(0,0,0,0.08)",
      },
      borderRadius: {
        xl: "14px"
      }
    },
  },
  plugins: [],
}