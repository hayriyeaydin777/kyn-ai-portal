/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				ink: '#26343d',
				paper: '#f4f6f5',
				teal: '#174b4d',
				coral: '#ff4d3d',
				line: '#d9e1df'
			}
		}
	},
	plugins: [require('tailwindcss-animate')]
};
