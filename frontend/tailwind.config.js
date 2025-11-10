/** @type {import('tailwindcss').Config} */
import aspectRatio from '@tailwindcss/aspect-ratio';

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      // Add aspect ratio utilities
      aspectRatio: {
        '4/3': '4 / 3',
        '16/9': '16 / 9',
        '1/1': '1 / 1',
      },
    },
  },
  plugins: [
    aspectRatio,
  ],
}
