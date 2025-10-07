import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        lime: '#A8E6CF',
        blush: '#FFB6C1',
        sky: '#89CFF0',
      },
    },
  },
  plugins: [],
};

export default config;
