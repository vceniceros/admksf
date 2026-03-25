
export default {
  bootstrap: () => import('./main.server.mjs').then(m => m.default),
  inlineCriticalCss: true,
  baseHref: '/',
  locale: undefined,
  routes: [
  {
    "renderMode": 0,
    "preload": [
      "chunk-ZTETD75Z.js",
      "chunk-WWU4GDHV.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-2UMAGHI7.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/consorcios/nuevo"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-2UMAGHI7.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/consorcios/*/editar"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-AQ2HDRRQ.js",
      "chunk-NVVJVOXG.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-CCJV35WC.js",
      "chunk-W5VVCSR3.js",
      "chunk-AHGSYY2B.js"
    ],
    "route": "/dashboard/*/gastos"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-UYXYFXSQ.js",
      "chunk-WWU4GDHV.js",
      "chunk-W5VVCSR3.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/gastos/carga-de-gasto"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-UYXYFXSQ.js",
      "chunk-WWU4GDHV.js",
      "chunk-W5VVCSR3.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/gastos/*/editar"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-6FS55SKN.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/propietarios"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-Y6CQ7JJ6.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/unidades"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-RWZFHJKJ.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/proveedores"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-EZXUX3RM.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/saldos-mensuales"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-2STTNHR4.js",
      "chunk-NVVJVOXG.js",
      "chunk-AHGSYY2B.js"
    ],
    "route": "/dashboard/*/pagos"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-SSCPBIOC.js",
      "chunk-NVVJVOXG.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/pagos/carga-de-pago"
  },
  {
    "renderMode": 0,
    "preload": [
      "chunk-SSCPBIOC.js",
      "chunk-NVVJVOXG.js",
      "chunk-AHGSYY2B.js",
      "chunk-JZIT6UYD.js"
    ],
    "route": "/dashboard/*/pagos/*/editar"
  }
],
  entryPointToBrowserMapping: undefined,
  assets: {
    'index.csr.html': {size: 659, hash: '6f37c84fa3c37ceac9ece4d42bdaa305b7c99d05764a5f4dd5ef27aeb453ed95', text: () => import('./assets-chunks/index_csr_html.mjs').then(m => m.default)},
    'index.server.html': {size: 1030, hash: 'bd988a702419b97e4dadb1b26dd9369e7f4959025586a40894d886cbd6a34f3b', text: () => import('./assets-chunks/index_server_html.mjs').then(m => m.default)},
    'styles.css': {size: 26, hash: '4Rfk4i+aeU4', text: () => import('./assets-chunks/styles_css.mjs').then(m => m.default)}
  },
};
