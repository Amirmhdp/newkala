// const colors = require('tailwindcss/colors');
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./build/**/*.html'],
  theme: {
    extend: {},
    // colors:{
    //   amir:{
    //     10:'red',
    //     30:'blue'
    //   }
    // }
    fontFamily:{
      vazirRegular:['vazir'],
      vazirMedium:['vazir']
    }

  },
  plugins: [],
}

// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     "./index.html",
//     "./src/**/*.{js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [
//     // اینجا پلاگین مربوط به scrollbar رو اضافه می‌کنیم
//     require('tailwind-scrollbar')({ nocompatible: true }) // یا راه حل دستی
//   ],
// }

