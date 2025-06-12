/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Public Sans"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
                mono: ['"Fira Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
                serif: ['"Bitter"', 'ui-serif', 'system-ui', 'serif'],
                ui: ['"Lexend"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
            },
            fontSize: {
                'tiny': '0.75rem',   
            },    
            extend: {
                rotate: {
                    '225': '225deg',
                }
            }
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
